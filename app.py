"""Main entrypoint for the app."""
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from utils import StreamingLLMCallbackHandler
from chat import get_chain
from schema import ChatResponse

app = FastAPI()

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    stream_handler = StreamingLLMCallbackHandler(websocket)
    chat_history = []
    agent_chain = get_chain(stream_handler)

    while True:
        try:
            # Receive and send back the client message
            question = await websocket.receive_text()
            resp = ChatResponse(sender="you", message=question, type="stream")
            await websocket.send_json(resp.dict())

            # Construct a response
            start_resp = ChatResponse(sender="bot", message="", type="start")
            await websocket.send_json(start_resp.dict())

            """
            result = agent_chain.run(
                {"question": question, "chat_history": chat_history}
            )
            chat_history.append((question, result))
            """

            # result = await agent_chain.arun(input=question)
            result = agent_chain.run(input=question)
            
            print(result)
            print("="*40)

            end_resp = ChatResponse(sender="bot", message="", type="end")
            await websocket.send_json(end_resp.dict())
        except WebSocketDisconnect:
            logging.info("websocket disconnect")
            break
        except Exception as e:
            logging.error(e)
            resp = ChatResponse(
                sender="bot",
                message="Sorry, something went wrong. Try again.",
                type="error",
            )
            await websocket.send_json(resp.dict())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9000)
