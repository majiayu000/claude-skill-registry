---
name: mcp-playwright
description: This skill provides guidance for using Playwright MCP for browser automation. Use when navigating web pages, interacting with web elements, taking screenshots, filling forms, running browser tests, or automating any browser-based tasks.
---

# Playwright MCP

## Overview

This skill enables browser automation using Playwright through MCP. Playwright provides powerful browser control capabilities including navigation, element interaction, screenshots, and form handling.

## When to Use This Skill

- Navigating and interacting with web pages
- Taking screenshots of web content
- Filling out forms and submitting data
- Testing web applications
- Extracting information from web pages
- Automating repetitive browser tasks

## Quick Start Workflow

1. Navigate to a page: `browser_navigate`
2. Take a snapshot to get element refs: `browser_snapshot`
3. Interact with elements using refs from snapshot: `browser_click`, `browser_type`

## Core Tools

### Navigation

**browser_navigate** - Navigate to a URL
```
mcp__playwright__browser_navigate({ url: "https://example.com" })
```

**browser_navigate_back** - Go back to previous page
```
mcp__playwright__browser_navigate_back({})
```

### Page Analysis

**browser_snapshot** - Get accessibility tree (preferred for interaction)
```
mcp__playwright__browser_snapshot({})
```

**browser_take_screenshot** - Capture visual screenshot
```
mcp__playwright__browser_take_screenshot({
  type: "png",
  fullPage: true,
  filename: "screenshot.png"
})
```

### Element Interaction

**browser_click** - Click an element (requires ref from snapshot)
```
mcp__playwright__browser_click({
  element: "Submit button",
  ref: "button[ref='submit']"
})
```

**browser_type** - Type text into an element
```
mcp__playwright__browser_type({
  element: "Search input",
  ref: "input[ref='search']",
  text: "search query",
  submit: true
})
```

**browser_hover** - Hover over an element
```
mcp__playwright__browser_hover({
  element: "Menu item",
  ref: "li[ref='menu']"
})
```

### Form Handling

**browser_fill_form** - Fill multiple form fields
```
mcp__playwright__browser_fill_form({
  fields: [
    { name: "Username", type: "textbox", ref: "input[name='user']", value: "john" },
    { name: "Remember", type: "checkbox", ref: "input[name='remember']", value: "true" }
  ]
})
```

**browser_select_option** - Select dropdown option
```
mcp__playwright__browser_select_option({
  element: "Country",
  ref: "select[ref='country']",
  values: ["JP"]
})
```

### Waiting and Dialogs

**browser_wait_for** - Wait for conditions
```
mcp__playwright__browser_wait_for({ text: "Loading complete" })
mcp__playwright__browser_wait_for({ textGone: "Please wait..." })
mcp__playwright__browser_wait_for({ time: 2 })
```

**browser_handle_dialog** - Handle browser dialogs
```
mcp__playwright__browser_handle_dialog({ accept: true, promptText: "input" })
```

### Page Management

**browser_tabs** - Manage tabs
```
mcp__playwright__browser_tabs({ action: "list" })
mcp__playwright__browser_tabs({ action: "new" })
mcp__playwright__browser_tabs({ action: "select", index: 0 })
```

**browser_close** - Close page
```
mcp__playwright__browser_close({})
```

### Advanced

**browser_evaluate** - Execute JavaScript
```
mcp__playwright__browser_evaluate({ function: "() => document.title" })
```

**browser_press_key** - Press keyboard key
```
mcp__playwright__browser_press_key({ key: "Enter" })
```

## Best Practices

1. **Always snapshot first**: Use `browser_snapshot` before interacting to get element refs
2. **Use descriptive element names**: Provide clear descriptions in `element` parameter
3. **Wait for content**: Use `browser_wait_for` before interacting with dynamic content
4. **Handle dialogs**: Check for dialog prompts and handle appropriately
5. **Clean up**: Close browser when done with `browser_close`

## References

For complete tool parameters, see `references/tools.md`.
