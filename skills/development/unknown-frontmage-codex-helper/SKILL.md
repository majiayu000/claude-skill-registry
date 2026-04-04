---
name: node-llm-web-automation
description: Build or update Node.js + LLM API workflows that replace Codex/MCP UI exploration for web automation at lower cost. Use when a user asks to productize page-structure discovery into a Node runner (Puppeteer/Playwright) with LLM-based element selection, deterministic playback control, cost controls, logging, and fallback paths.
---

# Node LLM Web Automation

## Overview

Turn manual Codex-driven page exploration into a low-cost Node.js automation flow that uses a single LLM call to pick DOM candidates, then drives the UI deterministically.

## Workflow

### 1) Define the automation scope

- List entry URLs (login, course detail, list page).
- Mark manual steps (captcha, 2FA) and provide a pause + resume checkpoint.
- Decide the end condition (completion badge, video end, DOM state change).

### 2) Implement deterministic candidate scanning

- Collect clickable candidates from all frames (anchors, buttons, list items).
- Attach metadata: text, href, data-key/resourceId, tag/class, domIndex, frame URL.
- Run heuristic filtering first; only call LLM if needed.

### 3) LLM selection (single shot)

- Send a minimal payload with the candidate list and a strict JSON schema.
- Parse JSON defensively; fall back to heuristic ordering if parsing fails.
- Cache the selection per page to avoid repeated calls.

### 4) Execute playback loop

- Click the selected item, wait for `video` to appear, force mute + playbackRate.
- Poll progress every N seconds; stop when progress reaches 100% or completion DOM appears.
- On failure: dump DOM + screenshot + current URL for support.

### 5) Cost controls and reliability

- Avoid LLM calls during long playback; only use it for selection.
- Keep payload small (truncate text, drop large attributes).
- Use timeouts and retries for video start.

## References

- See `references/node-llm-runner.md` for prompt templates, candidate schema, and error-handling patterns.

## Notes for this repo

- If working inside `codex_helper`, start from `tools/simple-runner-manual.js` and adapt it to the target site.
- Keep the LLM call optional; prefer heuristic selection when possible.
