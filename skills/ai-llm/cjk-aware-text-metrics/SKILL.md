---
name: cjk-aware-text-metrics
description: "CJK/Latin weighted token estimation for multilingual LLM pipelines. Use when processing Japanese/Chinese/Korean text with fixed chars-per-token constants."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---

# CJK-Aware Text Metrics

**Extracted:** 2026-02-11
**Context:** Multilingual LLM pipelines where token estimation affects cost, chunking, or rate limits

## Problem

Fixed chars-per-token constants (e.g., `CHARS_PER_TOKEN = 4`) assume Latin text.
Japanese/Chinese/Korean text uses ~2.5 chars/token, causing ~60% underestimation
in token counts, cost previews, and chunk sizing for CJK-heavy documents.

## Solution

1. **Detect CJK characters by Unicode range:**

```python
def _is_cjk(char: str) -> bool:
    cp = ord(char)
    return (
        0x4E00 <= cp <= 0x9FFF      # CJK Unified Ideographs
        or 0x3040 <= cp <= 0x309F   # Hiragana
        or 0x30A0 <= cp <= 0x30FF   # Katakana
        or 0x3400 <= cp <= 0x4DBF   # CJK Extension A
        or 0xF900 <= cp <= 0xFAFF   # CJK Compatibility
    )
```

2. **Weighted token estimation:**

```python
CJK_CHARS_PER_TOKEN = 2.5
LATIN_CHARS_PER_TOKEN = 4.0

def estimate_tokens(text: str) -> int:
    cjk_count = sum(1 for c in text if _is_cjk(c))
    other_count = len(text) - cjk_count
    return int(cjk_count / CJK_CHARS_PER_TOKEN + other_count / LATIN_CHARS_PER_TOKEN)
```

3. **Chunk splitting must use token-based accumulation** (not char-based):

```python
# BAD: char_limit = token_limit * FIXED_CONSTANT
# GOOD: accumulate estimated tokens per paragraph
current_tokens += estimate_tokens(para)
if current_tokens > token_limit:
    flush_chunk()
```

## When to Use

- Building LLM pipelines that process Japanese/Chinese/Korean text
- Implementing chunk splitting for multilingual documents
- Estimating API costs for non-English content
- Any text metric (token count, cost, rate limit) using a fixed chars-per-token constant
