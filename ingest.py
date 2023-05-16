'''
Description: 
Author: colin gao
Date: 2023-05-10 14:12:34
LastEditTime: 2023-05-16 15:04:47
'''
import pickle

from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from textsplitter import ChineseTextSplitter
from langchain.vectorstores.faiss import FAISS
from configs.config import *

from dotenv import load_dotenv
load_dotenv()

def ingest():
    loader = DirectoryLoader(DOCS_ROOT_PATH, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    text_splitter = ChineseTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    documents = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')

    vector_store = FAISS.from_documents(documents, embeddings)

    # Save vectorstore
    with open("vectorstore.pkl", "wb") as f:
        pickle.dump(vector_store, f)

if __name__ == "__main__":
    ingest()