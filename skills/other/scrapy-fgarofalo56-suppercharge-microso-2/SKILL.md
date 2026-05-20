---
name: scrapy
description: "Scrapy framework for web scraping and crawling at scale. Build spiders, extract data, and manage crawl pipelines. Use for large-scale scraping, data extraction, or building web crawlers."
---

# Scrapy Skill

Complete guide for Scrapy - web scraping framework.

## Quick Reference

### Key Components

| Component      | Description            |
| -------------- | ---------------------- |
| **Spider**     | Crawling logic         |
| **Item**       | Data container         |
| **Pipeline**   | Data processing        |
| **Middleware** | Request/response hooks |
| **Selector**   | Data extraction        |

### Commands

```bash
scrapy startproject <name>    # Create project
scrapy genspider <name> <domain>  # Create spider
scrapy crawl <spider>         # Run spider
scrapy shell <url>            # Interactive shell
scrapy list                   # List spiders
```

---

## 1. Installation

```bash
pip install scrapy

# With extras
pip install scrapy[all]
```

---

## 2. Project Structure

### Create Project

```bash
scrapy startproject myproject
cd myproject
scrapy genspider example example.com
```

### Directory Structure

```
myproject/
├── scrapy.cfg
└── myproject/
    ├── __init__.py
    ├── items.py
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        ├── __init__.py
        └── example.py
```

---

## 3. Basic Spider

### Simple Spider

```python
# spiders/example.py
import scrapy

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com"]

    def parse(self, response):
        # Extract data
        for item in response.css("div.item"):
            yield {
                "title": item.css("h2::text").get(),
                "price": item.css("span.price::text").get(),
                "link": item.css("a::attr(href)").get()
            }

        # Follow pagination
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

### Run Spider

```bash
# Run and output to file
scrapy crawl example -o output.json
scrapy crawl example -o output.csv
scrapy crawl example -o output.jsonl

# With arguments
scrapy crawl example -a category=electronics
```

---

## 4. Selectors

### CSS Selectors

```python
# Get text
response.css("h1::text").get()
response.css("h1::text").getall()

# Get attribute
response.css("a::attr(href)").get()
response.css("img::attr(src)").getall()

# Nested selection
response.css("div.item").css("span.price::text").get()

# Multiple classes
response.css("div.item.featured")

# Child selector
response.css("div.parent > span")

# Contains text
response.css("a:contains('Next')")
```

### XPath Selectors

```python
# Get text
response.xpath("//h1/text()").get()
response.xpath("//h1/text()").getall()

# Get attribute
response.xpath("//a/@href").get()

# By text content
response.xpath("//button[text()='Submit']")
response.xpath("//div[contains(text(), 'Hello')]")

# By attribute
response.xpath("//input[@placeholder='Search']")

# Parent/child
response.xpath("//div[@class='parent']//span")

# Following sibling
response.xpath("//label[text()='Email']/following-sibling::input")
```

### Re (Regex)

```python
# Extract with regex
response.css("p::text").re(r"Price: (\d+)")
response.css("p::text").re_first(r"\d+")

# Clean text
import re
text = response.css("p::text").get()
clean = re.sub(r"\s+", " ", text).strip()
```

---

## 5. Items

### Define Items

```python
# items.py
import scrapy

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class ReviewItem(scrapy.Item):
    product_id = scrapy.Field()
    author = scrapy.Field()
    rating = scrapy.Field()
    text = scrapy.Field()
    date = scrapy.Field()
```

### Use Items

```python
from myproject.items import ProductItem

class ProductSpider(scrapy.Spider):
    name = "products"

    def parse(self, response):
        item = ProductItem()
        item["name"] = response.css("h1::text").get()
        item["price"] = response.css(".price::text").get()
        item["url"] = response.url
        yield item
```

### Item Loaders

```python
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags

class ProductLoader(ItemLoader):
    default_output_processor = TakeFirst()

    name_in = MapCompose(str.strip)
    price_in = MapCompose(remove_tags, str.strip, float)
    description_out = Join()

# Usage in spider
def parse(self, response):
    loader = ProductLoader(item=ProductItem(), response=response)
    loader.add_css("name", "h1::text")
    loader.add_css("price", ".price::text")
    loader.add_xpath("description", "//div[@class='desc']//text()")
    yield loader.load_item()
```

---

## 6. Pipelines

### Define Pipeline

```python
# pipelines.py
class CleanDataPipeline:
    def process_item(self, item, spider):
        # Clean price
        if item.get("price"):
            item["price"] = float(item["price"].replace("$", ""))
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        url = item.get("url")
        if url in self.seen:
            raise scrapy.exceptions.DropItem(f"Duplicate: {url}")
        self.seen.add(url)
        return item

class SaveToDBPipeline:
    def open_spider(self, spider):
        # Connect to database
        self.connection = create_connection()

    def close_spider(self, spider):
        # Close connection
        self.connection.close()

    def process_item(self, item, spider):
        # Save to database
        save_item(self.connection, item)
        return item
```

### Enable Pipelines

```python
# settings.py
ITEM_PIPELINES = {
    "myproject.pipelines.CleanDataPipeline": 100,
    "myproject.pipelines.DuplicatesPipeline": 200,
    "myproject.pipelines.SaveToDBPipeline": 300,
}
```

---

## 7. Settings

### Common Settings

```python
# settings.py

# Project info
BOT_NAME = "myproject"

# Spider modules
SPIDER_MODULES = ["myproject.spiders"]
NEWSPIDER_MODULE = "myproject.spiders"

# Crawl responsibly
ROBOTSTXT_OBEY = True

# Concurrency
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Delays
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# User agent
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Retry
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]

# Caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = "httpcache"

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = "scrapy.log"

# Output
FEED_EXPORT_ENCODING = "utf-8"
```

### Per-Spider Settings

```python
class MySpider(scrapy.Spider):
    name = "myspider"

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS": 4,
        "ITEM_PIPELINES": {
            "myproject.pipelines.SpecialPipeline": 100
        }
    }
```

---

## 8. Middlewares

### Downloader Middleware

```python
# middlewares.py
import random

class RandomUserAgentMiddleware:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/89.0"
    ]

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(self.user_agents)

class ProxyMiddleware:
    def process_request(self, request, spider):
        request.meta["proxy"] = "http://proxy.example.com:8080"

class RetryMiddleware:
    def process_response(self, request, response, spider):
        if response.status in [403, 429]:
            # Retry with delay
            return request.copy()
        return response
```

### Enable Middleware

```python
# settings.py
DOWNLOADER_MIDDLEWARES = {
    "myproject.middlewares.RandomUserAgentMiddleware": 400,
    "myproject.middlewares.ProxyMiddleware": 410,
}
```

---

## 9. Handling JavaScript

### Scrapy-Splash

```bash
pip install scrapy-splash
```

```python
# settings.py
SPLASH_URL = "http://localhost:8050"

DOWNLOADER_MIDDLEWARES = {
    "scrapy_splash.SplashCookiesMiddleware": 723,
    "scrapy_splash.SplashMiddleware": 725,
}

SPIDER_MIDDLEWARES = {
    "scrapy_splash.SplashDeduplicateArgsMiddleware": 100,
}

# spider
from scrapy_splash import SplashRequest

class JSSpider(scrapy.Spider):
    def start_requests(self):
        yield SplashRequest(
            url="https://example.com",
            callback=self.parse,
            args={"wait": 2}
        )
```

### Scrapy-Playwright

```bash
pip install scrapy-playwright
playwright install
```

```python
# settings.py
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

# spider
class PlaywrightSpider(scrapy.Spider):
    def start_requests(self):
        yield scrapy.Request(
            url="https://example.com",
            meta={"playwright": True, "playwright_page_methods": [
                PageMethod("wait_for_selector", "div.loaded")
            ]}
        )
```

---

## 10. Advanced Patterns

### Following Links

```python
class CrawlSpider(scrapy.Spider):
    def parse(self, response):
        # Extract data from listing page
        for item in response.css("div.item"):
            detail_url = item.css("a::attr(href)").get()
            yield response.follow(
                detail_url,
                callback=self.parse_detail,
                meta={"category": response.meta.get("category")}
            )

        # Follow pagination
        for next_page in response.css("a.page-link::attr(href)"):
            yield response.follow(next_page, self.parse)

    def parse_detail(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "category": response.meta.get("category"),
            "content": response.css("div.content::text").getall()
        }
```

### Multiple Start URLs

```python
class MultiSpider(scrapy.Spider):
    name = "multi"

    def start_requests(self):
        categories = ["electronics", "clothing", "books"]
        for cat in categories:
            yield scrapy.Request(
                url=f"https://example.com/{cat}",
                callback=self.parse,
                meta={"category": cat}
            )
```

### Login Required

```python
class AuthSpider(scrapy.Spider):
    name = "auth"

    def start_requests(self):
        yield scrapy.Request(
            url="https://example.com/login",
            callback=self.login
        )

    def login(self, response):
        # Extract CSRF token if needed
        token = response.css("input[name='csrf']::attr(value)").get()

        yield scrapy.FormRequest.from_response(
            response,
            formdata={
                "username": "myuser",
                "password": "mypass",
                "csrf": token
            },
            callback=self.after_login
        )

    def after_login(self, response):
        # Check login success
        if "Welcome" in response.text:
            yield scrapy.Request(
                url="https://example.com/dashboard",
                callback=self.parse_dashboard
            )
```

---

## 11. Testing

### Spider Contracts

```python
class ProductSpider(scrapy.Spider):
    name = "products"

    def parse(self, response):
        """
        @url https://example.com/products
        @returns items 10 20
        @returns requests 1
        @scrapes name price url
        """
        for item in response.css("div.product"):
            yield {
                "name": item.css("h2::text").get(),
                "price": item.css(".price::text").get(),
                "url": item.css("a::attr(href)").get()
            }
```

### Run Tests

```bash
scrapy check products
```

### Unit Tests

```python
import unittest
from scrapy.http import HtmlResponse
from myproject.spiders.products import ProductSpider

class TestProductSpider(unittest.TestCase):
    def setUp(self):
        self.spider = ProductSpider()

    def test_parse(self):
        html = """
        <div class="product">
            <h2>Product 1</h2>
            <span class="price">$99</span>
        </div>
        """
        response = HtmlResponse(
            url="https://example.com",
            body=html,
            encoding="utf-8"
        )

        results = list(self.spider.parse(response))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Product 1")
```

---

## 12. Deployment

### Scrapy Cloud (Zyte)

```bash
pip install shub
shub login
shub deploy
```

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "myspider", "-o", "output.json"]
```

### Schedule with Cron

```bash
0 * * * * cd /path/to/project && scrapy crawl myspider -o /data/$(date +\%Y\%m\%d_\%H\%M).json
```

---

## Best Practices

1. **Respect robots.txt** - ROBOTSTXT_OBEY = True
2. **Use delays** - Be respectful to servers
3. **Handle errors** - Retry and log failures
4. **Cache responses** - Development efficiency
5. **Use items** - Structured data
6. **Pipeline processing** - Clean and validate
7. **Test spiders** - Contracts and unit tests
8. **Monitor crawls** - Log and stats
9. **Rotate user agents** - Avoid blocks
10. **Use proxies** - For large-scale scraping
