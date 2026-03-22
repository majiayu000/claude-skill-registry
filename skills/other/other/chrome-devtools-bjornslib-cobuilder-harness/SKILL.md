---
name: chrome-devtools
description: Use for Chrome DevTools browser automation, E2E testing, screenshot capture, console log inspection, network request monitoring, performance tracing, Core Web Vitals, page navigation, form filling, JavaScript evaluation. 26 tools for browser debugging and testing.
version: 1.0.0
title: "Chrome Devtools"
status: active
---

# chrome-devtools Skill

Browser automation and debugging via Chrome DevTools Protocol. Supports E2E testing, screenshots, console/network inspection, and performance analysis.

## Context Efficiency

Traditional MCP approach:
- All 26 tools loaded at startup
- Estimated context: 13000 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `click`: Clicks on the provided element
- `close_page`: Closes the page by its index. The last open page cannot be closed.
- `drag`: Drag an element onto another element
- `emulate`: Emulates various features on the selected page.
- `evaluate_script`: Evaluate a JavaScript function inside the currently selected page. Returns the response as JSON
so returned values have to JSON-serializable.
- `fill`: Type text into a input, text area or select an option from a <select> element.
- `fill_form`: Fill out multiple form elements at once
- `get_console_message`: Gets a console message by its ID. You can get all messages by calling list_console_messages.
- `get_network_request`: Gets a network request by an optional reqid, if omitted returns the currently selected request in the DevTools Network panel.
- `handle_dialog`: If a browser dialog was opened, use this command to handle it
- `hover`: Hover over the provided element
- `list_console_messages`: List all console messages for the currently selected page since the last navigation.
- `list_network_requests`: List all requests for the currently selected page since the last navigation.
- `list_pages`: Get a list of pages open in the browser.
- `navigate_page`: Navigates the currently selected page to a URL.
- `new_page`: Creates a new page
- `performance_analyze_insight`: Provides more detailed information on a specific Performance Insight of an insight set that was highlighted in the results of a trace recording.
- `performance_start_trace`: Starts a performance trace recording on the selected page. This can be used to look for performance problems and insights to improve the performance of the page. It will also report Core Web Vital (CWV) scores for the page.
- `performance_stop_trace`: Stops the active performance trace recording on the selected page.
- `press_key`: Press a key or key combination. Use this when other input methods like fill() cannot be used (e.g., keyboard shortcuts, navigation keys, or special key combinations).
- `resize_page`: Resizes the selected page's window so that the page has specified dimension
- `select_page`: Select a page as a context for future tool calls.
- `take_screenshot`: Take a screenshot of the page or element.
- `take_snapshot`: Take a text snapshot of the currently selected page based on the a11y tree. The snapshot lists page elements along with a unique
identifier (uid). Always use the latest snapshot. Prefer taking a snapshot over taking a screenshot. The snapshot indicates the element selected
in the DevTools Elements panel (if any).
- `upload_file`: Upload a file through a provided element.
- `wait_for`: Wait for the specified text to appear on the selected page.

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
python .claude/skills/mcp-skills/executor.py --skill chrome-devtools --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill chrome-devtools --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Take a screenshot of the page"

Your workflow:
1. Identify tool: `take_screenshot`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill chrome-devtools --call '{"tool": "take_screenshot", "arguments": {}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill chrome-devtools --describe take_screenshot
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 13000 tokens | 100 tokens |
| Active | 13000 tokens | 5k tokens |
| Executing | 13000 tokens | 0 tokens |

Savings: ~61% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
