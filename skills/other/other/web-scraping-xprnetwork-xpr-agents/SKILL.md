---
name: web-scraping
description: Web scraping tools for fetching and extracting data from web pages
---

## Web Scraping

You have web scraping tools for fetching and extracting data from web pages:

**Single page:**
- `scrape_url` — fetch a URL and get cleaned text content + metadata (title, description, link count)
  - Use format="text" (default) for most tasks — strips all HTML
  - Use format="markdown" to preserve headings, links, lists, bold/italic
  - Use format="html" only when you need raw HTML

**Link discovery:**
- `extract_links` — fetch a page and extract all links with text and type (internal/external)
  - Use the `pattern` parameter to filter by regex (e.g. `"\\.pdf$"` for PDF links)
  - Links are deduplicated and resolved to absolute URLs

**Multi-page research:**
- `scrape_multiple` — fetch up to 10 URLs in parallel for comparison/research
  - One failure doesn't block others (uses Promise.allSettled)

**Best practices:**
- Prefer "text" format for content extraction, "markdown" for preserving structure
- Don't scrape the same domain more than 5 times per minute
- Combine with `store_deliverable` to save scraped content as job evidence
- For very large pages, the content is limited to 5MB
