---
name: scrapling
description: Local Python web scraping with anti-bot bypass, adaptive element tracking, and stealth browser automation. This skill should be used when scraping pages behind Cloudflare or anti-bot protection, extracting specific elements with CSS/XPath selectors, stealth fetching with TLS impersonation, local scraping without API keys, or when adaptive element tracking is needed to survive site redesigns. Complements the firecrawl skill (cloud API) with 100% local execution.
---

# Scrapling -- Local Stealth Web Scraping

100% local Python library (BSD-3, [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)). No API keys, no cloud dependencies. Built-in Cloudflare solver, TLS impersonation, and adaptive element tracking.

## When to Use Scrapling vs Firecrawl

| Need | Use | Why |
|------|-----|-----|
| Clean markdown from a URL | `firecrawl scrape --only-main-content` | Optimized for LLM markdown conversion |
| Bypass Cloudflare/anti-bot | `scrapling` stealth fetch | Built-in Turnstile solver, Patchright stealth |
| Extract specific elements | `scrapling` with CSS/XPath selectors | Element-level precision, adaptive tracking |
| No API key available | `scrapling` | 100% local, zero credentials |
| Batch cloud scraping | `firecrawl crawl` / `batch-scrape` | Cloud infrastructure, parallel processing |
| Site redesign resilience | `scrapling` adaptive mode | SQLite-backed similarity matching |
| Full-site concurrent crawl | `scrapling` Spider framework | Scrapy-like with pause/resume |
| Web search + scrape | `firecrawl search --scrape` | Combined search + extraction |

## Installation

Run once to set up Scrapling with all features:

```bash
~/.claude/skills/scrapling/scripts/scrapling_install.sh
```

Installs `scrapling[all]` via uv, downloads Chromium + system dependencies, and verifies all fetchers load.

## Quick Start -- Stdout Wrapper

The wrapper uses Scrapling's Python API directly (faster than CLI, avoids curl_cffi cert issues) and outputs to stdout for piping into `filter_web_results.py`:

```bash
# Basic HTTP fetch (fastest, TLS impersonation)
python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py https://example.com

# Stealth mode (Patchright, anti-bot bypass)
python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py https://protected.site --stealth

# Stealth + Cloudflare solver
python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py https://cf-protected.site --stealth --solve-cloudflare

# Dynamic (Playwright Chromium, JS rendering)
python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py https://js-heavy.site --dynamic

# With CSS selector for targeted extraction
python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py https://example.com --css ".product-list"

# Pipe through firecrawl's filter for token efficiency
python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py https://example.com --stealth | \
  python3 ~/.claude/skills/firecrawl/scripts/filter_web_results.py --sections "Pricing" --max-chars 5000
```

**Full path:** `python3 ~/.claude/skills/scrapling/scripts/scrapling_fetch.py`
**Flags:** `--stealth`, `--dynamic`, `--css SELECTOR`, `--solve-cloudflare`, `--impersonate BROWSER`, `--format {text,html}`, `--no-headless`, `--timeout SECONDS`

For `--network-idle`, `--real-chrome`, or POST requests, use the CLI direct path below.

## Quick Start -- CLI Direct

For file-based output (Scrapling's native CLI):

```bash
# HTTP fetch -> markdown
scrapling extract get 'https://example.com' content.md

# HTTP with CSS selector and browser impersonation
scrapling extract get 'https://example.com' content.md --css-selector '.main-content' --impersonate chrome

# Dynamic fetch (Playwright, JS rendering)
scrapling extract fetch 'https://example.com' content.md

# Stealth with Cloudflare bypass
scrapling extract stealthy-fetch 'https://protected.site' content.md --solve-cloudflare

# Stealth with CSS selector, visible browser for debugging
scrapling extract stealthy-fetch 'https://site.com' content.md --css-selector '.data' --no-headless
```

### Three Fetcher Tiers

| CLI verb | Engine | Stealth | JS | Speed |
|----------|--------|---------|-----|-------|
| `get` | curl_cffi (HTTP) | TLS impersonation | No | Fast |
| `fetch` | Playwright/Chromium | Medium | Yes | Medium |
| `stealthy-fetch` | Patchright/Chrome | Maximum | Yes | Slower |

## Python API

For element-level extraction, automation, or when the CLI is insufficient:

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher

# Simple HTTP fetch with CSS extraction
page = Fetcher.get('https://example.com', impersonate='chrome')
titles = page.css('.item h2::text').getall()
links = page.css('a::attr(href)').getall()

# Stealth with Cloudflare bypass
page = StealthyFetcher.fetch('https://protected.site',
    headless=True, solve_cloudflare=True,
    hide_canvas=True, block_webrtc=True)
data = page.css('.content').get_all_text()

# Page automation (login, click, fill)
def login(page):
    page.fill('#username', 'user')
    page.fill('#password', 'pass')
    page.click('#submit')

page = StealthyFetcher.fetch('https://app.example.com', page_action=login)
```

### Parsing (no fetching)

```python
from scrapling.parser import Selector

page = Selector("<html>...</html>")
page.css('.item::text').getall()       # CSS with pseudo-elements
page.xpath('//div[@class="item"]')     # XPath
page.find_all('div', class_='item')    # BeautifulSoup-style
page.find_by_text('Add to Cart')       # Text search
page.find_by_regex(r'Price: \$\d+')    # Regex search
```

## Adaptive Scraping

Scrapling's signature feature. Elements are fingerprinted to SQLite and relocated by similarity scoring after site redesigns.

```python
from scrapling.fetchers import Fetcher

Fetcher.adaptive = True
page = Fetcher.get('https://example.com')

# First run: save element fingerprint
products = page.css('.product-list', auto_save=True)

# Later, after site redesign breaks the selector:
products = page.css('.product-list', adaptive=True)  # Still finds it
```

Read: `references/adaptive-scraping.md`

## Spider Framework

For full-site crawling with concurrency, pause/resume, and session routing:

```python
from scrapling.spiders import Spider, Response, Request
from scrapling.fetchers import FetcherSession, StealthySession

class ResearchSpider(Spider):
    name = "research"
    start_urls = ["https://example.com/"]
    concurrent_requests = 10

    def configure_sessions(self, manager):
        manager.add("fast", FetcherSession(impersonate="chrome"))
        manager.add("stealth", StealthySession(headless=True), lazy=True)

    async def parse(self, response: Response):
        for link in response.css('a::attr(href)').getall():
            if "protected" in link:
                yield Request(link, sid="stealth")
            else:
                yield Request(link, sid="fast")
        for item in response.css('.article'):
            yield {"title": item.css('h2::text').get(), "url": response.url}

result = ResearchSpider().start(crawldir="./data")  # Pause/resume enabled
result.items.to_json("output.json")
```

## Troubleshooting

- **Browser not found:** Run `scrapling install` to download browser dependencies
- **Import error on fetchers:** Install the full package: `uv pip install "scrapling[all]"`
- **Cloudflare still blocking:** Combine flags: `--solve-cloudflare --block-webrtc --hide-canvas`
- **SSL cert error with HTTP fetcher:** curl_cffi's bundled CA certs can be stale on macOS/pyenv. The wrapper handles this automatically (`verify=False`). For Python API, pass `verify=False` to `Fetcher.get()`.
- **Slow stealthy fetch:** Expected--browser automation is inherently slower than HTTP requests. Use `get` (HTTP) when stealth is not needed.

## Reference Documentation

| File | Contents |
|------|----------|
| `references/cli-reference.md` | Full CLI extract command reference (get, post, fetch, stealthy-fetch) |
| `references/python-api-reference.md` | Python API (Fetcher, DynamicFetcher, StealthyFetcher, Sessions, Spiders) |
| `references/adaptive-scraping.md` | Adaptive element tracking deep-dive (save, match, similarity scoring) |
