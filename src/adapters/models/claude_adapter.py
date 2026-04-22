from __future__ import annotations

import json

from langchain_anthropic import ChatAnthropic
from loguru import logger

from src.adapters.models.base import BaseModelAdapter


class ClaudeAdapter(BaseModelAdapter):
    """Anthropic Claude model adapter."""

    def __init__(
        self,
        api_key: str,
        model_name: str = "claude-3-opus-20240229",
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ):
        self.model = ChatAnthropic(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        logger.info(f"Initialized ClaudeAdapter with model: {model_name}")

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
