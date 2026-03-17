---
name: python-module-to-package-refactor
description: "Use when splitting a Python module (>400 LOC) into a package. mock.patch target update rules and checklist."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-09"
---

# Python Module-to-Package Refactoring with Patch Target Updates

**Extracted:** 2026-02-09
**Context:** Splitting a monolithic Python module into a package while maintaining test compatibility

## Problem

When refactoring `module.py` (700+ LOC) into `module/` package with sub-modules, `unittest.mock.patch()` targets in tests break because they still point to the old flat module path. `__init__.py` re-exports fix regular imports but NOT `patch()` targets.

## Solution

### Rule: `patch()` must target where the name is LOOKED UP, not where it's defined or re-exported

Three cases to handle:

### 1. Function called directly within its own module

```python
# critique.py defines _call_critique_api() and critique_cards() calls it
# OLD: patch("pkg.quality._call_critique_api")
# NEW: patch("pkg.quality.critique._call_critique_api")
```

### 2. Function imported by another sub-module

```python
# pipeline.py does: from .critique import critique_cards
# To mock critique_cards inside run_quality_pipeline():
# OLD: patch("pkg.quality.critique_cards")
# NEW: patch("pkg.quality.pipeline.critique_cards")  # where it's looked up!
```

### 3. Third-party module references

```python
# critique.py does: import anthropic
# OLD: patch("pkg.quality.anthropic.Anthropic")
# NEW: patch("pkg.quality.critique.anthropic.Anthropic")
```

### Checklist for safe refactoring

1. Create package directory and sub-modules (bottom-up: leaf deps first)
2. Create `__init__.py` with re-exports (preserves `from pkg.module import X`)
3. **grep all test files** for `patch("pkg.module.` and update targets
4. Delete old `module.py`
5. Run full test suite (not just the module's tests - e2e tests often have patches too)

## Example

```
# Before: quality.py (706 LOC)
# After:
quality/
  __init__.py    (re-exports)
  heuristic.py   (scoring)
  duplicate.py   (similarity)
  critique.py    (LLM API)
  pipeline.py    (orchestration)

# Dependency flow (no cycles):
# pipeline.py -> heuristic.py -> duplicate.py
# pipeline.py -> critique.py
```

## Gotcha: Split-Target Pattern (Cross-Module Imports)

When two modules import the same function for different purposes, each needs its own patch target:

```python
# main.py imports extract_text for preview()
# service.py imports extract_text for process_file()

# Preview tests → patch main (preview calls it directly)
@patch("pdf2anki.main.extract_text")
def test_preview_shows_text(...):

# Convert tests → patch service (convert delegates to service.process_file)
@patch("pdf2anki.service.extract_text")
def test_convert_txt_to_tsv(...):
```

### Migration checklist (when moving functions between modules)

1. `grep -r '@patch("module_a.' tests/` to find all patches
2. For each patch, trace the call chain: which module *looks up* this function at runtime?
3. Update target to the module where `from X import func` appears
4. Run tests - failures reveal missed patches

## When to Use

- Splitting any Python module (>400 LOC) into a package
- Any refactoring that moves functions between modules when tests use `patch()`
- Introducing a service/adapter layer that changes import paths
- Grep pattern to find affected tests: `grep -r 'patch("pkg.old_module\.' tests/`
