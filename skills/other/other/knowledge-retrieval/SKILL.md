---
name: knowledge-retrieval
description: (ePost) Use when you need prior art, past decisions, or existing patterns — checks docs/, skills, and RAG before external sources
user-invocable: false

metadata:
  agent-affinity: [epost-planner, epost-fullstack-developer, epost-debugger, epost-researcher, epost-code-reviewer]
  keywords: [retrieve, search, knowledge, context, rag, lookup, prior-art]
  platforms: [all]
  triggers: ["what do we know about", "check knowledge", "prior art", "previous decision"]
  connections:
    enhances: [research, plan]
---

# Knowledge Retrieval Skill

## Purpose

Internal-first knowledge retrieval protocol. Each piece of knowledge lives in exactly ONE tier. Search sources in order, stop when sufficient context found.

## Three Knowledge Tiers

| Tier | Type | Owner | Updated |
|------|------|-------|---------|
| **Procedural** | How to do things (methodology, pipelines, decision frameworks) | Skills | Versioned releases |
| **Codebase** | What exists in the code (components, tokens, patterns, implementations) | RAG system | Automatic (file watcher) |
| **Project** | What we decided & learned (ADRs, findings, conventions) | `docs/` | Organic (captured during work) |

**Rule**: Each piece of knowledge lives in exactly ONE tier. Other systems reference it, never copy it.

## When Active

- Starting implementation (check for existing patterns)
- Debugging (check for similar findings)
- Making decisions (check for prior ADRs)
- Researching libraries (check for previous evaluations)
- Reviewing code (check for conventions)

## Retrieval Chain (5 Levels)

Search sources in order, stop when sufficient context found:

| Level | Source | Tool | When to Use |
|-------|--------|------|-------------|
| 1 | `docs/` (multi-level) | Glob `**/docs/index.json`, then filter by agentHint + tags | Decisions, conventions, findings, patterns |
| 2 | RAG systems | MCP `query` | Code, components, tokens, implementations |
| 3 | Skills | Read skill-index.json | Methodology, procedures, guidelines |
| 4 | Codebase | Grep, Glob, Read | Exact matches, files RAG missed |
| 5 | External | Context7, WebSearch | Library APIs, latest external info |

### Level 1 Multi-Level Discovery

`docs/index.json` registries can exist at any level. Discover them all with a single glob, then read each to understand its scope from the `description` field:

```
Glob: **/docs/index.json
```

Use the registry closest to the files being worked on as primary. See `references/search-strategy.md` for query patterns.

**No registry found?** Prompt the user:
> No `docs/index.json` found. Run `/docs` to initialize one. This enables consistent, session-persistent knowledge retrieval for all agents.

## Search Protocol

Search sources in order, stop when sufficient context found. See `references/search-strategy.md` for full retrieval chain, query examples, and source-specific techniques.

**Key principle**: Start internal (docs/ index — all levels), then RAG, then skills, then codebase grep, then external (Context7/WebSearch). Stop as soon as you have sufficient context.

## Decision Matrix

| Question Type | Go to | Skip |
|---------------|-------|------|
| "What did we decide about X?" | L1 `docs/decisions/` | RAG, External |
| "How is X implemented?" | L2 RAG → L4 Codebase | Skills |
| "What components exist?" | L2 RAG | `docs/` |
| "What's the token value?" | L2 RAG | Skills |
| "What's the process for X?" | L3 Skills | RAG |
| "What's our convention?" | L1 `docs/conventions/` | External |
| "Why does X break?" | L1 `docs/findings/` → L2 RAG → L4 Codebase | — |
| "How to use library X API?" | L5 External (Context7) | `docs/` |
| "Should we use technology X?" | L1 `docs/decisions/` → L5 External | RAG |
| "What's the system architecture?" | L1 `docs/architecture/` | External |
| "How does feature X work?" | L1 `docs/features/` → L4 Codebase | — |

## Integration with Existing Skills

### docs-seeker
Handles Context7 + WebSearch (Level 5):
```
docs-seeker → resolve-library-id → get-library-docs
docs-seeker → WebSearch (if Context7 fails)
```

### research
Handles deep multi-source investigation:
```
research → knowledge-retrieval (internal first)
research → docs-seeker (external)
research → synthesize findings
```

## Cross-Source Bridging

docs/ (L1) and RAG (L2) complement each other. Bridge them:

| docs/ finding | RAG action |
|---------------|------------|
| ADR mentions component path | Query RAG for current implementation state |
| PATTERN describes approach | Query RAG for usage examples across codebase |
| FINDING references file | Query RAG for related files in same module |
| Convention names a pattern | Query RAG for conformance/violations |

| RAG finding | docs/ action |
|-------------|--------------|
| Result looks like a recurring pattern | Check `docs/patterns/` for documented version |
| Multiple results share an approach | Check `docs/conventions/` for existing convention |
| No docs/ entry for frequently-queried topic | Flag for `knowledge-capture` |

**Rule**: Always cross-reference. An ADR without code validation is stale. A code pattern without docs is undocumented risk.

## Cross-Platform RAG Coordination

When a query spans platforms, coordinate RAG queries:

| Scenario | Query strategy |
|----------|---------------|
| Design tokens, colors, typography | Query both web (2636) + iOS (2637) RAGs |
| Component parity check | Query both, compare by concept |
| Pattern consistency | Query both, note divergences |
| Platform-specific implementation | Query single platform RAG only |

**Dedup rule**: Group results by concept, not file. Note platform differences.
**Authority rule**: Definitions live in design system RAG, usage examples in platform RAG. Prefer the authoritative source.

## Staleness Detection

| Source | Freshness Signal | Action |
|--------|-----------------|--------|
| `docs/` | `updatedAt` field | Verify if >90 days old, cross-check with RAG |
| RAG code chunks | Auto-indexed on file change | Trust current code content |
| RAG sidecar metadata | `stale_sidecar: true` flag | Metadata outdated but code chunks still valid |
| Skills | Manually updated | Check last commit date |
| Codebase | Always current | Trust HEAD |
| Context7 | Live docs | Trust current |
| WebSearch | Publication date | Prefer <2 years |

**RAG staleness rule**: When `stale_sidecar: true`, use code chunks for implementation details but ignore metadata fields (summary, topics, component_names). Sidecar regeneration is handled server-side automatically.

## Best Practices

1. **Start internal**: Always check `docs/index.json` first
2. **Use agentHint**: Match hints against current task for relevance
3. **Skip irrelevant levels**: No RAG server? Skip L2, go directly to L4 (Grep/Glob codebase search) — never block on RAG availability
4. **Stop when sufficient**: Don't search all levels unnecessarily
5. **Attribute sources**: Note where each finding came from
6. **Validate staleness**: Check dates on knowledge entries
7. **Expand keywords**: Try synonyms if no results
8. **Combine results**: Merge complementary findings
9. **Update knowledge**: If external search yields new insight, capture it

## Aspect Files

| File | Purpose |
|------|---------|
| `search-strategy.md` | How to search each source |
| `priority-matrix.md` | Decision table for source priority |

## Related Skills

- `knowledge-retrieval/references/knowledge-base.md` — Knowledge system structure
- `knowledge-capture` — Persist new learnings
- `docs-seeker` — External documentation retrieval
- `research` — Deep multi-source investigation

## References

- `references/search-strategy.md` — Source-specific search techniques
- `references/priority-matrix.md` — Decision table for source selection
