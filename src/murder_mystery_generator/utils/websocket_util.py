import json
import yaml
from src.murder_mystery_generator.utils.yaml_utils import get_selected_characters_path
import asyncio
import json
from websockets import connect
import os

characters = {
    'background': '',
    'weight_style': 0,
    'weight_composition': 0,
    'start_at': 0,
    'end_at': 0,
    'appearance': []
}

characters_json_path = 'outputs/comfy/characters.json'
characters_root_path = 'src/murder_mystery_generator/characters'
characters_img_path = 'outputs/cards'

# ------------------ Gradio as a client ------------------
async def send_json_file():
    with open(characters_json_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    async with connect("ws://100.89.254.17:8188") as websocket:
        await websocket.send(json.dumps(json_data))
        message = await websocket.recv()

def write_characters_json(
    background: str,
    weight_style: float,
    weight_composition: float,
    start_at: float,
    end_at: float,
    character_names: list,
    ):
    characters['background'] = background
    characters['weight_style'] = weight_style
    characters['weight_composition'] = weight_composition
    characters['start_at'] = start_at
    characters['end_at'] = end_at

    character_files = get_selected_characters_path(character_names, characters_root_path)
    appearance = []
    for character_file in character_files:
        with open(character_file) as f:
            data = yaml.safe_load(f)
            appearance.append(data.get('appearance'))
    characters['appearance'] = appearance

    with open(characters_json_path, 'w') as f:
        json.dump(characters, f, indent=4)
    print(f"Characters JSON file written to {characters_json_path}")

    asyncio.run(send_json_file())
    print("Characters JSON file sent to server!")

# ------------------ Gradio as a host ------------------
# def save_websocket_images(message):
#     for filename, image_data in message.items():
#         with open(f"{characters_img_path}/{filename}", "wb+") as f:
#             f.write(image_data)

def show_comfy_images():
    images = [os.path.join(characters_img_path, file) for file in os.listdir(characters_img_path) if file.endswith('.png')]
    return tuple(images)


