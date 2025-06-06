import gradio as gr
from PIL import Image
import yaml
import os
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import download_yaml, get_yaml_name
from src.murder_mystery_generator.main import run_crewai, generate_character_card_info
from src.murder_mystery_generator.utils.websocket_utils import write_characters_json, show_comfy_images, json_to_png
from src.murder_mystery_generator.utils.card_utils import remove_files_in_directory
import asyncio
from websockets.server import serve
import json
import threading
import time
from queue import Queue

character_choices = ["Jeff", "Hiroharu Nakasuna", "Maya", "Elvin"]
card_frame_img_path = "ComfyUI Workflow/Card Design"
output_file = "outputs/cards"
count = 0

def update_selected_characters(selected):
    return ", ".join(selected)

def add_yaml_characters(file, character_options):
    download_yaml(file, "src/murder_mystery_generator/characters")
    character_name = get_yaml_name(file)
    if character_name is not None and character_name not in character_choices:
        character_choices.append(character_name)
        return gr.CheckboxGroup(choices=character_choices)
    else:
        return character_options
    
def update_card_frame_image(selected_frame):
    selected_card_frame_path = os.path.join(card_frame_img_path, f"{selected_frame}.png")
    if os.path.exists(selected_card_frame_path):
        return Image.open(selected_card_frame_path)
    else:
        return None
    
def update_card_frame_path(selected_frame):
    selected_card_frame_path = os.path.join(card_frame_img_path, f"{selected_frame}.png")
    if os.path.exists(selected_card_frame_path):
        return selected_card_frame_path
    else:
        return None

async def handler(websocket):
    global count
    await websocket.send("Connected!")
    async for message in websocket:
        message_json = json.loads(message)
        img_json = message_json.get("img")
        print("Received images!")
        for img in img_json:
            json_to_png(img, f"{output_file}/{count}.png")
            count += 1
            print(f"Processed {count} images. Latest image saved at: {output_file}/{count - 1}.png")

async def main():
    print("Host open!")
    async with serve(handler, "0.0.0.0", 8188, max_size=10 * 1024 * 1024): # max message size 10MB
        await asyncio.Future()

# ------------------ Gradio interface ------------------
with gr.Blocks() as demo:
    gr.Markdown("""
        # MurderMysteryGenerator

        **MurderMysteryGenerator** leverages [crewAI](https://crewai.com) and [comfyUI](https://www.comfy.org/) to create engaging stories and characters for a Murder Mystery Game.
                
        **To run MurderMysteryGenerator, you will need two computers: one for running crewAI and Gradio, and another for running comfyUI.** These systems communicate with each other via websockets. Make Sure two computers are running before you press "Run".

        """)
    with gr.Row():
        with gr.Column(variant="panel"):
            with gr.Row():
                with gr.Column():
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Characters")
                            upload_yaml = gr.File(
                                label="Upload YAML File", file_types=[".yaml"]
                            )
                            character_options = gr.CheckboxGroup(
                                choices=character_choices,
                                label="Select Characters",
                                interactive=True
                            )
                            upload_yaml.change(
                                add_yaml_characters,
                                inputs=[upload_yaml, character_options],
                                outputs=character_options
                            )
                    with gr.Row():
                        with gr.Column():
                            gr.Markdown("### Story Settings")
                            topic = gr.Textbox(label="Topic", value="Magic World", interactive=True)
                            year = gr.Number(label="Year", value=1999, interactive=True)
                with gr.Column():
                    gr.Markdown("### Character Generation Settings")
                    with gr.Accordion('Card Design', open=True):
                        character_bg = gr.Textbox(label="Background of Character Image", interactive=True, lines=2, value='a castle in the sunset')
                        card_frame = gr.Dropdown(
                            label="Card Frame", 
                            choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], 
                            value=None, 
                            interactive=True
                        )
                        font_color = gr.ColorPicker(
                            label="Font Color", 
                            value="#FFFFFF", 
                            interactive=True
                        )
                        card_frame_img = gr.Image(
                            label="Card Frame", 
                            type="pil", 
                            interactive=False
                        )
                        card_frame_img_path_text = gr.Textbox(
                            label="Card Frame Image Path", 
                            interactive=False,
                            visible=False
                        )
                        card_frame.change(
                            update_card_frame_image, 
                            inputs=[card_frame], 
                            outputs=card_frame_img
                        )
                        card_frame.change(
                            update_card_frame_path,
                            inputs=[card_frame],
                            outputs=card_frame_img_path_text
                        )
                    with gr.Accordion('Style Combination', open=False):
                        weight_style = gr.Slider(
                            label="Weight Style",
                            minimum=0.5,
                            maximum=2,
                            value=1.5,
                            step=0.05,
                            interactive=True
                        )
                        weight_composition = gr.Slider(
                            label="Weight Compostion",
                            minimum=0.5,
                            maximum=1,
                            value=0.75,
                            step=0.05,
                            interactive=True
                        )
                        start_at = gr.Number(
                            label="Start At", value=0, interactive=True
                        )
                        end_at = gr.Number(
                            label="End At", value=1, interactive=True
                        )
            
            run_btn = gr.Button("Run", variant="primary")

        with gr.Column():
            gallery = gr.Gallery(label="Generated Cards", show_label=True, elem_id="gallery", columns=[4], object_fit="contain", height="auto", type="filepath")
            output_script = gr.Textbox(label="Output Script", interactive=False, lines=10)
            get_message_btn = gr.Button("Get Message")

    # ------------------ Main functions ------------------
    run_btn.click(
        remove_files_in_directory
    ).success(
        run_crewai, 
        inputs=[character_options, topic, year], 
        outputs=output_script
    ).success(
        generate_character_card_info,
        inputs=[
            character_options,
            card_frame_img_path_text,
            font_color
        ]
    ).success(
        write_characters_json,
        inputs=[
            character_bg,
            weight_style,
            weight_composition,
            start_at,
            end_at,
            character_options
        ]
    )

    get_message_btn.click(
        show_comfy_images,
        outputs=gallery
    )

def run_gradio():
    demo.launch()

def run_async():
    asyncio.run(main())

if __name__ == "__main__":
    t1 = threading.Thread(target=run_gradio)
    t1.daemon = True
    t2 = threading.Thread(target=run_async)
    t2.daemon = True
    
    t1.start()
    t2.start()

    while True:
        time.sleep(1)