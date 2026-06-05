# Anti-AI Voice Rules — Chinese editorial content

A shared reference for all skills that produce Chinese editorial content (xhs cards, substack summaries, news cards, captions, etc.). When LLMs write Chinese, they default to a set of phrasings that real writers rarely use. This doc lists those phrasings, why they're bad, what to write instead, and a grep self-check that any skill can run before sign-off.

## When to apply

Any skill whose output includes Chinese prose that summarizes, reflects on, or comments about external content — articles, books, interviews, technical docs. Examples: article summaries, carousel/card copy, captions, social posts, teaching decks.

Skip when: the output is a direct literal translation of a source, code, terse UI text, or English-only.

## What this catches

Real readers detect LLM-generated Chinese through specific phrasing patterns. Across many user feedback rounds, **9 categories** consistently surface:

1. Insight-frame openers
2. False-dichotomy reframing
3. Vague universalizing about hidden truths
4. Inevitability fatalism
5. Abstract authority
6. Manufactured strawman dichotomies
7. Absolutes
8. Performative reading / looking reactions
8a. Manufactured behavior change / fake forward-looking habits
8b. Sentimental anthropomorphism / fake emotional duration claims
9. Hype-style event inflation ("a thing the internet waited 30 years for")

Plus 2 meta-rules: examples must be **concrete**, memorable quotes must be **preserved with original + translation**.

---

## 1. Insight-frame openers (formulaic "I will now share wisdom")

Banned phrases:
- 我读完最大的感受是 / 最大的体会是 / 印象最深的是
- 归根结底 / 说到底 / 本质上 / 究其本质
- 最重要的不是 X，是 Y
- 真正让我意识到的是

**Why bad**: formulaic openers that pretend to deliver wisdom. Real writers don't announce their insights this way.

**Fix**: state the observation as a flat fact. The reader can decide whether it's a takeaway.

## 2. False-dichotomy reframing (rhetorical inversion as fake insight)

Banned phrases:
- 不是 X，而是 Y / 与其说 X，不如说 Y / 看似 X，实则 Y
- 不像在讲 X，更像是在讲 Y
- 表面上是 X，背后是 Y
- 单看 X 不 Y，合在一起 Z / 拆开看 X，合起来 Y / 分开看每一 X，加起来 Y / 一项一项看 X，连起来 Y（"whole-vs-parts reveal"——把"单独看不起眼，合在一起厉害"包装成深刻观察）

**Why bad**: rhetorical inversion masquerading as a deep observation. Just two ways of saying the same thing in opposing directions. The whole-vs-parts variant is the same move with different grammar — "alone X, together Y" pretends to deliver a synthesis insight without committing to a specific claim.

**Fix**: contrast specific named things side-by-side, not abstract X-vs-Y inversions. For whole-vs-parts, either state the combined effect directly ("这一组合就是 GTM 版的 news feed") or skip the meta-framing entirely.

## 3. Vague universalizing about hidden truths

Banned phrases:
- 那些没人说的 / 没人明说 / 藏在 X 之下的
- 每个人都 X，却很少 Y / 谁都知道 X，但很少有人 Y
- 不为人知的 / 真相是

**Why bad**: claims of secret/hidden knowledge that the writer is uniquely revealing. Almost always overclaim.

**Fix**: name the specific gap (e.g. "在中文社区里讨论得少" instead of "没人说的").

## 4. Inevitability fatalism

Banned phrases:
- 绕不开 / 躲不掉 / 回避不了 / 必然要面对
- 终将 / 无法逃避

**Why bad**: dramatized framing of normal trade-offs as cosmic destiny.

**Fix**: describe the trade-off directly.

## 5. Abstract authority

Banned phrases:
- X 的底层逻辑 / X 的本质 / X 的核心在于
- X 背后真正的问题是

**Why bad**: gestures at depth without delivering it.

**Fix**: name the specific mechanism, paper, person, or decision.

## 6. Manufactured strawman dichotomies + dramatized framing

Banned phrases:
- 听人喊 "X" / 总有人说 "X"
- 有人说 X 就好，有人说 X 就废，多半是因为…
- X 就对了 / X 就废了 / 一刀切 (in invented quotation marks attributed to nobody)

**Why bad**: manufactures opposing voices to look balanced, then delivers "the real take" — a classic LLM rhetorical move.

**Fix**: state your point directly without inventing strawmen. If you must reference a debate, name the actual debate.

## 7. Absolutes

Banned phrases:
- 任何 / 所有 / 每个 / 必须 / 反复强调

**Why bad**: real writers hedge; LLMs overclaim.

**Fix**: weaken to 大部分 / 多半 / 你得 / 提到了 etc.

## 8. Performative reading / looking reactions

Banned phrases:
- 我读得最慢 / 我读得最久 / 我读得最快 / 我读得最来劲 / 我读得最认真
- 我看得最 X
- 读到这里我 (停了 / 想了很久 / 合上了书)
- 让我印象深 / 让我印象最深 / 印象最深的是
- 我反复读 / 我反反复复读 / 反复琢磨
- 这段让我想了很久

**Why bad**: describes YOUR reading process instead of what's on the page. The reader doesn't care how slowly/quickly/intensely you read. The performative gesture signals sincerity / depth without committing to a claim.

**Fix**: state what the section says, not your reaction to reading it. If notable, name what specifically makes it notable.

## 8a. Manufactured behavior change / fake forward-looking habits

Banned phrases:
- 合上书后我留了个习惯 / 合上书后我决定 / 合上书后我开始
- 读完之后我留了个习惯 / 读完之后我会
- 从此以后我会 / 从今以后我准备
- 我现在每次 X 都会
- 以后做 X 时我会 / 下次我会

**Why bad**: manufactures a personal behavior change that sounds caring/actionable but is fabricated. Real readers rarely change a specific habit because of one article.

**Fix**: attribute action to the AUTHOR (`书里建议X`, `作者给的提醒是`), or describe it as an idea worth considering, NOT as your new habit.

## 8b. Sentimental anthropomorphism / fake emotional duration claims

Banned phrases:
- 这本书陪了我 N 年 / 这本书陪伴我 / 这本书陪着我走过
- 这本书在我书架上 N 年 (when sentimental, not literal)
- 这本书像老朋友 / 像一位老师
- 一遍又一遍翻过 / 我反复翻这本书
- 这本书改变了我的人生
- 第一版陪了我 N 年

**Why bad**: books, articles, films don't "accompany" anyone — that's projection. Round-number duration claims are too neat, too sentimental.

**Fix**: drop the sentimental duration. If past engagement is relevant, be concrete (`第一版我读过`, `第一版很多工程师手边都有过`). Don't anthropomorphize.

---

## 9. Hype-style event inflation

Banned phrases:
- 互联网等了 X 年的事 / 等了 X 年才发生 / X 年来终于
- X 年里(从来)没人做成的事 / X 年没人能做到
- 整整 X 年(都|从)没 / 整整 X 年没人
- 终于来了 / 终于做成了 / 终于发生了
- 万年一遇 / 百年一遇 / 千载难逢
- X 年最重要的 / X 年最关键的 / X 年最大的
- 改变历史 / 改变了历史 / 历史性的(一刻|时刻)
- 划时代 / 划时代的 / 跨时代
- 翻天覆地 / 前所未有 / 史无前例
- 翻开新的一页 / 开启了新纪元 / 新时代的开端
- 颠覆 / 颠覆了 / 颠覆性
- 一举改写 / 一战改写 / 改写了规则
- 重新定义(了)?

**Why bad**: dramatic event framing that inflates a normal product launch
into a generational moment. Real reporting describes what changed and lets
the reader judge significance. The hype pattern is a tell of LLM-flavored
writing — humans almost never reach for "互联网等了 30 年的事" unedited.

**Fix**: state the factual change. Drop the cosmic adjectives. If
historical context is real, name it precisely — "HTTP 402 状态码在 1997
年写进规范后，第一次被大规模实现" beats "互联网等了 30 年才发生的事."
If you want suspense, point at the **forward implications** (what this
might mean a year from now) rather than inflating the present moment.

❌ "5月7日，AWS 把一件互联网等了 30 年才发生的事做成了。这是改变历史的一刻。"
✅ "5月7日，AWS 上线 AgentCore Payments —— 这是 HTTP 402 状态码从 1997
   年写进规范后第一次被一家云厂商大规模实现。"

---

## 10. Dramatized "extreme" descriptors (狠 / 猛 / 吓人 family)

Banned phrases:
- 更狠 / 狠的(是|细节|做法|地方|玩法|招|手) / 狠在 / 狠到 / 够狠 / 狠人
- 更猛 / 猛的是 / **看着就猛 / 看上去就猛 / 看起来就猛** / 真猛 / 太猛 / 蛮猛 / 猛到 (when used as dramatic emphasis, not literal physical force like 火力猛 / 凶猛)
- **数字看着就猛 / 数字 X 猛** (number-as-impressive commentary)
- **吓人 / 吓人的数字 / 真吓人** (作为评价词；"吓"在物理恐吓语境不算)
- 这一招更绝 / 更骚的操作 / 骚操作 (same dramatic-emphasis family)
- 爆表 / 炸裂 / 炸了 (作为评价词)
- 真牛 / 太牛 / 牛 X / 屌爆了 / 太屌了 (颂扬性短形容词)

**Why bad**: stylized adjectives that AI loves to use to dramatize a
normal technical detail. They signal "look at this surprising thing" without
committing to a specific assessment, and they read as performative
emphasis rather than reporting. Real writers either describe the thing
factually or name what specifically makes it noteworthy ("unusual",
"rare in commodity fabs", "first time"-with-evidence).

**Fix**: describe what makes it noteworthy directly. Use neutral framing
words like "反常规", "不太常见", "特殊", "另一处", or just drop the
descriptor and let the fact stand on its own.

❌ "还有个更狠的细节：每批晶圆都重做一套 mask。"
✅ "还有一处反常规的操作：每批晶圆都重做一套上层金属层 mask。"

❌ "Cerebras 这一招更骚——用 scribe line 走线。"
✅ "Cerebras 还做了一件商用 fab 里少见的事：用 scribe line 走线。"

---

## 10b. Colloquial short verbs (一拳一脚的口语短动词)

Banned phrases (when used in serious tech/business writing):
- 捞起来 / 把 X 捞起来
- 直接砸 (X 资源 / X 钱 / X MW)
- 满血 / 满血跑 (作为硬件性能形容)
- 飞起 (作为速度评价)
- 卡死 (描述硬件瓶颈时)
- 干掉 (描述技术方案失败时——但 "蒸发干掉 / dry out" 翻译时不算)
- 牛 / 屌 / 猛 (作为评价词)
- 整 / 闹 / 玩 (作为一字动词搭专业术语)

**Why bad**: tech-article register expects substantive, slightly formal verbs.
One-shot SVO punchy verbs like "捞 / 砸 / 整 / 干" are casual chat register —
they make the article feel like a tweet thread rather than a magazine piece.
The mismatch between technical depth (e.g. "84 个 Vicor brick + VPD") and
casual verbs ("直接砸 750MW 把它捞起来") feels jarring.

**Fix**: use substantive / formal verbs.

| ❌ 太轻 | ✓ 文章感更稳 |
|---|---|
| 捞起来 | 重新带回视线 / 请回主桌 / 拍板与之深度合作 |
| 直接砸 (X) | 投入 (X) / 押下 (X 的赌注) / 包下 (X) |
| 干掉 (技术失败) | 失效 / 崩溃 / 走不通 |
| 卡死 (硬件) | 受限于 / 卡在 / 瓶颈在 |
| 满血 / 满血跑 | 满负载 / 跑满算力 / 100% 利用 |
| 飞起 | 速度拉满 / 跑出极速 |
| 牛 / 屌 / 猛 | 出色 / 突出 / 表现强 |

❌ "5 年前没人看好的 Cerebras，今年 OpenAI 直接砸 750MW 把它捞起来。"
✅ "5 年前业内对 Cerebras 普遍持保留意见，今年 OpenAI 把它从冷板凳上请回主桌——签下 750MW 算力、$24.6B backlog。"

❌ "把数代进去——GPU 卡死，Cerebras 满血。"
✅ "把数代进去——GPU 等内存等到闲死，Cerebras 跑满算力。"

❌ "vapor chamber 直接干掉。"
✅ "vapor chamber 直接失效。"

**Caveat**: 这些词很多有合法技术语境（"程序卡死" / "蒸发干掉 / dry-out"）。
所以 grep 时**只针对最 unambiguous 的短语模式**——具体见 self-check 段。

---

## 10c. Forced novelty metaphors (硬凑"画面感"的比喻)

Banned phrases:
- 往里写得有人扣扳机 / 扣下扳机 / 扣动扳机（源文只说 "trigger / 触发器"，被写成"扣扳机"这个开枪动作）
- 同类：把"启动 / 触发 / 开启 / 推一把"硬写成 踩一脚油门 / 拧开阀门 / 摁下开关 / 点一把火 这类与上下文无关的身体动作比喻

**Why bad**: 比喻不是承重的——它只是给一个平常的机制词（触发器、启动）裹上一层戏剧化画面。
真正的技术写作用平实的术语；源文自己写的就是 "trigger"，不是 "pull the trigger"。
读者一眼能看出这是为了"显得生动"而硬加的装饰，反而是 LLM 腔的标志。

**Fix**: 用源文给的那个平实机制词。如果源文已经给了一个比喻（小本子 / 工作手册 / 闹钟），
就沿用那一个，别再自己发明第二个互相打架的比喻。

❌ "Memory 和 Skill 都是仓库，往里写得有人扣扳机。"
✅ "Memory 和 Skill 都是仓库，往里写需要一个触发器。"

**Caveat**: 贴切的、源文给的、或已成俗的比喻不在此列（闹钟提醒 / 随身小本子 都没问题）。
这一条只针对**自己硬加的花哨动作比喻**，不是禁掉所有比喻。

---

## Meta-rule A: Examples must be concrete

When the source gives examples, use the source's actual examples — not generic substitutes invented to look thorough. Every example must reference at least one of:
- A named entity (person / company / system / publication / place)
- A specific number or quantity
- A specific consequence with who pays the cost

When the source lists multiple cases (`payment networks / banks / airlines / HR`), include them or pick the most striking 2-3. Don't reduce a named list to a vague `各种 AI 系统`.

❌ "作者举了一个具体例子：一份预测信用风险的算法用错地方就成了歧视工具。" (fabricated)
✅ "书里举的几个场景都不抽象——支付网络要拦诈骗交易，银行要拦坏账贷款，航空公司要拦劫机者，HR 系统要筛掉'不靠谱'的应聘者。" (article's actual list)

## Meta-rule B: Preserve memorable quotes (original + translation)

When the source contains a memorable line (a quotable aphorism, a phrase that captures the thesis), preserve it with BOTH the original AND a Chinese translation. Never paraphrase a 金句 away.

Markdown convention for quotes:

```
> "Machine learning is like money laundering for bias."
> 机器学习像是给偏见洗钱。
```

The renderer styles the original (italic, primary text) and translation (gray) as a paired blockquote.

When to use:
- The author italicized / set it off in the source
- It compresses a thesis into one sentence
- It uses metaphor or wordplay that loses something in translation

Rules: always both lines, keep the quotation marks in the original, faithful (not literal) translation, place the quote near the argument it supports.

---

## Self-check (run before sign-off)

```bash
SLUG=<your-markdown.md>
grep -nE "最大的感受|归根结底|说到底|本质上|不是.*而是|不像在讲.*更像|没人(明)?说|绕不开|躲不掉|底层逻辑|核心在于|听人喊|就对了|就废了|任何|所有|每个|必须|反复强调|我读得最|我看得最|读到这里我|让我印象(最)?深|印象最深|我反复读|我反反复复|合上书[后我]|读完之后我|从此以后我|我现在每次|以后我会|这次读完(，我|我)|陪了我[一二三四五六七八九十0-9]+年|陪伴(着)?我|陪着我走过|像老朋友|像一位老师|改变了我的人生|一遍又一遍|等了[一二三四五六七八九十0-9]+年|[一二三四五六七八九十0-9]+年里(从来)?没人|整整[一二三四五六七八九十0-9]+年|终于(来了|做成了|发生了)|万年一遇|百年一遇|千载难逢|改变(了)?历史|历史性的(一刻|时刻)|划时代|跨时代|翻天覆地|前所未有|史无前例|翻开新的一页|开启了新纪元|颠覆(了|性)?|一举改写|改写了规则|重新定义|合在一起看|单看.*合在一起|拆开看.*合起来|拆开看.*合在一起|分开看.*加起来|一项一项看.*合起来|一个一个看.*加起来|更狠|狠的(是|细节|做法|地方|玩法|招|手)|够狠|狠人|狠在|狠到|更猛|更绝|骚操作|更骚|捞起来|直接砸|满血跑|看着就猛|看上去就猛|看起来就猛|真猛|太猛|猛到|吓人的数字|真吓人|爆表|炸裂|真牛|太牛|屌爆|太屌|扣扳机|扣下扳机|扣动扳机" "$SLUG"
```

Pass criterion: zero hits. Any hit → rewrite that line before showing the user.

The exception: literal quotes from the source article are preserved as-is. If the author literally wrote "the underlying logic," translate it faithfully — that's not LLM voice, it's translation. Wrap such lines in the `> quote` blockquote convention so they're visually attributed.

---

## How to integrate into your skill

In your skill's `SKILL.md`:

```markdown
**Voice rules (Chinese editorial)**: every paragraph must pass the anti-AI-voice rules at
`.claude/skills/explainer-deck/references/anti-ai-voice.md`. Run the grep self-check from that file before
the human approval gate. Zero hits is the bar.
```

In your skill's `references/` (or wherever you describe voice): link to this file rather than duplicating the banlist. When you add a new pattern, add it here so all skills benefit.

## Maintenance

When a user flags a new AI-flavored pattern:
1. Add the pattern as a new banned category in this doc (or extend an existing one).
2. Add the trigger phrases to the grep regex.
3. Add a worked before/after example.
4. Note the user-flagged source if it's the first time the pattern was caught.

This file is intentionally append-only — patterns once banned stay banned.
