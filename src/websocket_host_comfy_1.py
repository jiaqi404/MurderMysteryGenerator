import asyncio
from websockets.server import serve
import json
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper


# message = None
character_json_path = "message.json"  # 角色信息的JSON文件路径

async def handler(websocket):
    await websocket.send("Connected!")
    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    async for message in websocket:
        print(f"Received: {message}")
        if message != None:
            message_json = json.loads(message)
            with open(character_json_path, "w") as f:
                json.dump(message_json, f, indent=4) 
                
                wf = ComfyWorkflowWrapper("message.json") 
                results = api.queue_and_wait_images(wf, "Save Image")
                for filename, image_data in results.items():
                    with open(f"{filename}", "wb+") as f:
                        f.write(image_data)  


        await websocket.send(f"Echo: {message}")


  

# ---------------------------------------------------

# ================== 新增功能代码 ==================
# async def trigger_comfyui_workflow():
#     """自动触发ComfyUI工作流（新增函数）"""

#     try:
#         # 读取保存的message.json
#         with open("message.json", "r", encoding="utf-8") as f:
#             workflow = json.load(f)


#         # 提交到ComfyUI
#         async with aiohttp.ClientSession() as session:
#             print("正在提交工作流到ComfyUI...")
#             async with session.post(
#                 "http://127.0.0.1:8188/prompt",  
#                 json={"prompt": workflow}
#             ) as response:
#                 if response.status == 200:
#                     print("工作流已成功提交至ComfyUI")
#                 else:
#                     print(f"提交失败: {await response.text()}")


#     except Exception as e:
#         print(f"工作流触发异常: {str(e)}")


# async def modified_handler(websocket):
#     """包装原有handler以添加新功能"""
#     # 调用原有处理逻辑
#     await handler(websocket)
#     # 在消息处理后自动触发工作流
#     await trigger_comfyui_workflow()


async def main():
    async with serve(handler, "0.0.0.0", 8188):  # 监听所有接口
        await asyncio.Future()
# ================================================

if __name__ == "__main__":
    asyncio.run(main())