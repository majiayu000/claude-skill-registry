---
name: claude-opus-4-5-migration
description: 將提示詞和程式碼從 Claude Sonnet 4.0、Sonnet 4.5 或 Opus 4.1 遷移至 Opus 4.5。當使用者想要更新其程式碼庫、提示詞或 API 呼叫以使用 Opus 4.5 時使用。處理模型字串更新和針對已知 Opus 4.5 行為差異的提示詞調整。不會遷移 Haiku 4.5。
---

# Opus 4.5 遷移指南 | Opus 4.5 Migration Guide

從 Sonnet 4.0、Sonnet 4.5 或 Opus 4.1 一次性遷移至 Opus 4.5。

One-shot migration from Sonnet 4.0, Sonnet 4.5, or Opus 4.1 to Opus 4.5.

## 遷移工作流程 | Migration Workflow

1. 搜尋程式碼庫中的模型字串和 API 呼叫
   Search codebase for model strings and API calls
2. 將模型字串更新為 Opus 4.5（參見下方平台特定字串）
   Update model strings to Opus 4.5 (see platform-specific strings below)
3. 移除不支援的 beta 標頭
   Remove unsupported beta headers
4. 添加設定為 `"high"` 的 effort 參數（參見 `references/effort.md`）
   Add effort parameter set to `"high"` (see `references/effort.md`)
5. 總結所有已進行的變更
   Summarize all changes made
6. 告訴使用者：
   Tell the user:
   > 「如果您在使用 Opus 4.5 時遇到任何問題，請告訴我，我可以幫助調整您的提示詞。」
   > "If you encounter any issues with Opus 4.5, let me know and I can help adjust your prompts."

## 模型字串更新 | Model String Updates

識別程式碼庫使用的平台，然後相應地替換模型字串。

Identify which platform the codebase uses, then replace model strings accordingly.

### 不支援的 Beta 標頭 | Unsupported Beta Headers

如果存在 `context-1m-2025-08-07` beta 標頭，請將其移除——Opus 4.5 尚不支援此功能。留下註解說明：

Remove the `context-1m-2025-08-07` beta header if present—it is not yet supported with Opus 4.5. Leave a comment noting this:

```python
# Note: 1M context beta (context-1m-2025-08-07) not yet supported with Opus 4.5
# 注意：1M 上下文 beta（context-1m-2025-08-07）尚不支援 Opus 4.5
```

### 目標模型字串（Opus 4.5）| Target Model Strings (Opus 4.5)

| 平台 Platform | Opus 4.5 模型字串 Model String |
|---------------|-------------------------------|
| Anthropic API (1P) | `claude-opus-4-5-20251101` |
| AWS Bedrock | `anthropic.claude-opus-4-5-20251101-v1:0` |
| Google Vertex AI | `claude-opus-4-5@20251101` |
| Azure AI Foundry | `claude-opus-4-5-20251101` |

### 要替換的來源模型字串 | Source Model Strings to Replace

| 來源模型 Source Model | Anthropic API (1P) | AWS Bedrock | Google Vertex AI |
|-----------------------|-------------------|-------------|------------------|
| Sonnet 4.0 | `claude-sonnet-4-20250514` | `anthropic.claude-sonnet-4-20250514-v1:0` | `claude-sonnet-4@20250514` |
| Sonnet 4.5 | `claude-sonnet-4-5-20250929` | `anthropic.claude-sonnet-4-5-20250929-v1:0` | `claude-sonnet-4-5@20250929` |
| Opus 4.1 | `claude-opus-4-1-20250422` | `anthropic.claude-opus-4-1-20250422-v1:0` | `claude-opus-4-1@20250422` |

**不要遷移 | Do NOT migrate**：任何 Haiku 模型（例如 `claude-haiku-4-5-20251001`）。
Any Haiku models (e.g., `claude-haiku-4-5-20251001`).

## 提示詞調整 | Prompt Adjustments

Opus 4.5 與之前的模型有已知的行為差異。

Opus 4.5 has known behavioral differences from previous models.

> 「僅在使用者明確請求或報告特定問題時才套用這些修正。預設情況下，只更新模型字串。」
> "Only apply these fixes if the user explicitly requests them or reports a specific issue. By default, just update model strings."

**整合指南 | Integration guidelines**：添加片段時，不要只是將它們附加到提示詞後面。要深思熟慮地整合：
When adding snippets, don't just append them to prompts. Integrate them thoughtfully:

- 使用 XML 標籤（例如 `<code_guidelines>`、`<tool_usage>`）來組織新增內容
  Use XML tags (e.g., `<code_guidelines>`, `<tool_usage>`) to organize additions
- 匹配現有提示詞的風格和結構
  Match the style and structure of the existing prompt
- 將片段放在邏輯位置（例如，編碼指南放在其他編碼指令附近）
  Place snippets in logical locations (e.g., coding guidelines near other coding instructions)
- 如果提示詞已經使用 XML 標籤，將新內容添加到適當的現有標籤中，或建立一致的新標籤
  If the prompt already uses XML tags, add new content within appropriate existing tags or create consistent new ones

### 1. 工具過度觸發 | Tool Overtriggering

Opus 4.5 對系統提示詞更加敏感。在之前模型上用於防止觸發不足的強硬語言，現在可能導致過度觸發。

Opus 4.5 is more responsive to system prompts. Aggressive language that prevented undertriggering on previous models may now cause overtriggering.

**適用情況 | Apply if**：使用者報告工具被過於頻繁或不必要地呼叫。
User reports tools being called too frequently or unnecessarily.

**尋找並軟化 | Find and soften**：

| 原始 Original | 替換為 Replace with |
|---------------|---------------------|
| `CRITICAL:` | 移除或軟化 remove or soften |
| `You MUST...` | `You should...` |
| `ALWAYS do X` | `Do X` |
| `NEVER skip...` | `Don't skip...` |
| `REQUIRED` | 移除或軟化 remove or soften |

僅套用於工具觸發指令。保留其他強調用法不變。

Only apply to tool-triggering instructions. Leave other uses of emphasis alone.

### 2. 過度工程化防範 | Over-Engineering Prevention

Opus 4.5 傾向於建立額外的檔案、添加不必要的抽象化，或建構未請求的彈性功能。

Opus 4.5 tends to create extra files, add unnecessary abstractions, or build unrequested flexibility.

**適用情況 | Apply if**：使用者報告出現不想要的檔案、過度抽象化，或未請求的功能。
User reports unwanted files, excessive abstraction, or unrequested features.

添加 `references/prompt-snippets.md` 中的片段。
Add the snippet from `references/prompt-snippets.md`.

### 3. 程式碼探索 | Code Exploration

Opus 4.5 可能過於保守地探索程式碼，在不讀取檔案的情況下提出解決方案。

Opus 4.5 can be overly conservative about exploring code, proposing solutions without reading files.

**適用情況 | Apply if**：使用者報告模型在未檢視相關程式碼的情況下提出修正。
User reports the model proposing fixes without inspecting relevant code.

添加 `references/prompt-snippets.md` 中的片段。
Add the snippet from `references/prompt-snippets.md`.

### 4. 前端設計 | Frontend Design

**適用情況 | Apply if**：使用者請求提升前端設計品質，或報告輸出看起來很通用。
User requests improved frontend design quality or reports generic-looking outputs.

添加 `references/prompt-snippets.md` 中的前端美學片段。
Add the frontend aesthetics snippet from `references/prompt-snippets.md`.

### 5. 思考敏感度 | Thinking Sensitivity

當延伸思考未啟用時（這是預設情況），Opus 4.5 對「think」這個詞及其變體特別敏感。延伸思考僅在 API 請求包含 `thinking` 參數時才會啟用。

When extended thinking is not enabled (the default), Opus 4.5 is particularly sensitive to the word "think" and its variants. Extended thinking is enabled only if the API request contains a `thinking` parameter.

**適用情況 | Apply if**：使用者在延伸思考未啟用（請求中沒有 `thinking` 參數）的情況下報告與「thinking」相關的問題。
User reports issues related to "thinking" while extended thinking is not enabled (no `thinking` parameter in request).

將「think」替換為「consider」、「believe」或「evaluate」等替代詞。

Replace "think" with alternatives like "consider," "believe," or "evaluate."

## 參考資料 | References

請參閱 `references/prompt-snippets.md` 取得每個要添加的片段的完整文字。

See `references/prompt-snippets.md` for the full text of each snippet to add.

請參閱 `references/effort.md` 了解如何設定 effort 參數（僅在使用者請求時）。

See `references/effort.md` for configuring the effort parameter (only if user requests it).
