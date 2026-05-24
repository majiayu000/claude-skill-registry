---
name: exa-research
description: Comprehensive research skill using Exa AI tools for web search and code context retrieval. Use when conducting research on technologies, finding code examples, discovering latest tools, or gathering comprehensive information on any topic. Combines web search for articles/news with code search for implementation examples.
---

# Exa Research

## Overview

Enable comprehensive research using Exa AI's powerful search capabilities. This skill provides workflows for web research, code discovery, and combined research strategies using two primary tools.

## When to Use This Skill

Use this skill when researching new technologies, finding code examples, discovering latest trends, gathering comprehensive information on technical topics, comparing solutions, or learning how to implement specific features.

## Core Capabilities

### 1. Web Research (exa_web_search)

Search the web for articles, news, documentation, and general information.

**Best for:** Latest news and trends, product comparisons, technology overviews, blog posts and articles, documentation and guides

**Key Parameters:**
- query (required): Search query
- numResults (optional): Number of results (default: 8, max: 50)
- type (optional): Search depth - "auto" (balanced), "fast" (quick), "deep" (comprehensive, recommended)
- livecrawl (optional): "fallback" (backup) or "preferred" (prioritize fresh content)
- contextMaxCharacters (optional): Max context length (default: 10000)

**Example Usage:**
```python
from servers.exa import exa_web_search

# Quick research
result = await exa_web_search("latest AI tools 2025", numResults=10)

# Deep research with live crawling
result = await exa_web_search(
    query="Next.js 15 new features",
    numResults=20,
    type="deep",
    livecrawl="preferred",
    contextMaxCharacters=15000
)
```

### 2. Code Discovery (exa_get_code_context)

Search for code examples, implementation patterns, and technical documentation from open source repositories.

**Best for:** Code examples and snippets, implementation patterns, API usage examples, framework-specific code, library documentation, real-world implementations

**Key Parameters:**
- query (required): Search query describing what code you need
- tokensNum (optional): Token count (1000-50000, default: 5000)
  - Use 2000-3000 for focused examples
  - Use 5000-8000 for comprehensive documentation
  - Use 10000+ for extensive research

**Example Usage:**
```python
from servers.exa import exa_get_code_context

# Find specific examples
code = await exa_get_code_context(
    query="React useState hook examples",
    tokensNum=3000
)

# Comprehensive documentation
code = await exa_get_code_context(
    query="Next.js Better Auth complete setup guide",
    tokensNum=10000
)
```

## Research Workflows

### Workflow 1: Technology Research

When researching a new technology, framework, or tool:

1. Start with web search to understand the landscape
2. Get code examples to see implementation
3. Find latest updates with live crawling

### Workflow 2: Implementation Research

When learning how to implement a specific feature:

1. Search for implementation guides
2. Get working code examples

### Workflow 3: Comparison Research

When comparing different solutions:

1. Search for comparisons
2. Get code examples for each solution

### Workflow 4: Discovery Research

When discovering new tools or trends:

1. Search for latest tools
2. Get implementation examples for interesting finds

## Query Optimization Tips

### Web Search Queries

**Good queries:**
- "latest AI coding tools 2025" (specific, timely)
- "Next.js 15 new features comparison" (focused, comparative)
- "React Server Components best practices" (specific topic)

**Avoid:**
- "AI tools" (too broad)
- "programming" (too generic)
- Single words without context

**Tips:**
- Include year for latest information
- Use specific technology names
- Add context words: "latest", "best", "comparison", "guide"
- Combine related terms

### Code Search Queries

**Good queries:**
- "React useState hook examples" (specific API)
- "Next.js Better Auth implementation setup" (specific use case)
- "FastAPI authentication middleware patterns" (specific pattern)

**Avoid:**
- "React code" (too broad)
- "authentication" (needs framework context)
- "how to code" (too generic)

**Tips:**
- Include framework/library name
- Specify the feature or API
- Add context: "examples", "implementation", "setup", "configuration"
- Be specific about what you want to learn

## Best Practices

### Token Management

- Web search: Use higher numResults (15-20) for comprehensive research
- Code search: Adjust tokensNum based on need (2000-3000 for quick, 5000-8000 for standard, 10000+ for deep)

### Search Strategy

1. Start broad, then narrow
2. Use both tools: Combine web search with code search
3. Iterate: Refine queries based on initial results
4. Fresh content: Use livecrawl="preferred" for latest information

### Result Processing

- Web results: Focus on recent dates, authoritative sources
- Code results: Look for complete examples, not just snippets
- Combine insights: Merge web context with code examples

## Common Use Cases

### Use Case 1: Learning a New Framework
```python
# Get overview
overview = await exa_web_search("Next.js 15 overview features", numResults=10, type="deep")

# Get starter code
starter = await exa_get_code_context("Next.js 15 getting started tutorial", tokensNum=8000)

# Find best practices
practices = await exa_web_search("Next.js 15 best practices 2025", numResults=8)
```

### Use Case 2: Solving a Specific Problem
```python
# Search for solutions
solutions = await exa_web_search("how to fix [error] in [framework]", numResults=10)

# Get working code
code = await exa_get_code_context("[framework] [problem] solution examples", tokensNum=5000)
```

### Use Case 3: Staying Current
```python
# Latest news
news = await exa_web_search(
    "latest [technology] updates 2025",
    numResults=15,
    livecrawl="preferred"
)

# New features code
features = await exa_get_code_context("[technology] new features examples", tokensNum=5000)
```

## Resources

See scripts/ directory for helper utilities:
- research_workflow.py - Automated multi-step research workflows
- query_optimizer.py - Query optimization and suggestion tool

See references/ directory for detailed guides:
- search_strategies.md - Advanced search strategies and patterns
- query_patterns.md - Effective query patterns with examples

## Quick Reference

Import the tools:
```python
from servers.exa import exa_web_search, exa_get_code_context
```

Basic web search:
```python
result = await exa_web_search("your query", numResults=10)
```

Basic code search:
```python
code = await exa_get_code_context("your query", tokensNum=5000)
```

Combined research:
```python
# Get context
context = await exa_web_search("topic overview", numResults=10, type="deep")

# Get code
code = await exa_get_code_context("topic implementation examples", tokensNum=8000)
```

