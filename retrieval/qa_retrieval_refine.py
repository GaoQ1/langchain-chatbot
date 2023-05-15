'''
Description: 
Author: colin gao
Date: 2023-05-05 13:32:05
LastEditTime: 2023-05-11 18:09:11
'''
from colorama import init, Fore, Style

from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from textsplitter import ChineseTextSplitter
from langchain.prompts import PromptTemplate
from langchain import OpenAI
from langchain.chains.question_answering import load_qa_chain


from configs.config import *
from templates import QA_REFINE_PROMPT, REFINE_PROMPT
from utils import ingest

from dotenv import load_dotenv
load_dotenv()

init()

loader = DirectoryLoader(DOCS_ROOT_PATH, glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

text_splitter = ChineseTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

documents = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

vector_store = ingest(documents, embeddings)

qa_prompt_template = PromptTemplate(input_variables=["context_str", "question"], template= QA_REFINE_PROMPT)

refine_prompt_template = PromptTemplate(input_variables=["existing_answer", "question"], template=REFINE_PROMPT)

llm_model = OpenAI(
    model_name='gpt-3.5-turbo', 
    temperature=TEMPERTURE,
    streaming=STREAMING)

qa_chain = load_qa_chain(
    llm=llm_model, 
    chain_type="refine", 
    question_prompt=qa_prompt_template,
    refine_prompt=refine_prompt_template,
    verbose=True
)

while True:
    question = input("Please enter your question (or type 'exit' to end): ")
    if question.lower() == 'exit':
        break

    docs = vector_store.similarity_search(question, k=3)

    result = qa_chain.run(
        input_documents=docs, 
        question=question
    )

    print(f'{Fore.BLUE}{Style.BRIGHT}AI:{Fore.RESET}{Style.NORMAL} {result}')
