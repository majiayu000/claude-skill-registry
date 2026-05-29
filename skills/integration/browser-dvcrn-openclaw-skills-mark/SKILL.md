---
name: powerskills-browser
description: Edge browser automation via Chrome DevTools Protocol (CDP). List tabs, navigate, take screenshots, extract page content/HTML, execute JavaScript, click elements, type text, fill forms, scroll. Use when needing to control Edge browser, scrape web content, automate web forms, or take browser screenshots on Windows. Requires Edge with --remote-debugging-port=9222.
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---

# PowerSkills — Browser

Edge browser automation via CDP (Chrome DevTools Protocol).

## Requirements

- Microsoft Edge running with remote debugging:
  ```powershell
  Start-Process "msedge" -ArgumentList "--remote-debugging-port=9222"
  ```
- Default port configurable in `config.json` (`edge_debug_port`)

## Actions

```powershell
.\powerskills.ps1 browser <action> [--params]
```

| Action | Params | Description |
|--------|--------|-------------|
| `tabs` | | List open browser tabs |
| `navigate` | `--url URL` | Navigate to URL |
| `screenshot` | `--out-file path.png [--target-id id]` | Capture page as PNG |
| `content` | `[--target-id id]` | Get page text content |
| `html` | `[--target-id id]` | Get full page HTML |
| `evaluate` | `--expression "js"` | Execute JavaScript expression |
| `click` | `--selector "#btn"` | Click element by CSS selector |
| `type` | `--selector "#input" --text "hello"` | Type into element |
| `new-tab` | `--url URL` | Open new tab |
| `close-tab` | `--target-id id` | Close tab by ID |
| `scroll` | `--scroll-target top\|bottom\|selector` | Scroll page |
| `fill` | `--fields-json '[{"selector":"#a","value":"b"}]'` | Fill multiple form fields |
| `wait` | `--seconds N` | Wait N seconds (default: 3) |

## Examples

```powershell
# List open tabs
.\powerskills.ps1 browser tabs

# Navigate and screenshot
.\powerskills.ps1 browser navigate --url "https://example.com"
.\powerskills.ps1 browser screenshot --out-file page.png

# Extract page text
.\powerskills.ps1 browser content

# Run JavaScript
.\powerskills.ps1 browser evaluate --expression "document.title"

# Fill a login form
.\powerskills.ps1 browser fill --fields-json '[{"selector":"#user","value":"alex"},{"selector":"#pass","value":"secret","submit":"#login"}]'
```

## Multi-Tab Support

Pass `--target-id` (from `tabs` output) to operate on a specific tab. Without it, actions target the first page.

## Fill Fields Format

JSON array of objects with `selector`, `value`, and optional `submit`:

```json
[
  {"selector": "#search-input", "value": "PowerShell automation"},
  {"selector": "#filter-type", "value": "recent", "submit": "#apply-btn"}
]
```

Supports text inputs, selects, and checkboxes. Last field can include `submit` to click a button.
