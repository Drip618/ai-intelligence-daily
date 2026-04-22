from __future__ import annotations

import os

import httpx
from loguru import logger

from src.models import Item
from src.plugins.fetchers.base import BaseFetcher


class GithubFetcher(BaseFetcher):
    """Github repository fetcher."""

    def __init__(self, keywords: list[str] | None = None, min_stars: int = 100):
        self.keywords = keywords or ["AI", "LLM", "Agent"]
        self.min_stars = min_stars
        self.base_url = "https://api.github.com/search/repositories"
        self.token = os.getenv("GITHUB_TOKEN")

    @property
    def name(self) -> str:
        return "Github"

    def fetch(self, keywords: list[str] | None = None) -> list[Item]:
        kws = keywords or self.keywords
        items = []

        for kw in kws:
            logger.info(f"Fetching Github repos for keyword: {kw}")
            params = {
                "q": f"{kw} stars:>{self.min_stars} created:>2026-01-01",
                "sort": "stars",
                "order": "desc",
                "per_page": 10,
            }
            headers = {}
            if self.token:
                headers["Authorization"] = f"token {self.token}"

            try:
                response = httpx.get(self.base_url, params=params, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()

                for repo in data.get("items", []):
                    item = Item(
                        title=repo["name"],
                        description=repo.get("description") or "",
                        category="开源项目",
                        source="Github",
                        tags=[kw, "open-source"],
                        url=repo["html_url"],
                    )
                    items.append(item)
            except Exception as e:
                logger.error(f"Failed to fetch Github repos: {e}")

        return items
