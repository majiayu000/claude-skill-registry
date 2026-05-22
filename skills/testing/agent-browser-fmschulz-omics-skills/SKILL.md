---
name: agent-browser
description: Browser automation via agent-browser CLI. Use for web navigation, form filling, screenshots, scraping, login flows, UI testing, or any browser interaction. Prefer this over Playwright or dev-browser unless the user explicitly asks for those tools.
---

# Agent Browser

## Setup
- Ensure the CLI is installed: `npm install -g agent-browser`.
- Download Chromium once: `agent-browser install`.
- On Linux, install system deps if needed: `agent-browser install --with-deps`.
- Use `--json` for machine-readable output when needed.

## Default workflow (AI-friendly)
1. `agent-browser open <url>`
2. `agent-browser snapshot -i --json`
3. Interact by refs: `click @eN`, `fill @eN "text"`
4. Re-snapshot after navigation or major UI changes.

## Useful commands
- `agent-browser find role button click --name "Submit"`
- `agent-browser get text @e1 --json`
- `agent-browser screenshot [path]`
- `agent-browser open <url> --headed` (debug)

## Sessions and profiles
- `--session <name>` for isolated sessions.
- `--profile <path>` for persistent state.

## References
- `references/quick-start.md` for full quick start and installation details.
