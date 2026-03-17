---
name: ai-output-validation
version: 1.0
description: |
  Ensures all AI-generated output fields have proper validation.
  Auto-activates on "AI 輸出", "LLM", "Gemini", "GPT", "truncate", "截斷" keywords.
  Lesson learned: 2026-01-08 Quick Feedback, Report, Deep Analyze truncation bugs.
allowed-tools: [Read, Grep, Bash]
trigger_keywords:
  - AI 輸出
  - LLM
  - Gemini
  - GPT
  - truncate
  - 截斷
  - max_tokens
  - 字數限制
  - 輸出驗證
auto_activate: true
priority: high
---

# AI Output Validation - AI 輸出驗證

**Purpose**: 確保所有 AI 生成的欄位都有完整的驗證機制

**Lesson Learned**: 2026-01-08 三個截斷 Bug
- Quick Feedback: `max_tokens=50` 太小，回傳 1-3 字
- Report: 硬截斷 `[:15]` 切斷句子中間
- Deep Analyze: 缺少 display_text/quick_suggestion 驗證

---

## 核心原則

### ❌ 錯誤做法
```python
# 硬截斷 - 會切斷句子
result["text"] = ai_response[:15]

# max_tokens 太小 - AI 會截斷
response = await llm.generate(max_tokens=50)  # 中文需要更多 tokens

# 沒有驗證 - 不知道是否完整
return {"message": ai_response}
```

### ✅ 正確做法
```python
# 1. 定義限制（基於 prompt 或資料範圍）
MAX_CHARS = 15
MIN_CHARS = 7

# 2. 用 prompt 控制長度（讓 AI 自己處理）
prompt = "請用 15 字以內回應..."

# 3. 加大 max_tokens（避免 AI 被迫截斷）
response = await llm.generate(max_tokens=500)

# 4. 驗證並 fallback
if len(text) < MIN_CHARS:
    logger.warning(f"Too short: {text}")
    text = FALLBACK_MESSAGE

# 5. Log warning（不要硬截斷）
if len(text) > MAX_CHARS:
    logger.warning(f"Over limit: {len(text)} chars")
```

---

## 檢查清單

### 每個 AI 生成欄位必須檢查：

```
□ 1. 定義 min_chars - 太短時 fallback
     根據欄位用途決定最小字數
     例：鼓勵文 7 字、建議 5 字

□ 2. 定義 max_chars - 超過時 log warning
     根據 prompt 要求或 UI 限制
     例：同心圓 15 字、display 20 字

□ 3. max_tokens 足夠大 - 避免 AI 被迫截斷
     中文建議 500+（每字約 1-3 tokens）
     檢查 finish_reason != MAX_TOKENS

□ 4. 有 fallback 機制 - 太短或失敗時使用
     預設訊息列表
     random.choice(FALLBACK_MESSAGES)

□ 5. Log warning - 方便監控
     記錄實際長度
     記錄被 fallback 的情況

□ 6. 本地測試 3+ 次 - 確認 AI 實際輸出
     不要只看一次結果
     觀察變異性
```

---

## 驗證範本

```python
# 標準 AI 輸出驗證模式
def validate_ai_output(
    text: str,
    min_chars: int,
    max_chars: int,
    fallback: str,
    field_name: str = "output"
) -> str:
    """驗證 AI 輸出，太短用 fallback，太長 log warning"""

    if len(text) < min_chars:
        logger.warning(
            f"{field_name} too short ({len(text)} chars): '{text}', "
            f"using fallback"
        )
        return fallback

    if len(text) > max_chars:
        logger.warning(
            f"{field_name} over {max_chars} chars: "
            f"{len(text)} chars - '{text[:30]}...'"
        )
        # 不要硬截斷！只 log warning

    return text
```

---

## 專案 AI 欄位參考表

| API | 欄位 | Min | Max | 來源 |
|-----|------|-----|-----|------|
| Quick Feedback | message | 7 | 15 | prompt 要求 |
| Deep Analyze | display_text | 4 | 20 | prompt 要求 |
| Deep Analyze | quick_suggestion | 5 | 20 | 200句: 5-17 字 |
| Report | encouragement | - | 15 | prompt 要求 |
| Report | issue | - | - | 無限制 |
| Report | analyze | - | - | 無限制 |
| Report | suggestion | - | - | 無限制 |

---

## 診斷指令

```bash
# 找出所有 AI 呼叫點
grep -rn "generate_text\|chat_completion\|_call_gemini" app/services/

# 找出所有 max_tokens 設定
grep -rn "max_tokens" app/services/

# 找出潛在的硬截斷
grep -rn "\[:.*\]" app/services/ | grep -v ".pyc"

# 檢查是否有 min/max 驗證
grep -rn "min_chars\|max_chars\|MIN_\|MAX_" app/services/
```

---

## IMPORTANT

- **不要硬截斷** - 會切斷句子中間
- **用 prompt 控制長度** - 讓 AI 自己處理
- **加大 max_tokens** - 避免 finish_reason=MAX_TOKENS
- **本地測試 3+ 次** - 觀察 AI 輸出變異
- **Log warning** - 方便監控異常

---

**Version**: 1.0
**Created**: 2026-01-08
**Lesson From**: Quick Feedback, Report, Deep Analyze truncation bugs
