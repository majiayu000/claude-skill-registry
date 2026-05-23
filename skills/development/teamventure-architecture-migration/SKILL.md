---
name: teamventure-architecture-migration
description: Use when refactoring TeamVenture domains/architecture; enforces migration order (Planning→Authorization→Identity→Infrastructure) and preferred steps (split classes before moving packages).
---

# TeamVenture Architecture Migration (Order + Guardrails)

## Migration order (domain/context)

1. **Planning (core)**: Plans + review collaboration (memberships, itinerary revisions, itinerary suggestions)
2. **Authorization (supporting)**: Policy/permission checks (no ownership of business fact tables)
3. **Identity (supporting)**: Auth/login/session/user profile
4. **Infrastructure (supporting)**: Read/write routing, cache/MQ wiring, monitoring hardening

## Refactor order inside a domain

1. **Split classes first** (semantic/CQRS refactor), keep packages stable
   - Example: `*Service` → `*QueryService` + `*CommandService`
2. **Move packages second** (mechanical refactor)
   - Move in small batches; keep public API/HTTP routes stable

## CQRS + read/write split rule

- Query methods must be annotated with `@Transactional(readOnly = true)` to route to **slave**
- Command methods must use default or explicit `@Transactional` to route to **master**
- Permission checks that must be immediately consistent should read from **master** (or cache with strict invalidation)

## Execution checklist (per step)

- Make change in smallest viable slice
- Run Java tests (`mvn test`) and fix regressions introduced by the slice
- Avoid broad renames and unrelated refactors

