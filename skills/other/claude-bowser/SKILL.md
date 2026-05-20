---
name: claude-bowser
description: Observable browser automation using Chrome MCP tools. Use when you need to browse websites, take screenshots, interact with web pages, or perform browser tasks in your current Chrome. Keywords - browse, screenshot, browser, chrome, bowser, ui testing, observable.
attribution: Imported from https://github.com/disler/bowser — credit to @disler
---

# Claude Bowser

## Purpose

Automate browsing using Chrome MCP tools (`mcp__claude_in_chrome__*`) available when Claude Code is started with `--chrome`. This uses your real Chrome browser — observable, with your existing profile, cookies, and extensions.

## Pre-flight Check

**Before doing anything**, verify Chrome MCP tools are available. Look for tools matching `mcp__claude_in_chrome__*`.

- If available: proceed with the workflow.
- If NOT available: stop and reply to the user: _"Chrome tools are not available. Please restart Claude Code with the `--chrome` flag: `claude --chrome`"_

## Workflow

1. Resize the browser window to 1440x900
2. Execute the user's request using Chrome MCP tools (navigate, click, screenshot, etc.)
3. Report results back to the user

## Limitations

- **No parallel instances.** All Chrome MCP connections share a single Chrome extension controller. Only one bowser task at a time.
- **Observable only.** This uses your real Chrome — there is no headless mode.
