---
name: long-document-llm-pipeline
description: "Use when processing documents over 50K characters through LLM APIs with section splitting and batch cost reduction."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-08"
---

# Long Document LLM Processing Pipeline

**Extracted:** 2026-02-08 (updated 2026-02-09)
**Context:** When processing documents over ~50K characters through LLM APIs for extraction, generation, or analysis tasks.

## Problem

Sending large documents (>50K chars) as a single LLM prompt causes:
1. **Lost in the Middle** - LLMs lose attention on content in the middle of long inputs (30%+ accuracy drop, per Liu et al. 2023)
2. **High cost** - Entire document becomes input tokens even if only portions are relevant
3. **No partial retry** - If generation fails, must re-process the entire document
4. **No parallelism** - Single sequential API call

## Solution: 6-Step Pipeline

```
Document
  |
  v
[1] Text Extraction (pymupdf4llm, page_chunks=True)
  |
  v
[2] Structure Detection (Markdown headers, TOC, Japanese patterns)
  |
  v
[3] Section Splitting (5K-30K chars per section)
  |
  v
[4] Breadcrumb Context (prepend section path to each chunk)
  |
  v
[5] Batch API / Async Parallel (50% cost reduction with Batch)
  |
  v
[6] Merge + Deduplicate Results
```

---

## Step 1: Structured Extraction (pymupdf4llm)

Use `page_chunks=True` to get structured per-page data with metadata:

```python
import pymupdf4llm

# BAD: Flat string, loses structure
text = pymupdf4llm.to_markdown("input.pdf")

# GOOD: Structured per-page data with TOC and metadata
chunks = pymupdf4llm.to_markdown("input.pdf", page_chunks=True)
# Returns: list[dict] with keys:
#   - "metadata": {file_path, page_count, page_number, ...}
#   - "toc_items": [[level, title, page_number], ...]
#   - "text": "# Heading\n\nContent..."
#   - "tables": [...], "images": [...], "page_boxes": [...]
```

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page_chunks` | bool | Return list of page dicts instead of string |
| `hdr_info` | callable/None | Custom header detection. `None` = auto-detect by font size |
| `page_separators` | bool | Insert `--- end of page=n ---` markers |
| `margins` | float/seq | Page margins (exclude headers/footers) |

### Heading Detection

`hdr_info=None` auto-detects headings by font size via `IdentifyHeaders` and prefixes them with `#` markers. `toc_items` returns `[level, title, page_number]` from the PDF's built-in TOC.

---

## Steps 2-3: Heading-Stack Sectioning with Breadcrumb

Use a **dictionary-keyed heading stack** where keys are heading levels. When a new heading appears, clear all levels >= its own level, then set the new heading.

```python
heading_stack: dict[int, str] = {}

for heading_text, level in headings:
    # Clear deeper/same levels (new H1 clears H2, H3; new H2 clears H3)
    keys_to_remove = [k for k in heading_stack if k >= level]
    for k in keys_to_remove:
        del heading_stack[k]
    heading_stack[level] = heading_text

    # Build breadcrumb from remaining stack (sorted by level)
    stack_list = [document_title] if document_title else []
    for lvl in sorted(heading_stack.keys()):
        stack_list.append(heading_stack[lvl])
    breadcrumb = " > ".join(stack_list)
```

### Behavior

```
Input:                           heading_stack        breadcrumb
# 本論                           {1: "本論"}          "本論"
## 第1章                         {1: "本論", 2: "第1章"}  "本論 > 第1章"
### 第1節                        {1,2,3}              "本論 > 第1章 > 第1節"
## 第2章   ← clears H3           {1: "本論", 2: "第2章"}  "本論 > 第2章"
# 結論     ← clears H2, H3       {1: "結論"}          "結論"
```

### Fallback Chain

```
1. Markdown headings (#, ##, ###) → preferred
2. Japanese headings (第X章, 序論/本論/結論, 1. etc.) → fallback
3. Single preamble section (level=0) → last resort
```

### Oversized Section Sub-splitting

After heading-based splitting, any section exceeding `max_chars` gets sub-split at `\n\n` paragraph boundaries. Sub-sections inherit the parent's breadcrumb.

### Data Model

```python
@dataclass(frozen=True, slots=True)
class Section:
    id: str           # "section-0", "section-1-2"
    heading: str      # "第1章 概要"
    level: int        # 1=H1, 2=H2, 3=H3, 0=preamble
    breadcrumb: str   # "正理の海 > 本論 > 第1章"
    text: str         # Section body (including heading line)
    page_range: str   # "pp.3-18" or ""
    char_count: int   # len(text), precomputed
```

---

## Step 4: Breadcrumb Context in Prompts

Always prepend section hierarchy to LLM prompts:

```python
prompt = (
    f"Document: {title}\n"
    f"Section: {breadcrumb}\n"  # e.g., "Chapter 3 > Section 2"
    f"Pages: {page_range}\n\n"
    f"---\n\n{section_text}"
)
```

---

## Step 5: API Call Strategy

### Decision Matrix: When to Chunk

| Document Size | Approach | Rationale |
|--------------|----------|-----------|
| < 50K chars | Single prompt | Within attention sweet spot |
| 50K - 200K chars | Structure-aware chunking | Avoid Lost in the Middle |
| > 200K chars | Structure-aware + model routing | Cost optimization critical |

### Anthropic Batch API (50% Cost Reduction)

For non-real-time processing:

```python
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

requests = [
    Request(
        custom_id=f"section-{i}",
        params=MessageCreateParamsNonStreaming(
            model="claude-sonnet-4-5-20250929",
            max_tokens=8192,
            system=[{
                "type": "text",
                "text": SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }],
            messages=[{"role": "user", "content": section_prompt}],
        ),
    )
    for i, section_prompt in enumerate(section_prompts)
]
batch = client.messages.batches.create(requests=requests)
```

Key facts: 50% discount, max 100K requests/256MB per batch, prompt caching stacks with discount.

### Model Routing per Section

```python
def select_model(section_text: str) -> str:
    if len(section_text) < 5_000:
        return "claude-haiku-4-5-20251001"  # Simple/short
    return "claude-sonnet-4-5-20250929"     # Complex
```

---

## Cost Example

572K char Japanese document (20 sections):

| Approach | Estimated Cost |
|----------|---------------|
| Single chunk, Sonnet | ~$0.90 |
| Structured + Batch + Sonnet | ~$0.45 |
| Structured + Batch + mixed models | ~$0.35 |

## When to Use

- Processing PDFs/documents >50K characters through any LLM API
- Building document-to-X pipelines (flashcards, summaries, Q&A datasets)
- Japanese/multilingual documents with chapter/section structure
- Any task where hierarchical context improves LLM output quality

## References

- [Lost in the Middle (Liu et al. 2023)](https://arxiv.org/abs/2307.03172)
- [Claude Batch Processing API](https://platform.claude.com/docs/en/build-with-claude/batch-processing)
