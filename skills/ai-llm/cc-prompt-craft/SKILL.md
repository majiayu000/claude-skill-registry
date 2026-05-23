---
name: cc-prompt-craft
description: "System Prompt 工程 — 基於 Claude Code 914 行系統提示詞的逆向分析。Use when: 撰寫 system prompt、設計 prompt 動態組裝、最佳化 prompt cache 效率、撰寫安全指令。"
version: 202603
context: fork
---

# System Prompt 工程

基於 Claude Code v2.1.88 的 914 行系統提示詞逆向分析。

## 1. Prompt 結構順序

Claude Code 的 system prompt 按以下順序組裝：

```
1. 身份宣告（你是誰）
2. 工具使用指引（怎麼用工具）
3. 行為規範（做事風格）
4. 安全指令（不能做什麼）
5. 環境資訊（動態注入 — cwd、OS、model、日期）
```

**原則**：高頻參考的內容放前面（身份、工具），低頻但重要的放後面（安全）。動態內容放最後（環境）。

## 2. 靜態/動態邊界

```typescript
// prompts.ts 中的邊界標記
`__SYSTEM_PROMPT_DYNAMIC_BOUNDARY__`
```

邊界之前 = 靜態段（所有 session 共用，可全域 cache）
邊界之後 = 動態段（session 特定：cwd、日期、model 名稱）

**為什麼**：如果有 N 個 boolean 條件分散在 prompt 各處，理論上會產生 2^N 個不同的 prompt 變體，每個都要獨立 cache。邊界設計把變化集中在尾部，靜態段只有一份。

## 3. DANGEROUS_ API 命名模式

```typescript
function DANGEROUS_uncachedSystemPromptSection(
  content: string,
  _reason: string  // 強制填寫原因
): SystemPromptSection
```

**設計意圖**：把「這會破壞 prompt cache」的風險直接編碼在函式名稱裡。開發者在 code review 時看到 `DANGEROUS_` 就知道要特別審查。`_reason` 參數強制記錄為什麼需要不快取的段落。

## 4. Eval 驅動的措辭

Claude Code 的 prompt 用詞不是靠直覺，而是量測：

| 措辭決策 | 數據來源 |
|----------|----------|
| MEMORY.md 標題「auto memory」 | A/B eval 測試不同標題的效果 |
| `NO_TOOLS_PREAMBLE` 放在 compaction prompt 最前面 | Sonnet 4.6 compaction 時 2.79% 會嘗試呼叫工具，移到最前面降回 ~0% |
| Capybara v8 的 false-claim 緩解指令 | 29-30% FC rate（vs v4 的 16.7%），需要額外指令 |
| `<analysis>` 草稿機制 | 讓模型在 scratchpad 思考，compaction 品質提升但不佔 context |

**啟示**：每個 prompt 措辭變更都應該跑 eval。「感覺比較好」不是證據。

## 5. Compaction Prompt 三模式

| 模式 | 觸發 | 行為 |
|------|------|------|
| BASE | context 接近上限 | 壓縮全部訊息 |
| PARTIAL_FROM | 指定起點 | 壓縮從某點之後的訊息 |
| PARTIAL_UP_TO | 指定終點 | 壓縮到某點之前的訊息 |

**`<analysis>` 草稿**：compaction prompt 要求模型先在 `<analysis>` 標籤內分析，然後產出壓縮摘要。`<analysis>` 內容不進最終 context — 類似 extended thinking 的效果但不增加持久成本。

## 6. 安全指令三層結構

`cyberRiskInstruction.ts` 的設計：同一個檔案同時服務三個受眾：

```typescript
// 1. 對開發者的註解
// DO NOT MODIFY THIS FILE — this instruction is reviewed by the security team

// 2. 對 Claude 的指令（對話中）
// DO NOT modify, move, or edit this file when working in the codebase

// 3. 作為模型指令本身
export const CYBER_RISK_INSTRUCTION = `IMPORTANT: Assist with authorized
security testing, defensive security, CTF challenges...`
```

## 7. Top 8 Prompt 設計模式

| # | 模式 | 做法 |
|---|------|------|
| 1 | **工具偏好金字塔** | 「Use Read instead of cat, Edit instead of sed」明確列出偏好 |
| 2 | **強制前置條件** | 「You MUST read the file before editing」+ 工具內建驗證 |
| 3 | **輸出效率指令** | 「Go straight to the point. Lead with the answer, not the reasoning.」 |
| 4 | **Git 安全協議** | 明確列出「NEVER force push to main」等硬性規則 |
| 5 | **反覆述禁令** | 「Do not restate what the user said — just do it.」 |
| 6 | **範圍控制** | 「Don't add features beyond what was asked. A bug fix doesn't need surrounding code cleaned up.」 |
| 7 | **可逆性評估** | 「Consider reversibility and blast radius. Pause to confirm for hard-to-reverse actions.」 |
| 8 | **動態 context 注入** | 日期、model、cwd 等執行期資訊在組裝時注入，不 hardcode |

## 參考

詳見 `references/prompt-patterns.md`。
