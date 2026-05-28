---
name: search
description: Search codebase semantically by concept or functionality. Use when looking for code related to a topic, feature, or pattern rather than exact text matches.
---

# Semantic Code Search

Search the codebase using Mira's semantic search to find code by meaning, not just text.

**Query:** $ARGUMENTS

## Instructions

1. Use the `mcp__mira__search_code` tool with the query provided above
2. Set an appropriate limit (default: 10 results)
3. Present results clearly with:
   - File path and line numbers
   - Relevance score
   - Code snippet preview
4. Group related results if they're from the same module
5. Suggest follow-up searches if results seem incomplete

## Example Usage

```
/mira:search authentication middleware
/mira:search error handling patterns
/mira:search database connection pooling
```
