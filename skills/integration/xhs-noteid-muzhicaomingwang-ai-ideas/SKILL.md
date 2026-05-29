---
name: xhs-noteid
description: Extract Xiaohongshu (小红书) noteId from shared note text or URLs, including xhslink.com short links and xiaohongshu.com/discovery/item/<noteId> links. Use when the user asks for “noteId/笔记ID”, provides a 小红书 share message, or pastes an xhslink short URL that needs redirect expansion.
---

# Extract noteId from XiaoHongShu shares

## Fast path (no network)

- Find and return the `<noteId>` in URLs like `https://www.xiaohongshu.com/discovery/item/<noteId>`.
- Also accept share text that contains that URL; extract the same `<noteId>`.
- Prefer returning only the ID (or `noteId: <id>` if the user wants a labeled answer).

## Short-link path (`xhslink.com`)

If the user only provides a short link like `http://xhslink.com/o/...`, expand redirects to a long URL, then extract the `<noteId>` from `/discovery/item/<noteId>`.

- Resolve redirect (requires network access/approval in sandboxed runs):
  - `curl -sS -L -o /dev/null -w '%{url_effective}' '<short-url>'`
- Extract `<noteId>` from the resolved URL.

## Script

Use `scripts/extract_noteid.py` for deterministic extraction and optional short-link resolution.

