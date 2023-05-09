'''
Description: 
Author: colin gao
Date: 2023-05-08 16:50:54
LastEditTime: 2023-05-09 18:43:12
'''
import os

STREAMING = False

INGEST = True

PINECONE = False

TEMPERTURE = 0.3

VS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")

DOCS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

# 文本分句长度
SENTENCE_SIZE = 100

# 匹配后单段上下文长度
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 20

# return top-k text chunk from vector store
VECTOR_SEARCH_TOP_K = 5
