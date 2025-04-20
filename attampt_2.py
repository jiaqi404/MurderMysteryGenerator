from comfy_api_simplified import ComfyApiWrapper, ComfyWorkflowWrapper
import json
import random


character_json_path = "message.json"
character_img_path = "outputs/cards"

with open(character_json_path, "r") as f:
    character_json = json.load(f)

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
    print("Appearance:", Appearance)

    api = ComfyApiWrapper("http://127.0.0.1:8188/")
    # api = ComfyApiWrapper("https://smth.com/", user="user", password="password")

    wf = ComfyWorkflowWrapper("character_style_Combination.json")

    #Random seed within a large range
    random_seed = random.randint(1, 2**48 - 1)  
    wf.set_node_param("KSampler", "seed", random_seed) 

    #YAML appearence
    wf.set_node_param("Combine CLIP Text Encode (Positive)", "inputs", Appearance)
    wf.set_node_param("Customer Text Encode (Positive)", "inputs", Appearance)
    wf.set_node_param("Style CLIP Text Encode (Positive)", "inputs", "score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, abstractionism, brush stroke, traditional media,"+ Appearance)

    #Background image generate
    wf.set_node_param("Background CLIP Text Encode (Positive)", "inputs", Background)

    #Style combination
    wf.set_node_param("IPAdapter Style & Composition SDXL", "weight_style", Weight_style)
    wf.set_node_param("IPAdapter Style & Composition SDXL", "weight_composition", Weight_composition)
    wf.set_node_param("IPAdapter Style & Composition SDXL", "start_at", Start_at)
    wf.set_node_param("IPAdapter Style & Composition SDXL", "end_at", End_at)


    results = api.queue_and_wait_images(wf, output_node_title="Image Detail Transfer")
    for filename, image_data in results.items():
        filepath = f"{character_img_path}/{i}.png"
        with open(filepath, "wb+") as f:
            f.write(image_data)