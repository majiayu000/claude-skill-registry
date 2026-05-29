---
name: browserless
description: Browserless cloud browser automation service. Run headless Chrome at scale for scraping, screenshots, and PDF generation. Use for cloud browser automation, scalable scraping, or headless Chrome as a service. Triggers on browserless, headless chrome, browser service, cloud scraping, screenshot api, pdf generation, chrome as a service.
---

# Browserless Cloud Browser Automation

Complete guide for Browserless - headless Chrome as a service.

## Quick Reference

### Key Features

| Feature | Description |
|---------|-------------|
| **REST API** | HTTP endpoints for screenshots, PDFs, scraping |
| **WebSocket** | Puppeteer/Playwright connection |
| **Screenshots** | Page captures at scale |
| **PDF** | Document generation |
| **Scraping** | Data extraction |
| **Functions** | Custom script execution |

### Endpoints

```
/screenshot - Capture screenshots
/pdf - Generate PDFs
/content - Get page HTML
/scrape - Extract data
/function - Run custom code
```

## Setup

### Self-Hosted (Docker)

```bash
docker run -d \
  -p 3000:3000 \
  -e "TOKEN=your-token" \
  -e "CONCURRENT=10" \
  -e "QUEUED=10" \
  --name browserless \
  ghcr.io/browserless/chromium
```

### Docker Compose

```yaml
services:
  browserless:
    image: ghcr.io/browserless/chromium
    ports:
      - "3000:3000"
    environment:
      - TOKEN=your-secure-token
      - CONCURRENT=10
      - QUEUED=50
      - TIMEOUT=60000
      - MAX_PAYLOAD_SIZE=5mb
      - HEALTH_CHECK=true
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 4G
```

### Cloud Service

```
Sign up at browserless.io
Get API token
Use: wss://chrome.browserless.io?token=YOUR_TOKEN
```

## REST API

### Screenshots

```bash
# Basic screenshot
curl -X POST "http://localhost:3000/screenshot?token=your-token" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  -o screenshot.png

# With options
curl -X POST "http://localhost:3000/screenshot?token=your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "fullPage": true,
      "type": "png",
      "quality": 80
    },
    "viewport": {
      "width": 1920,
      "height": 1080
    },
    "waitForSelector": "#content"
  }' \
  -o screenshot.png
```

### PDF Generation

```bash
curl -X POST "http://localhost:3000/pdf?token=your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "options": {
      "format": "A4",
      "printBackground": true,
      "margin": {
        "top": "1cm",
        "right": "1cm",
        "bottom": "1cm",
        "left": "1cm"
      }
    }
  }' \
  -o document.pdf
```

### Scrape Data

```bash
curl -X POST "http://localhost:3000/scrape?token=your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "elements": [
      {"selector": "h1", "name": "title"},
      {"selector": ".price", "name": "price"},
      {"selector": "img", "name": "images", "attr": "src"}
    ]
  }'
```

## JavaScript Integration

### Using Puppeteer

```javascript
const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.connect({
    browserWSEndpoint: "ws://localhost:3000?token=your-token",
  });

  const page = await browser.newPage();
  await page.goto("https://example.com");
  const title = await page.title();
  console.log("Title:", title);

  await browser.close();
})();
```

### Using Playwright

```javascript
const { chromium } = require("playwright");

(async () => {
  const browser = await chromium.connectOverCDP(
    "ws://localhost:3000?token=your-token"
  );

  const context = await browser.newContext();
  const page = await context.newPage();

  await page.goto("https://example.com");
  const title = await page.title();
  console.log("Title:", title);

  await browser.close();
})();
```

### REST API with Fetch

```javascript
async function takeScreenshot(url) {
  const response = await fetch(
    "http://localhost:3000/screenshot?token=your-token",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url,
        options: { fullPage: true },
      }),
    }
  );
  return Buffer.from(await response.arrayBuffer());
}

async function scrapeData(url, elements) {
  const response = await fetch(
    "http://localhost:3000/scrape?token=your-token",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, elements }),
    }
  );
  return await response.json();
}
```

## Python Integration

### Using Playwright

```python
from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp(
            'ws://localhost:3000?token=your-token'
        )
        page = await browser.new_page()
        await page.goto('https://example.com')
        title = await page.title()
        print(f'Title: {title}')
        await browser.close()

asyncio.run(main())
```

### REST API with Requests

```python
import requests

def screenshot(url, options=None):
    response = requests.post(
        'http://localhost:3000/screenshot',
        params={'token': 'your-token'},
        json={
            'url': url,
            'options': options or {'fullPage': True}
        }
    )
    return response.content

def scrape(url, elements):
    response = requests.post(
        'http://localhost:3000/scrape',
        params={'token': 'your-token'},
        json={'url': url, 'elements': elements}
    )
    return response.json()

# Usage
screenshot_data = screenshot('https://example.com')
with open('screenshot.png', 'wb') as f:
    f.write(screenshot_data)
```

## Function API

### Custom Functions

```javascript
// POST /function
{
  "code": `
    export default async ({ page }) => {
      await page.goto('https://example.com');
      await page.waitForSelector('.loaded');

      const data = await page.evaluate(() => {
        return {
          title: document.title,
          items: Array.from(document.querySelectorAll('.item'))
            .map(el => ({
              name: el.querySelector('.name').textContent,
              price: el.querySelector('.price').textContent
            }))
        };
      });

      return { data, type: 'application/json' };
    }
  `
}
```

## Advanced Options

### Viewport and Device

```json
{
  "url": "https://example.com",
  "viewport": {
    "width": 375,
    "height": 812,
    "deviceScaleFactor": 2,
    "isMobile": true,
    "hasTouch": true
  }
}
```

### Wait Conditions

```json
{
  "url": "https://example.com",
  "waitForSelector": "#content",
  "waitForTimeout": 2000,
  "waitForEvent": "networkidle0",
  "waitForFunction": "window.loaded === true"
}
```

### Authentication

```json
{
  "url": "https://example.com",
  "authenticate": {
    "username": "user",
    "password": "pass"
  },
  "cookies": [
    {
      "name": "session",
      "value": "abc123",
      "domain": "example.com"
    }
  ]
}
```

## Docker Configuration

### Full Configuration

```yaml
services:
  browserless:
    image: ghcr.io/browserless/chromium
    ports:
      - "3000:3000"
    environment:
      - TOKEN=your-secure-token
      - CONCURRENT=10
      - QUEUED=50
      - TIMEOUT=60000
      - CONNECTION_TIMEOUT=30000
      - MAX_PAYLOAD_SIZE=10mb
      - ENABLE_CORS=true
      - HEALTH_CHECK=true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 4G
```

## Monitoring

```bash
# Health check
curl http://localhost:3000/

# Queue stats
curl http://localhost:3000/stats

# Prometheus metrics
curl http://localhost:3000/metrics
```

## Best Practices

1. **Use tokens** - Secure your instance
2. **Set timeouts** - Prevent hanging sessions
3. **Limit concurrency** - Based on resources
4. **Close sessions** - Prevent memory leaks
5. **Use health checks** - Monitor availability
6. **Queue management** - Handle request bursts
7. **Retry logic** - Handle transient failures
8. **Resource limits** - Set Docker constraints
9. **Use functions** - For complex workflows
10. **Monitor metrics** - Track performance

## When to Use This Skill

- Cloud-based browser automation
- Scalable screenshot services
- PDF generation at scale
- Web scraping infrastructure
- Headless Chrome as a service
- Parallel browser operations
