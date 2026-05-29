---
name: mcp-brave-search
description: This skill provides guidance for using Brave Search MCP to search the web. Use when searching for current information, news, articles, local businesses, or any web content. Supports both general web searches and location-based local searches.
---

# Brave Search MCP

## Overview

This skill enables web searching using the Brave Search API through MCP. Brave Search provides privacy-focused web search capabilities including general web searches and local business searches.

## When to Use This Skill

- Searching for current information and news
- Finding documentation and tutorials
- Researching technologies and libraries
- Finding local businesses and services
- Getting up-to-date information beyond knowledge cutoff

## Available Tools

### brave_web_search

Perform a general web search.

**Tool:** `mcp__brave-search__brave_web_search`

**Parameters:**
- `query` (required): Search query (max 400 chars, 50 words)
- `count` (optional): Number of results (1-20, default 10)
- `offset` (optional): Pagination offset (max 9, default 0)

**Example:**
```
mcp__brave-search__brave_web_search({
  query: "xterm.js WebGL addon tutorial",
  count: 10
})
```

### brave_local_search

Search for local businesses and places.

**Tool:** `mcp__brave-search__brave_local_search`

**Parameters:**
- `query` (required): Local search query (e.g., "pizza near Central Park")
- `count` (optional): Number of results (1-20, default 5)

**Example:**
```
mcp__brave-search__brave_local_search({
  query: "coffee shops near Shibuya Tokyo",
  count: 5
})
```

## Common Workflows

### Research a Technology

```
mcp__brave-search__brave_web_search({
  query: "VS Code extension development best practices 2024",
  count: 10
})
```

### Find Latest Information

```
mcp__brave-search__brave_web_search({
  query: "xterm.js latest release features",
  count: 5
})
```

### Find Error Solutions

```
mcp__brave-search__brave_web_search({
  query: "WebGL context lost xterm.js solution",
  count: 10
})
```

### Local Business Search

```
mcp__brave-search__brave_local_search({
  query: "coworking space near Shinjuku",
  count: 5
})
```

## Best Practices

1. **Be specific**: Include relevant keywords for better results
2. **Use quotes**: For exact phrase matching, use quotes in query
3. **Include year**: Add current year for recent information
4. **Use local search appropriately**: Only use `brave_local_search` for location-based queries
5. **Paginate results**: Use `offset` to get more results beyond the first page

## References

For detailed tool parameters, see `references/tools.md`.
