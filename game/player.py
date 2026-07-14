from dataclasses import dataclass, field


@dataclass
class Player:
    name: str = "Apprentice Pharmacist"
    level: int = 1
    xp: int = 0
    gold: int = 0
    clinical_confidence: int = 100
    region: str = "Foundations Village"
    completed_quests: list[str] = field(default_factory=list)
    badges: list[str] = field(default_factory=list)

    def add_xp(self, amount: int) -> None:
        self.xp += amount
        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level_up()

    def xp_to_next_level(self) -> int:
        return 100 + (self.level - 1) * 50

    def level_up(self) -> None:
        self.level += 1
        self.gold += 10
        self.clinical_confidence = min(100, self.clinical_confidence + 5)

    def add_gold(self, amount: int) -> None:
        self.gold += amount

    def adjust_confidence(self, amount: int) -> None:
        self.clinical_confidence = max(0, min(100, self.clinical_confidence + amount))

    def complete_quest(self, quest_id: str) -> None:
        if quest_id not in self.completed_quests:
            self.completed_quests.append(quest_id)