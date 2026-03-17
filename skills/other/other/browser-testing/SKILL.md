---
name: browser-testing
description: Browser automation for testing IntelliFill. Replaces puppeteer MCP to save ~4.8k tokens.
---

# Browser Testing

This skill covers browser automation for IntelliFill testing. It lazy-loads on demand instead of consuming context upfront like MCP servers.

## When I Need This

- Testing form filling in Chrome
- Capturing screenshots for docs
- Debugging UI issues visually
- Automating upload/download flows

## Quick Setup

Start Chrome with remote debugging first:
```bash
start chrome --remote-debugging-port=9222 --user-data-dir="N:/IntelliFill/quikadmin/chrome-debug-profile"
```

## Core Patterns

### Connect to Running Chrome
```typescript
const browser = await puppeteer.connect({ browserURL: 'http://localhost:9222' });
const page = await browser.newPage();
```

### Navigate and Interact
```typescript
await page.goto('http://localhost:8080/login');
await page.type('[name="email"]', 'test@example.com');
await page.type('[name="password"]', 'password123');
await page.click('[type="submit"]');
await page.waitForNavigation();
```

### Screenshot
```typescript
await page.screenshot({ path: 'output.png', fullPage: true });
```

### File Upload (IntelliFill document flow)
```typescript
const [chooser] = await Promise.all([
  page.waitForFileChooser(),
  page.click('#upload-button')
]);
await chooser.accept(['./test-files/sample.pdf']);
await page.waitForSelector('.upload-complete');
```

## IntelliFill URLs

| Page | URL |
|------|-----|
| Login | http://localhost:8080/login |
| Dashboard | http://localhost:8080/dashboard |
| Documents | http://localhost:8080/documents |
| Upload | http://localhost:8080/documents/upload |

## Prefer Cypress/Playwright

For proper E2E tests, use the **e2e-testing** skill instead - it has full test infrastructure. This skill is for quick manual browser automation when you need direct Puppeteer control.
