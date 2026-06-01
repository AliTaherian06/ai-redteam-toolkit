"""Ollama target adapter."""

import os

import ollama


class OllamaTarget:
    """Sends prompts to a locally-hosted Ollama model."""

    def __init__(self, model: str | None = None, host: str | None = None) -> None:
        """Initializes the Ollama target."""
        self.model = model or os.getenv("OLLAMA_MODEL", "phi3:mini")
        self.host = host or os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.client = ollama.Client(host=self.host)

    def send(self, prompt: str) -> str:
        """Sends a prompt to Ollama and returns text."""
        response = self.client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response["message"]["content"] or ""
