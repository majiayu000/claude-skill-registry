---
name: web-scraping
description: Scrape web pages based on a provided URL using the scpr CLI app.
---

When asked to scrape a web page, use the `scpr` command line interface.

Basic usage (scrape a single page):

```bash
scpr --url https://example.com --output ./scraped
```

This will scrape the page and save it as a markdown file in the `./scraped` folder.

**Recursive scraping**

To scrape a page and all linked pages within the same domain:

```bash
scpr --url https://example.com --output ./scraped --recursive --allowed example.com --max 3
```

**Parallel scraping**

Speed up recursive scraping with multiple threads:

```bash
scpr --url https://example.com --output ./scraped --recursive --allowed example.com --max 2 --parallel 5
```

**Additional options**

- `--log` - Set logging level (info, debug, warn, error)
- `--max` - Maximum depth of pages to follow (default: 1)
- `--parallel` - Number of concurrent threads (default: 1)
- `--allowed` - Allowed domains for recursive scraping (can be specified multiple times)

For more details, run:

```bash
scpr --help
```

Once you are done with scraping, you should scan the output folder to find the content the user asked you for, here is an example flow:

```bash
scpr --url https://example.com --output ./scraped --recursive --allowed example.com --max 2
cd ./scraped
grep -r "pattern of interest"
```
