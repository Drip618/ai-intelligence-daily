# AI Intelligence Daily - 全球资讯速递

> 每日自动从全球 50+ 数据源获取资讯，AI 智能总结分析

## 🌟 项目特性

- **全球数据源** - 覆盖 GitHub, HuggingFace, YouTube, B站, Reddit, Hacker News 等 50+ 站点
- **智能分类** - 自媒体、影视后期、审美提升、AI行业、工具插件
- **AI 总结** - 通义千问大模型智能解读每条资讯
- **精美 UI** - 响应式设计，支持深色/浅色/护眼三种主题
- **多端支持** - Web 浏览器 + 桌面应用 + 移动端 PWA
- **PDF 导出** - 一键导出排版精美的 PDF 报告
- **自定义 API** - 支持用户添加任意数据源
- **推送渠道** - 预留邮件、Telegram、企业微信等推送方式

## 📁 项目结构

```
project_v2/
├── generate_report.py        # 数据获取与处理核心
├── generate_browser_friendly.py  # HTML/PDF 生成器
├── run.sh                    # 一键运行脚本
├── config/                   # 用户配置目录
│   └── user_config.json      # 用户自定义设置
├── data/                     # 数据存储目录
│   └── knowledge/
│       └── daily_reports/    # 每日报告 JSON
├── output/                   # 输出目录
│   ├── Daily_Report_*.html   # 每日 HTML 报告
│   └── Daily_Report_*.pdf    # 每日 PDF 报告
├── electron/                 # Electron 桌面应用
│   ├── main.js
│   ├── renderer.js
│   ├── index.html
│   └── package.json
├── .github/
│   └── workflows/
│       └── daily-report.yml  # GitHub Actions 自动化
└── README.md                 # 本文件
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 依赖库：`requests`, `weasyprint`

### 安装

```bash
# 安装依赖
pip install requests weasyprint

# 克隆项目
git clone <your-repo-url>
cd project_v2
```

### 运行

```bash
# 方法1: 一键运行
./run.sh

# 方法2: 分步运行
python3 generate_report.py --no-ai
python3 generate_browser_friendly.py
```

### 配置 API Key（可选）

创建 `.env` 文件启用 AI 总结功能：

```env
DASHSCOPE_API_KEY=your-api-key-here
GITHUB_TOKEN=your-github-token
```

### 查看报告

运行后在 `output/` 目录下找到生成的 HTML 和 PDF 文件：

```bash
open output/Daily_Report_$(date +%Y-%m-%d).html
```

## ⚙️ 自定义设置

在浏览器中打开 HTML 报告后，点击右上角 **⚙️ 设置** 按钮：

- **主题设置** - 深色/浅色/护眼三种模式
- **每分类条数** - 控制每个分类显示的内容数量
- **自定义 API** - 添加你自己的数据源接口
- **推送渠道** - 配置邮件、Telegram、企业微信等推送方式

## 🌐 数据源

### 自媒体
- YouTube Trending
- B站热门
- Product Hunt
- Substack Trending

### 影视后期
- Blender Community
- After Effects Plugins
- DaVinci Resolve
- Video Copilot
- Greyscalegorilla

### 审美提升
- Dribbble Trending
- Behance Featured
- Pinterest Trending
- Awwwards SOTD
- Designspiration

### AI行业
- HuggingFace Models
- GitHub AI Search
- GitHub Trending AI
- Papers With Code
- arXiv AI Papers
- Hacker News
- TechCrunch
- The Verge

### 工具插件
- GitHub Trending
- Chrome Extensions
- AlternativeTo
- Indie Hackers

## 📱 桌面应用（Electron）

```bash
cd electron
npm install
npm start
```

## 🌍 部署到 GitHub Pages

1. 启用 GitHub Actions
2. 推送代码到仓库
3. Actions 会自动每日生成报告并发布到 GitHub Pages

## 📄 License

MIT License - 仅供个人学习与行业洞察使用

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**AI Intelligence Daily** - 让全球资讯触手可及 🌐
