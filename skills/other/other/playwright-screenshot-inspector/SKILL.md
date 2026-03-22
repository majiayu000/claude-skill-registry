---
name: playwright-screenshot-inspector
description: LLM-powered visual testing expert for automated screenshot capture, analysis, and UI verification using Playwright with multimodal AI inspection.
metadata:
  category: Testing
  tags:
  - playwright
  - visual-testing
  - screenshots
  - ui-verification
  - automation
  pairs-with:
  - skill: playwright-e2e-tester
    reason: Visual regression testing extends E2E test suites with screenshot comparison
  - skill: webapp-testing
    reason: Screenshot inspection automates the visual verification that interactive testing does manually
  - skill: color-contrast-auditor
    reason: Automated screenshot analysis can detect contrast violations across UI states
---

# Playwright Screenshot Inspector

LLM-powered visual testing expert for automated screenshot capture, analysis, and UI verification using Playwright with multimodal AI inspection.

## Activation Triggers

**Activate on:**
- "screenshot test", "visual test", "screenshot inspection"
- "playwright headless", "playwright screenshot"
- "UI verification", "visual regression"
- "theme compliance test", "dark mode test", "light mode test"
- "automated screenshot", "capture and analyze"
- "compare screenshots", "visual diff"

**NOT for:**
- Simple one-off screenshots (use browser DevTools)
- Pixel-perfect comparison without AI (use native Playwright `toHaveScreenshot`)
- Non-web UI testing (use platform-specific tools)
- Performance testing (use Lighthouse/WebPageTest)

---

## Core Philosophy

Traditional visual testing compares pixels. **LLM-powered visual testing understands semantics.**

Instead of "these 50 pixels changed", LLM inspection answers:
- "Is the content actually rendered?"
- "Does the theme switch correctly?"
- "Are interactive elements visible and properly styled?"
- "What's broken vs. what's just different?"

---

## The Screenshot Inspection Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM SCREENSHOT INSPECTION                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CAPTURE (Playwright)                                    │
│     └─► Wait for React hydration, not just network          │
│                                                             │
│  2. READ (Claude vision)                                    │
│     └─► Pass screenshot to LLM with specific questions      │
│                                                             │
│  3. ANALYZE (Structured response)                           │
│     └─► Extract: content present? theme correct? errors?    │
│                                                             │
│  4. ACT (Conditional logic)                                 │
│     └─► Pass/fail based on semantic understanding           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Critical: Waiting for React Content

**The #1 failure mode**: Taking screenshots before React hydrates.

### Anti-Pattern: Network Idle Alone
```python
# ❌ WRONG - React may not have rendered yet
page.goto(url)
page.wait_for_load_state('networkidle')
page.screenshot(path='broken.png')  # Often blank!
```

### Correct Pattern: Wait for Actual Content
```python
# ✅ CORRECT - Wait for React to mount
page.goto(url, wait_until='domcontentloaded')
page.wait_for_load_state('networkidle')

# Give React time to hydrate
import time
time.sleep(0.5)

# Wait for actual content selector
page.wait_for_selector('.main-content, h1, [data-testid="app"]',
                       state='visible',
                       timeout=10000)

# Verify content exists
body_text = page.locator('body').inner_text()
if len(body_text) < 50:
    time.sleep(2)  # Extra wait for slow hydration

page.screenshot(path='good.png', full_page=True)
```

### Content Verification Function
```python
def wait_for_react_content(page, selectors, timeout=10000):
    """Wait for React to hydrate by checking for actual content."""
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_load_state('networkidle')
    time.sleep(0.5)  # React hydration buffer

    for selector in selectors.split(','):
        try:
            locator = page.locator(selector.strip())
            if locator.count() > 0:
                locator.first.wait_for(state='visible', timeout=timeout)
                return True
        except:
            continue

    # Fallback: wait for substantial body content
    try:
        page.wait_for_function(
            'document.body.innerText.length > 100',
            timeout=timeout
        )
        return True
    except:
        return False
```

---

## Headless Mode: Preventing Window Spam

**Always use `headless=True`** to prevent browser windows from spawning:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # CRITICAL: headless=True prevents visible browser windows
    browser = p.chromium.launch(headless=True)

    context = browser.new_context(
        viewport={'width': 1280, 'height': 800},
        color_scheme='dark'  # Initial theme
    )
    page = context.new_page()

    # ... your test logic ...

    browser.close()  # Always clean up
```

### Theme Testing Pattern
```python
# Dark mode screenshot
page.emulate_media(color_scheme='dark')  # Note: on PAGE, not context
page.goto(url)
wait_for_react_content(page, '.app-container, main, h1')
page.screenshot(path='dark.png', full_page=True)

# Light mode screenshot
page.emulate_media(color_scheme='light')
page.reload()
wait_for_react_content(page, '.app-container, main, h1')
page.screenshot(path='light.png', full_page=True)
```

---

## LLM Screenshot Analysis Patterns

### Pattern 1: Content Verification
```
Prompt: "Analyze this screenshot. Answer:
1. Is the main content rendered (not blank/loading)?
2. What major UI elements are visible?
3. Are there any error states or broken layouts?
4. Rate content completeness: FULL / PARTIAL / EMPTY"
```

### Pattern 2: Theme Compliance
```
Prompt: "This is a {dark/light} mode screenshot. Verify:
1. Background color matches expected theme (dark bg for dark mode)
2. Text has sufficient contrast against background
3. Interactive elements are visible and styled correctly
4. No theme leakage (dark elements on light bg or vice versa)"
```

### Pattern 3: Comparison Analysis
```
Prompt: "Compare these two screenshots (before/after). Identify:
1. What changed between them?
2. Are changes intentional (theme switch) or bugs?
3. Is any content missing in the 'after' version?
4. Rate similarity: IDENTICAL / MINOR_DIFF / MAJOR_DIFF / BROKEN"
```

### Pattern 4: Accessibility Check
```
Prompt: "Evaluate this screenshot for visual accessibility:
1. Is text readable (sufficient size and contrast)?
2. Are interactive elements clearly identifiable?
3. Is there visual hierarchy (headings, sections)?
4. Any elements that would fail WCAG contrast requirements?"
```

---

## Complete Test Script Template

```python
#!/usr/bin/env python3
"""
LLM-Powered Screenshot Test Suite
Captures screenshots and uses Claude vision for semantic analysis.
"""

from playwright.sync_api import sync_playwright
import os
import time

PAGES_TO_TEST = [
    # (path, name, content_selectors)
    ('/', 'Home', '.hero, main, h1'),
    ('/about', 'About', '.about-content, main, h1'),
    ('/dashboard', 'Dashboard', '.dashboard, .stats, h1'),
]

BASE_URL = 'http://localhost:5173'
SCREENSHOT_DIR = '/tmp/visual-tests'


def wait_for_content(page, selectors, timeout=10000):
    """Wait for React/Vue/Svelte to hydrate."""
    page.wait_for_load_state('domcontentloaded')
    page.wait_for_load_state('networkidle')
    time.sleep(0.5)

    for selector in selectors.split(','):
        try:
            loc = page.locator(selector.strip())
            if loc.count() > 0:
                loc.first.wait_for(state='visible', timeout=timeout)
                return True
        except:
            continue

    try:
        page.wait_for_function('document.body.innerText.length > 100', timeout=timeout)
        return True
    except:
        return False


def capture_themed_screenshots(page, url, name, selectors):
    """Capture both dark and light mode screenshots."""
    safe_name = name.lower().replace(' ', '-')
    results = {'name': name, 'url': url}

    for theme in ['dark', 'light']:
        page.emulate_media(color_scheme=theme)

        if theme == 'dark':
            page.goto(url, wait_until='domcontentloaded')
        else:
            page.reload(wait_until='domcontentloaded')

        content_loaded = wait_for_content(page, selectors)

        if not content_loaded:
            print(f"  ⚠️  {theme} mode: Content slow to load, waiting...")
            time.sleep(2)

        screenshot_path = f'{SCREENSHOT_DIR}/{safe_name}-{theme}.png'
        page.screenshot(path=screenshot_path, full_page=True)

        # Check content length
        body_text = page.locator('body').inner_text().strip()
        results[f'{theme}_screenshot'] = screenshot_path
        results[f'{theme}_content_length'] = len(body_text)
        results[f'{theme}_has_content'] = len(body_text) > 50

        print(f"  {theme}: {'✅' if results[f'{theme}_has_content'] else '❌'} ({len(body_text)} chars)")

    return results


def run_tests():
    """Run visual tests on all pages."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            color_scheme='dark'
        )
        page = context.new_page()

        # Capture console errors
        errors = []
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)

        results = []

        for path, name, selectors in PAGES_TO_TEST:
            print(f"Testing {name}...")
            url = f'{BASE_URL}{path}'
            result = capture_themed_screenshots(page, url, name, selectors)
            result['errors'] = list(errors)
            errors.clear()
            results.append(result)

        browser.close()

        # Summary
        print("\n" + "=" * 50)
        print("VISUAL TEST SUMMARY")
        print("=" * 50)

        passed = sum(1 for r in results
                     if r.get('dark_has_content') and r.get('light_has_content'))
        print(f"\nPassed: {passed}/{len(results)}")
        print(f"Screenshots: {SCREENSHOT_DIR}")

        return results


if __name__ == '__main__':
    run_tests()
```

---

## MCP vs Native Playwright Decision Tree

```
What are you doing?
│
├─ Interactive debugging / exploring
│  └─► Playwright MCP (see live browser)
│
├─ Automated test suite
│  └─► Native Python Playwright (headless)
│
├─ CI/CD pipeline
│  └─► Native Python Playwright (headless)
│
├─ Screenshot capture for LLM analysis
│  └─► Native Python Playwright (headless)
│
└─ One-off inspection
   └─► Either works, MCP is convenient
```

---

## Common Failures and Fixes

### Failure: Blank Screenshots
**Cause**: Screenshot taken before React hydrates
**Fix**: Wait for content selectors, add hydration buffer

### Failure: "Reconnecting..." Badge Visible
**Cause**: HMR/WebSocket not connected (cosmetic in tests)
**Fix**: This is often fine - focus on actual content

### Failure: Theme Not Applied
**Cause**: `emulate_media` called on context instead of page
**Fix**: Use `page.emulate_media(color_scheme='dark')`

### Failure: Browser Windows Spawning
**Cause**: `headless=False` or using MCP instead of native
**Fix**: Use `p.chromium.launch(headless=True)`

### Failure: Timeout on Content
**Cause**: Wrong selectors or page actually broken
**Fix**: Verify selectors exist, check console errors

---

## Integration with Claude Code

When Claude reads screenshots captured by this pattern:

1. **Request specific analysis**: Don't just show screenshot - ask targeted questions
2. **Provide context**: "This should be dark mode" or "This is the login page"
3. **Compare systematically**: Before/after, dark/light, desktop/mobile
4. **Trust semantic analysis**: LLM can tell "blank page" from "content loaded"

---

## References

### Research Papers
- [Using Vision LLMs For UI Testing](https://courses.cs.washington.edu/courses/cse503/25wi/final-reports/Using%20Vision%20LLMs%20For%20UI%20Testing.pdf) - University of Washington
- [Vision-driven Automated Mobile GUI Testing](https://arxiv.org/html/2407.03037v1) - Multimodal LLM approach
- [ScreenLLM: Stateful Screen Schema](https://arxiv.org/html/2503.20978v1) - UI understanding framework

### Tools & Integrations
- [Building an AI QA Engineer with Claude + Playwright](https://alexop.dev/posts/building_ai_qa_engineer_claude_code_playwright/)
- [AI-Powered Visual Testing in Playwright](https://testrig.medium.com/ai-powered-visual-testing-in-playwright-from-pixels-to-perception-dd3ee49911d5)
- [Playwright Visual Regression Testing Guide](https://testgrid.io/blog/playwright-visual-regression-testing/)

### Official Documentation
- [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)

---

## Version History

- **2026-01-23**: Initial skill creation
  - Researched multimodal LLM screenshot analysis best practices
  - Documented React hydration waiting patterns
  - Added headless mode requirements
  - Created complete test script template

---

**Core Insight**: The difference between useless and useful screenshot tests is waiting for content, not just network. LLMs can analyze semantics, but only if there's actually content to analyze.
