from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from game.questions import Question


@dataclass
class QuestionStats:
    times_seen: int = 0
    times_correct: int = 0
    times_incorrect: int = 0
    last_seen: Optional[str] = None
    mastered: bool = False

    def record_attempt(self, correct: bool) -> None:
        self.times_seen += 1
        self.last_seen = datetime.now(timezone.utc).isoformat()

        if correct:
            self.times_correct += 1
        else:
            self.times_incorrect += 1

        self.mastered = self.times_correct >= 2 and self.times_incorrect == 0


@dataclass
class QuestionBank:
    questions: List[Question]
    stats: Dict[str, QuestionStats] = field(default_factory=dict)

    def _get_stats(self, question_id: str) -> QuestionStats:
        if question_id not in self.stats:
            self.stats[question_id] = QuestionStats()
        return self.stats[question_id]

    def record_result(self, question_id: str, correct: bool) -> None:
        self._get_stats(question_id).record_attempt(correct)

    def select_next_question(self) -> Optional[Question]:
        if not self.questions:
            return None

        def score(q: Question) -> Tuple[int, int, int]:
            s = self._get_stats(q.id)

            # Highest priority:
            # 1) Incorrect questions
            # 2) Unseen questions
            # 3) Old mastered questions due for review
            # 4) Everything else
            incorrect_priority = 0 if s.times_incorrect > 0 else 1
            unseen_priority = 0 if s.times_seen == 0 else 1
            mastered_priority = 0 if not s.mastered else 1

            # Lower score = higher priority
            return (
                incorrect_priority,
                unseen_priority,
                mastered_priority,
            )

        return sorted(self.questions, key=score)[0]

    def get_review_queue(self) -> List[Question]:
        """
        Returns questions ordered by adaptive priority.
        Useful for Study Mode and Review Mode.
        """
        return sorted(
            self.questions,
            key=lambda q: (
                0 if self._get_stats(q.id).times_incorrect > 0 else 1,
                0 if self._get_stats(q.id).times_seen == 0 else 1,
                0 if not self._get_stats(q.id).mastered else 1,
                self._get_stats(q.id).times_seen,
            ),
        )