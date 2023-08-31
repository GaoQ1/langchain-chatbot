'''
Description: 
Author: colin gao
Date: 2023-05-26 17:54:39
LastEditTime: 2023-05-26 23:06:42
'''
import sys
sys.path.append("..")

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback

from configs.config import *
from .log import logger

def load_tools(vectorstore):
    def searchVector(key_word):
        chat_llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=TEMPERTURE
        )

        retriever = RetrievalQA.from_chain_type(
            llm=chat_llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            return_source_documents=False
        )
        
        result = retriever.run(key_word)
        
        return result

    dict_tools = {
        'Vector Search': searchVector
    }
    return dict_tools


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        logger.info(f'Spent a total of {cb.total_tokens} tokens')

    return result

import requests
def test_youtube_access(in_logger=''):
    logger = print if not in_logger else in_logger.info
    url = "https://www.youtube.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            logger("成功访问YouTube")
            return True
        else:
            logger(f"访问YouTube失败，状态码：{response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger(f"访问YouTube时出现异常: {e}")
        return False
