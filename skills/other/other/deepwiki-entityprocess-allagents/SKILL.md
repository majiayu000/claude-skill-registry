---
name: deepwiki
description: AI-generated documentation for GitHub repositories
---

# DeepWiki MCP Tools

## When to Use
- Understanding a GitHub repository's architecture
- Cross-repo comparisons and Q&A
- Finding how a specific feature is implemented in a repo
- Getting an overview of unfamiliar codebases

## Available Tools
- `mcp__deepwiki__read_wiki_structure` — Get documentation topics for a repo
- `mcp__deepwiki__read_wiki_contents` — Read full documentation for a repo
- `mcp__deepwiki__ask_question` — Ask any question about a repo

## Query Strategies
- Start with `read_wiki_structure` to understand what documentation is available
- Use `ask_question` for specific implementation questions: "How does auth work in owner/repo?"
- For comparisons, ask about each repo separately then synthesize
- Repository names use `owner/repo` format (e.g., "langchain-ai/langchainjs")

## Limitations
- Free to use, no API key required
- Only works with public GitHub repositories
- Documentation is AI-generated and may miss recent changes
- Best for architecture-level understanding, not line-by-line code review
