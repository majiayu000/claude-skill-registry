---
name: webcrawler-deep-crawl
description: "Deep-crawl any website from start URLs, return per-page LLM-ready text/markdown/HTML plus metadata (title, description, author, language, canonical URL, OG) and in-scope outbound links. Use when user mentions deep crawl website, recursive crawl, crawl a whole site, scrape entire website, scrape docs site, scrape documentation, scrape knowledge base, scrape blog, build RAG corpus, build vector database from website, knowledge base for chatbot, GPT knowledge files, llms.txt, sitemap crawl, BFS crawl, scrape with depth or page limit, include exclude URL globs, remove boilerplate, strip navigation header footer, website to markdown, website to text, multi-page extraction, bulk page scraping, clean markdown from URL, docs site to markdown corpus, site to clean corpus. Also applies to building RAG pipelines, indexing a customer site, syncing docs into a vector store, generating training corpora from any docs hub, or expanding a single start URL into a clean corpus of every reachable in-scope page."
---

# Website Deep Crawl

> Input: one or more start URLs (+ optional scope, depth, page-count, globs, removal selectors). Output: per-page records `{url, crawl, metadata, text, markdown, html, outboundLinks}` for every page reached within scope.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

From a small set of start URLs, breadth-first crawl every reachable in-scope page, strip boilerplate (navigation, header, footer, cookie banners, etc.), and emit per-page LLM-ready content (text / markdown / HTML) plus structured metadata — suitable for feeding RAG pipelines, vector databases, or chatbot knowledge bases.

## Prerequisites

- One or more start URLs are provided by the caller.
- Target pages are publicly reachable, OR the running browser is already logged in for any pages behind authentication.
- A working directory is available for writing per-page JSON records and the crawl state file.

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Login Verification (when prerequisites include login requirement)

If login status for the target site has been confirmed in the current session → skip this step.

Otherwise: open the target site and observe the page login status:
- Logout/sign-out entry, user avatar, or username exists → logged in, continue execution
- Login/register entry exists with no logout entry → not logged in, inform the user that login is needed first, assist the user in completing the login flow

User refuses or cannot log in → terminate execution.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. Its role is equivalent to copy-pasting on the user's behalf — the data is already on screen, automation merely saves time. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `browser-act --session <name> eval "$(python scripts/xxx.py {params})"`. `$(...)` is bash syntax; use the bash tool for execution. The `eval` token below refers to the browser-act CLI `eval` subcommand — always include the `browser-act --session <name>` prefix and the `"$(...)"` substitution.

Below are all atomic capabilities discovered and verified during the exploration phase, listed by command template with parameters. Simply invoke them as needed — no need to read `scripts/*.py` source code or re-verify. Only inspect scripts when execution fails for troubleshooting. Combine freely as needed during execution.

### API: discover URLs from /llms.txt

Probes `{origin}/llms.txt` (a convention used by LLM-friendly documentation sites) and returns every URL it lists. Fast path — try this first.

`eval "$(python scripts/discover-llms-txt.py 'https://example.com')"`

Parameters:
- positional `origin`: the site origin (scheme + host), e.g. `https://docs.example.com`

Output example:
```json
{
  "error": false,
  "source": "llms.txt",
  "count": 88,
  "urls": ["https://docs.example.com/intro", "https://docs.example.com/install"]
}
```

On failure (file missing or HTTP error): `{"error": true, "message": "llms.txt not available (HTTP 404)", "urls": []}` — move on to sitemap discovery.

### API: discover URLs from /sitemap.xml

Probes `{origin}/sitemap.xml` and `{origin}/sitemap_index.xml`, follows nested sitemap indexes, and collects every `<loc>` URL.

`eval "$(python scripts/discover-sitemap.py 'https://example.com' --max-urls 5000)"`

Parameters:
- positional `origin`: site origin
- `--max-urls`: hard cap to stop ballooning sitemap indexes, default `5000`

Output example:
```json
{
  "error": false,
  "source": "sitemap.xml",
  "count": 86,
  "urls": ["https://example.com/page-a", "https://example.com/page-b"]
}
```

On failure: `{"error": true, "message": "No sitemap found at standard paths", "urls": []}` — fall back to DOM link discovery.

### DOM: discover URLs from the current page

Reads `<a href>` from the currently loaded page DOM, normalizes them to absolute URLs, drops fragments, asset extensions, and out-of-scope links, and optionally applies include / exclude glob filters. Use when llms.txt and sitemap are both unavailable, or to extend the queue with links discovered while crawling.

`eval "$(python scripts/discover-links.py 'https://example.com/docs/' --include-globs '[]' --exclude-globs '["**/changelog/**"]')"`

Parameters:
- positional `start_url`: scope URL. Only links under its directory (or equal to it) are kept.
- `--include-globs`: JSON array of glob patterns; if non-empty, a link must match at least one to be kept. Default `[]` (no include filter).
- `--exclude-globs`: JSON array of glob patterns; matching links are dropped. Default `[]`.

Glob semantics: `**` matches any characters (including `/`), `*` matches any except `/`, `?` matches one character. Example: `https://example.com/{docs,api}/**`.

Output example:
```json
{
  "error": false,
  "source": "dom",
  "page": "https://example.com/docs/intro",
  "scope_base": "https://example.com/docs/",
  "count": 12,
  "links": ["https://example.com/docs/intro", "https://example.com/docs/install"]
}
```

### DOM: extract clean content + metadata + outbound links from the current page

The core extractor. Run this on every crawled page after `wait stable`. Returns the page body in the requested format(s), structured metadata, and the in-scope outbound links found on this page (so callers can extend the BFS queue without a second DOM pass).

`eval "$(python scripts/extract-page-content.py 'https://example.com/docs/' --output-format markdown --remove-selectors '.cookie-banner,#chat-widget' --include-globs '[]' --exclude-globs '[]')"`

Parameters:
- positional `start_url`: scope URL — used to filter the outboundLinks array to in-scope links only.
- `--output-format`: one of `markdown`, `text`, `html`, `all`. Default `markdown`. `all` includes every body field.
- `--remove-selectors`: comma-separated CSS selectors to delete from the chosen content root before extraction (in addition to the built-in boilerplate list). Use this to strip site-specific chrome (e.g. `.cookie-banner`, `#chat-widget`).
- `--keep-selector`: a single CSS selector identifying the main content area. If set, only this element's content is extracted (overrides the built-in content-root heuristic). Use this when the site has a known main wrapper, e.g. `article.docs-content`.
- `--include-globs` / `--exclude-globs`: same semantics as `discover-links`; applied to the returned `outboundLinks` array.

Content-root heuristic (used when `--keep-selector` is not provided), in priority order: `<main>`, `[role="main"]`, `<article>`, `#content`, `.content`, `<body>`.

Built-in boilerplate removal (always applied) includes: `nav`, `header`, `footer`, `aside`, `script`, `style`, `noscript`, `iframe`, `[role="navigation"]`, `[role="banner"]`, `[role="contentinfo"]`, `.cookie*`, `.advertisement`, `.modal`, `.popup`, `.share`, `.social`, `.breadcrumb`, `.toc`, `[aria-hidden="true"]`, etc.

Output example:
```json
{
  "error": false,
  "url": "https://example.com/docs/intro",
  "crawl": {
    "loadedUrl": "https://example.com/docs/intro",
    "loadedTime": "2026-06-25T04:37:23.643Z",
    "referrerUrl": null
  },
  "metadata": {
    "canonicalUrl": "https://example.com/docs/intro",
    "title": "Introduction — Example Docs",
    "description": "Get started with Example.",
    "author": null,
    "keywords": [],
    "languageCode": "en",
    "publishedAt": null,
    "modifiedAt": null,
    "ogImage": "https://example.com/og.png",
    "ogType": "website"
  },
  "text": "Introduction\n\nGet started with Example…",
  "markdown": "# Introduction\n\nGet started with Example…",
  "outboundLinks": [
    "https://example.com/docs/install",
    "https://example.com/docs/quick-start"
  ]
}
```

[AI Intervention] On pages with infinite scroll or lazy-loaded sections, before invoking this script: `scroll down` repeatedly (until page height stops growing or a max-scroll cap is hit) so the dynamic content is in the DOM. The script reads what is currently rendered — it cannot trigger lazy loading on its own.

### Composite: full deep crawl from start URL(s)

End-to-end flow. The Agent orchestrates discovery → BFS queue → per-page extraction → persistence. Records are written one per page so that crashes can resume from where they stopped.

Step 1 — seed the queue:

For each start URL, perform discovery in this priority order and merge results. Stop discovery once the queue has enough URLs to honor `max_pages`.

  a. `eval "$(python scripts/discover-llms-txt.py '{origin}')"` — instant full list when available.
  b. `eval "$(python scripts/discover-sitemap.py '{origin}' --max-urls {cap})"` — broad coverage.
  c. If both fail or return zero in-scope URLs: navigate to the start URL, `wait stable`, then `eval "$(python scripts/discover-links.py '{start_url}' --include-globs '{globs}' --exclude-globs '{globs}')"`.

Filter all discovered URLs to scope: every URL must start with the start URL's `origin + dirname/`, and must satisfy include / exclude globs.

Step 2 — initialize state:

Create the following in the working directory:
- `crawl_state.json` — `{visited: [], queue: [...seedUrls], output_dir: "...", config: {...}}`
- `pages/` directory — one JSON file per successfully crawled page, named by URL hash

Step 3 — BFS loop (one URL at a time, in queue order, until `max_pages` reached or queue empty):

For each `url` popped from the queue:

  a. Skip if `url` is in `visited` or its `metadata.canonicalUrl` (from a prior page) is already in `visited`.
  b. `navigate {url}` → `wait stable` (use `--timeout 60000` for slow sites).
  c. (Optional, only when the target has lazy-loaded content) `scroll down` until height stable or 10 scrolls done.
  d. `eval "$(python scripts/extract-page-content.py '{start_url}' --output-format {format} --remove-selectors '{selectors}' --include-globs '{globs}' --exclude-globs '{globs}')"`.
  e. If result `error: true` → record the failure into `crawl_state.json#failed` and continue. Do NOT retry blindly.
  f. Write the JSON record to `pages/{hash}.json`.
  g. Append `url` and `metadata.canonicalUrl` to `visited`.
  h. For each link in `outboundLinks`: if not in `visited` and not already in `queue`, append to `queue`. Cap queue size at `max_pages * 4` to bound memory.
  i. Persist `crawl_state.json` after every page (resume on next run if interrupted).

Step 4 — finalize:

Emit a summary `{total_pages, success_count, failed_count, duration_seconds, output_dir}`. Optionally concatenate all `pages/*.json` into a single `dataset.jsonl` for downstream loading.

Configuration parameters (set by the Agent before Step 1 based on user request):
- `start_urls`: list of seed URLs (one or more)
- `max_pages`: hard cap on pages crawled, default `100`
- `max_depth`: hard cap on link depth from start URL, default unlimited (`-1`)
- `include_globs`: JSON array, default `[]`
- `exclude_globs`: JSON array, default `[]`
- `output_format`: `markdown` | `text` | `html` | `all`, default `markdown`
- `remove_selectors`: comma-separated site-specific selectors to strip, default `""`
- `keep_selector`: optional content-root selector, default `""`
- `output_dir`: where to write `pages/` and `crawl_state.json`, default `./output/{site}-crawl/`

Output example (per-page record, written to `pages/{hash}.json`):
```json
{
  "url": "https://example.com/docs/intro",
  "crawl": { "loadedUrl": "...", "loadedTime": "...", "referrerUrl": null, "depth": 0 },
  "metadata": { "title": "...", "description": "...", "languageCode": "en", "canonicalUrl": "..." },
  "text": "...",
  "markdown": "# ...",
  "outboundLinks": ["..."]
}
```

Summary example:
```json
{
  "total_pages": 86,
  "success_count": 84,
  "failed_count": 2,
  "duration_seconds": 412,
  "output_dir": "./output/example-crawl/"
}
```

## Pagination

This is a recursive crawler, not a list with pages. Boundary control is by `max_pages` (queue length cap) and `max_depth` (links-away-from-start cap), not by API pagination. Termination: queue empty OR `max_pages` reached OR no more in-scope outbound links discovered.

## Success Criteria

`success_count >= 1 AND success_count / total_pages >= 0.8 AND extracted markdown body length per page > 100 chars for at least 80% of pages`

## Known Limitations

- Pages behind authentication require the running browser to be logged in beforehand — this Skill does not handle login flows.
- Pages whose content is rendered after async user interaction beyond simple scroll (e.g. clicking "Load more", expanding accordions to reveal content) need the Agent to add the relevant click before invoking extract-page-content; otherwise the hidden content will be missing.
- `<iframe>` content is removed by default (treated as boilerplate). If a page's main content lives inside an iframe, the Agent must first `navigate` into the iframe URL and crawl it separately.
- File downloads (PDF, DOCX, XLSX) are not handled. URLs with these extensions are intentionally filtered from the crawl queue.
- Some sites' boilerplate is structurally indistinguishable from main content (e.g. "Was this page helpful?" footers placed inside `<main>`). The Agent should pass site-specific patterns via `--remove-selectors` to strip them.
- Single-page applications that load content via JS after navigation may need a longer `wait stable --timeout`. Anti-scraping CAPTCHAs are not bypassed by this Skill; the calling browser must already pass them.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through the command templates serially within a single session; do not parallelize within one browser (prone to triggering anti-scraping restrictions). Refer to rate information in "Known Limitations" above to add appropriate intervals. To increase throughput, open multiple stealth browser sessions and distribute work across them — each session has an independent fingerprint so rate limits apply per session
- **Test before batch execution**: After writing a batch script, you must first test with 1-2 items to verify the script runs correctly; only then run the full batch. Never skip testing and execute in batch directly
- **Reduce redundant pre-operations**: When multiple steps depend on the same prerequisite state, complete them in batch under that state to avoid repeatedly establishing the same state
- **Error resumption**: Save results item by item during batch processing; on failure, resume from the breakpoint rather than starting over
- **Prefer llms.txt / sitemap.xml over DOM discovery**: A single fetch returns the full URL list; DOM discovery requires loading every page first. Always try the two API discovery routes first and only fall back to DOM when both return empty.
- **Polite delay between pages**: Default to 500–1500 ms between page navigations to avoid burst patterns. Tighten only on sites you control or own.

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/webcrawler-deep-crawl.memory.md` (working directory is determined by the Agent running the Skill, typically the project root or current working directory)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used or how many results were returned — those are task outputs, not experience.
