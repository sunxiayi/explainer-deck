#!/usr/bin/env python3
"""列出所有"还没回答"的提问（基于实际已答状态，不靠行号基准）。
判定：按 qid 分组，inbox 里该 qid 的提问数 > answers.json 里该 qid 的回答数 → 多出来的就是待答。
输出 JSON 数组到 stdout：[{qid, slideId, anchorText, question, qIndex}]
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
INBOX = os.path.join(ROOT, 'qa-inbox.jsonl')
ANSWERS = os.path.join(ROOT, 'qa-answers.json')


def load_inbox():
    rows = []
    try:
        with open(INBOX, encoding='utf-8') as f:
            for ln in f:
                ln = ln.strip()
                if ln:
                    try:
                        rows.append(json.loads(ln))
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return rows


def load_answers():
    try:
        with open(ANSWERS, encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, ValueError):
        return {}


def pending():
    rows = load_inbox()
    answers = load_answers()
    # inbox 按 qid 分组，保持顺序
    by_qid = {}
    for r in rows:
        by_qid.setdefault(r.get('qid'), []).append(r)
    out = []
    for qid, qs in by_qid.items():
        n_ans = len(answers.get(qid, {}).get('answers', []))
        for i in range(n_ans, len(qs)):
            r = qs[i]
            out.append({
                'qid': qid,
                'slideId': r.get('slideId'),
                'anchorText': r.get('anchorText'),
                'question': r.get('question'),
                'qIndex': i,
            })
    return out


if __name__ == '__main__':
    print(json.dumps(pending(), ensure_ascii=False, indent=2))
