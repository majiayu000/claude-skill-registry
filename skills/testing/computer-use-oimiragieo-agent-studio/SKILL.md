---
name: computer-use
description: Browser automation with Playwright for computer use. Click, type, scroll, screenshot, and execute JavaScript. Use for web testing, automation, and visual verification tasks.
context:fork: true
allowed-tools: read, write, bash
---

# Computer Use Skill

## Overview

This skill provides Playwright-powered browser automation capabilities via MCP, enabling programmatic interaction with web pages including clicking, typing, scrolling, and screenshot capture.

**Context Savings**: ~90% reduction

- **MCP Mode**: ~12,000 tokens always loaded (6 tools + cursor overlay)
- **Skill Mode**: ~300 tokens metadata + on-demand loading

## Requirements

- Python 3.10+ installed
- Playwright (auto-installed by executor)
- Chromium browser (auto-installed via `playwright install chromium`)

## Tools

The server provides 6 tools for browser automation:

### Lifecycle Tools

| Tool                 | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `initialize_browser` | Launch Chromium browser with URL, viewport size, headless mode |
| `close_browser`      | Close browser and release all resources                        |

### Interaction Tools

| Tool             | Description                                                                               |
| ---------------- | ----------------------------------------------------------------------------------------- |
| `execute_action` | Execute actions: click_at, type_text_at, scroll_to_percent, press_key, execute_javascript |
| `click_selector` | Click element by CSS selector                                                             |
| `fill_selector`  | Fill form field by CSS selector                                                           |

### State Capture Tools

| Tool            | Description                                   |
| --------------- | --------------------------------------------- |
| `capture_state` | Take screenshot and return path + current URL |

## Quick Reference

```bash
# List available tools
python executor.py --list

# Initialize browser (headless)
python executor.py --tool initialize_browser --args '{"url": "https://example.com", "width": 1440, "height": 900}'

# Initialize browser (visible)
CU_HEADFUL=1 python executor.py --tool initialize_browser --args '{"url": "https://google.com"}'

# Click at coordinates (0-1000 scale)
python executor.py --tool execute_action --args '{"action_name": "click_at", "args": {"x": 500, "y": 300}}'

# Type text at coordinates
python executor.py --tool execute_action --args '{"action_name": "type_text_at", "args": {"x": 500, "y": 300, "text": "Hello World", "press_enter": true}}'

# Scroll to 50% of page
python executor.py --tool execute_action --args '{"action_name": "scroll_to_percent", "args": {"y": 500}}'

# Click by CSS selector
python executor.py --tool click_selector --args '{"selector": "button.submit", "nth": 0}'

# Fill form field
python executor.py --tool fill_selector --args '{"selector": "input[name=search]", "text": "Claude AI", "press_enter": true}'

# Take screenshot
python executor.py --tool capture_state --args '{"action_name": "after_click"}'

# Execute JavaScript
python executor.py --tool execute_action --args '{"action_name": "execute_javascript", "args": {"code": "document.title"}}'

# Close browser
python executor.py --tool close_browser
```

## Configuration

### Environment Variables

| Variable          | Description                      | Default            |
| ----------------- | -------------------------------- | ------------------ |
| `CU_HEADFUL`      | Show browser window (1/true/yes) | `false` (headless) |
| `CU_SLOW_MO`      | Delay between actions (ms)       | `250`              |
| `CU_SHOW_CURSOR`  | Show cursor overlay (1/true/yes) | `false`            |
| `CU_NO_SANDBOX`   | Disable Chromium sandbox         | `false`            |
| `CU_DEVICE_SCALE` | Device scale factor              | `2`                |

### Setup

1. **First run** (auto-installs dependencies):

   ```bash
   python .claude/skills/computer-use/executor.py --list
   ```

2. **For visible browser automation**:
   ```bash
   export CU_HEADFUL=1
   export CU_SLOW_MO=500
   ```

## Coordinate System

The system uses a **0-1000 normalized scale** for viewport-independent automation:

- `x=0` = left edge, `x=1000` = right edge
- `y=0` = top edge, `y=1000` = bottom edge

This allows the same coordinates to work across different screen sizes.

**Example**: To click the center of the viewport:

```json
{ "action_name": "click_at", "args": { "x": 500, "y": 500 } }
```

## Tool Details

### initialize_browser

Launch Playwright Chromium browser with specified configuration.

**Parameters**:

- `url` (string, required): Initial URL to navigate to
- `width` (number, optional): Viewport width in pixels (default: 1440)
- `height` (number, optional): Viewport height in pixels (default: 900)
- `headless` (boolean, optional): Run headless (overrides `CU_HEADFUL` env var)

**Returns**:

```json
{
  "ok": true,
  "url": "https://example.com",
  "width": 1440,
  "height": 900,
  "headless": true,
  "slow_mo_ms": 250
}
```

### execute_action

Execute a single browser automation action.

**Parameters**:

- `action_name` (string, required): One of:
  - `open_web_browser` - Navigate to URL
  - `click_at` - Click at coordinates
  - `type_text_at` - Type text at coordinates
  - `scroll_to_percent` - Scroll to position
  - `press_key` - Press keyboard key
  - `execute_javascript` - Run JS code
- `args` (object, required): Action-specific arguments

**Action Arguments**:

| Action               | Required Args                   | Optional Args |
| -------------------- | ------------------------------- | ------------- |
| `open_web_browser`   | `url`                           | -             |
| `click_at`           | `x`, `y` (0-1000)               | -             |
| `type_text_at`       | `x`, `y`, `text`                | `press_enter` |
| `scroll_to_percent`  | `y` (0-1000)                    | -             |
| `press_key`          | `key` (e.g., "Enter", "Meta+L") | -             |
| `execute_javascript` | `code`                          | -             |

### capture_state

Take a screenshot of the current browser state.

**Parameters**:

- `action_name` (string, required): Label for the screenshot file
- `result_ok` (boolean, optional): Whether previous action succeeded
- `error_msg` (string, optional): Error message if action failed

**Returns**:

```json
{
  "ok": true,
  "path": "/tmp/gemini_computer_use/1234567890_action.png",
  "mime_type": "image/png",
  "url": "https://example.com"
}
```

### click_selector

Click an element by CSS selector.

**Parameters**:

- `selector` (string, required): CSS selector for the element
- `nth` (number, optional): Index if multiple matches (default: 0)

### fill_selector

Fill a form field by CSS selector.

**Parameters**:

- `selector` (string, required): CSS selector for the input field
- `text` (string, required): Text to enter
- `press_enter` (boolean, optional): Press Enter after typing
- `clear` (boolean, optional): Clear field before typing (default: true)

### close_browser

Close the browser and release all Playwright resources.

**Parameters**: None

## Usage Examples

### Web Search Automation

```bash
# Initialize browser
python executor.py --tool initialize_browser --args '{"url": "https://google.com"}'

# Click search box (approximate center)
python executor.py --tool execute_action --args '{"action_name": "click_at", "args": {"x": 500, "y": 400}}'

# Type search query
python executor.py --tool execute_action --args '{"action_name": "type_text_at", "args": {"x": 500, "y": 400, "text": "Claude AI", "press_enter": true}}'

# Capture results
python executor.py --tool capture_state --args '{"action_name": "search_results"}'

# Close browser
python executor.py --tool close_browser
```

### Form Filling with Selectors

```bash
# Initialize
python executor.py --tool initialize_browser --args '{"url": "https://example.com/form"}'

# Fill fields by selector
python executor.py --tool fill_selector --args '{"selector": "#name", "text": "John Doe"}'
python executor.py --tool fill_selector --args '{"selector": "#email", "text": "john@example.com"}'

# Click submit button
python executor.py --tool click_selector --args '{"selector": "button[type=submit]"}'

# Capture result
python executor.py --tool capture_state --args '{"action_name": "form_submitted"}'
```

### JavaScript Extraction

```bash
# Get all links on page
python executor.py --tool execute_action --args '{"action_name": "execute_javascript", "args": {"code": "Array.from(document.querySelectorAll(\"a\")).map(a => ({text: a.textContent, href: a.href}))"}}'

# Get page title
python executor.py --tool execute_action --args '{"action_name": "execute_javascript", "args": {"code": "document.title"}}'
```

## Integration with Agents

This skill integrates with the following agents:

- **qa**: For automated browser testing and visual verification
- **developer**: For debugging web applications
- **devops**: For deployment verification and smoke tests

## Troubleshooting

| Error                                | Cause                                   | Fix                                                         |
| ------------------------------------ | --------------------------------------- | ----------------------------------------------------------- |
| "Browser not initialized"            | Tool called before `initialize_browser` | Call `initialize_browser` first                             |
| "Playwright not found"               | Dependencies not installed              | Run `pip install playwright && playwright install chromium` |
| "click_at requires x and y"          | Missing coordinates                     | Provide both `x` and `y` in 0-1000 range                    |
| "Page load wait timed out"           | Slow page load                          | Increase timeout or wait for specific element               |
| "No editable element at click point" | Wrong coordinates                       | Use `fill_selector` instead for form fields                 |

## Security Notes

- Browser automation executes locally via Playwright
- No remote code execution by default
- Screenshots saved to `/tmp/gemini_computer_use/` (or system temp)
- Clear screenshots after sensitive operations
