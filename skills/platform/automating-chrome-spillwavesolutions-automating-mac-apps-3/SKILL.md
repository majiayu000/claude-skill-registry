---
name: automating-chrome
description: Automates Google Chrome and Chromium-based browsers via JXA with AppleScript dictionary discovery. Use when asked to "automate Chrome tabs", "control browser with JXA", "Chrome AppleScript automation", "Chromium browser scripting", or "browser tab management". Covers windows, tabs, execute(), tunneling patterns, and permissions.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Chrome / Chromium Browsers (JXA-first, AppleScript discovery)

## Technology Status

JXA/AppleScript browser automation is legacy. JavaScript injection is disabled by default in modern Chrome. Modern alternatives: Selenium/ChromeDriver, Puppeteer, PyXA.

**Related Skills**: `web-browser-automation`, `automating-mac-apps`

**PyXA Installation:** See `automating-mac-apps` skill (PyXA Installation section).

## Contents
- [Scope](#scope)
- [Core framing](#core-framing)
- [Workflow (default)](#workflow-default)
- [Quick Examples](#quick-examples)
- [Modern Alternatives](#modern-alternatives)
- [What to load](#what-to-load)

## Scope
- Primary target: Google Chrome (bundle ID: com.google.Chrome).
- Chromium-based variants (Brave: com.brave.Browser, Edge: com.microsoft.edgemac, Arc: company.thebrowser.Browser) often expose similar dictionaries but may differ by bundle name and permissions.
- Always verify dictionary availability in Script Editor for target browser before automation.

**Security Note**: JavaScript injection via AppleScript is disabled by default in Chrome. Enable via: View → Developer → Allow JavaScript from Apple Events (not recommended for production use).

## Core framing
- AppleScript dictionaries define the automation surface.
- JXA provides logic and data handling.
- `execute()` runs JavaScript in page context but doesn't reliably return values—use tunneling patterns (save to clipboard/localStorage) for data extraction instead.

**⚠️ Security Warning**: The tunneling approach (clipboard/localStorage) can expose sensitive data. Use modern APIs for production automation.
- **Tunneling Patterns Explained:** Since `execute()` doesn't return JavaScript results directly, work around this by having your injected script save data to accessible locations like the system clipboard (`navigator.clipboard.writeText()`) or localStorage (`localStorage.setItem()`). Then retrieve the data in your JXA script using system commands or by reading back from localStorage via another `execute()` call.

## Workflow (default)
1) Discover dictionary terms in Script Editor (Chrome or target browser).
2) Prototype minimal AppleScript commands in target browser.
3) Port to JXA and add defensive checks:
   - Wrap operations in try/catch blocks
   - Check browser process status: `chrome.running()`
   - Verify window/tab indices exist before access
   - Handle permission dialogs programmatically when possible
4) Use batch URL reads and reverse-order deletes for tab operations.
5) Use tunneling patterns for DOM data extraction.
6) Validate results: Log tab counts, URLs, or extracted data to confirm operations succeeded.

## Quick Examples

**Open new tab and navigate:**
```javascript
const chrome = Application('Google Chrome');
chrome.windows[0].tabs.push(chrome.Tab());
chrome.windows[0].tabs[chrome.windows[0].tabs.length - 1].url = 'https://example.com';
```

**Execute JavaScript in current tab:**
```javascript
const result = chrome.execute({javascript: 'document.title'});
// Note: execute() runs JS but doesn't reliably return values
```

**Batch close tabs (reverse order):**
```javascript
const tabs = chrome.windows[0].tabs;
for (let i = tabs.length - 1; i >= 0; i--) {
  if (tabs[i].url().includes('unwanted')) {
    tabs[i].close();
  }
}
```

**Extract page data via tunneling:**
```javascript
// Inject script to save title to localStorage
chrome.execute({javascript: 'localStorage.setItem("pageTitle", document.title)'});
// Retrieve via another execute call
chrome.execute({javascript: 'console.log(localStorage.getItem("pageTitle"))'});
```

**Check browser permissions:**
```javascript
try {
  const chrome = Application('Google Chrome');
  chrome.windows[0].tabs[0].url(); // Test access
  console.log('Permissions OK');
} catch (error) {
  console.log('Permission error:', error.message);
}
```

## Modern Alternatives

For production Chrome automation, see the `web-browser-automation` skill for comprehensive guides covering:

- **PyXA**: macOS-native Chrome automation with full integration
- **Selenium**: Cross-platform automation with automatic ChromeDriver management
- **Puppeteer**: Node.js automation with bundled Chrome
- **Multi-browser workflows**: Chrome, Edge, Brave, and Arc coordination

**Quick PyXA Example** (see web-browser-automation skill for details):
```python
import PyXA

# Launch Chrome and navigate
chrome = PyXA.Application("Google Chrome")
chrome.activate()
chrome.open_location("https://example.com")

# Get current tab info
current_tab = chrome.current_tab()
print(f"Page title: {current_tab.title()}")
print(f"Current URL: {current_tab.url()}")
```

### PyObjC with Selenium (Cross-Platform with macOS Integration)
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from AppKit import NSWorkspace

# Configure Chrome options
options = Options()
options.add_argument("--remote-debugging-port=9222")
options.add_argument('--headless=new')  # Modern headless mode

# Launch Chrome with Selenium (automatic ChromeDriver management)
driver = webdriver.Chrome(options=options)
driver.get('https://example.com')

# macOS integration via PyObjC
workspace = NSWorkspace.sharedWorkspace()
frontmost_app = workspace.frontmostApplication()
print(f"Frontmost app: {frontmost_app.localizedName()}")

print(f"Page title: {driver.title}")
driver.quit()
```

### Selenium with ChromeDriver (Recommended for Cross-Platform)
```bash
# Install Selenium (latest: 4.38.0)
pip install selenium

# ChromeDriver is automatically managed by Selenium Manager (v4.11+)
# No manual download needed - compatible version downloaded automatically

# Basic Python example
from selenium import webdriver

driver = webdriver.Chrome()  # Automatic ChromeDriver management
driver.get('https://example.com')
print(driver.title)
driver.quit()
```

**Advanced Configuration:**
```python
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless=new')  # Modern headless mode (required)
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.get('https://example.com')
print(f"Page title: {driver.title}")
driver.quit()
```

**Manual ChromeDriver Setup (for specific versions):**
```python
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Download from https://googlechromelabs.github.io/chromedriver/
# Match major version with your Chrome installation
service = Service(executable_path='/path/to/chromedriver')
options = Options()
driver = webdriver.Chrome(service=service, options=options)
```

**Note**: Selenium 4.11+ automatically downloads compatible ChromeDriver. Manual setup only needed for specific version requirements or CI/CD environments.

### Puppeteer (Recommended for Node.js)
```bash
# Install Puppeteer (latest: 24.35.0)
npm install puppeteer
# Bundles compatible Chrome automatically
```

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new'  // Modern headless mode (required in v24+)
  });
  const page = await browser.newPage();
  await page.goto('https://example.com');
  const title = await page.title();
  console.log(title);
  await browser.close();
})();
```

**Advanced Puppeteer Configuration:**
```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage();

  // Set viewport
  await page.setViewport({ width: 1280, height: 720 });

  await page.goto('https://example.com');

  // Wait for element and interact
  await page.waitForSelector('h1');
  const title = await page.title();

  console.log(`Page title: ${title}`);
  await browser.close();
})();
```

### Chrome DevTools Protocol (Advanced)
```javascript
// WebSocket connection to CDP
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:9222/devtools/page/{page-id}');

// Send CDP commands
ws.send(JSON.stringify({
  id: 1,
  method: 'Runtime.evaluate',
  params: { expression: 'document.title' }
}));
```

**Setup Requirements**:
- ChromeDriver: Download from [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
- Puppeteer: `npm install puppeteer`
- CDP: Launch Chrome with `--remote-debugging-port=9222`

## Validation Checklist
- [ ] Browser automation permissions granted (System Settings > Privacy & Security)
- [ ] Chrome running and accessible: `chrome.running()` returns true
- [ ] JavaScript injection enabled (View > Developer > Allow JavaScript from Apple Events)
- [ ] Tab/window indices verified before access
- [ ] Error handling wraps all operations
- [ ] Data extraction via tunneling confirmed
- [ ] Results logged and validated

## When Not to Use
- Cross-platform browser automation (use Selenium or Playwright)
- Production web scraping or testing (use ChromeDriver/Puppeteer)
- JavaScript injection disabled (default in modern Chrome)
- Non-macOS platforms
- Heavy DOM manipulation (use Puppeteer/Playwright)

## What to load
- Chrome JXA basics: `automating-chrome/references/chrome-basics.md`
- Recipes (tabs, URLs, windows): `automating-chrome/references/chrome-recipes.md`
- Advanced patterns (execute tunneling, incognito): `automating-chrome/references/chrome-advanced.md`
- Dictionary translation table: `automating-chrome/references/chrome-dictionary.md`
- Browser name mapping: `automating-chrome/references/chromium-browser-names.md`
- Form automation basics: `automating-chrome/references/chrome-form-automation.md`

**Related Skills for Modern Chrome Automation**:
- `web-browser-automation`: Complete guide for Chrome, Edge, Brave, and Arc automation
- `automating-mac-apps`: PyXA fundamentals and conversion guides