from __future__ import annotations

import httpx
from loguru import logger

from src.plugins.pushers.base import BasePusher


class TelegramPusher(BasePusher):
    """Telegram Bot API pusher."""

    def __init__(self, bot_token: str, chat_id: str):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{bot_token}"

    def push(self, content: str, **kwargs) -> bool:
        url = f"{self.base_url}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": content,
            "parse_mode": "HTML",
        }

        try:
            response = httpx.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Telegram push successful")
            return True
        except Exception as e:
            logger.error(f"Telegram push failed: {e}")
            return False
