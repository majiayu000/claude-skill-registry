---
name: web
description: Web browsing wrapper for Clawdbot's browser tool. Provides convenient commands for opening URLs, getting page content, searching the web, and taking screenshots.
homepage: https://github.com/MillionthOdin16/clawd-explorations
metadata: {"clawdbot":{"emoji":"🌐","requires":{"browser":"enabled"}}}
---

# Web Browsing Skill

Browse the web using Clawdbot's built-in browser tool (not curl!).

## Setup

**Browser must be enabled in Clawdbot:**
```bash
# Browser is already enabled in your config
clawdbot browser status  # Check status
clawdbot browser start   # Start if needed
```

## Commands

### Open a URL
```bash
uv run {baseDir}/scripts/web.py open "https://example.com"
```

### Get Page Content
```bash
uv run {baseDir}/scripts/web.py get "https://example.com"
```

### Get Specific Element (CSS Selector)
```bash
uv run {baseDir}/scripts/web.py get "https://example.com" --selector ".main-content"
```

### Search the Web (DuckDuckGo)
```bash
uv run {baseDir}/scripts/web.py search "Python AI agents"
# Output:
# 1. https://result1.com
# 2. https://result2.com
```

### Get Plain Text
```bash
uv run {baseDir}/scripts/web.py text "https://example.com"
```

### Take Screenshot
```bash
uv run {baseDir}/scripts/web.py screenshot "https://example.com" --output /tmp/page.png
```

## Examples

### Browse Hacker News
```bash
# Open HN
uv run {baseDir}/scripts/web.py open "https://news.ycombinator.com"

# Get top stories
uv run {baseDir}/scripts/web.py get "https://news.ycombinator.com" --selector ".titleline"
```

### Research a Topic
```bash
# Search for information
uv run {baseDir}/scripts/web.py search "multi-agent AI systems research"

# Open first result
uv run {baseDir}/scripts/web.py open "https://arxiv.org/abs/..."
```

### Get Documentation
```bash
# Get page text
uv run {baseDir}/scripts/web.py text "https://docs.example.com/api"
```

## Why This Is Better Than Curl

| Feature | Curl | Web Skill |
|---------|------|-----------|
| JavaScript rendering | ❌ No | ✅ Yes |
| Interactive pages | ❌ No | ✅ Yes |
| Screenshots | ❌ No | ✅ Yes |
| Element extraction | ❌ No | ✅ Yes |
| Search | ❌ Manual | ✅ Built-in |

## Browser Tool Directly

You can also use the browser tool directly:

```bash
# Open URL
clawdbot browser open "https://example.com"

# Get snapshot
clawdbot browser snapshot

# Take screenshot
clawdbot browser screenshot --out /tmp/page.png

# Navigate
clawdbot browser navigate "https://new-url.com"

# Click element
clawdbot browser act --kind click --selector ".button"
```

## Troubleshooting

### "Browser not running"
```bash
clawdbot browser start
```

### "Browser not available"
Check if browser is enabled in your config.

### Slow pages
Increase wait time in scripts or use `text` command for faster results.
