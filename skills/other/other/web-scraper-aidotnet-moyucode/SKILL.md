---
name: web-scraper
description: 从网页提取和处理数据，使用CSS选择器、XPath智能解析，支持限速和错误处理。
metadata:
  short-description: 从网页提取数据
---

# Web Scraper Skill

## Description
Extract and process data from web pages with intelligent parsing capabilities.

## Trigger
- `/scrape` command
- User requests web data extraction
- User needs to parse HTML

## Prompt

You are a web scraping expert that extracts data efficiently and ethically.

### Puppeteer Scraper (TypeScript)

```typescript
import puppeteer from 'puppeteer';

interface Product {
  name: string;
  price: number;
  rating: number;
  url: string;
}

async function scrapeProducts(url: string): Promise<Product[]> {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  // Set user agent to avoid detection
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
  
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  // Wait for products to load
  await page.waitForSelector('.product-card');
  
  const products = await page.evaluate(() => {
    const items = document.querySelectorAll('.product-card');
    return Array.from(items).map(item => ({
      name: item.querySelector('.product-name')?.textContent?.trim() ?? '',
      price: parseFloat(item.querySelector('.price')?.textContent?.replace('$', '') ?? '0'),
      rating: parseFloat(item.querySelector('.rating')?.getAttribute('data-rating') ?? '0'),
      url: item.querySelector('a')?.href ?? '',
    }));
  });
  
  await browser.close();
  return products;
}
```

### Cheerio Parser (Node.js)

```typescript
import axios from 'axios';
import * as cheerio from 'cheerio';

async function parseArticle(url: string) {
  const { data } = await axios.get(url, {
    headers: { 'User-Agent': 'Mozilla/5.0' }
  });
  
  const $ = cheerio.load(data);
  
  return {
    title: $('h1.article-title').text().trim(),
    author: $('span.author-name').text().trim(),
    date: $('time').attr('datetime'),
    content: $('article.content p').map((_, el) => $(el).text()).get().join('\n\n'),
    tags: $('a.tag').map((_, el) => $(el).text()).get(),
  };
}
```

### Rate Limiting

```typescript
class RateLimiter {
  private queue: (() => Promise<void>)[] = [];
  private processing = false;
  
  constructor(private delayMs: number = 1000) {}
  
  async add<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      this.queue.push(async () => {
        try {
          resolve(await fn());
        } catch (e) {
          reject(e);
        }
      });
      this.process();
    });
  }
  
  private async process() {
    if (this.processing) return;
    this.processing = true;
    
    while (this.queue.length > 0) {
      const fn = this.queue.shift()!;
      await fn();
      await new Promise(r => setTimeout(r, this.delayMs));
    }
    
    this.processing = false;
  }
}

// Usage
const limiter = new RateLimiter(2000); // 2 seconds between requests
const results = await Promise.all(
  urls.map(url => limiter.add(() => scrapeProducts(url)))
);
```

## Tags
`web-scraping`, `data-extraction`, `parsing`, `automation`, `html`

## Compatibility
- Codex: ✅
- Claude Code: ✅
