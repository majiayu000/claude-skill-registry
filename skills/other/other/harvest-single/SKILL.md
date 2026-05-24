---
name: harvest-single
description: Single page smart extraction - articles, docs, blog posts to clean markdown
allowed-tools: [Bash, Read, Write, WebFetch]
keywords: [harvest, scrape, extract, single, page, article, documentation, markdown]
---

# Harvest Single Page

Extract and clean content from a single web page. Auto-detects content type (article, documentation, API reference, blog post) and produces clean, structured markdown.

## Usage

```
/harvest <url>
```

## Examples

```bash
# Extract a blog post
/harvest https://blog.example.com/best-practices-2024

# Extract API documentation page
/harvest https://docs.stripe.com/api/charges

# Extract a GitHub README
/harvest https://github.com/owner/repo
```

## How It Works

1. Fetch URL content via WebFetch or crawl4ai
2. Detect content type (article, docs, API ref, blog, wiki)
3. Extract main content, strip navigation/ads/footers
4. Preserve code blocks, tables, images
5. Add metadata header (source, date, word count)
6. Save to `.claude/cache/agents/harvest/`

## Output Format

```markdown
# [Page Title]
> Source: [URL]
> Extracted: [timestamp]
> Type: [article|docs|api|blog|wiki]
> Words: [count]

[Clean extracted content in markdown]

## Links Found
- [Link text](URL)
```

## Fallback Chain

1. crawl4ai Docker (port 11235) - preferred
2. WebFetch tool - built-in fallback
3. curl + html2text - last resort

## When to Use

- Quick grab of a single page's content
- Extracting a specific doc page for reference
- Saving an article for later analysis
- Getting clean markdown from messy HTML
