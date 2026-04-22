#!/usr/bin/env python3
"""Mobile-friendly HTTP server with data refresh support."""

import json
import subprocess
import sys
import threading
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingMixIn

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"


class DailyReportHandler(SimpleHTTPRequestHandler):
    """HTTP handler with /api/fetch and /api/generate endpoints."""

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            # Serve the latest daily report
            today = datetime.now().strftime("%Y-%m-%d")
            latest = OUTPUT_DIR / f"Daily_Report_{today}.html"
            if latest.exists():
                self.path = str(latest)
            else:
                # Fallback to most recent report
                reports = sorted(OUTPUT_DIR.glob("Daily_Report_*.html"), reverse=True)
                if reports:
                    self.path = str(reports[0])
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.end_headers()
                    self.wfile.write(
                        '<h1>报告尚未生成</h1><p>请先运行: python3 generate_report.py --no-ai</p>'.encode('utf-8')
                    )
                    return

        if self.path == '/api/status':
            self.send_json({
                "status": "ok",
                "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "reports_available": len(list(OUTPUT_DIR.glob("Daily_Report_*.html")))
            })
            return

        super().do_GET()

    def do_POST(self):
        if self.path == '/api/fetch':
            self.handle_fetch()
        elif self.path == '/api/generate':
            self.handle_generate()
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def handle_fetch(self):
        """Run generate_report.py to fetch new data."""
        self.log_message("Fetching new data...")
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "generate_report.py"), "--no-ai"],
            capture_output=True, text=True, cwd=str(BASE_DIR),
            timeout=300
        )
        if result.returncode == 0:
            self.send_json({"success": True, "message": "数据抓取成功", "output": result.stdout})
        else:
            self.send_json({
                "success": False,
                "error": result.stderr or "抓取失败",
                "output": result.stdout
            })

    def handle_generate(self):
        """Run generate_browser_friendly.py to generate HTML + PDF."""
        self.log_message("Generating report...")
        result = subprocess.run(
            [sys.executable, str(BASE_DIR / "generate_browser_friendly.py")],
            capture_output=True, text=True, cwd=str(BASE_DIR),
            timeout=120
        )
        if result.returncode == 0:
            self.send_json({"success": True, "message": "报告生成成功", "output": result.stdout})
        else:
            self.send_json({
                "success": False,
                "error": result.stderr or "生成失败",
                "output": result.stdout
            })

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""
    allow_reuse_address = True
    daemon_threads = True


def get_local_ip():
    """Get local IP address for mobile access."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Daily Report HTTP Server")
    parser.add_argument("--port", type=int, default=8765, help="Port number (default: 8765)")
    parser.add_argument("--host", default=None, help="Host (default: 0.0.0.0 for LAN access)")
    args = parser.parse_args()

    host = args.host or "0.0.0.0"
    port = args.port

    server = ThreadedHTTPServer((host, port), DailyReportHandler)
    local_ip = get_local_ip()

    print("=" * 60)
    print("  每日情报速递 - HTTP 服务器")
    print("=" * 60)
    print(f"\n  本机访问: http://localhost:{port}")
    print(f"  手机访问: http://{local_ip}:{port}")
    print(f"\n  API 端点:")
    print(f"    POST /api/fetch    - 抓取最新数据")
    print(f"    POST /api/generate - 生成 HTML + PDF")
    print(f"    GET  /api/status   - 查看服务器状态")
    print(f"\n  按 Ctrl+C 停止服务器")
    print("=" * 60 + "\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n服务器已停止。")
        server.shutdown()


if __name__ == "__main__":
    main()
