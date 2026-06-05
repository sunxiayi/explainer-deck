#!/usr/bin/env python3
"""陪读问答本地服务 — 把网页里选中的提问写进 qa-inbox.jsonl，并把回复 qa-answers.json 喂回网页。
端口由 deck 路径派生（每个 deck 唯一，避免冲突），被占用时自动 +1 探测。
用法: python3 qa/qa-server.py   启动后控制台会打印实际地址。
"""
import http.server, json, os, time, hashlib, socket
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))      # .../explainer/qa
DECK = os.path.dirname(ROOT)                            # .../explainer
INBOX = os.path.join(ROOT, 'qa-inbox.jsonl')
ANSWERS = os.path.join(ROOT, 'qa-answers.json')
PORTFILE = os.path.join(ROOT, 'qa-port.txt')           # 实际端口写这里，前端读它

# RED for errors, YELLOW for warnings (per user global instruction)
RED = '\033[31m'; YELLOW = '\033[33m'; RESET = '\033[0m'

def derive_port():
    """从 deck 绝对路径派生一个 8800–8999 的基准端口，每个 deck 不同。被占用则顺延。"""
    h = int(hashlib.md5(DECK.encode()).hexdigest(), 16)
    base = 8800 + (h % 200)
    for off in range(40):
        p = base + off
        if p > 8999:
            p = 8800 + (p - 9000)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            if s.connect_ex(('127.0.0.1', p)) != 0:   # 连不上 = 空闲
                return p
    return base

PORT = derive_port()

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DECK, **k)

    def log_message(self, fmt, *args):
        pass  # quiet

    def _send_json(self, code, raw_bytes):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(raw_bytes)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(raw_bytes)

    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/qa/qa-answers.json' or p == '/qa-answers.json':
            try:
                with open(ANSWERS, 'rb') as f:
                    b = f.read()
            except FileNotFoundError:
                b = b'{}'
            return self._send_json(200, b)
        return super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path == '/ask':
            try:
                n = int(self.headers.get('Content-Length', 0))
                data = json.loads(self.rfile.read(n) or b'{}')
            except Exception as e:
                print(RED + 'ERROR parsing /ask body: %s' % e + RESET)
                return self._send_json(400, b'{"ok":false}')
            data['server_ts'] = time.time()
            with open(INBOX, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
            print(YELLOW + 'NEW QUESTION [%s] slide=%s: %s' % (
                data.get('qid'), data.get('slideId'), str(data.get('question'))[:60]) + RESET)
            return self._send_json(200, json.dumps({'ok': True, 'qid': data.get('qid')}).encode())
        return self._send_json(404, b'{"error":"not found"}')


if __name__ == '__main__':
    if not os.path.exists(ANSWERS):
        with open(ANSWERS, 'w', encoding='utf-8') as f:
            f.write('{}')
    open(INBOX, 'a').close()
    with open(PORTFILE, 'w') as f:
        f.write(str(PORT))
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(('127.0.0.1', PORT), Handler)
    url = 'http://127.0.0.1:%d/index.html' % PORT
    print('=' * 56)
    print('陪读问答服务已启动:  ' + url)
    print('停止服务: 在本终端按 Ctrl+C，或告诉 Claude "关闭问答"。')
    print('=' * 56)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n服务已停止。')
        httpd.shutdown()
    finally:
        try:
            os.remove(PORTFILE)
        except OSError:
            pass
