'''
Description: 
Author: colin gao
Date: 2023-05-17 15:54:12
LastEditTime: 2023-05-18 18:37:20
'''
import pickle
from pathlib import Path
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from langchain.vectorstores import VectorStore
from schema import ChatItem

from chat_agent import get_chain
from utils import logger

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

vectorstore: Optional[VectorStore] = None

@app.on_event("startup")
def startup_event():
    logger.info("loading vectorstore")
    if not Path("vectorstore.pkl").exists():
        raise ValueError("vectorstore.pkl does not exist, please run ingest.py first")
    with open("vectorstore.pkl", "rb") as f:
        vectorstore = pickle.load(f)
    
    global agent_chain
    agent_chain = get_chain(vectorstore)


@app.post("/chat", summary="chat接口", description="该接口为chat的接口")
def chat(item: ChatItem):
    question, chat_history = item.text, item.history
    result = agent_chain.run(input=question)

    logger.info(f"chat result is {result}")

    return {
        "result": result
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
