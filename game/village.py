from dataclasses import dataclass


@dataclass
class Location:
    name: str
    icon: str
    description: str


FOUNDATIONS_LOCATIONS = [
    Location(
        name="Grand Pharmacist",
        icon="🧙",
        description="The wisest pharmacist in all of Pharmacia. He guides new apprentices."
    ),
    Location(
        name="Healer's Clinic",
        icon="🏥",
        description="Patients from across Pharmacia seek care here. Clinical reasoning will determine their fate."
    ),
    Location(
        name="Library",
        icon="📚",
        description="Ancient books and forgotten therapeutic knowledge."
    ),
    Location(
        name="Apothecary",
        icon="⚗️",
        description="A place where medicines, potions, and pharmaceutical wisdom are prepared."
    ),
    Location(
        name="Village Square",
        icon="🏛️",
        description="The heart of Foundations Village."
    ),
]