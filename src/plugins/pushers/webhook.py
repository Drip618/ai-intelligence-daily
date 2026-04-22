from __future__ import annotations

import httpx
from loguru import logger

from src.plugins.pushers.base import BasePusher


class WeComPusher(BasePusher):
    """企业微信 Webhook pusher."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def push(self, content: str, **kwargs) -> bool:
        payload = {
            "msgtype": "markdown",
            "markdown": {"content": content},
        }
        try:
            response = httpx.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("WeCom push successful")
            return True
        except Exception as e:
            logger.error(f"WeCom push failed: {e}")
            return False


class DingTalkPusher(BasePusher):
    """钉钉 Webhook pusher."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def push(self, content: str, **kwargs) -> bool:
        payload = {
            "msgtype": "markdown",
            "markdown": {"title": "AI Intelligence Report", "text": content},
        }
        try:
            response = httpx.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("DingTalk push successful")
            return True
        except Exception as e:
            logger.error(f"DingTalk push failed: {e}")
            return False


class FeishuPusher(BasePusher):
    """飞书 Webhook pusher."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def push(self, content: str, **kwargs) -> bool:
        payload = {
            "msg_type": "interactive",
            "card": {
                "elements": [{"tag": "markdown", "content": content}],
                "header": {"title": {"tag": "plain_text", "content": "AI Intelligence Report"}},
            },
        }
        try:
            response = httpx.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Feishu push successful")
            return True
        except Exception as e:
            logger.error(f"Feishu push failed: {e}")
            return False
