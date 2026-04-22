from __future__ import annotations

from abc import ABC, abstractmethod


class BasePusher(ABC):
    """Base class for all push notification senders."""

    @abstractmethod
    def push(self, content: str, **kwargs) -> bool:
        """Push content to target channel.

        Returns:
            True if successful, False otherwise
        """
