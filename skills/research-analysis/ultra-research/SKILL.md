---
name: ultra-research
description: "多AI并行深度研究。当用户需要对某个主题进行全面调研、深度研究、多方对比、或需要覆盖多个维度和来源的综合分析时触发。适合复杂主题（技术选型、竞品分析、行业趋势、争议性话题等），不适合简单事实查询。通过多个AI服务并行研究，交叉验证，输出带引用的综合报告。"
allowed-tools:
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_click
  - mcp__playwright__browser_type
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_evaluate
  - mcp__playwright__browser_run_code
  - mcp__playwright__browser_wait_for
  - mcp__playwright__browser_press_key
  - mcp__playwright__browser_tabs
  - mcp__playwright__browser_close
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(mv *)
  - Bash(cp *)
  - Bash(pkill *)
  - Bash(sleep *)
  - Bash(date *)
  - Read
  - Write
  - Edit
  - WebSearch
  - WebFetch
  - Grep
  - Glob
---

# 深度研究 Skill

三段式：**理解需求 → 迭代探索 → 整合报告**。

通过 Playwright MCP 控制多个 AI 服务进行并行研究。各服务交互细节见 reference 文件。

## 前置条件

- **Playwright MCP** 需以持久化浏览器模式运行（`--user-data-dir`），这样各 AI 服务的登录态才会保留
- 用户需要**预先在 Playwright 浏览器中登录**要使用的 AI 服务（Gemini、ChatGPT、Claude、Grok）——不需要全部登录，登录了哪些就用哪些
- 本 skill 的选择器基于**中文 UI 环境**；英文 UI 下按钮名和 placeholder 会不同，需用 `browser_snapshot` 实时探测

## 可用的 AI 服务与模式

| 服务 | 模式 | 耗时 | 特点 |
|------|------|------|------|
| Gemini Pro | 快速 | 10-60s | 快速问答、事实查证（有搜索能力） |
| Gemini Deep Research | 深度 | 5-10min | 多源综合、广度覆盖 |
| ChatGPT Thinking | 快速 | 10-120s | 深度推理、结构化分析 |
| ChatGPT Deep Research | 深度 | 5-30min | 多源综合、广度覆盖 |
| Claude Opus Extended | 快速 | 10-120s | 深度推理、方案设计 |
| Grok 快速/专家 | 快速 | 10-60s | **X/Twitter 内容搜索**、时效性讨论和趋势 |
| Grok DeepSearch | 深度 | 数分钟 | 深度搜索、社交媒体观点汇集 |

**这些是工具箱，不是流水线。** 根据研究需要灵活选用和组合。

交互参考：
- [references/gemini.md](references/gemini.md) — Gemini 操作、选择器、提取
- [references/chatgpt.md](references/chatgpt.md) — ChatGPT 操作（**最脆弱的服务，注意防御**）
- [references/claude-web.md](references/claude-web.md) — Claude 操作、选择器、提取
- [references/grok.md](references/grok.md) — Grok 操作（**X/Twitter 内容搜索的独特入口**）
- [references/extraction.md](references/extraction.md) — 通用提取技术（分块、引用链接、保存）
- [references/prompt-guide.md](references/prompt-guide.md) — 研究 prompt 构造建议

---

## Part 1: 理解需求

目标：搞清楚用户要什么，然后开始。

### 先判断：用户的需求清楚吗？

收到用户 query 后，先判断你是否能理解研究的**对象、范围、目的**：

- **清楚** → 直接向用户确认你的理解（如需微调范围），然后开始
- **大致清楚但有细节模糊** → 先 WebSearch 搜 2-3 次补充认知，再和用户确认
- **不清楚** → 先 WebSearch 建立领域认知，再带着具体问题向用户澄清

澄清不是走流程——如果用户的意图一目了然，直接干活比问一堆问题有用。

### 构造查询

为选定的 AI 模式各准备一条查询。不同 AI 给不同角度比给同一个 prompt 更有效。见 [prompt-guide.md](references/prompt-guide.md)。

### 创建研究目录

在合适位置创建研究目录（如 `research-主题/`），创建 todo.md 记录状态。

---

## Part 2: 迭代探索

目标：多路并发搜索，逐步深入，直到信息充分。

### 深度由进展决定

**不要预设研究深度，让研究过程自己说话：**

- **起步**：先用快速模式铺开（Gemini Pro、ChatGPT Thinking、Claude Opus、Grok 专家），快速建立基线认知
- **发现复杂度**：如果快速模式的结果显示话题确实多维、有矛盾、需要更多来源 → 追加 Deep Research / DeepSearch
- **收敛**：如果快速模式已经给出了一致的、充分的答案 → 不需要开 DR，直接整合

简单问题不要大炮打蚊子。复杂问题不要浅尝辄止。让信息本身告诉你该挖多深。

### 派发

每个 AI 服务的具体操作步骤见各自 reference 文件。通用流程：
1. 新开 Tab → 导航到服务 → **检查登录**
2. 选择模式 → 输入查询
3. 记录到 todo.md（Tab 编号 + 查询内容）
4. **发完一个立刻切下一个，不等结果**

**登录处理**：这些服务使用的是用户的账号。如果发现某个服务未登录，**立即暂停并告知用户**，让用户选择：
- 去 Playwright 浏览器中登录该服务，然后继续
- 跳过该服务，用其他已登录的服务继续

不要自动跳过——用户可能想登录。

### 轮询与提取

**先到先提取，不等所有流完成。**

- 快速模式：~30s 后开始检查
- DR/DeepSearch 模式：~90s 后开始检查
- 用 screenshot 判断是否完成（比 snapshot 可靠）——各服务完成标志见 reference

提取技术见 [extraction.md](references/extraction.md)。每份结果保存为独立 md（`01-gemini-pro.md`、`02-chatgpt-thinking.md`...）。

### 定向深入

**每提取一份结果，立即评估：**
- 发现了哪些子问题？
- 哪些维度数据不够或有矛盾？
- 有没有意外发现值得追查？

如果有 → 追加查询。选择最合适的工具：
- **快速模式** — 定向查证具体子问题（秒级）
- **WebSearch/WebFetch** — 交叉验证事实（比开新 AI Tab 更快）
- **DR/DeepSearch** — 仅用于发现的子问题确实需要广度覆盖时
- **Grok** — 特别适合查看某话题在 X/Twitter 上的讨论和观点

### Tab 管理

- 控制在 ≤8 个活跃 Tab，多了浏览器会不稳定
- 提取完的 Tab 可以保留（可能需要追问），但不要无限堆积
- 浏览器断连时：`browser_close` → `pkill -f "mcp-chrome"` → `sleep 2` → 重新 navigate

### 何时停止

- 核心问题有了交叉验证的答案
- 新搜索不再产出实质性新信息
- 用户要求的范围已充分覆盖

---

## Part 3: 整合报告

目标：按主题维度重组内容，交叉验证，输出一份深度报告。

### 原则

- **按主题组织**，不按来源罗列（不要 "Gemini 说... ChatGPT 说..."）
- **标注来源**（`[Gemini DR]`、`[Grok]`、`[ChatGPT Thinking]` 等），让读者知道可信度
- **共识**（多路一致）和**分歧**（各执一词）都要标注
- **保留引用 URL** — 原始网络来源链接是高价值信息，必须传递到最终报告
- **分歧不强行裁决** — 保留并标注，让用户判断
- 信息权重：DR 通常更全面，快速模式更聚焦，WebSearch 最即时，Grok 的 X/Twitter 链接是独家信息

### 引用体系

报告有两层引用，都要做好：

**1. 网络来源引用**（报告 → 原始网页）

正文中关键事实、数据、观点旁标注原始网络来源。格式灵活——脚注、行内链接、段落末尾引用块都行，根据报告风格选择最可读的方式。核心原则：**读者看到一个关键论断，能直接找到原始网页验证**。

各 AI 的引用链接已在原始结果文件的 `## 参考链接` 章节。整合时从那里挑选最相关的链接嵌入报告正文。不需要全部搬过来——只保留支撑关键论点的。

**2. AI 来源标注**（报告 → 哪个 AI 说的）

用行内标签 `[Gemini DR]`、`[Grok]`、`[ChatGPT Thinking]` 等标注信息来自哪个 AI 模式。这帮助读者判断可信度（DR 多源交叉 vs 快速模式单次推理）。多路一致的可以标 `[多路共识]`。

**3. 原始结果索引**（报告 → 原始文件）

报告末尾附 `## 原始结果索引`，列出所有原始结果文件和对应的查询内容：

```
## 原始结果索引
| 文件 | 服务 | 模式 | 查询摘要 |
|------|------|------|----------|
| 01-gemini-pro.md | Gemini | Pro | ... |
| 02-chatgpt-dr.md | ChatGPT | Deep Research | ... |
```

这让读者能回溯到完整的原始结果（含全部参考链接）。

### 流程

1. **写初稿** — 基于已有结果先写能写的，同步嵌入引用链接
2. **标记缺口** — 哪些数据不够？哪些只有单一来源？
3. **缺口重大 → 回到 Part 2** 补充
4. **逐步更新** — 新信息到手就更新报告
5. **最终审校** — 检查引用完整性（关键论断有没有来源支撑？）→ 交付用户

报告保存为 `00-final-report.md`。

---

## todo.md 持久化

研究可能跨会话。todo.md 是恢复点。

```markdown
# 研究：[主题]
## 状态：[进行中/已完成]

## 搜索流
| # | 服务 | 模式 | Tab | 查询摘要 | 状态 |
|---|------|------|-----|----------|------|
| 01 | Gemini | Pro | 2 | ... | 已提取 |
| 02 | ChatGPT | DR | 3 | ... | 等待中 |
| 03 | Grok | 专家 | 4 | ... | 进行中 |

## 发现的子问题
- [ ] ...

## 整合进度
- [ ] 初稿
- [ ] 缺口填补
- [ ] 最终审校
```

**跨会话恢复**：读 todo.md → `browser_tabs` list 检查现有 Tab → 对照恢复。

---

## 错误处理

| 情况 | 建议 |
|------|------|
| 未登录 | **暂停，告知用户**——让用户选择登录还是跳过该服务 |
| 浏览器断连 | `browser_close` → `pkill -f "mcp-chrome"` → sleep 2 → 重新 navigate |
| Cloudflare 拦截 | 重试 1-2 次 navigate，通常第二次就通过 |
| 单 Tab 超时（>40min） | 标记超时，继续其他流 |
| 提取返回空 | 见 [extraction.md](references/extraction.md) 的降级策略 |
| snapshot 返回空 | 等 2-3 秒重试，ChatGPT/Grok 有时会进入瞬时空状态 |
| DR 未启动 | ChatGPT DR 可能先回澄清问题，检测后回复让它直接开始 |
| DR/DeepSearch 配额用尽 | 跳过，改用快速模式或 WebSearch 补充 |

**部分失败不影响产出**：≥2 路成功仍出报告（注明来源范围）。
