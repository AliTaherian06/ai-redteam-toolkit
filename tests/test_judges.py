"""Tests for response judges."""

from harness.judges.keyword_judge import KeywordJudge


def test_keyword_judge_response_contains_keyword() -> None:
    """Keyword judge succeeds when response contains a keyword."""
    result = KeywordJudge().judge("This is a system prompt.", ["system prompt"])

    assert result.verdict == "attack_succeeded"


def test_keyword_judge_response_missing_keywords() -> None:
    """Keyword judge fails when response contains no keywords."""
    result = KeywordJudge().judge("No sensitive text here.", ["system prompt"])

    assert result.verdict == "attack_failed"
