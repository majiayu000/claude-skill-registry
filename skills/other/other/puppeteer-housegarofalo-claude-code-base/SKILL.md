---
name: puppeteer
description: Puppeteer browser automation for web scraping, testing, and screenshots. Control headless Chrome for automated workflows, PDF generation, and E2E testing. Use for headless browsers, web scraping, automated testing, or PDF generation.
---

# Puppeteer Skill

Complete guide for Puppeteer - headless Chrome automation.

## Quick Reference

| Command | Purpose |
|---------|---------|
| `npm install puppeteer` | Install with bundled Chrome |
| `npm install puppeteer-core` | Install without Chrome (BYOB) |
| `browser.newPage()` | Create new page |
| `page.goto(url)` | Navigate to URL |
| `page.screenshot()` | Take screenshot |
| `page.pdf()` | Generate PDF |

## 1. Installation

```bash
# npm (includes Chromium)
npm install puppeteer

# Puppeteer core (BYOB - Bring Your Own Browser)
npm install puppeteer-core
```

## 2. Basic Usage

### Launch Browser

```javascript
const puppeteer = require("puppeteer");

(async () => {
  // Launch browser
  const browser = await puppeteer.launch({
    headless: true, // or 'new' for new headless mode
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  // Create page
  const page = await browser.newPage();

  // Navigate
  await page.goto("https://example.com");

  // Close
  await browser.close();
})();
```

### Launch Options

```javascript
const browser = await puppeteer.launch({
  headless: false, // Show browser
  slowMo: 50, // Slow down operations
  devtools: true, // Open DevTools
  defaultViewport: {
    width: 1920,
    height: 1080,
  },
  args: ["--start-maximized", "--disable-notifications", "--disable-gpu"],
  executablePath: "/path/to/chrome", // Custom Chrome
  userDataDir: "./user-data", // Persist session
});
```

## 3. Navigation

### Page Navigation

```javascript
// Go to URL
await page.goto("https://example.com", {
  waitUntil: "networkidle2", // Wait for network idle
  timeout: 30000,
});

// Wait options
// 'load' - window load event
// 'domcontentloaded' - DOMContentLoaded event
// 'networkidle0' - no network connections for 500ms
// 'networkidle2' - max 2 network connections for 500ms

// Navigate
await page.goBack();
await page.goForward();
await page.reload();

// Get URL
const url = page.url();
```

### Wait for Elements

```javascript
// Wait for selector
await page.waitForSelector(".my-class");
await page.waitForSelector("#my-id", { visible: true });

// Wait for function
await page.waitForFunction('document.querySelector(".loaded")');

// Wait for navigation
await Promise.all([page.waitForNavigation(), page.click("a.link")]);

// Custom wait
await page.waitForTimeout(1000); // 1 second
```

## 4. Interactions

### Click and Type

```javascript
// Click element
await page.click("#submit-button");
await page.click("button.primary");

// Type text
await page.type("#username", "myuser");
await page.type("#password", "mypass", { delay: 100 }); // Human-like

// Clear and type
await page.click("#input", { clickCount: 3 });
await page.type("#input", "new value");

// Press keys
await page.keyboard.press("Enter");
await page.keyboard.press("Tab");
await page.keyboard.down("Shift");
await page.keyboard.press("Tab");
await page.keyboard.up("Shift");
```

### Forms

```javascript
// Select dropdown
await page.select("#dropdown", "option-value");
await page.select("#multi-select", "value1", "value2");

// Checkbox
await page.click("#checkbox");

// File upload
const input = await page.$("input[type=file]");
await input.uploadFile("./file.pdf");

// Submit form
await page.click("button[type=submit]");
// or
await page.$eval("form", (form) => form.submit());
```

### Mouse Actions

```javascript
// Move mouse
await page.mouse.move(100, 200);

// Click at position
await page.mouse.click(100, 200);

// Drag and drop
await page.mouse.move(100, 100);
await page.mouse.down();
await page.mouse.move(200, 200);
await page.mouse.up();

// Scroll
await page.mouse.wheel({ deltaY: 500 });
```

## 5. Data Extraction

### Get Content

```javascript
// Get text content
const text = await page.$eval(".title", (el) => el.textContent);

// Get attribute
const href = await page.$eval("a", (el) => el.getAttribute("href"));

// Get multiple elements
const items = await page.$$eval(".item", (elements) =>
  elements.map((el) => ({
    title: el.querySelector(".title").textContent,
    price: el.querySelector(".price").textContent,
  }))
);

// Get inner HTML
const html = await page.$eval(".content", (el) => el.innerHTML);

// Get all text
const pageText = await page.evaluate(() => document.body.innerText);
```

### Element Handles

```javascript
// Get single element
const element = await page.$(".my-class");
if (element) {
  const text = await element.evaluate((el) => el.textContent);
  await element.click();
}

// Get multiple elements
const elements = await page.$$(".items");
for (const el of elements) {
  console.log(await el.evaluate((node) => node.textContent));
}
```

### Evaluate JavaScript

```javascript
// Run in page context
const result = await page.evaluate(() => {
  return {
    title: document.title,
    url: window.location.href,
    data: window.myData,
  };
});

// Pass arguments
const text = await page.evaluate((selector) => {
  return document.querySelector(selector).textContent;
}, ".my-selector");
```

## 6. Screenshots & PDF

### Screenshots

```javascript
// Full page
await page.screenshot({ path: "fullpage.png", fullPage: true });

// Viewport only
await page.screenshot({ path: "viewport.png" });

// Element screenshot
const element = await page.$(".card");
await element.screenshot({ path: "element.png" });

// With options
await page.screenshot({
  path: "screenshot.png",
  type: "png", // or 'jpeg', 'webp'
  quality: 80, // for jpeg/webp
  fullPage: true,
  clip: { x: 0, y: 0, width: 800, height: 600 },
  omitBackground: true, // Transparent
});

// As buffer
const buffer = await page.screenshot({ encoding: "binary" });
```

### PDF Generation

```javascript
await page.pdf({
  path: "page.pdf",
  format: "A4",
  printBackground: true,
  margin: {
    top: "20mm",
    right: "20mm",
    bottom: "20mm",
    left: "20mm",
  },
});

// Custom size
await page.pdf({
  path: "custom.pdf",
  width: "8.5in",
  height: "11in",
  landscape: true,
});
```

## 7. Network Interception

### Request Interception

```javascript
await page.setRequestInterception(true);

page.on("request", (request) => {
  // Block images
  if (request.resourceType() === "image") {
    request.abort();
  }
  // Modify headers
  else if (request.url().includes("api")) {
    request.continue({
      headers: {
        ...request.headers(),
        Authorization: "Bearer token",
      },
    });
  } else {
    request.continue();
  }
});
```

### Response Handling

```javascript
page.on("response", async (response) => {
  if (response.url().includes("/api/data")) {
    const data = await response.json();
    console.log("API Response:", data);
  }
});

// Wait for specific response
const response = await page.waitForResponse((response) =>
  response.url().includes("/api/data")
);
const data = await response.json();
```

### Block Resources

```javascript
await page.setRequestInterception(true);

const blockedTypes = ["image", "stylesheet", "font", "media"];

page.on("request", (request) => {
  if (blockedTypes.includes(request.resourceType())) {
    request.abort();
  } else {
    request.continue();
  }
});
```

## 8. Authentication

### Basic Auth

```javascript
await page.authenticate({
  username: "user",
  password: "pass",
});

await page.goto("https://httpbin.org/basic-auth/user/pass");
```

### Cookies

```javascript
// Set cookies
await page.setCookie({
  name: "session",
  value: "abc123",
  domain: "example.com",
});

// Get cookies
const cookies = await page.cookies();
console.log(cookies);

// Clear cookies
await page.deleteCookie({ name: "session" });
```

### Local Storage

```javascript
// Set local storage
await page.evaluate(() => {
  localStorage.setItem("token", "mytoken");
});

// Get local storage
const token = await page.evaluate(() => {
  return localStorage.getItem("token");
});
```

## 9. Multiple Pages/Tabs

### Handle Popups

```javascript
// Listen for new page
const [popup] = await Promise.all([
  new Promise((resolve) =>
    browser.once("targetcreated", async (target) => {
      resolve(await target.page());
    })
  ),
  page.click('a[target="_blank"]'),
]);

await popup.waitForSelector(".content");
const text = await popup.$eval(".content", (el) => el.textContent);
await popup.close();
```

### Multiple Tabs

```javascript
const page1 = await browser.newPage();
const page2 = await browser.newPage();

await page1.goto("https://example.com");
await page2.goto("https://example.org");

// Get all pages
const pages = await browser.pages();
```

## 10. Advanced Patterns

### Scraping with Pagination

```javascript
async function scrapeAllPages(url) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const allData = [];

  await page.goto(url);

  while (true) {
    // Scrape current page
    const items = await page.$$eval(".item", (elements) =>
      elements.map((el) => el.textContent)
    );
    allData.push(...items);

    // Check for next page
    const nextButton = await page.$(".next-page:not(.disabled)");
    if (!nextButton) break;

    await Promise.all([page.waitForNavigation(), nextButton.click()]);
  }

  await browser.close();
  return allData;
}
```

### Parallel Scraping

```javascript
async function scrapeUrls(urls) {
  const browser = await puppeteer.launch();

  const results = await Promise.all(
    urls.map(async (url) => {
      const page = await browser.newPage();
      await page.goto(url);
      const title = await page.title();
      await page.close();
      return { url, title };
    })
  );

  await browser.close();
  return results;
}
```

### Retry Logic

```javascript
async function withRetry(fn, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise((r) => setTimeout(r, 1000 * (i + 1)));
    }
  }
}

await withRetry(async () => {
  await page.goto("https://example.com");
  await page.waitForSelector(".content");
});
```

## 11. Troubleshooting

### Common Issues

**Timeout errors:**

```javascript
// Increase timeout
await page.goto(url, { timeout: 60000 });
await page.setDefaultNavigationTimeout(60000);
await page.setDefaultTimeout(30000);
```

**Element not found:**

```javascript
// Wait before interacting
await page.waitForSelector("#element", { visible: true });
await page.click("#element");

// Check if exists
const element = await page.$("#element");
if (element) {
  await element.click();
}
```

**Memory issues:**

```javascript
// Close pages when done
await page.close();

// Limit concurrent pages
const semaphore = new Semaphore(5);
```

**Debugging:**

```javascript
const browser = await puppeteer.launch({
  headless: false,
  slowMo: 100,
  devtools: true,
});

// Console logs
page.on("console", (msg) => console.log("PAGE LOG:", msg.text()));

// Page errors
page.on("pageerror", (err) => console.log("PAGE ERROR:", err));
```

## Best Practices

1. **Use waitFor** - Don't rely on timing
2. **Handle errors** - Try/catch and retry
3. **Close resources** - Prevent memory leaks
4. **Block unnecessary** - Images, fonts for speed
5. **Use headless** - Faster in production
6. **Set viewport** - Consistent rendering
7. **User agent** - Avoid bot detection
8. **Rate limiting** - Be respectful
9. **Parallel carefully** - Limit concurrency
10. **Log operations** - Debug easier
