# AI Intelligence Daily - 移动端部署指南

## 方案概览

本项目提供三种移动端使用方案，请根据你的需求选择：

| 方案 | 适用场景 | 难度 | 是否需要电脑 |
|------|---------|------|-------------|
| **方案 A**: 局域网 Web 访问 | 快速体验 | ⭐ 最简单 | ✅ 需要 |
| **方案 B**: Capacitor 原生 App | 长期稳定使用 | ⭐⭐ 中等 | ⚙️ 构建时需要 |
| **方案 C**: Electron 桌面端 | 电脑端使用 | ⭐ 简单 | ❌ 不需要 |

---

## 方案 A：局域网 Web 访问（推荐快速体验）

### 适用场景
- 快速在手机上查看报告
- 不需要安装 App
- 电脑和手机在同一 WiFi

### 使用步骤

```bash
# 1. 在电脑上启动服务器
python3 start_mobile.py

# 2. 手机浏览器扫描终端显示的二维码
#    或手动输入地址: http://[你的电脑IP]:8765

# 3. 添加到手机主屏幕（可选）
# iOS: Safari → 分享 → 添加到主屏幕
# Android: Chrome → 菜单 → 添加到主屏幕
```

### 特点
- ✅ 即时可用，无需编译
- ✅ 数据由电脑 Python 脚本抓取
- ⚠️ 需要电脑和手机在同一 WiFi
- ⚠️ 电脑需要保持服务器运行

---

## 方案 B：Capacitor 原生 App（推荐长期使用）

### 适用场景
- 希望手机独立运行，不依赖电脑
- 需要完整的 App 体验
- 愿意花 10-20 分钟进行初始配置

### 前置要求

#### iOS
- macOS 系统
- Xcode（App Store 免费下载）
- 苹果开发者账号（免费即可）

#### Android
- Android Studio（免费下载）
- JDK 17+

### 构建步骤

```bash
# 1. 进入项目目录
cd "数据收集1.0"

# 2. 运行一键构建脚本
./build_mobile.sh        # 构建 iOS + Android
./build_mobile.sh ios    # 仅构建 iOS
./build_mobile.sh android # 仅构建 Android

# 3. 等待依赖安装完成（首次约 2-5 分钟）
```

### iOS 部署

```bash
# 在 Xcode 中打开项目
cd mobile && npx cap open ios

# Xcode 中操作：
# 1. 选择你的 iPhone 或模拟器
# 2. 选择 Team（你的 Apple ID）
# 3. 点击 ▶️ Run
```

### Android 部署

```bash
# 在 Android Studio 中打开项目
cd mobile && npx cap open android

# Android Studio 中操作：
# 1. 等待 Gradle 同步完成
# 2. 选择设备或模拟器
# 3. 点击 ▶️ Run
```

### 更新数据

```bash
# 每次需要更新 App 内容时：
cd mobile
npm run build:web    # 重新生成 Web 资源
npx cap sync         # 同步到原生项目
```

### 特点
- ✅ 手机完全独立运行
- ✅ 原生 App 体验（启动画面、状态栏等）
- ✅ 支持离线缓存
- ⚠️ 首次配置需要一些时间
- ⚠️ 数据源受 CORS 限制（App 中可绕过）

---

## 方案 C：Electron 桌面端

### 适用场景
- 主要在电脑上使用
- 需要桌面应用体验

### 使用步骤

```bash
# 进入 Electron 项目
cd project_v2/electron

# 安装依赖（首次）
npm install

# 运行
npm start

# 打包成可执行文件（可选）
npm run build:mac    # macOS
npm run build:win    # Windows
npm run build:linux  # Linux
```

---

## 数据源说明

### 电脑端方案（方案 A/C）
使用 Python 脚本 `generate_report.py`，支持所有平台：
- HuggingFace Trending
- GitHub Trending
- 微博热搜
- B站热门
- 知乎热榜
- 豆瓣影视
- 猫眼电影

### 移动端原生方案（方案 B）
由于浏览器 CORS 限制，部分 API 无法直接调用：
- ✅ GitHub API（支持 CORS）
- ✅ HuggingFace（App 中可用）
- ❌ 微博/B站/知乎（需要代理或后端）

**解决方案：**
1. 使用 Capacitor HTTP 插件绕过 CORS
2. 自建 API 代理服务器
3. 使用 RSSHub 公共实例

---

## 常见问题

### Q: 手机连接不上电脑服务器？
A: 检查以下几点：
1. 电脑和手机是否在同一 WiFi
2. 防火墙是否允许 8765 端口
3. 尝试关闭防火墙或使用其他端口

### Q: Capacitor 构建失败？
A: 常见问题：
```bash
# 清理缓存重新安装
cd mobile
rm -rf node_modules ios android
npm install
./build_mobile.sh
```

### Q: iOS 签名失败？
A: 在 Xcode 中：
1. 选择项目 → Signing & Capabilities
2. 选择你的 Team（Apple ID）
3. 确保 Bundle Identifier 唯一

### Q: Android Gradle 同步失败？
A: 
1. 确保已安装 Android SDK
2. File → Sync Project with Gradle Files
3. 检查 `android/build.gradle` 中的 SDK 版本

---

## 目录结构

```
数据收集1.0/
├── generate_report.py              # 数据抓取脚本
├── generate_browser_friendly.py    # HTML/PDF 生成脚本
├── run_server.py                   # HTTP 服务器
├── start_mobile.py                 # 一键启动脚本（含二维码）
├── build_mobile.sh                 # 移动端构建脚本
├── mobile/                         # Capacitor 移动端项目
│   ├── package.json
│   ├── capacitor.config.json
│   └── www/                        # Web 资源目录
│       └── index.html
├── project_v2/electron/            # Electron 桌面端项目
│   ├── package.json
│   ├── main.js
│   └── preload.js
├── output/                         # 生成的报告
│   ├── Daily_Report_*.html
│   └── Daily_Report_*.pdf
└── data/knowledge/daily_reports/   # 原始数据
    └── report_*.json
```

---

## 技术支持

如遇问题，请检查：
1. Python 版本 >= 3.10
2. Node.js 版本 >= 18
3. 所有依赖是否正确安装
4. 网络连接是否正常

```bash
# 检查环境
python3 --version
node --version
npm --version
```
