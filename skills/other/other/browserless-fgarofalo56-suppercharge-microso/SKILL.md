---
name: browserless
description: "Browserless cloud browser automation service. Run headless Chrome at scale for scraping, screenshots, and PDF generation. Use for cloud browser automation, scalable scraping, or headless Chrome as a service."
---

# Browserless Skill

Complete guide for Browserless - headless Chrome as a service.

## Quick Reference

### Key Features

| Feature         | Description                     |
| --------------- | ------------------------------- |
| **REST API**    | HTTP endpoints                  |
| **WebSocket**   | Puppeteer/Playwright connection |
| **Screenshots** | Page captures                   |
| **PDF**         | Document generation             |
| **Scraping**    | Data extraction                 |
| **Functions**   | Custom scripts                  |

### Endpoints

```
/screenshot - Capture screenshots
/pdf - Generate PDFs
/content - Get page HTML
/scrape - Extract data
/function - Run custom code
```

---

## 1. Setup

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

---

## 2. REST API

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

### Get Content

```bash
# Get HTML
curl -X POST "http://localhost:3000/content?token=your-token" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}' \
  -o page.html
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

---

## 3. JavaScript Integration

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
    "ws://localhost:3000?token=your-token",
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
    },
  );

  const buffer = await response.arrayBuffer();
  return Buffer.from(buffer);
}

async function generatePDF(url) {
  const response = await fetch("http://localhost:3000/pdf?token=your-token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url,
      options: { format: "A4", printBackground: true },
    }),
  });

  return await response.arrayBuffer();
}

async function scrapeData(url, elements) {
  const response = await fetch(
    "http://localhost:3000/scrape?token=your-token",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, elements }),
    },
  );

  return await response.json();
}
```

---

## 4. Python Integration

### Using Pyppeteer

```python
import asyncio
from pyppeteer import connect

async def main():
    browser = await connect(
        browserWSEndpoint='ws://localhost:3000?token=your-token'
    )

    page = await browser.newPage()
    await page.goto('https://example.com')

    title = await page.title()
    print(f'Title: {title}')

    await browser.close()

asyncio.run(main())
```

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

def pdf(url, options=None):
    response = requests.post(
        'http://localhost:3000/pdf',
        params={'token': 'your-token'},
        json={
            'url': url,
            'options': options or {
                'format': 'A4',
                'printBackground': True
            }
        }
    )
    return response.content

def scrape(url, elements):
    response = requests.post(
        'http://localhost:3000/scrape',
        params={'token': 'your-token'},
        json={
            'url': url,
            'elements': elements
        }
    )
    return response.json()

# Usage
screenshot_data = screenshot('https://example.com')
with open('screenshot.png', 'wb') as f:
    f.write(screenshot_data)

data = scrape('https://example.com', [
    {'selector': 'h1', 'name': 'title'},
    {'selector': '.price', 'name': 'price'}
])
print(data)
```

---

## 5. Function API

### Custom Functions

```javascript
// POST /function
{
  "code": `
    export default async ({ page }) => {
      await page.goto('https://example.com');

      // Custom logic
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

### With Context

```javascript
{
  "code": `
    export default async ({ page, context }) => {
      const { url, searchTerm } = context;

      await page.goto(url);
      await page.type('#search', searchTerm);
      await page.click('#submit');
      await page.waitForNavigation();

      const results = await page.$$eval('.result', els =>
        els.map(el => el.textContent)
      );

      return { data: results, type: 'application/json' };
    }
  `,
  "context": {
    "url": "https://example.com",
    "searchTerm": "puppeteer"
  }
}
```

---

## 6. Advanced Options

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
  },
  "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
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

### JavaScript Injection

```json
{
  "url": "https://example.com",
  "addScriptTag": [
    { "content": "window.injected = true;" },
    { "url": "https://cdn.example.com/script.js" }
  ],
  "addStyleTag": [{ "content": "body { background: red; }" }]
}
```

---

## 7. Proxy Support

### Using Proxy

```json
{
  "url": "https://example.com",
  "launch": {
    "args": ["--proxy-server=http://proxy.example.com:8080"]
  }
}
```

### Authenticated Proxy

```javascript
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://localhost:3000?token=your-token",
});

const page = await browser.newPage();

await page.authenticate({
  username: "proxy-user",
  password: "proxy-pass",
});

await page.goto("https://example.com");
```

---

## 8. Docker Configuration

### Full Configuration

```yaml
services:
  browserless:
    image: ghcr.io/browserless/chromium
    ports:
      - "3000:3000"
    environment:
      # Authentication
      - TOKEN=your-secure-token

      # Concurrency
      - CONCURRENT=10
      - QUEUED=50

      # Timeouts
      - TIMEOUT=60000
      - CONNECTION_TIMEOUT=30000

      # Resources
      - MAX_PAYLOAD_SIZE=10mb
      - MAX_CPU_PERCENT=99
      - MAX_MEMORY_PERCENT=99

      # Features
      - ENABLE_CORS=true
      - ENABLE_API_GET=true
      - HEALTH_CHECK=true
      - DEBUG=browserless*

      # Function limits
      - FUNCTION_ENABLE_INCOGNITO_MODE=true
      - FUNCTION_EXTERNALS=["lodash","moment"]

      # Proxy
      - DEFAULT_LAUNCH_ARGS=["--proxy-server=http://proxy:8080"]

    volumes:
      - ./downloads:/downloads
      - ./tmp:/tmp

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

---

## 9. Monitoring

### Health Check

```bash
curl http://localhost:3000/
# Returns: {"status": "ok", ...}

curl http://localhost:3000/stats
# Returns queue and session stats
```

### Metrics Endpoint

```bash
curl http://localhost:3000/metrics
# Prometheus-compatible metrics
```

### Debugging

```bash
# Enable debug logging
docker run -e "DEBUG=browserless*" ghcr.io/browserless/chromium

# View live sessions
curl http://localhost:3000/sessions
```

---

## 10. Common Patterns

### Batch Processing

```javascript
const urls = ["https://example1.com", "https://example2.com"];

async function batchScreenshots(urls) {
  const results = await Promise.all(
    urls.map(async (url) => {
      const response = await fetch(
        "http://localhost:3000/screenshot?token=your-token",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url, options: { fullPage: true } }),
        },
      );
      return { url, screenshot: await response.arrayBuffer() };
    }),
  );
  return results;
}
```

### Retry Logic

```javascript
async function withRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise((r) => setTimeout(r, 1000 * (i + 1)));
    }
  }
}

const screenshot = await withRetry(() => takeScreenshot("https://example.com"));
```

### Queue Management

```javascript
const pLimit = require('p-limit');

const limit = pLimit(5); // Max 5 concurrent

const urls = [...]; // Many URLs

const results = await Promise.all(
  urls.map(url =>
    limit(() => takeScreenshot(url))
  )
);
```

---

## 11. Troubleshooting

### Common Issues

**Connection timeout:**

```javascript
// Increase connection timeout
const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://localhost:3000?token=your-token",
  timeout: 60000,
});
```

**Memory issues:**

```yaml
# Docker resource limits
deploy:
  resources:
    limits:
      memory: 8G
```

**Queue full:**

```bash
# Increase queue size
docker run -e "QUEUED=100" ghcr.io/browserless/chromium
```

**Session leak:**

```javascript
// Always close browser
try {
  // ... operations
} finally {
  await browser.close();
}
```

---

## Best Practices

1. **Use tokens** - Secure your instance
2. **Set timeouts** - Prevent hanging sessions
3. **Limit concurrency** - Based on resources
4. **Close sessions** - Prevent memory leaks
5. **Use health checks** - Monitor availability
6. **Queue management** - Handle bursts
7. **Retry logic** - Handle transient failures
8. **Resource limits** - Docker constraints
9. **Use functions** - Complex workflows
10. **Monitor metrics** - Track performance
