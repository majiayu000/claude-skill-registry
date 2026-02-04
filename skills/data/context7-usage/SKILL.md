---
# VERSION: 2.43.0
name: context7-usage
description: "Patterns for using Context7 MCP for library documentation (v2.25)"
---

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
Documentation retrieval should be precise, fast, and authoritative.

## Your Work, Step by Step
1. **Identify library**: Extract from the user’s request.
2. **Resolve ID**: Use Context7 to find the exact source.
3. **Query**: Ask for targeted, actionable guidance.
4. **Fallback**: Use MiniMax when Context7 lacks coverage.

## Ultrathink Principles in Practice
- **Think Different**: Prefer indexed docs over scraping.
- **Obsess Over Details**: Ensure the right library ID.
- **Plan Like Da Vinci**: Define the query before running it.
- **Craft, Don't Code**: Return only relevant excerpts.
- **Iterate Relentlessly**: Re-query for clarity.
- **Simplify Ruthlessly**: Avoid unnecessary searches.

# Context7 MCP Usage Patterns

## Overview

Context7 MCP provides indexed documentation for popular libraries and frameworks. It's more efficient than web scraping because it uses pre-indexed, structured documentation.

## Available Tools

| Tool | Purpose | Parameters |
|------|---------|------------|
| `mcp__plugin_context7_context7__resolve-library-id` | Find Context7 library ID | `libraryName`, `query` |
| `mcp__plugin_context7_context7__query-docs` | Query documentation | `libraryId`, `query` |

## Usage Pattern

```yaml
# Step 1: Resolve library ID
mcp__plugin_context7_context7__resolve-library-id:
  libraryName: "React"  # Extract from user query
  query: "useTransition hook usage"  # Full query for ranking

# Step 2: Query docs with resolved ID
mcp__plugin_context7_context7__query-docs:
  libraryId: "/vercel/next.js"  # From step 1
  query: "How to use useTransition hook"
```

## Decision Tree

```
Is this about a library/framework?
|
+-- YES --> Is it in Context7?
|   |
|   +-- YES --> Use Context7 MCP
|   |   1. resolve-library-id
|   |   2. query-docs
|   |
|   +-- NO --> Fallback to MiniMax MCP
|
+-- NO --> Use WebSearch (native) or MiniMax MCP
```

## Supported Libraries (Examples)

### Frontend
- React (`/facebook/react`)
- Next.js (`/vercel/next.js`)
- Vue.js (`/vuejs/vue`)
- Angular (`/angular/angular`)
- Svelte (`/sveltejs/svelte`)

### Languages
- TypeScript (`/microsoft/TypeScript`)
- JavaScript (MDN)

### Backend
- Node.js (`/nodejs/node`)
- Express (`/expressjs/express`)
- Fastify (`/fastify/fastify`)

### CSS/UI
- Tailwind CSS (`/tailwindlabs/tailwindcss`)
- Chakra UI (`/chakra-ui/chakra-ui`)

### Databases
- PostgreSQL
- MongoDB (`/mongodb/docs`)
- Redis

## Cost Optimization

| Approach | Token Usage | Quality |
|----------|-------------|---------|
| Context7 | ~50% less | High (official docs) |
| Web Search | Baseline | Variable |
| MiniMax | Baseline | High |

**Why Context7 saves tokens:**
- Pre-indexed documentation
- Structured responses
- No web scraping overhead
- Focused, relevant content

## Integration with Ralph Loop

```bash
# CLI usage
ralph library "React 19 useTransition"
ralph lib "Next.js 15 app router"
ralph docs "TypeScript generics"

# Slash command
/library-docs React hooks best practices
```

## Fallback Strategy

If Context7 doesn't have the library:
1. Log warning: "Library not found in Context7"
2. Fallback to `mcp__MiniMax__web_search`
3. Return results from MiniMax

## Best Practices

1. **Extract library name first** - Parse user query to identify the library
2. **Use full query for ranking** - Pass complete query to resolve-library-id
3. **Handle not-found gracefully** - Always have MiniMax fallback ready
4. **Combine with code examples** - Request code snippets in your prompt
