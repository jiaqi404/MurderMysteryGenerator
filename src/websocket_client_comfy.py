import asyncio
import json
from websockets import connect
import os
import base64

async def send_images():
    # Load the image files
    image_file_path = "./outputs/characters"
    images_json = {'img':[]}  # List to store all image data

    for image_name in os.listdir(image_file_path):
        image_path = os.path.join(image_file_path, image_name)
        
        with open(image_path, "rb") as file:
            image_data = file.read()
            images_json['img'].append(base64.encodebytes(image_data).decode('utf-8'))

    # 使用ws://或正确配置wss
    async with connect("ws://100.119.199.109:8188") as websocket:
        # Send the JSON data as a string
        await websocket.send(json.dumps(images_json))
        message = await websocket.recv()
        print(f"Received: {message}")

asyncio.run(send_images())