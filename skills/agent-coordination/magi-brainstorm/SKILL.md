---
name: magi-brainstorm
description: "三機(Claude/Gemini/Codex)平行分析創意，評估可行性、維護性、安全風險後投票共識"
---

# MAGI Brainstorm 快捷指令

> `/magi-brainstorm [idea]` - 創意發想與可行性分析

此指令為 `/magi brainstorm [idea]` 的快捷方式。

## 使用方式

```
/magi-brainstorm 實現即時通知系統的最佳方式
```

## 執行內容

自動啟動 MAGI 三機平行分析：

| 機體 | 引擎 | 分析重點 |
|------|------|----------|
| MELCHIOR-1 | Claude Opus | 創新可行性、技術選型 |
| BALTHASAR-2 | Gemini | 實作可維護性、團隊匹配度 |
| CASPER-3 | Codex/GPT | 安全風險、合規性要求 |

---

## 🚨 強制執行規則

<MANDATORY>
執行此指令時，必須嚴格遵守以下規則：

**禁止事項：**
- ❌ 禁止委派給其他 agent 處理
- ❌ 禁止使用非指定的工具

**必須使用：**
- ✅ MELCHIOR-1: `Task` tool with `subagent_type="general-purpose"`, `model="opus"`
- ✅ BALTHASAR-2: `mcp__gemini__ask-gemini` (先用 ToolSearch 載入)
- ✅ CASPER-3: `mcp__codex-cli__ask-codex` (先用 ToolSearch 載入)

**執行步驟：**
1. 先調用 `ToolSearch` 載入 `mcp__gemini__ask-gemini` 和 `mcp__codex-cli__ask-codex`
2. 在**單一訊息**中同時發出三個 tool calls（Task + Gemini + Codex）
3. 等待三機回應後彙整共識報告
</MANDATORY>

---

## 模型設定（brainstorm 任務）

| 機體 | 模型 | 參數 |
|------|------|------|
| MELCHIOR-1 | `opus` | - |
| BALTHASAR-2 | `gemini-3-pro-preview` | - |
| CASPER-3 | `gpt-5.2` | `reasoningEffort: "high"` |

---

請參考 `/magi-system` 了解完整的投票機制與共識報告格式。
