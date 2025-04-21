import asyncio
from websockets.server import serve
import json
from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper
import random

character_json_path = "./outputs/comfy/characters.json"
comfyui_workflow = "./ComfyUI Workflow/main_workflow.json"
character_img_path = "./outputs/characters"

def start_comfy(character_json, api: ComfyApiWrapper, comfyui_workflow):
    Background = character_json["background"]
    Weight_style = character_json["weight_style"]
    Weight_composition = character_json["weight_composition"]
    Start_at = character_json["start_at"]
    End_at = character_json["end_at"]
    Appearance_list = character_json["appearance"]
    character_num = len(Appearance_list)
    print("character_num:", character_num)

    for i in range(character_num):
        Appearance = Appearance_list[i]
        Appearance = "1person, solo, medium shot, masterpiece, best quality, intricate details, refined digital painting, " + Appearance
        print("Appearance:", Appearance)

        wf = ComfyWorkflowWrapper(comfyui_workflow)

        # Random seed within a large range
        random_seed = random.randint(1, 2**48 - 1)
        wf.set_node_param("KSampler", "seed", random_seed)

        # YAML appearance
        wf.set_node_param("Combine CLIP Text Encode (Positive)", "text", Appearance)
        wf.set_node_param("Customer Text Encode (Positive)", "text", Appearance)
        wf.set_node_param("Style CLIP Text Encode (Positive)", "text", "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, abstractionism, brush stroke, traditional media," + Appearance)

        # Background image generate
        wf.set_node_param("Background CLIP Text Encode (Positive)", "text", Background)

        # Style combination
        wf.set_node_param("IPAdapter Style & Composition SDXL", "weight_style", Weight_style)
        wf.set_node_param("IPAdapter Style & Composition SDXL", "weight_composition", Weight_composition)
        wf.set_node_param("IPAdapter Style & Composition SDXL", "start_at", Start_at)
        wf.set_node_param("IPAdapter Style & Composition SDXL", "end_at", End_at)

        # Generate images and wait for results
        result = api.queue_and_wait_images(wf, output_node_title="Image Detail Transfer")
        for filename, image_data in result.items():
            filepath = f"{character_img_path}/{filename}.png"
            with open(filepath, "wb+") as f:
                f.write(image_data)

async def handler(websocket):
    # await websocket.send("Connected!")
    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    async for message in websocket:
        print(f"Received: {message}")
        if message != None:
            # Save the received message to a JSON file
            with open(character_json_path, "w") as f:
                json.dump(json.loads(message), f, indent=4)

            # Load the character JSON file
            with open(character_json_path, "r") as f:
                character_json = json.load(f)

            # Start the ComfyUI workflow with the character JSON
            start_comfy(character_json, api, comfyui_workflow)

async def main():
    async with serve(handler, "0.0.0.0", 8188):  # 监听所有接口
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())