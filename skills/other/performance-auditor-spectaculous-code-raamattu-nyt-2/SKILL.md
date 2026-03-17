---
name: performance-auditor
description: Expert assistant for monitoring and optimizing performance in the KR92 Bible Voice project. Use when analyzing query performance, optimizing database indexes, reviewing React Query caching, monitoring AI call costs, or identifying N+1 queries. Helps diagnose slow operations across database, frontend, and AI systems.
---

# Performance Auditor

Expert performance optimization for the Raamattu Nyt application across database, frontend, and AI systems.

## Quick Start

Choose your performance concern:

- **Database performance**: Slow queries, missing indexes, sequential scans → See `references/sql-queries.md`
- **React Query optimization**: Caching strategy, stale times, unnecessary refetches → See `references/react-query-patterns.md`
- **AI performance**: Latency, costs, cache effectiveness → See `references/ai-monitoring.md`
- **N+1 query detection**: Finding and fixing N+1 patterns → See `references/n+1-detection.md`
- **Optimization checklist**: Complete performance audit → See `references/checklist.md`
- **Common gotchas**: Known issues and pitfalls → See `references/learnings.md`

## Performance Targets

Reference targets for healthy performance:

| Operation | Target |
|-----------|--------|
| Single verse lookup | <20ms |
| Chapter load | <50ms |
| Text search | <100ms |
| AI translation | <500ms |
| Page load (FCP) | <1.5s |
| API response | <200ms |

## How to Use This Skill

1. Identify your performance issue (database, frontend, AI, or N+1)
2. Read the appropriate reference file above
3. Run SQL scripts or code patterns from `scripts/` if needed
4. Check `references/learnings.md` if results seem unexpected

## Key Tools

- **Database analysis**: Read `references/sql-queries.md` then run `scripts/analyze-queries.sql`
- **N+1 detection**: See `references/n+1-detection.md` and `scripts/detect-n+1.js`
- **Cache optimization**: See `references/react-query-patterns.md` for staleTime/gcTime strategy
- **AI monitoring**: See `references/ai-monitoring.md` for latency and cost tracking

## Context Files

For codebase structure reference:
- `Docs/context/db-schema-short.md` - Database tables and indexes
- `Docs/context/supabase-map.md` - Edge functions to monitor
