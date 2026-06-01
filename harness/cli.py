"""Command line interface for the harness."""

from pathlib import Path

import typer
from dotenv import load_dotenv

from harness.runner import load_attacks, run_attacks, write_results

app = typer.Typer(help="Run prompt-injection attacks against LLM targets.")


@app.callback()
def main() -> None:
    """Runs the AI red-team toolkit CLI."""


def build_target(name: str):
    """Builds a target adapter by name."""
    if name == "openai":
        from harness.targets.openai_target import OpenAITarget

        return OpenAITarget()
    if name == "ollama":
        from harness.targets.ollama_target import OllamaTarget

        return OllamaTarget()
    raise typer.BadParameter(f"Unknown target: {name}. Supported: openai, ollama.")


@app.command()
def run(
    catalog: Path = typer.Option(..., exists=True, file_okay=True, dir_okay=True),
    target: str = typer.Option("openai"),
    output: Path = typer.Option(...),
) -> None:
    """Runs catalog attacks and writes JSON results."""
    load_dotenv()
    attacks = load_attacks(catalog)
    results = run_attacks(attacks, build_target(target))
    write_results(results, output)
    typer.echo(f"Wrote {len(results)} result(s) to {output}")


if __name__ == "__main__":
    app()
