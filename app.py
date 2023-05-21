'''
Description: 
Author: colin gao
Date: 2023-05-17 15:54:12
LastEditTime: 2023-05-21 14:21:19
'''
import pickle
from pathlib import Path
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from utils import StreamingLLMCallbackHandler, QuestionGenCallbackHandler

from langchain.vectorstores import VectorStore
from schema import ChatItem, ChatResponse

from chatbot import get_chain, get_ws_chain
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


@app.websocket("/chat_ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    question_handler = QuestionGenCallbackHandler(websocket)
    stream_handler = StreamingLLMCallbackHandler(websocket)
    chat_history = []
    qa_chain = get_ws_chain(vectorstore, question_handler, stream_handler)

    while True:
        try:
            # Receive and send back the client message
            question = await websocket.receive_text()
            resp = ChatResponse(sender="you", message=question, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            result = await qa_chain.acall(
                {"question": question, "chat_history": chat_history}
            )
            chat_history.append((question, result["answer"]))

            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logger.info("websocket disconnect")
            break
        except Exception as e:
            logger.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
