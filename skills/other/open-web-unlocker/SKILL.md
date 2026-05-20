---
name: open-web-unlocker
description: >
  Fetch web pages and search results as clean markdown, structured JSON, or
  raw HTML. Use this skill when the task involves fetching a URL, scraping web
  content, or querying search engines (examples include reading articles,
  extracting product data, getting search results from Brave/Bing/DuckDuckGo,
  or handling JS-rendered and anti-bot pages).
---

# Open Web Unlocker — Fetch Skill

Open Web Unlocker fetches web pages and returns clean markdown, raw HTML, or structured JSON. It handles static pages, JS-rendered pages, anti-bot challenges, and search engine results — all via a single CLI command with no installation required.

## Quick start

```bash
bunx open-web-unlocker fetch <url>
```

Bun (`bunx`) is preferred. Node (`npx`) also works.

## Format selection

```bash
bunx open-web-unlocker fetch <url> --format markdown   # default
bunx open-web-unlocker fetch <url> --format json
bunx open-web-unlocker fetch <url> --format html
```

**Which format to use:**

| Format     | When to use                                                  |
|------------|--------------------------------------------------------------|
| `markdown` | Default. Clean content with nav/footer/boilerplate stripped. Best for reading or summarizing pages. |
| `json`     | When you need structured extracted fields (title, author, price, etc.) |
| `html`     | When you need the full raw page including all elements       |

50+ site-specific parsers produce high-quality markdown and JSON for common domains. Pages without a parser fall back to generic extraction, which may include more noise.

## Search engines

Fetch search result pages directly — Open Web Unlocker parses them into structured results:

```bash
bunx open-web-unlocker fetch "https://search.brave.com/search?q=query"
bunx open-web-unlocker fetch "https://www.bing.com/search?q=query"
bunx open-web-unlocker fetch "https://duckduckgo.com/?q=query"
```

Google is **not** supported.

## Timeout

```bash
bunx open-web-unlocker fetch <url> --timeout 45000
```

Default per-strategy timeouts: ~8s for fetch, ~15s for browser. Increase `--timeout` for slow or JS-heavy pages.
