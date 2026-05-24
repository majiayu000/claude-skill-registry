---
name: obscura
description: "Stealth headless browser with CDP server for anti-fingerprint browsing, parallel scraping, and low-memory CDP automation. This skill should be used when stealth browsing, anti-detection scraping, headless CDP automation with fingerprint protection, or tracker-free page fetching is needed. Triggers on 'stealth browse', 'anti-fingerprint', 'obscura', 'stealth CDP', 'undetectable scraping', 'headless stealth', 'tracker-free browsing'."
---

# Obscura

Rust headless browser with built-in anti-fingerprinting and CDP server. Fills the gap between Lightpanda (CDP, no stealth) and Scrapling (stealth, no CDP). Binary at `~/tools/obscura/obscura`.

## When to Use

| Scenario | Tool |
|----------|------|
| Clean single-page markdown | Firecrawl |
| Cloudflare Turnstile bypass | Scrapling |
| Reddit | Lightpanda / Scrapling |
| Twitter/X | Jina |
| Interactive `@ref` automation | agent-browser |
| **Stealth CDP automation** | **Obscura** |
| **Batch stealth scraping** | **Obscura** |
| **Low-RAM headless (30MB)** | **Obscura** |

## Usage

Fetch a page with stealth:
```bash
obscura fetch --stealth --quiet https://example.com --eval "document.title"
```

Parallel batch scrape:
```bash
obscura scrape URL1 URL2 URL3 --concurrency 25 --format json
```

Start CDP server (port 9224 to avoid Chrome conflict on 9222):
```bash
obscura serve --port 9224 --stealth
```

Chain through Proxelar for defense-in-depth — `--proxy` is a **global flag**, goes before the subcommand:
```bash
obscura --proxy http://127.0.0.1:8080 serve --port 9224 --stealth
obscura --proxy http://127.0.0.1:8080 fetch --stealth https://example.com
```

Connect Puppeteer: `browserWSEndpoint: "ws://127.0.0.1:9224/devtools/browser"`
Connect Playwright: `endpointURL: "ws://127.0.0.1:9224"`

CDP domain coverage: see `references/cdp-coverage.md`. Includes non-standard `LP.getMarkdown` for DOM-to-Markdown.

## Gotchas

- **Port 9224 is convention, not default.** The binary defaults to 9222 (Chrome's port). Always pass `--port 9224`.
- **`--stealth` is off by default.** Pass it explicitly for anti-fingerprinting and tracker blocking.
- **`--proxy` is a global flag.** Place it before `fetch`/`serve`/`scrape`, not after.
- **`--quiet` suppresses the banner.** Use it when piping output.
- **WebSocket path differs from Lightpanda.** Obscura: `/devtools/browser`. Lightpanda: bare endpoint.
- **Ad-hoc signed binary, no notarization.** SHA-256 recorded at `~/tools/obscura/obscura.sha256`. Verify on update.

## Helper Scripts

| Script | Purpose |
|--------|---------|
| `scripts/obscura_serve.sh` | Start CDP server on 9224 with cleanup trap, PID file, optional `--with-proxelar` |
