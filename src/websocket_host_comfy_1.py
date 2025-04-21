import asyncio
from websockets.server import serve
import json
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper


# message = None
character_json_path = "./outputs/comfy/characters.json"  # 角色信息的JSON文件路径

async def handler(websocket):
    await websocket.send("Connected!")
    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    async for message in websocket:
        print(f"Received: {message}")
        if message != None:
            message_json = json.loads(message)
            with open(character_json_path, "w") as f:
                json.dump(message_json, f, indent=4) 
                
                # wf = ComfyWorkflowWrapper("message.json") 
                # results = api.queue_and_wait_images(wf, "Save Image")
                # for filename, image_data in results.items():
                #     with open(f"{filename}", "wb+") as f:
                #         f.write(image_data)  


        await websocket.send(f"Echo: {message}")

async def main():
    async with serve(handler, "0.0.0.0", 8188):  # 监听所有接口
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())