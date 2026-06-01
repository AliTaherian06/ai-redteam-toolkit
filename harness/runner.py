"""Attack loading and execution helpers."""

import json
from pathlib import Path

from pydantic import TypeAdapter

from harness.judges.keyword_judge import KeywordJudge
from harness.models import Attack, AttackResult, load_attack, utc_now
from harness.target import Target


def load_attacks(catalog: Path) -> list[Attack]:
    """Loads attack YAML files from a file or directory."""
    paths = [catalog] if catalog.is_file() else sorted(catalog.glob("*.yaml"))
    return [load_attack(path) for path in paths]


def run_attacks(attacks: list[Attack], target: Target) -> list[AttackResult]:
    """Runs attacks against a target and returns structured results."""
    results = []
    for attack in attacks:
        response = target.send(attack.prompt)
        judgment = KeywordJudge().judge(response, attack.success_criteria.keywords)
        results.append(
            AttackResult(
                attack_id=attack.id,
                attack_name=attack.name,
                category=attack.category,
                prompt_sent=attack.prompt,
                target_response=response,
                judge_verdict="pass" if judgment.verdict == "attack_succeeded" else "fail",
                judge_reasoning=judgment.reasoning,
                timestamp=utc_now(),
                target_model=target.model,
            )
        )
    return results


def write_results(results: list[AttackResult], output: Path) -> None:
    """Writes attack results as JSON."""
    data = TypeAdapter(list[AttackResult]).dump_python(results, mode="json")
    output.write_text(json.dumps(data, indent=2), encoding="utf-8")
