---
name: magi-arch
description: "三機(Claude/Gemini/Codex)平行審查架構，評估擴展性、模組化、安全性後投票共識"
---

# MAGI Architecture 快捷指令

> `/magi-arch [design]` - 架構設計評估

此指令為 `/magi arch [design]` 的快捷方式。

## 使用方式

```
/magi-arch 新的認證模組設計
```

## 執行內容

自動啟動 MAGI 三機平行分析：

| 機體 | 引擎 | 分析重點 |
|------|------|----------|
| MELCHIOR-1 | Claude Opus | 架構合理性、擴展性設計 |
| BALTHASAR-2 | Gemini | 模組化程度、介面設計清晰度 |
| CASPER-3 | Codex/GPT | 安全架構、信任邊界識別 |

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

## 模型設定（architecture 任務）

| 機體 | 模型 | 參數 |
|------|------|------|
| MELCHIOR-1 | `opus` | - |
| BALTHASAR-2 | `gemini-3-pro-preview` | - |
| CASPER-3 | `gpt-5.1-codex-max` | `reasoningEffort: "xhigh"` |

---

## Prompt 模板

### MELCHIOR-1 (Claude Opus)
```
[MAGI SYSTEM - MELCHIOR-1 架構分析]
角色：科學家（創新者）- 專注架構、可行性、技術深度

任務：{task_description}

請從以下角度分析：
1. 架構合理性與技術選型
2. 擴展性與未來維護
3. 一致性模型是否恰當
4. 失敗恢復機制

輸出格式：
## MELCHIOR-1 架構分析報告
### 評分（0-10）
### 優點
### 待改進項目（標註 HIGH/MEDIUM/LOW）
### 投票
VOTE: [APPROVE/REJECT/ABSTAIN]
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASON: [理由]
```

### BALTHASAR-2 (Gemini)
```
[MAGI SYSTEM - BALTHASAR-2 模組化分析]
角色：母親（守護者）- 專注品質、可維護性、最佳實踐

任務：{task_description}

請從以下角度分析：
1. 模組化程度與元件獨立性
2. 介面設計清晰度
3. 文件完整性
4. 日常操作便利性

輸出格式：
## BALTHASAR-2 模組化分析報告
### 評分（0-10）
### 優點
### 待改進項目（標註 HIGH/MEDIUM/LOW）
### 投票
VOTE: [APPROVE/REJECT/ABSTAIN]
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASON: [理由]
```

### CASPER-3 (Codex)
```
[MAGI SYSTEM - CASPER-3 安全分析]
角色：直覺（防護者）- 專注安全、風險、邊界條件

任務：{task_description}

請從以下角度分析：
1. 機密外洩風險
2. 信任邊界識別
3. 權限管理
4. 供應鏈安全

輸出格式：
## CASPER-3 安全審查報告
### 評分（0-10）
### 優點
### 安全風險（標註 CRITICAL/HIGH/MEDIUM/LOW）
### 投票
VOTE: [APPROVE/REJECT/ABSTAIN]
CONFIDENCE: [HIGH/MEDIUM/LOW]
REASON: [理由]
VETO: [YES/NO]
```

---

請參考 `/magi-system` 了解完整的投票機制與共識報告格式。
