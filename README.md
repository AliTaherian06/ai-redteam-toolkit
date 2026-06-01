ai-redteam-toolkit
==================

ai-redteam-toolkit is an open-source AI red-teaming tool: a Python harness that runs adversarial prompt-injection attacks against any LLM endpoint and records structured results. Attack categories include direct injection, indirect injection via tool/document inputs, tool-use hijacking, and data exfiltration. The harness uses a YAML attack catalog so attacks are versionable, reviewable, and community-extensible. A future agent layer (Reporter) selects attacks for a target endpoint and produces a CISO-readable PDF security report.

This sprint provides the foundation: a CLI, YAML attack loading, an OpenAI target adapter, keyword judging, and JSON result output.

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

How to Contribute an Attack
---------------------------

Add a YAML file under `attack_catalog/` that follows `attack_catalog/schema.md`. Keep each attack focused, include clear success criteria, and add references for reviewers. New catalog content should include tests when it changes parser or runner behavior.

Test
----

```bash
uv run pytest
```
