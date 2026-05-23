---
name: web-search
description: Web search using Jina Search API. Returns search results with titles, URLs, and descriptions. Use for finding documentation, facts, current information, or any web content. Lightweight, no browser required.
---

# Web Search

Perform web searches using the Jina Search API. Returns formatted search results with titles, URLs, and descriptions.

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
{baseDir}/search.py "your search query"
```

## Examples

```bash
# Basic search
{baseDir}/search.py "python async await tutorial"

# Search for recent news
{baseDir}/search.py "latest AI developments 2024"

# Find documentation
{baseDir}/search.py "nodejs fs promises API"
```

## Output Format

Returns markdown-formatted search results:

```
## Search Results

[Title of first result](https://example.com/page1)
Description or snippet from the search result...

[Title of second result](https://example.com/page2)
Description or snippet from the search result...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Finding relevant web pages for research
- Any task requiring web search without interactive browsing
