"""Judge protocol definitions."""

from typing import Protocol

from harness.models import JudgeResult


class Judge(Protocol):
    """Defines a response judge."""

    def judge(self, response: str, keywords: list[str]) -> JudgeResult:
        """Judges a target response."""
        ...
