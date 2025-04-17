from pydantic import BaseModel

class Character(BaseModel):
    name: str
    age: int
    personality: str
    appearance: str
    backstory: str

    # Set description to be all the character's attributes
    @property
    def description(self):
        return f"Name: {self.name}\nAge: {self.age}\nPersonality: {self.personality}\nAppearance: {self.appearance}\nBackstory: {self.backstory}"