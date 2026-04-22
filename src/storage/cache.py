from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from loguru import logger


class CacheManager:
    """Simple file-based cache."""

    def __init__(self, cache_path: str = "./data/cache", ttl_hours: int = 24):
        self.cache_path = Path(cache_path)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def get(self, key: str) -> str | None:
        file_path = self.cache_path / f"{key}.json"
        if not file_path.exists():
            return None

        data = json.loads(file_path.read_text())
        cached_at = datetime.fromisoformat(data["cached_at"])
        if datetime.now() - cached_at > self.ttl:
            file_path.unlink()
            return None

        return data.get("value")

    def set(self, key: str, value: str):
        file_path = self.cache_path / f"{key}.json"
        data = {"value": value, "cached_at": datetime.now().isoformat()}
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
        logger.debug(f"Cached: {key}")

    def clear(self):
        for file_path in self.cache_path.glob("*.json"):
            file_path.unlink()
        logger.info("Cache cleared")
