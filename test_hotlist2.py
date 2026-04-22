#!/usr/bin/env python3
import requests, json

# Test various Chinese hot list APIs
apis = {
    "hotapi1": "https://hot.imsyy.top/api/weibo",
    "hotapi2": "https://api.imsyy.top/hot/weibo",
    "hotapi3": "https://rebang.today/api/hot?source=weibo",
    "hotapi4": "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=5",
}

for name, url in apis.items():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10, verify=True)
        print(f"{name}: status={r.status_code}")
        print(f"  body[:300]: {r.text[:300]}")
    except Exception as e:
        print(f"{name}: ERROR {e}")
