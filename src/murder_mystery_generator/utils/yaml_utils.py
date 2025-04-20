import yaml
import os
from pathlib import Path
from src.murder_mystery_generator.character import Character

# download yaml files from gradio
def download_yaml(file, output_path):
    if file is not None:
        with open(f"{output_path}/{os.path.basename(file)}", "w") as output_file:
            with open(file.name, 'r') as input_file:
                input_yaml = yaml.safe_load(input_file)
                # Add lora_label in it
                input_yaml['lora_label'] = Path(file).stem
                # Save yaml
                yaml.dump(input_yaml, output_file)

# get "name" from yaml file
def get_yaml_name(file):
    if file is None:
        return None
    with open(file.name, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('name')

# gat all characters' path
def get_all_characters_path(characters_root_path):
    characters_path = []
    for file in Path(characters_root_path).rglob("*.yaml"):
        characters_path.append(file)
    return characters_path

# get selected characters' path
def get_selected_characters_path(character_names, characters_root_path):
    characters_path = get_all_characters_path(characters_root_path)
    selected_path = []
    for character_name in character_names:
        for character_path in characters_path:
            with open(character_path, 'r') as f:
                if get_yaml_name(f) == character_name:
                    selected_path.append(character_path)
    return selected_path

# format characters to Character class
def format_characters(characters_path):
    characters = []
    for character_path in characters_path:
        with open(character_path) as f:
            characters.append(Character(**yaml.safe_load(f)))
    return characters