---
name: web-rag
description: (ePost) Use when searching web codebase for components, design tokens, Next.js patterns, or any luz_next implementation via vector search
user-invocable: false

metadata:
  agent-affinity: [epost-muji, epost-fullstack-developer, epost-planner, epost-researcher]
  keywords: [rag, vector-search, klara-theme, luz-next, web, components, design-tokens, patterns, implementation]
  platforms: [web]
  triggers: [search components, find component, klara-theme, design token, luz_next, web pattern, implementation]
  connections:
    enhances: [web-frontend]
---

# Web RAG Skill

## Purpose

Vector search for the web codebase. Semantic search across luz_next application code, klara-theme component libraries, design tokens, and implementation patterns via MCP tools.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `query` | Semantic search — returns code chunks with relevance scores |
| `status` | Health check, indexed modules, document counts |
| `catalog` | List available components/hooks/styles per module (no vector search) |
| `navigate` | O(1) shortcut to known code locations |
| `expansions` | Component alias mappings + synonym groups for query planning |

Tool parameters are self-describing — check inputSchema for current options.

## Discovery Protocol

Before querying, discover what's indexed:

1. **Call `status`** — returns available modules, document counts, health
2. **Call `catalog`** (optional) — lists components/hooks/styles for discovery
3. **Call `expansions`** (once per session) — get component aliases and synonym groups

Use discovered values for `module`, `filters.scope`, and `filters.component` params.

## When to Use

| Scenario | RAG | Grep/Glob | Context7 |
|----------|-----|-----------|----------|
| Find component by concept | yes | if know filename | no |
| Search design tokens | yes | yes | no |
| Library API docs | no | no | yes |
| Pattern across codebase | yes | exact match only | no |
| Discover available components | catalog | no | no |

## Query Strategy

1. **Known component or file?** -> `query` + component filter (get canonical name from `expansions`)
2. **Known topic area?** -> `query` + topic/file_type filters (discover valid values via `status`)
3. **Conceptual/cross-cutting?** -> Smart query with HyDE (see `references/smart-query.md`)
4. **< 3 results or low scores?** -> Broaden: remove filters, try synonyms, alternate casing
5. **Still nothing?** -> Fall through to Grep/Glob (codebase search)

## Rules

1. Start broad, refine with filters — not longer queries
2. Natural language works best — "button with loading state" over "btn loading"
3. Low relevance scores suggest rephrasing needed
4. If server offline, fall back to Grep/Glob
5. `stale_sidecar: true` in results — trust code chunks, ignore metadata fields
6. Do NOT generate synonym variants — server handles expansion automatically

## Integration

Priority level 2 in `knowledge-retrieval` chain:
1. `docs/` files -> 2. **RAG** -> 3. Skills/codebase -> 4. Context7

## Related Skills

- `knowledge-retrieval` — Orchestrates source priority
- `web-frontend` — Frontend patterns (enhanced by this skill)
- `docs-seeker` — External documentation lookup

## References

- `references/smart-query.md` — HyDE + multi-query retrieval strategy
- `references/sidecar-workflow.md` — AI-generated metadata enrichment
- `references/component-mappings.md` — Get canonical names via `expansions` MCP tool
- `references/synonym-groups.md` — Get synonym groups via `expansions` MCP tool
