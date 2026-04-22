from __future__ import annotations

import json
from pathlib import Path

from loguru import logger

from src.models import KnowledgeEntry


class KnowledgeBase:
    """Local file-based knowledge base management."""

    def __init__(self, knowledge_path: str = "./data/knowledge"):
        self.base_path = Path(knowledge_path)
        self.short_term_path = self.base_path / "short_term"
        self.long_term_path = self.base_path / "long_term"
        self.skills_path = self.base_path / "skills"

        self._ensure_dirs()

    def _ensure_dirs(self):
        for path in [self.short_term_path, self.long_term_path, self.skills_path]:
            path.mkdir(parents=True, exist_ok=True)

    def add_short_term(self, entry: KnowledgeEntry):
        """Add entry to short-term memory."""
        file_path = self.short_term_path / f"{entry.created_at.strftime('%Y%m%d_%H%M%S')}.json"
        file_path.write_text(json.dumps(entry.to_dict(), ensure_ascii=False, indent=2))
        logger.info(f"Added short-term entry: {entry.content[:50]}...")

    def promote_to_long_term(self, entry: KnowledgeEntry):
        """Promote entry from short-term to long-term memory."""
        file_path = self.long_term_path / f"{entry.created_at.strftime('%Y%m%d_%H%M%S')}.json"
        file_path.write_text(json.dumps(entry.to_dict(), ensure_ascii=False, indent=2))
        logger.info(f"Promoted to long-term: {entry.content[:50]}...")

    def load_long_term(self) -> list[KnowledgeEntry]:
        """Load all long-term entries."""
        entries = []
        for file_path in self.long_term_path.glob("*.json"):
            data = json.loads(file_path.read_text())
            entries.append(KnowledgeEntry.from_dict(data))
        return entries

    def search(self, category: str | None = None, tags: list[str] | None = None) -> list[KnowledgeEntry]:
        """Search knowledge base."""
        entries = self.load_long_term()
        if category:
            entries = [e for e in entries if e.category == category]
        if tags:
            entries = [e for e in entries if any(t in e.tags for t in tags)]
        return entries
