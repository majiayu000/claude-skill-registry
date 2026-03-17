---
name: using-scrapy
description: "Scrape websites at scale using Scrapy, a Python web crawling and scraping framework. Use when: (1) Crawling multiple pages or entire sites, (2) Extracting structured data from HTML/XML, or (3) Building automated data pipelines from web sources."
---

# Scrapy Web Scraping Skill

Scrapy is a fast, high-level Python web crawling and scraping framework. It enables structured data extraction from websites, supports crawling entire sites, and integrates pipelines to process and store scraped data.

## When to use

- Crawl entire websites or follow links across many pages
- Extract structured data (prices, articles, product listings) into JSON/CSV
- Run scheduled or large-scale scraping pipelines
- Need built-in support for request throttling, retries, and middlewares

## Required tools / APIs

- No external API required
- Python 3.8+ required
- Scrapy: Web crawling and scraping framework

Install options:

```bash
# pip
pip install scrapy

# Ubuntu/Debian
sudo apt-get install -y python3-pip && pip install scrapy

# macOS
brew install python && pip install scrapy

# Verify installation
scrapy version
```

## Skills

### basic_usage

Create and run a simple Scrapy spider to scrape a single page.

```bash
# Create a new Scrapy project
scrapy startproject myproject
cd myproject

# Generate a spider
scrapy genspider quotes quotes.toscrape.com

# Run the spider and save to JSON
scrapy crawl quotes -o output.json

# Run the spider and save to CSV
scrapy crawl quotes -o output.csv
```

**Python spider (quotes.py):**

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("a.tag::text").getall(),
            }

        # Follow pagination links
        next_page = response.css("li.next a::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

### robust_usage

Production-oriented spider with settings, item pipelines, and error handling.

```bash
# Run with custom settings (rate limiting, retries)
scrapy crawl quotes \
  -s DOWNLOAD_DELAY=1 \
  -s AUTOTHROTTLE_ENABLED=True \
  -s RETRY_TIMES=3 \
  -o output.json

# Run from a script (no project required)
scrapy runspider spider.py -o output.json
```

**Python with error handling and structured items:**

```python
import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess

class ArticleSpider(scrapy.Spider):
    name = "articles"
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 10,
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": "open-skills-bot/1.0 (+https://github.com/besoeasy/open-skills)",
        "RETRY_TIMES": 3,
        "FEEDS": {"output.json": {"format": "json"}},
    }

    def __init__(self, start_url=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [start_url or "https://quotes.toscrape.com"]

    def parse(self, response):
        for article in response.css("article, div.post, div.entry"):
            yield {
                "url": response.url,
                "title": article.css("h1::text, h2::text").get("").strip(),
                "body": " ".join(article.css("p::text").getall()),
            }

        for link in response.css("a::attr(href)").getall():
            if link.startswith("/") or response.url in link:
                yield response.follow(link, self.parse)

    def errback(self, failure):
        self.logger.error(f"Request failed: {failure.request.url} — {failure.value}")


# Run without a Scrapy project
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(ArticleSpider, start_url="https://quotes.toscrape.com")
    process.start()
```

### extract_with_xpath

Use XPath selectors for precise extraction from complex HTML structures.

```python
import scrapy

class XPathSpider(scrapy.Spider):
    name = "xpath_example"
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                "text": quote.xpath(".//span[@class='text']/text()").get(),
                "author": quote.xpath(".//small[@class='author']/text()").get(),
                "tags": quote.xpath(".//a[@class='tag']/text()").getall(),
            }
```

## Output format

Scrapy yields Python dicts (or Item objects) per scraped record. When saved to file:

- `output.json` — Array of JSON objects, one per item
- `output.csv` — CSV with headers matching dict keys
- `output.jsonl` — One JSON object per line (memory-efficient for large crawls)

Example item:
```json
{
  "text": "The world as we have created it is a process of our thinking.",
  "author": "Albert Einstein",
  "tags": ["change", "deep-thoughts", "thinking", "world"]
}
```

Error shape: Scrapy logs errors to stderr; unhandled HTTP errors trigger the `errback` method if defined.

## Rate limits / Best practices

- Enable `ROBOTSTXT_OBEY = True` to respect robots.txt automatically
- Set `DOWNLOAD_DELAY` (seconds between requests) to avoid overloading servers
- Enable `AUTOTHROTTLE_ENABLED = True` for adaptive rate limiting
- Set a descriptive `USER_AGENT` identifying your bot
- Use `CONCURRENT_REQUESTS_PER_DOMAIN = 1` for polite single-domain crawling
- Cache responses during development: `HTTPCACHE_ENABLED = True`

## Agent prompt

```text
You have scrapy web-scraping capability. When a user asks to scrape or crawl a website:

1. Confirm the target URL and data fields to extract (e.g., title, price, link)
2. Create a Scrapy spider using CSS or XPath selectors to target those fields
3. Enable ROBOTSTXT_OBEY=True and set DOWNLOAD_DELAY>=1 to be polite
4. Follow pagination links if the user needs data across multiple pages
5. Save results to output.json or output.csv

Always identify your bot with a descriptive USER_AGENT and never scrape login-protected or paywalled content.
```

## Troubleshooting

**Error: "Forbidden by robots.txt"**
- Symptom: Spider skips URLs and logs "Forbidden by robots.txt"
- Solution: Review the site's robots.txt; only scrape paths that are allowed, or set `ROBOTSTXT_OBEY = False` if you have explicit permission from the site owner

**Error: "Empty or missing data"**
- Symptom: Items are yielded with empty strings or `None` values
- Solution: Inspect the page source (`scrapy shell <url>`) and adjust your CSS/XPath selectors to match the actual HTML structure

**Error: "Too many redirects / 429 Too Many Requests"**
- Symptom: Requests fail with HTTP 429 or redirect loops
- Solution: Increase `DOWNLOAD_DELAY`, enable `AUTOTHROTTLE_ENABLED = True`, or add a `Retry-After` respecting middleware

**Error: "JavaScript-rendered content not found"**
- Symptom: Expected data is missing because the site uses client-side rendering
- Solution: Use `scrapy-playwright` or `scrapy-splash` middleware to render JavaScript before parsing

## See also

- [../using-web-scraping/SKILL.md](../using-web-scraping/SKILL.md) — Browser-based scraping with Playwright/Puppeteer
- [../phone-specs-scraper/SKILL.md](../phone-specs-scraper/SKILL.md) — Scraping phone specifications from public sites
- [../web-search-api/SKILL.md](../web-search-api/SKILL.md) — Find target URLs to scrape via search APIs
