---
name: arch-performance-optimization
description: Use when analyzing and improving performance for database queries, API endpoints, frontend rendering, or cross-service communication. Triage skill that routes to database-optimization, frontend-patterns, or provides API/job/cross-service profiling guidance.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
infer: true
---

# Performance Optimization

Triage skill for performance issues. Routes to the correct sub-tool or reference based on bottleneck type.

## Decision Tree

```
Performance Issue?
├── Database (slow queries, N+1, indexes, pagination)
│   → Invoke database-optimization skill (covers all DB patterns)
├── Frontend (rendering, bundle size, change detection)
│   → ⚠️ MUST READ docs/claude/frontend-patterns.md
│   → Key: OnPush, trackBy, lazy loading, virtual scroll, tree-shaking
├── API/Endpoint (response time, payload, serialization)
│   → ⚠️ MUST READ references/performance-patterns.md (parallel queries, caching, DTOs)
├── Background Jobs (throughput, batch processing)
│   → ⚠️ MUST READ references/performance-patterns.md (bounded parallelism, batch ops)
└── Cross-Service (message bus, eventual consistency)
    → ⚠️ MUST READ references/performance-patterns.md (payload size, idempotency)
```

## Quick Assessment Checklist

1. **Identify** bottleneck type using decision tree above
2. **Measure** baseline (response time, query count, bundle size)
3. **Route** to correct sub-tool or reference
4. **Apply** patterns from the routed resource
5. **Verify** improvement against baseline
6. **Monitor** for regressions

## EP-Specific Quick Wins

- **Parallel tuple queries**: `var (a, b) = await (queryA, queryB);`
- **Eager loading**: `repo.GetAllAsync(filter, ct, e => e.Related)`
- **Projections**: `.Select(e => new { e.Id, e.Name })` instead of full entity
- **Full-text search**: `searchService.Search(q, text, Entity.SearchColumns())`
- **Batch updates**: `repo.UpdateManyAsync(items, dismissSendEvent: true, checkDiff: false)`
- **Paged processing**: `PageBy(skip, take)` at database level

For detailed patterns, profiling commands, and anti-patterns:
**⚠️ MUST READ:** `.claude/skills/arch-performance-optimization/references/performance-patterns.md`

## Approval Gate

Present findings and optimization plan. Wait for explicit user approval before making changes -- performance optimizations can have wide-reaching side effects.


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
