#!/usr/bin/env python3
import requests, json

# Try the most reliable free Chinese hot list APIs
apis = {
    "rebang_api": "https://api.rebang.today/api/hot?source=weibo&limit=5",
    "duanxian_api": "https://duanxian.api.300600.xyz/api/weibo",
    "new_api_1": "https://api.03c3.cn/api/weibo",
    "new_api_2": "https://tenapi.cn/v2/weibohot",
}

for name, url in apis.items():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        r = requests.get(url, headers=headers, timeout=10)
        print(f"\n{name}: status={r.status_code}")
        print(f"  body[:500]: {r.text[:500]}")
    except Exception as e:
        print(f"\n{name}: ERROR {e}")
