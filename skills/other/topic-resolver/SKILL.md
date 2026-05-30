---
name: topic-resolver
description: "Pre-search topic resolution. Maps vague queries to concrete entities (GitHub orgs, X handles, subreddits, docs URLs) before searching. Run as first step of any research workflow to dramatically improve search precision."
---

# Topic Resolver

Before running any web search or research workflow, resolve the topic to concrete, searchable entities. One small LLM call upfront saves 10x the tokens in search noise.

## The Problem

Raw topic queries produce noisy results:

```
User: "latest in Next.js"
Raw search: "next.js latest" -> news articles, old tutorials, unrelated mentions
```

## The Solution

Resolve first, search second:

```
User: "latest in Next.js"
Step 1: Topic -> Entities
  Framework: Next.js 15
  Org: vercel/next.js (GitHub)
  Docs: https://nextjs.org/blog
  Community: r/nextjs (Reddit)
  Maintainer: @timneutkens (X)
  Release channel: github.com/vercel/next.js/releases

Step 2: Parallel searches on resolved entities
  - GitHub: vercel/next.js latest commits + releases
  - X: @timneutkens latest posts
  - Reddit: r/nextjs top this week
  - Docs: nextjs.org/blog latest entries
```

## Entity Categories

For any topic, resolve to these categories (only if applicable):

| Category | Example |
|----------|---------|
| **Official repo** | GitHub owner/repo |
| **Org account** | X/Twitter handle |
| **Docs URL** | Authoritative documentation |
| **Release channel** | RSS, changelog, release page |
| **Community** | Subreddit, Discord, forum |
| **Key maintainers** | Individual accounts (up to 3) |
| **Related packages** | npm, pip, cargo names |
| **Benchmarks** | Known comparison sites |

## Resolution Rules

1. **Use LLM knowledge first** - most entities are memorable (Next.js -> vercel/next.js is obvious)
2. **Only search when uncertain** - don't waste tokens resolving obvious mappings
3. **Cap at 8 entities** - more than that is noise
4. **Verify if critical** - for high-stakes research, confirm 1-2 entities via web fetch
5. **Cache resolutions** - topic -> entities cached in `~/.claude/topic-cache.jsonl`

## Output Format

```json
{
  "topic": "Next.js 15",
  "entities": {
    "repo": "vercel/next.js",
    "docs": "https://nextjs.org/docs",
    "blog": "https://nextjs.org/blog",
    "x_handles": ["@timneutkens", "@rauchg"],
    "subreddit": "r/nextjs",
    "npm": "next"
  },
  "confidence": 0.95,
  "resolved_at": "2026-04-12T04:00:00Z"
}
```

## Integration

- **oracle agent**: Calls topic-resolver first, then searches resolved entities
- **harvest agent**: Uses resolved entities as starting URLs for deep crawl
- **growth agent**: Uses resolved competitors/communities for market analysis

## When NOT to Use

- Very specific queries (already pointing at one thing)
- Internal/private topics (no public entities to resolve)
- Time-sensitive urgent research (skip the resolution step)

## Example Workflow

```
1. User: "whats happening with Astro framework"
2. topic-resolver:
   - repo: withastro/astro
   - docs: https://astro.build/blog
   - x: @astrodotbuild
   - subreddit: r/astrojs
3. oracle parallel search:
   - Latest commits on withastro/astro
   - Recent @astrodotbuild posts
   - r/astrojs top this week
   - Astro blog last 10 posts
4. Cluster results, return coherent update
```
