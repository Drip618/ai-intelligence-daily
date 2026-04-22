# AI Intelligence Daily - 密钥配置指南

## 📋 项目仓库

- **仓库地址**: https://github.com/Drip618/ai-intelligence-daily
- **状态**: ✅ 已推送（私有仓库）
- **GitHub Actions**: ✅ 已配置

---

## 🔐 需要配置的 Secrets

请在 GitHub 仓库中配置以下 Secrets：

### 步骤
1. 访问: https://github.com/Drip618/ai-intelligence-daily/settings/secrets/actions
2. 点击 **New repository secret**
3. 添加以下 Secrets:

| Secret Name | 值 (你需要替换) | 说明 |
|-------------|----------------|------|
| `DASHSCOPE_API_KEY` | `你的通义千问 API Key` | 用于 AI 智能总结，从阿里云获取 |
| `GITHUB_TOKEN` | 已自动配置 | GitHub Actions 自动使用，无需手动配置 |

### 如何获取 DASHSCOPE_API_KEY

1. 访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/apiKey)
2. 登录你的阿里云账号
3. 创建 API Key
4. 复制 Key 值到 GitHub Secrets

---

## 🚀 手动触发工作流

### 方法1: GitHub 界面
1. 进入仓库 → **Actions** → **Daily Report Generator**
2. 点击 **Run workflow**
3. 选择分支 (main)
4. 点击 **Run workflow**

### 方法2: CLI
```bash
cd project_v2
gh workflow run daily-report.yml
```

---

## 📊 查看报告

### 本地生成
```bash
cd project_v2
./run.sh
```

### GitHub Actions 生成后
- 进入 **Actions** → 查看运行结果
- 下载 Artifacts 获取 HTML/PDF 报告

---

## ⚙️ 自定义设置

在浏览器中打开 HTML 报告后，点击右上角 **⚙️ 设置**：

- 🎨 主题切换 (深色/浅色/护眼)
- 📊 每分类条数
- 🔌 自定义 API 添加
- 📮 推送渠道配置

---

## 📱 桌面应用

```bash
cd electron
npm install
npm start
```

---

## ❓ 常见问题

### Q: 为什么某些分类没有数据？
A: 部分数据源被反爬，系统会自动切换其他可用源。

### Q: 如何增加数据获取成功率？
A: 1. 配置 DASHSCOPE_API_KEY 2. 使用自定义 API 3. 添加更多数据源

### Q: Actions 运行失败怎么办？
A: 查看 Actions 日志，检查 Secrets 配置是否正确。

---

**最后更新**: 2026-04-22
