---
name: mcp-undetected-chromedriver
description: Use for stealth browser automation that bypasses bot detection. Undetected ChromeDriver for web scraping, anti-detection browsing, form filling, screenshots, PDF export, JavaScript evaluation. 16 tools for automation without triggering bot protection.
version: 1.0.0
title: "Mcp Undetected Chromedriver"
status: active
---

# mcp-undetected-chromedriver Skill

Stealth browser automation using undetected ChromeDriver. Bypasses common bot detection while providing full browser control for scraping, testing, and automation.

## Context Efficiency

Traditional MCP approach:
- All 16 tools loaded at startup
- Estimated context: 8000 tokens

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

- `browser_navigate`: Navigate to a URL

    Args:
        url: The URL to navigate to - required
        timeout: The timeout for the navigation - optional, default is 30000
    
- `browser_screenshot`: Take a screenshot of the current page or a specific element

    Args:
        name: The name of the screenshot - required, default is "screenshot"
        storeBase64: Whether to store the screenshot as a base64 string - optional, default is True
        downloadsDir: The directory to save the screenshot to - optional, default is the user's Downloads directory
    
- `browser_click`: Click an element on the page

    Args:
        selector: The selector of the element to click - required
    
- `browser_iframe_click`: Click an element inside an iframe on the page

    Args:
        iframeSelector: The selector of the iframe - required
        selector: The selector of the element to click - required
    
- `browser_fill`: fill out an input field

    Args:
        selector: CSS selector for input field - required
        value: The value to fill - required
    
- `browser_select`: Select an element on the page with Select tag

    Args:
        selector: CSS selector for element to select - required
        value: The value to select - required
    
- `browser_hover`: Hover over an element on the page

    Args:
        selector: CSS selector for element to hover over - required
    
- `browser_evalute`: Evaluate a JavaScript expression in the browser console

    Args:
        script: The JavaScript expression to evaluate - required
    
- `browser_close`: Close the browser and release all resources
- `browser_get_visible_text`: Get the visible text of the current page
- `browser_get_visible_html`: Get the HTML of the current page
- `browser_go_back`: Navigate back in browser history
- `browser_go_forward`: Navigate forward in browser history
- `browser_drag`: Drag an element to another element

    Args:
        sourceSelector: The selector for the element to drag - required
        targetSelector: The selector for the target location - required
    
- `browser_press_key`: Press a key on the keyboard

    Args:
        key: The key to press - required, (e.g. 'Enter', 'ArrowDown', 'a')
        selector: Optional CSS selector to focus on before pressing the key - optional
    
- `browser_save_as_pdf`: Save the current page as a PDF

    Args:
        outputPath: The path to save the PDF to - required
        filename: The name of the PDF file - optional, default is "page.pdf"
        format: The format of the PDF - optional, default is "A4" (e.g. "A4", "LETTER", "LEGAL", "TABLOID")
        printBackground: Whether to print the background - optional, default is True
        margin: The margin of the PDF - optional, default is None (e.g. {"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"})
    

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
python .claude/skills/mcp-skills/executor.py --skill mcp-undetected-chromedriver --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill mcp-undetected-chromedriver --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Navigate to a website with stealth browser"

Your workflow:
1. Identify tool: `browser_navigate`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill mcp-undetected-chromedriver --call '{"tool": "browser_navigate", "arguments": {"url": "https://example.com"}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill mcp-undetected-chromedriver --describe browser_screenshot
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
| Idle | 8000 tokens | 100 tokens |
| Active | 8000 tokens | 5k tokens |
| Executing | 8000 tokens | 0 tokens |

Savings: ~37% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
