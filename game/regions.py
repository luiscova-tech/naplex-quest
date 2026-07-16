from dataclasses import dataclass


@dataclass
class Region:
    name: str
    description: str
    guardian: str


FOUNDATIONS_VILLAGE = Region(
    name="Foundations Village",
    description=(
        "A peaceful village where every great pharmacist begins their journey.\n\n"
        "Here you'll learn the foundations of pharmacology, calculations, "
        "drug information, and clinical reasoning."
    ),
    guardian="The Grand Pharmacist",
)