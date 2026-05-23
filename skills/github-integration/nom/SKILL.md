---
description: "Fetch recent GitHub activity from the Nom feed"
argument-hint: "[org/repo] [--search QUERY] [--type TYPE] [--org ORG] [--from DATE] [--to DATE] [--limit N] [--rss]"
allowed-tools: ["mcp_web_fetch"]
---

Fetch GitHub activity from Nom (beta.nomit.dev) and present it clearly.

Base URL: `https://beta.nomit.dev`

**Fetch method**: Use `mcp_web_fetch` to fetch URLs. Do not use curl or shell commands.

**Input validation** (always apply before building URLs):

- `org` and `repo`: Must match `^[a-zA-Z0-9][\w.-]*$` (alphanumeric, hyphens, underscores, dots). Reject or sanitize invalid input.
- Query params: Use proper URL encoding (e.g. encodeURIComponent) for search text and filter values.
- `limit`: Clamp to 1–100. Default 20.

$ARGUMENTS parsing rules:

- If the first argument looks like `org/repo` (contains `/`), use the repo feed at `/api/feed/{org}/{repo}`
- Otherwise use the global feed at `/api/feed`
- `--search TEXT` — free-text search (full-text on title/summary)
- `--type TYPE` — filter by event type: `pull_request`, `issue`, `release`, `push`
- `--org ORG` — filter by GitHub org (global feed only)
- `--from DATE` / `--to DATE` — date range (ISO 8601, e.g. 2026-01-01) (global feed only)
- `--limit N` — results to return (default 20, max 100)
- `--rss` — fetch RSS XML instead of JSON (repo feed: `/api/feed/{org}/{repo}/rss`; global: `/api/feed/rss`)

Build `q` for global feed by joining filters: e.g. `type:pull_request org:vercel from:2026-01-01` plus any `--search` text.

API endpoints (JSON):

- Global feed: `GET /api/feed`
- Repo feed: `GET /api/feed/{org}/{repo}`

RSS endpoints (if `--rss`):

- Global: `GET /api/feed/rss`
- Repo: `GET /api/feed/{org}/{repo}/rss`

Use mcp_web_fetch with the constructed URL. For JSON, present results as a clean readable summary. For each item show:

- Event type label (PR / Issue / Release / Push)
- Title as a markdown link to the URL
- One-line AI summary
- Author and timestamp (relative if possible)

Response shape: `{ items: [...], pagination: { offset, limit, has_more } }`. Each item has `id`, `type`, `org`, `repo`, `title`, `summary`, `url`, `author`, `contributors`, `updated_at`.

Example output format:

```
**PR** [Add turbo support](https://github.com/vercel/next.js/pull/123)
timneutkens · 2 hours ago
Adds experimental Turbo support to the build pipeline, cutting build times by ~40%.

**Release** [v14.2.0](https://github.com/vercel/next.js/releases/tag/v14.2.0)
vercel-release-bot · 1 day ago
Major release introducing partial pre-rendering and improved image optimisation.
```
