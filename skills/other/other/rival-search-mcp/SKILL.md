---
name: rival-search-mcp
description: "Deterministic deep research via RivalSearchMCP. 10 tools: 5-engine web search (DuckDuckGo/Bing/Yahoo/Mojeek/Wikipedia), 9-platform social search (Reddit/HN/StackOverflow/Dev.to/Medium/ProductHunt/Bluesky/Lobste.rs/Lemmy), 5-source news (Google/Bing/Guardian/GDELT/DDG), 5 academic DBs (OpenAlex/CrossRef/arXiv/PubMed/EuropePMC), GitHub search, website mapping, content extraction with OCR, and persistent research workspaces. No API keys required. Use when the user needs web research, competitive analysis, content discovery, or academic paper search."
---

# RivalSearchMCP

You have access to 10 research tools via the CLI at `scripts/cli.py`. Run all commands with `uv run scripts/cli.py`.

Every tool returns deterministic, auditable output. There is no in-server LLM — you're the one doing the synthesis.

## How to invoke tools

```bash
uv run scripts/cli.py call-tool <tool_name> --flag value
```

## Available tools

- `web_search` — concurrent search across DuckDuckGo, Bing, Yahoo, Mojeek, Wikipedia. Use for general web queries.
- `social_search` — Reddit, Hacker News, Stack Overflow, Dev.to, Medium, Product Hunt, Bluesky, Lobste.rs, Lemmy. Use for community discussions.
- `news_aggregation` — Google News, Bing News, The Guardian, GDELT, DuckDuckGo News. Use for current events. Accepts `--time-range day|week|month|anytime`.
- `github_search` — search public GitHub repos. Use for code, libraries, projects.
- `map_website` — crawl a site in `research` / `docs` / `map` mode. Use to explore site structure or documentation.
- `content_operations` — one tool, six ops (`retrieve`, `stream`, `analyze`, `extract`, `score`, `find_conflicts`). Use to get full page content, rate source quality, or surface disagreements between sources.
- `document_analysis` — extract text from PDFs, Word docs, images (image OCR via EasyOCR). Use for document processing.
- `research_topic` — two modes: `topic` (search + fetch + findings) and `entity` (fan out to 8 sources for a unified profile). Pass `--session-id` to auto-save findings.
- `scientific_research` — OpenAlex, CrossRef, arXiv, PubMed, Europe PMC (papers) + Kaggle, HuggingFace, Dataverse, Zenodo (datasets).
- `research_memory` — persistent workspaces with `start` / `add` / `get` / `list` / `delete`. Use to iterate research across calls.

## When to chain tools

- Found a URL from search? → `content_operations --operation retrieve --url <url>`
- Want to assess source trust before using results? → `content_operations --operation score --urls '[…]'`
- Two sources seem to disagree? → `content_operations --operation find_conflicts --urls '[…]'`
- Found a PDF link? → `document_analysis --url <url>`
- Need to explore a website? → `map_website --url <url> --mode docs`
- Doing iterative research? → `research_memory --operation start --topic "..."` once, then pass `--session-id` to `research_topic` on every call.
- Need a unified entity profile in one shot? → `research_topic --mode entity --topic "OpenAI"`

## Tool reference

For full flags, types, and defaults for each tool, read:

- [resources/search.md](resources/search.md) — web_search, social_search, news_aggregation, github_search, map_website
- [resources/content.md](resources/content.md) — content_operations, document_analysis
- [resources/research.md](resources/research.md) — research_topic, scientific_research, research_memory

## Output

All tools return structured text to stdout. Errors go to stderr. Exit codes: 0 success, 1 tool error, 2 connection failed.
