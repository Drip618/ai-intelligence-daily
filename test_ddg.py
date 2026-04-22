#!/usr/bin/env python3
import requests, re

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Test DDG search
url = "https://html.duckduckgo.com/html/?q=test"
r = requests.get(url, headers={"User-Agent": UA}, timeout=15)
print(f"DDG status: {r.status_code}, len: {len(r.text)}")

if r.status_code == 200:
    if "captcha" in r.text.lower() or "verify" in r.text.lower():
        print("  CAPTCHA detected!")
    
    # Try multiple patterns
    patterns = [
        r'class="result__a"[^>]+href="([^"]+)".*?>(.*?)</a>',
        r'class="result__snippet"[^>]*>(.*?)</a>',
        r'<a[^>]+href="(/\?uddg=[^"]+)"',
    ]
    for p in patterns:
        results = re.findall(p, r.text, re.DOTALL)
        print(f"  Pattern '{p[:40]}...': {len(results)} results")
        if results:
            print(f"    Sample: {str(results[0])[:100]}")
    
    # Check page structure
    print(f"\n  First 500 chars:\n{r.text[:500]}")
