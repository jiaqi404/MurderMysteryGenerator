#!/usr/bin/env python
import warnings
from src.murder_mystery_generator.crew import MurderMysteryGenerator
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import get_selected_characters_path, format_characters
from src.murder_mystery_generator.utils.card_utils import get_content, generate_card_info
import os

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

characters_path = Path(__file__).parent / "characters"
output_path = 'outputs/murder_case_outline.md'

character_md_path = "outputs/characters.md"
card_output_path = "outputs/cards"

def generate_character_card_info(
        character_names,
        card_frame_path
    ):
    for character_name in character_names:
        img_path = os.path.join(card_output_path, f"{character_name}.png")

        print("Generating card of "+character_name+"...")
        generate_card_info(
            image_path=card_frame_path,
            output_path=img_path,
            title=character_name,
            subtitle=get_content(character_md_path, character_name, "Occupation"),
            text=get_content(character_md_path, character_name, "Background")
        )

# ------------------ Main function ------------------ 
def run_crewai(character_names, topic, year):
    character_files = get_selected_characters_path(character_names, characters_path)
    characters = format_characters(character_files)
    inputs = {
        "characters": "\n".join([character.description for character in characters]),
        'topic': topic,
        'year': year,
        'character_amount': len(characters),
    }
    
    try:
        MurderMysteryGenerator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    
    with open(output_path, 'r', encoding='utf-8') as file:
        return file.read()