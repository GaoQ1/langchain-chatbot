'''
Description: 
Author: colin gao
Date: 2023-05-07 22:11:25
LastEditTime: 2023-05-16 17:44:52
'''
"""Create a ConversationalRetrievalChain for question/answering."""
from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationalRetrievalChain
from templates import CONDENSE_PROMPT, QA_PROMPT
from langchain.prompts import PromptTemplate

from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.vectorstores.base import VectorStore

from dotenv import load_dotenv
load_dotenv()

import code

def get_chain(
    vectorstore: VectorStore, question_handler, stream_handler, tracing: bool = False
) -> ConversationalRetrievalChain:
    manager = AsyncCallbackManager([])
    question_manager = AsyncCallbackManager([question_handler])
    stream_manager = AsyncCallbackManager([stream_handler])
    
    if tracing:
        tracer = LangChainTracer()
        tracer.load_default_session()
        manager.add_handler(tracer)
        question_manager.add_handler(tracer)
        stream_manager.add_handler(tracer)

    question_gen_llm = OpenAI(
        temperature=0,
        verbose=True,
        callback_manager=question_manager,
    )
    streaming_llm = OpenAI(
        streaming=True,
        callback_manager=stream_manager,
        verbose=True,
        temperature=0,
    )

    CONDENSE_TEMPLATE = PromptTemplate(input_variables=["chat_history", "question"], template=CONDENSE_PROMPT)
    QA_TEMPLATE = PromptTemplate(input_variables=["context", "question"], template=QA_PROMPT)

    question_generator = LLMChain(
        llm=question_gen_llm, 
        prompt=CONDENSE_TEMPLATE,
        callback_manager=manager
    )
    
    doc_chain = load_qa_chain(
        streaming_llm, chain_type="stuff", prompt=QA_TEMPLATE, callback_manager=manager
    )

    qa = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=doc_chain,
        question_generator=question_generator,
        callback_manager=manager,
    )

    return qa

if __name__ == "__main__":
    from configs.config import *
    import pickle

    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

    qa_chain = get_chain(vectorstore, [], [])

    # result = qa({'question': question, 'chat_history': chat_history})

    result = qa_chain(
        {"question": "这篇文章主要讲的是什么？", "chat_history": []}
    )

    print(result)

