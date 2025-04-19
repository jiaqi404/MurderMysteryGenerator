import gradio as gr
from PIL import Image
import yaml
import os
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import download_yaml, get_yaml_name
from src.murder_mystery_generator.main import run_crewai

character_choices = ["Jeff", "Hiroharu Nakasuna", "Maya", "Elvin"]

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

# Gradio interface
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
                        gr.Markdown("### Characters")
                        upload_yaml = gr.File(
                            label="Upload YAML File", file_types=[".yaml"]
                        )
                        character_options = gr.CheckboxGroup(
                            choices=character_choices,
                            label="Select Characters",
                            interactive=True
                        )
                        # selected_characters = gr.Textbox(
                        #     label="Selected Characters",
                        #     interactive=False
                        # )

                        upload_yaml.change(
                            add_yaml_characters,
                            inputs=[upload_yaml, character_options],
                            outputs=character_options
                        )
                        # character_options.change(
                        #     update_selected_characters,
                        #     inputs=character_options,
                        #     outputs=selected_characters
                        # )
                    with gr.Column():
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Story Settings")
                                topic = gr.Textbox(label="Topic", interactive=True)
                                year = gr.Number(label="Year", value=2025, interactive=True)
                        with gr.Row():
                            with gr.Column():
                                gr.Markdown("### Character Generation Settings")
                                card_bg = gr.Textbox(label="Background of Character Image", interactive=True, lines=2)
                                with gr.Accordion('Style Combination', open=True):
                                    with gr.Row():
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

    run_btn.click(run_crewai, inputs=[character_options, topic, year], outputs=output_script)

demo.launch()