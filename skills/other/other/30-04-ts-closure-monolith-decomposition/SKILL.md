---
name: 30-04-ts-closure-monolith-decomposition
description: Decompose a large closure-based module into domain modules with shared state. Use when a single function/closure owns 1000+ lines of state and logic trapped by closure capture.
---

# 30.04 Closure Monolith Decomposition

Decompose a single closure that owns all state into domain modules with shared refs. The closure pattern traps everything — state, functions, types — inside one scope. Nothing can be tested, HMR'd, or reasoned about independently.

Born from decomposing a 3129-line `createSpacetimeClient()` closure into 10 modules (885 lines remaining, -72%).

## When to Use

- A single function/closure owns 1000+ lines of state and logic
- Everything is trapped because it captures `let` variables
- You can't test, HMR, or reason about individual concerns
- Functions that should be independent are coupled by shared closure scope

## Prerequisites

- Working build command identified (`bun run build`, not just `tsc --noEmit`)
- Working test suite (or baseline test count to verify no regressions)
- Clean git state — commit before starting

## Core Principle: Shared Refs Over Closures

If there's only one instance, the state is a module-level ref. Not a factory. Not closure capture. Not dependency injection.

```typescript
// WRONG — closure capture (the disease you're curing)
function createThing(options) {
  const { world, renderer } = options;
  const doStuff = () => { world.update(); renderer.draw(); };
  return { doStuff };
}

// WRONG — factory pattern (same disease, different symptoms)
function createBridge(deps) {
  return { doStuff: () => { deps.world.update(); deps.renderer.draw(); } };
}

// RIGHT — shared refs, standalone functions
export const bridge = {
  world: null as IWorld | null,
  renderer: null as GameRenderer | null,
};
export const doStuff = () => { bridge.world!.update(); bridge.renderer!.draw(); };
```

**Never replace a closure with a factory.** One singleton = one ref object.

## Workflow

### Phase 0: Baseline

```bash
bun run build   # The REAL build — not tsc --noEmit
bun test
git commit
```

⚠️ `tsc --noEmit` and `tsc -b` (project references) have different strictness. `isolatedModules`, unused import detection, and export visibility all differ. **Always verify with the real build command.**

### Phase 1: Extract State

Create `client-state.ts` (or `{module}-state.ts`). Move ALL mutable state out of the closure:

| State kind | Pattern |
|-----------|---------|
| Session/connection state | Named ref object: `export const stdb = { connection: null, ... }` |
| Constructor-time refs | Separate ref object: `export const bridge = { world: null, renderer: null, ... }` |
| Entity Maps, caches, Sets | Direct exports: `export const shipEntities = new Map()` |
| Convenience aliases | Destructured re-export: `export const { positions, rotations } = entityState` |

**Commit after this.** State is exported but unused — safe checkpoint.

⚠️ `export const { ... } = thing` is valid TypeScript but breaks under `isolatedModules` when consumed via `const { x } from "./state"`. Consumers must use `import { x } from "./state"`.

### Phase 2: Wire Closure Locals → Shared Refs

Mechanical find-and-replace. For each closure `let` that now exists in shared state:

```
connection → stdb.connection
playerShipEntityId → stdb.playerShipEntityId
```

This is N variables across M sites. It's mechanical. Do it in one pass.

**Gotcha: object literal keys and getter names.** A regex replacing `dockState` with `stdb.dockState` also hits:

```typescript
get stdb.dockState() { ... }      // BROKEN — was: get dockState()
stdb.serverUpdateRate: pStats.x,  // BROKEN — was: serverUpdateRate: pStats.x
```

Run build immediately after. Fix these before committing.

**Commit after this.** Closure locals eliminated — next phases extract functions.

### Phase 3: Extract Pure Functions

Functions that only READ shared state and CALL external APIs. No closure captures. Safest extraction.

| Kind | Target |
|------|--------|
| Reducer wrappers | `features/{domain}/actions.ts` |
| Read-only queries | `queries.ts` |
| Debug utilities | `modules/debug.ts` |

### Phase 4: Extract Domain Logic

Functions that READ + WRITE shared state (entity Maps, ECS, caches). They reference constructor-time refs — use `bridge.world!` in the extracted file.

The `!` assertion is justified: these functions only run after initialization.

Local aliases at the top of hot functions:

```typescript
export const applyShipUpsert = (entityId: string) => {
  const world = bridge.world!;
  const renderer = bridge.renderer!;
  // ... rest uses local vars, no repeated bridge.xxx!
};
```

### Phase 5: Extract Infrastructure

- **Table callback wiring** → `table-handlers.ts` (casts + store callbacks)
- **SQL query definitions** → `subscription-queries.ts` (pure data)
- **Snapshot recording** → alongside entity bridge (reads same state)

### Phase 6: Clean Up (after every extraction)

1. `bun run build` — catch unused imports
2. Remove dead imports, dead helpers, dead type aliases
3. `bun test` — verify no regressions
4. Commit

## What Stays in the Closure

Connection lifecycle genuinely needs closure-scoped state:

- Retry/reconnect flags (`tokenRetry`, `reconnectScheduled`, `connectAttempt`)
- Subscription handles that reset on disconnect
- Phase orchestration that calls `cleanupConnection` / `scheduleReconnect`

**The test:** if it resets on disconnect, it belongs in the closure.

## Rules

1. **Shared refs, never factories.** One instance = one ref object.
2. **State moves first, functions follow.** Can't extract a function until its state is accessible.
3. **Build after every step.** The real build. Not `--noEmit`.
4. **Commit before risky regex replacements.** Easy rollback > clever recovery.
5. **Don't rationalize coupling.** "Devs rarely edit this" is not architecture. A god object is the problem.
6. **Mechanical work doesn't need permission.** 8 variable renames across 90 sites — do it.
7. **Question prior analysis.** Plans written before doing the work contain assumptions the work invalidates.

## Anti-Patterns

| Anti-pattern | Why it's wrong | Do instead |
|-------------|---------------|------------|
| Factory to replace closure | Same coupling, extra indirection | Module-level ref |
| `tsc --noEmit` as build check | Misses `isolatedModules`, unused exports | Real `bun run build` |
| Extracting + leaving duplicate | Old code still exists = not refactored | Delete from source after wiring |
| Regex without build verify | Breaks object keys, getters, interfaces | Build immediately, fix before commit |
| "Justified" factory for singleton | Prior analysis assumed multi-instance | Re-examine — is there ever >1? |
