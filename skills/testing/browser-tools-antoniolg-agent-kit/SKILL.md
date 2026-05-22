---
name: browser-tools
description: Use the browser-tools CLI (Chrome DevTools Protocol via puppeteer-core) to drive Chrome for navigation, eval, screenshots, DOM picking, console logs, cookies, search, and tab inspection.
---

# Browser Tools

## Overview

Use this skill whenever a task needs Chrome automation via DevTools (navigate, evaluate JS, screenshots, DOM picking, console logs, cookies, search/content extraction, or listing/terminating DevTools-enabled Chrome).

## Quick start

1. Launch Chrome with DevTools enabled (use the repo's package manager to run `tsx`):
   - `pnpm tsx skills/browser-tools/scripts/browser-tools.ts start --profile`
2. Navigate:
   - `pnpm tsx skills/browser-tools/scripts/browser-tools.ts nav https://example.com`
3. Screenshot:
   - `pnpm tsx skills/browser-tools/scripts/browser-tools.ts screenshot`

## Common commands

- `start` Launch Chrome with `--remote-debugging-port` and optional profile copy.
- `nav <url>` Navigate current tab (or `--new`).
- `eval <code...>` Run JS in page context (supports async).
- `screenshot` Capture viewport to a temp PNG path.
- `pick <message...>` Interactive DOM element picker.
- `console` Stream console logs (filters, follow mode).
- `cookies` Dump cookies as JSON.
- `search <query...>` Google search in Chrome; optional readable content.
- `content <url>` Readability extraction to markdown-like text.
- `inspect` List DevTools-enabled Chrome processes + tabs.
- `kill` Terminate DevTools-enabled Chrome processes.

## Notes

- Script path: `skills/browser-tools/scripts/browser-tools.ts` (copied from steipete/agent-scripts).
- Dependencies: `puppeteer-core`, `commander`, `tsx` (or Bun). If missing, install in the active repo or run the copy from `~/Projects/oss/agent-scripts`.
- The tool connects to Chrome via `http://localhost:<port>` and supports DevTools ports and pipes for inspect/kill.

## Resources

### scripts/

- `browser-tools.ts` (CLI)
