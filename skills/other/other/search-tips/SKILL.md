---
name: search-tips
description: >
  This skill should be used when performing web research beyond a simple single search -- looking
  into topics, comparing options, investigating questions, finding recommendations, or any task
  where effective use of Exa, Firecrawl, and Reddit tools matters. Triggers on "research",
  "look into", "investigate", "compare", "find out about", "search for", "find information",
  "what do people think about", "what are the best", "look up", or multi-source search tasks.
  Also invocable explicitly by deep-research team members via the Skill tool.
---

# Search Tips

Accumulated guidance for web research using Exa, Firecrawl CLI, and Reddit MCP tools. These
are **starting points, not rigid rules** -- think strategically about each situation and
adapt. If a different approach makes more sense for what you're trying to do, go with it.
Run `npx firecrawl-cli <command> --help` to check available options beyond what's documented
here. Reference files cover tool-specific deep dives -- see bottom of this file.

## Setup

Before starting research, load the required MCP tools using ToolSearch:

1. **Exa tools** -- `web_search_advanced_exa` and `get_code_context_exa`
2. **Reddit tools** -- `get_top_posts`, `get_post_comments`, `get_reddit_post`, `get_subreddit_info`

Firecrawl CLI (`npx firecrawl-cli`) runs via Bash -- no MCP setup needed. Load only what
the task requires.

## The Research Cycle

Prefer Exa and Firecrawl over built-in WebSearch/WebFetch.

Research alternates between **searching** (discovering sources) and **fetching** (extracting
content from them). Find promising leads, read the best ones, refine your understanding,
search again.

### Searching

Finding sources you don't have yet.

- **Exa search** (`web_search_advanced_exa`) -- primary tool for web discovery. Natural
  language queries, add filters as needed (domains, dates, categories).
- **Exa code context** (`get_code_context_exa`) -- programming topics. Worth trying before
  general Exa search for technical/code tasks -- surfaces repos, packages, and docs.
- **Firecrawl CLI search** (`npx firecrawl-cli search`) -- Google-powered keyword search.
  Useful when keyword matching works better than Exa's semantic approach, for site-scoped
  queries (`site:reddit.com {query}`), and for content-type filtering (`--categories research`
  for academic, `--sources news`, `--tbs qdr:w` for time).

**Default Exa search pattern:** Default to `enableHighlights: true` and `textMaxCharacters: 1`.
This returns quoted passages from actual page text while preventing the MCP server from
flooding context with full text. Use `highlightsPerUrl` and `highlightsNumSentences` to
control volume if needed.

### Fetching

Extracting content from a source you've identified.

- **Firecrawl CLI scrape** (`npx firecrawl-cli scrape "<url>" --only-main-content`) -- primary
  tool for reading a known URL. The flag strips nav/sidebars to save tokens.
- **Reddit MCP** (`get_post_comments`, `get_reddit_post`) -- for reading Reddit threads.
  Firecrawl can't scrape reddit.com directly.
- **Firecrawl CLI map** (`npx firecrawl-cli map "<url>" --search "query"`) -- discover URLs
  on a site (useful when you need to find the right page, or when scrape returns empty).

### Adapting the Workflow

The defaults above won't always be right. Some common deviations:

- **Exa full text as a scraping fallback** -- some sites are blocked or inaccessible via
  Firecrawl (LinkedIn, Twitter/X, etc.), but Exa often has the full page text in its index.
  Drop both `enableHighlights` and `textMaxCharacters: 1` to get the complete text. Be aware
  this can produce large responses.
- **`--only-main-content` can strip too much** -- if you got empty or partial results, retry
  without the flag. Known to fail on Future plc sites, Blogspot, and GDPR-heavy sites. See
  Content Extraction below.

The reference files cover more edge cases -- scraping issues, category restrictions, and
academic search.

## Search Strategy

### How Exa Works

Exa is a **neural/semantic search engine**. It uses embeddings to understand meaning.

- **Natural questions or statements work best** -- Exa finds pages that answer them
- **Longer, more specific queries work BETTER** -- unlike keyword-based search
- **Keyword lists tend to confuse** the semantic model

Good: "What do professional reviewers say are the most reliable dishwasher brands in 2025?"
Bad: "best dishwasher 2025 reliable"

### Query Reformulation

For broad topics, Exa's `additionalQueries` parameter can automate this -- it bundles query
variations in a single call at no extra cost (see `references/exa-tips.md`). For manual
reformulation, try generating 3-5 query variations:

| Technique             | What It Does                          | Example                                      |
| --------------------- | ------------------------------------- | -------------------------------------------- |
| **Paraphrase**        | Same meaning, different words         | "RAG failures" -> "problems in RAG systems"  |
| **Decompose**         | Break into sub-questions              | "Why fail?" -> "Why return irrelevant docs?" |
| **Scope shift**       | Broader context or narrower specifics | "Challenges in production AI search"         |
| **Perspective shift** | Different viewpoints                  | User vs expert vs critic view                |
| **Temporal framing**  | Target different time periods         | "Recent 2024-2025" vs "foundational"         |

### Domain Filtering

Try `includeDomains` when the authoritative site for a topic is known -- faster and less noisy
than broad search. Try `excludeDomains` to suppress sites that keep appearing but aren't
useful (e.g., exclude `youtube.com` when video pages crowd out needed editorial content about 
YouTube creators/content).

### Searching by Content Type

Match your research target to the right approach. Reference files have full strategies.

- **Social sentiment / opinions** -- Exa `tweet` for Twitter; `site:reddit.com` via Firecrawl
  search + Reddit MCP for discussions. See `references/twitter.md`, `references/reddit.md`.
- **People / companies** -- Exa `people` or `company` category for discovery, then broaden.
  See `references/people-companies.md`.
- **Academic papers** -- Exa `research paper` category; academic APIs for structured data.
  See `references/academic-search.md`.
- **Code / GitHub** -- `get_code_context_exa` for code; `gh api` for repo data.
  See `references/code-github.md`.
- **News** -- Exa `news` category with date filters; Firecrawl CLI
  `search --sources news --tbs qdr:w` for Google News with time filtering.
- **Financial reports** -- Exa `financial report` with domain/date filtering.
- **Personal blogs / independent takes** -- Exa `personal site` for practitioner opinions,
  blog posts, and independent analysis. Full parameter support (unlike most specialized
  categories). See `references/personal-sites.md`.

Some categories reject certain parameters (400/500 errors). See `references/exa-tips.md`.

## Content Extraction

Always use `--only-main-content` by default -- it strips nav, sidebars, and footers, saving
significant tokens. If you get empty or partial results, retry without the flag; it's known
to strip article bodies on Future plc sites (iMore, Pocket-lint), GDPR-heavy sites
(StorageReview), and Blogspot blogs -- see `references/scraping-issues.md`.

For even narrower extraction, use `--include-tags` (e.g., `--include-tags "article"`,
`--include-tags ".post-content"`).

## Scraping Issues

When Firecrawl scrape fails (policy blocks, paywalls, SPA rendering), check
`references/scraping-issues.md` for per-site workarounds. General fallback: try Exa full text
(drop `enableHighlights` and `textMaxCharacters`). For interactive pages that need clicks or
form fills, escalate to `npx firecrawl-cli browser` (see `references/firecrawl-tips.md`).

## Operational Notes

**Parallel call failures:** If any tool call in a parallel batch fails, all sibling calls
fail too. Retry individually. Keep failure-prone calls (Reddit MCP) in their own batch.

**Rate limits:** Retry once after a short pause. If still blocked, try a different tool for the
same intent before giving up -- Exa rate-limited? Try Firecrawl search. Reddit MCP throttled?
Try Exa with `includeDomains: ["reddit.com"]`. Only note the gap and move on after both the
original tool and an alternative have failed.

## Reference Files

### Content-type strategies
- **`references/twitter.md`** -- Exa tweet category, restrictions, query tips, livecrawl
- **`references/reddit.md`** -- Discovery via Firecrawl search, Reddit MCP for reading,
  batching gotchas, rate limits
- **`references/people-companies.md`** -- Exa people/company categories, LinkedIn, multi-
  category approach
- **`references/code-github.md`** -- Code search, GitHub repos/issues, gh api, raw URLs
- **`references/personal-sites.md`** -- Independent blogs, practitioner opinions, full
  parameter support, portfolio exploration
- **`references/academic-search.md`** -- Academic domains, free APIs, Firecrawl CLI

### Tool reference
- **`references/exa-tips.md`** -- Category restrictions, additionalQueries,
  highlights/summaries
- **`references/firecrawl-tips.md`** -- CLI commands (search, scrape, map, crawl, download,
  browser), PDF scraping, arxiv extraction, MCP fallback notes

### Troubleshooting
- **`references/scraping-issues.md`** -- main-content detection fixes, paywalls, Discourse
  JSON, policy-blocked sites, API workarounds
