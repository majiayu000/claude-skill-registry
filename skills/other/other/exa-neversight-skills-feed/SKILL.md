---
name: exa
description: Search the web and extract content using Exa AI. Use when searching for current information, researching topics, fetching content from URLs, or finding code examples. Also use for competitive research, finding similar pages, or extracting structured content.
---

# Exa Web Search & Content Extraction

Real-time web search and content extraction powered by Exa AI.

## Usage

Use the Python script at `scripts/exa.py`. Requires `EXA_API_KEY` environment variable.

### Web Search

```bash
# Basic search
python scripts/exa.py search --query "latest AI research"

# Fast search for simple queries
python scripts/exa.py search --query "node.js version" --type fast

# Deep search for comprehensive results
python scripts/exa.py search --query "React server components" --type deep --num-results 10

# With full text content
python scripts/exa.py search --query "GraphQL best practices" --text

# Filter by domain
python scripts/exa.py search --query "LLM research" --include-domains "arxiv.org,paperswithcode.com"

# Filter by date
python scripts/exa.py search --query "AI news" --start-date "2025-01-01T00:00:00.000Z"
```

### Extract URL Content

```bash
# Extract from documentation
python scripts/exa.py contents --urls "https://docs.python.org/3/tutorial/classes.html"

# Multiple URLs
python scripts/exa.py contents --urls "https://example.com/page1,https://example.com/page2"

# Prefer live content
python scripts/exa.py contents --urls "https://example.com/page" --livecrawl preferred
```

### Code Examples

```bash
# Find code examples
python scripts/exa.py code --query "React useState hook examples"

# Quick syntax lookup
python scripts/exa.py code --query "Python list comprehension" --tokens 2000

# Detailed patterns
python scripts/exa.py code --query "GraphQL resolver patterns" --tokens 15000
```

## Search Types

| Type | Use Case | Speed |
| ---- | -------- | ----- |
| `fast` | Quick lookups, simple queries | Fastest |
| `auto` | General purpose (default) | Medium |
| `deep` | Complex research, comprehensive | Slowest |

## When to Use Each Command

| Use `search` | Use `contents` | Use `code` |
| ------------ | -------------- | ---------- |
| Finding relevant pages | Have a specific URL | Programming questions |
| General web research | Extracting known content | API/library usage |
| News and articles | Reading documentation | Code examples |

## Query Tips

- Be specific: "React useEffect cleanup function examples" not "useEffect"
- Include the library/framework name
- Specify the programming language
- Mention the use case (authentication, caching, etc.)

## Rules

- Use `--type fast` for simple factual queries
- Use `--type deep` for research requiring comprehensive results
- Use `--text` to get full page content in search results
- Use `code` command for programming questions instead of `search`
- Use `contents` when you have a specific URL to extract
- Use `--format json` for structured output when needed
