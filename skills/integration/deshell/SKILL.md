---
name: deshell
description: Fetch web pages as clean Markdown and search the web via the DeShell proxy
version: 1.5.0
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - "node"
        - "npm"
        - "curl"
      env:
        - "DESHELL_API_KEY"
        - "DESHELL_PROXY_URL"
    primaryEnv: "DESHELL_API_KEY"
    install:
      - kind: node
        package: "@deshell/mcp"
        bins: [deshell]
---

# DeShell Skill

Gives agents discoverable, consistent access to the DeShell proxy — no manual URL construction, no remembering headers or API keys.

DeShell converts web pages into clean Markdown, saving 60–80% of tokens for LLM consumption.

## Setup

1. Get your API key from https://deshell.ai (sign up or use your existing key)
2. Install the `deshell` CLI manually (one-time):

   ```bash
   npm install @deshell/mcp
   ```
3. Set the `DESHELL_API_KEY` environment variable

## Commands

```bash
# Fetch any URL as clean Markdown
deshell fetch https://example.com

# Search the web and get results as Markdown
deshell search "best practices for Go error handling"

# Multi-word queries work naturally — no quoting needed
deshell search top 10 AI companies 2025

# Take a screenshot of a web page and return it as an image
deshell screenshot https://example.com

# Render a web page (such as a single page javascript app) before trying to extract markdown
deshell render https://example.com

# Fetch a URL and return its raw content bypassing any attempt to render markdown
deshell raw https://example.com

# Fetch a URL and return its content without using the cache
deshell nocache https://example.com
```

## Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `DESHELL_API_KEY`   | (none) | API key |
| `DESHELL_PROXY_URL` | `https://proxy.deshell.ai/` | Proxy base URL |
| `DESHELL_EXTRA_HEADERS` | (none) | Comma-separated extra headers in `Header-Name:value` format |

## Output

- `deshell fetch` — returns page content as Markdown on stdout
- `deshell search` — returns search results with titles, URLs, descriptions, and page content as Markdown on stdout
- Errors are written to stderr; non-zero exit code on failure

## Extra Headers

To pass additional DeShell headers, use comma-separated `Header-Name:value` pairs:

```bash
# Single header
DESHELL_EXTRA_HEADERS="X-DeShell-No-Cache:true" deshell fetch https://example.com

# Multiple headers
DESHELL_EXTRA_HEADERS="X-DeShell-No-Cache:true,X-DeShell-Max-Tokens:2000" deshell fetch https://example.com
```

## Examples

```bash
# Research a topic
deshell search "OpenClaw agent framework"

# Read documentation
deshell fetch https://docs.github.com/en/rest

# Force fresh fetch (bypass cache)
DESHELL_EXTRA_HEADERS="X-DeShell-No-Cache:true" deshell fetch https://news.ycombinator.com
```

## Fallback — Direct curl

If you prefer not to install npm packages, you can call the proxy directly with curl:

```bash
# Fetch a page
curl -s "https://proxy.deshell.ai/https://example.com" \
  -H "X-DeShell-Key: YOUR_API_KEY"

# Search the web
curl -s "https://proxy.deshell.ai/search?q=your+query" \
  -H "X-DeShell-Key: YOUR_API_KEY" \
  -H "Accept: text/markdown"
```
