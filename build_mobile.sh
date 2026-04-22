#!/bin/bash
# AI Intelligence Daily - 移动端一键构建脚本
# 用法: ./build_mobile.sh [ios|android|both]

set -e

cd "$(dirname "$0")"
PROJECT_DIR="mobile"
PARENT_DIR="$(pwd)"

echo "============================================================"
echo "  📱 AI Intelligence Daily - 移动端构建"
echo "============================================================"
echo ""

# 检查依赖
check_deps() {
    echo "🔍 检查依赖..."
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装"
        echo "   请运行: brew install node"
        exit 1
    fi
    
    if ! command -v npm &> /dev/null; then
        echo "❌ npm 未安装"
        exit 1
    fi
    
    echo "   ✅ Node.js: $(node -v)"
    echo "   ✅ npm: $(npm -v)"
    
    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 未安装"
        exit 1
    fi
    echo "   ✅ Python3: $(python3 --version)"
    echo ""
}

# 安装 Node 依赖
install_deps() {
    echo "📦 安装依赖..."
    cd "$PROJECT_DIR"
    npm install
    cd ..
    echo "   ✅ 依赖安装完成"
    echo ""
}

# 生成 Web 资源
generate_web() {
    echo "📊 生成 Web 资源..."
    
    # 确保 www 目录存在
    mkdir -p "$PROJECT_DIR/www"
    
    # 如果有 Python 生成的报告，复制过来
    if [ -f "output/Daily_Report_$(date +%Y-%m-%d).html" ]; then
        cp "output/Daily_Report_$(date +%Y-%m-%d).html" "$PROJECT_DIR/www/index.html"
        echo "   ✅ 已复制今日报告"
    elif [ -f "$PROJECT_DIR/www/index.html" ]; then
        echo "   ✅ 使用现有 index.html"
    else
        echo "   ⚠️ 暂无报告，使用默认页面"
        cat > "$PROJECT_DIR/www/index.html" << 'HTMLEOF'
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Intelligence Daily</title></head>
<body style="background:#0f172a;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;font-family:system-ui">
<div style="text-align:center"><h1>🤖 AI Intelligence Daily</h1><p>点击「抓取数据」获取今日资讯</p></div>
</body></html>
HTMLEOF
    fi
    echo ""
}

# 初始化 Capacitor
init_capacitor() {
    echo "⚙️ 初始化 Capacitor..."
    cd "$PROJECT_DIR"
    
    if [ ! -f "capacitor.config.json" ]; then
        npx cap init "AI Intelligence Daily" com.aiintelligence.daily --web-dir www
    fi
    
    cd ..
    echo "   ✅ Capacitor 初始化完成"
    echo ""
}

# 添加平台
add_platforms() {
    local target=${1:-"both"}
    cd "$PROJECT_DIR"
    
    if [ "$target" = "ios" ] || [ "$target" = "both" ]; then
        echo "🍎 添加 iOS 平台..."
        if [ ! -d "ios" ]; then
            npx cap add ios
            echo "   ✅ iOS 平台已添加"
        else
            echo "   ℹ️  iOS 平台已存在"
        fi
    fi
    
    if [ "$target" = "android" ] || [ "$target" = "both" ]; then
        echo "🤖 添加 Android 平台..."
        if [ ! -d "android" ]; then
            npx cap add android
            echo "   ✅ Android 平台已添加"
        else
            echo "   ℹ️  Android 平台已存在"
        fi
    fi
    
    cd ..
    echo ""
}

# 同步
sync() {
    echo "🔄 同步项目..."
    cd "$PROJECT_DIR"
    npx cap sync
    cd ..
    echo "   ✅ 同步完成"
    echo ""
}

# 打开 IDE
open_ide() {
    local target=${1:-"ios"}
    cd "$PROJECT_DIR"
    
    if [ "$target" = "ios" ]; then
        echo "🍎 打开 Xcode..."
        npx cap open ios
    elif [ "$target" = "android" ]; then
        echo "🤖 打开 Android Studio..."
        npx cap open android
    fi
    
    cd ..
}

# 主流程
main() {
    local target=${1:-"both"}
    
    check_deps
    install_deps
    generate_web
    init_capacitor
    add_platforms "$target"
    sync
    
    echo "============================================================"
    echo "  ✅ 构建完成！"
    echo "============================================================"
    echo ""
    echo "  📁 项目位置: $PROJECT_DIR/"
    echo ""
    echo "  接下来的步骤："
    echo ""
    
    if [ "$target" = "ios" ] || [ "$target" = "both" ]; then
        echo "  🍎 iOS:"
        echo "     1. 确保已安装 Xcode"
        echo "     2. 运行: cd mobile && npx cap open ios"
        echo "     3. 在 Xcode 中选择你的设备/模拟器"
        echo "     4. 点击 Run (▶️)"
        echo ""
    fi
    
    if [ "$target" = "android" ] || [ "$target" = "both" ]; then
        echo "  🤖 Android:"
        echo "     1. 确保已安装 Android Studio"
        echo "     2. 运行: cd mobile && npx cap open android"
        echo "     3. 在 Android Studio 中同步 Gradle"
        echo "     4. 选择设备/模拟器，点击 Run"
        echo ""
    fi
    
    echo "  📱 测试:"
    echo "     运行: ./build_mobile.sh test"
    echo "     在浏览器中预览移动端页面"
    echo ""
    echo "============================================================"
}

# 测试模式
test_mode() {
    echo "🧪 启动测试服务器..."
    echo "   访问: http://localhost:8080"
    echo "   按 Ctrl+C 停止"
    echo ""
    python3 -m http.server 8080 -d "$PROJECT_DIR/www"
}

# 运行
case "${1:-build}" in
    build|ios|android|both)
        main "$1"
        ;;
    test)
        test_mode
        ;;
    *)
        echo "用法: $0 [build|ios|android|both|test]"
        echo ""
        echo "  build    - 构建所有平台 (默认)"
        echo "  ios      - 仅构建 iOS"
        echo "  android  - 仅构建 Android"
        echo "  both     - 构建所有平台"
        echo "  test     - 启动测试服务器"
        exit 1
        ;;
esac
