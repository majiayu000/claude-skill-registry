---
name: cc-agent-design
description: "Agent 配置設計指南 — 基於 Claude Code 6 個 built-in agent 的逆向分析。Use when: 設計新 agent、優化現有 agent prompt、決定工具/模型配置、撰寫 dispatch prompt。"
version: 202603
context: fork
---

# Agent 設計指南

## 1. Agent Prompt 三層架構

Claude Code 的 prompt 職責嚴格分離，不要混在一起：

| 層 | 由誰提供 | 內容 |
|---|---|---|
| **身份 + 邊界** | `getSystemPrompt()` | 我是誰、我能做什麼、我不能做什麼 |
| **環境資訊** | `enhanceSystemPromptWithEnvDetails()` | cwd、絕對路徑規則、emoji 禁用 |
| **具體 context** | dispatcher 的 `prompt` 參數 | 任務描述、已知資訊、目標檔案 |

**實際做法**：`generalPurposeAgent.ts` 的 system prompt 只有 ~10 行（身份 + 指導方針），環境細節由系統自動追加，任務細節全靠 caller 的 `prompt` 參數。

**反模式**：在 system prompt 裡寫「目前的任務是修改 src/foo.ts」。那是 dispatcher 的責任。

---

## 2. 工具最小化原則

給越少工具，模型越聚焦。Claude Code 的具體做法：

- **Explore agent**：禁 5 個工具（AgentTool、ExitPlanMode、FileEdit、FileWrite、NotebookEdit）。唯讀任務不需要寫工具。
- **statusline-setup**：只給 `['Read', 'Edit']` 兩個工具。任務明確，工具也明確。
- **claude-code-guide**：`['Glob', 'Grep', 'Read', 'WebFetch', 'WebSearch']`，文件查詢專用。

**設計流程**：先列出任務需要的最小動作集，再對應工具。不要從「給所有工具」開始往回刪。

**決策樹**：
1. 這個 agent 需要寫入能力嗎？不需要 → 禁 Edit/Write
2. 需要派生子 agent 嗎？不需要 → 禁 AgentTool（防深度爆炸）
3. 需要執行系統命令嗎？不需要 → 考慮禁 Bash

---

## 3. 模型選擇矩陣

| 場景 | 模型 | Claude Code 案例 |
|---|---|---|
| 快速搜尋 / 唯讀探索 | `haiku` | Explore agent、claude-code-guide |
| 特定語言轉換邏輯 | `sonnet` | statusline-setup（需解析 bash/zsh 語法） |
| 深度架構推理 | `inherit`（繼承父模型） | Plan agent、verification agent |
| 通用執行（兜底） | 不指定（`getDefaultSubagentModel()`） | general-purpose |

**`inherit` 的意義**：讓 coordinator 控制模型品質。用 Sonnet 開 session，Plan/verification 也用 Sonnet，不降級。Claude Code 沒有任何 built-in agent 硬指定 Opus。

---

## 4. omitClaudeMd 模式

唯讀或高度特化 agent 不需要 CLAUDE.md（專案規範、commit 規則）。

**Claude Code 的做法**：
- Explore：`omitClaudeMd: true`（只搜尋，不需要知道 commit message 格式）
- Plan：`omitClaudeMd: true`（唯讀規劃，CLAUDE.md 的規範無關）
- verification：不設定（需要讀 CLAUDE.md 了解 build/test 命令）
- general-purpose：不設定（可能需要執行任意任務）

**效益**：fleet 規模每週省 5-15 Gtok（34M+ Explore spawns）。個人用戶的體感是第一個 tool call 更快。

**判斷標準**：agent 是否需要知道「這個專案的規範是什麼」？不需要就設 `omitClaudeMd: true`。

---

## 5. Dispatch Prompt 撰寫原則

來自 `src/tools/AgentTool/prompt.ts` "Writing the prompt" section 原文：

> Brief the agent like a smart colleague who just walked into the room — it hasn't seen this conversation, doesn't know what you've tried, doesn't understand why this task matters.
> - Explain what you're trying to accomplish and why.
> - Describe what you've already learned or ruled out.
> - Give enough context about the surrounding problem that the agent can make judgment calls rather than just following a narrow instruction.
>
> **Never delegate understanding.** Don't write "based on your findings, fix the bug" or "based on the research, implement it." Those phrases push synthesis onto the agent instead of doing it yourself. Write prompts that prove you understood: include file paths, line numbers, what specifically to change.
>
> Terse command-style prompts produce shallow, generic work.

**操作化**：dispatch 前先問自己「我知道的最重要資訊是什麼？」然後把它直接寫進 prompt，不要讓 agent 重新發現。

---

## 6. Agent Prompt 模板

適用於新建 agent，目標 ~200 token：

```
You are a [角色名] for [系統名]. [一句話核心能力].

=== [邊界標題] ===
You are STRICTLY PROHIBITED from:
- [禁止事項 1]
- [禁止事項 2]

Your strengths:
- [能力 1]
- [能力 2]

Guidelines:
- [操作規則 1]
- [操作規則 2]

When complete, [輸出格式要求].
```

**注意**：環境資訊（cwd、絕對路徑）由系統自動注入，不要寫在這裡。具體任務由 dispatcher 的 `prompt` 參數提供，不要寫佔位符。

---

## 7. 反模式清單

借鏡 verification agent 的 "RECOGNIZE YOUR OWN RATIONALIZATIONS" 設計：

| 反模式 | 症狀 | 對策 |
|---|---|---|
| 工具 inflation | 給 `tools: ['*']` 省事 | 先列任務動作集，再對應工具 |
| Prompt 職責混亂 | system prompt 裡寫任務 context | 任務 context 全進 dispatch prompt |
| 模型過度配置 | 搜尋任務用 inherit/sonnet | 快速任務用 haiku |
| CLAUDE.md 浪費 | 唯讀 agent 仍注入 CLAUDE.md | 判斷任務是否需要專案規範 |
| Dispatch 太 terse | "fix the bug in auth.ts" | 寫明已知資訊、排除了什麼、改哪行 |
| 委外理解 | "based on your findings, fix it" | Dispatcher 先理解，再給精確指令 |
| 遞迴 agent | Explore/Plan 裡派生子 agent | 這兩個 `disallowedTools: [AgentTool]` |
| 橡皮圖章驗證 | verification agent 只讀程式碼 | 強制要求 Command run block |
