---
name: using-jina-reader
description: Fetch web page content using Jina Reader as a fallback when websites block direct access. Use when WebFetch returns 403, 406, captcha pages, empty content, Cloudflare blocks, or anti-bot responses. Also use when the user explicitly asks to use Jina Reader.
---

# Jina Reader

Jina Reader (`r.jina.ai`) converts web pages to clean markdown. Use it as a fallback when `WebFetch` fails due to bot protection, Cloudflare, captchas, or other blocking.

## When to Use

- `WebFetch` returns 403, 406, or other access-denied status codes
- Response content is a Cloudflare challenge page, captcha, or "please enable JavaScript"
- Response body is empty or nonsensical despite a 200 status
- User explicitly requests Jina Reader

## How to Use

Prepend `https://r.jina.ai/` to the target URL:

```
https://r.jina.ai/https://example.com/page
```

Call this with `WebFetch`:

```
WebFetch url="https://r.jina.ai/https://example.com/page"
```

The response is the page content converted to clean markdown.

## Headers

For better results, pass these headers via `WebFetch`:

- `Accept: text/markdown` — ensures markdown output
- `X-No-Cache: true` — bypass Jina's cache for fresh content

## Limitations

- Jina Reader has rate limits on free usage
- Some pages with heavy JS rendering may still return incomplete content
- Very long pages may be truncated

## Workflow

1. Try `WebFetch` with the original URL first
2. If blocked, retry via `https://r.jina.ai/<original-url>`
3. If Jina also fails, inform the user and suggest they open the page manually
