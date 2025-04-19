#!/usr/bin/env python
import warnings
from src.murder_mystery_generator.crew import MurderMysteryGenerator
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import get_selected_characters_path, format_characters

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

characters_path = Path(__file__).parent / "characters"
output_path = 'outputs/murder_case_outline.md'

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