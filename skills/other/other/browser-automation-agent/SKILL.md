---
name: browser-automation-agent
description: Automate web browsers for AI agents using agent-browser CLI with deterministic element selection.
---

# Browser Automation with Agent-Browser

Agent-browser is a headless browser automation CLI designed specifically for AI agents. It provides fast browser control with deterministic element selection through accessibility tree snapshots, making it ideal for agent-driven web automation workflows.

## When to use

- Use case 1: When the user asks to automate web interactions (fill forms, click buttons, navigate sites)
- Use case 2: When you need to capture screenshots or generate PDFs of web pages
- Use case 3: For web scraping tasks that require JavaScript rendering or complex interactions
- Use case 4: When building automation workflows that need deterministic element references
- Use case 5: For testing web applications with agent-driven scenarios

## Required tools / APIs

- No external API required (runs locally)
- agent-browser: Headless browser CLI with Rust/Node.js implementation
- Chromium: Downloaded automatically during installation

Install options:

```bash
# via npm (global)
npm install -g agent-browser
agent-browser install  # Downloads Chromium

# via Homebrew (macOS/Linux)
brew install agent-browser

# Verify installation
agent-browser --version
```

## Skills

### browser_open_and_snapshot

Open a URL and capture the accessibility tree to identify interactive elements.

```bash
# Open a webpage
agent-browser open https://example.com

# Get snapshot with element references
agent-browser snapshot

# The snapshot shows elements with @e1, @e2 references
# Example output:
# @e1 button "Sign In"
# @e2 input "Email" (email)
# @e3 input "Password" (password)
```

**Node.js:**

```javascript
const { execSync } = require('child_process');

function browserCommand(cmd) {
  return execSync(`agent-browser ${cmd}`, { encoding: 'utf-8' });
}

async function openAndSnapshot(url) {
  browserCommand(`open ${url}`);
  await new Promise(r => setTimeout(r, 2000)); // Wait for page load
  const snapshot = browserCommand('snapshot');
  return snapshot; // Returns element tree with references
}

// Usage
// const elements = await openAndSnapshot('https://example.com');
// console.log(elements);
```

### browser_interact

Interact with page elements using deterministic references from snapshots.

```bash
# Fill a form field
agent-browser fill @e2 "user@example.com"
agent-browser fill @e3 "password123"

# Click a button
agent-browser click @e1

# Type text into active element
agent-browser type "search query" --enter

# Navigate
agent-browser back
agent-browser forward
agent-browser reload
```

**Node.js:**

```javascript
function fillForm(formData) {
  for (const [ref, value] of Object.entries(formData)) {
    execSync(`agent-browser fill ${ref} "${value}"`, { encoding: 'utf-8' });
  }
}

function clickElement(ref) {
  return execSync(`agent-browser click ${ref}`, { encoding: 'utf-8' });
}

// Usage
// fillForm({ '@e2': 'user@example.com', '@e3': 'password123' });
// clickElement('@e1');
```

### browser_capture

Capture screenshots, PDFs, or extract page content.

```bash
# Take a screenshot
agent-browser screenshot output.png

# Generate PDF
agent-browser pdf document.pdf

# Get page text content
agent-browser text

# Get HTML source
agent-browser html

# Get specific element attribute
agent-browser attribute @e5 href
```

**Node.js:**

```javascript
function captureScreenshot(filename) {
  return execSync(`agent-browser screenshot ${filename}`, { encoding: 'utf-8' });
}

function generatePDF(filename) {
  return execSync(`agent-browser pdf ${filename}`, { encoding: 'utf-8' });
}

function getPageText() {
  return execSync('agent-browser text', { encoding: 'utf-8' });
}

function getElementAttribute(ref, attr) {
  return execSync(`agent-browser attribute ${ref} ${attr}`, { encoding: 'utf-8' }).trim();
}

// Usage
// captureScreenshot('page.png');
// const text = getPageText();
// const link = getElementAttribute('@e10', 'href');
```

### browser_session_management

Manage browser sessions, tabs, and persistent state.

```bash
# Session management
agent-browser open https://example.com --session myapp
agent-browser close --session myapp

# Tab management
agent-browser open https://example.com --new-tab
agent-browser tabs list
agent-browser tabs switch 0

# Cookie and storage
agent-browser cookies get example.com
agent-browser storage set mykey "myvalue"
agent-browser storage get mykey

# Close browser
agent-browser close
```

**Node.js:**

```javascript
function openSession(url, sessionName) {
  return execSync(`agent-browser open ${url} --session ${sessionName}`, { encoding: 'utf-8' });
}

function closeSession(sessionName) {
  return execSync(`agent-browser close --session ${sessionName}`, { encoding: 'utf-8' });
}

function manageStorage(action, key, value = null) {
  const cmd = value
    ? `agent-browser storage ${action} ${key} "${value}"`
    : `agent-browser storage ${action} ${key}`;
  return execSync(cmd, { encoding: 'utf-8' }).trim();
}

// Usage
// openSession('https://app.example.com', 'shopping-session');
// manageStorage('set', 'cart-id', '12345');
// const cartId = manageStorage('get', 'cart-id');
```

## Rate limits / Best practices

- Add delays between interactions (1-2 seconds) to allow page rendering
- Use `--wait` flag for actions that trigger navigation or async updates
- Close browser sessions when done to free system resources
- Use `--session` flags to isolate different automation workflows
- Cache snapshots when repeatedly interacting with the same page structure
- Prefer element references (@e1) over selectors for deterministic behavior

## Agent prompt

```text
You have browser automation capability through agent-browser. When a user asks to automate web interactions:

1. Open the URL with `agent-browser open <url>`
2. Get the accessibility snapshot with `agent-browser snapshot` to identify interactive elements
3. Parse the snapshot output to find element references (like @e1, @e2)
4. Use `fill`, `click`, or `type` commands with element references to interact
5. Use `screenshot` or `pdf` to capture results when requested
6. Always close the browser session with `agent-browser close` when done

For multi-step workflows:
- Wait 1-2 seconds between actions for page updates
- Take snapshots after navigation to get updated element references
- Use sessions (`--session name`) to maintain state across multiple operations
- Extract page text or HTML to verify successful interactions

Always prefer agent-browser over other scraping tools when:
- JavaScript rendering is required
- User interactions (clicks, form fills) are needed
- You need screenshots or visual verification
```

## Troubleshooting

**Error: Chromium not installed:**
- Symptom: "Browser binary not found" error
- Solution: Run `agent-browser install` to download Chromium

**Error: Element reference not found (@e5):**
- Symptom: "Element not found" when using a reference
- Solution: Take a fresh snapshot after page navigation; element references change between pages

**Error: Timeout waiting for element:**
- Symptom: Commands hang or timeout
- Solution: Add explicit wait time with `--wait 5000` flag or use delays between commands

**Page not fully loaded:**
- Symptom: Snapshot shows incomplete page elements
- Solution: Add sleep/delay after opening URL before taking snapshot

**Session conflicts:**
- Symptom: "Session already exists" or unexpected state
- Solution: Close existing sessions with `agent-browser close --session <name>` before starting new ones

## See also

- [using-web-scraping.md](using-web-scraping.md) — HTML parsing and content extraction without browser
- [generate-report.md](generate-report.md) — Creating reports from scraped data
- [pdf-manipulation.md](pdf-manipulation.md) — Working with generated PDFs

---

## Additional Notes

### Advantages over traditional scraping
- Handles JavaScript-rendered content automatically
- Deterministic element selection through accessibility tree
- Screenshot and PDF generation built-in
- Persistent sessions and state management
- Designed for agent workflows with clear CLI interface

### Cloud integration (optional)
Agent-browser supports cloud browser providers:
- Browserbase: `agent-browser --provider browserbase`
- Browser Use: Enterprise browser automation
- Kernel: Distributed browser sessions

For most use cases, local installation is sufficient and avoids external dependencies.
