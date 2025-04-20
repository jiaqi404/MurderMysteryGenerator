import asyncio
import json
from websockets import connect

async def send_json_file():
    # Load the JSON file
    json_file_path = "./outputs/comfy/app.json"
    with open(json_file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)
        print(json_data)

    # 使用ws://或正确配置wss
    async with connect("ws://100.89.254.17:8188") as websocket:
        # Send the JSON data as a string
        await websocket.send(json.dumps(json_data))
        message = await websocket.recv()
        print(f"Received: {message}")

asyncio.run(send_json_file())