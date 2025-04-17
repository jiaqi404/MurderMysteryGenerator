#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from murder_mystery_generator.crew import MurderMysteryGenerator
from murder_mystery_generator.character import Character
import yaml
from pathlib import Path

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
    Run the crew.
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