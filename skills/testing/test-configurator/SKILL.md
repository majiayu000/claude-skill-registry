---
description: Test INAV Configurator with remote debugging and Chrome DevTools Protocol
triggers:
  - test configurator
  - debug configurator
  - configurator testing
  - test inav configurator ui
---

# Test Configurator Skill

Use this skill to test the INAV Configurator using Chrome DevTools Protocol remote debugging.

## Prerequisites

The configurator must be running with remote debugging enabled. This happens automatically in development mode.

## Quick Start

### 1. Start Configurator

```bash
cd inav-configurator
npm start
```

Remote debugging is **automatically enabled** in development mode (port 9222).

### 2. Verify Connection

```bash
# Check if CDP endpoint is accessible
curl -s http://localhost:9222/json/version

# List available pages
curl -s http://localhost:9222/json/list | jq '.'

# Find the INAV Configurator page ID
curl -s http://localhost:9222/json/list | jq -r '.[] | select(.title == "INAV Configurator") | .id'
```

Expected output: JSON response with Chrome version info and page list.

## Testing Methods

### Method 1: Chrome DevTools UI (Interactive)

Best for: Manual exploration, debugging, setting breakpoints

```bash
# Open Chrome browser and navigate to:
chrome://inspect

# Look for "INAV Configurator" under Remote Target
# Click "inspect" to open DevTools

# In DevTools console, you can run:
document.title                                    # Get page title
document.querySelector('#tab-configuration')      # Find elements
window.innerWidth + 'x' + window.innerHeight      # Window size
```

### Method 2: Playwright CDP (Automated)

Best for: Writing automated tests, PR validation

```javascript
const { chromium } = require('playwright');

// Connect to running configurator
const browser = await chromium.connectOverCDP('http://localhost:9222');
const contexts = browser.contexts();
const page = contexts[0].pages().find(p => p.url().includes('localhost:5174'));

// Test actions
await page.screenshot({ path: 'configurator.png' });
await page.click('#tab-configuration');
const title = await page.title();
console.log('Title:', title);

await browser.close();
```

### Method 3: curl + CDP Commands (Quick Tests)

Best for: Quick validation, CI/CD checks

```bash
# Get page ID
PAGE_ID=$(curl -s http://localhost:9222/json/list | jq -r '.[] | select(.title == "INAV Configurator") | .id')

# Connect via WebSocket and send CDP commands
# (Requires wscat, websocat, or Python websocket client)
```

### Method 4: Chrome DevTools MCP (Claude-Assisted)

Best for: AI-assisted testing, interactive exploration

**Status:** ✅ Verified working (tested 2025-12-18)

**See also:** `claude/developer/docs/testing/chrome-devtools-mcp.md` for detailed MCP usage guide

The Chrome DevTools MCP server provides direct integration with Claude Code for automated testing and UI interaction.

**Capabilities verified:**
- `mcp__chrome-devtools__list_pages` - List open browser pages
- `mcp__chrome-devtools__take_snapshot` - Capture accessibility tree (PREFERRED)
- `mcp__chrome-devtools__click` - Click UI elements (see caveat below)
- `mcp__chrome-devtools__fill` - Fill form inputs
- `mcp__chrome-devtools__navigate_page` - Navigate to URLs
- `mcp__chrome-devtools__evaluate_script` - Run JavaScript
- `mcp__chrome-devtools__take_screenshot` - Capture visual screenshots (rarely needed)

**⚠️ CRITICAL: Connect Button Requires JavaScript**

The Connect/Disconnect button does NOT work with `mcp__chrome-devtools__click`. Always use `evaluate_script`:

```javascript
// ✅ CORRECT way to connect:
mcp__chrome-devtools__evaluate_script({
  function: `() => {
    const connectLink = document.querySelector('a.connect');
    if (connectLink) {
      connectLink.click();
      return { clicked: true };
    }
    return { clicked: false };
  }`
})

// Then wait for connection:
mcp__chrome-devtools__wait_for({
  text: "Disconnect",
  timeout: 8000
})
```

See `claude/developer/docs/testing/chrome-devtools-mcp.md` for complete details and examples.

**IMPORTANT: Prefer Snapshots over Screenshots**

The Configurator's HTML is well-structured with clear IDs and semantic markup. Snapshots provide all necessary information without the overhead of visual rendering.

**Example HTML clarity:**
```html
<div id="port-picker">
    <div class="connect_controls" id="connectbutton">
        <div class="connect_b">
            <a class="connect" href="#"></a>
        </div>
        <a class="connect_state" data-i18n="connect"></a>
    </div>
```
This is clearly the connect button - no screenshot needed.

**When to use each:**
- **Snapshot (90% of cases)**: Element existence, UI state, form values, tab navigation
- **Screenshot (10% of cases)**: Visual layout bugs, CSS issues, alignment problems

**Example Usage:**

You can ask Claude:
- "Take a snapshot of the configurator" - Get UI element tree (PREFERRED)
- "What tabs are visible?" - List navigation elements
- "Check if the I2C speed input exists" - Verify specific elements
- "Click the Configuration tab and tell me what you see" - Interactive testing
- "Fill the port selector with /dev/ttyACM0" - Automated form filling
- "Take a screenshot" - Only for visual/CSS validation

**Activation:**
- MCP is activated when Chrome DevTools MCP server is configured in Claude settings
- If MCP tools aren't available, start a new Claude session with configurator running
- Configurator must be running (`npm start`) for tools to work

## Common Testing Tasks

### Test I2C Speed Warning Bug

```bash
# Via Chrome DevTools console
document.querySelector('input[name="i2cspeed"]').value = '800';
document.querySelector('.i2c-speed-warning')?.style.display || 'none';
```

### Verify Battery Current Limiter

```bash
# Check if field exists
document.querySelector('input[name="max_battery_current"]') ? 'Found' : 'Not found';
```

### Get All Navigation Tabs

```bash
# In Chrome DevTools console
Array.from(document.querySelectorAll('[id^="tab-"]')).map(t => t.id);
```

### Take Screenshot

```bash
# Via Chrome DevTools: Cmd/Ctrl + Shift + P → "Capture screenshot"
# Or use Playwright (see Method 2 above)
```

## Troubleshooting

### Port 9222 Not Listening

```bash
# Check if configurator is running
ps aux | grep electron

# Check port status
ss -tln | grep 9222

# Restart configurator
cd inav-configurator && npm start
```

### Connection Refused

```bash
# Verify CDP endpoint
curl http://localhost:9222/json/version

# If it fails, check:
# 1. Configurator is running (npm start)
# 2. Remote debugging code is in js/main/main.js (lines 39-47)
# 3. Not running production build (npm run package enables different mode)
```

### No Pages Found

```bash
# List all pages
curl -s http://localhost:9222/json/list

# Wait 2-3 seconds after launch for pages to appear
# Or restart configurator
```

### MCP Not Working

MCP requires a new Claude session to load:
1. Stop configurator
2. Exit Claude (Ctrl+D)
3. Start new Claude session in `inav-configurator` directory
4. Start configurator: `npm start`
5. MCP tools should now be available

## Code Location

Remote debugging is enabled in:
```
inav-configurator/js/main/main.js (lines 39-47)
```

Automatically enabled when `!app.isPackaged` (development mode).

## Documentation

**Full guides in:** `claude/developer/docs/`
- `TESTING-QUICKSTART.md` - Overview of all methods
- `configurator-automated-testing.md` - Playwright guide
- `configurator-debugging-setup.md` - CDP setup details
- `TESTING-VERIFIED-WORKING.md` - Verification results

**Helper scripts:**
- `inav-configurator/start-with-debugging.sh`
- `claude/developer/helpers/test-configurator-startup.js`

## Example Workflows

### Before Creating PR

```bash
cd inav-configurator
npm start

# In another terminal:
# 1. Open chrome://inspect
# 2. Test your changes manually
# 3. Take screenshots for PR description
# 4. Verify no JavaScript errors in console
```

### Write Automated Test

```bash
cd inav-configurator
npm start

# Create test file
cat > tests/my-feature.spec.js << 'EOF'
const { chromium } = require('playwright');

test('my feature works', async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const page = browser.contexts()[0].pages()[0];

  // Test your feature
  await page.click('#my-button');
  const result = await page.textContent('#result');
  expect(result).toBe('Expected text');

  await browser.close();
});
EOF

# Run test
node tests/my-feature.spec.js
```

### Debug a Bug Report

```bash
cd inav-configurator
npm start

# Open chrome://inspect
# Reproduce bug while monitoring:
# - Console for JavaScript errors
# - Network tab for failed requests
# - Elements tab for DOM issues
# Take screenshot of bug for documentation
```

## Related Skills

- **build-inav-target** - Build firmware for hardware testing
- **flash-firmware-dfu** - Flash firmware to flight controller
- **run-configurator** - Launch configurator in development mode
- **git-workflow** - Create branches for fixes
- **create-pr** - Create pull request after testing

## Notes

- Remote debugging is **automatically enabled** in development mode
- Port 9222 is the standard CDP port
- Production builds have debugging **disabled** for security
- Multiple test methods available (pick based on use case)
- Documentation is comprehensive and verified working

---

**Status:** ✅ Verified working (2025-12-18)
**CDP Endpoint:** http://localhost:9222
**Configurator Version:** 9.0.0
**Electron Version:** 38.7.2
