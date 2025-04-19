#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from src.murder_mystery_generator.crew import MurderMysteryGenerator
from src.murder_mystery_generator.character import Character
import yaml
from pathlib import Path
from src.murder_mystery_generator.utils.yaml_utils import get_selected_characters, format_characters

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# ------------------ Load characters ------------------
characters_path = Path(__file__).parent / "characters"
characters = []
for file in characters_path.rglob("*.yaml"):
    with open(file) as f:
        characters.append(Character(**yaml.safe_load(f)))

# ------------------ Main function ------------------
def run():
    """
    Run the crew with `crewai run`
    """
    inputs = {
        "characters": "\n".join([character.description for character in characters]),
        'topic': 'Cyberpunk',
        'year': 2077,
        'character_amount': len(characters),
        # 'year': str(datetime.now().year)
    }
    
    try:
        MurderMysteryGenerator().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

# ------------------ Main function for gradio ------------------ 
def run_crewai(character_names, topic, year):
    character_files = get_selected_characters(character_names, characters_path)
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