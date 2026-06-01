"""Tests for attack loading and running."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from harness.models import Attack, load_attack
from harness.runner import run_attacks


class MockTarget:
    """Mock target for runner tests."""

    model = "mock-model"

    def send(self, prompt: str) -> str:
        """Returns a fixed response."""
        return f"system prompt response to {prompt}"


def test_load_valid_attack_yaml_returns_attack(valid_attack_yaml: Path) -> None:
    """Loading valid YAML returns an Attack model."""
    attack = load_attack(valid_attack_yaml)

    assert isinstance(attack, Attack)
    assert attack.id == "hello_direct"


def test_load_malformed_attack_yaml_raises_validation_error(tmp_path: Path) -> None:
    """Loading malformed YAML raises ValidationError."""
    path = tmp_path / "bad.yaml"
    path.write_text("id: missing_fields", encoding="utf-8")

    with pytest.raises(ValidationError):
        load_attack(path)


def test_runner_with_mocked_target_produces_attack_result(attack: Attack) -> None:
    """Runner produces an AttackResult from a mocked target."""
    results = run_attacks([attack], MockTarget())

    assert len(results) == 1
    assert results[0].attack_id == attack.id
    assert results[0].judge_verdict == "pass"
    assert results[0].target_model == "mock-model"
