import os
from unittest.mock import MagicMock, patch

from src.adapters.models.base import BaseModelAdapter
from src.adapters.models.openai_adapter import OpenAIAdapter


class TestBaseModelAdapter:
    def test_abstract_methods(self):
        import abc
        assert hasattr(BaseModelAdapter, '__abstractmethods__')


class TestOpenAIAdapter:
    @patch("src.adapters.models.openai_adapter.ChatOpenAI")
    def test_generate(self, mock_chat):
        mock_instance = MagicMock()
        mock_instance.invoke.return_value.content = "Hello, world!"
        mock_chat.return_value = mock_instance

        adapter = OpenAIAdapter(api_key="test-key", model_name="gpt-4-turbo")
        result = adapter.generate("Say hello")

        assert result == "Hello, world!"
        mock_instance.invoke.assert_called_once()

    def test_classify_returns_dict(self):
        adapter = OpenAIAdapter(api_key="test-key")
        result = adapter.classify(
            content="New LLM framework released",
            categories=["大模型", "Agent", "工具"],
        )
        assert isinstance(result, dict)
        assert "category" in result
        assert "tags" in result

    def test_summarize_returns_str(self):
        adapter = OpenAIAdapter(api_key="test-key")
        result = adapter.summarize(["Text 1", "Text 2"])
        assert isinstance(result, str)
