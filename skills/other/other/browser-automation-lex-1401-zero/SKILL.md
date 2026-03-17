---
name: Browser Automation
description: Automate browser interactions using Playwright or Puppeteer
---

# Browser Automation Tool

This skill leverages the system's ability to run Playwright/Puppeteer scripts for web scraping, testing, and automation.

## Actions

### Run Playwright Script

Execute a Node.js script that uses Playwright.

```bash
node <script_path>
```

### Install Browsers

Ensure Playwright browsers are installed.

```bash
npx playwright install
```

## Example Script Structure

```javascript
import { chromium } from 'playwright';

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('https://example.com');
  // ... automation logic ...
  await browser.close();
})();
```
