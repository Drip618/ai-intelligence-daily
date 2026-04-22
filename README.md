# AI Intelligence Daily - 全球资讯速递

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  🚀 每日自动从全球 50+ 数据源获取资讯<br>
  🤖 AI 智能总结分析 | 🎨 精美 UI | 📱 多端支持
</p>

---

## ✨ 项目特性

| 特性 | 说明 |
|------|------|
| **全球数据源** | 覆盖 GitHub, HuggingFace, YouTube, B站, Reddit, Hacker News 等 50+ 站点 |
| **智能分类** | 自媒体、影视后期、审美提升、AI行业、工具插件 |
| **AI 总结** | 通义千问大模型智能解读每条资讯 |
| **精美 UI** | 响应式设计，支持深色/浅色/护眼三种主题 |
| **多端支持** | Web 浏览器 + 桌面应用 + 移动端 PWA |
| **PDF 导出** | 一键导出排版精美的 PDF 报告 |
| **自定义 API** | 支持用户添加任意数据源 |
| **推送渠道** | 预留邮件、Telegram、企业微信等推送方式 |

## 📸 界面预览

<div align="center">
  <table>
    <tr>
      <td><strong>深色模式</strong></td>
      <td><strong>浅色模式</strong></td>
    </tr>
    <tr>
      <td>🌙 沉浸式深色体验</td>
      <td>☀️ 清爽浅色界面</td>
    </tr>
  </table>
</div>

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 依赖库：`requests`, `weasyprint`

### 安装

```bash
# 克隆项目
git clone https://github.com/YOUR_USERNAME/ai-intelligence-daily.git
cd ai-intelligence-daily

# 安装依赖
pip install -r requirements.txt
```

### 运行

```bash
# 方法1: 一键运行
./run.sh

# 方法2: 分步运行
python3 generate_report.py --no-ai
python3 generate_browser_friendly.py
```

### 查看报告

```bash
# macOS
open output/Daily_Report_$(date +%Y-%m-%d).html

# Linux
xdg-open output/Daily_Report_$(date +%Y-%m-%d).html

# Windows
start output\Daily_Report_%DATE:~0,10%.html
```

## ⚙️ 配置

### 环境变量（可选）

创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=your-api-key-here
GITHUB_TOKEN=your-github-token
```

### 自定义设置

在浏览器中打开 HTML 报告 → 点击右上角 **⚙️ 设置**：

- 🎨 **主题切换** - 深色/浅色/护眼
- 📊 **每分类条数** - 控制显示数量
- 🔌 **自定义 API** - 添加数据源
- 📮 **推送渠道** - 配置推送方式

## 🌐 数据源

### 自媒体
- YouTube Trending / B站热门
- Product Hunt / Substack

### 影视后期
- Blender Community / AE Plugins
- DaVinci Resolve / Video Copilot

### 审美提升
- Dribbble / Behance / Pinterest
- Awwwards SOTD / Designspiration

### AI行业
- HuggingFace / GitHub AI
- arXiv / Hacker News
- TechCrunch / The Verge

### 工具插件
- GitHub Trending / Chrome Extensions
- AlternativeTo / Indie Hackers

## 🖥️ 桌面应用

```bash
cd electron
npm install
npm start
```

## 🌍 自动化部署

### GitHub Actions

项目已配置 GitHub Actions，每天自动运行：

1. Fork 或克隆此仓库
2. 在 Settings → Secrets 中配置 API Keys
3. Actions 会每天 08:00 (北京时间) 自动生成报告

### GitHub Pages

报告会自动部署到 `https://YOUR_USERNAME.github.io/ai-intelligence-daily/`

## 📁 项目结构

```
├── generate_report.py        # 数据获取核心
├── generate_browser_friendly.py  # HTML/PDF 生成
├── run.sh                    # 一键运行脚本
├── requirements.txt          # Python 依赖
├── electron/                 # 桌面应用
│   ├── main.js
│   ├── preload.js
│   ├── welcome.html
│   └── package.json
├── .github/workflows/        # GitHub Actions
│   └── daily-report.yml
├── config/                   # 用户配置
├── data/                     # 数据存储
└── output/                   # 输出目录
```

## 📖 详细文档

- [部署指南](DEPLOY.md)
- [项目规划](PLAN.md)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License - 仅供个人学习与行业洞察使用

---

<p align="center">
  <strong>AI Intelligence Daily</strong> - 让全球资讯触手可及 🌐
</p>
