---
name: web-research
description: "Guidelines for using web search and documentation lookup tools (WebSearch, WebFetch, context7 MCP). Use when agents need to verify technical claims, check library APIs, or research current tool capabilities."
durability: encoded-preference
---

# Web Research

## Tool Selection

### WebSearch
Use for broad questions where you need to discover information:
- Current state of tools, frameworks, or platform features
- Compatibility and support status
- Best practices and community patterns
- Feature announcements or changelogs

### WebFetch
Use when you have a specific URL to retrieve:
- Official documentation pages
- GitHub READMEs or issue threads
- Specification documents
- Fallback when context7 has no results for a library

### context7 (MCP)
Use for library-specific API verification:
1. `resolve-library-id` -- Find the library ID first
2. `query-docs` -- Query with a specific question about the library API

**When to use context7:**
- Verifying library-specific APIs that may have changed
- Checking correct usage patterns or configuration options
- Confirming parameter names, return types, or method signatures

**Do NOT use context7 for:**
- Well-established, stable APIs (basic JavaScript, SQL, HTTP)
- Simple operations Claude confidently knows
- Internal/project-specific code

## When NOT to Search

Do not search for information Claude confidently knows:
- Standard library APIs, basic language syntax
- General software engineering concepts
- Well-known design patterns
- Information already available in the codebase

## Graceful Degradation

If context7 MCP tools are unavailable (server not configured), fall back to WebFetch for official documentation URLs. Do not fail the workflow because of missing optional tools.

If WebSearch is unavailable, use WebFetch with known documentation URLs as a fallback.
