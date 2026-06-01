"""Target protocol for LLM adapters."""

from typing import Protocol


class Target(Protocol):
    """Defines a target that can receive attack prompts."""

    model: str

    def send(self, prompt: str) -> str:
        """Sends a prompt and returns the target response."""
        ...
