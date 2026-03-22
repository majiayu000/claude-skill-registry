---
name: ios-rag
description: (ePost) Use when searching iOS codebase for Swift views, UIKit/SwiftUI patterns, or design system tokens via vector search
user-invocable: false

metadata:
  agent-affinity: [epost-a11y-specialist, epost-muji, epost-fullstack-developer]
  keywords: [rag, vector-search, ios, swift, swiftui, uikit, design-system]
  platforms: [ios]
  triggers: ["search swift", "find view", "ios pattern", "theme token"]
  connections:
    enhances: [ios-development]
---

# iOS RAG Skill

## Purpose

Vector search across iOS repositories. Semantic search of Swift code, SwiftUI views, UIKit patterns, and design tokens via MCP tools. Call `status` to discover currently indexed projects.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `query` | Semantic search — returns code chunks with relevance scores |
| `status` | Health check, indexed projects, document counts |
| `navigate` | O(1) shortcut to known code locations |
| `expansions` | Component alias mappings + synonym groups for query planning |

Tool parameters are self-describing — check inputSchema for current options. iOS also exposes filter metadata via `GET /api/rag/filters` (REST) — use `query` inputSchema for MCP-accessible filter options.

## Discovery Protocol

Before querying, discover what's indexed:

1. **Call `status`** — returns available projects, document counts, health
2. **Call `expansions`** (once per session) — get component aliases and synonym groups

Use discovered project names for `filters.project` param. Use `enforce_scope: false` to search across all indexed projects.

## When to Use

| Scenario | RAG | Grep/Glob | Context7 |
|----------|-----|-----------|----------|
| Find Swift view by concept | yes | if know filename | no |
| Search theme tokens | yes | yes | no |
| Apple framework API | no | no | yes |
| Cross-project pattern | yes | one repo at a time | no |
| Existing view for task | yes | no | no |

## Query Strategy

1. **Known view or file?** -> `query` + component filter (get canonical name from `expansions`)
2. **Known topic area?** -> `query` + topic/file_type filters (discover valid values via `status`)
3. **Conceptual/cross-cutting?** -> Smart query with HyDE (see `references/smart-query.md`)
4. **< 3 results or low scores?** -> Broaden: remove filters, try synonyms, alternate casing
5. **Still sparse?** -> Try `enforce_scope: false` to search all indexed repos
6. **Still nothing?** -> Fall through to Grep/Glob (codebase search)

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
- `ios-development` — iOS development patterns (enhanced by this skill)
- `docs-seeker` — External Apple documentation lookup

## References

- `references/smart-query.md` — HyDE + multi-query retrieval strategy
- `references/sidecar-workflow.md` — AI-generated metadata enrichment
- `references/component-mappings.md` — Get canonical names via `expansions` MCP tool
- `references/synonym-groups.md` — Get synonym groups via `expansions` MCP tool
