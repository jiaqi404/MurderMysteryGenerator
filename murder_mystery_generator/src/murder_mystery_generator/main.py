#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from murder_mystery_generator.crew import MurderMysteryGenerator
from murder_mystery_generator.character import Character

import yaml
from pathlib import Path

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


characters_path = Path(__file__).parent / "characters"
characters = []
for file in characters_path.rglob("*.yaml"):
    with open(file) as f:
        characters.append(Character(**yaml.safe_load(f)))

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


# def train():
#     """
#     Train the crew for a given number of iterations.
#     """
#     inputs = {
#         "topic": "AI LLMs"
#     }
#     try:
#         MurderMysteryGenerator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while training the crew: {e}")

# def replay():
#     """
#     Replay the crew execution from a specific task.
#     """
#     try:
#         MurderMysteryGenerator().crew().replay(task_id=sys.argv[1])

#     except Exception as e:
#         raise Exception(f"An error occurred while replaying the crew: {e}")

# def test():
#     """
#     Test the crew execution and returns the results.
#     """
#     inputs = {
#         "topic": "AI LLMs",
#         "current_year": str(datetime.now().year)
#     }
#     try:
#         MurderMysteryGenerator().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

#     except Exception as e:
#         raise Exception(f"An error occurred while testing the crew: {e}")
