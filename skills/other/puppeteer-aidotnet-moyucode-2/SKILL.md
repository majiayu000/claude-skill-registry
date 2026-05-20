---
name: puppeteer
description: 使用Puppeteer（Google）进行浏览器自动化和PDF生成。支持无头Chrome控制，用于网页爬虫、截图、PDF生成和自动化测试。
metadata:
  short-description: 浏览器自动化和PDF生成
source:
  repository: https://github.com/puppeteer/puppeteer
  license: Apache-2.0
  stars: 89k+
---

# Puppeteer Tool

## Description
Headless Chrome/Chromium automation for PDF generation, screenshots, web scraping, and testing.

## Source
- Repository: [puppeteer/puppeteer](https://github.com/puppeteer/puppeteer)
- License: Apache-2.0
- Maintainer: Google

## Installation

```bash
npm install puppeteer
```

## Usage Examples

### Generate PDF from HTML

```typescript
import puppeteer from 'puppeteer';

async function generatePDF(html: string, outputPath: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setContent(html, { waitUntil: 'networkidle0' });
  
  await page.pdf({
    path: outputPath,
    format: 'A4',
    margin: { top: '20mm', right: '20mm', bottom: '20mm', left: '20mm' },
    printBackground: true,
  });
  
  await browser.close();
}

// Usage
const html = `
  <html>
    <head><style>body { font-family: Arial; }</style></head>
    <body><h1>Invoice #001</h1><p>Total: $100.00</p></body>
  </html>
`;
await generatePDF(html, 'invoice.pdf');
```

### Take Screenshot

```typescript
async function takeScreenshot(url: string, outputPath: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  await page.screenshot({
    path: outputPath,
    fullPage: true,
    type: 'png',
  });
  
  await browser.close();
}
```

### Web Scraping

```typescript
async function scrapeData(url: string) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  
  const data = await page.evaluate(() => {
    const items = document.querySelectorAll('.product');
    return Array.from(items).map(item => ({
      title: item.querySelector('h2')?.textContent?.trim(),
      price: item.querySelector('.price')?.textContent?.trim(),
    }));
  });
  
  await browser.close();
  return data;
}
```

### Form Automation

```typescript
async function submitForm(url: string, formData: Record<string, string>) {
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  
  await page.goto(url);
  
  // Fill form fields
  for (const [selector, value] of Object.entries(formData)) {
    await page.type(selector, value);
  }
  
  // Submit
  await page.click('button[type="submit"]');
  await page.waitForNavigation();
  
  await browser.close();
}
```

## PDF Options

```typescript
interface PDFOptions {
  path?: string;
  scale?: number;                    // 0.1 - 2, default 1
  displayHeaderFooter?: boolean;
  headerTemplate?: string;
  footerTemplate?: string;
  printBackground?: boolean;
  landscape?: boolean;
  pageRanges?: string;               // '1-5, 8, 11-13'
  format?: 'Letter' | 'Legal' | 'A4' | 'A3';
  width?: string;
  height?: string;
  margin?: { top, right, bottom, left };
}
```

## Tags
`browser`, `pdf`, `screenshot`, `automation`, `scraping`

## Compatibility
- Codex: ✅
- Claude Code: ✅
