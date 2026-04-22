"""Utility functions for AI Intelligence Agent."""

from __future__ import annotations

import hashlib
import yaml
from pathlib import Path


def load_config(config_path: str = "config/default.yaml") -> dict:
    """Load configuration from YAML file."""
    path = Path(config_path)
    if not path.exists():
        return {}
    
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def dedup_items(items: list, key: str = "url") -> list:
    """Deduplicate items by a given key."""
    seen = set()
    unique = []
    for item in items:
        k = getattr(item, key, str(item)) if hasattr(item, key) else str(item)
        if k not in seen:
            seen.add(k)
            unique.append(item)
    return unique


def hash_string(s: str) -> str:
    """Generate MD5 hash of a string."""
    return hashlib.md5(s.encode()).hexdigest()
