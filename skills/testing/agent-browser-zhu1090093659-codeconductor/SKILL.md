---
name: agent-browser
description: Browser automation via the agent-browser CLI for navigation, interaction, snapshots, extraction, screenshots, network controls, storage, tabs, frames, and debugging. Use when tasks require automated web UI actions, form filling, scraping, state capture, or repeatable browser workflows.
---

# Agent Browser

## Overview

Use agent-browser to automate web UI tasks from CodeConductor. Prefer `/browser <args>` to execute commands through the built-in integration.

## Quick start

1. Navigate: `/browser open https://example.com`
2. Snapshot: `/browser snapshot`
3. Act using refs or selectors (click, fill, type).
4. Validate with `get` or `is` commands.
5. Capture `screenshot` or `trace` if needed.
6. `close` when done.

## Workflow

1. Define the target URL, required outputs, and authentication needs.
2. Set viewport/device/headers/credentials when required.
3. Use `snapshot` or `find` commands to locate elements deterministically.
4. Use `wait` to stabilize before actions.
5. Execute actions in small steps and validate with `get` or `is`.
6. Save artifacts (screenshot, state, trace) only when needed.
7. Close the browser.

## Selector and waiting guidance

- Prefer refs from `snapshot` output for deterministic targeting.
- Use semantic locators: `find role`, `find label`, `find text`, `find placeholder`, `find testid`.
- Use `wait` for elements, text, URL patterns, or network idle before actions.

## Command reference (all supported)

### Core
```
agent-browser open <url>
agent-browser click <sel>
agent-browser dblclick <sel>
agent-browser fill <sel> <text>
agent-browser type <sel> <text>
agent-browser press <key>
agent-browser hover <sel>
agent-browser select <sel> <val>
agent-browser check <sel>
agent-browser uncheck <sel>
agent-browser scroll <dir> [px]
agent-browser screenshot [path]
agent-browser snapshot
agent-browser eval <js>
agent-browser close
```

### Get info
```
agent-browser get text <sel>
agent-browser get html <sel>
agent-browser get value <sel>
agent-browser get attr <sel> <attr>
agent-browser get title
agent-browser get url
agent-browser get count <sel>
agent-browser get box <sel>
```

### Check state
```
agent-browser is visible <sel>
agent-browser is enabled <sel>
agent-browser is checked <sel>
```

### Find elements
```
agent-browser find role <role> <action> [value]
agent-browser find text <text> <action>
agent-browser find label <label> <action> [value]
agent-browser find placeholder <ph> <action> [value]
agent-browser find testid <id> <action> [value]
agent-browser find first <sel> <action> [value]
agent-browser find nth <n> <sel> <action> [value]
```

### Wait
```
agent-browser wait <selector>
agent-browser wait <ms>
agent-browser wait --text "<text>"
agent-browser wait --url "<pattern>"
agent-browser wait --load networkidle
agent-browser wait --fn "<condition>"
```

### Mouse
```
agent-browser mouse move <x> <y>
agent-browser mouse down [button]
agent-browser mouse up [button]
agent-browser mouse wheel <dy> [dx]
```

### Settings
```
agent-browser set viewport <w> <h>
agent-browser set device <name>
agent-browser set geo <lat> <lng>
agent-browser set offline [on|off]
agent-browser set headers <json>
agent-browser set credentials <u> <p>
agent-browser set media [dark|light]
```

### Cookies and storage
```
agent-browser cookies
agent-browser cookies set <name> <val>
agent-browser cookies clear

agent-browser storage local
agent-browser storage local <key>
agent-browser storage local set <k> <v>
agent-browser storage local clear

agent-browser storage session
agent-browser storage session <key>
agent-browser storage session set <k> <v>
agent-browser storage session clear
```

### Network
```
agent-browser network route <url>
agent-browser network route <url> --abort
agent-browser network route <url> --body <json>
agent-browser network unroute [url]
agent-browser network requests
```

### Tabs and frames
```
agent-browser tab
agent-browser tab new [url]
agent-browser tab <n>
agent-browser tab close [n]
agent-browser frame <sel>
agent-browser frame main
```

### Debug
```
agent-browser trace start [path]
agent-browser trace stop [path]
agent-browser console
agent-browser errors
agent-browser highlight <sel>
agent-browser state save <path>
agent-browser state load <path>
```

### Navigation
```
agent-browser back
agent-browser forward
agent-browser reload
```

## CodeConductor execution

When running from chat, prefix commands with `/browser`:

- `/browser open https://example.com`
- `/browser snapshot`
- `/browser find role button click --name "Submit"`
