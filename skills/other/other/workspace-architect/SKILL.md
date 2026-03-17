---
name: browser-automation
description: Local Python-based browser automation toolkit using Playwright. Provides command-line tools for navigating, interacting with, and testing web applications without using MCP protocols. Supports clicking, typing, hovering, screenshots, content extraction, and JavaScript execution.
license: ISC
---

# Browser Automation Skill

This skill provides local browser automation capabilities using Python and Playwright. All browser automation is performed locally via CLI commands - **no MCP servers required**.

## Prerequisites

Install Playwright Python library:

```bash
pip install playwright
playwright install chromium
```

## Available Tools

All tools are implemented as subcommands in `assets/skills/browser-automation/scripts/browser_tools.py`. Run any command with `--help` to see detailed usage.

### browser_navigate

Navigate to a URL and wait for the page to load.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_navigate <url>
```

**Example:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_navigate https://example.com
```

### browser_click

Click an element on a page using a CSS selector or text match.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_click <url> <selector> [--text TEXT]
```

**Parameters:**
- `url`: URL to navigate to
- `selector`: CSS selector for the element
- `--text`: (Optional) Text to match instead of using selector

**Examples:**
```bash
# Click by selector
python assets/skills/browser-automation/scripts/browser_tools.py browser_click https://example.com "#submit-button"

# Click by text
python assets/skills/browser-automation/scripts/browser_tools.py browser_click https://example.com "button" --text "Submit"
```

### browser_type

Type text into an input field, with optional form submission.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_type <url> <selector> <text> [--submit]
```

**Parameters:**
- `url`: URL to navigate to
- `selector`: CSS selector for the input field
- `text`: Text to type
- `--submit`: (Optional) Press Enter after typing

**Examples:**
```bash
# Type into field
python assets/skills/browser-automation/scripts/browser_tools.py browser_type https://example.com "#email" "user@example.com"

# Type and submit
python assets/skills/browser-automation/scripts/browser_tools.py browser_type https://example.com "#search" "query" --submit
```

### browser_screenshot

Capture a screenshot of the current page.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_screenshot <url> <path> [--full_page]
```

**Parameters:**
- `url`: URL to navigate to
- `path`: Output file path for the screenshot
- `--full_page`: (Optional) Capture the entire scrollable page

**Examples:**
```bash
# Viewport screenshot
python assets/skills/browser-automation/scripts/browser_tools.py browser_screenshot https://example.com /tmp/screenshot.png

# Full page screenshot
python assets/skills/browser-automation/scripts/browser_tools.py browser_screenshot https://example.com /tmp/full.png --full_page
```

### browser_get_content

Extract text or HTML content from the page or a specific element.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_get_content <url> [--selector SELECTOR] [--html]
```

**Parameters:**
- `url`: URL to navigate to
- `--selector`: (Optional) CSS selector, defaults to 'body'
- `--html`: (Optional) Return HTML instead of text

**Examples:**
```bash
# Get all page text
python assets/skills/browser-automation/scripts/browser_tools.py browser_get_content https://example.com

# Get specific element text
python assets/skills/browser-automation/scripts/browser_tools.py browser_get_content https://example.com --selector "#main-content"

# Get HTML
python assets/skills/browser-automation/scripts/browser_tools.py browser_get_content https://example.com --selector "article" --html
```

### browser_hover

Hover over an element to trigger hover states or tooltips.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_hover <url> <selector>
```

**Parameters:**
- `url`: URL to navigate to
- `selector`: CSS selector for the element

**Example:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_hover https://example.com ".menu-item"
```

### browser_evaluate

Execute custom JavaScript code in the browser context.

**Usage:**
```bash
python assets/skills/browser-automation/scripts/browser_tools.py browser_evaluate <url> <script>
```

**Parameters:**
- `url`: URL to navigate to
- `script`: JavaScript code to execute

**Examples:**
```bash
# Get page title
python assets/skills/browser-automation/scripts/browser_tools.py browser_evaluate https://example.com "document.title"

# Get element count
python assets/skills/browser-automation/scripts/browser_tools.py browser_evaluate https://example.com "document.querySelectorAll('button').length"

# Manipulate DOM
python assets/skills/browser-automation/scripts/browser_tools.py browser_evaluate https://example.com "document.body.style.backgroundColor = 'red'"
```

## Best Practices

1. **Always use full URLs**: Include the protocol (http:// or https://)
2. **Wait for content**: The tool automatically waits for 'networkidle' state
3. **Use robust selectors**: Prefer ID selectors (#id) or specific CSS classes
4. **Error handling**: All commands exit with non-zero status on failure and print errors to stderr
5. **Headless mode**: All operations run in headless Chromium by default

## Common Patterns

### Form Automation
```bash
# Fill out a multi-field form
python assets/skills/browser-automation/scripts/browser_tools.py browser_type https://example.com "#name" "John Doe"
python assets/skills/browser-automation/scripts/browser_tools.py browser_type https://example.com "#email" "john@example.com"
python assets/skills/browser-automation/scripts/browser_tools.py browser_click https://example.com "#submit"
```

### Visual Testing
```bash
# Note: Each command runs in a separate browser instance (stateless).
# The after screenshot won't show the toggled state from the click command.
# For stateful testing, combine actions in a custom Playwright script.

# Capture initial state
python assets/skills/browser-automation/scripts/browser_tools.py browser_screenshot https://example.com /tmp/before.png

# Compare different pages or states (each is independent)
python assets/skills/browser-automation/scripts/browser_tools.py browser_screenshot https://example.com/page1 /tmp/page1.png
python assets/skills/browser-automation/scripts/browser_tools.py browser_screenshot https://example.com/page2 /tmp/page2.png
```

### Content Extraction
```bash
# Extract and process page content
python assets/skills/browser-automation/scripts/browser_tools.py browser_get_content https://example.com --selector "article" > article.txt
```

## Architecture

- **Stateless design**: Each command launches a new browser instance
- **No persistent sessions**: Browser closes after each operation
- **Local execution**: All automation runs locally, no remote MCP servers
- **Simple I/O**: Results printed to stdout, errors to stderr

## Troubleshooting

If you encounter issues:

1. **Install Playwright browsers**: Run `playwright install chromium`
2. **Check Python version**: Requires Python 3.8+
3. **Verify URL accessibility**: Ensure the target URL is reachable
4. **Inspect selectors**: Use browser DevTools to verify CSS selectors

## Related Resources

- Examples: `assets/skills/webapp-testing/examples/`
- Playwright Documentation: https://playwright.dev/python/
