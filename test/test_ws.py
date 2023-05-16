'''
Description: 
Author: colin gao
Date: 2023-05-15 21:51:12
LastEditTime: 2023-05-16 17:53:12
'''
import asyncio
import websockets
import json

import code

async def test_websocket():
    async with websockets.connect("ws://127.0.0.1:9000/chat") as websocket:
        query = "这篇文章主要讲的是什么？"
        await websocket.send(query)

        while True:
            try:
                response = await websocket.recv()
                print(response)
            except websockets.exceptions.ConnectionClosedOK:
                break

asyncio.run(test_websocket())
