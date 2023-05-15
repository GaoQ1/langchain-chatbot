'''
Description: 
Author: colin gao
Date: 2023-05-08 16:50:54
LastEditTime: 2023-05-14 17:13:59
'''
import os

STREAMING = False

INGEST = False

VS_METHOD = "chroma" # faiss/pinecone/chroma

TEMPERTURE = 0.3

VS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vector_store")

DOCS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

MAX_TOKENS_LIMIT = 2000

# 文本分句长度
SENTENCE_SIZE = 2000

# 匹配后单段上下文长度
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 0

# return top-k text chunk from vector store
VECTOR_SEARCH_TOP_K = 5
