# Workflow — 并行 agent 编排 + 完整 prompt 模板

完整的"从文章到 deck"流水线。每一步都给可复用的命令/prompt。

---

## Phase 1 (15–20 min): Setup + Foundation slides

**主 agent 自己做**——foundation slides 是后续所有 walkthrough 的"词典"，必须由一个 agent 写完保持术语一致。

### Step 1.1 — 准备目录

```bash
ARTICLE_DIR="${PROJECT_ROOT}/xhs/<source>/<slug>"   # 文章已 fetch 的目录
EXPLAINER_DIR="${ARTICLE_DIR}/explainer"
mkdir -p "$EXPLAINER_DIR/img"
cp .claude/skills/explainer-deck/references/deck-template.html "$EXPLAINER_DIR/index.html"
```

### Step 1.2 — 读文章 + 规划

读 `article.txt` 全文，列两份清单：

1. **Foundation 术语清单**（~15 条）—— 一个 CS 大二学生不会立刻懂的词
2. **Walkthrough 段落清单**（~45 张 slide）—— 按文章原始 section 切

把术语 cluster 到合适的 foundation slide 上：
- 不要一个术语一张 slide（太碎）
- 相关术语合并讲（FLOPs + bandwidth + AI 强度合一张）

### Step 1.3 — 写 foundation slides (s1–s15)

直接 Edit `index.html`，把 `<!-- INSERT_PART1_SLIDES -->` 替换为 15 张 slide 内容，把 `<!-- TOC_INSERT_PART1 -->` 替换为对应 TOC 条目。

每张 slide 必须包含 `.deepdive` box 引用 `references/resource-bank.md` 里 vetted 资源。

---

## Phase 2 (10–15 min, 并行): Walkthrough slides

**起 3 个 agent 并行**——文章按 section 切 3 段，每段 14-16 张 slide。

### Step 2.1 — 切分文章

按文章自然 section 切：

| Agent | 覆盖文章前 N% | 典型内容 | Slide ID 范围 |
|---|---|---|---|
| A | 前 33% | 论文 thesis + 概念入门 | s16–s30 |
| B | 中 33% | 技术 deep-dive | s31–s46 |
| C | 后 33% + synthesis | 商业 / 应用 / 总结 | s47–s62 |

每个 agent 收到一份 ID 范围 + 分配的 section 列表。

### Step 2.2 — 并行起 agent

**同一个 message 里发 3 个 Agent tool call**（必须并行，不要串行）：

```
Agent({
  subagent_type: "general-purpose",
  description: "Walkthrough Part A",
  prompt: <Agent A prompt below>,
  run_in_background: true
})
Agent({
  subagent_type: "general-purpose",
  description: "Walkthrough Part B",
  prompt: <Agent B prompt below>,
  run_in_background: true
})
Agent({
  subagent_type: "general-purpose",
  description: "Walkthrough Part C",
  prompt: <Agent C prompt below>,
  run_in_background: true
})
```

每个 agent 写到自己的临时文件 `part2-{A|B|C}.html`，包含 `<section>` blocks + 末尾的 `<!-- TOC ... TOC -->` 注释块。

### Agent prompt 模板（适用于 A/B/C，按 section 不同改 4 处）

```
You're writing HTML slide fragments for a Chinese teaching deck that
explains <article topic>. The deck is at <deck path> — READ IT FIRST
to see existing styling/CSS and foundation slides (s01-s15).

The article is at: <article.txt path> — READ IT IN FULL.

# Your assignment

Write slides <FIRST_ID>–<LAST_ID> (<COUNT> slides) covering article sections:
- "<Section 1 name>" (key concepts: ...)
- "<Section 2 name>" (...)
- "<Section N name>" (...)

Suggested slide breakdown (adjust as needed):
- s<N>: 标题 (要点)
- s<N+1>: 标题 (要点)
- ...

# Format requirements

Write EACH slide as a complete `<section class="slide" id="sN">...</section>`
block, ready to paste. Use these CSS classes from the deck:
- `.slide-num` for "SLIDE NN" label
- `<h2>` for slide title (will be yellow)
- `.takeaway` for the key insight box (▸ prefix)
- `.analogy` for analogy boxes (类比 prefix)
- `.example` for example boxes (例子 prefix)
- `.warning` for caveat boxes (注意 prefix)
- `.deepdive` for external resource links (selectively on key slides)
- `<pre>` for ASCII diagrams
- `<table>` for comparisons
- `<code>` for inline tech terms

See `.claude/skills/explainer-deck/references/slide-patterns.md` for
canonical patterns to copy.

# Voice & content rules

- Treat reader as CS sophomore/junior with no domain background
- ALWAYS explain a tech term from scratch the FIRST time it appears
- But if it's covered in foundation (s01-s15), say "见 slide N" and
  don't re-explain at length
- Use analogies aggressively (every abstract concept → real-world parallel)
- Do the math explicitly when numbers involved (show formula, plug in,
  get a number with units)
- Keep numbers concrete — preserve all article numbers exactly
- Reference earlier slides by ID when reusing concepts
- Write in the deck's `--language` (English default, or Chinese) — pass the chosen language into the agent prompt
- NO emoji anywhere (use unicode shapes ▸ ◂ ▲ ▼)
- AVOID AI-flavored patterns. For a **Chinese** deck, the banlist:
  任何/所有/每个/必须/反复强调/本质上/不是X而是Y/底层逻辑/核心在于/
  绕不开/躲不掉/更狠/狠的/骚操作/颠覆/划时代/重新定义/终于来了
  For an **English** deck: no hype/event-inflation, no "it's not X, it's Y"
  false-dichotomy reframing, no absolutes (any/every/must), no performative
  reading reactions — name the specific mechanism instead.

(Full anti-AI-voice grep regex at .claude/skills/explainer-deck/references/anti-ai-voice.md)

# Foundation slide map (what's already explained)

- slide 02: <topic of slide 02>
- slide 03: <topic of slide 03>
- ...
- slide 15: <topic of slide 15>

# Output

Save to: <EXPLAINER_DIR>/part2-<A|B|C>.html

Format:
- Just the `<section>` blocks, separated by blank lines
- At the very end, a `<!-- TOC ... TOC -->` comment block listing
  TOC entries:

  <!-- TOC
  <a href="#sN">N · slide title</a>
  <a href="#sN+1">N+1 · slide title</a>
  ...
  TOC -->

# Domain-specific musts (customize per topic)

- If article involves <specific concept>: use <specific framing>
- If article includes <specific quote>: preserve it verbatim
- Closing slide (last in your range) should hand off to next agent's range
  with one sentence: "下面 (slide <NEXT_FIRST>+) Agent <X> 会接着拆 <topic>"

After writing, briefly report (under 100 words) what slides you produced.
```

### Step 2.3 — 等 agent 完成

3 个 agent 并行运行，10-15 分钟。会自动通知完成。**不要轮询 / sleep**——harness 会主动通知。

---

## Phase 3 (5 min): Image fetch

**主 agent 做**——agent 写完后下载图片，因为他们没有 WebSearch/WebFetch 权限。

### Step 3.1 — 找图

```
WebFetch(<原文 URL>, "List all image URLs in this page. Look for product
photos, diagrams, screenshots. For each, briefly describe what it shows.")
```

如果原文是 substack 付费：直接 fetch `substackcdn.com` 或 `substack-post-media.s3.amazonaws.com` 通常能拿到图（图片本身不付费保护）。

也可以 `WebSearch "<company> press kit image"` 找官方 press kit。

### Step 3.2 — 下载

```bash
cd "$EXPLAINER_DIR/img"

# 关键：URL 里有 $ 必须用单引号，否则 bash 吃掉 → 拿到 9 字节 error
curl -sL -o image1.jpeg 'https://substack-post-media.s3.amazonaws.com/public/images/UUID_WxH.jpeg'
curl -sL -o image2.png 'https://cdn.sanity.io/images/.../image.png'
# ... 5-10 张

ls -lh    # 验证大小（<10KB 通常是 error 页）
md5 *.png *.jpeg    # 验证 MD5 不重复（substackcdn URL 偶尔返回错误图片）
```

### Step 3.3 — 注入图片到 slides

挑 4-6 张关键 walkthrough slide 注入图片：

```html
<div class="figure">
  <img src="img/<file>.<ext>" alt="...">
  <div class="figure-caption">说明 <span class="src">来源：...</span></div>
</div>
```

注入位置：**在 `.takeaway` 之前**。

Side-by-side 用 `.figure-row`。

---

## Phase 4 (3 min): Assemble

合并所有 agent 输出到主 deck。

```bash
cd "$EXPLAINER_DIR"

python3 <<'PYEOF'
parts = {n: open(f'part2-{n}.html').read() for n in ['A','B','C']}
slides, toc = [], []
for n in ['A','B','C']:
    c = parts[n]
    if '<!-- TOC' in c:
        body, t = c.split('<!-- TOC', 1)
        lines = t.split('TOC -->', 1)[0].strip().splitlines()
        toc.extend(l for l in lines if l.strip())
    else:
        body = c
    slides.append(body.rstrip())

html = open('index.html').read()
html = html.replace('  <!-- INSERT_PART2_SLIDES -->', '\n\n'.join(slides) + '\n')
html = html.replace('    <!-- TOC_INSERT_PART2 -->', '    ' + '\n    '.join(toc))
open('index.html', 'w').write(html)
PYEOF
```

---

## Phase 5 (5 min): Verify + cleanup

```bash
cd "$EXPLAINER_DIR"

# 检查
grep -c '<section class="slide"' index.html      # 应该等于 foundation + walkthrough 总数
grep -c 'href="#s'              index.html      # TOC 链接数应该相等
grep -n 'INSERT_PART\|TOC_INSERT' index.html    # 应该 0 行（无残留 placeholder）
grep -oE 'id="s[0-9a-z]+"' index.html | sort -u | wc -l   # 应该等于 slide 数（无重复 ID）

# 图片完整性
ls img/                                          # 所有引用的图都在
md5 img/*.{png,jpeg} 2>/dev/null | sort         # 无重复 MD5

# AI-voice 检查（必须 0 命中）
grep -cE "$(cat .claude/skills/explainer-deck/references/anti-ai-voice.md | grep -A2 'grep -nE' | tail -1 | sed 's/grep -nE "//;s/" .*//')" index.html

# 清理
rm part2-A.html part2-B.html part2-C.html
rm img/<size <1KB 的>   # 失败的下载
```

---

## Phase 6 (interactive): Q&A expansion loop

Deck 出来后，用户看的时候经常会问"这点不懂"——开始**反复扩写 specific slide** 的 loop。

### Pattern

1. 用户问："X 这个我看不懂"
2. **先回答 + 再问加不加**：
   - 在对话里写一段详细解释（数学 + 类比 + 示意图）
   - 末尾问："要不要把这段加到 slide N？"
3. 用户回 `加上` → Edit slide N 注入新内容
4. 用户回 `不用` 或别的问题 → 继续

### 注入新内容的常用位置

| 用户问的类型 | 注入位置 |
|---|---|
| "X 概念不懂" | 在相关 `<h3>` 节之间或之前 |
| "这个数学怎么推" | 在数字出现的 `<pre>` 之前加 `<h3>推导</h3>` |
| "为什么是 X 不是 Y" | 在结论前加 `<h3>为什么这样选</h3>` |
| "X 跟 Y 什么关系" | 加 `<table>` 对比 |
| "举个例子" | 加 `<div class="example">` |
| "深一层这是什么物理" | 加 `<h3>背后的物理</h3>` 段 |

### 插入新 slide 的字母后缀技巧

如果用户问的内容**大到值得单独一张 slide**（>200 字 + 多个新概念），不要塞到现有 slide，单独加：

```html
<section class="slide" id="s24h">   <!-- 字母后缀避免 renumber -->
  ...
</section>
```

TOC 也加一行：

```html
<a href="#s24h">24+ · 历史教训</a>
```

后缀建议：
- `h` = history（历史背景）
- `m` = math（数学推导）
- `q` = Q&A（用户问的深挖）
- `d` = deepdive（额外资料）

---

## Phase 7 (optional): Update deepdive resources

如果用户问的概念在 `resource-bank.md` 里没有合适资源——

1. WebSearch 找具体视频/blog
2. 验证 URL 仍可用
3. 加到对应 slide 的 `<div class="deepdive">`
4. 同步加到 `resource-bank.md`（标 vetted 日期）

**永远不用 channel URL，永远用具体 watch?v=ID URL**。这条规则没有例外。

---

## Time budget summary

| Phase | 时间 | 谁做 |
|---|---|---|
| 1 Setup + Foundation | 15-20 min | 主 agent |
| 2 Walkthrough (并行) | 10-15 min | 3 个 agent 并行 |
| 3 Image fetch + 注入 | 5 min | 主 agent |
| 4 Assemble | 3 min | 主 agent (bash script) |
| 5 Verify + cleanup | 5 min | 主 agent |
| **合计**（initial deck） | **~40 min** | |
| 6 Q&A expansion (interactive) | per question 3-5 min | 主 agent |

一个典型的 deck 在 40 分钟内可以达到 "60 slides + 5 张图 + 15 个 deepdive 资源链接" 的完成度。Q&A loop 之后可以扩展到 80+ slides 包含很多深挖。

---

## Common failure modes

1. **Agent 重复解释 foundation 概念** → 在每个 agent prompt 里精确列出 foundation slide 内容
2. **图片 URL 重复 / 损坏** → MD5 验证 + 单引号 URL + 直接 S3 不走 CDN
3. **Slide ID 冲突** → 每个 agent 给精确 ID 范围（s16-30 / s31-46 / s47-62）
4. **AI-voice 漏网** → 用 grep 二次扫描全文，命中就改
5. **Channel URL 滥用** → 用 WebSearch 找具体视频，永远不用 channel root
6. **新 slide 插入打乱全部 renumber** → 用字母后缀 `s24h`
