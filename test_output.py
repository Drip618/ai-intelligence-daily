#!/usr/bin/env python3
"""Test script to verify sorting and category distribution."""

import json
from pathlib import Path

TYPE_ORDER = {"文字": 0, "图片": 1, "视频": 2, "软件": 3}

kb_path = Path("data/knowledge/daily_reports/report_2026-04-22.json")
kb = json.loads(kb_path.read_text(encoding="utf-8"))
items = kb["items"]

print(f"Total items: {len(items)}")
print(f"Date: {kb['date']}")
print()

groups = {}
for item in items:
    c = item.get("platform", "其他")
    groups.setdefault(c, []).append(item)

for cat, cat_items in groups.items():
    print(f"【{cat}】({len(cat_items)} items)")
    for i, item in enumerate(cat_items):
        summary = item.get("summary", "")
        detail = item.get("detail", item.get("raw_detail", ""))
        text_len = len(summary + detail)
        content_type = item.get("content_type", "文字")
        title_preview = item["title"][:50]
        print(f"  {i+1:2d}. [{content_type}] len:{text_len:3d} | {title_preview}")
    print()

all_sorted = True
for cat, cat_items in groups.items():
    def sort_key(item):
        s = item.get("summary", "")
        d = item.get("detail", item.get("raw_detail", ""))
        tl = len(s + d)
        ct = item.get("content_type", "文字")
        return (TYPE_ORDER.get(ct, 99), tl)

    is_sorted = all(sort_key(cat_items[i]) <= sort_key(cat_items[i+1]) for i in range(len(cat_items) - 1))
    status = "PASS" if is_sorted else "FAIL"
    if not is_sorted:
        all_sorted = False
    print(f"[{status}] {cat} sorting: type->length order")

print(f"\nOverall: {'ALL PASS' if all_sorted else 'SOME FAILURES'}")
