# Slide Patterns — Copy-paste 建块

每个 pattern 一个例子。用的时候改 title / 数字 / 内容 即可。

---

## 1. Standard slide skeleton

最小骨架——所有 slide 都从这个开始：

```html
<section class="slide" id="sN">
  <div class="slide-num">SLIDE NN</div>
  <h2>Slide 标题</h2>

  <p>主体段落。第一句话陈述这张 slide 要讲什么。</p>

  <h3>小节标题</h3>
  <p>...</p>

  <div class="takeaway">关键点：用一句话总结读完这张 slide 应该记住的东西。</div>
</section>
```

每张 slide **必须有**：`slide-num`、`<h2>` 标题、一个 `.takeaway` 收尾。
每张 slide **可选**：`<h3>` 小节、ASCII 图、表格、box（analogy/example/warning/deepdive）、图片。

---

## 2. Concept with analogy

讲一个抽象概念时配类比。`<div class="analogy">` 用 `类比` 前缀。

```html
<section class="slide" id="s5">
  <div class="slide-num">SLIDE 05</div>
  <h2>KV Cache——理解 Cerebras 一切限制的关键</h2>

  <p>LLM 生成一句话是<strong>一个 token 一个 token 蹦出来</strong>。每生成一个新 token，要回头"看"前面所有 token。</p>

  <p>问题：如果每次都重算前面所有 token，复杂度是 O(N²)，慢到不可用。</p>

  <p>解法：<strong>KV Cache</strong> —— 把每个 token 算过的 K 和 V 向量存下来。下次直接读，不重算。</p>

  <div class="analogy">类比饭店点单：每来一个新客人，服务员不会把所有旧菜重新做一遍——他记住已经做好的菜在哪里，新客人来了直接端走，只做新菜。KV cache 就是模型的"已做菜单"。</div>

  <div class="takeaway">"模型大" + "上下文长" + "用户多" 都会让 KV cache 膨胀——这是后面所有架构选择的根源。</div>
</section>
```

---

## 3. Numbers with concrete examples

涉及数字时配 `<div class="example">`。

```html
<section class="slide" id="s8">
  <div class="slide-num">SLIDE 08</div>
  <h2>FLOPs / Bandwidth / Arithmetic Intensity</h2>

  <p>评估一颗 AI 芯片，三个数最重要：</p>

  <h3>1. FLOPs — 算力</h3>
  <p><strong>Floating-point Operations per second</strong>。</p>
<pre>
1 TFLOPS  =  10¹²  次/秒
1 PFLOPS  =  10¹⁵  次/秒
1 EFLOPS  =  10¹⁸  次/秒
</pre>

  <div class="example">B300 GPU FP4 算力 = 13.5 PFLOPS = 13,500,000,000,000,000 次/秒。Cerebras WSE-3 FP16 dense = 15.6 PFLOPS。</div>

  <div class="takeaway">Cerebras 押注"很多 AI workload 是 memory-bound"——所以钱花在 SRAM 带宽，不在 FLOPs。</div>
</section>
```

---

## 4. ASCII diagram + table comparison

讲对比时用 `<pre>` 和 `<table>`：

```html
<section class="slide" id="s9">
  <div class="slide-num">SLIDE 09</div>
  <h2>内存金字塔——SRAM / HBM / DDR 区别</h2>

<pre>
速度 ────────────────────────── 容量

     寄存器     &lt;1 ns      字节级       ← 最快
        ↓
     L1 cache   ~1 ns      KB
        ↓
     SRAM      ~5 ns     几十 MB ~ 几十 GB
        ↓
     HBM      ~150 ns    几十 GB ~ 几百 GB
        ↓
     DDR      ~100 ns    几百 GB ~ TB
</pre>

  <table>
    <thead><tr><th></th><th>SRAM</th><th>HBM</th><th>DDR</th></tr></thead>
    <tbody>
      <tr><td>速度</td><td>极快</td><td>中</td><td>中</td></tr>
      <tr><td>带宽</td><td>PB/s 级</td><td>TB/s 级</td><td>~100 GB/s</td></tr>
      <tr><td>价格 per GB</td><td>$$$$$</td><td>$$$$</td><td>$$</td></tr>
    </tbody>
  </table>

  <div class="takeaway">SRAM 比 HBM 快 30 倍，但同样面积只能装 1/100 的数据。Cerebras 用速度换容量——一切优势和限制的根源。</div>
</section>
```

---

## 5. Concept with caveat (warning)

需要提醒用户"注意"的事用 `<div class="warning">`：

```html
<section class="slide" id="s50">
  <div class="slide-num">SLIDE 50</div>
  <h2>Photonic wafer + Ranovus——往 z 轴方向开一扇天窗</h2>

  <p>电学走 wafer 边缘走不通，Cerebras 的解法：<strong>在 WSE 上面再 hybrid-bond 一张"光子晶圆"</strong>。</p>

  <p>关键合作方：Ranovus（加拿大公司，做 co-packaged optics）。</p>

  <div class="warning">原文原话：Cerebras 声称 photonic wafer "<strong>不是 LLM 推理需要的</strong>"。他们追这个是为了 HPC（科学计算）客户——近期 IPO 投资人不能把这件事算进估值里。</div>

  <div class="takeaway">SemiAnalysis 对这条路线持<strong>怀疑态度</strong>。它存在路线图上的意义，是证明 Cerebras 自己也意识到 150 GB/s 是个真问题。</div>
</section>
```

---

## 6. Foundation slide with deepdive resources

Foundation slide 应该带 `<div class="deepdive">` 链接外部资源：

```html
<section class="slide" id="s8">
  <div class="slide-num">SLIDE 08</div>
  <h2>FLOPs / Bandwidth / Arithmetic Intensity</h2>

  <p>评估一颗 AI 芯片，三个数最重要...</p>
  <!-- 概念内容 -->

  <div class="takeaway">Cerebras 押注"很多 AI workload 是 memory-bound"——钱花在 SRAM 带宽。</div>

  <div class="deepdive">
    <div class="deepdive-title">想深入这个概念 · 强推</div>
    <ul>
      <li><a href="https://horace.io/brrr_intro.html" target="_blank">Horace He: Making Deep Learning Go Brrrr From First Principles</a><span class="meta"> · Blog · 20 min</span> — <strong>看懂这一篇 roofline / memory-bound vs compute-bound，本节 80% 内容你就吃透了</strong></li>
      <li><a href="https://timdettmers.com/2023/01/30/which-gpu-for-deep-learning/" target="_blank">Tim Dettmers: Which GPU for Deep Learning</a><span class="meta"> · Blog</span> — 硬件选型 + 直觉性 FLOPs/bandwidth 解释</li>
    </ul>
  </div>
</section>
```

**关键规则**：

- 永远用具体视频/文章 URL，不用 channel root
- 每条链接配格式标签（YouTube · 60 min / Blog / Docs）+ 1 行 description
- 必读资源标 "· 强推" 或 "· 必读"
- 资源数量 1-3 条够，多了反而稀释

详见 `resource-bank.md` 已 vetted 的 URL 库。

---

## 7. Slide with embedded image

讲完概念后配真实图：

```html
<section class="slide" id="s35">
  <div class="slide-num">SLIDE 35</div>
  <h2>Engine Block——四层三明治</h2>

  <p>Cerebras 把整套"硅 + 散热 + 供电"做成一个独立模块...</p>

<pre>
   ┌─────────────────────────────────────┐
   │  冷却液 manifold                    │
   ├─────────────────────────────────────┤
   │  Cold Plate                         │
   │  ▓▓▓▓ 微通道 ▓▓▓▓                  │
   ├─────────────────────────────────────┤
   │  WSE-3 Wafer                        │
   ├─────────────────────────────────────┤
   │  Compliant Connector                │
   ├─────────────────────────────────────┤
   │  PCB                                │
   └─────────────────────────────────────┘
</pre>

  <div class="figure">
    <img src="img/sa-engine-block.jpeg" alt="Engine Block 真实剖面图">
    <div class="figure-caption">Engine Block 真实剖面图——四层结构对应上面的示意。<span class="src">来源：SemiAnalysis / Cerebras</span></div>
  </div>

  <div class="takeaway">Engine Block = "硅 + 冷板 + 弹性连接器 + PCB 的整体可拆模块"。</div>
</section>
```

**图片选择规则**：

- 真实产品/官方图 > 概念图 > ASCII 图（但 ASCII 在跨设备显示一致）
- 配 `figure-caption` 说明 + `<span class="src">` 标来源（必须）
- 单图用 `.figure`，对比图用 `.figure-row`（包含 2+ `.figure`）
- 图片放在 `<takeaway>` 之前

---

## 8. Side-by-side comparison images

```html
<div class="figure-row">
  <div class="figure">
    <img src="img/wse3-chip.png" alt="WSE-3 chip product shot">
    <div class="figure-caption">WSE-3 芯片产品照。<span class="src">来源：Cerebras</span></div>
  </div>
  <div class="figure">
    <img src="img/cs3-system.png" alt="CS-3 system">
    <div class="figure-caption">CS-3 服务器系统。<span class="src">来源：Cerebras</span></div>
  </div>
</div>
```

---

## 9. Math walkthrough slide

复杂概念配公式 + 一步步代数据：

```html
<section class="slide" id="s24">
  <div class="slide-num">SLIDE 24</div>
  <h2>Wafer 总良率——Murphy's Model 算给你看</h2>

  <p>半导体工业有个经典良率公式，叫 <strong>Murphy's Model</strong>。</p>

  <h3>Murphy 公式</h3>
<pre>
Y = e^(-A × D)

Y：yield（能用的 die 比例）
A：die 面积 (cm²)
D：缺陷密度 (defects/cm²)
</pre>

  <h3>代入数字，看普通 GPU 的良率</h3>
<pre>
H100 (814 mm² = 8.14 cm²)，5nm 工艺 D = 0.1 defect/cm²：
   Y = e^(-8.14 × 0.1)
     = e^(-0.814)
     = 0.443
     = <b>44.3% 良率</b>

意思：晶圆上的 100 颗 H100，只有 44 颗能卖。
</pre>

  <h3>代入 Cerebras 整张 wafer</h3>
<pre>
整张 WSE-3 (462 cm²)，同样 D = 0.1：
   Y = e^(-462 × 0.1)
     = e^(-46.2)
     ≈ <b>0.0000000000000000001</b>   （基本就是 0）
</pre>

  <div class="takeaway">"Murphy 公式说 0% 良率，实际跑出 100%" = Cerebras 用"冗余 + 重路由"改写了半导体行业 60 年的良率假设。</div>
</section>
```

---

## 10. Synthesis / closing slide

最后总结性的 slide：

```html
<section class="slide" id="s61">
  <div class="slide-num">SLIDE 61</div>
  <h2>终极赌注——3 件事必须同时成立，Cerebras 才赢</h2>

  <p>合在一起看，SemiAnalysis 整篇文章的核心论点其实是一个"三个 if 都对，Cerebras 起飞"的赌局。</p>

<pre>
赌注 1：模型够好
  ├── GPT-5.5 级别智能能塞进 120B
  └── 用户愿意为"GPT-5.5 速度版"付溢价
                            │
                            ▼  且
赌注 2：部署标准化
  └── CS-4 把 LPM/kW 拉回 1.5-1.7
                            │
                            ▼  且
赌注 3：长 context 问题不致命
  └── KV cache 压缩 + 96.3k ISL 真实需求被满足
</pre>

  <p>呼应一开头 Opus 4.6 fast 的故事——整篇 thesis 闭环就在这里。</p>

  <div class="takeaway">Cerebras IPO 不是赌"硬件够不够屌"——是赌"OpenAI 的 1.25GW 期权会不会被行权"。一个二元事件决定估值 $40B 还是 $150B+。</div>
</section>
```

---

## 11. Final / wrap-up slide

```html
<section class="slide" id="s62">
  <div class="slide-num">SLIDE 62 · 完</div>
  <h2>总结 + 推荐继续看什么</h2>

  <h3>一张图回顾全篇</h3>
<pre>
Cerebras 全部故事 = 一颗超大芯片 × 一个超大客户 × 一个超快赛道
</pre>

  <h3>推荐继续读</h3>
  <ul>
    <li><strong>SemiAnalysis InferenceX</strong> — throughput vs interactivity 曲线原始论文</li>
    <li><strong>Cerebras S-1</strong> — MRA / warrant 法律细节</li>
    <li><strong>DeepSeek V3 论文 MLA 章节</strong> — KV cache 压缩工程实现</li>
  </ul>

  <div class="takeaway">SemiAnalysis 这篇真正的价值不在结论，在它的"全栈"——把 silicon / software / power / cooling / money 5 件事在一篇里串起来。</div>
</section>
```

---

## 12. Insert new slide WITHOUT renumbering — letter suffix trick

如果 deck 已经完成，用户问"这点想看更深的"要插入新 slide，用**字母后缀**避免全文 renumber：

```html
<!-- 原本是 s24 → s25，要在中间插一张 -->
<section class="slide" id="s24">
  <!-- 原 s24 内容 -->
</section>

<!-- 新插入的 slide，ID 用字母后缀 -->
<section class="slide" id="s24h">
  <div class="slide-num">SLIDE 24+ · 历史教训</div>
  <h2>Trilogy 1984 失败 vs Cerebras 2024 成功</h2>
  <!-- 新内容 -->
</section>

<!-- s25 保持不变 -->
<section class="slide" id="s25">
  <!-- 原 s25 内容 -->
</section>
```

TOC 同步加一行：

```html
<a href="#s24">24 · Wafer 总良率 · Murphy's Model</a>
<a href="#s24h">24+ · Trilogy 历史教训</a>
<a href="#s25">25 · 44GB SRAM 看着多</a>
```

**好处**：

- 不用全文 renumber 数十张 slide
- 用户视觉上一眼看出"24+"是 24 的延伸
- JS 总数自动算（`slides.length`），数字会更新

字母后缀建议：`h` (history) / `m` (math) / `q` (Q&A) / `d` (deepdive)，按内容性质选。

---

## 13. Q&A response — expand specific slide on demand

Deck 建完后，用户问"这块讲得不够细，能展开吗"——找到对应 slide，在合适位置 `Edit` 注入更多内容。

模式：

1. 用 `grep -n 'id="sN"'` 找 slide 位置
2. 读出当前 slide 内容
3. 选择注入点——通常在 `<h3>` 节之间，或 `.takeaway` 之前
4. 加 `<h3>新小节标题</h3>` + 内容
5. 如果加 `<table>` / `<pre>` 用现成 CSS class

例子：用户问"为什么 core 做这么小"——找 s22，在 "缺陷的物理学" 之后插 "缺陷的 5 种类型 + sizing tradeoff + BIST"：

```html
<!-- 原内容 -->
<h3>缺陷的物理学</h3>
<pre>...</pre>

<!-- 注入新内容 -->
<h3>缺陷有 5 种主要类型</h3>
<table>
  <thead><tr><th>类型</th><th>原因</th><th>占比</th></tr></thead>
  <tbody>...</tbody>
</table>

<h3>决策：为什么是 0.05 mm² 而不是 0.5</h3>
<pre>...</pre>

<h3>怎么测出哪些 core 坏了 — BIST</h3>
<pre>...</pre>

<!-- 原"小 core 的代价"继续 -->
<h3>"小 core" 的代价</h3>
...
```

详见 `SKILL.md` § "Q&A expansion loop" 章节。

---

## 14. Common voice mistakes to avoid

每张 slide 写完前，搜一遍以下词，确保 0 命中：

```
任何 / 所有 / 每个 / 必须 / 反复强调
本质上 / 不是X而是Y / 底层逻辑 / 核心在于
绕不开 / 躲不掉
最大的感受 / 印象最深 / 读到这里我
终于来了 / 颠覆 / 划时代 / 重新定义
更狠 / 狠的 / 骚操作 / 更绝
```

完整 banlist + grep 命令见 `.claude/skills/explainer-deck/references/anti-ai-voice.md`。

---

## Style reminders

- **永远用 Unicode 几何符号代替 emoji**：▸ ◂ ▲ ▼ ★ ✓ ✗ ※
- **行内英文术语用 `<code>`**：<code>KV cache</code>、<code>BIST</code>、<code>elastomer socket</code>
- **第一次出现术语时**写 "中文（English）"，例如 "缺陷（defect）"、"算术强度（arithmetic intensity）"
- **数字保留单位**：`50 W/cm²`、`25,000 安培`、`160 μm`、`$24.6B`
- **类比要具体**：不说"很多"，说"25 微波炉"；不说"很小差"，说"一根头发宽"
