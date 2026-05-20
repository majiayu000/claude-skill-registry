---
name: web-scraper
description: 使用CSS选择器从网页提取数据，支持分页、限速和多种输出格式。
metadata:
  short-description: 从网站爬取数据
source:
  repository: https://github.com/cheeriojs/cheerio
  license: MIT
---

# Web Scraper Tool

## Description
Extract structured data from web pages using CSS selectors with rate limiting and pagination support.

## Trigger
- `/scrape` command
- User requests web data extraction
- User needs to parse HTML

## Usage

```bash
# Scrape single page
python scripts/web_scraper.py --url "https://example.com" --selector ".item" --output data.json

# Scrape with multiple selectors
python scripts/web_scraper.py --url "https://example.com" --selectors "title:.title,price:.price,link:a@href"

# Scrape multiple pages
python scripts/web_scraper.py --urls urls.txt --selector ".product" --output products.json --delay 2
```

## Tags
`scraping`, `web`, `html`, `data-extraction`, `automation`

## Compatibility
- Codex: ✅
- Claude Code: ✅
