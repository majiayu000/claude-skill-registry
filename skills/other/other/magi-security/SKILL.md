---
name: magi-security
description: "三機(Claude/Gemini/Codex)平行安全審查，掃描OWASP漏洞、威脅建模後投票(CASPER有VETO權)"
---

# MAGI Security 快捷指令

> `/magi-security [scope]` - 安全漏洞掃描

此指令為 `/magi security [scope]` 的快捷方式。

## 使用方式

```
/magi-security 支付流程模組
/magi-security src/api/
```

## 執行內容

自動啟動 MAGI 三機平行分析（深度安全模式）：

| 機體 | 引擎 | 分析重點 |
|------|------|----------|
| MELCHIOR-1 | Claude Opus | 安全架構評估、威脅面分析 |
| BALTHASAR-2 | Gemini Pro | 安全編碼實踐、輸入驗證完整性 |
| CASPER-3 | Codex/GPT (Max) | 完整威脅建模、滲透測試建議、CVE 掃描 |

## ⚠️ 特別注意

此任務類型下，**CASPER-3 的 VETO 權重更高**。任何 CRITICAL 或 HIGH 安全問題都會觸發深度審查。

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

## 模型設定（security 任務）

| 機體 | 模型 | 參數 |
|------|------|------|
| MELCHIOR-1 | `opus` | - |
| BALTHASAR-2 | `gemini-3-pro-preview` | - |
| CASPER-3 | `gpt-5.1-codex-max` | `reasoningEffort: "xhigh"` |

---

請參考 `/magi-system` 了解完整的投票機制與共識報告格式。
