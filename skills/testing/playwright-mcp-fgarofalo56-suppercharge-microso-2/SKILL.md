---
name: playwright-mcp
description: Expert browser automation using Playwright MCP tools. Enables web scraping, form filling, automated testing, screenshot capture, PDF generation, and page interaction. Use when automating browsers, extracting web data, filling forms, testing web apps, taking screenshots, or interacting with web pages programmatically.
---

# Playwright Browser Automation Expert

Expert guidance for browser automation using Playwright MCP tools. This skill provides comprehensive capabilities for web scraping, form automation, testing, screenshot capture, and programmatic browser control.

## Core Capabilities

1. **Navigation & Page Control** - Navigate URLs, manage tabs, resize windows
2. **Element Interaction** - Click, type, hover, drag, select options
3. **Form Automation** - Fill forms, upload files, submit data
4. **Content Extraction** - Accessibility snapshots, screenshots, console logs
5. **Testing & Verification** - Verify elements, text, values
6. **Advanced Features** - PDF generation, tracing, custom JavaScript

## Quick Reference - Available MCP Tools

### Navigation Tools
| Tool | Purpose |
|------|---------|
| `browser_navigate` | Navigate to a URL |
| `browser_navigate_back` | Go back to previous page |
| `browser_tabs` | List, create, close, or select tabs |
| `browser_close` | Close the current page |
| `browser_resize` | Resize browser window |

### Interaction Tools
| Tool | Purpose |
|------|---------|
| `browser_click` | Click on elements |
| `browser_type` | Type text into fields |
| `browser_fill_form` | Fill multiple form fields at once |
| `browser_select_option` | Select dropdown options |
| `browser_hover` | Hover over elements |
| `browser_drag` | Drag and drop between elements |
| `browser_press_key` | Press keyboard keys |
| `browser_file_upload` | Upload files |
| `browser_handle_dialog` | Handle alert/confirm/prompt dialogs |

### Information Retrieval Tools
| Tool | Purpose |
|------|---------|
| `browser_snapshot` | Get accessibility tree snapshot (preferred over screenshot) |
| `browser_take_screenshot` | Capture visual screenshot |
| `browser_console_messages` | Get console log messages |
| `browser_network_requests` | Get all network requests |

### Advanced Tools
| Tool | Purpose |
|------|---------|
| `browser_evaluate` | Execute JavaScript on page |
| `browser_run_code` | Run Playwright code snippets |
| `browser_wait_for` | Wait for text/element/time |
| `browser_install` | Install browser if missing |

---

## Instructions

### Step 1: Understanding the Page (ALWAYS DO FIRST)

Before interacting with any page, ALWAYS capture an accessibility snapshot:

```
Use browser_snapshot to understand the page structure.
This returns element references (ref) needed for interactions.
```

The snapshot provides:
- Element references (`ref`) for targeting
- Element types (button, textbox, link, etc.)
- Accessible names and descriptions
- Page structure hierarchy

### Step 2: Navigation

Navigate to URLs and manage browser state:

```
browser_navigate: url="https://example.com"
browser_navigate_back: (no parameters)
browser_tabs: action="list" | "new" | "close" | "select", index=N
```

### Step 3: Element Interaction

All interactions require two key parameters:
- `element`: Human-readable description (for logging/permission)
- `ref`: Exact element reference from snapshot

**Clicking:**
```
browser_click:
  element="Submit button"
  ref="button[Submit]"
  button="left" | "right" | "middle"  (optional)
  doubleClick=true/false (optional)
```

**Typing:**
```
browser_type:
  element="Search input"
  ref="textbox[Search]"
  text="search query"
  submit=true  (optional - press Enter after)
  slowly=true  (optional - type character by character)
```

**Form Filling (Multiple Fields):**
```
browser_fill_form:
  fields=[
    {"name": "Username", "type": "textbox", "ref": "textbox[Username]", "value": "john"},
    {"name": "Password", "type": "textbox", "ref": "textbox[Password]", "value": "secret"},
    {"name": "Remember", "type": "checkbox", "ref": "checkbox[Remember]", "value": "true"}
  ]
```

### Step 4: Waiting and Synchronization

Wait for page state before proceeding:

```
browser_wait_for:
  text="Welcome"           # Wait for text to appear
  textGone="Loading..."    # Wait for text to disappear
  time=5                   # Wait N seconds
```

### Step 5: Data Extraction

**Accessibility Snapshot (Preferred):**
```
browser_snapshot:
  filename="page-snapshot.md"  (optional - save to file)
```

**Screenshot:**
```
browser_take_screenshot:
  type="png" | "jpeg"
  fullPage=true/false
  element="Header section"  (optional - screenshot specific element)
  ref="header[Main]"        (optional - with element)
  filename="screenshot.png" (optional)
```

**Console Messages:**
```
browser_console_messages:
  level="error" | "warning" | "info" | "debug"
```

**Network Requests:**
```
browser_network_requests:
  includeStatic=true/false
```

---

## Common Workflows

### Web Scraping Workflow

1. Navigate to target URL
2. Take accessibility snapshot to understand structure
3. Extract data from snapshot or use evaluate for complex extraction
4. Handle pagination if needed
5. Close browser when done

```
Example sequence:
1. browser_navigate(url="https://example.com/products")
2. browser_snapshot()
3. browser_evaluate(function="() => { return [...document.querySelectorAll('.product')].map(p => p.textContent) }")
4. browser_click(element="Next page", ref="link[Next]")
5. Repeat 2-4 until done
```

### Form Automation Workflow

1. Navigate to form page
2. Take snapshot to identify form fields
3. Fill all fields using browser_fill_form
4. Handle any file uploads
5. Submit and verify success

```
Example sequence:
1. browser_navigate(url="https://example.com/signup")
2. browser_snapshot()
3. browser_fill_form(fields=[...])
4. browser_file_upload(paths=["C:/docs/resume.pdf"])
5. browser_click(element="Submit", ref="button[Submit]")
6. browser_wait_for(text="Success")
```

### Testing Workflow

1. Navigate to application
2. Perform actions
3. Verify expected state
4. Capture evidence (screenshots, snapshots)

```
Example sequence:
1. browser_navigate(url="https://app.example.com")
2. browser_type(element="Username", ref="textbox[Username]", text="testuser")
3. browser_type(element="Password", ref="textbox[Password]", text="password", submit=true)
4. browser_wait_for(text="Dashboard")
5. browser_take_screenshot(filename="login-success.png")
```

---

## Best Practices

### 1. Always Snapshot First
Never try to interact with elements without first taking a snapshot. The snapshot provides the exact `ref` values needed.

### 2. Use Descriptive Element Names
The `element` parameter should clearly describe what you're interacting with for better logging and debugging.

### 3. Wait Appropriately
After navigation or actions that trigger page changes, use `browser_wait_for` to ensure the page is ready.

### 4. Prefer Accessibility Snapshots Over Screenshots
Snapshots are:
- Faster and lighter
- More accurate for element identification
- Better for LLM processing
- Don't require vision capabilities

### 5. Handle Errors Gracefully
- Check for dialogs using `browser_handle_dialog`
- Verify page state after actions
- Use console messages for debugging

### 6. Use Semantic Selectors
Reference elements by their accessible names rather than fragile CSS selectors when possible.

---

## Tool Parameter Reference

### browser_click
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| element | string | Yes | Human-readable element description |
| ref | string | Yes | Exact element reference from snapshot |
| button | string | No | "left", "right", or "middle" |
| doubleClick | boolean | No | Perform double-click |
| modifiers | array | No | ["Alt", "Control", "Meta", "Shift"] |

### browser_type
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| element | string | Yes | Human-readable element description |
| ref | string | Yes | Exact element reference from snapshot |
| text | string | Yes | Text to type |
| submit | boolean | No | Press Enter after typing |
| slowly | boolean | No | Type one character at a time |

### browser_fill_form
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| fields | array | Yes | Array of field objects |

Field object structure:
```json
{
  "name": "Field name",
  "type": "textbox|checkbox|radio|combobox|slider",
  "ref": "element reference",
  "value": "value to set"
}
```

### browser_navigate
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| url | string | Yes | URL to navigate to |

### browser_tabs
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| action | string | Yes | "list", "new", "close", or "select" |
| index | number | No | Tab index for close/select |

### browser_wait_for
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| text | string | No | Text to wait for |
| textGone | string | No | Text to wait to disappear |
| time | number | No | Seconds to wait |

### browser_take_screenshot
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| type | string | No | "png" or "jpeg" (default: png) |
| fullPage | boolean | No | Capture full scrollable page |
| element | string | No | Element description to screenshot |
| ref | string | No | Element reference (with element) |
| filename | string | No | Save filename |

### browser_evaluate
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| function | string | Yes | JavaScript function to execute |
| element | string | No | Element description (if targeting element) |
| ref | string | No | Element reference (if targeting element) |

### browser_run_code
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| code | string | Yes | Playwright code snippet |

Example:
```javascript
async (page) => {
  await page.getByRole('button', { name: 'Submit' }).click();
  return await page.title();
}
```

---

## When to Use This Skill

- Automating web browser interactions
- Scraping data from websites
- Filling out web forms automatically
- Taking screenshots of web pages
- Testing web applications
- Extracting content from dynamic pages
- Automating repetitive browser tasks
- Generating PDFs from web pages
- Debugging web applications

## Keywords

playwright, browser automation, web scraping, form filling, screenshot, pdf, testing, selenium alternative, puppeteer alternative, web testing, accessibility snapshot, headless browser, browser control, click, type, navigate, web interaction, dom, element interaction
