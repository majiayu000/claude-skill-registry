---
name: automating-browser
description: "Controls Chrome browser: takes screenshots, clicks buttons, fills forms, downloads images, inspects pages, captures network requests, checks console errors, debugs API issues. Use when: 'screenshot', 'click', 'fill form', 'download image', 'check browser', 'look at screen', 'capture page', 'check for errors', 'debug network', 'API failing', 'console errors'. Provides MCP tool discovery for 70 tabz_* browser automation tools."
---

# Tabz MCP - Browser Automation

## Overview

Control Chrome browser programmatically via the Tabz MCP server. 70 tools for screenshots, interaction, network debugging, and more.

## Tool Discovery (MCP-CLI Mode)

```bash
# List all tabz tools
mcp-cli tools tabz

# Search for specific tools
mcp-cli tools tabz | grep screenshot
mcp-cli grep "network"

# Get tool schema before calling (REQUIRED)
mcp-cli info tabz/tabz_screenshot

# Call tool
mcp-cli call tabz/tabz_screenshot '{}'
```

## Browser Debugging (Common Issues)

### Check Console Errors

```bash
mcp-cli info tabz/tabz_get_console_logs
mcp-cli call tabz/tabz_get_console_logs '{"level": "error"}'
```

### Debug Network/API Issues

```bash
# 1. Enable capture BEFORE triggering the action
mcp-cli info tabz/tabz_enable_network_capture
mcp-cli call tabz/tabz_enable_network_capture '{}'

# 2. Trigger the action (click button, navigate, etc.)

# 3. Get failed requests (status >= 400)
mcp-cli info tabz/tabz_get_network_requests
mcp-cli call tabz/tabz_get_network_requests '{"statusMin": 400}'

# Or filter by URL pattern
mcp-cli call tabz/tabz_get_network_requests '{"urlPattern": "api/"}'
```

### Screenshot for Visual QA

```bash
mcp-cli info tabz/tabz_screenshot
mcp-cli call tabz/tabz_screenshot '{}'
# Returns file path - use Read tool to view the image
```

### Check Page State

```bash
mcp-cli info tabz/tabz_get_page_info
mcp-cli call tabz/tabz_get_page_info '{}'
# Returns URL, title, loading state

mcp-cli info tabz/tabz_get_element
mcp-cli call tabz/tabz_get_element '{"selector": "#error-message", "includeStyles": true}'
```

### Performance Profiling

```bash
mcp-cli info tabz/tabz_profile_performance
mcp-cli call tabz/tabz_profile_performance '{}'
# Returns: DOM node count, JS heap size, event listeners, timing metrics
```

### DOM Tree Inspection

```bash
mcp-cli info tabz/tabz_get_dom_tree
mcp-cli call tabz/tabz_get_dom_tree '{"maxDepth": 3}'
# Or focus on specific element
mcp-cli call tabz/tabz_get_dom_tree '{"selector": "main", "maxDepth": 5}'
```

### Code Coverage Analysis

```bash
mcp-cli info tabz/tabz_get_coverage
mcp-cli call tabz/tabz_get_coverage '{"type": "js"}'
# Shows used vs unused bytes per file
```

## Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| Tab Management | `list_tabs`, `switch_tab`, `rename_tab`, `open_url` | Navigate tabs |
| Tab Groups | `create_group`, `add_to_group`, `ungroup_tabs` | Organize tabs |
| Windows | `list_windows`, `create_window`, `tile_windows` | Window management |
| Audio | `speak`, `list_voices`, `play_audio` | TTS notifications |
| Page Info | `get_page_info`, `get_element`, `get_dom_tree` | Inspect content |
| Interaction | `click`, `fill` | Click/type |
| Screenshots | `screenshot`, `screenshot_full` | Capture visuals |
| Downloads | `download_image`, `download_file` | Save files |
| Network | `enable_network_capture`, `get_network_requests` | Debug APIs |
| Console | `get_console_logs`, `execute_script` | Debug JS |
| Performance | `profile_performance`, `get_coverage` | Diagnose slowness |
| Emulation | `emulate_device`, `emulate_geolocation` | Responsive testing |

## Tab Groups (Parallel Workers)

When multiple Claude workers run in parallel, each MUST create their own named group:

```bash
# Create unique group for this worker
mcp-cli info tabz/tabz_create_group
mcp-cli call tabz/tabz_create_group '{"tabIds": [123, 456], "title": "ISSUE-ID: Research", "color": "blue"}'

# Add more tabs later
mcp-cli call tabz/tabz_add_to_group '{"groupId": 12345, "tabIds": [789]}'

# Cleanup when done
mcp-cli call tabz/tabz_ungroup_tabs '{"tabIds": [123, 456, 789]}'
```

**Group colors:** grey, blue, red, yellow, green, pink, purple, cyan

## Quick Patterns

**Screenshot:**
```bash
mcp-cli call tabz/tabz_screenshot '{}'
```

**Click:**
```bash
mcp-cli call tabz/tabz_click '{"selector": "button.submit"}'
```

**Fill form:**
```bash
mcp-cli call tabz/tabz_fill '{"selector": "#email", "value": "test@example.com"}'
```

**Switch tab:**
```bash
mcp-cli call tabz/tabz_list_tabs '{}'  # Get tab IDs (large integers like 1762556601)
mcp-cli call tabz/tabz_switch_tab '{"tabId": 1762556601}'
```

**TTS notification:**
```bash
mcp-cli call tabz/tabz_speak '{"text": "Done!", "priority": "high"}'
```

## Important Notes

1. **Always check schema first**: Run `mcp-cli info tabz/<tool>` before `mcp-cli call`
2. **Tab IDs**: Chrome tab IDs are large integers (e.g., `1762556601`), not 1, 2, 3
3. **Network capture**: Enable BEFORE the page makes requests
4. **Screenshots**: Return file paths - use Read tool to view
5. **Selectors**: CSS selectors - `#id`, `.class`, `button[type="submit"]`
6. **JSON quoting**: Use single quotes around JSON, double quotes inside

## Heredoc for Complex JSON

For complex nested JSON, use heredoc to avoid escaping issues:

```bash
mcp-cli call tabz/tabz_execute_script - <<'EOF'
{"code": "document.querySelector('button').click()"}
EOF
```

## Resources

See `references/workflows.md` for more patterns.
