---
name: website-review
description: Use this skill when performing QA reviews of the EVOLEA website (Astro frontend at localhost:4321), Admin Dashboard V2 (localhost:5175), or production sites (planted.com, admin.planted.com). Orchestrates visual inspection, console/network error detection, accessibility auditing, Core Web Vitals measurement, and interactive testing using Chrome DevTools MCP. (project)
---

# Website Review Workflow

This skill enables comprehensive QA workflows for EVOLEA web properties using Chrome DevTools MCP integration.

## Prerequisites

1. **Chrome Debug Mode Running**
   ```bash
   # Start Chrome with debug port (run once per session)
   scripts\chrome-debug.bat
   ```

2. **MCP Server Connected**
   - Verify with `/mcp` command - look for `chrome-devtools` server
   - If not connected, restart Claude Code (MCP servers load on startup)

3. **For Keystatic CMS**
   - Production: https://www.evolea.ch/keystatic
   - Staging: https://evolea-website.pages.dev/keystatic
   - Auth state persists in `%USERPROFILE%\.chrome-debug-profile`

## Target Sites

| Site | URL | Auth Required | Notes |
|------|-----|---------------|-------|
| Local Dev | http://localhost:4321 | No | Run `npm run dev` |
| Production | https://www.evolea.ch | No | Primary custom domain |
| Staging | https://evolea-website.pages.dev | No | Cloudflare Pages default |
| GitHub Pages | https://cgjen-box.github.io/evolea-website/ | No | Static fallback |

**Note:** `https://evolea.ch` redirects to `https://www.evolea.ch` (301)

## Workflow Overview

```
+---------------------+     +---------------------+     +---------------------+
|  1. NAVIGATE &      |---->|  2. VISUAL          |---->|  3. CONSOLE/NETWORK |
|     SCREENSHOT      |     |     INSPECTION      |     |     ERROR CHECK     |
+---------------------+     +---------------------+     +---------------------+
                                                                  |
+---------------------+     +---------------------+               |
|  6. GENERATE        |<----|  5. INTERACTIVE     |<--------------+
|     REPORT          |     |     TESTING         |               |
+---------------------+     +---------------------+               |
                                   ^                              |
                                   |            +-----------------+
                                   |            |
                            +------+------------v--+
                            |  4. ACCESSIBILITY &  |
                            |     PERFORMANCE      |
                            +----------------------+
```

## Phase 1: Navigate and Screenshot

**Goal:** Capture initial page state across viewports

**MCP Tools:**
- `navigate_page(url)` - Navigate to target URL
- `resize_page(width, height)` - Set viewport size
- `take_screenshot()` - Capture visual state
- `wait_for(selector, timeout)` - Wait for page load

**Viewport Sizes:**
- Desktop: 1440x900
- Tablet: 768x1024
- Mobile: 375x812

**Example Workflow:**
1. Navigate to URL
2. Wait for main content selector
3. Screenshot desktop viewport
4. Resize to tablet, screenshot
5. Resize to mobile, screenshot

## Phase 2: Visual Inspection

**Goal:** Analyze visual state and DOM structure

**MCP Tools:**
- `take_snapshot()` - Capture DOM snapshot (accessibility tree)
- `evaluate_script(script)` - Run DOM queries

**Checks:**
- Layout renders correctly
- Images load (no broken images)
- Fonts load correctly
- No overlapping elements
- Responsive breakpoints work

## Phase 3: Console and Network Error Check

**Goal:** Detect JavaScript errors and failed requests

**MCP Tools:**
- `list_console_messages()` - Get all console output
- `get_console_message(id)` - Get specific message details
- `list_network_requests()` - Get all network activity
- `get_network_request(id)` - Get request/response details

**Error Categories:**
- **Critical:** JavaScript exceptions, failed API calls (4xx/5xx)
- **Warning:** Console warnings, slow requests (>3s)
- **Info:** Deprecation notices, third-party issues

## Phase 4: Accessibility and Performance

### Accessibility (WCAG 2.1 AA)

**Automated Checks via evaluate_script:**
```javascript
// Check for missing alt text
document.querySelectorAll('img:not([alt])').length

// Check for form labels
document.querySelectorAll('input:not([aria-label]):not([id])').length

// Check for heading hierarchy
Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6')).map(h => h.tagName)
```

**Manual Checks:**
- Keyboard navigation works (Tab through page)
- Focus states visible
- Screen reader landmarks present
- Touch targets >= 44px

### Performance (Core Web Vitals)

**MCP Tools:**
- `performance_start_trace()` - Begin recording
- `performance_stop_trace()` - End recording
- `performance_analyze_insight()` - Get analysis

**Metrics to Check:**
- **LCP (Largest Contentful Paint):** < 2.5s good, < 4s needs improvement
- **INP (Interaction to Next Paint):** < 200ms good, < 500ms needs improvement
- **CLS (Cumulative Layout Shift):** < 0.1 good, < 0.25 needs improvement

## Phase 5: Interactive Testing

**Goal:** Verify interactive elements work correctly

**MCP Tools:**
- `click(selector)` - Click element
- `fill(selector, value)` - Fill input
- `fill_form(fields)` - Fill multiple form fields
- `press_key(key)` - Keyboard input
- `hover(selector)` - Hover state
- `handle_dialog(action)` - Handle alerts/confirms

**Test Scenarios:**
- Navigation links work
- Form submission works
- Buttons trigger expected actions
- Modal dialogs open/close
- Dropdowns/selects function

## Phase 6: Generate Report

Use `TEST-REPORT-TEMPLATE.md` to create structured report including:
- Screenshots at each viewport
- Console errors found
- Network issues found
- Accessibility issues
- Performance metrics
- Interactive test results
- Overall pass/fail status

---

## Quick Commands

```bash
# Start local Astro dev server
npm run dev

# Start Chrome in debug mode
scripts\chrome-debug.bat
```

## MCP Tools Reference (26 Total)

### Input Automation
| Tool | Purpose |
|------|---------|
| `click` | Click an element |
| `drag` | Drag from one point to another |
| `fill` | Fill a form field |
| `fill_form` | Fill multiple form fields |
| `handle_dialog` | Handle alert/confirm/prompt dialogs |
| `hover` | Hover over an element |
| `press_key` | Press keyboard key |
| `upload_file` | Upload file to input |

### Navigation
| Tool | Purpose |
|------|---------|
| `close_page` | Close current page/tab |
| `list_pages` | List all open pages |
| `navigate_page` | Navigate to URL |
| `new_page` | Open new page/tab |
| `select_page` | Switch to specific page |
| `wait_for` | Wait for element/condition |

### Emulation
| Tool | Purpose |
|------|---------|
| `emulate` | Emulate device (mobile, etc.) |
| `resize_page` | Set viewport dimensions |

### Performance
| Tool | Purpose |
|------|---------|
| `performance_start_trace` | Start performance recording |
| `performance_stop_trace` | Stop and get trace data |
| `performance_analyze_insight` | Analyze performance metrics |

### Network
| Tool | Purpose |
|------|---------|
| `list_network_requests` | Get network request history |
| `get_network_request` | Get specific request details |

### Debugging
| Tool | Purpose |
|------|---------|
| `take_screenshot` | Capture visual screenshot |
| `take_snapshot` | Capture accessibility tree (DOM) |
| `list_console_messages` | Get browser console logs |
| `get_console_message` | Get specific console message |
| `evaluate_script` | Execute JavaScript in page |

## Reference Documents

- `TESTING-MANUAL.md` - Detailed test cases for each page type
- `TEST-REPORT-TEMPLATE.md` - Report format
- `AUTH-SETUP.md` - Production authentication setup
- `.claude/skills/EVOLEA-SKILL.md` - Visual design reference
