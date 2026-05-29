---
name: browser
description: Minimal Chrome DevTools Protocol tools for browser automation and scraping. Use when you need to start Chrome, navigate pages, execute JavaScript, take screenshots, or interactively pick DOM elements.
---

# Browser Tools

Minimal CDP tools for collaborative site exploration and scraping.

**IMPORTANT**: All scripts are located in `~/.factory/skills/browser/` and must be called with full paths.

## Start Chrome

```bash
~/.factory/skills/browser/start.js              # Fresh profile
~/.factory/skills/browser/start.js --profile    # Copy your profile (cookies, logins)
```

Start Chrome on `:9222` with remote debugging.

## Navigate

```bash
~/.factory/skills/browser/nav.js https://example.com
~/.factory/skills/browser/nav.js https://example.com --new
```

Navigate current tab or open new tab.

## Evaluate JavaScript

```bash
~/.factory/skills/browser/eval.js 'document.title'
~/.factory/skills/browser/eval.js 'document.querySelectorAll("a").length'
```

Execute JavaScript in active tab (async context).

**IMPORTANT**: The code must be a single expression or use IIFE for multiple statements:

- Single expression: `'document.title'`
- Multiple statements: `'(() => { const x = 1; return x + 1; })()'`
- Avoid newlines in the code string - keep it on one line

## Screenshot

```bash
~/.factory/skills/browser/screenshot.js
```

Screenshot current viewport, returns temp file path.

## Pick Elements

```bash
~/.factory/skills/browser/pick.js "Click the submit button"
```

Interactive element picker. Click to select, Cmd/Ctrl+Click for multi-select, Enter to finish.

## Usage Notes

- Start Chrome first before using other tools
- The `--profile` flag syncs your actual Chrome profile so you're logged in everywhere
- JavaScript evaluation runs in an async context in the page
- Pick tool allows you to visually select DOM elements by clicking on them
