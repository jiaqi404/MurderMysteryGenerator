import gradio as gr
from PIL import Image
import yaml
import os
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import download_yaml, get_yaml_name
from src.murder_mystery_generator.main import run_crewai, generate_character_card_info

character_choices = ["Jeff", "Hiroharu Nakasuna", "Maya", "Elvin"]
card_frame_img_path = "ComfyUI Workflow/Card Design"

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

# ------------------ Gradio interface ------------------
with gr.Blocks() as demo:
    gr.Markdown("""
        # MurderMysteryGenerator

        **MurderMysteryGenerator** uses AI to generate murder mystery stories and characters. 
                
        It is a tool for writers, game developers, and anyone who wants to create engaging narratives.
        """)
    with gr.Tab("Tool"):
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
                                topic = gr.Textbox(label="Topic", value="Cyberpunk", interactive=True)
                                year = gr.Number(label="Year", value=2077, interactive=True)
                    with gr.Column():
                        gr.Markdown("### Character Generation Settings")
                        with gr.Accordion('Card Design', open=True):
                            character_bg = gr.Textbox(label="Background of Character Image", interactive=True, lines=2)
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
                                minimum=1,
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
                            embeds_scaling = gr.Textbox(
                                label="Embeds Scaling", value="K+V", interactive=True
                            )
                
                run_btn = gr.Button("Run", variant="primary")

            with gr.Column():
                gallery = gr.Gallery(label="Generated Cards", show_label=True, elem_id="gallery", columns=[4], object_fit="contain", height="auto")
                output_script = gr.Textbox(label="Output Script", interactive=False, lines=10)
    
    with gr.Tab("Game"):
        text_input = gr.Textbox(label="Enter your text", placeholder="Type something...")
        image_output = gr.Image(label="Generated Image")

    run_btn.click(
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
    )

demo.launch()