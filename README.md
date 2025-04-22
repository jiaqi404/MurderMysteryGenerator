# MurderMysteryGenerator

MurderMysteryGenerator is a powerful tool that leverages [crewAI](https://crewai.com) and [comfyUI](https://www.comfy.org/) to create engaging stories and characters for a Murder Mystery Game.

## Getting Started

To run MurderMysteryGenerator, you will need two computers: one for running crewAI and Gradio, and another for running comfyUI. These systems communicate with each other via websockets. Follow the steps below to set up and connect the components.

---

### Installation Instructions

#### For the Computer Running crewAI and Gradio:

1. Create and activate a Python environment:
    ```bash
    conda create -n myenv python<3.13
    conda activate myenv
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Install crewAI:
    ```bash
    crewai install
    ```

#### For the Computer Running comfyUI:

1. Use the provided workflow file `ComfyUI Workflow/main_workflow.json` for generation.

2. Download and install the following models:
    - [Stable Diffusion XL Base 1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/blob/main/sd_xl_base_1.0.safetensors)
    - [Pony Diffusion V6 XL](https://civitai.com/models/257749/pony-diffusion-v6-xl)
    - [Not Artists Styles for Pony Diffusion V6 XL](https://civitai.com/models/264290/styles-for-pony-diffusion-v6-xl-not-artists-styles)
    - [DreamShaper](https://civitai.com/models/4384/dreamshaper)
    - [epiCPhotoGasm](https://civitai.com/models/132632?modelVersionId=177124)

3. Install the following nodes via the Node Manager:
    - ComfyUI_IPAdapter_plus
    - ComfyUI-Inspyrenet-Rembg
    - ComfyUI Easy Use

4. Install five external models by searching "plus" in the Model Manager with the following criteria:
    - Type: IP-Adapter
    - Base: SDXL

    Models to install:
    - `ip-adapter-faceid-plusv2_sdxl.bin`
    - `ip-adapter_sdxl.safetensors`
    - `ip-adapter-plus_sdxl_vit-h.safetensors`
    - `ip-adapter-plus-face_sdxl_vit-h.safetensors`
    - `ip_plus_composition_sdxl.safetensors`

---

### Websocket Connection

To enable communication between the two computers, you can use any method of your choice. We recommend using the VPN service [tailscale](https://tailscale.com/). Tailscale creates a private network between the devices, allowing them to communicate via private IP addresses.

1. Set up the VPN and connect both computers.
2. Update the `host_ip` in the following files to match the private IP address of the comfyUI computer:
    - `src/websocket_comfy.py`
    - `src/murder_mystery_generator/utils/websocket_utils.py`

---

### Running the Application

#### On the Computer Running crewAI and Gradio:
Start the application by running:
```bash
python app.py
```

#### On the Computer Running comfyUI:
Navigate to the `src` directory and start the websocket server:
```bash
cd src
python websocket_comfy.py
```

---

### Using the Application

Once both systems are running, you can use the Gradio interface to interact with MurderMysteryGenerator! Follow these steps:

1. Use the Gradio interface to input your murder mystery game details.
2. Press the "Run" button to send a request to comfyUI for image generation.
3. Once the generation is complete, press the "Get Message" button to retrieve and display the generated images.

Enjoy creating your own murder mystery game with the help of AI!

---