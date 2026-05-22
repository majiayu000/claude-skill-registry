---
name: vercel-llm-docs
description: Fetch LLM-optimized documentation for Vercel, the frontend cloud platform.
agents: [blaze, nova, bolt]
triggers: [vercel, vercel docs, deployment, hosting, edge functions, serverless]
llm_docs:
  - vercel
---

# Vercel Documentation (llms.txt)

Vercel is the platform for frontend developers, providing the speed and reliability to build and deploy web applications. This skill allows agents to fetch its LLM-optimized documentation.

## Usage

To get detailed documentation for Vercel, use the `firecrawl_scrape` tool:

```
firecrawl_scrape({ url: "https://vercel.com/llms.txt", formats: ["markdown"] })
```

## Key Features

- **Zero-config deployments** - Git push to deploy
- **Edge Network** - Global CDN with edge functions
- **Preview deployments** - Automatic PR previews
- **Analytics** - Built-in web vitals and analytics
- **AI SDK** - Tools for building AI applications

## Related Skills

- `shadcn-stack` - Next.js stack (optimized for Vercel)
- `turborepo-llm-docs` - Monorepo build system (Vercel product)
