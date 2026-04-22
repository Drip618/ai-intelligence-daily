from __future__ import annotations

from loguru import logger

from src.adapters.models.base import BaseModelAdapter
from src.models import Item, KnowledgeEntry
from src.plugins.fetchers.base import BaseFetcher
from src.plugins.pushers.base import BasePusher
from src.storage.knowledge_base import KnowledgeBase


class Workflow:
    """Orchestrate the intelligence collection workflow."""

    def __init__(self, model_adapter: BaseModelAdapter, knowledge_base: KnowledgeBase):
        self.model_adapter = model_adapter
        self.knowledge_base = knowledge_base

    def collect_from_fetchers(self, fetchers: list[BaseFetcher]) -> dict[str, list[Item]]:
        """Collect items from all fetchers."""
        items_by_source: dict[str, list[Item]] = {}

        for fetcher in fetchers:
            logger.info(f"Fetching from {fetcher.name}...")
            try:
                items = fetcher.fetch()
                items_by_source[fetcher.name] = items
                logger.info(f"Fetched {len(items)} items from {fetcher.name}")
            except Exception as e:
                logger.error(f"Failed to fetch from {fetcher.name}: {e}")
                items_by_source[fetcher.name] = []

        return items_by_source

    def classify_items(
        self,
        items_by_source: dict[str, list[Item]],
        model_adapter: BaseModelAdapter,
    ) -> dict[str, list[Item]]:
        """Classify and tag items using AI model."""
        categories = ["大模型", "Agent", "Skill", "工具", "工作流", "资讯", "教程", "开源项目"]
        classified: dict[str, list[Item]] = {}

        for source, items in items_by_source.items():
            classified_items = []
            for item in items:
                try:
                    result = model_adapter.classify(
                        content=f"{item.title}\n{item.description}",
                        categories=categories,
                    )
                    item.category = result.get("category", source)
                    item.tags.extend(result.get("tags", []))
                    classified_items.append(item)
                except Exception as e:
                    logger.error(f"Failed to classify item: {e}")
                    classified_items.append(item)

            classified[source] = classified_items

        return classified

    def update_knowledge_base(
        self,
        classified_items: dict[str, list[Item]],
        knowledge_base: KnowledgeBase,
    ):
        """Add items to knowledge base."""
        for source, items in classified_items.items():
            for item in items:
                entry = KnowledgeEntry(
                    content=f"{item.title}: {item.description}",
                    category=item.category,
                    tags=item.tags,
                    source_url=item.url,
                )
                knowledge_base.add_short_term(entry)

    def push_report(self, report: str, pushers: list[BasePusher]):
        """Push report to all channels."""
        for pusher in pushers:
            try:
                success = pusher.push(report)
                if success:
                    logger.info(f"Successfully pushed to {pusher.__class__.__name__}")
                else:
                    logger.warning(f"Failed to push to {pusher.__class__.__name__}")
            except Exception as e:
                logger.error(f"Push failed for {pusher.__class__.__name__}: {e}")
