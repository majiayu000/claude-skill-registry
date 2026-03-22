---
name: ddd-architecture
description: Domain-Driven Design architecture guide for this Angular project. Activates when discussing folder structure, file placement, domain organization, component organization, or creating new features/components/services.
---

# DDD Architecture (Project-Specific)

For complete architecture rules, read `.github/instructions/architecture.instructions.md`.

## Quick Reference

```
src/app/features/{domain}/
  feature/   → Smart components (inject stores, orchestrate)
  ui/        → Dumb components (input/output only)
  data/
    models/         → TypeScript interfaces
    infrastructure/ → HTTP services
    state/          → NgRx Signal Stores
  util/      → Pure helper functions
```

## Critical Rules

- **No barrel files** (`index.ts`) — strictly prohibited
- **Each component in its own subfolder** — `feature/task-dashboard/task-dashboard.ts`
- **No type suffixes** — `TaskCard`, not `TaskCardComponent`; `TaskApi`, not `TaskApiService`
- **kebab-case files** — `task-card.ts`, `task-store.ts`
- **Domains don't import from other domains** — shared code goes in `src/app/shared/`
