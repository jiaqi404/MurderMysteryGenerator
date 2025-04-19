#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from src.murder_mystery_generator.crew import MurderMysteryGenerator
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import get_all_characters_path, get_selected_characters_path, format_characters

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ------------------ Main function for test ------------------
# characters_path = Path(__file__).parent / "characters"
# characters = format_characters(get_all_characters_path(characters_path))

# def run():
#     """
#     Run the crew with `crewai run`
#     """
#     inputs = {
#         "characters": "\n".join([character.description for character in characters]),
#         'topic': 'Cyberpunk',
#         'year': 2077,
#         'character_amount': len(characters),
#         # 'year': str(datetime.now().year)
#     }
    
#     try:
#         MurderMysteryGenerator().crew().kickoff(inputs=inputs)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")

# ------------------ Main function ------------------ 
characters_path = Path(__file__).parent / "characters"
output_path = 'outputs/murder_case_outline.md'

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