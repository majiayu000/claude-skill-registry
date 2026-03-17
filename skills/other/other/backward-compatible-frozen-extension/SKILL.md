---
name: backward-compatible-frozen-extension
description: "Use when extending a frozen dataclass or Pydantic pipeline with new fields without breaking existing consumers."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Backward-Compatible Frozen Dataclass Extension
# frozen dataclass/Pydantic パイプラインの後方互換拡張

**Extracted / 抽出日:** 2026-02-09
**Context / コンテキスト:** When extending an existing Python pipeline that uses frozen (immutable) dataclasses or Pydantic models, without breaking existing consumers.
既存の frozen（イミュータブル）dataclass / Pydantic モデルを使った Python パイプラインを、既存コンシューマーを壊さずに拡張する場合。

---

## Problem / 課題

You have a working pipeline with frozen dataclasses flowing between stages:

```
Extraction → Processing → Quality → Output
```

You need to add richer data (e.g., section metadata) to the pipeline, but:
- Existing consumers rely on the current fields
- `frozen=True` prevents mutation after creation
- Tests and CLI already depend on the current interface
- You can't break the existing code path for simple inputs

動作中のパイプラインに豊富なデータ（例：セクションメタデータ）を追加したいが、既存コンシューマーが現在のフィールドに依存しており、テストやCLIが現在のインターフェースに依存している。

---

## Solution / 解決策

### 4 Techniques Combined / 4つの手法を組み合わせ

### 1. Optional Field with Default / デフォルト値付きオプショナルフィールド

Add new fields with default values to frozen dataclasses. All existing constructors continue to work.

```python
# BEFORE
@dataclass(frozen=True, slots=True)
class ExtractedDocument:
    source_path: str
    text: str
    chunks: tuple[str, ...]
    file_type: str

# AFTER — backward compatible, no existing code breaks
@dataclass(frozen=True, slots=True)
class ExtractedDocument:
    source_path: str
    text: str
    chunks: tuple[str, ...]          # kept for old consumers
    file_type: str
    sections: tuple[Section, ...] = ()  # NEW: empty = no sections
```

For Pydantic `frozen=True` models, the same applies:

```python
class AppConfig(BaseModel, frozen=True):
    model: str = "claude-sonnet-4-5-20250929"
    # ... existing fields ...
    batch_enabled: bool = False        # NEW: defaults preserve compat
    batch_poll_interval: float = 30.0  # NEW
```

### 2. Parallel Functions (Don't Modify) / 並列関数（既存を変更しない）

Create new functions alongside existing ones instead of modifying them.

```python
# EXISTING — untouched, all tests still pass
def build_user_prompt(text: str, *, max_cards: int = 50, ...) -> str:
    ...

# NEW — only called when sections are available
def build_section_prompt(
    section: Section,
    *,
    document_title: str = "",
    max_cards: int = 20,  # smaller default for sections
    ...
) -> str:
    ...
```

### 3. Branch in Orchestrator / オーケストレーターで分岐

The orchestrator checks for new data availability and branches:

```python
def extract_cards(
    text: str,
    *,
    chunks: list[str] | None = None,
    sections: list[Section] | None = None,  # NEW optional param
    ...
) -> tuple[ExtractionResult, CostTracker]:

    if sections:
        # NEW path: section-aware processing
        for section in sections:
            prompt = build_section_prompt(section, ...)
            ...
    else:
        # OLD path: chunk-based processing (unchanged)
        for chunk in text_chunks:
            prompt = build_user_prompt(chunk, ...)
            ...
```

### 4. Populate Both Old and New Fields / 新旧両フィールドを設定

When constructing the data, populate both the old field (for backward compat) and the new field (for new consumers):

```python
sections = split_by_headings(markdown_text)

return ExtractedDocument(
    source_path=str(file_path),
    text=full_text,
    chunks=tuple(s.text for s in sections),  # OLD: still works
    file_type="pdf",
    sections=tuple(sections),                 # NEW: richer data
)
```

---

## Example: Full Pipeline Extension / 完全なパイプライン拡張例

```python
# main.py — orchestrator decides which path to take
def _process_file(*, file_path, config, ...):
    doc = extract_text(file_path, ...)

    if doc.sections:
        # New path: section-aware with per-section model routing
        result, tracker = extract_cards(
            doc.text,
            sections=list(doc.sections),
            ...
        )
    else:
        # Old path: paragraph-boundary chunks
        result, tracker = extract_cards(
            doc.text,
            chunks=list(doc.chunks) if len(doc.chunks) > 1 else None,
            ...
        )

    # Quality pipeline works on both paths — receives merged card list
    cards, report, tracker = run_quality_pipeline(cards=list(result.cards), ...)
```

---

## Key Principles / 重要な原則

| Principle | Description |
|-----------|-------------|
| **Add, don't modify** | New fields have defaults; new functions coexist with old |
| **Old path untouched** | Existing code path runs identically for simple inputs |
| **Opt-in enrichment** | New data is available only when the producer provides it |
| **Single merge point** | Downstream stages (quality, output) work on the same types |
| **Test isolation** | Old tests pass without changes; new tests cover new paths |

---

## When to Use / 使用すべき場面

- Adding metadata/context to an existing frozen data pipeline
- Extending a CLI tool with new features while keeping old behavior
- Introducing a new processing mode (batch, async, section-aware) alongside existing mode
- Any Python project using `@dataclass(frozen=True)` or `BaseModel(frozen=True)` that needs non-breaking evolution

---

## Anti-Patterns to Avoid / 避けるべきアンチパターン

```python
# WRONG: Modifying existing function signature in breaking way
def build_user_prompt(section: Section, ...)  # was: (text: str, ...)

# WRONG: Removing old field
@dataclass(frozen=True)
class ExtractedDocument:
    sections: tuple[Section, ...]  # removed chunks — breaks consumers

# WRONG: Making new field required
class ExtractedDocument:
    sections: tuple[Section, ...]  # no default — all constructors break

# WRONG: Mutating frozen instance
doc.sections = new_sections  # FrozenInstanceError
```
