from dataclasses import dataclass


@dataclass
class Dialogue:
    speaker: str
    text: str


INTRO_DIALOGUE = [
    Dialogue(
        speaker="Grand Pharmacist",
        text=(
            "Welcome, Apprentice Pharmacist.\n\n"
            "The Book of Therapeutics has been shattered.\n"
            "Its chapters have scattered across the Kingdom of Pharmacia.\n\n"
            "Without that knowledge, medication errors are increasing "
            "and the Shadow Alchemist grows stronger."
        ),
    ),
    Dialogue(
        speaker="Grand Pharmacist",
        text=(
            "Your journey begins in Foundations Village.\n\n"
            "Recover the lost knowledge.\n"
            "Help the people of Pharmacia.\n"
            "Master every therapeutic region.\n\n"
            "Only then may you enter the NAPLEX Temple."
        ),
    ),
]