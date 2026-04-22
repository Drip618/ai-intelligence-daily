#!/bin/bash
# AI Intelligence Daily - 完整打包脚本
# 将当前项目打包成可直接分发的格式

set -e

cd "$(dirname "$0")"

PACK_DIR="/tmp/每日情报速递_完整包"
rm -rf "$PACK_DIR"
mkdir -p "$PACK_DIR"

echo "============================================================"
echo "  📦 每日情报速递 - 完整打包"
echo "============================================================"
echo ""

# 1. 复制桌面端报告
echo "📄 复制桌面端报告..."
cp output/Daily_Report_2026-04-22.html "$PACK_DIR/" 2>/dev/null || echo "  无桌面端HTML报告"
cp output/Daily_Report_2026-04-22.pdf "$PACK_DIR/" 2>/dev/null || echo "  无PDF报告"

# 2. 复制移动端H5
echo "📱 复制移动端H5..."
cp mobile/www/index.html "$PACK_DIR/移动端_H5.html" 2>/dev/null || echo "  无移动端H5"

# 3. 复制项目文件
echo "📁 复制项目文件..."
mkdir -p "$PACK_DIR/project"
cp generate_report.py "$PACK_DIR/project/"
cp generate_browser_friendly.py "$PACK_DIR/project/"
cp run_server.py "$PACK_DIR/project/"
cp start_mobile.py "$PACK_DIR/project/"
cp requirements.txt "$PACK_DIR/project/"
cp -r mobile "$PACK_DIR/project/"
cp -r project_v2 "$PACK_DIR/project/"
cp build_mobile.sh "$PACK_DIR/project/"

# 4. 创建使用说明
echo "📝 创建使用说明..."
cat > "$PACK_DIR/使用说明.txt" << 'EOF'
============================================================
  AI Intelligence Daily - 每日情报速递
  使用说明
============================================================

📁 文件说明：
  - Daily_Report_2026-04-22.html  桌面端完整报告（双击打开）
  - Daily_Report_2026-04-22.pdf   PDF 版本报告
  - 移动端_H5.html                移动端页面（手机浏览器打开）
  - project/                      完整项目文件

💻 桌面端使用：
  1. 双击 Daily_Report_2026-04-22.html 即可在浏览器中查看
  2. 双击 Daily_Report_2026-04-22.pdf 用预览/PDF阅读器打开

📱 手机端使用：
  方式1（最简单）:
    1. 将"移动端_H5.html"发送到手机（AirDrop/微信等）
    2. 用手机浏览器打开
    3. 点击"添加到主屏幕"即可像App一样使用
  
  方式2（完整版）:
    1. 电脑运行: python3 start_mobile.py
    2. 手机浏览器扫描二维码或输入地址
    3. 点击"添加到主屏幕"

🔧 完整项目使用：
  cd project
  python3 start_mobile.py  # 启动服务器

  # 构建iOS App（需要Xcode）:
  cd mobile && npx cap open ios
  
  # 构建Android App（需要Android Studio）:
  cd mobile && npx cap open android

============================================================
EOF

# 5. 打包成ZIP
echo ""
echo "📦 打包成 ZIP..."
cd /tmp
zip -r "每日情报速递.zip" "每日情报速递_完整包/" > /dev/null

echo ""
echo "============================================================"
echo "  ✅ 打包完成！"
echo "============================================================"
echo ""
echo "  📁 打包位置: /tmp/每日情报速递_完整包/"
echo "  📦 压缩包:   /tmp/每日情报速递.zip"
echo ""
ls -lh "/tmp/每日情报速递_完整包/"
echo ""
ls -lh "/tmp/每日情报速递.zip"
echo "============================================================"
