---
name: web-browser
description: "Allows to interact with web pages by performing actions such as clicking buttons, filling out forms, and navigating links. It works by remote controlling Google Chrome or Chromium browsers using the Chrome DevTools Protocol (CDP). When Claude needs to browse the web, it can use this skill to do so."
license: Stolen from Mario
---

# Web Browser Skill

Full-featured browser automation with CDP tools for collaborative site exploration.

**🔧 修复说明**：已修复关闭主浏览器的问题。现在使用完全独立的浏览器实例，不影响你的主 Chrome。详见 [FIX_NOTE.md](./FIX_NOTE.md)

**🎲 随机端口**：每次启动时自动生成随机端口（9222-9999），避免端口冲突。端口信息保存在 `~/.cache/scraping-web-browser/port.txt`，下次启动会复用相同端口。

**💾 持久化存储**：默认使用 Chromium 浏览器，数据持久化保存在 `~/.cache/scraping-web-browser/`，包括 cookies、localStorage、session data 等，重启后自动恢复。

## Quick Start

```bash
# Run demo to test everything works
node demo.js

# Get current port
node scripts/get-port.js

# Start Chromium browser (default, with persistent storage)
node scripts/start.js
```

## Browser Management

### Start Chromium (Default)

\`\`\`bash
./scripts/start.js              # Start Chromium with persistent storage
./scripts/start.js --chrome     # Use Google Chrome instead of Chromium
\`\`\`

Start Chromium on a random port (9222-9999) with remote debugging. The port is saved and reused for subsequent starts.

**Important**: This skill starts a completely independent browser instance with its own profile directory (`~/.cache/scraping-web-browser`). It will NOT affect your existing Chrome browser or close any open tabs. The browser runs in the background and persists cookies, localStorage, and session data between restarts.

### Stop Chrome

\`\`\`bash
./scripts/stop.js               # Stop the browser
\`\`\`

Gracefully stop the browser. Port configuration is preserved for next start.

### Get Port

\`\`\`bash
./scripts/get-port.js           # Show current port
\`\`\`

## Navigation

### Navigate

\`\`\`bash
./scripts/nav.js https://example.com
./scripts/nav.js https://example.com --new
\`\`\`

Navigate current tab or open new tab.

### Reload

\`\`\`bash
./scripts/reload.js                     # Normal reload
./scripts/reload.js --force-cache       # Force using cache
./scripts/reload.js --force-no-cache    # Force reload without cache
\`\`\`

Reload the current page with cache control.

### Tabs

\`\`\`bash
./scripts/tabs.js list                  # List all tabs
./scripts/tabs.js new                   # Open new tab
./scripts/tabs.js new "https://example.com"  # Open new tab with URL
./scripts/tabs.js switch 1              # Switch to tab by index
./scripts/tabs.js close 0               # Close tab by index
./scripts/tabs.js close-others          # Close all other tabs
\`\`\`

Manage browser tabs.

## Form Interaction

### Click

\`\`\`bash
./scripts/click.js "#submit-button"
./scripts/click.js ".cta-button"
\`\`\`

Click an element by selector.

### Type

\`\`\`bash
./scripts/type.js "#username" "john@example.com"
./scripts/type.js "#password" "secret123"
./scripts/type.js "#search" "query" --clear    # Clear before typing
\`\`\`

Type text into an input field.

### Select

\`\`\`bash
./scripts/select.js "#country" "United States"
./scripts/select.js "select[name=language]" "JavaScript"
\`\`\`

Select an option from a dropdown.

### Checkbox

\`\`\`bash
./scripts/checkbox.js "#terms" check
./scripts/checkbox.js "#newsletter" uncheck
./scripts/checkbox.js "[name=privacy]" toggle
\`\`\`

Check, uncheck, or toggle checkboxes and radiobuttons.

### Submit

\`\`\`bash
./scripts/submit.js "form"
./scripts/submit.js "#login-form"
\`\`\`

Submit a form.

## Waiting & Detection

### Wait For

\`\`\`bash
./scripts/wait-for.js selector "#result"
./scripts/wait-for.js visible ".loading"
./scripts/wait-for.js hidden ".spinner"
./scripts/wait-for.js text "Success"
./scripts/wait-for.js url "/dashboard" 5000
\`\`\`

Wait for elements, visibility, text, or URL changes.

### Wait For URL

\`\`\`bash
./scripts/wait-for-url.js "https://example.com/dashboard"
./scripts/wait-for-url.js "/success" 5000
\`\`\`

Wait for URL to change to a specific value.

### Check Visible

\`\`\`bash
./scripts/check-visible.js "#button"
./scripts/check-visible.js ".modal"
\`\`\`

Check if an element is visible.

### Get Element

\`\`\`bash
./scripts/get-element.js "#button"
./scripts/get-element.js ".card"
\`\`\`

Get detailed information about an element.

## Storage & Cookies

### Cookies

\`\`\`bash
./scripts/cookies.js list
./scripts/cookies.js get "session"
./scripts/cookies.js set "token" "abc123"
./scripts/cookies.js delete "session"
./scripts/cookies.js clear
./scripts/cookies.js export cookies.json
./scripts/cookies.js import cookies.json
\`\`\`

Manage cookies (list, get, set, delete, clear, export, import).

### Storage

\`\`\`bash
./scripts/storage.js list
./scripts/storage.js get local "token"
./scripts/storage.js set local "user" '\{"name":"John"\}'
./scripts/storage.js delete session "temp"
./scripts/storage.js clear local
\`\`\`

Manage localStorage and sessionStorage.

### Clear Data

\`\`\`bash
./scripts/clear-data.js cookies
./scripts/clear-data.js localStorage
./scripts/clear-data.js sessionStorage
./scripts/clear-data.js cache
./scripts/clear-data.js all
\`\`\`

Clear browser data.

## Network & Performance

### Network

\`\`\`bash
./scripts/network.js start
./scripts/network.js stop
./scripts/network.js capture "https://example.com"
./scripts/network.js export requests.json
\`\`\`

Monitor and capture network requests.

### Performance

\`\`\`bash
./scripts/performance.js
\`\`\`

Get performance metrics and timing breakdown.

### Intercept

\`\`\`bash
./scripts/intercept.js block "*.png"
./scripts/intercept.js mock "/api/data" '\{"result":"success"\}'
./scripts/intercept.js log "/api/*"
./scripts/intercept.js clear
\`\`\`

Block, mock, or log network requests.

## Advanced Features

### Scroll

\`\`\`bash
./scripts/scroll.js down 500
./scripts/scroll.js up 500
./scripts/scroll.js top
./scripts/scroll.js bottom
./scripts/scroll.js element "#section"
\`\`\`

Scroll the page.

### Hover

\`\`\`bash
./scripts/hover.js "#menu"
./scripts/hover.js ".dropdown"
\`\`\`

Hover over an element.

### Upload

\`\`\`bash
./scripts/upload.js "#file-input" "/path/to/file.txt"
./scripts/upload.js "input[type=file]" "./image.png"
\`\`\`

Upload a file.

### Download

\`\`\`bash
./scripts/download.js start "*.pdf"
./scripts/download.js click "#download-btn"
./scripts/download.js list
./scripts/download.js clear
\`\`\`

Manage file downloads.

### PDF

\`\`\`bash
./scripts/pdf.js ./page.pdf
./scripts/pdf.js ./page.pdf A4
./scripts/pdf.js ~/Downloads/report.pdf Letter
\`\`\`

Export current page as PDF.

## Debugging & Tools

### Debug

\`\`\`bash
./scripts/debug.js
\`\`\`

Show browser debug information.

### Inspect

\`\`\`bash
./scripts/inspect.js "#button"
./scripts/inspect.js ".card"
\`\`\`

Inspect elements in detail.

### Find Text

\`\`\`bash
./scripts/find-text.js "Hello World"
./scripts/find-text.js "Error" --case-sensitive
\`\`\`

Find text on the page.

### Get Meta

\`\`\`bash
./scripts/get-meta.js
\`\`\`

Get page metadata (Open Graph, Twitter Card, JSON-LD, etc.).

## JavaScript Evaluation

### Evaluate JavaScript

\`\`\`bash
./scripts/eval.js 'document.title'
./scripts/eval.js 'document.querySelectorAll("a").length'
./scripts/eval.js 'JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => ({ text: a.textContent.trim(), href: a.href })).filter(link => !link.href.startsWith("https://")))'
\`\`\`

Execute JavaScript in active tab (async context). Be careful with string escaping, best to use single quotes.

## Screenshots

### Screenshot

\`\`\`bash
./scripts/screenshot.js
\`\`\`

Screenshot current viewport, returns temp file path.

## Element Selection

### Pick Elements

\`\`\`bash
./scripts/pick.js "Click the submit button"
\`\`\`

Interactive element picker. Click to select, Cmd/Ctrl+Click for multi-select, Enter to finish.

## Console

### Check Console

\`\`\`bash
./scripts/check-console.js
\`\`\`

Check console logs and errors.

### Console Logs

\`\`\`bash
./scripts/console-logs.js
\`\`\`

Get console logs.

## Script Reference

### Browser Management (3)
- `start.js` - Start Chrome with random port
- `stop.js` - Stop Chrome
- `get-port.js` - Get current port

### Navigation (3)
- `nav.js` - Navigate to URL
- `reload.js` - Reload page
- `tabs.js` - Manage tabs

### Form Interaction (5)
- `click.js` - Click element
- `type.js` - Type text
- `select.js` - Select dropdown option
- `checkbox.js` - Check/uncheck/toggle
- `submit.js` - Submit form

### Waiting & Detection (4)
- `wait-for.js` - Wait for element/visible/hidden/text/url
- `wait-for-url.js` - Wait for URL change
- `check-visible.js` - Check element visibility
- `get-element.js` - Get element info

### Storage & Cookies (3)
- `cookies.js` - Cookie management
- `storage.js` - localStorage/sessionStorage management
- `clear-data.js` - Clear browser data

### Network & Performance (4)
- `network.js` - Network monitoring
- `performance.js` - Performance metrics
- `intercept.js` - Request interception
- `reload.js` - Reload with cache control

### Advanced Features (6)
- `scroll.js` - Page scrolling
- `hover.js` - Mouse hover
- `upload.js` - File upload
- `download.js` - File download
- `pdf.js` - PDF export
- `tabs.js` - Tab management

### Debugging & Tools (4)
- `debug.js` - Debug information
- `inspect.js` - Element inspection
- `find-text.js` - Text search
- `get-meta.js` - Page metadata

### Core (4)
- `eval.js` - JavaScript evaluation
- `screenshot.js` - Screenshot
- `pick.js` - Element picker
- `check-console.js` - Console check

**Total: 36 scripts**

## Best Practices

1. **Always stop browser**: Use `node scripts/stop.js` when done to release resources
2. **Check port**: Use `node scripts/get-port.js` to see current port
3. **Error handling**: If errors occur, restart browser and retry
4. **Persistence**: All data (cookies, localStorage, sessions) persists in `~/.cache/scraping-web-browser/`
5. **Wait strategies**: Use `wait-for.js` for dynamic content
6. **Network monitoring**: Use `network.js start/stop` to analyze requests
7. **Debugging**: Use `debug.js` and `inspect.js` for troubleshooting

## Port Management

- **Random port**: Automatically generated on first start (9222-9999)
- **Port persistence**: Port is saved to `~/.cache/scraping-web-browser/port.txt`
- **Reuse**: Next start uses the same port
- **Reset**: Delete port.txt to get a new random port
- **Check port**: Run `node scripts/get-port.js` to see current port

## Configuration Directory

- **Config**: `~/.cache/scraping-web-browser/`
- **Port file**: `~/.cache/scraping-web-browser/port.txt`
- **Cookies**: `~/.cache/scraping-web-browser/Default/Cookies`
- **LocalStorage**: `~/.cache/scraping-web-browser/Default/Local Storage/`

## Process Management

\`\`\`bash
# View process
ps aux | grep "scraping-web-browser"

# Stop browser
node scripts/stop.js

# Force stop
pkill -f "scraping-web-browser"
\`\`\`