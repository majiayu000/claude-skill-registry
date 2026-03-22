---
name: search
description: Searches the web, legal databases, case law, patents, and case.dev knowledge base via the casedev CLI. Use when the user mentions "search", "legal research", "find cases", "case law", "patent search", "web search", "fetch URL", "webfetch", "legal skills", or needs to research legal topics, find similar cases, or retrieve web content.
---

# case.dev Search

Unified search across web, legal databases, case law, patents, vault contents, and the case.dev skills knowledge base.

Requires the `casedev` CLI. See `setup` skill for installation and auth.

## Web Search

```bash
casedev search web "employment discrimination California" --json
casedev search web "SEC enforcement actions 2024" --limit 20 --json
```

Flags:
- `--limit` / `-l` — max results (default: 10)
- `--news` — news articles instead of general web
- `--type` — explicit type: `search` or `news`
- `--include-domain` — restrict to domain(s), repeatable
- `--exclude-domain` — exclude domain(s), repeatable

## Web Fetch

Fetch and extract content from URLs:

```bash
casedev search webfetch "https://example.com/ruling.html" --json
```

Flags:
- `--livecrawl` — force live crawl instead of cache
- `--subpages` — also crawl linked subpages
- `--subpage-target N` — max subpages (default: 5)
- `--max-chars N` — truncate content
- `--timeout N` — livecrawl timeout in seconds (default: 30)
- `--context` — contextual hint for extraction
- `--no-summary` — skip summary generation
- `--no-highlights` — skip highlights extraction
- `--strict` — fail if any URL cannot be fetched
- `--fallback` — if fetch fails, fall back to web search

Multiple URLs: `casedev search webfetch URL1 URL2 --json`

## Legal Search

Find legal authorities by topic:

```bash
casedev search legal "breach of fiduciary duty" --json
casedev search legal "ERISA preemption" --jurisdiction "federal" --json
```

Flags:
- `--jurisdiction` — filter by jurisdiction
- `--limit` / `-l` — max results (default: 10)
- `--deep` — uses the research endpoint with multi-query analysis
- `--alt-query` — additional search queries for deep mode, repeatable

Deep mode example:
```bash
casedev search legal "force majeure pandemic" --deep \
  --alt-query "impossibility of performance COVID" \
  --alt-query "frustration of purpose" --json
```

## Case Search

Two modes — query-based and similarity-based:

### By query
```bash
casedev search cases "wrongful termination retaliation" --json
casedev search cases "patent infringement software" --jurisdiction "federal" --json
```

### By similarity (find cases similar to a known case)
```bash
casedev search cases --url "https://casetext.com/case/example-v-example" --json
casedev search cases --url "https://example.com/case" --after "2020-01-01" --json
```

Flags:
- `--jurisdiction` — filter by jurisdiction
- `--limit` / `-l` — max results (default: 10)
- `--url` — source case URL for similarity search
- `--after` — only cases published after this date (ISO format, similarity mode)

## Patent Search

```bash
casedev search patent "machine learning natural language processing" --json
```

Flags:
- `--assignee` — filter by patent assignee
- `--inventor` — filter by inventor name
- `--status` — application status filter
- `--type` — application type filter
- `--filing-from` — filing date range start
- `--filing-to` — filing date range end
- `--offset` — pagination offset (default: 0)
- `--limit` / `-l` — max results (default: 25)

## Vault Semantic Search

Search within vault documents (also available via `vaults` skill):

```bash
casedev search vault "indemnification clause" --vault VAULT_ID --json
```

See `vaults` skill for full vault search documentation.

## Skills Knowledge Base

Search and read from the case.dev legal skills knowledge base:

```bash
# Search skills
casedev skills search "contract review" --json
casedev search skills "deposition preparation" --json

# Read a specific skill
casedev skills read SKILL_SLUG --json
casedev skills read SKILL_SLUG --content-only
```

Skills search flags: `--limit` / `-l` (1-20, default: 10), `--show-summary`.

Skills read flags: `--no-references`, `--content-only`.

## Troubleshooting

**"Missing query"**: Provide the search query as a positional argument or with `--query "..."`.

**"Missing vault ID"** for vault search: Use `--vault VAULT_ID` or set focus.

**Web fetch unavailable**: Use `--fallback` to fall back to web search, or use `casedev search web` directly.

**No legal results**: Try broader terms, remove jurisdiction filter, or use `--deep` mode with `--alt-query` variations.
