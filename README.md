ai-redteam-toolkit
==================

ai-redteam-toolkit is an open-source AI red-teaming tool: a Python harness that runs adversarial prompt-injection attacks against any LLM endpoint and records structured results. Attack categories include direct injection, indirect injection via tool/document inputs, tool-use hijacking, and data exfiltration. The harness uses a YAML attack catalog so attacks are versionable, reviewable, and community-extensible. A future agent layer (Reporter) selects attacks for a target endpoint and produces a CISO-readable PDF security report.

This sprint provides the foundation: a CLI, YAML attack loading, an OpenAI target adapter, keyword judging, and JSON result output.

## How This Was Built
I built this project with AI coding tools as my pair programmer. I asked them to scaffold the harness, draft the YAML attack-catalog schema, write the OpenAI and Ollama target adapters, build the keyword-judging logic, and draft the pytest tests. They were fast and reliable on the plumbing — the argparse wiring for `python -m harness run` (`--catalog`, `--target`, `--output`), JSON result formatting, `.env` configuration handling, and test scaffolding.

The security substance was mine. I chose the problem, defined the four attack categories (direct injection, indirect injection via tool/document inputs, tool-use hijacking, data exfiltration), wrote realistic attack prompts, defined clear success criteria for each catalog entry, and designed the catalog schema to be versionable and reviewable. The overall architecture — YAML catalog → harness runner → structured JSON results → future Reporter layer — was my call, and I reviewed the generated implementation and verified the outputs myself.

Where AI fell short: its first-draft attack prompts were cartoonishly obvious ("ignore all previous instructions" style) rather than realistic adversarial prompts that would actually test a model's guardrails. Its keyword judge had false-positive problems on benign refusals and partial compliances until I reworked the criteria. It also initially missed Ollama adapter details, so I fixed those and rewrote the tests that didn't match the runner's actual behavior.

Install
-------

```bash
uv sync
```

If `uv` is unavailable:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Configuration
-------------

Create a local `.env` file:

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

For local model attacks (free, no API key needed):

1. Install Ollama (https://ollama.com) and pull a model: `ollama pull phi3:mini`
2. Run with --target ollama:

```bash
python -m harness run --catalog attack_catalog/examples --target ollama --output results.json
```

Run
---

```bash
uv run python -m harness run --catalog attack_catalog/examples --target openai --output results.json
```


The output file is a JSON array of structured attack results.



The commands compose as a pipeline: `uv sync` installs dependencies, the `.env` file (or a local Ollama setup) configures the target, `python -m harness run` executes the attack catalog against that target and writes the JSON results, and `pytest` validates the parser and runner.

How to Contribute an Attack
---------------------------

Add a YAML file under `attack_catalog/` that follows `attack_catalog/schema.md`. Keep each attack focused, include clear success criteria, and add references for reviewers. New catalog content should include tests when it changes parser or runner behavior.

Test
----

```bash
uv run pytest
```
