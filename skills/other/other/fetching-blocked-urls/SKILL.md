---
name: fetching-blocked-urls
description: Retrieve clean markdown from URLs when web_fetch fails. Converts pages via Jina AI reader service with automatic retry. Use when web_fetch or curl returns 403, blocked, paywall, timeout, JavaScript-rendering errors, or empty content or user explicitly suggests using jina.
metadata:
  version: 0.1.1
---

# Fetching Blocked URLs

Retrieve readable content from URLs that web_fetch cannot access. Jina AI's reader service renders JavaScript, bypasses soft blocks, and returns clean markdown.

## Activation Triggers

Invoke this skill immediately when web_fetch returns:
- 403 Forbidden or access denied
- Paywall or login wall indicators
- Empty, garbled, or truncated content
- JavaScript-heavy SPA failures
- Timeout errors

## Core Command

```bash
curl -s --max-time 30 "https://r.jina.ai/TARGET_URL"
```

The service returns markdown with page title, body text, and preserved links.

## Retry Pattern

Jina's backend has ~10% intermittent failures. Use retry logic to achieve 99%+ success:

```bash
for attempt in 1 2 3; do
  result=$(curl -s --max-time 30 "https://r.jina.ai/TARGET_URL" 2>&1)
  echo "$result" | grep -q "upstream connect error" || { echo "$result"; break; }
  [ $attempt -lt 3 ] && sleep 1
done
```

## Workflow Integration

1. **Primary**: Use web_fetch (native tool)
2. **Fallback**: This skill with retry when web_fetch fails
3. **Escalate**: Request user assistance only after retry exhaustion

Attempt this fallback before asking users to copy-paste content manually.

## Output Format

Jina returns structured markdown:
- `Title:` page title
- `URL Source:` original URL
- `Markdown Content:` extracted body text, links preserved

## Limitations

- Long pages may truncate
- Sites blocking all scrapers remain inaccessible
- Login-required content limited to public portions
- Real-time dynamic content may not render

## Domain Access

`r.jina.ai` is whitelisted in Claude container network configuration.
