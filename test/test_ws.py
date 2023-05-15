'''
Description: 
Author: colin gao
Date: 2023-05-15 21:51:12
LastEditTime: 2023-05-15 22:11:53
'''
import asyncio
import websockets
import json

async def test_websocket():
    async with websockets.connect("ws://127.0.0.1:9000/chat") as websocket:
        query = "你好"
        await websocket.send(query)

        while True:
            try:
                response = await websocket.recv()
                print(response)
            except websockets.exceptions.ConnectionClosedOK:
                break

asyncio.run(test_websocket())
