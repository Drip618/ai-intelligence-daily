# 部署指南

## 🚀 快速部署到 GitHub

### 1. 创建私有仓库

1. 访问 [GitHub New Repository](https://github.com/new)
2. 仓库名：`ai-intelligence-daily`
3. 选择 **Private**（私有仓库）
4. 勾选 **Add a README file**
5. 点击 **Create repository**

### 2. 推送代码

```bash
# 进入项目目录
cd project_v2

# 初始化 Git
git init

# 添加远程仓库 (替换为你的仓库地址)
git remote add origin https://github.com/YOUR_USERNAME/ai-intelligence-daily.git

# 添加所有文件
git add .

# 提交
git commit -m "🚀 Initial commit: AI Intelligence Daily"

# 推送到 GitHub
git push -u origin main
```

### 3. 配置 Secrets

在 GitHub 仓库中配置以下 Secrets：

1. 进入 **Settings** → **Secrets and variables** → **Actions**
2. 添加以下 Secrets：

| Secret Name | 说明 |
|-------------|------|
| `DASHSCOPE_API_KEY` | 通义千问 API Key（用于 AI 总结） |
| `GITHUB_TOKEN` | GitHub Personal Access Token（用于获取更多数据） |

### 4. 启用 GitHub Pages

1. 进入 **Settings** → **Pages**
2. Source 选择 **GitHub Actions**
3. 保存后，GitHub Actions 会自动部署

### 5. 测试手动触发

1. 进入 **Actions** 标签页
2. 点击 **Daily Report Generator**
3. 点击 **Run workflow** → **Run workflow**
4. 等待完成后，访问 `https://YOUR_USERNAME.github.io/ai-intelligence-daily/`

## 💻 本地部署

### 环境要求

- Python 3.10+
- Node.js 16+（可选，用于 Electron）

### 安装依赖

```bash
# Python 依赖
pip install -r requirements.txt

# macOS 额外安装 weasyprint 系统依赖
brew install pango glib cairo

# Linux (Ubuntu/Debian)
sudo apt-get install -y build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Windows
# 参考: https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows
```

### 运行

```bash
# 一键运行
./run.sh

# 或分步运行
python3 generate_report.py --no-ai
python3 generate_browser_friendly.py

# 查看报告
open output/Daily_Report_$(date +%Y-%m-%d).html
```

## 🖥️ Electron 桌面应用

```bash
cd electron
npm install
npm start
```

构建桌面应用：

```bash
# macOS
npm run build:mac

# Windows
npm run build:win

# Linux
npm run build:linux
```

## 📱 PWA 移动端

1. 部署到 GitHub Pages 后
2. 使用手机浏览器访问
3. 点击"添加到主屏幕"
4. 即可像原生应用一样使用

## 🔧 自定义配置

### 添加自定义 API

在浏览器中打开 HTML 报告 → 点击 ⚙️ 设置 → 添加 API：

```json
{
  "name": "My Custom API",
  "url": "https://api.example.com/news",
  "method": "GET",
  "headers": {
    "Authorization": "Bearer YOUR_TOKEN"
  },
  "data_path": "data.items",
  "title_field": "title",
  "summary_field": "description",
  "url_field": "link",
  "category": "AI行业",
  "content_type": "文字",
  "enabled": true
}
```

### 配置推送渠道

目前支持以下推送渠道（需要在后端实现）：

- 📧 邮件推送
- 💬 Telegram Bot
- 📱 企业微信
- 🔗 Webhook

## 📊 数据源说明

项目支持 50+ 数据源，包括：

- **API 类型**: 直接调用 API，数据可靠
- **抓取类型**: 从网页 HTML 中提取，可能受反爬限制

系统会随机选择可用数据源，确保每日内容多样性。

## ❓ 常见问题

### Q: 为什么某些分类没有数据？
A: 部分数据源可能被反爬或需要认证。系统会自动切换到其他可用源。

### Q: 如何增加数据获取成功率？
A: 1. 配置 GitHub Token 2. 使用自定义 API 3. 启用 AI 总结

### Q: PDF 导出乱码怎么办？
A: 确保安装了 weasyprint 的完整系统依赖（中文字体）。

### Q: 如何在手机上查看？
A: 部署到 GitHub Pages 后，使用手机浏览器访问并添加到主屏幕。
