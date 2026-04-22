from __future__ import annotations

from src.models import Item


class MarkdownFormatter:
    """Format items into beautiful Markdown tables."""

    def format_items(self, items: list[Item]) -> str:
        if not items:
            return ""

        header = "| 标题 | 简介 | 分类 | 来源 | 标签 | 直达链接 |\n"
        separator = "|------|------|------|------|------|----------|\n"

        rows = "".join(item.to_markdown_row() + "\n" for item in items)
        return header + separator + rows

    def format_daily_report(self, items_by_source: dict[str, list[Item]]) -> str:
        """Format complete daily report."""
        report = "# AI Intelligence Daily Report\n\n"

        all_items = []
        for source, items in items_by_source.items():
            if items:
                report += f"## {source}\n\n"
                report += self.format_items(items)
                report += "\n"
                all_items.extend(items)

        if all_items:
            report += "---\n"
            report += f"\n*Report generated at {all_items[0].collected_at.strftime('%Y-%m-%d %H:%M')}*"
        return report
