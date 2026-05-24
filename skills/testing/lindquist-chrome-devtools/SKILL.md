---
name: chrome-devtools
description: Control and inspect Chrome browser using Chrome DevTools Protocol - navigate pages, debug network requests, analyze performance, take screenshots, interact with elements, and automate browser tasks.
allowed-tools: mcp__chrome-devtools__*
---

# Chrome DevTools MCP Skill

Complete Chrome browser automation and debugging using the Chrome DevTools Protocol. This skill provides access to all Chrome DevTools capabilities for web development, testing, and debugging tasks.

## Capabilities

1. **Navigate & Automate** - Control browser navigation, tabs, and page interactions
2. **Interact with Pages** - Click, type, drag, fill forms, upload files
3. **Debug & Inspect** - View console logs, network requests, execute scripts
4. **Performance Analysis** - Record traces and get performance insights
5. **Emulation** - Test different devices, network conditions, viewports
6. **Visual Testing** - Take screenshots and DOM snapshots

## Quick Reference

For detailed instructions on each operation, see:
- [NAVIGATION.md](references/NAVIGATION.md) - Page navigation, tabs, waiting
- [INTERACTION.md](references/INTERACTION.md) - Clicking, typing, forms, uploads
- [DEBUGGING.md](references/DEBUGGING.md) - Console logs, network requests, script execution
- [PERFORMANCE.md](references/PERFORMANCE.md) - Performance tracing and analysis
- [EMULATION.md](references/EMULATION.md) - Device and network emulation
- [VISUAL.md](references/VISUAL.md) - Screenshots and DOM snapshots

## Common Workflows

### Web Testing Workflow
1. Navigate to page with `navigate_page`
2. Interact with elements using `click`, `fill`, `press_key`
3. Verify results with `take_screenshot` or `list_console_messages`
4. Check network activity with `list_network_requests`

### Performance Analysis Workflow
1. Start trace with `performance_start_trace`
2. Navigate or interact with page
3. Stop trace with `performance_stop_trace`
4. Get insights with `performance_analyze_insight`

### Debugging Workflow
1. Navigate to problematic page
2. Check console with `list_console_messages`
3. Inspect network with `list_network_requests`
4. Execute diagnostic scripts with `evaluate_script`
5. Take screenshots for visual confirmation

### Form Testing Workflow
1. Navigate to form page
2. Fill individual fields with `fill` or use `fill_form` for bulk entry
3. Upload files if needed with `upload_file`
4. Submit and verify with screenshots/console

## Tool Categories Overview

### Input Automation (8 tools)
- `click` - Click on elements
- `drag` - Drag and drop operations
- `fill` - Enter text in fields
- `fill_form` - Fill multiple form fields
- `handle_dialog` - Manage alerts/dialogs
- `hover` - Hover over elements
- `press_key` - Keyboard input
- `upload_file` - File upload handling

### Navigation (6 tools)
- `navigate_page` - Go to URLs
- `new_page` - Create new tabs
- `close_page` - Close tabs
- `list_pages` - View open tabs
- `select_page` - Switch tabs
- `wait_for` - Wait for conditions

### Emulation (2 tools)
- `emulate` - Device/condition simulation
- `resize_page` - Viewport sizing

### Performance (3 tools)
- `performance_start_trace` - Begin recording
- `performance_stop_trace` - End recording
- `performance_analyze_insight` - Get recommendations

### Network (2 tools)
- `list_network_requests` - View all requests
- `get_network_request` - Get request details

### Debugging (5 tools)
- `evaluate_script` - Run JavaScript
- `take_screenshot` - Capture visuals
- `take_snapshot` - Capture DOM
- `list_console_messages` - View console
- `get_console_message` - Get specific message

## Critical Instructions

**REQUIRED**: Before using ANY Chrome DevTools tools, you MUST load the relevant reference file(s) using the Read tool. These references contain essential operational instructions that are NOT included in this overview.

When the user asks to work with Chrome DevTools:

1. **Identify the operation** they want to perform (navigate, debug, test, analyze)
2. **MANDATORY: Load the relevant reference file(s)** using the Read tool BEFORE executing any tools:
   - Navigation tasks → Read `references/NAVIGATION.md` FIRST
   - Interaction tasks → Read `references/INTERACTION.md` FIRST
   - Debugging tasks → Read `references/DEBUGGING.md` FIRST
   - Performance tasks → Read `references/PERFORMANCE.md` FIRST
   - Emulation tasks → Read `references/EMULATION.md` FIRST
   - Visual testing tasks → Read `references/VISUAL.md` FIRST
3. **Execute the appropriate MCP tool commands** following the patterns from the loaded reference
4. **Report results clearly** with screenshots or data as appropriate
5. **Chain operations** when needed (e.g., navigate → interact → verify)

**DO NOT attempt to use Chrome DevTools tools without first loading and reading the relevant reference documentation.**

## Best Practices

- **Always wait appropriately** - Use `wait_for` to ensure page readiness
- **Handle errors gracefully** - Check console messages and network errors
- **Take screenshots** - Visual confirmation is valuable for debugging
- **Chain operations logically** - Navigate before interacting, start trace before actions
- **Clean up** - Close pages when done to free resources
- **Use selectors carefully** - Ensure element selectors are specific and reliable

## Examples

### Take a screenshot of a website
```
User: "Take a screenshot of example.com"
Me: Uses navigate_page → wait_for → take_screenshot
```

### Test form submission
```
User: "Fill out the login form on staging.example.com"
Me: Uses navigate_page → fill_form → click → list_console_messages
```

### Analyze page performance
```
User: "Check the performance of our homepage"
Me: Uses performance_start_trace → navigate_page → performance_stop_trace → performance_analyze_insight
```

### Debug network issues
```
User: "Why is the API call failing on /dashboard?"
Me: Uses navigate_page → list_network_requests → get_network_request (for failed request)
```

### Test mobile viewport
```
User: "How does the site look on iPhone 13?"
Me: Uses emulate (iPhone 13) → navigate_page → take_screenshot
```

## Configuration

The Chrome DevTools MCP server should be configured in Claude Code's MCP settings:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

Optional configuration flags:
- `--headless false` - Show browser window
- `--categoryEmulation` - Enable emulation tools
- `--categoryPerformance` - Enable performance tools
- `--categoryNetwork` - Enable network tools
