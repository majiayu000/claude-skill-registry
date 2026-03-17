---
name: tavily-tools
type: complex
depth: base
user-invocable: false
description: >-
  Executes Tavily AI search, extraction, crawling, mapping, and deep research via Python CLI. Use when web search, URL content extraction, site crawling, or multi-step research needed.
---

# [H1][TAVILY-TOOLS]
>**Dictum:** *Command-specific arguments enforce correct invocation.*

<br>

Execute Tavily AI web operations through unified Python CLI.

[IMPORTANT] `search` requires `--query`; `extract` requires `--urls`; `crawl`/`map` require `--url`; `research` requires `--query`. 1Password injects API key automatically.

---
## [1][COMMANDS]

| [CMD]    | [REQUIRED_ARG] | [PURPOSE]                             |
| -------- | -------------- | ------------------------------------- |
| search   | `--query TEXT` | AI-powered web search with results    |
| extract  | `--urls URLS`  | Extract content from one or more URLs |
| crawl    | `--url URL`    | Crawl website from base URL           |
| map      | `--url URL`    | Map website URL structure             |
| research | `--query TEXT` | Multi-step deep research with report  |

---
## [2][USAGE]

```bash
# Search
uv run .claude/skills/tavily-tools/scripts/tavily.py search --query "Vite 7 new features"
uv run .claude/skills/tavily-tools/scripts/tavily.py search --query "React 19" --topic news
uv run .claude/skills/tavily-tools/scripts/tavily.py search --query "Effect-TS" --search-depth advanced --max-results 20

# Extract content from URLs
uv run .claude/skills/tavily-tools/scripts/tavily.py extract --urls "https://example.com"
uv run .claude/skills/tavily-tools/scripts/tavily.py extract --urls "https://a.com,https://b.com" --format text

# Crawl website
uv run .claude/skills/tavily-tools/scripts/tavily.py crawl --url "https://docs.effect.website"
uv run .claude/skills/tavily-tools/scripts/tavily.py crawl --url "https://nx.dev" --max-depth 3 --max-breadth 50

# Map site structure
uv run .claude/skills/tavily-tools/scripts/tavily.py map --url "https://nx.dev"
uv run .claude/skills/tavily-tools/scripts/tavily.py map --url "https://effect.website" --max-depth 2 --limit 200

# Deep research (multi-step, structured report)
uv run .claude/skills/tavily-tools/scripts/tavily.py research --query "Nx 22 migration strategies"
uv run .claude/skills/tavily-tools/scripts/tavily.py research --query "Effect vs RxJS comparison" --model pro
```

---
## [3][ARGUMENTS]

**search**: `--query TEXT [options]`
- `--query` — Search query (required)
- `--topic` — Topic: `general`, `news` (default: `general`)
- `--search-depth` — Depth: `basic`, `advanced` (default: `basic`)
- `--max-results` — Number of results (default: `10`)
- `--include-images` — Include images in results (flag)
- `--include-raw-content` — Include raw HTML (flag)
- `--include-domains` — Comma-separated whitelist
- `--exclude-domains` — Comma-separated blacklist
- `--time-range` — Time filter (e.g., `day`, `week`, `month`, `year`)
- `--country` — Country code for localized results

**extract**: `--urls URLS [options]`
- `--urls` — Comma-separated URLs (required)
- `--extract-depth` — Depth: `basic`, `advanced` (default: `basic`)
- `--format` — Output: `markdown`, `text` (default: `markdown`)
- `--include-images` — Include images (flag)

**crawl**: `--url URL [options]`
- `--url` — Base URL to crawl (required)
- `--max-depth` — Crawl depth (default: `1`)
- `--max-breadth` — Pages per depth level (default: `20`)
- `--limit` — Total page limit (default: `50`)
- `--allow-external` — Follow external links (flag)
- `--select-paths` — Comma-separated path filters
- `--instructions` — Natural language crawl instructions

**map**: `--url URL [options]`
- `--url` — Base URL to map (required)
- `--max-depth` — Map depth (default: `1`)
- `--max-breadth` — URLs per depth level (default: `20`)
- `--limit` — Total URL limit (default: `50`)
- `--allow-external` — Include external URLs (flag)

**research**: `--query TEXT [options]`
- `--query` — Research question (required)
- `--model` — Research agent: `mini`, `pro`, `auto` (default: `auto`)

---
## [4][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]      | [RESPONSE]                             |
| :-----: | ---------- | -------------------------------------- |
|   [1]   | `search`   | `{query, results[], images[], answer}` |
|   [2]   | `extract`  | `{urls[], results[], failed[]}`        |
|   [3]   | `crawl`    | `{base_url, results[], urls_crawled}`  |
|   [4]   | `map`      | `{base_url, urls[], total_mapped}`     |
|   [5]   | `research` | `{query, report, sources[]}`           |

---
## [5][ENVIRONMENT]

| [VAR]            | [REQUIRED] | [DESCRIPTION]                       |
| ---------------- | ---------- | ----------------------------------- |
| `TAVILY_API_KEY` | Yes        | Tavily API key (1Password injected) |

---
## [6][ERROR_HANDLING]

- HTTP errors print `[ERROR] <status>: <body>` and exit 1
- Rate limit (429): retry after backoff
- `extract` reports per-URL failures in `failed[]` array (partial success)
- `crawl`/`map` respect `--limit` to prevent runaway requests
- `research` uses extended timeout for multi-step processing
