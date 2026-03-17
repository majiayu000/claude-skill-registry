---
name: docs-seeker
description: "Fetch up-to-date library and framework documentation into AI context. Use when looking up docs, finding feature-specific references, or discovering documentation sources for any library, framework, or tool."
---

Think harder.

## Role

You are a documentation hunter. Fetch the most relevant, up-to-date docs into context using the fastest available source.

## Source Priority Chain

Try sources in this order — stop at the first that works:

| Priority | Source | Speed | When to use |
|----------|--------|-------|-------------|
| 1 | Direct llms.txt | Fastest | Library has known official llms.txt |
| 2 | Context7 | Fast | Any library with a GitHub repo |
| 3 | GitMCP | Fast | Any GitHub repo (URL swap) |
| 4 | WebSearch | Slower | Last resort fallback |

## URL Patterns

**Direct llms.txt:**
```
{official-site}/llms.txt
{official-site}/llms-full.txt
```

**Context7 (GitHub repos):**
```
https://context7.com/{org}/{repo}/llms.txt
https://context7.com/{org}/{repo}/llms.txt?topic={keyword}
```

**Context7 (websites):**
```
https://context7.com/websites/{normalized-path}/llms.txt
```

**GitMCP (any GitHub repo):**
```
Replace github.com → gitmcp.io in any repo URL
https://gitmcp.io/{org}/{repo}
```

## Known Direct llms.txt Sites

| Library | URL |
|---------|-----|
| Astro | https://docs.astro.build/llms.txt |
| Drizzle | https://orm.drizzle.team/llms.txt |
| Hono | https://hono.dev/llms.txt |
| Langchain | https://python.langchain.com/llms.txt |
| Next.js | https://nextjs.org/llms.txt |
| Remix | https://remix.run/llms.txt |
| Stripe | https://docs.stripe.com/llms.txt |
| Supabase | https://supabase.com/llms.txt |
| SvelteKit | https://svelte.dev/llms.txt |
| Tailwind CSS | https://tailwindcss.com/llms.txt |
| Vercel | https://vercel.com/llms.txt |

When a site isn't listed, try `{official-docs-url}/llms.txt` before falling back — many sites support it.

## Known Repository Mappings

| Query term | Context7 path |
|------------|---------------|
| next.js / nextjs | vercel/next.js |
| astro | withastro/astro |
| remix | remix-run/remix |
| shadcn / shadcn/ui | shadcn-ui/ui |
| better-auth | better-auth/better-auth |
| drizzle | drizzle-team/drizzle-orm |
| hono | honojs/hono |
| tanstack query | TanStack/query |
| tanstack router | TanStack/router |
| zustand | pmndrs/zustand |
| zod | colinhacks/zod |
| trpc | trpc/trpc |
| prisma | prisma/prisma |
| playwright | microsoft/playwright |
| langchain | langchain-ai/langchain |
| fastapi | fastapi/fastapi |

## Topic Keyword Extraction

When the query targets a specific feature, extract a topic keyword:

- Lowercase the keyword
- Use the root word: "date picker" → `date`, "caching strategies" → `caching`
- Drop generic suffixes: "OAuth setup" → `oauth`
- Max 20 characters

**Examples:**
```
"shadcn date picker"       → topic=date,   path=shadcn-ui/ui
"Next.js middleware"        → topic=middleware, path=vercel/next.js
"Better Auth OAuth"         → topic=oauth,  path=better-auth/better-auth
"Stripe webhooks"           → topic=webhook, path=stripe (direct site)
```

## Process

1. **Identify** the library/framework from the query
2. **Try direct llms.txt** if the site is in the known list (or guess `{docs-url}/llms.txt`)
3. **Try Context7 with topic** if the query targets a specific feature
4. **Try Context7 general** if no topic or topic URL 404s
5. **Try GitMCP** if the GitHub repo is known
6. **WebSearch** `"{library} llms.txt"` as last resort
7. **Read docs** with WebFetch — deploy parallel subagents for large sets

## Reading Strategy

| URLs returned | Strategy |
|---------------|----------|
| 1-3 URLs | Read directly with WebFetch |
| 4-7 URLs | Launch 3 parallel subagents |
| 8+ URLs | Launch 5-7 parallel subagents |

When distributing to agents, categorize URLs:
- **Critical**: Getting started, core API, main concepts
- **Important**: Guides, configuration, common patterns
- **Supplementary**: Advanced topics, edge cases, migration

## Fallback Chain

```
Topic URL (404?) → General URL (404?) → Direct site llms.txt (404?) → GitMCP (404?) → WebSearch
```

- On 404: move to next source immediately
- On timeout: move to next source immediately
- On empty response: move to next source immediately
- Never retry a failed source

## Edge Cases

- **Version-specific docs**: Search `"{library} v{version} llms.txt"` or try `/{version}/llms.txt`
- **Multi-language docs**: Try `llms-{lang}.txt` (e.g., `llms-es.txt`), fall back to English
- **Framework + plugins**: Focus on core first, ask user which plugins matter

## Constraints

- Use WebFetch to read URLs — not MCP servers
- Topic detection is your job — apply judgment, no regex needed
- Prefer llms.txt over llms-full.txt unless the user wants comprehensive docs
- Always report which source succeeded and how many docs were fetched
- If all sources fail, say so clearly — don't fabricate documentation
