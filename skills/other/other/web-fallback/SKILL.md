---
name: web-fallback
description: Fetch web content with automatic fallback from WebFetch to WebSearch
user-invocable: true
disable-model-invocation: true
---

# /web-fallback — Resilient Web Content Retrieval

When you need information from a URL but WebFetch might fail (auth walls, rate limits, blocked hosts), use this fallback chain.

## Usage

User provides: `/web-fallback <url> <what to find>`

## Fallback Chain

### Step 1: Try WebFetch
```
WebFetch(url=<url>, prompt=<what to find>)
```

If successful → return results.

### Step 2: Try WebSearch
If WebFetch fails (redirect, auth wall, timeout):
```
WebSearch(query="<domain> <what to find>")
```

Extract relevant results and summarize.

### Step 3: Try Cached/Alternative Sources
If WebSearch also fails:
- Check if a cached version exists: `WebFetch(url="https://webcache.googleusercontent.com/search?q=cache:<url>")`
- Try archive.org: `WebFetch(url="https://web.archive.org/web/<url>")`
- Search for the same content on alternative domains

### Step 4: Report Failure
If all steps fail, report:
- Which steps were tried
- Error messages from each
- Suggest the user try manually or provide the content via clipboard

## Notes
- Always report which fallback level succeeded
- For GitHub URLs, prefer `gh` CLI instead of WebFetch
- For npm package docs, prefer context7 MCP instead
- Rate limit: don't retry the same URL more than twice
