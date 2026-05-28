---
name: llm-docs
description: Fetch LLM-optimized documentation from llms.txt endpoints for up-to-date API references
agents: [blaze, rex, nova, tap, spark, grizz, bolt, cleo, cipher, tess, morgan, atlas, stitch]
triggers: [llms.txt, documentation, official docs, framework docs, api reference]
---

# LLM Documentation (llms.txt)

Many libraries provide LLM-optimized documentation at `/llms.txt` following the [llms.txt standard](https://llmstxt.org/).

## Available Sources

| Library | llms.txt URL | Full Version |
|---------|-------------|--------------|
| shadcn/ui | https://ui.shadcn.com/llms.txt | - |
| Effect | https://effect.website/llms.txt | https://effect.website/llms-full.txt |
| Drizzle ORM | https://orm.drizzle.team/llms.txt | https://orm.drizzle.team/llms-full.txt |
| TanStack | https://tanstack.com/llms.txt | - |
| Better Auth | https://www.better-auth.com/llms.txt | - |
| Elysia | https://elysiajs.com/llms.txt | - |
| Bun | https://bun.sh/llms.txt | - |
| Hono | https://hono.dev/llms.txt | https://hono.dev/llms-full.txt |
| Expo | https://docs.expo.dev/llms.txt | - |
| React Native | https://reactnative.dev/llms.txt | - |
| Zod | https://zod.dev/llms.txt | - |
| Prisma | https://www.prisma.io/llms.txt | - |
| tRPC | https://trpc.io/llms.txt | - |
| Turborepo | https://turbo.build/llms.txt | - |
| Supabase | https://supabase.com/llms.txt | - |
| Vercel | https://vercel.com/llms.txt | - |
| Stripe | https://stripe.com/llms.txt | - |
| Clerk | https://clerk.com/llms.txt | - |
| Vitest | https://vitest.dev/llms.txt | - |

## When to Use llms.txt

Use llms.txt when:
- **Starting work with a library** - Get the architectural overview first
- **Context7 lacks recent updates** - llms.txt is always current
- **You need official API reference links** - llms.txt links to authoritative docs
- **Understanding library structure** - See what sections/features exist

## llms.txt vs Context7

| Aspect | llms.txt | Context7 |
|--------|----------|----------|
| **Source** | Official project files | Indexed documentation |
| **Granularity** | Full overview + links | Query-based chunks |
| **Freshness** | Always current | Depends on indexing |
| **Best for** | Architecture overview | Specific API questions |

**Recommended workflow:** Start with llms.txt for overview, then use Context7 for specific implementation details.

---

## Workflow

### 1. Fetch llms.txt for Overview

Use Firecrawl to fetch the llms.txt file:

```
firecrawl_scrape({ 
  url: "https://effect.website/llms.txt",
  formats: ["markdown"]
})
```

This returns a structured overview with:
- Project description
- Key documentation sections
- Links to important resources

### 2. Fetch Full Documentation (if available)

For deeper context, some libraries provide `llms-full.txt`:

```
firecrawl_scrape({ 
  url: "https://effect.website/llms-full.txt",
  formats: ["markdown"]
})
```

**Note:** Full versions can be large. Only fetch when you need comprehensive documentation.

### 3. Follow Up with Context7

After understanding the structure from llms.txt, query specific topics:

```
context7_resolve_library_id({ libraryName: "effect typescript" })
→ /effect-ts/effect

context7_get_library_docs({ 
  libraryId: "/effect-ts/effect",
  topic: "schema validation with branded types"
})
```

---

## Quick Reference

### Frontend & UI
```
firecrawl_scrape({ url: "https://ui.shadcn.com/llms.txt" })     # shadcn/ui
firecrawl_scrape({ url: "https://tanstack.com/llms.txt" })      # TanStack (Router, Query, Table)
```

### TypeScript Ecosystem
```
firecrawl_scrape({ url: "https://effect.website/llms.txt" })    # Effect TypeScript
firecrawl_scrape({ url: "https://zod.dev/llms.txt" })           # Zod schema validation
firecrawl_scrape({ url: "https://trpc.io/llms.txt" })           # tRPC typesafe APIs
```

### Web Frameworks
```
firecrawl_scrape({ url: "https://elysiajs.com/llms.txt" })      # Elysia (Bun framework)
firecrawl_scrape({ url: "https://hono.dev/llms.txt" })          # Hono (Web Standards)
firecrawl_scrape({ url: "https://bun.sh/llms.txt" })            # Bun runtime
```

### Database & ORM
```
firecrawl_scrape({ url: "https://orm.drizzle.team/llms.txt" })  # Drizzle ORM
firecrawl_scrape({ url: "https://www.prisma.io/llms.txt" })     # Prisma ORM
firecrawl_scrape({ url: "https://supabase.com/llms.txt" })      # Supabase
```

### Authentication
```
firecrawl_scrape({ url: "https://www.better-auth.com/llms.txt" }) # Better Auth
firecrawl_scrape({ url: "https://clerk.com/llms.txt" })           # Clerk
```

### Mobile & React Native
```
firecrawl_scrape({ url: "https://docs.expo.dev/llms.txt" })     # Expo
firecrawl_scrape({ url: "https://reactnative.dev/llms.txt" })   # React Native
```

### Infrastructure & Deployment
```
firecrawl_scrape({ url: "https://vercel.com/llms.txt" })        # Vercel
firecrawl_scrape({ url: "https://turbo.build/llms.txt" })       # Turborepo
```

### Payments
```
firecrawl_scrape({ url: "https://stripe.com/llms.txt" })        # Stripe
```

### Testing
```
firecrawl_scrape({ url: "https://vitest.dev/llms.txt" })        # Vitest
```

---

## Best Practices

1. **Check llms.txt first** - Before diving into code, understand the library structure
2. **Use the registry** - Reference `llm-docs-registry.yaml` for known URLs
3. **Prefer llms.txt over scraping random pages** - It's curated for LLM consumption
4. **Combine sources** - llms.txt → Context7 → specific doc pages
5. **Cache when appropriate** - For repeated work, save llms.txt content locally
