from __future__ import annotations

import json

from langchain_ollama import ChatOllama
from loguru import logger

from src.adapters.models.base import BaseModelAdapter


class OllamaAdapter(BaseModelAdapter):
    """Ollama local model adapter."""

    def __init__(
        self,
        model_name: str = "llama3",
        base_url: str = "http://localhost:11434",
        temperature: float = 0.7,
    ):
        self.model = ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=temperature,
        )
        logger.info(f"Initialized OllamaAdapter with model: {model_name}")

    def generate(self, prompt: str, **kwargs) -> str:
        response = self.model.invoke(prompt)
        return response.content

    def classify(self, content: str, categories: list[str]) -> dict:
        prompt = f"""Please classify the following content into one of these categories: {', '.join(categories)}
Also generate 3-5 relevant tags.

Content: {content}

Respond ONLY with a JSON object in this format:
{{"category": "chosen_category", "tags": ["tag1", "tag2", "tag3"]}}
"""
        response = self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {"category": categories[0], "tags": ["AI"]}

    def summarize(self, texts: list[str], **kwargs) -> str:
        combined = "\n".join(texts)
        prompt = f"""Please summarize the following content concisely:

{combined}
"""
        return self.generate(prompt)
