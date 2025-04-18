import gradio as gr
from PIL import Image
import io
import base64
import yaml

character_choices = ["Jeff", "Nakasuna", "Maya", "Elvin"]

# Dummy function to generate an image from text
def text_to_image(text):
    # Create a blank image with text (for demonstration purposes)
    img = Image.new('RGB', (512, 512), color=(255, 255, 255))
    return img

def update_selected_characters(selected):
    return ", ".join(selected)

def get_yaml_name(file):
    if file is None:
        return None
    with open(file.name, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('name')

def add_yaml_characters(file, character_options):
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

        **SketchModeling** is a method for 3D mesh generation from a sketch.

        It has three steps:
        1. It generates image from sketch using Stable Diffusion and ControlNet.
        2. It removes the background of the image using RMBG.
        3. It reconsturcted the 3D model of the image using InstantMesh.

        On below, you can either upload a sketch image or draw the sketch yourself. Then press Run and wait for the model to be generated.
        """)
    with gr.Tab("Tool"):
        with gr.Row():
            with gr.Column(variant="panel"):
                with gr.Row():
                    with gr.Column():
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
                        with gr.Tab("Character Settings"):
                            generated_img = gr.Image(
                                type="pil", label="Gnerated Image", image_mode="RGBA", interactive=False
                            )
                        with gr.Tab("Story Settings"):
                            processed_img = gr.Image(
                                type="pil", label="Processed Image", image_mode="RGBA", interactive=False
                            )
                # with gr.Row():
                #     prompt = gr.Textbox(label="Pompt", interactive=True)
                #     controlnet_conditioning_scale = gr.Slider(
                #         label="Controlnet Conditioning Scale",
                #         minimum=0.5,
                #         maximum=1.5,
                #         value=0.85,
                #         step=0.05,
                #         interactive=True
                #     )
                # with gr.Accordion('Advanced options', open=False):
                #     with gr.Row():
                #         negative_prompt = gr.Textbox(label="Negative Prompt", value="low quality, black and white image", interactive=True)
                #         add_prompt = gr.Textbox(label="Styles", value=", 3d rendered, shadeless, white background, intact and single object", interactive=True)
                #         num_inference_steps = gr.Number(label="Inference Steps", value=50, interactive=True)
                run_btn = gr.Button("Run", variant="primary")

            with gr.Column():
                with gr.Row():
                    with gr.Column():
                        sketch_img = gr.Image(
                                type="pil", label="Upload Image", sources="upload", image_mode="RGBA"
                            )
                        # with gr.Tab("Input Image", visible=False):
                        #     input_img = gr.Image(
                        #         type="pil", image_mode="RGBA", interactive=False, visible=False
                        #     )
                    with gr.Column():
                        sketch_img = gr.Image(
                                type="pil", label="Upload Image", sources="upload", image_mode="RGBA"
                            )
    with gr.Tab("Game"):
        text_input = gr.Textbox(label="Enter your text", placeholder="Type something...")
        image_output = gr.Image(label="Generated Image")

    run_btn.click(text_to_image, inputs=text_input, outputs=image_output)

demo.launch()