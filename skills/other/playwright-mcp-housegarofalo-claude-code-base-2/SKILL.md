---
name: playwright-mcp
description: Browser automation via Playwright MCP server. Navigate, click, type, scrape, screenshot, and test web pages. Use when automating browser interactions, web scraping, E2E testing, PDF generation, or screenshot capture. Triggers on browser automation, web scraping, playwright, headless browser, E2E testing, screenshot, PDF export.
---

# Playwright MCP Browser Automation

Comprehensive browser automation using the Playwright MCP server integration.

## Setup

### Installation

```bash
npx @anthropic-ai/claude-code@latest mcp add playwright -- npx @playwright/mcp@latest
```

### Configuration Options

| Option | Description | Example |
|--------|-------------|---------|
| `--browser` | Browser to use | `chrome`, `firefox`, `webkit`, `msedge` |
| `--headless` | Run without UI | `--headless` (default) or `--no-headless` |
| `--device` | Emulate device | `--device="iPhone 15"` |
| `--viewport` | Set viewport size | `--viewport="1920x1080"` |
| `--caps` | Enable capabilities | `--caps=vision,pdf,testing,tracing` |

## Core Tools

### Navigation

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Navigate to URL |
| `browser_navigate_back` | Go back in history |
| `browser_tabs` | Manage tabs (list/new/close/select) |
| `browser_close` | Close page/browser |
| `browser_resize` | Resize window |

### Interaction

| Tool | Purpose |
|------|---------|
| `browser_click` | Click element |
| `browser_type` | Type into input |
| `browser_fill_form` | Fill multiple form fields |
| `browser_select_option` | Select dropdown option |
| `browser_hover` | Hover over element |
| `browser_drag` | Drag and drop |
| `browser_press_key` | Press keyboard key |
| `browser_file_upload` | Upload files |
| `browser_handle_dialog` | Handle JS dialogs |

### Information Retrieval

| Tool | Purpose |
|------|---------|
| `browser_snapshot` | Get page accessibility tree (preferred) |
| `browser_take_screenshot` | Capture visual screenshot |
| `browser_console_messages` | Get console logs |
| `browser_network_requests` | Get network requests |

### Utilities

| Tool | Purpose |
|------|---------|
| `browser_wait_for` | Wait for conditions |
| `browser_evaluate` | Execute JavaScript |
| `browser_run_code` | Run Playwright code |
| `browser_install` | Install browser |

## Common Patterns

### Web Scraping

```
1. browser_navigate to target URL
2. browser_wait_for content to load
3. browser_snapshot to get page structure
4. browser_evaluate to extract data
5. Repeat for pagination if needed
```

### Form Automation

```
1. browser_navigate to form page
2. browser_snapshot to find form fields
3. browser_fill_form with all field data
4. browser_click submit button
5. browser_wait_for success indicator
```

### Authentication Flow

```
1. browser_navigate to login page
2. browser_snapshot to identify fields
3. browser_type username into email field
4. browser_type password into password field
5. browser_click login button
6. browser_wait_for dashboard content
```

### Screenshot Capture

```
1. browser_navigate to target page
2. browser_wait_for content to load
3. browser_take_screenshot with options:
   - fullPage: true for entire page
   - element/ref for specific element
```

## Element References

Elements are identified using accessibility tree references from `browser_snapshot`:

```
- link[Home] - Link with text "Home"
- button[Submit] - Button labeled "Submit"
- textbox[Email] - Input field labeled "Email"
- combobox[Country] - Dropdown for Country
```

## Optional Capabilities

### Vision (`--caps=vision`)
- `browser_mouse_click_xy` - Click at coordinates
- `browser_mouse_drag_xy` - Drag between coordinates
- `browser_mouse_move_xy` - Move mouse

### PDF (`--caps=pdf`)
- `browser_pdf_save` - Save page as PDF

### Testing (`--caps=testing`)
- `browser_generate_locator` - Generate Playwright locator
- `browser_verify_element_visible` - Verify element visibility
- `browser_verify_text_visible` - Verify text on page
- `browser_verify_value` - Verify element value

### Tracing (`--caps=tracing`)
- `browser_start_tracing` - Start recording trace
- `browser_stop_tracing` - Stop and save trace

## Best Practices

1. **Always use browser_snapshot first** - Understand page structure before interacting
2. **Wait for content** - Use browser_wait_for before interactions
3. **Handle dynamic content** - Re-snapshot after page changes
4. **Use accessibility references** - More reliable than coordinates
5. **Handle dialogs promptly** - They block other actions
6. **Close browser when done** - Free up resources

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Browser not installed | Use `browser_install` tool |
| Element not found | Take fresh `browser_snapshot` |
| Timeout errors | Use `browser_wait_for` with longer time |
| Dialog blocking | Use `browser_handle_dialog` |
| Stale element | Re-snapshot after page changes |

## When to Use This Skill

- Automating browser interactions
- Web scraping dynamic content
- E2E testing workflows
- Generating PDFs from web pages
- Taking screenshots
- Form filling and submission
- Multi-page workflows
