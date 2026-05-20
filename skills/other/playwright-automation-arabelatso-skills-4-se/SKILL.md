---
name: playwright-automation
description: Browser automation via Playwright for web testing, screenshots, form filling, scraping, and verification. Use when tasks require navigating websites, interacting with web pages, or testing web applications.
---

# Playwright Automation

Browser automation skill using Playwright for web testing, verification, data extraction, and interactive workflows. Maintains persistent page state across script executions.

## When to Use This Skill

- Testing web applications (navigation, forms, assertions)
- Taking screenshots for visual verification
- Scraping web content or extracting data
- Automating browser workflows (login, form submission)
- Verifying UI changes after code modifications

## Approach Selection

- **Local/source-available sites**: Read source code first to write selectors directly
- **Unknown page layouts**: Use accessibility snapshots to discover elements
- **Visual feedback**: Take screenshots to see what the user sees

## Core Workflow

Write small, focused scripts — each does ONE thing:

```typescript
import { chromium } from "playwright";

const browser = await chromium.launch();
const page = await browser.newPage();

// Navigate
await page.goto("https://example.com");

// Wait for page to be ready
await page.waitForLoadState("networkidle");

// Interact
await page.fill('input[name="email"]', "user@example.com");
await page.click('button[type="submit"]');

// Verify
await page.waitForURL("**/dashboard");
const title = await page.title();
console.log({ title, url: page.url() });

// Screenshot
await page.screenshot({ path: "screenshot.png" });

await browser.close();
```

## Key Patterns

### Element Discovery with Accessibility Snapshots

```typescript
// Get accessibility tree to find interactive elements
const snapshot = await page.accessibility.snapshot();
console.log(JSON.stringify(snapshot, null, 2));
```

### Waiting Strategies

```typescript
await page.waitForLoadState("networkidle");     // Network idle
await page.waitForSelector(".results");          // Specific element
await page.waitForURL("**/success");             // URL pattern
await page.waitForFunction(() => window.ready);  // JS condition
```

### Form Interaction

```typescript
await page.fill('input[name="email"]', "user@example.com");
await page.fill('input[name="password"]', "secret");
await page.click('button[type="submit"]');
await page.waitForNavigation();
```

### Screenshots and PDFs

```typescript
await page.screenshot({ path: "page.png" });
await page.screenshot({ path: "full.png", fullPage: true });
await page.pdf({ path: "output.pdf" });
```

### Network Interception

```typescript
await page.route("**/api/**", (route) => {
  route.fulfill({ status: 200, body: JSON.stringify({ mock: true }) });
});
```

### Device Emulation

```typescript
const { devices } = require("playwright");
const iPhone = devices["iPhone 14"];
const context = await browser.newContext({ ...iPhone });
```

## Workflow Loop

For complex tasks, follow this pattern:

1. **Write a script** to perform one action
2. **Run it** and observe the output
3. **Evaluate** — did it work? What's the current state?
4. **Decide** — task complete or need another script?
5. **Repeat** until done

## Tips

- Use `networkidle` wait state after navigation for reliable page loads
- Prefer semantic selectors (`role`, `text`, `label`) over CSS selectors
- Take screenshots at key steps for debugging
- Use `page.evaluate()` for browser-context JavaScript (plain JS only, no TypeScript)
- For scraping large datasets, intercept network requests rather than scrolling DOM

**Inspired by:** [oh-my-opencode](https://github.com/code-yeongyu/oh-my-opencode) dev-browser skill
