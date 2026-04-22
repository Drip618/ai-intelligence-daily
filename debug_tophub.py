#!/usr/bin/env python3
import requests, re

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'

# Check tophub weibo structure
r = requests.get('https://tophub.today/n/KqndgxeLl9', headers={'User-Agent': UA}, timeout=15)
html = r.text

# Find all card/article-like structures
divs = re.findall(r'<div[^>]*class="([^"]*card|list-item|hot|item[^"]*)"[^>]*>', html)
print("Card-like divs:", divs[:10])

# Look for title patterns
titles = re.findall(r'class="title"[^>]*>([^<]+)<', html)
print("Titles found:", len(titles))
for t in titles[:5]:
    print(f"  - {t}")

# Look for link patterns
links = re.findall(r'<a[^>]+href="(/n/[^"]*|https?://[^"]+)"[^>]*class="[^"]*title[^"]*"', html)
print("Title links found:", len(links))
for l in links[:5]:
    print(f"  - {l}")

# Find the main content area
content_match = re.search(r'<table[^>]*>(.*?)</table>', html, re.DOTALL)
if content_match:
    table = content_match.group(0)
    print("\nTable content (first 3000 chars):")
    print(table[:3000])
else:
    # Look for other structures
    print("\nNo table found, showing structure around 'title':")
    idx = html.find('class="title"')
    if idx > 0:
        print(html[max(0,idx-200):idx+500])
    else:
        # Try div patterns
        print("\nSearching for list-like content...")
        # Look for numbered lists
        list_items = re.findall(r'<li[^>]*>(.*?)</li>', html, re.DOTALL)
        print(f"li items: {len(list_items)}")
        if list_items:
            print(list_items[0][:500])
