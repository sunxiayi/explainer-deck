# Resource Bank — vetted deepdive links by topic

Curated external resources for `.deepdive` boxes. All URLs validated as of 2026-05.
Re-verify before inserting into a new deck if it's been months.

## How to use

Find the topic of the slide. Copy the most relevant 1-2 resources. If the
slide is about a "one-stop" concept (FLOPs/bandwidth/roofline, lithography,
GPU 101), prefer a single must-read resource and mark the deepdive title
with "· 强推" or "· 必读".

---

## LLM / Inference / ML

### Transformer architecture, attention, training basics

- **Andrej Karpathy: "Let's build GPT from scratch"** — https://www.youtube.com/watch?v=kCc8FmEb1nY — YouTube · 2 h · Hand-codes a tiny transformer in PyTorch from zero. The single best resource for understanding attention/blocks.
- **Andrej Karpathy: "Intro to Large Language Models"** — https://www.youtube.com/watch?v=zjkBMFhNj_g — YouTube · 60 min · Science-popularizer version.
- **Lilian Weng: "The Transformer Family Version 2.0"** — https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ — Blog · Comprehensive variant catalog.

### Tokenization

- **Karpathy: "Let's build the GPT Tokenizer"** — https://www.youtube.com/watch?v=zduSFxRajkE — YouTube · 2 h · BPE from scratch.
- **OpenAI Tokenizer Playground** — https://platform.openai.com/tokenizer — Web · Try real splits live.

### KV cache, inference optimization

- **Lilian Weng: "Large Transformer Model Inference Optimization"** — https://lilianweng.github.io/posts/2023-01-10-inference-optimization/ — Blog · KV cache / paged attention / speculative decoding all in one.
- **Karpathy: "Let's reproduce GPT-2 (124M)"** — https://www.youtube.com/watch?v=l8pRSuU81PU — YouTube · 4 h · End-to-end implementation including inference paths.

### Roofline model, memory-bound vs compute-bound

- **Horace He: "Making Deep Learning Go Brrrr From First Principles"** — https://horace.io/brrr_intro.html — Blog · 20 min · ★ The classic. Should be linked from any FLOPs/bandwidth slide.

### Sharding / parallelism

- **HuggingFace: "Efficient Training on Multiple GPUs"** — https://huggingface.co/docs/transformers/v4.37.0/perf_train_gpu_many — Docs · Compares tensor/data/pipeline parallelism with code.
- **DeepSpeed paper** — https://arxiv.org/abs/2104.04473 — arxiv · Original Megatron-LM 3D parallelism paper.

### LLM hardware selection / GPU memory

- **Tim Dettmers: "Which GPU(s) to Get for Deep Learning"** — https://timdettmers.com/2023/01/30/which-gpu-for-deep-learning/ — Blog · Intuitive hardware selection + bandwidth/FLOPs.

---

## GPU architecture

- **Asianometry: How Nvidia Won AI** — https://www.youtube.com/watch?v=GuV-HyslPxk — YouTube · 20 min · Nvidia + CUDA 怎么从游戏卡变成 AI 霸主
- **Hot Chips conference** — https://hotchips.org — Free PDFs and (mostly) free videos from chip companies' annual technical talks.
- **ChipsAndCheese** — https://chipsandcheese.com/ — Blog · Deep architecture reviews of CPUs/GPUs.
- **AnandTech (legacy)** — https://www.anandtech.com — Archive only (site shut down 2024) but archives still readable for historical depth.

---

## Semiconductor manufacturing

### One-stop intro

- **Asianometry: TSMC Deep Dive (with Jon)** — https://www.youtube.com/watch?v=SDgrRQyBJZw — YouTube · 1 h · ★ TSMC 整套工艺历史 + 制造流程概览
- **Asianometry: How TSMC Keeps Getting Better** — https://www.youtube.com/watch?v=-DCZsT2plw8 — YouTube · 16 min · 制造流程 + 良率管理一气呵成

### Lithography & EUV

- **Asianometry: How ASML Won Lithography (& Why Japan Lost)** — https://www.youtube.com/watch?v=SB8qIO6Ti_M — YouTube · 17 min · ASML 怎么打败 Nikon/Canon
- **Asianometry: The Decision of the Century — Choosing EUV** — https://www.youtube.com/watch?v=fnTkvHaFEoU — YouTube · 20 min · EUV 物理 + 行业押注
- **ASML & EUV Lithography Deep Dive with Asianometry** — https://www.youtube.com/watch?v=Y1D7LfZk24k — YouTube · 光刻物理限制 + reticle limit 怎么来的

### Reticle limit, chiplet

- **SemiAnalysis: Die Size And Reticle Conundrum** — https://newsletter.semianalysis.com/p/die-size-and-reticle-conundrum-cost — Blog · 付费 · reticle limit 的成本模型
- **AnandTech archives** — https://www.anandtech.com — Search "chiplet" for legacy coverage

### Yield, defects, process variation

- **Asianometry: How TSMC Keeps Getting Better** — https://www.youtube.com/watch?v=-DCZsT2plw8 — YouTube · 16 min · 良率管理 + 工艺批次差异
- **SemiWiki forum** — https://semiwiki.com/ — Industry insiders discussing yield issues.

### Memory (HBM, DRAM scaling)

- **Asianometry: The Special Memory Powering the AI Revolution** — https://www.youtube.com/watch?v=yAw63F1W_Us — YouTube · 18 min · HBM 制造 + 为什么 AI 时代抢 HBM
- **SK Hynix tech blog** — https://news.skhynix.com — Direct from a HBM maker.

### Wafer-scale / Cerebras-specific

- **Cerebras CS-3 Walkthrough by Chief Architect Michael James** — https://www.youtube.com/watch?v=tlvfZulPYaw — YouTube · 45 min · Cerebras 首席架构师亲自讲 CS-3
- **Asianometry: Supersizing Wafer Scale — Powering Cerebras onto 5nm and 3nm** — https://www.youtube.com/watch?v=hh7A-0ogv5s — YouTube · 25 min · Cerebras 技术路线图

---

## Data center, thermal, power

- **ServeTheHome: Liquid Cooling High-End Servers (Direct to Chip / Rear Door / Immersion)** — https://www.youtube.com/watch?v=4Np1HnWiHb4 — YouTube · 21 min · 三种液冷方案实物对比
- **ServeTheHome: A Fun Data Center Tour at PhoenixNAP** — https://www.youtube.com/watch?v=qUmLnSEVVDw — YouTube · 21 min · 真实数据中心实地游
- **Open Compute Project** — https://www.opencompute.org/ — Site · Meta-led DC hardware standards. Liquid cooling specs, CDU reference designs all here.
- **Uptime Institute white papers** — https://uptimeinstitute.com — Free tier classification & PUE basics.

---

## Finance, IPO, capital structure

- **Matt Levine: Money Stuff** — https://www.bloomberg.com/account/newsletters/money-stuff — Email newsletter · Best writer on capital markets oddities (SPAC, warrants, dilution, etc.).
- **Stratechery (Ben Thompson)** — https://stratechery.com — Subscription · Strategy frameworks for tech companies.
- **Acquired podcast** — https://www.acquired.fm — Long form company histories. TSMC, Nvidia, ASML episodes are masterful.
- **Tegus / Alphasense** — Subscription · Expert call transcripts (industry insiders).

---

## AI strategy & competitive landscape

- **SemiAnalysis** — https://semianalysis.com — Subscription · ★ This is the source for AI hardware analysis.
- **Latent Space podcast** — https://www.latent.space — Free · Infra-focused AI podcast.
- **Dwarkesh Patel podcast** — https://www.dwarkesh.com — Free · Deep interviews with researchers and executives.

---

## 中文资源 (Chinese internet — 知乎 / B站 / 博客园)

Every deepdive box must be bilingual (see SKILL.md Step 7.5). Below are vetted-by-search Chinese resources by topic. **Caveat**: B站 reposts and 知乎 links die/move more often than YouTube — re-verify or warn the user. Vetted 2026-06 via search-result title+author match (not all opened individually).

### 神经网络 / 矩阵乘法 / Transformer
- **3Blue1Brown：深度学习之神经网络的结构（中字）** — https://www.bilibili.com/video/BV1bx411M7Zx/ — B站 · 19 min · 动画讲清神经网络在学什么
- **3Blue1Brown：线性代数的本质 · 矩阵与线性变换** — https://www.bilibili.com/video/BV1Ys411k7yQ/ — B站 · 系列 · "矩阵乘法到底在干嘛"讲到直觉级
- **3Blue1Brown 官方B站空间** — https://space.bilibili.com/88461692/ — 频道（注意力/反向传播等都有）

### Roofline / memory-bound / 性能分析
- **知乎：Roofline Model 与深度学习模型的性能分析** — https://zhuanlan.zhihu.com/p/34204282 — 知乎 · 中文最经典的 roofline 入门

### GPU / CUDA core / Tensor Core
- **ZOMI酱：Tensor Core 基本原理** — https://www.cnblogs.com/ZOMI/articles/18556565 — 博客园 · AI系统系列 · 国内讲 GPU/Tensor Core 最系统
- **AI 芯片 5 大架构拆解（CPU/GPU/TPU/NPU/LPU）** — https://www.bilibili.com/video/BV1vuoCBsEeb/ — B站 · 看清 GPU 在 AI 硬件里的位置

### 内存层级 / HBM / SRAM / DRAM
- **知乎：HBM、SRAM、DRAM 的特点对比** — https://zhuanlan.zhihu.com/p/657860237 — 知乎 · 三种内存差别 + 为什么 AI 抢 HBM

### 半导体 / 光刻 / 晶圆制造
- **史上最易懂的芯片制造讲解（中配，解析为原片3倍）** — https://www.bilibili.com/video/BV1YnYQziEBm/ — B站 · 从晶圆到芯片整套流程
- **老石谈芯（up 主）** — https://space.bilibili.com/612932327/ — B站 · 频道 · 中科院背景，光刻/制造硬核科普

### 稀疏 sparsity
- **知乎：一文带你读懂非结构化稀疏模型压缩和推理优化** — https://zhuanlan.zhihu.com/p/442273849 — 知乎 · 结构化 vs 非结构化稀疏

### 分布式训练 / 并行
- **知乎：大模型分布式训练并行技术（一）概述** — https://zhuanlan.zhihu.com/p/598714869 — 知乎 · 数据/张量/流水线并行系统综述

### Cerebras / wafer-scale (中文)
- **知乎：深挖 Cerebras — 世界上最大 AI 芯片的架构设计** — https://zhuanlan.zhihu.com/p/569595229 — 知乎 · 中文里核心+dataflow讲得最细
- **知乎：llm decode 加速器架构详解（一）Cerebras WSE** — https://zhuanlan.zhihu.com/p/2026781196298757013 — 知乎 · 从推理角度看 weight streaming / MemoryX
- **知乎：Cerebras、SambaNova 与 Groq — AI 芯片性能大对标** — https://zhuanlan.zhihu.com/p/1987225044905124706 — 知乎 · 把 Cerebras 放进竞品横向比

---

## Reference docs (when slide is about a specific spec)

- **Nvidia developer docs** — https://docs.nvidia.com — CUDA / cuDNN / Tensor Core spec
- **AMD ROCm docs** — https://rocm.docs.amd.com
- **TSMC press releases** — https://pr.tsmc.com — Process node announcements
- **Cerebras developer docs** — https://sdk.cerebras.net
- **Anthropic docs** — https://docs.anthropic.com
- **OpenAI docs** — https://platform.openai.com/docs

---

## Channel roots — LAST RESORT ONLY

Always search for the specific video first (use the WebSearch query template in `SKILL.md` § Step 7.5). Channel URLs make the user hunt through hundreds of videos — they're a usability failure. Only use these channel roots if:

1. You searched for the specific video and got nothing usable, AND
2. The channel is small enough that browsing is feasible (< 50 videos), AND
3. You include a clear hint like "搜 X 这个标题" in the description

Reputable channels worth browsing:

- https://www.youtube.com/@Asianometry — semis / TSMC / China tech
- https://www.youtube.com/@HighYield — chip architecture
- https://www.youtube.com/@ServeTheHomeVideo — servers / DC
- https://www.youtube.com/@DwarkeshPatel — AI interviews
- https://www.youtube.com/@LatentSpaceTV — AI infra
- https://www.youtube.com/@Cerebras — official Cerebras tech talks

---

## Maintenance

When you add a new resource:

1. Verify the URL is alive (curl head request or browser check).
2. Categorize it under a topic above (create a new topic if needed).
3. Include format hint ("· YouTube · 60 min" or "· Blog" or "· Docs").
4. Write a 1-line description that conveys "why this resource, not a generic intro".

When you find a resource that has died (404, channel deleted, paywalled-without-warning), remove it or replace with the closest equivalent.
