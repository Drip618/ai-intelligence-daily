#!/bin/bash
# AI Intelligence Daily - 一键启动脚本
# 自动获取本机 IP、启动服务器、显示二维码供手机扫描

set -e

cd "$(dirname "$0")"

# 获取本机局域网 IP
get_local_ip() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "127.0.0.1"
    else
        # Linux
        hostname -I | awk '{print $1}' || echo "127.0.0.1"
    fi
}

# 安装 qrcode 库（如果尚未安装）
install_qr_deps() {
    python3 -c "import qrcode" 2>/dev/null || pip3 install qrcode[pil] -q
}

# 清理旧的二维码图片
cleanup() {
    rm -f /tmp/daily_report_qr.png 2>/dev/null || true
}

# 主流程
echo "============================================================"
echo "  AI Intelligence Daily - 每日情报速递"
echo "============================================================"
echo ""
echo "正在启动服务器..."
echo ""

# 安装依赖
install_qr_deps
cleanup

# 获取 IP
LOCAL_IP=$(get_local_ip)
PORT=8765

# 启动服务器（后台运行）
python3 run_server.py --port $PORT --host 0.0.0.0 &
SERVER_PID=$!

# 等待服务器启动
sleep 2

echo ""
echo "============================================================"
echo "  服务器已启动！"
echo "============================================================"
echo ""
echo "  电脑访问: http://localhost:$PORT"
echo "  手机访问: http://$LOCAL_IP:$PORT"
echo ""
echo "  请用手机扫描下方二维码快速连接："
echo ""

# 生成二维码
python3 -c "
import qrcode
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data('http://$LOCAL_IP:$PORT')
qr.make(fit=True)
img = qr.make_image(fill_color='black', back_color='white')
img.save('/tmp/daily_report_qr.png')
print('二维码已生成: /tmp/daily_report_qr.png')
"

# 显示二维码（终端）
python3 -c "
from PIL import Image
import sys

img = Image.open('/tmp/daily_report_qr.png')
img = img.resize((40, 40), Image.NEAREST)
pixels = img.load()

for y in range(img.height):
    line = ''
    for x in range(img.width):
        # 使用 ANSI 转义码显示二维码
        r, g, b = pixels[x, y][:3]
        if r < 128:
            line += '\033[40m  \033[0m'
        else:
            line += '\033[47m  \033[0m'
    print(line)
"

echo ""
echo "============================================================"
echo "  使用说明"
echo "============================================================"
echo ""
echo "  手机端："
echo "  1. 确保手机和电脑在同一 WiFi 网络"
echo "  2. 扫描二维码或在浏览器输入地址"
echo "  3. 点击「添加到主屏幕」（iOS Safari / Android Chrome）"
echo "  4. 以后像打开 App 一样使用"
echo ""
echo "  电脑端："
echo "  1. 浏览器打开 http://localhost:$PORT"
echo "  2. 点击「刷新数据」获取最新内容"
echo ""
echo "  停止服务器：按 Ctrl+C"
echo "============================================================"
echo ""

# 等待用户中断
trap 'echo ""; echo "正在关闭服务器..."; kill $SERVER_PID 2>/dev/null; echo "服务器已停止。"; exit 0' INT TERM

wait $SERVER_PID
