#!/usr/bin/env python3
import requests, json

apis = {
    "weibo": "https://api.vvhan.com/api/hotlist/wbHot",
    "zhihu": "https://api.vvhan.com/api/hotlist/zhihuHotList",
    "xhs": "https://api.vvhan.com/api/hotlist/xhsList",
    "douyin": "https://api.vvhan.com/api/hotlist/dyHot",
    "bili": "https://api.vvhan.com/api/hotlist/bili",
    "36kr": "https://api.vvhan.com/api/hotlist/36Kr",
}

for name, url in apis.items():
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        ok = data.get("success", False)
        items = data.get("data", [])
        print(f"{name}: success={ok}, count={len(items)}")
        for item in items[:2]:
            if isinstance(item, dict):
                print(f"  - {item.get('title', '?')}")
            else:
                print(f"  - {item}")
    except Exception as e:
        print(f"{name}: ERROR {e}")
