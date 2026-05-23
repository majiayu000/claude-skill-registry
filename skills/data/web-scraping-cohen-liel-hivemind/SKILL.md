---
name: web-scraping
description: Web scraping and internet search patterns. Use when scraping websites, crawling pages, extracting data from HTML, automating browser interactions, or fetching external web content programmatically.
---

# Web Scraping & Internet Search Patterns

## HTTP Scraping (httpx + BeautifulSoup)
```python
import httpx
from bs4 import BeautifulSoup
import asyncio

async def scrape_page(url: str) -> dict:
    """Fetch and parse a single page."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyBot/1.0; +https://example.com/bot)"
    }
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=30) as client:
        response = await client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")

    return {
        "title": soup.find("title").get_text(strip=True) if soup.find("title") else "",
        "headings": [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])],
        "links": [a["href"] for a in soup.find_all("a", href=True)],
        "text": soup.get_text(separator="\n", strip=True)[:5000],
    }

async def scrape_many(urls: list[str], max_concurrent: int = 5) -> list[dict]:
    """Scrape many URLs with concurrency limit."""
    sem = asyncio.Semaphore(max_concurrent)

    async def fetch_one(url):
        async with sem:
            try:
                return await scrape_page(url)
            except Exception as e:
                return {"url": url, "error": str(e)}

    return await asyncio.gather(*[fetch_one(url) for url in urls])
```

## Browser Automation (Playwright)
```python
from playwright.async_api import async_playwright

async def scrape_with_browser(url: str) -> str:
    """Use for JS-heavy sites that need a real browser."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Block images/fonts for speed
        await page.route("**/*.{png,jpg,gif,webp,svg,woff,woff2}", lambda r: r.abort())

        await page.goto(url, wait_until="networkidle", timeout=30000)

        # Wait for specific element
        await page.wait_for_selector(".content", timeout=10000)

        # Extract data
        text = await page.inner_text("body")
        links = await page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)")

        await browser.close()
        return text

async def fill_form_and_submit(url: str, form_data: dict) -> str:
    """Automate form submission."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        for selector, value in form_data.items():
            await page.fill(selector, value)

        await page.click("button[type=submit]")
        await page.wait_for_load_state("networkidle")
        result = await page.inner_text("body")
        await browser.close()
        return result
```

## Web Search (via SerpAPI or DuckDuckGo)
```python
import httpx

async def search_web(query: str, num_results: int = 10) -> list[dict]:
    """Search the web using SerpAPI."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://serpapi.com/search",
            params={
                "q": query,
                "num": num_results,
                "api_key": settings.SERPAPI_KEY,
                "engine": "google",
            },
            timeout=30,
        )
        data = response.json()

    return [
        {
            "title": r.get("title"),
            "url": r.get("link"),
            "snippet": r.get("snippet"),
        }
        for r in data.get("organic_results", [])
    ]

async def search_duckduckgo(query: str) -> list[dict]:
    """Free alternative — DuckDuckGo instant answers (no API key)."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1},
            timeout=15,
        )
    data = response.json()
    results = []
    for r in data.get("Results", []):
        results.append({"title": r["Text"], "url": r["FirstURL"]})
    return results
```

## RSS Feed Reader
```python
import feedparser
import httpx

async def read_rss(feed_url: str) -> list[dict]:
    """Parse RSS/Atom feed."""
    async with httpx.AsyncClient() as client:
        response = await client.get(feed_url, timeout=15)
    feed = feedparser.parse(response.text)
    return [
        {
            "title": entry.title,
            "url": entry.link,
            "summary": entry.get("summary", ""),
            "published": entry.get("published", ""),
        }
        for entry in feed.entries[:20]
    ]
```

## Data Extraction (Structured)
```python
from pydantic import BaseModel
from typing import Optional
import re

class ProductData(BaseModel):
    name: str
    price: Optional[float]
    description: str
    image_url: Optional[str]

def extract_product(soup: BeautifulSoup, url: str) -> ProductData:
    """Extract structured product data."""
    # Try JSON-LD schema first (most reliable)
    json_ld = soup.find("script", type="application/ld+json")
    if json_ld:
        import json
        data = json.loads(json_ld.string)
        if data.get("@type") == "Product":
            return ProductData(
                name=data["name"],
                price=float(data.get("offers", {}).get("price", 0)),
                description=data.get("description", ""),
                image_url=data.get("image"),
            )

    # Fallback: heuristic selectors
    name = soup.find(["h1", '[class*="title"]', '[itemprop="name"]'])
    price_el = soup.find(['[class*="price"]', '[itemprop="price"]'])
    price_text = price_el.get_text() if price_el else ""
    price = float(re.search(r'[\d.]+', price_text).group()) if re.search(r'[\d.]+', price_text) else None

    return ProductData(
        name=name.get_text(strip=True) if name else "",
        price=price,
        description="",
        image_url=None,
    )
```

## Politeness & Rate Limiting
```python
import time, random

class PoliteScraper:
    def __init__(self, delay_range=(1, 3)):
        self.delay_range = delay_range
        self.last_request = {}

    async def fetch(self, url: str, session: httpx.AsyncClient) -> str:
        domain = httpx.URL(url).host

        # Respect per-domain delay
        if domain in self.last_request:
            elapsed = time.time() - self.last_request[domain]
            min_delay = random.uniform(*self.delay_range)
            if elapsed < min_delay:
                await asyncio.sleep(min_delay - elapsed)

        response = await session.get(url)
        self.last_request[domain] = time.time()
        return response.text
```

## Robots.txt Compliance
```python
from urllib.robotparser import RobotFileParser
from urllib.parse import urljoin

def can_scrape(url: str, user_agent: str = "*") -> bool:
    """Check robots.txt before scraping."""
    parsed = httpx.URL(url)
    robots_url = f"{parsed.scheme}://{parsed.host}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp.can_fetch(user_agent, url)
```

## Rules
- ALWAYS check robots.txt before scraping — respect disallow rules
- Set a descriptive User-Agent (not a fake browser agent) for bots
- Rate limit: minimum 1-2 second delay between requests to same domain
- Use Playwright only when necessary (JS rendering) — httpx is 10x faster
- Cache scraped pages (Redis/disk) to avoid re-fetching during development
- Handle rate limit responses (429): exponential backoff with jitter
- Never scrape personal data without legal basis (GDPR compliance)
- For large crawls: use Scrapy framework instead of rolling your own
- Store raw HTML alongside extracted data for re-processing
