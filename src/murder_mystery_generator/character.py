from pydantic import BaseModel

# ------------------ Formatting character string ------------------
class Character(BaseModel):
    name: str
    age: int
    personality: str
    appearance: str
    backstory: str

    @property
    def description(self):
        return f"Name: {self.name}\nAge: {self.age}\nPersonality: {self.personality}\nAppearance: {self.appearance}\nBackstory: {self.backstory}"