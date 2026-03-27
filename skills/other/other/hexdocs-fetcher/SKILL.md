---
name: hexdocs-fetcher
description: Fetches HexDocs documentation efficiently using WebFetch tool with automatic HTML-to-markdown conversion for context efficiency. Use this INSTEAD of direct WebFetch when looking up any Elixir library documentation on hexdocs.pm. Handles module docs, function docs, guides, and changelogs for any Hex package. Dramatically reduces token usage compared to raw HTML fetching.
effort: low
---

# HexDocs Fetcher

Efficiently fetch Elixir library documentation from hexdocs.pm using Claude Code's native `WebFetch` tool.

## Usage

When researching libraries, use `WebFetch`:

```
# Fetch library overview
WebFetch(
  url: "https://hexdocs.pm/oban",
  prompt: "Extract the main documentation, including module overview, installation instructions, and key functions. Format as clean markdown."
)

# Fetch specific module docs
WebFetch(
  url: "https://hexdocs.pm/phoenix_live_view/Phoenix.LiveView.html",
  prompt: "Extract the module documentation including all public functions, their specs, and examples."
)

# Fetch getting started guide
WebFetch(
  url: "https://hexdocs.pm/ecto/getting-started.html",
  prompt: "Extract the complete getting started guide content."
)
```

## Token Efficiency

WebFetch automatically converts HTML to markdown and extracts relevant content:

| Source | Raw HTML | With WebFetch | Benefit |
|--------|----------|---------------|---------|
| HexDocs page | ~80k tokens | ~15k tokens | **80% reduction** |
| Phoenix docs | ~120k tokens | ~25k tokens | **79% reduction** |
| README | ~20k tokens | ~8k tokens | **60% reduction** |

## Integration with hex-library-researcher

When evaluating libraries, fetch docs efficiently:

```
# Get library overview with focused extraction
WebFetch(
  url: "https://hexdocs.pm/oban",
  prompt: "Extract: 1) Installation instructions 2) Main features 3) Basic usage example"
)
```

## Common HexDocs URLs

```
# Library overview
https://hexdocs.pm/{library}

# Module documentation
https://hexdocs.pm/{library}/{Module}.html
https://hexdocs.pm/{library}/{Module.Submodule}.html

# Guides
https://hexdocs.pm/{library}/guides.html
https://hexdocs.pm/{library}/{guide-name}.html

# API reference
https://hexdocs.pm/{library}/api-reference.html
```

## Prompt Strategies

Use focused prompts for better extraction:

```
# For API docs
prompt: "Extract all public function docs with @spec and examples"

# For guides
prompt: "Extract the complete guide content preserving code examples"

# For troubleshooting
prompt: "Extract any troubleshooting sections, common errors, and FAQs"

# For configuration
prompt: "Extract configuration options and their defaults"
```

## Caching

WebFetch includes automatic 15-minute caching. When fetching the same URL multiple times in a session, results are cached automatically.

For longer persistence, save to planning directory:

```
# After fetching, write the result to a file
Write(
  file_path: ".claude/plans/{slug}/research/docs/oban.md",
  content: "{extracted content}"
)
```

## Tidewave Alternative

If Tidewave MCP is available, prefer `mcp__tidewave__get_docs` for exact version-matched documentation:

```
mcp__tidewave__get_docs(module: "Oban.Worker")
```

This fetches docs for the exact version in your `mix.lock`.
