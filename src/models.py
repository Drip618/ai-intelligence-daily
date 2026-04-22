from __future__ import annotations

import hashlib
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    """Represents a collected item (project, video, article, etc.)."""

    title: str
    description: str = ""
    category: str = ""
    source: str
    tags: list[str] = Field(default_factory=list)
    url: str
    collected_at: datetime = Field(default_factory=datetime.now)

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Item):
            return NotImplemented
        return self.url == other.url

    def to_markdown_row(self) -> str:
        """Convert to Markdown table row."""
        tags_str = ", ".join(self.tags) if self.tags else ""
        link = f"[访问]({self.url})"
        return f"| {self.title} | {self.description} | {self.category} | {self.source} | {tags_str} | {link} |"

    def dedup_key(self) -> str:
        """Generate deduplication key."""
        return hashlib.md5(self.url.encode()).hexdigest()


class KnowledgeEntry(BaseModel):
    """Represents an entry in the knowledge base."""

    content: str
    category: str
    tags: list[str] = Field(default_factory=list)
    source_url: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "source_url": self.source_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "KnowledgeEntry":
        return cls(
            content=data["content"],
            category=data["category"],
            tags=data.get("tags", []),
            source_url=data.get("source_url", ""),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
