import asyncio
from websockets.server import serve

async def handler(websocket):
    await websocket.send("Connected!")
    async for message in websocket:
        print(f"Received: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    async with serve(handler, "0.0.0.0", 8188):  # 监听所有接口
        await asyncio.Future()

asyncio.run(main())