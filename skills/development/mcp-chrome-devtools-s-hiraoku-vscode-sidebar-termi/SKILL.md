---
name: mcp-chrome-devtools
description: This skill provides guidance for using Chrome DevTools MCP for browser debugging and automation. Use when debugging web pages, analyzing performance, inspecting network requests, viewing console messages, or interacting with Chrome DevTools features programmatically.
---

# Chrome DevTools MCP

## Overview

This skill enables browser debugging and automation using Chrome DevTools through MCP. It provides access to Chrome DevTools features including page interaction, network analysis, console inspection, and performance tracing.

## When to Use This Skill

- Debugging web page issues
- Analyzing network requests and responses
- Inspecting console messages and errors
- Performance profiling and tracing
- Automated page interaction and testing
- Taking screenshots and snapshots

## Quick Start Workflow

1. List pages: `list_pages`
2. Select a page: `select_page`
3. Take snapshot: `take_snapshot`
4. Interact using uids from snapshot

## Core Tools

### Page Management

**list_pages** - Get all open pages
```
mcp__chrome-devtools__list_pages({})
```

**select_page** - Select a page for operations
```
mcp__chrome-devtools__select_page({ pageIdx: 0 })
```

**new_page** - Create a new page
```
mcp__chrome-devtools__new_page({ url: "https://example.com" })
```

**close_page** - Close a page
```
mcp__chrome-devtools__close_page({ pageIdx: 1 })
```

**navigate_page** - Navigate the selected page
```
mcp__chrome-devtools__navigate_page({ type: "url", url: "https://example.com" })
mcp__chrome-devtools__navigate_page({ type: "back" })
mcp__chrome-devtools__navigate_page({ type: "reload", ignoreCache: true })
```

### Snapshots and Screenshots

**take_snapshot** - Get accessibility tree (preferred for interaction)
```
mcp__chrome-devtools__take_snapshot({})
```

**take_screenshot** - Capture visual screenshot
```
mcp__chrome-devtools__take_screenshot({
  format: "png",
  fullPage: true,
  filePath: "./screenshot.png"
})
```

### Element Interaction

**click** - Click an element
```
mcp__chrome-devtools__click({ uid: "element-uid" })
mcp__chrome-devtools__click({ uid: "element-uid", dblClick: true })
```

**fill** - Fill input or select option
```
mcp__chrome-devtools__fill({ uid: "input-uid", value: "text" })
```

**fill_form** - Fill multiple form elements
```
mcp__chrome-devtools__fill_form({
  elements: [
    { uid: "username-uid", value: "user" },
    { uid: "password-uid", value: "pass" }
  ]
})
```

**hover** - Hover over an element
```
mcp__chrome-devtools__hover({ uid: "element-uid" })
```

**drag** - Drag and drop
```
mcp__chrome-devtools__drag({ from_uid: "source", to_uid: "target" })
```

### Debugging Tools

**list_console_messages** - Get console messages
```
mcp__chrome-devtools__list_console_messages({})
mcp__chrome-devtools__list_console_messages({ types: ["error", "warn"] })
```

**get_console_message** - Get specific message details
```
mcp__chrome-devtools__get_console_message({ msgid: 1 })
```

**list_network_requests** - Get network requests
```
mcp__chrome-devtools__list_network_requests({})
mcp__chrome-devtools__list_network_requests({ resourceTypes: ["fetch", "xhr"] })
```

**get_network_request** - Get request details
```
mcp__chrome-devtools__get_network_request({ reqid: 1 })
```

### Performance Tools

**performance_start_trace** - Start performance trace
```
mcp__chrome-devtools__performance_start_trace({
  reload: true,
  autoStop: true
})
```

**performance_stop_trace** - Stop performance trace
```
mcp__chrome-devtools__performance_stop_trace({})
```

**performance_analyze_insight** - Analyze performance insight
```
mcp__chrome-devtools__performance_analyze_insight({
  insightSetId: "insight-set-id",
  insightName: "LCPBreakdown"
})
```

### Advanced Tools

**evaluate_script** - Execute JavaScript
```
mcp__chrome-devtools__evaluate_script({
  function: "() => document.title"
})
```

**press_key** - Press keyboard key
```
mcp__chrome-devtools__press_key({ key: "Enter" })
mcp__chrome-devtools__press_key({ key: "Control+A" })
```

**emulate** - Emulate conditions
```
mcp__chrome-devtools__emulate({
  networkConditions: "Slow 3G",
  cpuThrottlingRate: 4
})
```

**handle_dialog** - Handle browser dialog
```
mcp__chrome-devtools__handle_dialog({ action: "accept" })
```

**wait_for** - Wait for text
```
mcp__chrome-devtools__wait_for({ text: "Loading complete" })
```

## Best Practices

1. **Always snapshot first**: Use `take_snapshot` before interacting to get uids
2. **Select page first**: Use `select_page` before page-specific operations
3. **Check console for errors**: Use `list_console_messages` for debugging
4. **Inspect network**: Use `list_network_requests` to debug API issues
5. **Use emulation**: Test with throttling for performance issues

## References

For complete tool parameters, see `references/tools.md`.
