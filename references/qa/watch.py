#!/usr/bin/env python3
"""阻塞等待"有未回答的提问"出现，一旦出现就打印待答清单并退出（唤醒 Claude 回答）。
判定基于实际已答状态（见 pending.py），不靠行号基准 —— 所以不会漏、不会重复唤醒已答的问题。
答完后 Claude 应再次运行本脚本，形成常驻循环。
用法: python3 qa/watch.py
"""
import time, os, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from pending import pending  # noqa: E402

POLL_SEC = 1

while True:
    p = pending()
    if p:
        sys.stdout.write('=== PENDING QUESTIONS (%d) ===\n' % len(p))
        sys.stdout.write(json.dumps(p, ensure_ascii=False, indent=2) + '\n')
        sys.stdout.flush()
        break
    time.sleep(POLL_SEC)
