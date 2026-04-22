from datetime import datetime

from src.models import Item, KnowledgeEntry


class TestItem:
    def test_create_item(self):
        item = Item(
            title="Test Project",
            description="A test project",
            category="开源项目",
            source="Github",
            tags=["test", "AI"],
            url="https://github.com/test/project",
        )
        assert item.title == "Test Project"
        assert item.category == "开源项目"
        assert len(item.tags) == 2

    def test_item_hash_for_dedup(self):
        item1 = Item(
            title="Project A",
            description="Description A",
            source="Github",
            url="https://github.com/a/b",
        )
        item2 = Item(
            title="Project B",
            description="Description B",
            source="Github",
            url="https://github.com/a/b",
        )
        assert hash(item1) == hash(item2)

    def test_to_markdown_row(self):
        item = Item(
            title="Test",
            description="Desc",
            category="Agent",
            source="Github",
            tags=["AI"],
            url="https://example.com",
        )
        row = item.to_markdown_row()
        assert "Test" in row
        assert "[访问](https://example.com)" in row


class TestKnowledgeEntry:
    def test_create_entry(self):
        entry = KnowledgeEntry(
            content="Test content",
            category="Agent",
            tags=["test"],
            created_at=datetime.now(),
        )
        assert entry.content == "Test content"
        assert entry.category == "Agent"

    def test_entry_to_dict(self):
        entry = KnowledgeEntry(
            content="Test",
            category="工具",
            tags=["AI"],
        )
        d = entry.to_dict()
        assert d["content"] == "Test"
        assert d["category"] == "工具"
