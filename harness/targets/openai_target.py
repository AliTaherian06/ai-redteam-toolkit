"""OpenAI target adapter."""

import os

from openai import OpenAI


class OpenAITarget:
    """Sends prompts to an OpenAI chat model."""

    def __init__(self, model: str | None = None) -> None:
        """Initializes the OpenAI target."""
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        self.client = OpenAI()

    def send(self, prompt: str) -> str:
        """Sends a prompt to OpenAI and returns text."""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""
