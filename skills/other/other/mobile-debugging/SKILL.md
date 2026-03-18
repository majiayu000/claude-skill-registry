---
name: mobile-debugging
description: Remote JavaScript console access and debugging on mobile devices. Use when debugging web pages on phones/tablets, accessing console errors without desktop DevTools, testing responsive designs on real devices, or diagnosing mobile-specific issues. Covers Eruda, vConsole, Chrome/Safari remote debugging, and cloud testing platforms.
---

# Mobile debugging methodology

Patterns for accessing JavaScript console and debugging web pages on mobile devices without traditional desktop DevTools.

## Quick-start: Inject console on any page

### Eruda bookmarklet (recommended)

Add this as a bookmark on your mobile browser, then tap it on any page:

```javascript
javascript:(function(){var script=document.createElement('script');script.src='https://cdn.jsdelivr.net/npm/eruda';document.body.append(script);script.onload=function(){eruda.init();}})();
```

### vConsole bookmarklet

```javascript
javascript:(function(){var script=document.createElement('script');script.src='https://unpkg.com/vconsole@latest/dist/vconsole.min.js';document.body.append(script);script.onload=function(){new VConsole();}})();
```

## In-page console tools

### Eruda setup

Eruda provides a full DevTools-like experience in a floating panel.

```html
<!-- CDN (development only) -->
<script src="https://cdn.jsdelivr.net/npm/eruda"></script>
<script>eruda.init();</script>

<!-- Conditional loading (recommended for production) -->
<script>
(function() {
    var src = 'https://cdn.jsdelivr.net/npm/eruda';
    // Only load when ?eruda=true or localStorage flag set
    if (!/eruda=true/.test(window.location) &&
        localStorage.getItem('active-eruda') !== 'true') return;

    var script = document.createElement('script');
    script.src = src;
    script.onload = function() { eruda.init(); };
    document.body.appendChild(script);
})();
</script>
```

```javascript
// NPM installation
// npm install eruda --save-dev

import eruda from 'eruda';

// Initialize with options
eruda.init({
    container: document.getElementById('eruda-container'),
    tool: ['console', 'elements', 'network', 'resources', 'info'],
    useShadowDom: true,
    autoScale: true
});

// Add custom buttons
eruda.add({
    name: 'Clear Storage',
    init($el) {
        $el.html('<button>Clear All Storage</button>');
        $el.find('button').on('click', () => {
            localStorage.clear();
            sessionStorage.clear();
            console.log('Storage cleared');
        });
    }
});

// Remove when done
eruda.destroy();
```

**Eruda features:**
- Console (logs, errors, warnings)
- Elements (DOM inspector)
- Network (XHR/fetch requests)
- Resources (localStorage, cookies, sessionStorage)
- Sources (page source code)
- Info (page/device information)
- Snippets (saved code snippets)

### vConsole setup

Lighter weight alternative, official tool for WeChat debugging.

```html
<!-- CDN -->
<script src="https://unpkg.com/vconsole@latest/dist/vconsole.min.js"></script>
<script>
var vConsole = new VConsole();
</script>
```

```javascript
// NPM
// npm install vconsole

import VConsole from 'vconsole';

// Initialize with options
const vConsole = new VConsole({
    theme: 'dark',
    onReady: function() {
        console.log('vConsole is ready');
    },
    log: {
        maxLogNumber: 1000
    }
});

// Dynamic configuration
vConsole.setOption('log.maxLogNumber', 5000);

// Destroy when done
vConsole.destroy();
```

**vConsole features:**
- Log panel (console.log, info, warn, error)
- System panel (device info)
- Network panel (XHR, fetch)
- Element panel (DOM tree)
- Storage panel (cookies, localStorage)

### Comparison: Eruda vs vConsole

| Feature | Eruda | vConsole |
|---------|-------|----------|
| Size | ~100KB | ~85KB |
| DOM Editing | Yes | View only |
| Network Details | Full | Basic |
| Plugin System | Yes | Yes |
| Dark Theme | Via plugin | Built-in |
| Best For | Full debugging | Quick logging |

## Native remote debugging

### Chrome DevTools (Android)

```bash
# 1. Enable USB debugging on Android
#    Settings → Developer Options → USB Debugging = ON

# 2. Connect via USB to computer

# 3. Open Chrome on computer, navigate to:
#    chrome://inspect#devices

# 4. Enable "Discover USB devices"

# 5. Accept debugging prompt on Android device

# 6. Click "Inspect" next to the page you want to debug
```

**Port forwarding for localhost:**
```bash
# In chrome://inspect, click "Port forwarding"
# Add: localhost:3000 → localhost:3000
# Now Android Chrome can access your dev server at localhost:3000
```

### Safari Web Inspector (iOS)

```bash
# 1. On iPhone/iPad:
#    Settings → Safari → Advanced → Web Inspector = ON

# 2. On Mac:
#    Safari → Preferences → Advanced → "Show Develop menu" = ON

# 3. Connect device via USB (or enable Wi-Fi debugging)

# 4. Open Safari on Mac:
#    Develop → [Device Name] → [Page to debug]

# Wireless debugging (after initial USB setup):
#    Develop → [Device] → Connect via Network
```

### Firefox Remote Debugging (Android)

```bash
# 1. On Android Firefox:
#    Settings → Advanced → Remote debugging = ON

# 2. On Desktop Firefox:
#    Open about:debugging

# 3. Connect Android via USB

# 4. Enable USB devices in about:debugging

# 5. Click "Connect" next to your device
```

## iOS debugging without Mac

### Using ios-webkit-debug-proxy

```bash
# Install on Windows (via Scoop)
scoop bucket add extras
scoop install ios-webkit-debug-proxy

# Install on Linux
sudo apt-get install ios-webkit-debug-proxy

# Install on Mac
brew install ios-webkit-debug-proxy

# Run the proxy
ios_webkit_debug_proxy -f chrome-devtools://devtools/bundled/inspector.html

# Connect to http://localhost:9221 to see connected devices
```

### Commercial: Inspect.dev

Inspect.dev provides iOS debugging from Windows/Linux with a familiar DevTools interface.

```bash
# Download from https://inspect.dev/
# 1. Install application
# 2. Connect iOS device via USB
# 3. Enable Web Inspector on iOS
# 4. Inspect.dev auto-detects pages
# 5. Click to open DevTools interface
```

## Cloud testing platforms

### LambdaTest (freemium)

```python
# LambdaTest provides real device cloud with console access
# Free tier: 100 minutes/month

import requests

# LambdaTest REST API for automation
LAMBDATEST_API = "https://api.lambdatest.com/automation/api/v1"

# For manual testing:
# 1. Go to https://www.lambdatest.com/
# 2. Select device/browser
# 3. Enter URL
# 4. DevTools available in toolbar

# Selenium/Playwright integration for automated console capture
from playwright.sync_api import sync_playwright

def test_on_lambdatest():
    with sync_playwright() as p:
        # Connect to LambdaTest
        browser = p.chromium.connect(
            f"wss://cdp.lambdatest.com/playwright?capabilities="
            f"{{\"browserName\":\"Chrome\",\"platform\":\"android\"}}"
        )
        page = browser.new_page()

        # Capture console logs
        logs = []
        page.on('console', lambda msg: logs.append(msg.text()))

        page.goto('https://example.com')
        browser.close()

        return logs
```

### BrowserStack

```python
# BrowserStack: $29/month+, 10,000+ real devices

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def get_browserstack_driver():
    """Create BrowserStack WebDriver with console logging."""

    capabilities = {
        'browserName': 'chrome',
        'device': 'Samsung Galaxy S21',
        'realMobile': 'true',
        'os_version': '11.0',
        'browserstack.console': 'verbose',  # Capture console logs
        'browserstack.networkLogs': 'true',
        'browserstack.user': 'YOUR_USERNAME',
        'browserstack.key': 'YOUR_KEY'
    }

    driver = webdriver.Remote(
        command_executor='https://hub-cloud.browserstack.com/wd/hub',
        desired_capabilities=capabilities
    )

    return driver

# After test, retrieve logs from BrowserStack dashboard or API
```

## Programmatic console capture

### Playwright console capture

```javascript
const { chromium, devices } = require('playwright');

async function captureConsoleLogs(url) {
    const browser = await chromium.launch();

    // Emulate mobile device
    const context = await browser.newContext({
        ...devices['iPhone 13']
    });

    const page = await context.newPage();

    // Capture all console messages
    const logs = [];
    page.on('console', msg => {
        logs.push({
            type: msg.type(),
            text: msg.text(),
            location: msg.location(),
            timestamp: new Date().toISOString()
        });
    });

    // Capture page errors
    const errors = [];
    page.on('pageerror', error => {
        errors.push({
            message: error.message,
            stack: error.stack,
            timestamp: new Date().toISOString()
        });
    });

    // Capture failed requests
    const failedRequests = [];
    page.on('requestfailed', request => {
        failedRequests.push({
            url: request.url(),
            failure: request.failure().errorText,
            timestamp: new Date().toISOString()
        });
    });

    await page.goto(url);
    await page.waitForLoadState('networkidle');

    await browser.close();

    return { logs, errors, failedRequests };
}

// Usage
captureConsoleLogs('https://example.com')
    .then(result => console.log(JSON.stringify(result, null, 2)));
```

### Puppeteer console capture

```javascript
const puppeteer = require('puppeteer');

async function debugMobilePage(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Set mobile viewport
    await page.setViewport({
        width: 375,
        height: 812,
        isMobile: true,
        hasTouch: true
    });

    // Mobile user agent
    await page.setUserAgent(
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) ' +
        'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    );

    // Console capture with full details
    page.on('console', async msg => {
        const args = await Promise.all(
            msg.args().map(arg => arg.jsonValue().catch(() => arg.toString()))
        );

        console.log(`[${msg.type().toUpperCase()}]`, ...args);

        // Get source location
        const location = msg.location();
        if (location.url) {
            console.log(`  at ${location.url}:${location.lineNumber}`);
        }
    });

    // Unhandled promise rejections
    page.on('pageerror', err => {
        console.error('[PAGE ERROR]', err.message);
    });

    await page.goto(url, { waitUntil: 'networkidle0' });

    // Execute JavaScript and capture result
    const result = await page.evaluate(() => {
        // Check for common mobile issues
        return {
            viewportWidth: window.innerWidth,
            devicePixelRatio: window.devicePixelRatio,
            touchSupport: 'ontouchstart' in window,
            errors: window.__capturedErrors || []
        };
    });

    console.log('Page info:', result);

    await browser.close();
}
```

## Error monitoring services

### Sentry integration

```javascript
// npm install @sentry/browser

import * as Sentry from '@sentry/browser';

Sentry.init({
    dsn: 'YOUR_SENTRY_DSN',
    environment: 'production',

    // Capture console.error
    integrations: [
        new Sentry.BrowserTracing(),
        new Sentry.Replay()  // Session replay for debugging
    ],

    // Sample rates
    tracesSampleRate: 0.1,
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,

    beforeSend(event) {
        // Filter or modify events
        return event;
    }
});

// Manual error capture
try {
    riskyOperation();
} catch (error) {
    Sentry.captureException(error);
}

// Add context
Sentry.setUser({ id: 'user123' });
Sentry.setTag('page', 'checkout');
```

### LogRocket for session replay

```javascript
// npm install logrocket

import LogRocket from 'logrocket';

LogRocket.init('your-app/your-project');

// Identify user
LogRocket.identify('user123', {
    name: 'Test User',
    email: 'user@example.com'
});

// Console logs automatically captured
console.log('This appears in LogRocket');

// Manual logging
LogRocket.log('Custom event', { data: 'value' });

// Track errors
LogRocket.captureException(new Error('Something went wrong'));
```

## Android screen mirroring with Scrcpy

```bash
# Install scrcpy
# Windows: scoop install scrcpy
# Mac: brew install scrcpy
# Linux: apt install scrcpy

# Basic mirroring
scrcpy

# With specific options
scrcpy --max-size 1024 --bit-rate 2M

# Wireless connection (after initial USB)
adb tcpip 5555
adb connect <device-ip>:5555
scrcpy

# Record session
scrcpy --record session.mp4

# Turn off device screen while mirroring
scrcpy --turn-screen-off
```

## Mobile debugging workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                  MOBILE DEBUGGING DECISION TREE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Q: Do you have physical access to the device?                  │
│      │                                                           │
│      ├─ YES: Can you connect via USB?                           │
│      │   │                                                       │
│      │   ├─ Android: Use Chrome DevTools Remote                 │
│      │   │           chrome://inspect#devices                    │
│      │   │                                                       │
│      │   └─ iOS: Have a Mac?                                    │
│      │       │                                                   │
│      │       ├─ YES: Use Safari Web Inspector                   │
│      │       │                                                   │
│      │       └─ NO: Use Inspect.dev or                          │
│      │              ios-webkit-debug-proxy                       │
│      │                                                           │
│      └─ NO USB: Inject Eruda/vConsole via bookmarklet           │
│                                                                  │
│  Q: Remote/production debugging?                                │
│      │                                                           │
│      ├─ Add conditional Eruda loading                           │
│      │  (?eruda=true parameter)                                 │
│      │                                                           │
│      └─ Set up Sentry/LogRocket for error monitoring            │
│                                                                  │
│  Q: Automated testing?                                          │
│      │                                                           │
│      ├─ Playwright/Puppeteer with mobile emulation              │
│      │                                                           │
│      └─ Cloud platforms (LambdaTest, BrowserStack)              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Common mobile debugging issues

### Touch events not firing

```javascript
// Check if touch events are supported
eruda.init();
console.log('Touch support:', 'ontouchstart' in window);
console.log('Pointer events:', 'onpointerdown' in window);

// Debug touch events
document.addEventListener('touchstart', e => {
    console.log('touchstart', e.touches.length, 'touches');
}, { passive: true });

document.addEventListener('click', e => {
    console.log('click at', e.clientX, e.clientY);
});
```

### Viewport issues

```javascript
// Log viewport information
console.log('Viewport:', {
    innerWidth: window.innerWidth,
    innerHeight: window.innerHeight,
    outerWidth: window.outerWidth,
    outerHeight: window.outerHeight,
    devicePixelRatio: window.devicePixelRatio,
    orientation: screen.orientation?.type
});

// Check meta viewport
const viewport = document.querySelector('meta[name="viewport"]');
console.log('Viewport meta:', viewport?.content);
```

### Performance debugging

```javascript
// Check performance timing
const perf = performance.getEntriesByType('navigation')[0];
console.log('Page load timing:', {
    dns: perf.domainLookupEnd - perf.domainLookupStart,
    tcp: perf.connectEnd - perf.connectStart,
    request: perf.responseStart - perf.requestStart,
    response: perf.responseEnd - perf.responseStart,
    domParsing: perf.domInteractive - perf.responseEnd,
    domComplete: perf.domComplete - perf.domInteractive,
    total: perf.loadEventEnd - perf.navigationStart
});

// Check memory (Chrome only)
if (performance.memory) {
    console.log('Memory:', {
        usedJSHeapSize: (performance.memory.usedJSHeapSize / 1048576).toFixed(2) + ' MB',
        totalJSHeapSize: (performance.memory.totalJSHeapSize / 1048576).toFixed(2) + ' MB'
    });
}
```

## Platform comparison

| Tool | Cost | Platforms | Setup Difficulty | Best For |
|------|------|-----------|------------------|----------|
| **Eruda** | Free | All browsers | Easy (bookmarklet) | Quick debugging |
| **vConsole** | Free | All browsers | Easy | WeChat apps |
| **Chrome Remote** | Free | Android only | Medium | Full DevTools |
| **Safari Inspector** | Free | iOS only | Easy (Mac required) | Full DevTools |
| **Inspect.dev** | Paid | iOS from any OS | Easy | iOS without Mac |
| **LambdaTest** | Freemium | All | Easy | Cloud testing |
| **BrowserStack** | Paid | All | Easy | Real devices |
| **Sentry** | Freemium | All | Medium | Error monitoring |
