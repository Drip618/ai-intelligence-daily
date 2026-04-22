from __future__ import annotations

import httpx
from loguru import logger

from src.models import Item
from src.plugins.fetchers.base import BaseFetcher


class BilibiliFetcher(BaseFetcher):
    """Bilibili video fetcher."""

    def __init__(self, keywords: list[str] | None = None, max_results: int = 20):
        self.keywords = keywords or ["AI", "大模型", "Agent"]
        self.max_results = max_results
        self.base_url = "https://api.bilibili.com/x/web-interface/search/type"

    @property
    def name(self) -> str:
        return "Bilibili"

    def fetch(self, keywords: list[str] | None = None) -> list[Item]:
        kws = keywords or self.keywords
        items = []

        for kw in kws:
            logger.info(f"Fetching Bilibili videos for: {kw}")
            params = {
                "search_type": "video",
                "keyword": kw,
                "order": "click",
                "page": 1,
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            try:
                response = httpx.get(self.base_url, params=params, headers=headers, timeout=30)
                response.raise_for_status()
                data = response.json()

                if data.get("code") == 0:
                    results = data["data"].get("result", [])[: self.max_results]
                    for video in results:
                        title = video.get("title", "")
                        title = title.replace('<em class="keyword">', "").replace("</em>", "")
                        item = Item(
                            title=title,
                            description=video.get("description", "")[:200],
                            category="教程",
                            source="Bilibili",
                            tags=[kw, "video"],
                            url=f"https://www.bilibili.com/video/{video['bvid']}",
                        )
                        items.append(item)
            except Exception as e:
                logger.error(f"Failed to fetch Bilibili videos: {e}")

        return items
