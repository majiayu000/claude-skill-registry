---
name: rival-search-mcp
description: "Deep research and competitor analysis using RivalSearchMCP. 10 tools: web search (Yahoo/DuckDuckGo), social media (Reddit/HN/Dev.to), news aggregation, GitHub search, website mapping, content extraction with OCR, scientific papers (arXiv/PubMed), and AI research agent. No API keys required. Use when the user needs web research, competitive analysis, content discovery, or academic paper search."
---

# RivalSearchMCP

You have access to 10 research tools via the CLI at `scripts/cli.py`. Run all commands with `uv run scripts/cli.py`.

## How to invoke tools

```bash
uv run scripts/cli.py call-tool <tool_name> --flag value
```

## Available tools

- `web_search` — search Yahoo and DuckDuckGo. Use for general web queries.
- `social_search` — search Reddit, Hacker News, Dev.to, Product Hunt, Medium. Use for community discussions and opinions.
- `news_aggregation` — search Google News. Use for current events and recent coverage.
- `github_search` — search public GitHub repos. Use for finding code, libraries, projects.
- `map_website` — crawl and map a website. Use to explore site structure or documentation.
- `content_operations` — retrieve, analyze, or extract from a URL. Use to get full page content after finding URLs.
- `document_analysis` — extract text from PDFs, Word docs, images (OCR). Use for document processing.
- `research_topic` — automated multi-source research on a topic. Use for broad research.
- `scientific_research` — search arXiv, PubMed, Semantic Scholar, Kaggle, HuggingFace. Use for academic papers and datasets.
- `research_agent` — AI agent that orchestrates all tools autonomously. Use for comprehensive deep research. Requires OPENROUTER_API_KEY.

## When to chain tools

- Found a URL from search? → `content_operations --operation retrieve --url <url>`
- Found a PDF link? → `document_analysis --url <url>`
- Need to explore a website? → `map_website --url <url> --mode docs`
- Want everything at once? → `research_agent --topic <topic>`

## Tool reference

For full flags, types, and defaults for each tool, read:

- [resources/search.md](resources/search.md) — web_search, social_search, news_aggregation, github_search, map_website
- [resources/content.md](resources/content.md) — content_operations, document_analysis
- [resources/research.md](resources/research.md) — research_topic, scientific_research, research_agent

## Output

All tools return structured text to stdout. Errors go to stderr. Exit codes: 0 success, 1 tool error, 2 connection failed.
