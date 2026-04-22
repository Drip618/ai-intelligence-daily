#!/bin/bash
# AI Intelligence Daily - 一键运行脚本

set -e

echo "============================================"
echo "  🚀 AI Intelligence Daily"
echo "  全球资讯速递 - 每日自动推送系统"
echo "============================================"
echo ""

# 获取今天的日期
TODAY=$(date +%Y-%m-%d)
echo "📅 日期: $TODAY"

# 步骤1: 获取数据
echo ""
echo "📡 步骤1: 获取全球资讯..."
python3 generate_report.py --no-ai

# 步骤2: 生成HTML+PDF
echo ""
echo "🎨 步骤2: 生成精美报告..."
python3 generate_browser_friendly.py

echo ""
echo "============================================"
echo "  ✅ 完成!"
echo "============================================"
echo ""
echo "📄 HTML报告: output/Daily_Report_${TODAY}.html"
echo "📑 PDF报告: output/Daily_Report_${TODAY}.pdf"
echo ""
echo "💡 提示:"
echo "  - 在浏览器中打开 HTML 文件查看交互式报告"
echo "  - 点击'导出PDF'按钮或浏览器打印功能导出PDF"
echo "  - 点击'设置'按钮配置自定义API和推送渠道"
echo ""
