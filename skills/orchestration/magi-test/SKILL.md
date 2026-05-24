---
name: magi-test
description: "三機(Claude/Gemini/Codex)平行審查測試，評估覆蓋率、邊界條件、異常處理後投票共識"
---

# MAGI Test 快捷指令

> `/magi-test [feature]` - 測試覆蓋評估

此指令為 `/magi test [feature]` 的快捷方式。

## 使用方式

```
/magi-test 用戶登入功能
/magi-test src/services/payment.ts
```

## 執行內容

自動啟動 MAGI 三機平行分析：

| 機體 | 引擎 | 分析重點 |
|------|------|----------|
| MELCHIOR-1 | Claude Sonnet | 測試策略、覆蓋完整性 |
| BALTHASAR-2 | Gemini Flash | 測試品質、Mock 使用合理性、測試隔離性 |
| CASPER-3 | Codex/GPT | 安全測試覆蓋、負面測試、邊界條件 |

---

## 🚨 強制執行規則

<MANDATORY>
執行此指令時，必須嚴格遵守以下規則：

**禁止事項：**
- ❌ 禁止委派給其他 agent 處理
- ❌ 禁止使用非指定的工具

**必須使用：**
- ✅ MELCHIOR-1: `Task` tool with `subagent_type="general-purpose"`, `model="sonnet"`
- ✅ BALTHASAR-2: `mcp__gemini__ask-gemini` (先用 ToolSearch 載入)
- ✅ CASPER-3: `mcp__codex-cli__ask-codex` (先用 ToolSearch 載入)

**執行步驟：**
1. 先調用 `ToolSearch` 載入 `mcp__gemini__ask-gemini` 和 `mcp__codex-cli__ask-codex`
2. 在**單一訊息**中同時發出三個 tool calls（Task + Gemini + Codex）
3. 等待三機回應後彙整共識報告
</MANDATORY>

---

## 模型設定（test 任務）

| 機體 | 模型 | 參數 |
|------|------|------|
| MELCHIOR-1 | `sonnet` | - |
| BALTHASAR-2 | `gemini-3-flash-preview` | - |
| CASPER-3 | `gpt-5.2-codex` | `reasoningEffort: "medium"` |

---

請參考 `/magi-system` 了解完整的投票機制與共識報告格式。
