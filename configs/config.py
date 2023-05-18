'''
Description: 
Author: colin gao
Date: 2023-05-08 16:50:54
LastEditTime: 2023-05-18 14:10:10
'''
import os

VS_METHOD = "faiss" # faiss/pinecone/chroma

TEMPERTURE = 0

DOCS_ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

MAX_TOKENS_LIMIT = 2000

# 文本分句长度
SENTENCE_SIZE = 2000

# 匹配后单段上下文长度
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 0
