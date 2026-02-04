---
name: codex-plugin-dev-start
description: Use when the user mentions plugin-dev, wants a plugin-dev-like toolkit inside Codex CLI, asks how to start creating skills/agents/MCP/commands/hooks, or wants a guided menu to choose the right Codex skill.
---

# Codex Plugin-Dev（Start）

## 目標
在 Codex CLI 內提供「像 plugin-dev 一樣」的起手式：先釐清要做的是哪一類（skill / agent / MCP / commands / hooks / validation / publish），再切到最適合的 skill。

## 你要做的事（流程）
1) 先用 1～3 個問題把需求分類（優先用下列選單）。  
2) 根據分類，切到對應的 `codex-plugin-dev-*` skill。  
3) 若使用者其實只是在寫 MCP server，優先用現成 `mcp-builder`；若是在寫 Codex skill，優先用 `codex-plugin-dev-create-skill`。

## 分類選單（問使用者選 1 個）
A) 我要建立/修改 **Codex skill（SKILL.md）**，並靠 description 觸發  
B) 我要做「像 agent」的流程（多步驟/分工/子任務），但在 Codex CLI 內  
C) 我要建立/整合 **MCP server**（工具化外部 API / 本地服務）  
D) 我要做可重用的 **commands/腳本**（一鍵跑測試、啟動、格式化等）  
E) 我要做 **hooks/automation**（pre-commit、commit-msg、CI helper）  
F) 我懷疑 skill 沒觸發／想做 **validation**（frontmatter/description/結構）  
G) 我想 **分享/安裝/搬移** skills（跨機器、給團隊用）

## 快速對應（內部路由規則）
- A → `codex-plugin-dev-create-skill`
- B → `codex-plugin-dev-create-agent`
- C → `codex-plugin-dev-create-mcp`
- D → `codex-plugin-dev-create-command`
- E → `codex-plugin-dev-create-hook`
- F → `codex-plugin-dev-validate`
- G → `codex-plugin-dev-publish`

