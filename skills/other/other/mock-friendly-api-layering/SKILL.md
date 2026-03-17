---
name: mock-friendly-api-layering
description: "Use when mock assertions fail due to public functions forwarding internal params like url or timeout to a shared helper."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---

# Mock-Friendly API Layering

**Extracted:** 2026-02-11
**Context:** AnkiConnect client (anki_connect.py) — public functions forwarding `url` to internal `_invoke` broke mock assertions.

## Problem

When public functions forward internal routing parameters (like `url`, `timeout`, `base_path`) to a low-level helper, tests that mock the helper fail on `assert_called_once_with()` because of unexpected kwargs.

```python
# BAD: ensure_deck forwards url to _invoke
def ensure_deck(name: str, *, url: str = ANKICONNECT_URL) -> None:
    _invoke("createDeck", url=url, deck=name)

# Test expects:
mock.assert_called_once_with("createDeck", deck="pdf2anki::test")
# Actual call:
# _invoke("createDeck", url="http://127.0.0.1:8765", deck="pdf2anki::test")
# → AssertionError: unexpected kwarg url
```

## Solution

Keep internal routing parameters only on the lowest-level function (`_invoke`). Public functions expose only business-relevant parameters.

```python
# GOOD: public function has no url param
def ensure_deck(name: str) -> None:
    _invoke("createDeck", deck=name)

# _invoke owns the url default internally
def _invoke(action: str, *, url: str = ANKICONNECT_URL, **params: Any) -> Any:
    ...
```

## Design Principle

| Layer | Owns | Example |
|-------|------|---------|
| `_invoke` (internal) | Transport: url, timeout, headers | `_invoke("action", url=..., **params)` |
| Public functions | Business params only | `ensure_deck(name)`, `push_cards(cards, deck_name=...)` |

## When to Use

- Wrapping HTTP APIs (AnkiConnect, REST, GraphQL) with an internal `_invoke` / `_request` helper
- Any module with a low-level helper + multiple public functions that delegate to it
- When `mock.assert_called_once_with()` fails due to extra kwargs from defaults
