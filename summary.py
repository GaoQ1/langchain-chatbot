'''
Description: 
Author: colin gao
Date: 2023-05-10 10:58:46
LastEditTime: 2023-05-10 16:48:58
'''
from colorama import init, Fore, Style
from langchain.document_loaders import TextLoader, DirectoryLoader
# from langchain.text_splitter import CharacterTextSplitter
from textsplitter import ChineseTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from templates import SUMMARY_PROMPT, REFINE_PROMPT

from configs.config import *

from dotenv import load_dotenv
load_dotenv()

init()

loader = DirectoryLoader(DOCS_ROOT_PATH, glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

text_splitter = ChineseTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=0
)
documents = text_splitter.split_documents(documents)

summary_prompt = PromptTemplate(template=SUMMARY_PROMPT, input_variables=["text"])
refine_prompt = PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=REFINE_PROMPT
)

chain = load_summarize_chain(
    ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0),
    chain_type="refine",
    question_prompt=summary_prompt,
    refine_prompt=refine_prompt
)
result = chain({"input_documents": documents[:3]}, return_only_outputs=True)

print(result)

