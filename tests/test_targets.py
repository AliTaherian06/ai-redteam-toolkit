"""Tests for target adapters and CLI."""

import json
from pathlib import Path

from harness.cli import app


def test_openai_target_uses_mocked_client(mocker) -> None:
    """OpenAI target returns mocked response content."""
    mock_client = mocker.patch("harness.targets.openai_target.OpenAI").return_value
    mock_choice = mocker.Mock()
    mock_choice.message.content = "hello"
    mock_client.chat.completions.create.return_value.choices = [mock_choice]

    from harness.targets.openai_target import OpenAITarget

    assert OpenAITarget(model="test-model").send("hi") == "hello"


def test_ollama_target_uses_mocked_client(mocker) -> None:
    """Ollama target returns mocked response content."""
    mock_client_cls = mocker.patch("harness.targets.ollama_target.ollama")
    mock_client = mock_client_cls.Client.return_value
    mock_client.chat.return_value = {"message": {"content": "hi from llama"}}

    from harness.targets.ollama_target import OllamaTarget

    assert OllamaTarget(model="phi3:mini").send("hi") == "hi from llama"


def test_cli_run_produces_output_file(cli_runner, valid_attack_yaml: Path, mocker) -> None:
    """CLI run writes an output file."""
    output = valid_attack_yaml.parent / "results.json"
    mock_target = mocker.Mock()
    mock_target.model = "mock-model"
    mock_target.send.return_value = "system prompt"
    mocker.patch("harness.cli.build_target", return_value=mock_target)

    result = cli_runner.invoke(
        app,
        [
            "run",
            "--catalog",
            str(valid_attack_yaml),
            "--target",
            "openai",
            "--output",
            str(output),
        ],
    )

    assert result.exit_code == 0
    assert json.loads(output.read_text(encoding="utf-8"))[0]["attack_id"] == "hello_direct"
