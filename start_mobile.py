#!/usr/bin/env python3
"""一键启动脚本 - 自动获取 IP、启动服务器、显示连接信息。"""

import http.server
import json
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def generate_qr_code(url):
    try:
        import qrcode
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        qr_path = "/tmp/ai_daily_qr.png"
        img.save(qr_path)
        return qr_path
    except ImportError:
        return None


def print_banner(local_ip, port):
    print("\n" + "=" * 60)
    print("  🚀 AI Intelligence Daily - 每日情报速递")
    print("=" * 60)
    print(f"\n  ✅ 服务器已启动！")
    print(f"\n  📱 手机访问地址:")
    print(f"     http://{local_ip}:{port}")
    print(f"\n  💻 电脑访问地址:")
    print(f"     http://localhost:{port}")
    print(f"\n  📋 使用说明:")
    print(f"     1. 确保手机和电脑在同一 WiFi")
    print(f"     2. 手机浏览器输入上方地址")
    print(f"     3. 点击「添加到主屏幕」即可像 App 一样使用")
    print(f"\n  ⏹  按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")


def main():
    port = 8765
    local_ip = get_local_ip()

    print("🔄 正在启动服务器...")

    # 生成 HTML 报告（如果今天还没有）
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = OUTPUT_DIR / f"Daily_Report_{today}.html"
    if not report_path.exists():
        print("📊 正在生成今日报告...")
        subprocess.run([sys.executable, str(BASE_DIR / "generate_browser_friendly.py")],
                      capture_output=True, timeout=120)

    # 生成二维码
    qr_path = generate_qr_code(f"http://{local_ip}:{port}")

    print_banner(local_ip, port)

    if qr_path:
        print(f"📱 二维码已生成: {qr_path}")
        print("   可用手机扫描此二维码快速连接\n")

        # macOS 尝试打开二维码图片
        if sys.platform == "darwin":
            subprocess.run(["open", qr_path], capture_output=True)

    # 自动打开浏览器
    webbrowser.open(f"http://localhost:{port}")

    # 启动 HTTP 服务器
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(BASE_DIR), **kwargs)

        def do_GET(self):
            if self.path == "/" or self.path == "/index.html":
                if report_path.exists():
                    self.path = str(report_path)
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<h1>报告尚未生成</h1>".encode("utf-8"))
                    return
            super().do_GET()

        def log_message(self, format, *args):
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")

    server = http.server.HTTPServer(("0.0.0.0", port), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止。")
        server.shutdown()


if __name__ == "__main__":
    main()
