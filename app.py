'''
Description: 
Author: colin gao
Date: 2023-05-17 15:54:12
LastEditTime: 2023-05-26 23:05:56
'''
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from schema import ChatItem
from chatbot import get_chain

from utils import logger

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

conversation_chat = get_chain()

@app.post("/chat", summary="chat接口", description="该接口为chat的接口")
def chat(item: ChatItem):
    question = item.text
    result = conversation_chat(question)

    logger.info(f"chat result is {result['response']}")

    return {
        "result": result['response']
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
