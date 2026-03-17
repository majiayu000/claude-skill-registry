---
name: headless-browser
description: Browse JS-heavy sites and extract text/snapshots using OpenClaw's built-in browser tool (no stealth).
metadata: {"openclaw":{"emoji":"🌐","requires":{"bins":["openclaw"]}}}
---

# Headless Browser (OpenClaw Browser Tool)

Use this skill when the user asks to:

- open a URL and extract visible text
- take a screenshot
- navigate JS-heavy sites

## Policy / constraints

- Do not attempt to bypass logins, paywalls, or bot protections.
- Do not use stealth plugins or "anti-bot evasion" techniques.
- If a page is blocked, propose alternatives (official APIs, RSS, public mirrors, or ask the user to provide the content).

## How to use (CLI)

Start the managed browser (if needed):

```bash
openclaw browser status
openclaw browser start
```

Open a page:

```bash
openclaw browser open "https://example.com"
```

Extract a snapshot (prefer `--format md` for readable output):

```bash
openclaw browser snapshot --format md --limit 200
```

Take a screenshot:

```bash
openclaw browser screenshot --full-page
```

## Job search guidance

- Prefer public job boards and company career pages.
- If the user mentions LinkedIn, prefer public listings and metadata; do not attempt to access restricted pages.
