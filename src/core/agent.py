from __future__ import annotations

import os

from dotenv import load_dotenv
from loguru import logger

from src.adapters.models.base import BaseModelAdapter
from src.adapters.models.openai_adapter import OpenAIAdapter
from src.adapters.models.claude_adapter import ClaudeAdapter
from src.adapters.models.qwen_adapter import QwenAdapter
from src.adapters.models.ollama_adapter import OllamaAdapter
from src.formatter import MarkdownFormatter
from src.plugins.fetchers.base import BaseFetcher
from src.plugins.pushers.base import BasePusher
from src.storage.knowledge_base import KnowledgeBase
from src.core.workflow import Workflow


load_dotenv()


class IntelligenceAgent:
    """Main intelligence agent controller."""

    def __init__(
        self,
        model_adapter: BaseModelAdapter,
        fetchers: list[BaseFetcher],
        pushers: list[BasePusher],
        knowledge_base: KnowledgeBase | None = None,
    ):
        self.model_adapter = model_adapter
        self.fetchers = fetchers
        self.pushers = pushers
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.formatter = MarkdownFormatter()
        self.workflow = Workflow(model_adapter, self.knowledge_base)

    @classmethod
    def from_config(cls, config: dict) -> "IntelligenceAgent":
        """Create agent from configuration."""
        model_config = config.get("model", {})
        provider = model_config.get("provider", "openai")
        api_key = model_config.get("api_key", os.getenv("OPENAI_API_KEY", ""))

        model_adapter = cls._create_model_adapter(provider, model_config, api_key)
        fetchers = cls._create_fetchers(config.get("fetchers", {}))
        pushers = cls._create_pushers(config.get("pushers", {}))
        kb = KnowledgeBase(config.get("storage", {}).get("knowledge_path", "./data/knowledge"))

        return cls(model_adapter, fetchers, pushers, kb)

    @staticmethod
    def _create_model_adapter(provider: str, model_config: dict, api_key: str) -> BaseModelAdapter:
        adapters = {
            "openai": lambda: OpenAIAdapter(
                api_key=api_key,
                model_name=model_config.get("model_name", "gpt-4-turbo"),
                temperature=model_config.get("temperature", 0.7),
            ),
            "claude": lambda: ClaudeAdapter(
                api_key=api_key or os.getenv("ANTHROPIC_API_KEY", ""),
                model_name=model_config.get("model_name", "claude-3-opus-20240229"),
                temperature=model_config.get("temperature", 0.7),
            ),
            "qwen": lambda: QwenAdapter(
                api_key=api_key or os.getenv("DASHSCOPE_API_KEY", ""),
                model_name=model_config.get("model_name", "qwen-turbo"),
                temperature=model_config.get("temperature", 0.7),
            ),
            "ollama": lambda: OllamaAdapter(
                model_name=model_config.get("model_name", "llama3"),
                temperature=model_config.get("temperature", 0.7),
            ),
        }
        return adapters[provider]()

    @staticmethod
    def _create_fetchers(fetcher_config: dict) -> list[BaseFetcher]:
        from src.plugins.fetchers.github import GithubFetcher
        from src.plugins.fetchers.huggingface import HuggingfaceFetcher
        from src.plugins.fetchers.video_platforms import BilibiliFetcher

        fetchers = []
        gh_config = fetcher_config.get("github", {})
        if gh_config.get("enabled", False):
            fetchers.append(GithubFetcher(
                keywords=gh_config.get("keywords", ["AI"]),
                min_stars=gh_config.get("min_stars", 100),
            ))

        hf_config = fetcher_config.get("huggingface", {})
        if hf_config.get("enabled", False):
            fetchers.append(HuggingfaceFetcher(keywords=hf_config.get("keywords", ["AI"])))

        bi_config = fetcher_config.get("bilibili", {})
        if bi_config.get("enabled", False):
            fetchers.append(BilibiliFetcher(
                keywords=bi_config.get("keywords", ["AI"]),
                max_results=bi_config.get("max_results", 20),
            ))

        return fetchers

    @staticmethod
    def _create_pushers(pusher_config: dict) -> list[BasePusher]:
        from src.plugins.pushers.email import EmailPusher
        from src.plugins.pushers.telegram import TelegramPusher
        from src.plugins.pushers.webhook import WeComPusher, DingTalkPusher, FeishuPusher

        pushers = []

        email_config = pusher_config.get("email", {})
        if email_config.get("enabled", False):
            pushers.append(EmailPusher(
                smtp_host=email_config.get("smtp_host", ""),
                smtp_port=email_config.get("smtp_port", 587),
                smtp_user=email_config.get("smtp_user", ""),
                smtp_password=email_config.get("smtp_password", ""),
                smtp_to=email_config.get("smtp_to", ""),
            ))

        wecom_config = pusher_config.get("wecom", {})
        if wecom_config.get("enabled", False):
            pushers.append(WeComPusher(webhook_url=wecom_config.get("webhook_url", "")))

        dingtalk_config = pusher_config.get("dingtalk", {})
        if dingtalk_config.get("enabled", False):
            pushers.append(DingTalkPusher(webhook_url=dingtalk_config.get("webhook_url", "")))

        feishu_config = pusher_config.get("feishu", {})
        if feishu_config.get("enabled", False):
            pushers.append(FeishuPusher(webhook_url=feishu_config.get("webhook_url", "")))

        telegram_config = pusher_config.get("telegram", {})
        if telegram_config.get("enabled", False):
            pushers.append(TelegramPusher(
                bot_token=telegram_config.get("bot_token", ""),
                chat_id=telegram_config.get("chat_id", ""),
            ))

        return pushers

    def run_daily_routine(self):
        """Execute daily intelligence collection workflow."""
        logger.info("Starting daily intelligence routine...")

        items_by_source = self.workflow.collect_from_fetchers(self.fetchers)
        classified_items = self.workflow.classify_items(items_by_source, self.model_adapter)
        self.workflow.update_knowledge_base(classified_items, self.knowledge_base)
        report = self.formatter.format_daily_report(classified_items)
        self.workflow.push_report(report, self.pushers)

        logger.info("Daily intelligence routine completed!")
