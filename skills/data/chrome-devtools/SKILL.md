---
name: chrome-devtools
description: Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging.
license: Apache-2.0
version: 1.1.0
---

# Chrome DevTools Agent Skill

Browser automation via Puppeteer scripts with persistent sessions. All scripts output JSON.

## Skill Location

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

```bash
# Detect skill location
SKILL_DIR=""
if [ -d ".claude/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR=".claude/skills/chrome-devtools/scripts"
elif [ -d "$HOME/.claude/skills/chrome-devtools/scripts" ]; then
  SKILL_DIR="$HOME/.claude/skills/chrome-devtools/scripts"
fi
cd "$SKILL_DIR"
```

## Choosing Your Approach

| Scenario | Approach |
|----------|----------|
| **Source-available sites** | Read source code first, write selectors directly |
| **Unknown layouts** | Use `aria-snapshot.js` for semantic discovery |
| **Visual inspection** | Take screenshots to verify rendering |
| **Debug issues** | Collect console logs, analyze with session storage |
| **Accessibility audit** | Use ARIA snapshot for semantic structure analysis |

## Automation Browsing Running Mode

- Detect current OS and launch browser as headless only when running on Linux, WSL, or CI environments.
- For macOS/Windows, browser always runs in headed mode for better debugging.
- Run multiple scripts/sessions in parallel to simulate real user interactions.
- Run multiple scripts/sessions in parallel to simulate different device types (mobile, tablet, desktop).
- Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

## ARIA Snapshot (Element Discovery)

When page structure is unknown, use `aria-snapshot.js` to get a YAML-formatted accessibility tree with semantic roles, accessible names, states, and stable element references.

### Get ARIA Snapshot

```bash
# Generate ARIA snapshot and output to stdout
node aria-snapshot.js --url https://example.com

# Save to file in snapshots directory
node aria-snapshot.js --url https://example.com --output ./.claude/chrome-devtools/snapshots/page.yaml
```

### Example YAML Output

```yaml
- banner:
  - link "Hacker News" [ref=e1]
    /url: https://news.ycombinator.com
  - navigation:
    - link "new" [ref=e2]
    - link "past" [ref=e3]
    - link "comments" [ref=e4]
- main:
  - list:
    - listitem:
      - link "Show HN: My new project" [ref=e8]
      - text: "128 points by user 3 hours ago"
- contentinfo:
  - textbox [ref=e10]
    /placeholder: "Search"
```

### Interpreting ARIA Notation

| Notation | Meaning |
|----------|---------|
| `[ref=eN]` | Stable identifier for interactive elements |
| `[checked]` | Checkbox/radio is selected |
| `[disabled]` | Element is inactive |
| `[expanded]` | Accordion/dropdown is open |
| `[level=N]` | Heading hierarchy (1-6) |
| `/url:` | Link destination |
| `/placeholder:` | Input placeholder text |
| `/value:` | Current input value |

### Interact by Ref

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
Use `select-ref.js` to interact with elements by their ref:

```bash
# Click element with ref e5
node select-ref.js --ref e5 --action click

# Fill input with ref e10
node select-ref.js --ref e10 --action fill --value "search query"

# Get text content
node select-ref.js --ref e8 --action text

# Screenshot specific element
node select-ref.js --ref e1 --action screenshot --output ./logo.png

# Focus element
node select-ref.js --ref e10 --action focus

# Hover over element
node select-ref.js --ref e5 --action hover
```

### Store Snapshots

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
Store snapshots for analysis in `<project>/.claude/chrome-devtools/snapshots/`:

```bash
# Create snapshots directory
mkdir -p .claude/chrome-devtools/snapshots

# Capture and store with timestamp
SESSION="$(date +%Y%m%d-%H%M%S)"
node aria-snapshot.js --url https://example.com --output .claude/chrome-devtools/snapshots/$SESSION.yaml
```

### Workflow: Unknown Page Structure

1. **Get snapshot** to discover elements:
   ```bash
   node aria-snapshot.js --url https://example.com
   ```

2. **Identify target** from YAML output (e.g., `[ref=e5]` for a button)

3. **Interact by ref**:
   ```bash
   node select-ref.js --ref e5 --action click
   ```

4. **Verify result** with screenshot or new snapshot:
   ```bash
   node screenshot.js --output ./result.png
   ```

## Local HTML Files

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
**IMPORTANT**: Never browse local HTML files via `file://` protocol. Always serve via local server:
**Why**: `file://` protocol blocks many browser features (CORS, ES modules, fetch API, service workers). Local server ensures proper HTTP behavior.

```bash
# Option 1: npx serve (recommended)
npx serve ./dist -p 3000 &
node navigate.js --url http://localhost:3000

# Option 2: Python http.server
python -m http.server 3000 --directory ./dist &
node navigate.js --url http://localhost:3000
```

**Note**: when port 3000 is busy, find an available port with `lsof -i :3000` and use a different one.

## Quick Start

```bash
# Install dependencies
cd .claude/skills/chrome-devtools/scripts
npm install  # Installs puppeteer, sharp, debug, yargs

# Test (browser stays running for session reuse)
node navigate.js --url https://example.com
# Output: {"success": true, "url": "...", "title": "..."}
```

**Linux/WSL only**: Run `./install-deps.sh` first for Chrome system libraries.

## Session Persistence

Browser state persists across script executions via WebSocket endpoint file (`.browser-session.json`).

**Default behavior**: Scripts disconnect but keep browser running for session reuse.

```bash
# First script: launches browser, navigates, disconnects (browser stays running)
node navigate.js --url https://example.com/login

# Subsequent scripts: connect to existing browser, reuse page state
node fill.js --selector "#email" --value "user@example.com"
node fill.js --selector "#password" --value "secret"
node click.js --selector "button[type=submit]"

# Close browser when done
node navigate.js --url about:blank --close true
```

**Session management**:
- `--close true`: Close browser and clear session
- Default (no flag): Keep browser running for next script

## Available Scripts

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
All in `.claude/skills/chrome-devtools/scripts/`:

| Script | Purpose |
|--------|---------|
| `navigate.js` | Navigate to URLs |
| `screenshot.js` | Capture screenshots (auto-compress >5MB via Sharp) |
| `click.js` | Click elements |
| `fill.js` | Fill form fields |
| `evaluate.js` | Execute JS in page context |
| `snapshot.js` | Extract interactive elements (JSON format) |
| `aria-snapshot.js` | Get ARIA accessibility tree (YAML format with refs) |
| `select-ref.js` | Interact with elements by ref from ARIA snapshot |
| `console.js` | Monitor console messages/errors |
| `network.js` | Track HTTP requests/responses |
| `performance.js` | Measure Core Web Vitals |

## Workflow Loop

1. **Execute** focused script for single task
2. **Observe** JSON output
3. **Assess** completion status
4. **Decide** next action
5. **Repeat** until done

## Writing Custom Test Scripts

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
For complex automation, write scripts to `<project>/.claude/chrome-devtools/tmp/`:

```bash
# Create tmp directory for test scripts
mkdir -p $SKILL_DIR/.claude/chrome-devtools/tmp

# Write a test script
cat > $SKILL_DIR/.claude/chrome-devtools/tmp/login-test.js << 'EOF'
import { getBrowser, getPage, disconnectBrowser, outputJSON } from '../scripts/lib/browser.js';

async function loginTest() {
  const browser = await getBrowser();
  const page = await getPage(browser);

  await page.goto('https://example.com/login');
  await page.type('#email', 'user@example.com');
  await page.type('#password', 'secret');
  await page.click('button[type=submit]');
  await page.waitForNavigation();

  outputJSON({
    success: true,
    url: page.url(),
    title: await page.title()
  });

  await disconnectBrowser();
}

loginTest();
EOF

# Run the test
node $SKILL_DIR/.claude/chrome-devtools/tmp/login-test.js
```

**Key principles for custom scripts**:
- Single-purpose: one script, one task
- Always call `disconnectBrowser()` at the end (keeps browser running)
- Use `closeBrowser()` only when ending session completely
- Output JSON for easy parsing
- Plain JavaScript only in `page.evaluate()` callbacks

## Screenshots

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
Store screenshots for analysis in `<project>/.claude/chrome-devtools/screenshots/`:

```bash
# Basic screenshot
node screenshot.js --url https://example.com --output ./.claude/chrome-devtools/screenshots/page.png

# Full page
node screenshot.js --url https://example.com --output ./.claude/chrome-devtools/screenshots/page.png --full-page true

# Specific element
node screenshot.js --url https://example.com --selector ".main-content" --output ./.claude/chrome-devtools/screenshots/element.png
```

### Auto-Compression (Sharp)

Screenshots >5MB auto-compress using Sharp (4-5x faster than ImageMagick):

```bash
# Default: compress if >5MB
node screenshot.js --url https://example.com --output ./.claude/chrome-devtools/screenshots/page.png

# Custom threshold (3MB)
node screenshot.js --url https://example.com --output ./.claude/chrome-devtools/screenshots/page.png --max-size 3

# Disable compression
node screenshot.js --url https://example.com --output ./.claude/chrome-devtools/screenshots/page.png --no-compress
```

Store screenshots for analysis in `<project>/.claude/chrome-devtools/screenshots/`.

## Console Log Collection & Analysis

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

### Capture Logs

```bash
# Capture all logs for 10 seconds
node console.js --url https://example.com --duration 10000

# Filter by type
node console.js --url https://example.com --types error,warn --duration 5000
```

### Session Storage Pattern

Store logs for analysis in `<project>/.claude/chrome-devtools/logs/<session>/`:

```bash
# Create session directory
SESSION="$(date +%Y%m%d-%H%M%S)"
mkdir -p .claude/chrome-devtools/logs/$SESSION

# Capture and store
node console.js --url https://example.com --duration 10000 > .claude/chrome-devtools/logs/$SESSION/console.json
node network.js --url https://example.com > .claude/chrome-devtools/logs/$SESSION/network.json

# View errors
jq '.messages[] | select(.type=="error")' .claude/chrome-devtools/logs/$SESSION/console.json
```

### Root Cause Analysis

```bash
# 1. Check for JavaScript errors
node console.js --url https://example.com --types error,pageerror --duration 5000 | jq '.messages'

# 2. Correlate with network failures
node network.js --url https://example.com | jq '.requests[] | select(.response.status >= 400)'

# 3. Check specific error stack traces
node console.js --url https://example.com --types error --duration 5000 | jq '.messages[].stack'
```

## Finding Elements

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
Use `snapshot.js` to discover selectors before interacting:

```bash
# Get all interactive elements
node snapshot.js --url https://example.com | jq '.elements[] | {tagName, text, selector}'

# Find buttons
node snapshot.js --url https://example.com | jq '.elements[] | select(.tagName=="button")'

# Find by text content
node snapshot.js --url https://example.com | jq '.elements[] | select(.text | contains("Submit"))'
```

## Error Recovery

Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.
If script fails:

```bash
# 1. Capture current state (without navigating to preserve state)
node screenshot.js --output ./.claude/skills/chrome-devtools/screenshots/debug.png

# 2. Get console errors
node console.js --url about:blank --types error --duration 1000

# 3. Discover correct selector
node snapshot.js | jq '.elements[] | select(.text | contains("Submit"))'

# 4. Try XPath if CSS fails
node click.js --selector "//button[contains(text(),'Submit')]"
```

## Common Patterns

### Web Scraping
```bash
node evaluate.js --url https://example.com --script "
  Array.from(document.querySelectorAll('.item')).map(el => ({
    title: el.querySelector('h2')?.textContent,
    link: el.querySelector('a')?.href
  }))
" | jq '.result'
```

### Form Automation
```bash
node navigate.js --url https://example.com/form
node fill.js --selector "#search" --value "query"
node click.js --selector "button[type=submit]"
```

### Performance Testing
```bash
node performance.js --url https://example.com | jq '.vitals'
```

## Script Options

All scripts support:
- `--headless false` - Show browser window
- `--close true` - Close browser completely (default: stay running)
- `--timeout 30000` - Set timeout (ms)
- `--wait-until networkidle2` - Wait strategy
Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

## Troubleshooting
Skills can exist in **project-scope** or **user-scope**. Priority: project-scope > user-scope.

| Error | Solution |
|-------|----------|
| `Cannot find package 'puppeteer'` | Run `npm install` in scripts directory |
| `libnss3.so` missing (Linux) | Run `./install-deps.sh` |
| Element not found | Use `snapshot.js` to find correct selector |
| Script hangs | Use `--timeout 60000` or `--wait-until load` |
| Screenshot >5MB | Auto-compressed; use `--max-size 3` for lower |
| Session stale | Delete `.browser-session.json` and retry |

### Screenshot Analysis: Missing Images

If images don't appear in screenshots, they may be waiting for animation triggers:

1. **Scroll-triggered animations**: Scroll element into view first
   ```bash
   node evaluate.js --script "document.querySelector('.lazy-image').scrollIntoView()"
   # Wait for animation
   node evaluate.js --script "await new Promise(r => setTimeout(r, 1000))"
   node screenshot.js --output ./result.png
   ```

2. **Sequential animation queue**: Wait longer and retry
   ```bash
   # First attempt
   node screenshot.js --url http://localhost:3000 --output ./attempt1.png

   # Wait for animations to complete
   node evaluate.js --script "await new Promise(r => setTimeout(r, 2000))"

   # Retry screenshot
   node screenshot.js --output ./attempt2.png
   ```

3. **Intersection Observer animations**: Trigger by scrolling through page
   ```bash
   node evaluate.js --script "window.scrollTo(0, document.body.scrollHeight)"
   node evaluate.js --script "await new Promise(r => setTimeout(r, 1500))"
   node evaluate.js --script "window.scrollTo(0, 0)"
   node screenshot.js --output ./full-loaded.png --full-page true
   ```

## Reference Documentation

- `./references/cdp-domains.md` - Chrome DevTools Protocol domains
- `./references/puppeteer-reference.md` - Puppeteer API patterns
- `./references/performance-guide.md` - Core Web Vitals optimization
- `./scripts/README.md` - Detailed script options
