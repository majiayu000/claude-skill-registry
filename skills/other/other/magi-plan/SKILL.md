---
name: magi-plan
description: "三機(Claude/Gemini/Codex)平行審查計畫，評估完整性、順序、風險後投票共識"
---

# MAGI Plan 快捷指令

> `/magi-plan [task]` - 工作計畫制定

此指令為 `/magi plan [task]` 的快捷方式。

## 使用方式

```
/magi-plan 重構用戶認證流程
```

## 執行內容

自動啟動 MAGI 三機平行分析：

| 機體 | 引擎 | 分析重點 |
|------|------|----------|
| MELCHIOR-1 | Claude Opus | 計畫完整性、技術路線圖 |
| BALTHASAR-2 | Gemini | 步驟細緻度、依賴順序正確性 |
| CASPER-3 | Codex/GPT | 安全實施順序、風險緩解措施 |

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

## 模型設定（plan 任務）

| 機體 | 模型 | 參數 |
|------|------|------|
| MELCHIOR-1 | `opus` | - |
| BALTHASAR-2 | `gemini-3-pro-preview` | - |
| CASPER-3 | `gpt-5.2-codex` | `reasoningEffort: "high"` |

---

請參考 `/magi-system` 了解完整的投票機制與共識報告格式。
