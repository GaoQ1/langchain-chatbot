'''
Description: 
Author: colin gao
Date: 2023-05-10 14:12:34
LastEditTime: 2023-05-16 17:01:24
'''
import os, datetime
import pickle

from configs.config import *
from langchain.vectorstores import Chroma
from langchain.vectorstores.faiss import FAISS

def ingest(documents, embeddings):
    if VS_METHOD == "chroma":
        if INGEST:
            vector_store = Chroma.from_documents(
                documents, 
                embeddings, 
                collection_name="my_collection_chroma",
                persist_directory=VS_ROOT_PATH
            )
        else:
            vector_store = Chroma(
                persist_directory=VS_ROOT_PATH,
                embedding_function=embeddings,
                collection_name="my_collection_chroma"
            )

    elif VS_METHOD == "faiss":
        vs_path = os.path.join(VS_ROOT_PATH, "my_collection_faiss")
        if INGEST:
            vector_store = FAISS.from_documents(documents, embeddings)
            vector_store.save_local(vs_path)
        else:
            vector_store = FAISS.load_local(vs_path, embeddings)

    return vector_store

