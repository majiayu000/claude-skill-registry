---
name: visit-webpage
description: Visit a webpage and extract its content as markdown, or fetch images. Use for reading articles, documentation, or any web page content. Handles both HTML pages (via Jina Reader) and image URLs (downloads and saves locally).
---

# Visit Webpage

Fetch and extract readable content from web pages as markdown, or download images. Handles JavaScript-rendered content via Jina Reader service.

## Setup

Optionally get a Jina API key for higher rate limits:
1. Create an account at https://jina.ai/
2. Get your API key from the dashboard
3. Add to your shell profile (`~/.profile` or `~/.zprofile` for zsh):
   ```bash
   export JINA_API_KEY="your-api-key-here"
   ```

Without an API key, the service works with rate limits.

## Usage

```bash
{baseDir}/visit.py <url>
```

## Examples

```bash
# Read an article (returns markdown)
{baseDir}/visit.py https://example.com/article

# Fetch documentation
{baseDir}/visit.py https://docs.python.org/3/library/asyncio.html

# Download an image (auto-detected by content-type)
{baseDir}/visit.py https://example.com/image.png
# Then use read tool to view: read /tmp/visit-image-xxx.png
```

## Output

For **HTML pages**: Returns markdown content to stdout.

For **images**: Downloads the image to a temp file and prints the path. Use the `read` tool to view it. Supports PNG, JPEG, GIF, and WebP formats.

## Features

- Extracts main content from HTML pages
- Converts HTML to clean markdown
- Handles JavaScript-rendered pages via Jina Reader
- Auto-detects and downloads images to temp files
- Retries on rate limiting (HTTP 451)
- 5MB max image size limit

## When to Use

- Reading articles, blog posts, or documentation
- Extracting content from search results
- Downloading images from URLs (then use `read` to view)
- Following links found during web search
