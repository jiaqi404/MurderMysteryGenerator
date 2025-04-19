import yaml
import os
from pathlib import Path
from src.murder_mystery_generator.character import Character

def download_yaml(file, output_path):
    if file is not None:
        with open(f"{output_path}/{os.path.basename(file)}", "w") as output_file:
            with open(file.name, 'r') as input_file:
                input_yaml = yaml.safe_load(input_file)
                # Add lora_label in it
                input_yaml['lora_label'] = Path(file).stem
                # Save yaml
                yaml.dump(input_yaml, output_file)

def get_yaml_name(file):
    if file is None:
        return None
    with open(file.name, 'r') as f:
        data = yaml.safe_load(f)
    return data.get('name')

def get_all_characters(characters_path):
    characters = []
    for file in Path(characters_path).rglob("*.yaml"):
        with open(file) as f:
            characters.append(f)
    return characters

def get_selected_characters(character_names, characters_path):
    character_yaml_files = get_all_characters(characters_path)
    selected_yaml_files = []
    for character_name in character_names:
        for character_yaml_file in character_yaml_files:
            if get_yaml_name(character_yaml_file) == character_name:
                selected_yaml_files.append(character_yaml_file)
    
    return selected_yaml_files

def format_characters(character_yaml_files):
    characters = []
    for character_yaml_file in character_yaml_files:
        print(yaml.safe_load(character_yaml_file))
        characters.append(Character(**yaml.safe_load(character_yaml_file)))
    return characters

# format_characters(get_selected_characters(['Lyra', 'Elvin'], "C:\\Users\\sdit\\Documents\\GitHub\\murder_mystery_generator\\src\\murder_mystery_generator\\characters"))
