---
name: exa-contents
version: 0.1.0
description: >
  Call Exa Contents (POST /contents) for LLM-ready extraction from known URLs:
  text, highlights, summaries, links, image links, subpages, freshness-controlled
  crawl. Use when the agent already has URLs. Prefer Exa MCP web_fetch_exa when
  available; otherwise raw HTTP with EXA_API_KEY. NOT for open-ended discovery
  (use exa-search) or auth-walled X/Twitter (use mktg-x). For full-site crawl of
  a known domain, firecrawl may be better.
allowed-tools:
  - Bash
  - Read
  - Write
  - Skill
author: Exa Labs (ported by mktg)
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: 📄
---

## On Activation

1. Read `brand/competitors.md` / `brand/landscape.md` if present for URL shortlists. Optional.
2. Confirm Exa auth (MCP or `EXA_API_KEY`) via `mktg doctor` if unsure.
3. Prefer MCP `web_fetch_exa` when available; otherwise use the cURL examples below.
4. If the page is auth-walled (X/Twitter login stub), route to `mktg-x` instead.

# Exa Contents

> Requires API key: Get one at https://dashboard.exa.ai/api-keys
>
> Header: `x-api-key: $EXA_API_KEY`

Use `POST https://api.exa.ai/contents` when the agent already knows the URLs and needs clean, LLM-ready extraction without running a new search. Start with one content mode: `highlights` for compact agent context, `text` for broad page context, or `summary` for Exa-side compression.

## Quick Start (cURL)

### Basic text extraction

```bash
curl -sS -X POST "https://api.exa.ai/contents" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{
    "urls": ["https://example.com"],
    "text": true
  }'
```

### Highlights with freshness control

```bash
curl -sS -X POST "https://api.exa.ai/contents" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{
    "urls": ["https://arxiv.org/abs/2307.06435"],
    "highlights": {
      "query": "methodology and results"
    },
    "maxAgeHours": 24,
    "livecrawlTimeout": 12000
  }'
```

## Endpoint

```text
POST https://api.exa.ai/contents
```

Authentication: `x-api-key: <API_KEY>` header. Exa also accepts `Authorization: Bearer <API_KEY>`, but prefer `x-api-key` in cURL examples for consistency.

Use this endpoint for known-URL extraction. If the agent needs discovery or ranking first, use `POST /search`.

## Parameters

### Core request parameters

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `urls` | string[] | Yes | - | URLs to extract content from. Use this for known URLs. |
| `text` | boolean or object | No | - | Return full page text as markdown. Object form supports `maxCharacters`, `includeHtmlTags`, `verbosity`, `includeSections`, and `excludeSections`. |
| `highlights` | boolean or object | No | - | Return key excerpts. Prefer `true` for agent workflows unless a custom focus is needed. |
| `summary` | boolean or object | No | - | Return per-page LLM summaries. Use when the caller wants Exa-side compression or structured extraction. |
| `maxAgeHours` | integer | No | - | Freshness control. `0` always live crawls; `-1` uses cache only; omit for default cache-first behavior with crawl fallback. |
| `livecrawlTimeout` | integer | No | `10000` | Timeout for live crawling in milliseconds. Use `10000` to `15000` for most freshness-sensitive calls. |
| `subpages` | integer | No | `0` | Number of linked subpages to crawl from each URL. |
| `subpageTarget` | string or string[] | No | - | Terms used to prioritize which subpages matter, such as `["api", "reference", "pricing"]`. |
| `extras.links` | integer | No | `0` | Number of links to extract from each page. |
| `extras.imageLinks` | integer | No | `0` | Number of image URLs to extract from each page. |
| `compliance` | string | No | - | Enterprise-only compliance mode, such as `hipaa`, when enabled for the account. |

### Text object options

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `maxCharacters` | integer | - | Character limit for returned text. Use this instead of `tokensNum`. |
| `includeHtmlTags` | boolean | `false` | Preserve HTML tags in output. |
| `verbosity` | string | `compact` | `compact`, `standard`, or `full`. Pair fresh section-aware extraction with `maxAgeHours: 0`. |
| `includeSections` | string[] | - | Only include selected sections: `header`, `navigation`, `banner`, `body`, `sidebar`, `footer`, `metadata`. |
| `excludeSections` | string[] | - | Exclude selected sections from the same section list. |

### Highlights object options

Prefer `highlights: true` for the highest-quality default. Only use object form when the agent needs a custom focus or budget.

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `query` | string | - | Custom query guiding which excerpts are returned. |
| `maxCharacters` | integer | - | Cap highlight characters per URL. Omit unless the caller has a strict budget. |

### Summary object options

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `query` | string | - | Custom query for the summary. |
| `schema` | object | - | JSON Schema for structured per-page summaries. |

## Content Modes

On `/contents`, `text`, `highlights`, and `summary` are top-level request fields.

| Mode | Best for | Notes |
| --- | --- | --- |
| `text` | Deep analysis and broad page context | Use `maxCharacters` to keep payloads bounded. |
| `highlights` | Agent workflows and factual lookups | Most token-efficient default. Excerpts are grounded in the source page. |
| `summary` | Compression or structured per-page extraction | Adds Exa-side synthesis per page. |

Avoid requesting multiple modes unless the caller truly needs multiple views of the same page.

## Freshness and Crawling

Use `maxAgeHours` as the normative freshness control.

| Value | Behavior |
| --- | --- |
| omitted | Use default cache-first behavior with crawl fallback when needed. |
| positive integer | Use cache if it is less than N hours old, otherwise live crawl. |
| `0` | Always live crawl. Highest freshness, higher latency. |
| `-1` | Cache only. Fastest, but fails if no cached content exists. |

Set `livecrawlTimeout` when live crawling should not block past a fixed budget.

### Subpages and extras

Use `subpages` and `subpageTarget` when linked pages matter.

```bash
curl -sS -X POST "https://api.exa.ai/contents" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{
    "urls": ["https://docs.example.com"],
    "text": {
      "maxCharacters": 5000
    },
    "subpages": 10,
    "subpageTarget": ["api", "reference", "guide"],
    "extras": {
      "links": 10,
      "imageLinks": 5
    }
  }'
```

Start with `subpages` around `5` to `10`, then increase only when the caller needs broader site coverage.

## Response Fields and Statuses

Inspect `statuses` even when the HTTP status is 200. The endpoint can succeed for one URL and fail for another in the same request.

```bash
curl -sS -X POST "https://api.exa.ai/contents" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{
    "urls": ["https://example.com", "https://bad.example"],
    "highlights": true
  }' | jq '{results, statuses}'
```

| Field | Type | Description |
| --- | --- | --- |
| `requestId` | string | Unique request identifier. |
| `results` | array | Extracted content result objects. |
| `results[].title` | string | Page title. |
| `results[].url` | string | Page URL. |
| `results[].publishedDate` | string or null | Estimated publication date when available. |
| `results[].author` | string or null | Author when available. |
| `results[].text` | string | Returned when `text` is requested. |
| `results[].highlights` | string[] | Returned when `highlights` is requested. |
| `results[].highlightScores` | number[] | Similarity scores for highlights. |
| `results[].summary` | string | Returned when `summary` is requested. |
| `results[].subpages` | array | Nested result objects from subpage crawling. |
| `results[].extras.links` | string[] | Extracted links when requested. |
| `statuses` | array | Per-URL success or error states. Always inspect this field. |
| `statuses[].id` | string | Requested URL. |
| `statuses[].status` | string | `success` or `error`. |
| `statuses[].error.tag` | string | Error type for failed URLs. |
| `statuses[].error.httpStatusCode` | integer or null | HTTP code associated with a per-URL failure. |
| `costDollars.total` | number | Total request cost when returned. |

Common per-URL error tags include `CRAWL_NOT_FOUND`, `CRAWL_TIMEOUT`, `CRAWL_LIVECRAWL_TIMEOUT`, `SOURCE_NOT_AVAILABLE`, `UNSUPPORTED_URL`, and `CRAWL_UNKNOWN_ERROR`.

## Anti-Patterns
- Keep `text`, `highlights`, and `summary` at the top level on `/contents`.
- Do not wrap extraction options in a `contents` object; that nesting belongs to `/search`.
- Do not assume HTTP 200 means every URL succeeded; inspect `statuses`.
- Do not send `stream: true`; `/contents` is not a streaming endpoint.
- Do not send `tokensNum`; use `text.maxCharacters` to cap extracted text.
- Do not use `useAutoprompt`, `numSentences`, `highlightsPerUrl`, or older `livecrawl` string values in new requests.
- Prefer `maxAgeHours` for freshness and pair it with `livecrawlTimeout` when crawl latency matters.
- Use `subpageTarget` with `subpages`; otherwise subpage selection is best effort.
- Pick one of `highlights`, `text`, or `summary` by default. Stack modes only when the caller truly needs multiple views of each page.

## Attribution

Ported from [exa-labs/agent-skills](https://github.com/exa-labs/agent-skills) - adapted for mktg's drop-in contract on 2026-07-18.

Upstream commit: 390ffee2d7e1d0dce2ed8efe4994c2b3c1c0173b

Drift detection: if the upstream skill changes, re-run `mktg-steal https://github.com/exa-labs/agent-skills` to evaluate the diff.
