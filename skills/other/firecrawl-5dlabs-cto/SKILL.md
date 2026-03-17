---
name: firecrawl
description: Web scraping, content extraction, and autonomous research agent for deep web investigation.
agents: [blaze, rex, nova, tap, spark, grizz, morgan, cleo]
triggers: [scrape, crawl, website, url, web content, research, external docs, competitive analysis, deep research]
---

# Firecrawl (Web Scraping & Research)

Use Firecrawl to extract content from websites, perform web searches, and conduct autonomous deep research.

## Tools

| Tool | Purpose |
|------|---------|
| `firecrawl_scrape` | Extract content from a single URL |
| `firecrawl_crawl` | Crawl multiple pages from a domain |
| `firecrawl_map` | Discover all URLs on a website |
| `firecrawl_search` | Search the web and extract results |
| `firecrawl_agent` | **Autonomous research agent** - finds data anywhere on the web |

---

## Firecrawl Agent (Deep Research)

The `firecrawl_agent` tool is an autonomous research agent that searches, navigates, and gathers data from anywhere on the web. **No URLs required** - just describe what you need.

### When to Use Agent vs Other Tools

| Scenario | Tool | Why |
|----------|------|-----|
| Know the exact URL | `scrape` | Faster, cheaper |
| Need to explore a site | `map` + `scrape` | Controlled discovery |
| Simple web search | `search` | Quick results |
| **Don't know where data is** | `agent` | Autonomous navigation |
| **Competitive analysis** | `agent` | Multi-site research |
| **Complex research questions** | `agent` | Finds hard-to-reach data |

### Basic Usage

```
firecrawl_agent({
  prompt: "Find the founders of Firecrawl and their backgrounds"
})
```

### Structured Output with Schema

For structured data, provide a JSON schema:

```
firecrawl_agent({
  prompt: "Compare how Stripe, Auth0, and Clerk handle refresh token rotation",
  schema: {
    "type": "object",
    "properties": {
      "providers": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "approach": { "type": "string" },
            "token_lifetime": { "type": "string" },
            "rotation_strategy": { "type": "string" }
          },
          "required": ["name", "approach"]
        }
      }
    }
  }
})
```

### With Optional URLs (Focus the Agent)

When you have starting points but need deeper investigation:

```
firecrawl_agent({
  urls: ["https://docs.stripe.com/api", "https://auth0.com/docs"],
  prompt: "Compare the webhook retry strategies and timeout configurations"
})
```

### Research Patterns

#### Competitive Analysis
```
firecrawl_agent({
  prompt: "How do major auth providers (Auth0, Clerk, Supabase Auth) implement multi-tenant authentication? Focus on tenant isolation and session management.",
  schema: {
    "type": "object",
    "properties": {
      "providers": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": { "type": "string" },
            "tenant_isolation": { "type": "string" },
            "session_management": { "type": "string" },
            "tradeoffs": { "type": "string" }
          }
        }
      }
    }
  }
})
```

#### Implementation Research
```
firecrawl_agent({
  prompt: "Find production examples of Effect-TS being used with Drizzle ORM. Include code patterns and gotchas.",
  schema: {
    "type": "object",
    "properties": {
      "examples": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "source": { "type": "string" },
            "pattern": { "type": "string" },
            "code_snippet": { "type": "string" },
            "notes": { "type": "string" }
          }
        }
      }
    }
  }
})
```

#### Best Practices Discovery
```
firecrawl_agent({
  prompt: "What are industry best practices for WebSocket reconnection strategies? Include timeout values and backoff algorithms used by Pusher, Ably, and Socket.io."
})
```

### Cost Management

Agent pricing is dynamic based on complexity. Control costs with:

- **Specific prompts** - More specific = fewer credits
- **Schemas** - Structured output reduces processing
- **Focus with URLs** - Optional URLs narrow the search scope

---

## Single Page Scraping

```
firecrawl_scrape({
  url: "https://docs.example.com/api/auth",
  formats: ["markdown"]
})
```

Returns clean markdown content from the page.

## Website Discovery

```
# First, map the site to find relevant pages
firecrawl_map({
  url: "https://docs.example.com",
  limit: 50
})

# Then scrape specific pages
firecrawl_scrape({ url: "https://docs.example.com/guides/quickstart" })
```

## Web Search

```
firecrawl_search({
  query: "Effect TypeScript error handling patterns",
  limit: 5
})
```

## Best Practices

1. **Use Agent for unknowns** - When you don't know where data lives, let Agent find it
2. **Use scrape for knowns** - When you have the URL, scrape is faster and cheaper
3. **Map before crawl** - Discover URLs first, then selectively scrape
4. **Use markdown format** - Cleaner for LLM consumption
5. **Limit crawl depth** - Avoid token overflow with `limit` parameter
6. **Be specific with prompts** - Include library names, versions, and specific requirements

## Tool Selection Guide

| Task | Tool | Example |
|------|------|---------|
| Read known docs | `scrape` | API documentation at specific URL |
| Research patterns | `agent` | Find implementation examples anywhere |
| Site exploration | `map` + `scrape` | Understand a new library's docs |
| Quick web search | `search` | Find recent articles on a topic |
| PRD enrichment | `scrape` | Extract requirements from linked docs |
| Competitive analysis | `agent` | Compare how competitors solve problems |
| Deep research | `agent` | Technical investigation across multiple sources |