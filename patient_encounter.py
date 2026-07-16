from dataclasses import dataclass
from enum import Enum, auto


class EncounterStage(Enum):
    INTRODUCTION = auto()
    HISTORY = auto()
    ASSESSMENT = auto()
    TREATMENT = auto()
    OUTCOME = auto()
    COMPLETE = auto()


@dataclass
class PatientEncounter:
    encounter_id: str
    patient_name: str
    chief_complaint: str
    reward_xp: int = 25
    reward_gold: int = 10
    current_stage: EncounterStage = EncounterStage.INTRODUCTION
    completed: bool = False

    def advance_stage(self):
        if self.current_stage == EncounterStage.INTRODUCTION:
            self.current_stage = EncounterStage.HISTORY

        elif self.current_stage == EncounterStage.HISTORY:
            self.current_stage = EncounterStage.ASSESSMENT

        elif self.current_stage == EncounterStage.ASSESSMENT:
            self.current_stage = EncounterStage.TREATMENT

        elif self.current_stage == EncounterStage.TREATMENT:
            self.current_stage = EncounterStage.OUTCOME

        elif self.current_stage == EncounterStage.OUTCOME:
            self.current_stage = EncounterStage.COMPLETE
            self.completed = True

    def reset(self):
        self.current_stage = EncounterStage.INTRODUCTION
        self.completed = False

    def is_complete(self) -> bool:
        return self.completed

    def get_stage_text(self) -> str:
        """Returns narrative text for the current encounter stage."""

        if self.current_stage == EncounterStage.INTRODUCTION:
            return (
                "A worried traveler enters the clinic.\n\n"
                "\"Excuse me... I've had a cough for several days, "
                "and now I have a fever. I don't know what's wrong.\""
            )

        if self.current_stage == EncounterStage.HISTORY:
            return "Begin gathering the patient's history."

        if self.current_stage == EncounterStage.ASSESSMENT:
            return "Review the available information and determine the likely problem."

        if self.current_stage == EncounterStage.TREATMENT:
            return "Choose the most appropriate treatment plan."

        if self.current_stage == EncounterStage.OUTCOME:
            return "Observe the patient's response to your clinical decisions."

        return "The encounter has been completed."

    def __str__(self):
        return (
            f"PatientEncounter("
            f"id='{self.encounter_id}', "
            f"patient='{self.patient_name}', "
            f"stage='{self.current_stage.name}', "
            f"completed={self.completed})"
        )