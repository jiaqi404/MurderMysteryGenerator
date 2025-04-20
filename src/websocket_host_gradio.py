import asyncio
from websockets.server import serve
import json
from base64 import b64decode

output_file = "outputs/cards"
count = 0

def json_to_png(json_data, output_file):
    img_bytes = b64decode(json_data)
    with open(output_file, "wb") as f:
        f.write(img_bytes)

async def handler(websocket):
    global count
    await websocket.send("Connected!")
    async for message in websocket:
        message_json = json.loads(message)
        img_json = message_json.get("img")
        print(len(img_json))
        for img in img_json:
            json_to_png(img, f"{output_file}/{count}.png")
            count += 1
            print(count)

async def main():
    async with serve(handler, "0.0.0.0", 8188, max_size=10 * 1024 * 1024):  # 设置最大消息大小为10MB
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())