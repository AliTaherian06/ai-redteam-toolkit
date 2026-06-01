"""Typed models for attacks, judgments, and results."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field


class SuccessCriteria(BaseModel):
    """Defines how an attack response is judged."""

    type: Literal["keyword_present"]
    keywords: list[str] = Field(min_length=1)


class Attack(BaseModel):
    """Represents one catalog attack."""

    id: str
    name: str
    category: str
    description: str
    prompt: str
    success_criteria: SuccessCriteria
    severity: Literal["informational", "low", "medium", "high", "critical"]
    references: list[str] = Field(default_factory=list)


class JudgeResult(BaseModel):
    """Represents the outcome of judging a target response."""

    verdict: Literal["attack_succeeded", "attack_failed"]
    reasoning: str


class AttackResult(BaseModel):
    """Represents the recorded result of one attack run."""

    attack_id: str
    attack_name: str
    category: str
    prompt_sent: str
    target_response: str
    judge_verdict: Literal["pass", "fail"]
    judge_reasoning: str
    timestamp: datetime
    target_model: str


def load_attack(path: Path) -> Attack:
    """Loads one attack YAML file."""
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    return Attack.model_validate(data)


def utc_now() -> datetime:
    """Returns the current UTC timestamp."""
    return datetime.now(timezone.utc)
