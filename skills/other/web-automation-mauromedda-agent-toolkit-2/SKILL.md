---
name: web-automation
description: >-
  Web automation, debugging, and E2E testing with Playwright. Handles interactive
  (login, forms, reproduce bugs) and passive modes (network/console capture).
  Triggers on "e2e test", "browser test", "playwright", "screenshot", "debug UI",
  "debug frontend", "reproduce bug", "network trace", "console output", "verify fix",
  "test that", "verify change", "test the flow", "http://localhost", "open browser",
  "click button", "fill form", "submit form", "check page", "web scraping",
  "automation script", "headless browser", "browser automation", "selenium alternative",
  "puppeteer alternative", "page object", "web testing", "UI testing", "frontend testing",
  "visual regression", "capture network", "intercept requests", "mock API responses".
  PROACTIVE: Invoke for security verification, UI fix verification, testing forms/dropdowns,
  or multi-step UI flows. ON SESSION RESUME - check for pending UI verifications.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Claude Code skill for web automation, debugging, and E2E testing using Playwright
# ABOUTME: Covers interactive automation, passive monitoring, screenshots, and security verification

# Web Automation with Playwright

Browser automation and debugging using Playwright in **Python** or **JavaScript/TypeScript**.

**Detailed patterns**: See `references/python-patterns.md` and `references/javascript-patterns.md`

---

## Quick Reference

| Task | Helper Script |
|------|---------------|
| Login / fill forms | `examples/python/form_interaction.py` |
| Take screenshots | `examples/python/screenshot_capture.py` |
| Handle cookie consent | `scripts/cookie_consent.py` |
| Discover page elements | `examples/python/element_discovery.py` |
| Capture network traffic | `scripts/network_inspector.py` |
| Debug console errors | `scripts/console_debugger.py` |
| Full debug (network+console) | `scripts/combined_debugger.py` |
| Compare websites visually | `examples/python/visual_compare.py` |

**Always run helpers first**:
```bash
uv run ~/.claude/skills/web-automation/examples/python/element_discovery.py http://localhost:3000
uv run ~/.claude/skills/web-automation/examples/python/screenshot_capture.py http://localhost:3000 --output /tmp/shots
```

---

## Modes of Operation

| Mode | When to Use | Example |
|------|-------------|---------|
| **Interactive** | Click, type, navigate | Login flow, form submission |
| **Passive** | Observe only | Network capture, console monitoring |
| **E2E Testing** | Automated test suites | Playwright Test framework |

---

## When to Invoke (Proactive)

1. **Verifying UI fixes** - After changing frontend code
2. **Testing form fields/dropdowns** - Verify correct values display
3. **Confirming visual changes** - Take screenshots
4. **Reproducing bugs** - Automate steps to reproduce
5. **Security verification** - After Gemini/static analysis finds issues

---

## 🔄 RESUMED SESSION CHECKPOINT

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - WEB AUTOMATION VERIFICATION              │
│                                                             │
│  1. Was I in the middle of browser automation?              │
│     → Run: ps aux | grep -E "chromium|playwright|node"      │
│                                                             │
│  2. Were there UI verification tasks pending?               │
│     → Check summary for "verify", "test UI", "screenshot"   │
│                                                             │
│  3. Did previous automation capture any findings?           │
│     → Check /tmp/ for screenshots, debug outputs            │
└─────────────────────────────────────────────────────────────┘
```

---

## Decision Flow

```
Task:
    +-- Need to interact? (click, type, submit) → Interactive mode
    +-- Just observe/capture? → Passive mode (combined_debugger.py)
    +-- Security verification? → Passive mode + grep for sensitive patterns
```

---

## CRITICAL: Handling Overlays

**Overlays WILL block automation.** Always dismiss after `page.goto()`:

### Python (Quick Pattern)
```python
page.goto('https://example.com')
page.wait_for_load_state('networkidle')

# Dismiss cookie consent
for sel in ['button:has-text("Accept all")', '[class*="cookie"] button[class*="accept"]']:
    try:
        btn = page.locator(sel).first
        if btn.is_visible(timeout=2000):
            btn.click()
            break
    except:
        continue
```

### Nuclear Option (Remove All Overlays)
```python
page.evaluate('''() => {
    const patterns = ['cookie', 'consent', 'modal', 'overlay', 'popup', 'backdrop'];
    for (const p of patterns) {
        document.querySelectorAll(`[class*="${p}"], [id*="${p}"]`).forEach(el => {
            if (getComputedStyle(el).position === 'fixed') el.remove();
        });
    }
    document.body.style.overflow = 'auto';
}''')
```

**Full implementation**: See `references/python-patterns.md`

---

## Core Patterns

### Python
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')  # CRITICAL
    # ... automation
    browser.close()
```

### JavaScript
```javascript
import { test, expect } from '@playwright/test';

test('example', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await expect(page.locator('.element')).toBeVisible();
});
```

---

## Common Operations

| Operation | Python | JavaScript |
|-----------|--------|------------|
| Screenshot | `page.screenshot(path='/tmp/s.png')` | `await page.screenshot({ path: '/tmp/s.png' })` |
| Full page | `page.screenshot(path='/tmp/s.png', full_page=True)` | `await page.screenshot({ path: '/tmp/s.png', fullPage: true })` |
| Fill input | `page.fill('input[name="email"]', 'x@y.com')` | `await page.fill('input[name="email"]', 'x@y.com')` |
| Select dropdown | `page.select_option('select#id', 'value')` | `await page.selectOption('select#id', 'value')` |
| Click | `page.click('button[type="submit"]')` | `await page.click('button[type="submit"]')` |
| Wait network | `page.wait_for_load_state('networkidle')` | `await page.waitForLoadState('networkidle')` |
| Wait element | `page.wait_for_selector('.result')` | `await page.waitForSelector('.result')` |

---

## Selector Strategies (Order of Preference)

1. **Role-based**: `page.get_by_role('button', name='Submit')`
2. **Text-based**: `page.get_by_text('Click me')`
3. **Test IDs**: `page.get_by_test_id('submit-btn')`
4. **CSS**: `page.locator('.btn-primary')`
5. **XPath** (last resort): `page.locator('//button[@type="submit"]')`

---

## Verification Checklist

| What to Verify | Approach |
|----------------|----------|
| Dropdown value | `page.locator('select').input_value()` |
| Input text | `page.locator('input').input_value()` |
| Element visible | `page.locator('.element').is_visible()` |
| Text content | `page.locator('.element').text_content()` |
| Page URL | `page.url` after action |

---

## Passive Debugging Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `combined_debugger.py` | Network + Console + Errors | `uv run ... --duration 30 --output /tmp/debug.json` |
| `network_inspector.py` | Network only | `uv run ... --errors-only` |
| `console_debugger.py` | Console/errors only | `uv run ... --with-stack-traces` |

### Security Verification
```bash
# After Gemini found sensitive data logging
uv run ~/.claude/skills/web-automation/scripts/console_debugger.py \
    http://localhost:3000 --duration 60 --output /tmp/security.json

grep -i "password\|token\|secret\|bearer" /tmp/security.json
```

---

## Visual Comparison

**NEVER say "I cannot visually browse"**. Instead:

```bash
# Compare two sites
uv run ~/.claude/skills/web-automation/examples/python/visual_compare.py \
    https://reference-site.com \
    http://localhost:3000 \
    --output /tmp/compare

# Then read the screenshots using Read tool
```

---

## Language Selection

| Use Case | Recommended | Reason |
|----------|-------------|--------|
| Existing JS/TS project | JavaScript | Consistent tooling |
| Existing Python project | Python | Consistent tooling |
| Quick scripts | Python | Simpler setup with `uv run` |
| Test suites | JavaScript | Better `@playwright/test` framework |

---

## Test Framework Integration

See `references/test-framework.md` for:
- Unified test runner (`test_utils.py`)
- Server auto-detection and startup
- Framework detection (Playwright, Jest, pytest, etc.)

```bash
# Detect and run tests with server
uv run ~/.claude/skills/web-automation/scripts/test_utils.py . --run --with-server
```

---

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Overlay blocking clicks | Call overlay dismissal after EVERY page load |
| DOM inspection before JS loads | Always `wait_for_load_state('networkidle')` first |
| Headful browser in CI | Always use `headless: true` |
| Flaky selectors | Prefer role/text selectors over CSS classes |
| Race conditions | Use explicit waits, not `wait_for_timeout` |

---

## Prerequisites

### Python
Scripts include inline dependencies (PEP 723); `uv run` auto-installs them.

### JavaScript
```bash
npm init -y
npm install -D @playwright/test
npx playwright install chromium
```

---

## Running E2E Tests

### JavaScript
```bash
npx playwright test                    # Run all
npx playwright test --ui               # UI mode
npx playwright test --headed           # See browser
```

### Python
```bash
pip install pytest-playwright
pytest tests/
```
