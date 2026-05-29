---
name: distil
description: Fetch web pages as clean Markdown and search the web via the distil.net proxy
version: 2.0.1
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - "curl"
      env:
        - "DISTIL_API_KEY"
    primaryEnv: "DISTIL_API_KEY"
---

# Distil Skill

Gives agents discoverable, consistent access to the Distil proxy — no manual URL construction, no remembering headers or API keys.

Distil converts web pages into clean Markdown, saving 60–80% of tokens for LLM consumption.

## Setup

1. Get your free API key with email verification from https://distil.net (sign up or use your existing key)
2. Set the `DISTIL_API_KEY` environment variable
3. Optional: set `DISTIL_PROXY_URL` (defaults to `https://proxy.distil.net`)

## Commands

```bash
# Fetch any URL as clean Markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Search the web and get results as Markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/search?q=best+practices+for+Go+error+handling" \
  -H "X-Distil-Key: $DISTIL_API_KEY" \
  -H "Accept: text/markdown"

# Take a screenshot of a web page and return it as an image
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/screenshot/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY" > screenshot.png

# Render a web page (such as a single page javascript app) before trying to extract markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/render/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Fetch a URL and return its raw content bypassing any attempt to render markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/raw/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Fetch a URL and return its content without using the cache
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/nocache/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"
```

## Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `DISTIL_API_KEY`   | (none, required) | API key |
| `DISTIL_PROXY_URL` | `https://proxy.distil.net` | Proxy base URL (override for self-hosted) |

## Output

- Responses are returned on stdout
- HTTP errors are returned with non-2xx status and an error payload

## Examples

```bash
# Research a topic
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/search?q=OpenClaw+agent+framework" \
  -H "X-Distil-Key: $DISTIL_API_KEY" \
  -H "Accept: text/markdown"

# Read documentation
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/https://docs.github.com/en/rest" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Force fresh fetch (bypass cache)
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/nocache/https://news.ycombinator.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"
```

## Fallback — Direct curl

If you prefer to call the proxy directly:

```bash
# Fetch a page
curl -s "https://proxy.distil.net/https://example.com" \
  -H "X-Distil-Key: YOUR_API_KEY"

# Search the web
curl -s "https://proxy.distil.net/search?q=your+query" \
  -H "X-Distil-Key: YOUR_API_KEY" \
  -H "Accept: text/markdown"
```

## Notes

Every reply request in Markdown will include how many raw tokens were saved by distil's markdown conversion, so you can see the efficiency benefits in real time. Distil's Markdown output is designed to be clean and concise, stripping away unnecessary HTML and boilerplate to give you just the content you need. This can save 60–80% of tokens compared to raw HTML, making it much more efficient for LLM consumption.

If you run out of tokens, distil will return the raw HTML content instead of Markdown, so you can still access the information even if you exceed your token limits. This way, you won't lose access to the content, but you'll be able to see how much more efficient the Markdown output is when you have tokens available. When this happens distil will inject a HTML comment within the web page you are accessing to let you know how to fix it.