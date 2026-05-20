---
name: browser-testing
description: "Use when testing web applications, debugging browser console errors, automating form interactions, or verifying UI implementations. Load for localhost testing, authenticated app testing (Gmail, Notion), or recording demo GIFs. Requires Chrome extension 1.0.36+, Claude Code 2.0.73+, paid plan."
keywords: browser, chrome, testing, console, debug, forms, ui, gif, localhost
---

# Browser Testing

Test and debug web applications via Chrome integration.

## Prerequisites

| Requirement | Minimum |
|-------------|---------|
| Chrome extension | 1.0.36+ |
| Claude Code CLI | 2.0.73+ |
| Plan | Pro/Team/Enterprise |

## Instructions

1. Enable Chrome: `claude --chrome` or `/chrome`
2. Get tab context: `tabs_context_mcp`
3. Navigate: `navigate` to URL
4. Interact: `find`, `form_input`, `computer`
5. Verify: `read_console_messages`, `read_page`
6. Evidence: `computer(action="screenshot")`

## Quick Commands

```bash
# Check for console errors
scripts/check-console-errors.sh TAB_ID

# Verify page loaded
scripts/verify-page-load.sh TAB_ID URL

# Run smoke test
scripts/smoke-test.sh URL
```

## MCP Tools

| Tool | Purpose |
|------|---------|
| `tabs_context_mcp` | Get tab IDs (call first) |
| `navigate` | Go to URL |
| `computer` | Click, type, screenshot |
| `find` | Find element by description |
| `form_input` | Fill form fields |
| `read_console_messages` | Debug with pattern filter |
| `read_page` | Get DOM/accessibility tree |
| `gif_creator` | Record interactions |

## References

| File | Load When |
|------|-----------|
| references/patterns.md | Designing test scenarios |
| references/examples.md | Need concrete examples |
