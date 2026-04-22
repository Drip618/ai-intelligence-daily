#!/usr/bin/env python3
import requests, re

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'

# Test tophub weibo
print("=== Testing Weibo ===")
r = requests.get('https://tophub.today/n/KqndgxeLl9', headers={'User-Agent': UA}, timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    html = r.text
    print(f'Total length: {len(html)}')
    # Check table pattern
    table_match = re.search(r'<table.*?</table>', html, re.DOTALL)
    if table_match:
        table_html = table_match.group()
        td_matches = re.findall(r'<td class="al">(.*?)</td>', table_html)
        link_matches = re.findall(r'<a href="([^"]+)"', table_html)
        print(f'Table td.al: {len(td_matches)}')
        print(f'Table links: {len(link_matches)}')
        for i, t in enumerate(td_matches[:5]):
            clean = re.sub(r'<[^>]+>', '', t)
            link = link_matches[i] if i < len(link_matches) else 'N/A'
            print(f'  {i+1}. {clean} -> {link}')
    else:
        print('No table, looking for div patterns...')
        items = re.findall(r'<div class="cc".*?</div>', html, re.DOTALL)
        print(f'Div cc items: {len(items)}')
        if not items:
            # Show first 2000 chars
            print(html[:2000])

print("\n=== Testing Zhihu ===")
r = requests.get('https://tophub.today/n/mproPpoq6O', headers={'User-Agent': UA}, timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    html = r.text
    table_match = re.search(r'<table.*?</table>', html, re.DOTALL)
    if table_match:
        table_html = table_match.group()
        td_matches = re.findall(r'<td class="al">(.*?)</td>', table_html)
        print(f'Table td.al: {len(td_matches)}')
        for t in td_matches[:5]:
            print(f'  - {re.sub(r"<[^>]+>", "", t)}')
    else:
        print('No table')
        print(html[:2000])

print("\n=== Testing Xiaohongshu ===")
r = requests.get('https://tophub.today/n/Om4ejxvENM', headers={'User-Agent': UA}, timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    html = r.text
    table_match = re.search(r'<table.*?</table>', html, re.DOTALL)
    if table_match:
        td_matches = re.findall(r'<td class="al">(.*?)</td>', table_match.group())
        print(f'Table td.al: {len(td_matches)}')
    else:
        print('No table')
        print(html[:2000])

print("\n=== Testing WeChat ===")
r = requests.get('https://tophub.today/n/Q1Vd5Ko85R', headers={'User-Agent': UA}, timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    html = r.text
    table_match = re.search(r'<table.*?</table>', html, re.DOTALL)
    if table_match:
        td_matches = re.findall(r'<td class="al">(.*?)</td>', table_match.group())
        print(f'Table td.al: {len(td_matches)}')
    else:
        print('No table')
        print(html[:2000])

print("\n=== Testing HuggingFace ===")
r = requests.get('https://tophub.today/n/JbDHmOXPke', headers={'User-Agent': UA}, timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    html = r.text
    table_match = re.search(r'<table.*?</table>', html, re.DOTALL)
    if table_match:
        td_matches = re.findall(r'<td class="al">(.*?)</td>', table_match.group())
        print(f'Table td.al: {len(td_matches)}')
    else:
        print('No table')
        print(html[:2000])

print("\n=== Testing Sina Tech ===")
r = requests.get('https://tech.sina.com.cn/', headers={'User-Agent': UA}, timeout=15)
print(f'Status: {r.status_code}')
if r.status_code == 200:
    html = r.text
    links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>', html)
    print(f'Links found: {len(links)}')
    for url, title in links[:10]:
        print(f'  - {title} -> {url}')
