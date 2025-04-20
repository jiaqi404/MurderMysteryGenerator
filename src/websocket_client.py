import asyncio
from websockets import connect

async def hello():
    # 使用ws://或正确配置wss
    async with connect("ws://100.89.254.17:8188") as websocket:
        await websocket.send("Hello world!")
        message = await websocket.recv()
        print(f"Received: {message}")

asyncio.run(hello())