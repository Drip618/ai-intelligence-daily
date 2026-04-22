from __future__ import annotations

import httpx
from loguru import logger

from src.models import Item
from src.plugins.fetchers.base import BaseFetcher


class HuggingfaceFetcher(BaseFetcher):
    """HuggingFace model/space fetcher."""

    def __init__(self, keywords: list[str] | None = None):
        self.keywords = keywords or ["AI", "LLM", "Agent"]
        self.base_url = "https://huggingface.co/api/models"

    @property
    def name(self) -> str:
        return "HuggingFace"

    def fetch(self, keywords: list[str] | None = None) -> list[Item]:
        kws = keywords or self.keywords
        items = []

        for kw in kws:
            logger.info(f"Fetching HuggingFace models for: {kw}")
            params = {
                "search": kw,
                "sort": "downloads",
                "direction": "-1",
                "limit": 10,
            }

            try:
                response = httpx.get(self.base_url, params=params, timeout=30)
                response.raise_for_status()
                models = response.json()

                for model in models:
                    item = Item(
                        title=model["modelId"],
                        description=model.get("description", "")[:200],
                        category="大模型",
                        source="HuggingFace",
                        tags=[kw, "model"],
                        url=f"https://huggingface.co/{model['modelId']}",
                    )
                    items.append(item)
            except Exception as e:
                logger.error(f"Failed to fetch HuggingFace models: {e}")

        return items
