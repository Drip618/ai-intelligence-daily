#!/usr/bin/env python3
"""AI Intelligence Daily - Beautiful Browser UI & PDF Generator"""

import json
from datetime import datetime
from pathlib import Path
from weasyprint import HTML

OUTPUT_DIR = Path(__file__).parent / "output"
KB_DIR = Path(__file__).parent / "data" / "knowledge" / "daily_reports"
CONFIG_DIR = Path(__file__).parent / "config"

CATS = {
    "自媒体": {"icon": "📱", "color": "#F59E0B", "gradient": "from-amber-500 to-orange-600"},
    "影视后期": {"icon": "🎬", "color": "#EF4444", "gradient": "from-red-500 to-rose-600"},
    "审美提升": {"icon": "🎨", "color": "#8B5CF6", "gradient": "from-violet-500 to-purple-600"},
    "AI行业": {"icon": "🤖", "color": "#3B82F6", "gradient": "from-blue-500 to-indigo-600"},
    "工具插件": {"icon": "🧰", "color": "#10B981", "gradient": "from-emerald-500 to-teal-600"},
}

TYPE_LABELS = {
    "文字": {"icon": "📝", "label": "文字资讯", "badge": "bg-blue-100 text-blue-700"},
    "图片": {"icon": "🖼️", "label": "图片内容", "badge": "bg-purple-100 text-purple-700"},
    "视频": {"icon": "🎥", "label": "视频教程", "badge": "bg-red-100 text-red-700"},
    "软件": {"icon": "💻", "label": "软件工具", "badge": "bg-green-100 text-green-700"},
    "插件": {"icon": "🔌", "label": "浏览器插件", "badge": "bg-teal-100 text-teal-700"},
}

THEMES = {
    "dark": {
        "name": "深色模式", "icon": "🌙",
        "bg": "#0a0a0f", "bgSecondary": "#12121a",
        "card": "#1a1a24", "cardHover": "#22222e",
        "text": "#f1f1f6", "textSecondary": "#8888a0",
        "accent": "#6366f1", "accentHover": "#818cf8",
        "border": "#2a2a3a", "borderLight": "#3a3a4a",
        "shadow": "rgba(99,102,241,0.15)",
        "headerBg": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
    },
    "light": {
        "name": "浅色模式", "icon": "☀️",
        "bg": "#f8f9fa", "bgSecondary": "#ffffff",
        "card": "#ffffff", "cardHover": "#f8f9ff",
        "text": "#1a1a2e", "textSecondary": "#6b7280",
        "accent": "#4f46e5", "accentHover": "#6366f1",
        "border": "#e5e7eb", "borderLight": "#d1d5db",
        "shadow": "rgba(79,70,229,0.1)",
        "headerBg": "linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #a855f7 100%)",
    },
    "eye": {
        "name": "护眼模式", "icon": "🌿",
        "bg": "#f0f7f0", "bgSecondary": "#e8f5e8",
        "card": "#ffffff", "cardHover": "#f0f8f0",
        "text": "#1a3a1a", "textSecondary": "#5a8a5a",
        "accent": "#16a34a", "accentHover": "#15803d",
        "border": "#c8e6c9", "borderLight": "#a5d6a7",
        "shadow": "rgba(22,163,74,0.1)",
        "headerBg": "linear-gradient(135deg, #16a34a 0%, #15803d 50%, #0f5132 100%)",
    },
}


def load_config():
    config_path = CONFIG_DIR / "user_config.json"
    if config_path.exists():
        return json.loads(config_path.read_text(encoding="utf-8"))
    return {
        "theme": "dark",
        "target_count": 50,
        "per_category": 10,
        "custom_apis": [],
        "push_channels": [],
    }


def load_kb(date_str=None):
    date_str = date_str or datetime.now().strftime("%Y-%m-%d")
    p = KB_DIR / f"report_{date_str}.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None


def group_items(items):
    groups = {cat: [] for cat in CATS}
    for item in items:
        cat = item.get("platform", "其他")
        if cat in groups:
            groups[cat].append(item)
        else:
            groups["AI行业"].append(item)
    return groups


def sort_by_length(items):
    def text_len(item):
        return len(item.get("summary", "") + item.get("detail", item.get("raw_detail", "")))
    return sorted(items, key=text_len)


def clean_link(url):
    if not url or url == "#":
        return "#"
    if url.startswith("//"):
        return "https:" + url
    return url


def build_html(kb):
    date_str = kb.get("date", datetime.now().strftime("%Y-%m-%d"))
    items = kb.get("items", [])
    total = len(items)
    groups = group_items(items)

    cat_order = list(CATS.keys())
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        date_display = date_obj.strftime("%Y年%m月%d日")
        day_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        day_name = day_names[date_obj.weekday()]
    except Exception:
        date_display = date_str
        day_name = ""

    config = load_config()
    theme_key = config.get("theme", "dark")
    theme = THEMES.get(theme_key, THEMES["dark"])

    # Sort items within each category
    for cat in cat_order:
        groups[cat] = sort_by_length(groups[cat])

    H = []

    # HTML Header
    H.append(f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Intelligence Daily - {date_display}</title>
<style>
:root {{
    --bg: {theme["bg"]};
    --bg-secondary: {theme["bgSecondary"]};
    --card: {theme["card"]};
    --card-hover: {theme["cardHover"]};
    --text: {theme["text"]};
    --text-secondary: {theme["textSecondary"]};
    --accent: {theme["accent"]};
    --accent-hover: {theme["accentHover"]};
    --border: {theme["border"]};
    --border-light: {theme["borderLight"]};
    --shadow: {theme["shadow"]};
    --header-bg: {theme["headerBg"]};
    --radius: 12px;
    --radius-sm: 8px;
    --font-sans: -apple-system, "PingFang SC", "Microsoft YaHei", "Noto Sans SC", "Helvetica Neue", sans-serif;
    --font-mono: "SF Mono", "Fira Code", monospace;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
    font-family: var(--font-sans);
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    transition: background .3s, color .3s;
    min-height: 100vh;
}}

/* ===== Scrollbar ===== */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: var(--accent); }}

/* ===== Navigation ===== */
.nav {{
    position: fixed; top: 0; left: 0; right: 0; height: 56px;
    background: var(--bg-secondary); border-bottom: 1px solid var(--border);
    display: flex; align-items: center; padding: 0 20px; z-index: 100;
    backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
}}
.nav-logo {{
    font-size: 14px; font-weight: 700; color: var(--text);
    display: flex; align-items: center; gap: 8px;
}}
.nav-logo-icon {{
    width: 28px; height: 28px; background: var(--accent);
    border-radius: 6px; display: flex; align-items: center; justify-content: center;
    font-size: 14px;
}}
.nav-title {{ font-size: 14px; font-weight: 700; }}
.nav-subtitle {{ font-size: 10px; color: var(--text-secondary); font-weight: 400; }}
.nav-right {{ margin-left: auto; display: flex; align-items: center; gap: 8px; }}
.nav-btn {{
    padding: 6px 12px; background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius-sm); color: var(--text-secondary);
    font-size: 12px; cursor: pointer; transition: all .2s;
    display: flex; align-items: center; gap: 4px;
}}
.nav-btn:hover {{ border-color: var(--accent); color: var(--accent); }}
.nav-btn.active {{ background: var(--accent); color: #fff; border-color: var(--accent); }}

/* ===== Category Tabs ===== */
.category-nav {{
    position: fixed; top: 56px; left: 0; right: 0; height: 44px;
    background: var(--bg-secondary); border-bottom: 1px solid var(--border);
    display: flex; align-items: center; padding: 0 16px; z-index: 99;
    gap: 6px; overflow-x: auto; scrollbar-width: none;
    -webkit-overflow-scrolling: touch;
}}
.category-nav::-webkit-scrollbar {{ display: none; }}
.cat-tab {{
    display: inline-flex; align-items: center; gap: 4px;
    padding: 6px 14px; border-radius: 20px; font-size: 12px;
    color: var(--text-secondary); cursor: pointer; border: 1px solid transparent;
    transition: all .2s; white-space: nowrap; user-select: none;
    font-weight: 500;
}}
.cat-tab:hover {{ background: var(--card); color: var(--text); border-color: var(--border); }}
.cat-tab.active {{ background: var(--accent); color: #fff; font-weight: 600; }}
.cat-tab .tab-count {{
    font-size: 10px; opacity: .7;
    background: rgba(255,255,255,.2); padding: 1px 6px; border-radius: 10px;
}}
.cat-tab:not(.active) .tab-count {{
    background: var(--card); opacity: 1;
}}

/* ===== Header ===== */
.header {{
    background: var(--header-bg);
    padding: 48px 20px 32px; text-align: center;
    margin-top: 100px; position: relative; overflow: hidden;
}}
.header::before {{
    content: ''; position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,102,241,.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(168,85,247,.08) 0%, transparent 50%);
    animation: glow 8s ease-in-out infinite alternate;
}}
@keyframes glow {{ 0% {{ opacity: .5; }} 100% {{ opacity: 1; }} }}
.header-label {{
    font-size: 10px; font-weight: 600; letter-spacing: 3px;
    color: rgba(255,255,255,.4); margin-bottom: 8px; position: relative;
}}
.header-title {{
    font-size: 28px; font-weight: 800; margin-bottom: 4px;
    color: #fff; position: relative;
}}
.header-date {{
    font-size: 13px; color: rgba(255,255,255,.35);
    margin-bottom: 20px; position: relative;
}}
.header-stats {{
    display: flex; justify-content: center; gap: 36px; position: relative;
}}
.stat {{ text-align: center; }}
.stat-num {{ font-size: 28px; font-weight: 800; display: block; color: #fff; }}
.stat-label {{ font-size: 11px; color: rgba(255,255,255,.35); }}

/* ===== Main Container ===== */
.container {{
    max-width: 1280px; margin: 0 auto; padding: 20px 16px 40px;
}}

/* ===== Section ===== */
.section {{ margin-bottom: 32px; }}
.content-section {{ display: none; animation: fadeIn .3s ease; }}
.content-section.active {{ display: block; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: translateY(0); }} }}

.section-anchor {{ display: block; position: relative; top: -110px; visibility: hidden; }}

/* ===== Category Header ===== */
.cat-header {{
    display: flex; align-items: center; gap: 10px;
    padding: 12px 0 16px; margin-bottom: 16px;
    border-bottom: 2px solid var(--accent);
}}
.cat-icon {{ font-size: 24px; }}
.cat-name {{ font-size: 18px; font-weight: 700; color: var(--accent); }}
.cat-desc {{ font-size: 12px; color: var(--text-secondary); margin-left: 8px; }}
.cat-count {{
    margin-left: auto; font-size: 11px; color: var(--text-secondary);
    background: var(--card); padding: 4px 12px; border-radius: 12px;
    border: 1px solid var(--border);
}}

/* ===== Grid Layout ===== */
.grid-layout {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 16px;
}}

/* ===== Card ===== */
.card {{
    background: var(--card); border-radius: var(--radius);
    overflow: hidden; border: 1px solid var(--border);
    transition: all .3s; display: flex; flex-direction: column;
}}
.card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 32px var(--shadow);
    border-color: var(--accent);
}}
.card-img {{
    width: 100%; aspect-ratio: 16/9; overflow: hidden;
    background: var(--bg); position: relative;
}}
.card-img img {{
    width: 100%; height: 100%; object-fit: cover; display: block;
    transition: transform .4s;
}}
.card:hover .card-img img {{ transform: scale(1.05); }}
.card-img-placeholder {{
    width: 100%; height: 100%;
    display: flex; align-items: center; justify-content: center;
    font-size: 32px; opacity: .15;
}}
.card-body {{ padding: 14px; flex: 1; display: flex; flex-direction: column; }}
.card-header {{ display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 8px; }}
.card-type-badge {{
    font-size: 10px; font-weight: 600; padding: 3px 8px;
    border-radius: 4px; display: inline-flex; align-items: center; gap: 3px;
    background: var(--bg); color: var(--text-secondary);
}}
.card-hot {{
    font-size: 11px; font-weight: 700; color: #ef4444;
    display: flex; align-items: center; gap: 2px;
}}
.card-title {{
    font-size: 14px; font-weight: 700; margin-bottom: 6px;
    line-height: 1.4; color: var(--text);
    display: -webkit-box; -webkit-line-clamp: 2;
    -webkit-box-orient: vertical; overflow: hidden;
}}
.card-summary {{
    font-size: 12px; font-weight: 600; color: var(--accent);
    background: color-mix(in srgb, var(--accent) 8%, transparent);
    padding: 4px 10px; border-radius: 6px;
    margin-bottom: 8px; align-self: flex-start;
}}
.card-detail {{
    font-size: 12px; color: var(--text-secondary); line-height: 1.6;
    margin-bottom: 10px; white-space: pre-wrap; flex: 1;
    display: -webkit-box; -webkit-line-clamp: 3;
    -webkit-box-orient: vertical; overflow: hidden;
}}
.card-footer {{
    display: flex; align-items: center; gap: 6px;
    font-size: 11px; flex-wrap: wrap; margin-top: auto;
    padding-top: 10px; border-top: 1px solid var(--border);
}}
.card-source {{
    font-weight: 600; color: var(--accent);
    background: var(--bg); padding: 2px 8px; border-radius: 4px;
}}
.card-link {{
    color: var(--accent); text-decoration: none; font-weight: 600;
    font-size: 11px; margin-left: auto; cursor: pointer;
    transition: color .2s;
}}
.card-link:hover {{ color: var(--accent-hover); }}

/* ===== Settings Modal ===== */
.modal-overlay {{
    position: fixed; inset: 0; background: rgba(0,0,0,.6);
    backdrop-filter: blur(4px); z-index: 200;
    display: none; align-items: center; justify-content: center;
}}
.modal-overlay.active {{ display: flex; }}
.modal {{
    background: var(--bg-secondary); border: 1px solid var(--border);
    border-radius: 16px; width: 90%; max-width: 560px;
    max-height: 80vh; overflow-y: auto;
    box-shadow: 0 24px 48px rgba(0,0,0,.3);
}}
.modal-header {{
    display: flex; align-items: center; padding: 20px;
    border-bottom: 1px solid var(--border);
}}
.modal-title {{ font-size: 18px; font-weight: 700; flex: 1; }}
.modal-close {{
    width: 32px; height: 32px; border-radius: 8px;
    border: 1px solid var(--border); background: var(--card);
    color: var(--text-secondary); cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; transition: all .2s;
}}
.modal-close:hover {{ border-color: #ef4444; color: #ef4444; }}
.modal-body {{ padding: 20px; }}
.setting-group {{ margin-bottom: 20px; }}
.setting-label {{ font-size: 13px; font-weight: 600; color: var(--text); margin-bottom: 8px; }}
.setting-desc {{ font-size: 11px; color: var(--text-secondary); margin-bottom: 10px; }}
.setting-input {{
    width: 100%; padding: 10px 12px; background: var(--card);
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    color: var(--text); font-size: 13px; outline: none;
    transition: border-color .2s;
}}
.setting-input:focus {{ border-color: var(--accent); }}
.setting-select {{
    padding: 10px 12px; background: var(--card);
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    color: var(--text); font-size: 13px; outline: none; cursor: pointer;
}}
.setting-btn {{
    padding: 10px 20px; background: var(--accent); color: #fff;
    border: none; border-radius: var(--radius-sm); font-size: 13px;
    font-weight: 600; cursor: pointer; transition: all .2s;
}}
.setting-btn:hover {{ background: var(--accent-hover); }}
.setting-btn-secondary {{
    padding: 10px 20px; background: var(--card); color: var(--text);
    border: 1px solid var(--border); border-radius: var(--radius-sm);
    font-size: 13px; font-weight: 600; cursor: pointer; transition: all .2s;
}}
.setting-btn-secondary:hover {{ border-color: var(--accent); color: var(--accent); }}

/* ===== Footer ===== */
.footer {{
    margin-top: 48px; padding: 32px 16px; text-align: center;
    border-top: 1px solid var(--border);
}}
.footer-icons {{ font-size: 24px; margin-bottom: 12px; letter-spacing: 6px; }}
.footer-text {{ font-size: 13px; color: var(--text-secondary); line-height: 1.7; max-width: 500px; margin: 0 auto 16px; }}
.footer-text strong {{ color: var(--accent); }}
.footer-links {{ display: flex; justify-content: center; gap: 16px; flex-wrap: wrap; margin-bottom: 12px; }}
.footer-link {{
    font-size: 12px; color: var(--accent); text-decoration: none;
    cursor: pointer; transition: color .2s;
}}
.footer-link:hover {{ color: var(--accent-hover); }}
.footer-bottom {{ font-size: 10px; color: var(--text-secondary); opacity: .4; }}

/* ===== Responsive ===== */
@media (max-width: 768px) {{
    .header {{ padding: 36px 14px 24px; margin-top: 100px; }}
    .header-title {{ font-size: 24px; }}
    .header-stats {{ gap: 24px; }}
    .stat-num {{ font-size: 24px; }}
    .container {{ padding: 14px 12px 32px; }}
    .grid-layout {{ grid-template-columns: 1fr; gap: 12px; }}
    .nav {{ padding: 0 12px; }}
    .cat-tab {{ padding: 5px 10px; font-size: 11px; }}
}}
@media (min-width: 1024px) {{
    .container {{ padding: 24px 32px; }}
    .header {{ padding: 56px 24px 40px; }}
    .grid-layout {{ grid-template-columns: repeat(3, 1fr); }}
}}

/* ===== PDF Print ===== */
@media print {{
    @page {{ margin: 10mm; size: A4; }}
    .nav, .category-nav, .footer, .nav-right, .modal-overlay {{ display: none !important; }}
    body {{
        background: #fff !important; color: #1a1a2e !important;
        font-size: 11px !important; line-height: 1.5 !important;
    }}
    .header {{
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;
        padding: 20px !important; margin-top: 0 !important;
    }}
    .header-label, .header-date {{ color: rgba(255,255,255,.5) !important; }}
    .header-title, .stat-num {{ color: #fff !important; }}
    .header-stats, .header-label, .header-title, .header-date, .stat {{ position: relative !important; }}
    .container {{ padding: 4mm !important; max-width: 100% !important; }}
    .content-section {{ display: block !important; margin-bottom: 16px !important; }}
    .cat-header {{ border-bottom-color: #4f46e5 !important; padding: 8px 0 10px !important; }}
    .cat-name {{ color: #1a1a2e !important; }}
    .cat-icon {{ color: #1a1a2e !important; }}
    .cat-count {{ background: #f0f0f0 !important; color: #666 !important; border-color: #ddd !important; }}
    .grid-layout {{
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 10px !important;
    }}
    .card {{
        break-inside: avoid; page-break-inside: avoid;
        border: 1px solid #e5e7eb !important; background: #fff !important;
        box-shadow: none !important;
    }}
    .card:hover {{ transform: none !important; box-shadow: none !important; }}
    .card-img {{ background: #f9fafb !important; }}
    .card-img-placeholder {{ opacity: .1 !important; }}
    .card-body {{ padding: 10px !important; }}
    .card-title {{ color: #1a1a2e !important; font-size: 11px !important; }}
    .card-summary {{
        color: #4f46e5 !important; background: rgba(79,70,229,.05) !important;
        font-size: 10px !important;
    }}
    .card-detail {{ color: #4b5563 !important; font-size: 10px !important; }}
    .card-type-badge {{ font-size: 9px !important; background: #f3f4f6 !important; }}
    .card-footer {{ border-top-color: #e5e7eb !important; font-size: 9px !important; }}
    .card-source {{ background: #f3f4f6 !important; color: #4f46e5 !important; }}
    .card-link {{ color: #4f46e5 !important; }}
}}
</style>
</head>
<body>
''')

    # Navigation
    H.append(f'''<nav class="nav">
    <div class="nav-logo">
        <div class="nav-logo-icon">🚀</div>
        <div>
            <div class="nav-title">AI Intelligence Daily</div>
            <div class="nav-subtitle">全球资讯速递</div>
        </div>
    </div>
    <div class="nav-right">
        <button class="nav-btn" onclick="toggleTheme()">🎨 主题</button>
        <button class="nav-btn" onclick="openSettings()">⚙️ 设置</button>
        <button class="nav-btn" onclick="window.print()">📄 导出PDF</button>
    </div>
</nav>''')

    # Category Navigation
    H.append(f'<div class="category-nav" id="categoryNav">')
    H.append(f'<div class="cat-tab active" data-cat="all">📊 全部<span class="tab-count">{total}</span></div>')
    for cat in cat_order:
        cfg = CATS[cat]
        cnt = len(groups.get(cat, []))
        H.append(f'<div class="cat-tab" data-cat="{cat}">{cfg["icon"]} {cat}<span class="tab-count">{cnt}</span></div>')
    H.append('</div>')

    # Header
    H.append(f'''<header class="header">
    <div class="header-label">GLOBAL INTELLIGENCE</div>
    <div class="header-title">每日全球资讯速递</div>
    <div class="header-date">{date_display} · {day_name}</div>
    <div class="header-stats">
        <div class="stat"><span class="stat-num">{total}</span><span class="stat-label">精选资讯</span></div>
        <div class="stat"><span class="stat-num">{len(cat_order)}</span><span class="stat-label">内容板块</span></div>
        <div class="stat"><span class="stat-num">50+</span><span class="stat-label">全球数据源</span></div>
    </div>
</header>''')

    # Main Content
    H.append('<main class="container">')

    for cat in cat_order:
        p_items = groups[cat]
        if not p_items:
            continue
        cfg = CATS[cat]
        H.append(f'<div class="section content-section" id="section-{cat}" data-cat="{cat}">')
        H.append(f'<span class="section-anchor" id="anchor-{cat}"></span>')
        H.append(f'<div class="cat-header">')
        H.append(f'<span class="cat-icon">{cfg["icon"]}</span>')
        H.append(f'<span class="cat-name">{cat}</span>')
        H.append(f'<span class="cat-desc">{cfg.get("desc", "")}</span>')
        H.append(f'<span class="cat-count">{len(p_items)} 条</span>')
        H.append('</div>')
        H.append('<div class="grid-layout">')

        for item in p_items:
            summary = item.get("summary", "")
            detail = item.get("detail", item.get("raw_detail", ""))
            if not detail:
                detail = summary

            img_url = item.get("image_url", "")
            icon = cfg["icon"]
            content_type = item.get("content_type", "文字")
            type_info = TYPE_LABELS.get(content_type, TYPE_LABELS["文字"])
            link = clean_link(item.get("url", "#"))
            extra = item.get("extra_info", {})
            hot = item.get("hot_score", 0)

            H.append('<div class="card">')
            if img_url:
                H.append(f'<div class="card-img"><img src="{img_url}" alt="" loading="lazy" onerror="this.parentElement.innerHTML=\'<div class=\\\'card-img-placeholder\\\'>{icon}</div>\'"></div>')
            else:
                H.append(f'<div class="card-img"><div class="card-img-placeholder">{icon}</div></div>')

            H.append('<div class="card-body">')
            H.append('<div class="card-header">')
            H.append(f'<span class="card-type-badge">{type_info["icon"]} {type_info["label"]}</span>')
            if hot and str(hot).replace(",", "").isdigit() and int(str(hot).replace(",", "")) > 100:
                H.append(f'<span class="card-hot">🔥 {hot:,}</span>')
            H.append('</div>')
            H.append(f'<div class="card-title">{item["title"]}</div>')
            if summary:
                H.append(f'<div class="card-summary">💡 {summary}</div>')
            H.append(f'<div class="card-detail">{detail[:180]}{"..." if len(detail) > 180 else ""}</div>')
            H.append('<div class="card-footer">')
            H.append(f'<span class="card-source">{item.get("source", "未知")}</span>')
            H.append(f'<a href="{link}" class="card-link" target="_blank" rel="noopener">查看原文 →</a>')
            H.append('</div></div></div>')
        H.append('</div></div>')

    H.append('</main>')

    # Footer
    footer_text = """<strong>AI Intelligence Daily</strong><br>
    每日自动从全球 50+ 数据源获取资讯，AI 智能总结分析。<br>
    仅供个人学习与行业洞察使用。
    """
    year = datetime.now().year
    H.append(f'''<footer class="footer">
    <div class="footer-icons">🌐 🤖 🎨 🎬 🧰</div>
    <div class="footer-text">{footer_text}</div>
    <div class="footer-links">
        <a class="footer-link" href="#" onclick="openSettings(); return false;">⚙️ 设置</a>
        <a class="footer-link" href="#" onclick="window.print(); return false;">📄 导出PDF</a>
        <a class="footer-link" href="https://github.com" target="_blank">🔗 GitHub</a>
    </div>
    <div class="footer-bottom">© {year} AI Intelligence Daily · 全球资讯 · AI驱动</div>
</footer>''')

    # Settings Modal
    H.append('''<div class="modal-overlay" id="settingsModal">
    <div class="modal">
        <div class="modal-header">
            <div class="modal-title">⚙️ 系统设置</div>
            <button class="modal-close" onclick="closeSettings()">✕</button>
        </div>
        <div class="modal-body">
            <div class="setting-group">
                <div class="setting-label">🎨 主题设置</div>
                <div class="setting-desc">选择你喜欢的界面风格</div>
                <select class="setting-select" id="themeSelect" onchange="applyTheme(this.value)">
                    <option value="dark">🌙 深色模式</option>
                    <option value="light">☀️ 浅色模式</option>
                    <option value="eye">🌿 护眼模式</option>
                </select>
            </div>
            <div class="setting-group">
                <div class="setting-label">📊 每分类条数</div>
                <div class="setting-desc">每个分类显示的内容数量</div>
                <input class="setting-input" type="number" id="perCategoryInput" value="10" min="5" max="20">
            </div>
            <div class="setting-group">
                <div class="setting-label">🔌 自定义 API</div>
                <div class="setting-desc">添加你自己的数据源</div>
                <div id="customApiList"></div>
                <button class="setting-btn-secondary" onclick="addCustomApi()" style="margin-top: 8px;">+ 添加 API</button>
            </div>
            <div class="setting-group">
                <div class="setting-label">📮 推送渠道</div>
                <div class="setting-desc">选择接收每日推送的方式（预留）</div>
                <select class="setting-select" id="pushChannel">
                    <option value="">暂未配置</option>
                    <option value="email">📧 邮件推送</option>
                    <option value="telegram">💬 Telegram Bot</option>
                    <option value="wechat">📱 企业微信</option>
                    <option value="webhook">🔗 Webhook</option>
                </select>
            </div>
            <button class="setting-btn" onclick="saveSettings()" style="width: 100%;">💾 保存设置</button>
        </div>
    </div>
</div>''')

    # JavaScript
    themes_json = json.dumps(THEMES, ensure_ascii=False)
    cat_order_json = json.dumps(cat_order, ensure_ascii=False)

    js = f'''<script>
const themes = {themes_json};
const catOrder = {cat_order_json};
let currentTheme = "{theme_key}";

function applyTheme(key) {{
    const t = themes[key]; if (!t) return;
    currentTheme = key;
    const r = document.documentElement.style;
    r.setProperty("--bg", t.bg);
    r.setProperty("--bg-secondary", t.bgSecondary);
    r.setProperty("--card", t.card);
    r.setProperty("--card-hover", t.cardHover);
    r.setProperty("--text", t.text);
    r.setProperty("--text-secondary", t.textSecondary);
    r.setProperty("--accent", t.accent);
    r.setProperty("--accent-hover", t.accentHover);
    r.setProperty("--border", t.border);
    r.setProperty("--border-light", t.borderLight);
    r.setProperty("--shadow", t.shadow);
    r.setProperty("--header-bg", t.headerBg);
    localStorage.setItem("aidTheme", key);
}}

function toggleTheme() {{
    const order = ["dark", "light", "eye"];
    const idx = order.indexOf(currentTheme);
    const next = order[(idx + 1) % order.length];
    applyTheme(next);
    document.getElementById("themeSelect").value = next;
}}

function switchCategory(cat) {{
    document.querySelectorAll('.cat-tab').forEach(t => {{
        t.classList.toggle('active', t.dataset.cat === cat);
    }});
    document.querySelectorAll('.content-section').forEach(s => {{
        s.classList.toggle('active', cat === 'all' || s.dataset.cat === cat);
    }});
    window.scrollTo({{top: 0, behavior: 'smooth'}});
}}

function handleImgError(img, icon) {{
    img.parentElement.innerHTML = '<div class="card-img-placeholder">' + icon + '</div>';
}}

document.querySelectorAll('.cat-tab').forEach(tab => {{
    tab.addEventListener('click', () => switchCategory(tab.dataset.cat));
}});

function openSettings() {{
    document.getElementById('settingsModal').classList.add('active');
}}
function closeSettings() {{
    document.getElementById('settingsModal').classList.remove('active');
}}
document.getElementById('settingsModal').addEventListener('click', (e) => {{
    if (e.target === e.currentTarget) closeSettings();
}});

let customApis = [];
function addCustomApi() {{
    const id = Date.now();
    customApis.push({{id, name: "", url: "", enabled: true}});
    renderCustomApis();
}}
function renderCustomApis() {{
    const container = document.getElementById('customApiList');
    if (!container) return;
    container.innerHTML = customApis.map(api => `
        <div style="display:flex;gap:8px;margin-bottom:8px;align-items:center;">
            <input class="setting-input" placeholder="名称" value="${{api.name}}" onchange="customApis.find(a=>a.id===${{api.id}}).name=this.value" style="flex:1;">
            <input class="setting-input" placeholder="API URL" value="${{api.url}}" onchange="customApis.find(a=>a.id===${{api.id}}).url=this.value" style="flex:2;">
            <button class="setting-btn" style="padding:6px 10px;background:#ef4444;" onclick="customApis=customApis.filter(a=>a.id!==${{api.id}});renderCustomApis();">✕</button>
        </div>
    `).join('');
}}
function saveSettings() {{
    const theme = document.getElementById('themeSelect').value;
    const perCat = parseInt(document.getElementById('perCategoryInput').value) || 10;
    const push = document.getElementById('pushChannel').value;
    const config = {{
        theme, per_category: perCat, custom_apis: customApis, push_channels: push ? [push] : []
    }};
    localStorage.setItem("aidConfig", JSON.stringify(config));
    applyTheme(theme);
    alert("设置已保存！");
    closeSettings();
}}

(function() {{
    const saved = localStorage.getItem("aidConfig");
    if (saved) {{
        try {{
            const config = JSON.parse(saved);
            if (config.theme) {{
                applyTheme(config.theme);
                const sel = document.getElementById("themeSelect");
                if (sel) sel.value = config.theme;
            }}
            if (config.per_category) {{
                const inp = document.getElementById("perCategoryInput");
                if (inp) inp.value = config.per_category;
            }}
            if (config.custom_apis) {{
                customApis = config.custom_apis;
                renderCustomApis();
            }}
        }} catch(e) {{}}
    }}
    applyTheme(currentTheme);
    const sel = document.getElementById("themeSelect");
    if (sel) sel.value = currentTheme;
}})();
</script>'''
    H.append(js)
    H.append('</body></html>')
    return "\n".join(H)


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"))
    args = parser.parse_args()
    date_str = args.date
    kb = load_kb(date_str)
    if not kb:
        # Try to load the most recent KB
        if KB_DIR.exists():
            reports = sorted(KB_DIR.glob("report_*.json"), reverse=True)
            if reports:
                kb = json.loads(reports[0].read_text(encoding="utf-8"))
                print(f"Using most recent report: {reports[0].name}")
            else:
                print(f"No knowledge base found for {date_str}")
                return
        else:
            print(f"No knowledge base found for {date_str}")
            return

    print("Generating HTML...")
    html_content = build_html(kb)

    html_path = OUTPUT_DIR / f"Daily_Report_{date_str}.html"
    html_path.write_text(html_content, encoding="utf-8")
    print(f"HTML saved: {html_path}")

    pdf_path = OUTPUT_DIR / f"Daily_Report_{date_str}.pdf"
    print("Generating PDF...")
    HTML(string=html_content, base_url=str(html_path)).write_pdf(pdf_path)
    print(f"PDF saved: {pdf_path}")

    print(f"\nDone! {kb['total']} items")


if __name__ == "__main__":
    main()
