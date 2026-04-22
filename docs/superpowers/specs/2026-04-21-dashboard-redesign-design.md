# AI Intelligence Dashboard 重设计

**目标**: 将现有脚本升级为 Web Dashboard + 数据引擎架构，提供多主题、多语言、多内容源的资讯报告体验。

**架构**: FastAPI 后端（数据抓取引擎）+ 纯 HTML/CSS/JS 前端 Dashboard（主题切换、语言切换、PDF下载）

**技术栈**: Python 3.11+, FastAPI, Uvicorn, Jinja2, requests, weasyprint, CSS3

---

## 1. 架构设计

```
┌─────────────────────────────────────────────────┐
│                  Web Dashboard                    │
│  ┌─────────────┬──────────────┬────────────────┐ │
│  │  主题切换    │   语言切换    │   PDF 下载      │ │
│  │ 跟随/白/黑/护 │  中文/英文    │  竖屏/横屏      │ │
│  └─────────────┴──────────────┴────────────────┘ │
│  ┌─────────────────────────────────────────────┐ │
│  │           Content Cards Grid                 │ │
│  │  [大模型] [Agent] [HuggingFace] [YouTube]    │ │
│  │  [GitHub] [微博] [知乎] [小红书] ...         │ │
│  └─────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────┘
                   │ HTTP API (JSON)
┌──────────────────┴──────────────────────────────┐
│                FastAPI Backend                   │
│  GET  /api/items          - 所有资讯             │
│  POST /api/generate        - 触发抓取+AI总结      │
│  POST /api/pdf             - 生成PDF并返回        │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │            Fetch Engine                    │  │
│  │  fetch_llm_news()      - 大模型动态(5条)    │  │
│  │  fetch_agent_framework()  - Agent框架(3条) │  │
│  │  fetch_huggingface()      - HF模型(3条)     │  │
│  │  fetch_youtube()          - YouTube(3条)   │  │
│  │  fetch_github_trending()  - GitHub Trending│  │
│  │  fetch_github_tools()     - 工具/软件/插件  │  │
│  │  fetch_weibo/zhihu/...()  - 各平台热点      │  │
│  │  fetch_web_search()       - 搜索兜底        │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │            AI Summarizer                   │  │
│  │  summarize_items(items, lang) → detailed   │  │
│  └────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────┐  │
│  │            PDF Generator                   │  │
│  │  generate_pdf(items, orientation) → PDF    │  │
│  └────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

## 2. 内容源设计（全部为最近3天最热）

| 板块 | 数据源 | 数量 | 付费标识 |
|------|--------|------|---------|
| 大模型动态 | Web Search + 36Kr + IT之家 | 5 | 是 |
| AI Agent 框架 | GitHub + Web Search | 3 | 是 |
| HuggingFace 热门模型 | HF API + Web Search | 3 | 否 |
| YouTube 热门 | Web Search | 3 | 否 |
| GitHub Trending | github.com/trending 页面 | 10 | 是 |
| GitHub 工具/软件/插件 | GitHub Search API | 8 | 是 |
| 微博热搜 | weibo API + 搜索兜底 | 12 | 否 |
| 知乎热榜 | zhihu API + 搜索兜底 | 12 | 否 |
| 小红书热门 | 搜索 | 8 | 否 |
| 微信公众号 | 搜索 | 8 | 否 |

**去重**: 标题相似度 >= 0.6 视为重复，合并平台信息。

**AI 总结**: 每条200-500字，支持中英双语输出。

## 3. 前端设计

**Dashboard 结构**:
- 顶部导航栏：Logo + 日期 + 主题切换按钮 + 语言切换按钮
- 内容区：卡片网格布局，每个板块一个卡片组
- 底部操作栏：PDF下载按钮（选择竖屏/横屏）

**主题系统**:
- CSS 变量驱动
- 4种主题：跟随系统、白天、黑夜、护眼
- 通过 `data-theme` 属性切换

**语言系统**:
- 前端UI文本通过 JSON i18n 文件切换
- 后端AI总结内容通过 `lang` 参数控制
- 通过 `data-lang` 属性切换

**布局**:
- 响应式网格，最小卡片宽度 350px
- 卡片内：标题（1行）+ 摘要（2行）+ 详情（折叠）+ 来源标签 + 热度 + 链接

## 4. PDF 设计

**演示文稿风格**:
- 封面页：大标题、日期、统计数字
- 内容页：每页2-3条资讯，左对齐，来源标签，热度标识
- 摘要页：要点速览
- 尾页：生成时间、数据来源

**选项**:
- `orientation`: portrait（竖屏 210x297mm）/ landscape（横屏 297x210mm）
- 通过 POST `/api/pdf` 传递

## 5. 错误处理

- 单个平台抓取失败不影响其他平台
- 所有 fetcher 有 try/except 兜底
- AI 总结失败时使用原始内容
- PDF 生成失败返回 HTML

## 6. 文件结构

```
data_collect/
├── server.py                    # FastAPI 主入口
├── engine/
│   ├── fetchers/               # 数据抓取引擎
│   │   ├── __init__.py
│   │   ├── llm_news.py
│   │   ├── agent_framework.py
│   │   ├── huggingface.py
│   │   ├── youtube.py
│   │   ├── github_trending.py
│   │   ├── github_tools.py
│   │   ├── weibo.py
│   │   ├── zhihu.py
│   │   ├── xiaohongshu.py
│   │   ├── weixin.py
│   │   └── search.py
│   ├── summarizer.py           # AI 总结
│   ├── dedup.py               # 去重
│   └── pdf_generator.py        # PDF 生成
├── web/
│   ├── dashboard.html           # 主页面
│   ├── dashboard.js             # 前端逻辑
│   ├── themes.css               # 主题样式
│   └── i18n.json                # 多语言
├── data/
│   └── knowledge/
│       └── daily_reports/       # 知识库
├── .env
└── requirements.txt
```
