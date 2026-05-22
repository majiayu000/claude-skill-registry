---
name: playwright
description: Dynamic access to playwright MCP server (22 tools)
version: 1.0.0
title: "Playwright"
status: active
---

# playwright Skill

Access playwright MCP server capabilities.

## Context Efficiency

Traditional MCP approach:
- All 22 tools loaded at startup
- Estimated context: 11000 tokens

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

- `browser_close`: Close the page
- `browser_resize`: Resize the browser window
- `browser_console_messages`: Returns all console messages
- `browser_handle_dialog`: Handle a dialog
- `browser_evaluate`: Evaluate JavaScript expression on page or element
- `browser_file_upload`: Upload one or multiple files
- `browser_fill_form`: Fill multiple form fields
- `browser_install`: Install the browser specified in the config. Call this if you get an error about the browser not being installed.
- `browser_press_key`: Press a key on the keyboard
- `browser_type`: Type text into editable element
- `browser_navigate`: Navigate to a URL
- `browser_navigate_back`: Go back to the previous page
- `browser_network_requests`: Returns all network requests since loading the page
- `browser_run_code`: Run Playwright code snippet
- `browser_take_screenshot`: Take a screenshot of the current page. You can't perform actions based on the screenshot, use browser_snapshot for actions.
- `browser_snapshot`: Capture accessibility snapshot of the current page, this is better than screenshot
- `browser_click`: Perform click on a web page
- `browser_drag`: Perform drag and drop between two elements
- `browser_hover`: Hover over element on page
- `browser_select_option`: Select an option in a dropdown
- `browser_tabs`: List, create, close, or select a browser tab.
- `browser_wait_for`: Wait for text to appear or disappear or a specified time to pass

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
python .claude/skills/mcp-skills/executor.py --skill playwright --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill playwright --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Navigate to a website with Playwright"

Your workflow:
1. Identify tool: `browser_navigate`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill playwright --call '{"tool": "browser_navigate", "arguments": {"url": "https://example.com"}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill playwright --describe browser_take_screenshot
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
| Idle | 11000 tokens | 100 tokens |
| Active | 11000 tokens | 5k tokens |
| Executing | 11000 tokens | 0 tokens |

Savings: ~54% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
