#!/usr/bin/env python3
"""把一条回复写进 qa-answers.json（按 qid 追加），网页轮询后会自动显示。
Claude 用法:
  python3 qa/answer.py <qid> <<'EOF'
  回复正文（支持 **粗体**、`代码`、换行）
  EOF
也可: python3 qa/answer.py <qid> "单行回复"
"""
import json, os, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
ANSWERS = os.path.join(ROOT, 'qa-answers.json')
RED = '\033[31m'; RESET = '\033[0m'

if len(sys.argv) < 2:
    print(RED + 'ERROR: need qid' + RESET); sys.exit(1)
qid = sys.argv[1]
text = sys.argv[2] if len(sys.argv) > 2 else sys.stdin.read()
text = text.rstrip('\n')
if not text.strip():
    print(RED + 'ERROR: empty answer' + RESET); sys.exit(1)

try:
    with open(ANSWERS, encoding='utf-8') as f:
        data = json.load(f)
except (FileNotFoundError, ValueError):
    data = {}

entry = data.setdefault(qid, {'answers': []})
entry['answers'].append({'text': text, 'ts': time.time()})

with open(ANSWERS, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('answered %s (now %d replies)' % (qid, len(entry['answers'])))
