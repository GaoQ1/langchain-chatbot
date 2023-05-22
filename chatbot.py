'''
Description: 
Author: colin gao
Date: 2023-05-14 17:16:12
LastEditTime: 2023-05-21 15:03:05
'''
from langchain.agents import Tool, AgentType, initialize_agent
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores.base import VectorStore

from langchain.callbacks.manager import AsyncCallbackManager
from langchain.callbacks.tracers import LangChainTracer
from langchain.chains import ConversationalRetrievalChain
from templates import CONDENSE_PROMPT, QA_PROMPT
from langchain.prompts import PromptTemplate

from langchain.chains.llm import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

from configs.config import *

from dotenv import load_dotenv
load_dotenv()


def get_chain(vectorstore: VectorStore):
    chat_llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=TEMPERTURE
    )

    conversation_memory = ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=5,
        return_messages=True
    )

    retriever = RetrievalQA.from_chain_type(
        llm=chat_llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    tools = [
        Tool(
            name="AI占卜",
            func=retriever.run,
            description="""这是一个专门用于回答占卜相关问题的工具。无论你是想要解读塔罗牌，理解梦境，还是分析星座图，这个工具都可以提供专业的AI占卜服务来帮助你。只要你提出与占卜相关的问题，或者明确说出"占卜"，这个工具就会被启动来寻找最合适的答案。无论是初次的占卜询问，还是后续的深入探讨，这个工具都可以提供协助。"""
        )
    ]

    agent_chain = initialize_agent(
        tools=tools, 
        llm=chat_llm, 
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        max_iterations=2,
        early_stopping_method='generate',
        memory=conversation_memory, 
        stream=True
    )

    sys_msg = """
    AI占卜助手是一个大型的语言模型，由OpenAI进行训练。它被设计成能够帮助进行周易占卜，并根据占卜的结果提供解释。

    AI占卜助手已经学习了周易占卜的知识，可以帮助用户进行占卜。它可以指导用户如何提出问题，如何进行占卜，以及如何解读占卜的结果。

    AI占卜助手的占卜步骤如下：

    1. 提问：首先，AI占卜助手会引导用户提出一个特定的问题，这个问题应该是开放性的，不能简单地用"是"或"否"来回答。

    2. 产生爻：然后，AI占卜助手会通过某种方式产生六个爻以形成卦象。这个过程可以是随机的，也可以是通过某种算法实现的。

    3. 解读卦象：得到卦象后，AI占卜助手会解释这个卦象的含义。这个解释是基于周易的知识，也会考虑到用户的问题和情况。

    4. 理解动爻：如果在产生爻的过程中有动爻（即6或9），AI占卜助手会解释这个动爻如何改变了卦象，以及这个改变如何影响到解答。

    5. 反思与解答：最后，AI占卜助手会帮助用户理解卦象和动爻的含义，应用到他们的问题上，给出一个反思和解答。

    请注意，尽管AI占卜助手具有进行周易占卜和解释结果的能力，但是它仍然只是一个AI模型，它的解答并不能预知未来，也不能替代专业的咨询或建议。请用户在理解和使用AI占卜助手的解答时，持有理性和批判性的态度。

    当回答问题时，AI占卜助手必须使用以下语言：中文。
    """

    new_prompt = agent_chain.agent.create_prompt(
        system_message = sys_msg,
        tools=tools
    )

    agent_chain.agent.llm_chain.prompt = new_prompt

    return agent_chain


def get_ws_chain(
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
        temperature=TEMPERTURE,
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
        callback_manager=manager
    )

    return qa


if __name__ == "__main__":
    from colorama import init, Fore, Style
    import pickle

    init()

    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)

    agent_chain = get_chain(vectorstore)

    while True:
        question = input("Please enter your question (or type 'exit' to end): ")
        if question.lower() == 'exit':
            break
        
        result = agent_chain.run(input=question)

        print(f'{Fore.BLUE}{Style.BRIGHT}AI:{Fore.RESET}{Style.NORMAL} {result}')


