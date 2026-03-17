---
name: context7
description: Query up-to-date library documentation and code examples before implementing features.
agents: [blaze, rex, nova, tap, spark, grizz, bolt, cleo, cipher, tess, morgan]
triggers: [documentation, docs, library, api, how to use, examples]
---

# Context7 (Library Documentation)

Use Context7 to query **up-to-date documentation** for any library before implementing code.

## Tools

| Tool | Purpose |
|------|---------|
| `context7_resolve_library_id` | Find the Context7 ID for a library |
| `context7_get_library_docs` | Query documentation for a specific topic |

## Workflow

**Always query docs before implementing:**

```
1. resolve_library_id({ libraryName: "effect typescript" })
   → Returns: /effect-ts/effect

2. get_library_docs({ 
     context7CompatibleLibraryID: "/effect-ts/effect", 
     topic: "schema validation" 
   })
   → Returns: Up-to-date documentation
```

## Common Library IDs

| Library | Context7 ID |
|---------|-------------|
| Effect | `/effect-ts/effect` |
| Better Auth | `/better-auth/better-auth` |
| Next.js | `/vercel/next.js` |
| React | `/facebook/react` |
| TanStack Query | `/tanstack/query` |
| Drizzle ORM | `/drizzle-team/drizzle-orm` |
| Elysia | `elysiajs` |
| Axum | `/tokio-rs/axum` |

## Best Practices

1. **Always resolve first** - Don't guess library IDs
2. **Be specific with topics** - "schema validation" not just "validation"
3. **Query before coding** - Get current patterns, not outdated knowledge
4. **Check multiple topics** - Query auth, then session, then middleware separately

## Example Queries

```
# React patterns
get_library_docs({ libraryId: "/facebook/react", topic: "useEffect cleanup" })

# Authentication
get_library_docs({ libraryId: "/better-auth/better-auth", topic: "next.js integration" })

# Type-safe APIs
get_library_docs({ libraryId: "/effect-ts/effect", topic: "tagged errors" })
```
