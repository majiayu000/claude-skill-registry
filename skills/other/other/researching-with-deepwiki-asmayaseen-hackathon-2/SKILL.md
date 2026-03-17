---
name: researching-with-deepwiki
description: |
  Research GitHub, GitLab, and Bitbucket repositories using DeepWiki MCP server. Use when exploring
  unfamiliar codebases, understanding project architecture, or asking questions about how a specific
  open-source project works. Provides AI-powered repo analysis and RAG-based Q&A about source code.
  NOT for fetching library API docs (use fetching-library-docs instead) or local files.
---

# Researching with DeepWiki

Research and understand codebases using the DeepWiki MCP server.

## MCP Server Setup

Add to your Claude Code settings:

```bash
claude mcp add -s user -t http deepwiki https://mcp.deepwiki.com/mcp
```

Or add to `settings.json`:

```json
{
  "mcpServers": {
    "deepwiki": {
      "type": "http",
      "url": "https://mcp.deepwiki.com/mcp"
    }
  }
}
```

### Private Repositories

For private repos, use the Devin.ai endpoint with authentication:

```json
{
  "mcpServers": {
    "deepwiki": {
      "type": "http",
      "url": "https://mcp.devin.ai/deepwiki/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_DEVIN_API_KEY"
      }
    }
  }
}
```

---

## When to Use DeepWiki

| Scenario | Use DeepWiki? |
|----------|---------------|
| Exploring unfamiliar open-source codebase | Yes |
| Understanding project architecture | Yes |
| Finding how a feature is implemented | Yes |
| Generating documentation for a repo | Yes |
| Working with your own local code | No - use Glob/Grep |
| Quick file lookups in known structure | No - use Read tool |

---

## Core Capabilities

### 1. Repository Analysis

Ask DeepWiki to analyze any public repository:

```
"Analyze the architecture of github.com/vercel/next.js"
"How is the routing system implemented in github.com/remix-run/react-router?"
"What design patterns are used in github.com/anthropics/anthropic-sdk-python?"
```

### 2. Code Structure Understanding

Get insights into project organization:

```
"Explain the directory structure of github.com/langchain-ai/langchain"
"What are the main modules in github.com/fastapi/fastapi?"
"How are tests organized in github.com/pytest-dev/pytest?"
```

### 3. Feature Investigation

Understand how specific features work:

```
"How does streaming work in github.com/openai/openai-python?"
"Where is authentication handled in github.com/better-auth/better-auth?"
"How are middleware implemented in github.com/honojs/hono?"
```

### 4. Architecture Visualization

DeepWiki can generate Mermaid diagrams:

```
"Generate an architecture diagram for github.com/prisma/prisma"
"Show the data flow in github.com/trpc/trpc"
```

---

## Best Practices

### 1. Be Specific with Questions

```
# Good - specific question
"How does the caching system work in github.com/vercel/swr?"

# Less effective - too broad
"Tell me about github.com/vercel/swr"
```

### 2. Reference Specific Paths

```
# Good - targeted investigation
"Explain the src/core directory in github.com/pmndrs/zustand"

# Also good - feature-focused
"How is the middleware pattern implemented in github.com/pmndrs/zustand?"
```

### 3. Compare Implementations

```
"Compare how github.com/tanstack/query and github.com/vercel/swr handle cache invalidation"
```

### 4. Learn from Popular Projects

```
"What patterns from github.com/shadcn-ui/ui should I follow for my component library?"
```

---

## Common Use Cases

### Learning a New Framework

```
1. "Explain the core concepts of github.com/honojs/hono"
2. "How do I add middleware in github.com/honojs/hono?"
3. "Show example route handlers from github.com/honojs/hono"
```

### Debugging Integration Issues

```
1. "How does github.com/drizzle-team/drizzle-orm handle connection pooling?"
2. "What error types are thrown by github.com/drizzle-team/drizzle-orm?"
```

### Preparing for Contributions

```
1. "What's the contribution workflow for github.com/anthropics/claude-code?"
2. "How are issues labeled in github.com/anthropics/claude-code?"
3. "What testing patterns are used in github.com/anthropics/claude-code?"
```

---

## Supported Platforms

| Platform | URL Format |
|----------|------------|
| GitHub | `github.com/owner/repo` |
| GitLab | `gitlab.com/owner/repo` |
| Bitbucket | `bitbucket.org/owner/repo` |

---

## Limitations

- **Rate limits**: Public endpoint has usage limits
- **Private repos**: Requires Devin.ai API key
- **Large repos**: May take time to analyze
- **Real-time changes**: Cached analysis may not reflect latest commits

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ DeepWiki MCP server configured`

## If Verification Fails

1. Check: MCP server is configured in settings
2. Test: Try a simple query like "analyze github.com/anthropics/anthropic-sdk-python"
3. **Stop and report** if still failing

## References

- [DeepWiki](https://deepwiki.com) - Main service
- [MCP endpoint](https://mcp.deepwiki.com/mcp) - Public MCP server