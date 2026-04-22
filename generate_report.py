#!/usr/bin/env python3
"""AI Intelligence Daily - Global News Aggregator"""

import json, os, time, re, random, hashlib, urllib.parse
import requests
from datetime import datetime, timedelta
from pathlib import Path
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Any

# ========== Configuration ==========

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data" / "knowledge" / "daily_reports"
CONFIG_DIR = BASE_DIR / "config"

for d in [OUTPUT_DIR, DATA_DIR, CONFIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Load environment variables
_env_path = BASE_DIR / ".env"
_env_vars = {}
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            _env_vars[k.strip()] = v.strip()

QWEN_API_KEY = os.getenv("QWEN_API_KEY", _env_vars.get("DASHSCOPE_API_KEY", ""))
QWEN_MODEL = os.getenv("QWEN_MODEL", "qwen-plus")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", _env_vars.get("GITHUB_TOKEN", ""))
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# Category definitions
CATEGORIES = {
    "自媒体": {"icon": "📱", "desc": "YouTube/B站/播客/Newsletter/创作者动态", "color": "#F59E0B"},
    "影视后期": {"icon": "🎬", "desc": "AE/PR/DaVinci/Blender/Nuke 行业动态", "color": "#EF4444"},
    "审美提升": {"icon": "🎨", "desc": "Dribbble/Behance/Pinterest/Awwwards 设计灵感", "color": "#8B5CF6"},
    "AI行业": {"icon": "🤖", "desc": "模型发布/论文/开源项目/工具推荐", "color": "#3B82F6"},
    "工具插件": {"icon": "🧰", "desc": "效率工具/浏览器插件/开发工具", "color": "#10B981"},
}

CONTENT_TYPES = {
    "文字": {"icon": "📝", "label": "文字资讯"},
    "图片": {"icon": "🖼️", "label": "图片内容"},
    "视频": {"icon": "🎥", "label": "视频教程"},
    "软件": {"icon": "💻", "label": "软件工具"},
    "插件": {"icon": "🔌", "label": "浏览器插件"},
}

# ========== User Config ==========

def load_user_config() -> dict:
    config_path = CONFIG_DIR / "user_config.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {
        "target_count": 50,
        "per_category": 10,
        "custom_apis": [],
        "enabled_categories": list(CATEGORIES.keys()),
        "fetch_strategy": "api_first",  # "api_first", "scrape_only", "hybrid"
        "push_channels": [],
    }

def save_user_config(config: dict):
    config_path = CONFIG_DIR / "user_config.json"
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

# ========== Global Source Registry ==========

GLOBAL_SOURCES = {
    # ===== 自媒体 =====
    "youtube_trending": {
        "category": "自媒体",
        "name": "YouTube Trending",
        "type": "api",
        "url": "https://www.youtube.com/feeds/videos.xml?chart=mostPopular&regionCode=US",
        "content_type": "视频",
        "enabled": True,
    },
    "bilibili_popular": {
        "category": "自媒体",
        "name": "B站热门",
        "type": "api",
        "url": "https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1",
        "content_type": "视频",
        "enabled": True,
    },
    "product_hunt": {
        "category": "自媒体",
        "name": "Product Hunt",
        "type": "scrape",
        "url": "https://www.producthunt.com/",
        "content_type": "文字",
        "enabled": True,
    },
    "substack_trending": {
        "category": "自媒体",
        "name": "Substack Trending",
        "type": "scrape",
        "url": "https://substack.com/",
        "content_type": "文字",
        "enabled": True,
    },

    # ===== 影视后期 =====
    "blender_community": {
        "category": "影视后期",
        "name": "Blender Community",
        "type": "scrape",
        "url": "https://www.blender.org/news/",
        "content_type": "图片",
        "enabled": True,
    },
    "ae_plugins": {
        "category": "影视后期",
        "name": "After Effects Plugins",
        "type": "scrape",
        "url": "https://aescripts.com/",
        "content_type": "软件",
        "enabled": True,
    },
    "davinci_resolve": {
        "category": "影视后期",
        "name": "DaVinci Resolve",
        "type": "scrape",
        "url": "https://www.blackmagicdesign.com/products/davinciresolve",
        "content_type": "软件",
        "enabled": True,
    },
    "video_copilot": {
        "category": "影视后期",
        "name": "Video Copilot",
        "type": "scrape",
        "url": "https://www.videocopilot.net/tutorials/",
        "content_type": "视频",
        "enabled": True,
    },
    "greyscalegorilla": {
        "category": "影视后期",
        "name": "Greyscalegorilla",
        "type": "scrape",
        "url": "https://greyscalegorilla.com/blog/",
        "content_type": "图片",
        "enabled": True,
    },

    # ===== 审美提升 =====
    "dribbble_trending": {
        "category": "审美提升",
        "name": "Dribbble Trending",
        "type": "scrape",
        "url": "https://dribbble.com/search/shots/popular",
        "content_type": "图片",
        "enabled": True,
    },
    "behance_featured": {
        "category": "审美提升",
        "name": "Behance Featured",
        "type": "scrape",
        "url": "https://www.behance.net/search/projects?field=graphic-design",
        "content_type": "图片",
        "enabled": True,
    },
    "pinterest_trending": {
        "category": "审美提升",
        "name": "Pinterest Trending",
        "type": "scrape",
        "url": "https://www.pinterest.com/today/",
        "content_type": "图片",
        "enabled": True,
    },
    "awwwards_sotd": {
        "category": "审美提升",
        "name": "Awwwards SOTD",
        "type": "scrape",
        "url": "https://www.awwwards.com/websites/",
        "content_type": "图片",
        "enabled": True,
    },
    "designspiration": {
        "category": "审美提升",
        "name": "Designspiration",
        "type": "scrape",
        "url": "https://www.designspiration.com/",
        "content_type": "图片",
        "enabled": True,
    },

    # ===== AI行业 =====
    "huggingface_trending": {
        "category": "AI行业",
        "name": "HuggingFace Models",
        "type": "api",
        "url": "https://huggingface.co/api/models?sort=trending&direction=-1&limit=15",
        "content_type": "图片",
        "enabled": True,
    },
    "github_ai_search": {
        "category": "AI行业",
        "name": "GitHub AI Search",
        "type": "api",
        "url": "https://api.github.com/search/repositories?q=ai+OR+llm+OR+gpt+OR+agent+OR+llama+sort:stars&per_page=20",
        "content_type": "软件",
        "enabled": True,
    },
    "github_ai_trending": {
        "category": "AI行业",
        "name": "GitHub Trending AI",
        "type": "scrape",
        "url": "https://github.com/trending?since=daily",
        "content_type": "软件",
        "enabled": True,
    },
    "papers_with_code": {
        "category": "AI行业",
        "name": "Papers With Code",
        "type": "scrape",
        "url": "https://paperswithcode.com/",
        "content_type": "文字",
        "enabled": True,
    },
    "arxiv_ai": {
        "category": "AI行业",
        "name": "arXiv AI Papers",
        "type": "api",
        "url": "https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&max_results=10",
        "content_type": "文字",
        "enabled": True,
    },

    # ===== 工具插件 =====
    "github_trending_tools": {
        "category": "工具插件",
        "name": "GitHub Trending",
        "type": "scrape",
        "url": "https://github.com/trending?since=daily",
        "content_type": "软件",
        "enabled": True,
    },
    "chrome_extensions": {
        "category": "工具插件",
        "name": "Chrome Extensions",
        "type": "scrape",
        "url": "https://chrome.google.com/webstore/category/extensions",
        "content_type": "插件",
        "enabled": True,
    },
    "alternative_to": {
        "category": "工具插件",
        "name": "AlternativeTo",
        "type": "scrape",
        "url": "https://alternativeto.net/",
        "content_type": "软件",
        "enabled": True,
    },
    "indie_hackers": {
        "category": "工具插件",
        "name": "Indie Hackers",
        "type": "scrape",
        "url": "https://www.indiehackers.com/",
        "content_type": "文字",
        "enabled": True,
    },

    # ===== 通用新闻 =====
    "reddit_popular": {
        "category": "AI行业",
        "name": "Reddit Popular",
        "type": "scrape",
        "url": "https://www.reddit.com/popular/",
        "content_type": "文字",
        "enabled": True,
    },
    "hn_frontpage": {
        "category": "AI行业",
        "name": "Hacker News",
        "type": "api",
        "url": "https://hacker-news.firebaseio.com/v0/topstories.json",
        "content_type": "文字",
        "enabled": True,
    },
    "techcrunch": {
        "category": "AI行业",
        "name": "TechCrunch",
        "type": "scrape",
        "url": "https://techcrunch.com/",
        "content_type": "文字",
        "enabled": True,
    },
    "theverge": {
        "category": "AI行业",
        "name": "The Verge",
        "type": "scrape",
        "url": "https://www.theverge.com/tech",
        "content_type": "文字",
        "enabled": True,
    },
}

# ========== Helper Functions ==========

def safe_get(url, headers=None, timeout=12):
    """Safe HTTP GET with error handling"""
    try:
        h = {"User-Agent": UA}
        if headers:
            h.update(headers)
        r = requests.get(url, headers=h, timeout=timeout)
        if r.status_code == 200:
            return r
    except Exception:
        pass
    return None

def clean_url(url):
    if not url or url == "#":
        return "#"
    if url.startswith("//"):
        return "https:" + url
    return url

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def dedup(items, threshold=0.7):
    unique, seen = [], []
    for item in items:
        if not any(similarity(item["title"], s) >= threshold for s in seen):
            seen.append(item["title"])
            unique.append(item)
    return unique

def balance_items(all_items, per_cat=10):
    by_cat = {}
    for item in all_items:
        by_cat.setdefault(item.get("platform", "其他"), []).append(item)
    result = []
    for cat in CATEGORIES:
        items = by_cat.get(cat, [])[:per_cat]
        result.extend(items)
    return result

def sort_by_length(items):
    def text_len(item):
        return len(item.get("summary", "") + item.get("detail", item.get("raw_detail", "")))
    return sorted(items, key=text_len)

def generate_picsum_url(title, category, width=800, height=450):
    seed = hashlib.md5((title + category).encode()).hexdigest()[:8]
    return f"https://picsum.photos/seed/{seed}/{width}/{height}"

# ========== Fetchers ==========

def fetch_huggingface(limit=10):
    """Fetch trending AI models from HuggingFace"""
    items = []
    try:
        r = requests.get("https://huggingface.co/api/models?sort=trending&direction=-1&limit=15", timeout=15)
        if r.status_code == 200:
            for model in r.json()[:limit]:
                mid = model.get("modelId", "")
                if not mid:
                    continue
                desc = model.get("description", "") or ""
                items.append({
                    "title": mid,
                    "summary": desc[:80],
                    "source": "HuggingFace",
                    "platform": "AI行业",
                    "hot_score": model.get("likes", 0),
                    "url": f"https://huggingface.co/{mid}",
                    "raw_detail": desc,
                    "content_type": "图片",
                })
    except Exception:
        pass
    return items

def fetch_github_ai(limit=10):
    """Fetch AI repositories from GitHub"""
    items = []
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    try:
        r = requests.get(
            "https://api.github.com/search/repositories?q=ai+OR+llm+OR+gpt+OR+agent+OR+llama+sort:stars&per_page=20",
            headers=headers,
            timeout=15
        )
        if r.status_code == 200:
            for repo in r.json().get("items", [])[:limit]:
                name = repo["full_name"]
                desc = repo.get("description", "") or ""
                items.append({
                    "title": name,
                    "summary": desc[:80],
                    "source": "GitHub AI",
                    "platform": "AI行业",
                    "hot_score": repo.get("stargazers_count", 0),
                    "url": repo["html_url"],
                    "raw_detail": desc,
                    "content_type": "软件",
                    "extra_info": {
                        "language": repo.get("language", ""),
                        "stars": repo.get("stargazers_count", 0),
                    },
                })
    except Exception:
        pass
    return items

def fetch_hacker_news(limit=8):
    """Fetch top stories from Hacker News"""
    items = []
    try:
        r = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        if r.status_code == 200:
            ids = r.json()[:20]
            for sid in ids[:limit]:
                sr = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5)
                if sr.status_code == 200:
                    story = sr.json()
                    if story.get("title"):
                        items.append({
                            "title": story["title"],
                            "summary": "",
                            "source": "Hacker News",
                            "platform": "AI行业",
                            "hot_score": story.get("score", 0),
                            "url": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                            "raw_detail": story.get("text", "") or "",
                            "content_type": "文字",
                        })
    except Exception:
        pass
    return items

def fetch_bilibili(limit=8):
    """Fetch popular videos from Bilibili"""
    items = []
    try:
        r = requests.get("https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1", timeout=10)
        if r.status_code == 200:
            videos = r.json().get("data", {}).get("list", [])
            for vid in videos[:limit]:
                title = vid.get("title", "")
                if not title:
                    continue
                bvid = vid.get("bvid", "")
                desc = vid.get("desc", "") or ""
                pic = vid.get("pic", "")
                if pic and not pic.startswith("http"):
                    pic = "https:" + pic
                items.append({
                    "title": title[:60],
                    "summary": desc[:60],
                    "source": "B站热门",
                    "platform": "自媒体",
                    "hot_score": vid.get("stat", {}).get("view", 0),
                    "url": f"https://www.bilibili.com/video/{bvid}",
                    "raw_detail": desc,
                    "content_type": "视频",
                    "image_url": pic,
                })
    except Exception:
        pass
    return items

def fetch_awwwards(limit=8):
    """Fetch Awwwards Sites of the Day"""
    items = []
    r = safe_get("https://www.awwwards.com/websites/", timeout=10)
    if r:
        seen = set()
        for a in re.finditer(r'<h3[^>]*>.*?<a[^>]+href="([^"]+)"', r.text, re.DOTALL):
            link = a.group(1).strip()
            if not link.startswith("/sites/"):
                continue
            title_m = re.search(r'>([^<]{3,})<', a.group(0))
            if not title_m:
                continue
            title = title_m.group(1).strip()
            if title in seen or len(title) < 3:
                continue
            seen.add(title)
            items.append({
                "title": title[:60],
                "summary": "",
                "source": "Awwwards",
                "platform": "审美提升",
                "hot_score": 0,
                "url": f"https://www.awwwards.com{link}",
                "raw_detail": "",
                "content_type": "图片",
            })
            if len(items) >= limit:
                break
    return items

def fetch_github_trending_non_ai(limit=8):
    """Fetch trending repos excluding AI"""
    items = []
    headers = {"User-Agent": UA}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    r = safe_get("https://github.com/trending?since=daily", headers=headers, timeout=15)
    if r:
        articles = re.findall(r'<article.*?</article>', r.text, re.DOTALL)
        for article in articles[:25]:
            h2 = re.search(r'<h2[^>]*>\s*<a[^>]+href="(/[^"]+)"', article)
            if not h2:
                continue
            repo = h2.group(1).strip()
            if repo.count('/') != 2:
                continue
            if any(kw in repo.lower() for kw in ["ai", "ml", "llm", "gpt", "model", "agent", "neural", "deep"]):
                continue
            desc_m = re.search(r'<p[^>]*>(.*?)</p>', article, re.DOTALL)
            desc = re.sub(r'<[^>]+>', '', desc_m.group(1)).strip() if desc_m else ""
            lang = re.search(r'itemprop="programmingLanguage"[^>]*>([^<]+)<', article)
            stars = re.search(r'([\d,]+)\s*stars?\s*today', article)
            items.append({
                "title": repo,
                "summary": desc[:80],
                "source": "GitHub Trending",
                "platform": "工具插件",
                "hot_score": int(stars.group(1).replace(",", "")) if stars and stars.group(1).replace(",", "").isdigit() else 0,
                "url": f"https://github.com{repo}",
                "raw_detail": desc,
                "content_type": "软件",
                "extra_info": {"language": lang.group(1).strip() if lang else "", "is_paid": False},
            })
            if len(items) >= limit:
                break
    return items

def fetch_github_design(limit=8):
    """Fetch design-related repos from GitHub"""
    items = []
    headers = {"User-Agent": UA, "Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    try:
        r = requests.get(
            "https://api.github.com/search/repositories?q=design+OR+ui+OR+frontend+OR+creative+OR+art+OR+css+sort:stars&per_page=20",
            headers=headers,
            timeout=15
        )
        if r.status_code == 200:
            for repo in r.json().get("items", [])[:limit]:
                name = repo["full_name"]
                desc = repo.get("description", "") or ""
                items.append({
                    "title": name,
                    "summary": desc[:80],
                    "source": "GitHub Design",
                    "platform": "审美提升",
                    "hot_score": repo.get("stargazers_count", 0),
                    "url": repo["html_url"],
                    "raw_detail": desc,
                    "content_type": "图片",
                    "extra_info": {"language": repo.get("language", ""), "is_paid": False},
                })
    except Exception:
        pass
    return items

def fetch_maoyan(limit=6):
    """Fetch Maoyan movies"""
    items = []
    r = safe_get("https://m.maoyan.com/ajax/movieOnInfoList?token=&optimus_uuid=&optimus_risk_level=&optimus_code=10", timeout=12)
    if r:
        try:
            movies = r.json().get("movieList", [])
            if isinstance(movies, list):
                for movie in movies[:limit]:
                    nm = movie.get("nm", "")
                    img = movie.get("img", "")
                    star = movie.get("star", "")
                    if nm:
                        items.append({
                            "title": nm,
                            "summary": f"主演: {star}"[:60] if star else "",
                            "source": "猫眼电影",
                            "platform": "审美提升",
                            "hot_score": 0,
                            "url": f"https://maoyan.com/films/{movie.get('id', '')}",
                            "raw_detail": "",
                            "content_type": "图片",
                            "image_url": img,
                        })
        except Exception:
            pass
    return items

def fetch_baidu_hot(limit=8):
    """Fetch Baidu Hot Search"""
    items = []
    try:
        r = safe_get("https://top.baidu.com/api/board?platform=wise&tab=realtime", headers={"Referer": "https://top.baidu.com/"}, timeout=10)
        if r:
            data = r.json()
            if data.get("success"):
                cards = data.get("data", {}).get("cards", [])
                for card in cards:
                    if card.get("component") == "tabTextList":
                        content_list = card.get("content", [])
                        for group in content_list:
                            for entry in group.get("content", []):
                                title = entry.get("query", "") or entry.get("word", "") or entry.get("hotName", "")
                                if not title or len(title) < 2:
                                    continue
                                url = entry.get("url", "") or f"https://www.baidu.com/s?wd={urllib.parse.quote(title)}"
                                hot = entry.get("hotScore", 0) or entry.get("topCount", 0) or 0
                                items.append({
                                    "title": title,
                                    "summary": "",
                                    "source": "百度热搜",
                                    "platform": "自媒体",
                                    "hot_score": hot,
                                    "url": url,
                                    "raw_detail": "",
                                    "content_type": "文字",
                                })
                                if len(items) >= limit:
                                    break
                    if len(items) >= limit:
                        break
    except Exception:
        pass
    return items

def fetch_zhihu(limit=8):
    """Fetch Zhihu Hot List"""
    items = []
    try:
        r = safe_get("https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=30", headers={"Referer": "https://www.zhihu.com/"}, timeout=15)
        if r:
            for entry in r.json().get("data", [])[:limit]:
                target = entry.get("target", {})
                title = target.get("title", "")
                if not title:
                    continue
                excerpt = target.get("excerpt", "")
                qid = target.get("id", "")
                items.append({
                    "title": title,
                    "summary": excerpt[:80] if excerpt else "",
                    "source": "知乎热榜",
                    "platform": "自媒体",
                    "hot_score": 0,
                    "url": target.get("url", "") or f"https://www.zhihu.com/question/{qid}",
                    "raw_detail": excerpt,
                    "content_type": "文字",
                })
    except Exception:
        pass
    return items

def fetch_arxiv(limit=6):
    """Fetch AI papers from arXiv"""
    items = []
    try:
        r = requests.get("https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&max_results=10", timeout=15)
        if r.status_code == 200:
            entries = re.findall(r'<entry>(.*?)</entry>', r.text, re.DOTALL)
            for entry in entries[:limit]:
                title_m = re.search(r'<title[^>]*>(.*?)</title>', entry, re.DOTALL)
                summary_m = re.search(r'<summary[^>]*>(.*?)</summary>', entry, re.DOTALL)
                link_m = re.search(r'<link[^>]+href="([^"]+)"', entry)
                title = re.sub(r'\s+', ' ', title_m.group(1).strip()) if title_m else ""
                summary = re.sub(r'\s+', ' ', summary_m.group(1).strip()) if summary_m else ""
                if title:
                    items.append({
                        "title": title[:80],
                        "summary": summary[:80],
                        "source": "arXiv",
                        "platform": "AI行业",
                        "hot_score": 0,
                        "url": link_m.group(1) if link_m else "",
                        "raw_detail": summary,
                        "content_type": "文字",
                    })
    except Exception:
        pass
    return items

def fetch_user_custom_apis(config: dict, limit=5) -> List[dict]:
    """Fetch from user-defined APIs"""
    items = []
    custom_apis = config.get("custom_apis", [])
    for api in custom_apis[:limit]:
        if not api.get("enabled", True):
            continue
        try:
            url = api.get("url", "")
            if not url:
                continue
            headers = api.get("headers", {"User-Agent": UA})
            method = api.get("method", "GET").upper()
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                path = api.get("data_path", "").split(".")
                for p in path:
                    if isinstance(data, dict):
                        data = data.get(p, [])
                if isinstance(data, list):
                    for entry in data[:5]:
                        items.append({
                            "title": entry.get(api.get("title_field", "title"), "Unknown"),
                            "summary": entry.get(api.get("summary_field", "description"), "")[:80],
                            "source": api.get("name", "Custom API"),
                            "platform": api.get("category", "AI行业"),
                            "hot_score": entry.get(api.get("score_field", "score"), 0),
                            "url": entry.get(api.get("url_field", "url"), ""),
                            "raw_detail": entry.get(api.get("detail_field", "body"), ""),
                            "content_type": api.get("content_type", "文字"),
                        })
        except Exception:
            pass
    return items

# ========== Image Fetcher ==========

def fetch_images_for_items(items):
    """Fetch images for items that don't have them"""
    success = 0
    for item in items:
        if item.get("image_url"):
            success += 1
            continue
        try:
            url = item.get("url", "")
            if url and not any(d in url for d in ["weibo.com", "zhihu.com", "baidu.com", "bilibili.com"]):
                resp = requests.get(url, headers={"User-Agent": UA}, timeout=5)
                if resp.status_code == 200:
                    for tag in ['og:image', 'twitter:image']:
                        m = re.search(rf'<meta[^>]+(?:property|name)=["\']{tag}["\'][^>]+content=["\']([^"\']+)["\']', resp.text)
                        if not m:
                            m = re.search(rf'<meta[^>]+content=["\']([^"\']+)["\'][^>]+(?:property|name)=["\']{tag}["\']', resp.text)
                        if m:
                            item["image_url"] = m.group(1)
                            success += 1
                            break
            if not item.get("image_url"):
                item["image_url"] = generate_picsum_url(item["title"], item.get("platform", ""))
                success += 1
        except Exception:
            item["image_url"] = generate_picsum_url(item["title"], item.get("platform", ""))
            success += 1
    return items

# ========== AI Summarizer ==========

def ai_summarize(items):
    """Summarize items using Qwen API"""
    if not QWEN_API_KEY:
        return items
    headers = {"Authorization": f"Bearer {QWEN_API_KEY}", "Content-Type": "application/json"}
    for i in range(0, len(items), 3):
        batch = items[i:i + 3]
        if all(item.get("detail") and len(item["detail"]) > 50 for item in batch):
            continue
        items_text = "\n---\n".join([
            f"标题：{it['title']}\n信息：{it.get('raw_detail', it.get('summary', '无'))}"
            for it in batch
        ])
        prompt = f"""用中文总结以下资讯，每条输出：
【一句话】20字以内概括
【详细解读】200-400字

{items_text}

按顺序输出，每条之间用 === 分隔。"""
        try:
            r = requests.post(
                f"{QWEN_BASE_URL}/chat/completions",
                headers=headers,
                json={
                    "model": QWEN_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 1500,
                },
                timeout=30,
            )
            if r.status_code == 200:
                content = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                if content:
                    parts = content.split("===")
                    for j, item in enumerate(batch):
                        if j < len(parts):
                            text = parts[j].strip()
                            summary, detail = "", text
                            if "【一句话】" in text:
                                sp = text.split("【详细解读】")
                                summary = sp[0].replace("【一句话】", "").strip()
                                detail = sp[1].strip() if len(sp) > 1 else text
                            item["summary"] = summary or item.get("summary", "")
                            item["detail"] = detail
                        else:
                            item["detail"] = item.get("raw_detail", item.get("summary", ""))
                    time.sleep(0.5)
                else:
                    for item in batch:
                        item["detail"] = item.get("raw_detail", item.get("summary", ""))
            else:
                for item in batch:
                    item["detail"] = item.get("raw_detail", item.get("summary", ""))
        except Exception:
            for item in batch:
                item["detail"] = item.get("raw_detail", item.get("summary", ""))
    return items

# ========== Main Pipeline ==========

def fetch_all(config: dict) -> List[dict]:
    """Main fetch pipeline"""
    all_items = []

    # Define fetch functions mapping
    fetch_funcs = {
        "huggingface_trending": lambda: fetch_huggingface(limit=10),
        "github_ai_search": lambda: fetch_github_ai(limit=10),
        "github_ai_trending": lambda: fetch_github_ai(limit=5),
        "hn_frontpage": lambda: fetch_hacker_news(limit=8),
        "bilibili_popular": lambda: fetch_bilibili(limit=8),
        "awwwards_sotd": lambda: fetch_awwwards(limit=8),
        "github_trending_tools": lambda: fetch_github_trending_non_ai(limit=8),
        "designspiration": lambda: fetch_github_design(limit=8),
        "maoyan_movies": lambda: fetch_maoyan(limit=6),
        "baidu_hot": lambda: fetch_baidu_hot(limit=8),
        "zhihu_hot": lambda: fetch_zhihu(limit=8),
        "arxiv_ai": lambda: fetch_arxiv(limit=6),
    }

    # Randomly select sources
    enabled_sources = [k for k, v in GLOBAL_SOURCES.items() if v.get("enabled", True)]
    selected_sources = random.sample(enabled_sources, min(len(enabled_sources), 15))

    print(f"[数据源] 从 {len(enabled_sources)} 个站点中随机选择 {len(selected_sources)} 个...")
    for source_key in selected_sources:
        if source_key in fetch_funcs:
            func = fetch_funcs[source_key]
            items = func()
            if items:
                all_items.extend(items)
                print(f"  ✓ {source_key}: {len(items)} 条")
            time.sleep(0.3)

    # Fetch user custom APIs
    custom_items = fetch_user_custom_apis(config, limit=5)
    if custom_items:
        all_items.extend(custom_items)
        print(f"  ✓ 自定义API: {len(custom_items)} 条")

    return all_items

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    parser.add_argument("--no-ai", action="store_true")
    args = parser.parse_args()
    date_str = args.date

    config = load_user_config()
    per_cat = config.get("per_category", 10)
    target = config.get("target_count", 50)

    print("=" * 60)
    print(f"AI Intelligence Daily - {date_str}")
    print(f"目标: {target} 条 | 每分类: {per_cat} 条")
    print("=" * 60)

    # Fetch
    all_items = fetch_all(config)
    print(f"\n原始: {len(all_items)} 条")

    # Deduplicate
    unique = dedup(all_items)
    print(f"去重: {len(unique)} 条")

    # Balance
    unique = balance_items(unique, per_cat=per_cat)
    unique = sort_by_length(unique)
    print(f"均衡分配: {len(unique)} 条")

    # AI summarize
    if unique and not args.no_ai:
        print("\n[AI] 智能总结中...")
        unique = ai_summarize(unique)

    # Fetch images
    if unique:
        print("\n[图片] 获取配图...")
        unique = fetch_images_for_items(unique)

    # Save
    kb = {"date": date_str, "total": len(unique), "items": unique}
    kb_path = DATA_DIR / f"report_{date_str}.json"
    kb_path.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n知识库: {kb_path}")

    # Stats
    from collections import Counter
    cat_counts = Counter(i["platform"] for i in unique)
    print("\n分类统计:")
    for cat in CATEGORIES:
        count = cat_counts.get(cat, 0)
        cfg = CATEGORIES[cat]
        print(f"  {cfg['icon']} {cat}: {count}")
    type_counts = Counter(i.get("content_type", "未知") for i in unique)
    print("\n内容类型:")
    for t, c in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        ti = CONTENT_TYPES.get(t, {"icon": "❓", "label": t})
        print(f"  {ti['icon']} {ti['label']}: {c}")

    print(f"\n{'=' * 60}")
    print(f"完成! {len(unique)} 条资讯")
    print(f"{'=' * 60}")

    return unique

if __name__ == "__main__":
    main()
