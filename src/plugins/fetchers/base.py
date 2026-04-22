from __future__ import annotations

from abc import ABC, abstractmethod

from src.models import Item


class BaseFetcher(ABC):
    """Base class for all data fetchers."""

    @abstractmethod
    def fetch(self, keywords: list[str] | None = None) -> list[Item]:
        """Fetch data and return list of Items."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return fetcher name."""
