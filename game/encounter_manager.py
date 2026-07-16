from patient_encounter import PatientEncounter


class EncounterManager:
    """Controls the active patient encounter."""

    def __init__(self):
        self.active_encounter = None

    def start_encounter(
        self,
        encounter_id: str,
        patient_name: str,
        chief_complaint: str,
        reward_xp: int = 25,
        reward_gold: int = 10,
    ):
        self.active_encounter = PatientEncounter(
            encounter_id=encounter_id,
            patient_name=patient_name,
            chief_complaint=chief_complaint,
            reward_xp=reward_xp,
            reward_gold=reward_gold,
        )

    def has_active_encounter(self) -> bool:
        return self.active_encounter is not None

    def get_encounter(self):
        return self.active_encounter

    def advance(self):
        if self.active_encounter is not None:
            self.active_encounter.advance_stage()

    def clear(self):
        self.active_encounter = None