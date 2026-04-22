from __future__ import annotations

from abc import ABC, abstractmethod


class BaseModelAdapter(ABC):
    """Base class for all model adapters."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text response from the model."""

    @abstractmethod
    def classify(self, content: str, categories: list[str]) -> dict:
        """Classify content into categories.

        Returns:
            dict with keys: category (str), tags (list[str])
        """

    @abstractmethod
    def summarize(self, texts: list[str], **kwargs) -> str:
        """Summarize a list of texts."""
