---
name: supabase-llm-docs
description: Fetch LLM-optimized documentation for Supabase, the open-source Firebase alternative.
agents: [blaze, nova, tap, spark]
triggers: [supabase, supabase docs, backend as a service, baas, postgres, realtime]
llm_docs:
  - supabase
---

# Supabase Documentation (llms.txt)

Supabase is an open-source Firebase alternative providing database, authentication, storage, and realtime subscriptions. This skill allows agents to fetch its LLM-optimized documentation.

## Usage

To get detailed documentation for Supabase, use the `firecrawl_scrape` tool:

```
firecrawl_scrape({ url: "https://supabase.com/llms.txt", formats: ["markdown"] })
```

## Key Features

- **PostgreSQL Database** - Full Postgres with Row Level Security
- **Authentication** - Built-in auth with social providers
- **Storage** - S3-compatible object storage
- **Realtime** - PostgreSQL changes via WebSockets
- **Edge Functions** - Deno-based serverless functions
- **Vector/AI** - pgvector for embeddings

## Related Skills

- `better-auth` - Alternative auth framework
- `effect-patterns` - Effect TypeScript patterns
