---
name: common-conventions
description: TMNL codebase conventions for file organization, barrel exports, naming patterns, comments, and module structure. The meta-skill for consistency.
model_invoked: true
triggers:
  - "convention"
  - "naming"
  - "barrel"
  - "index.ts"
  - "file structure"
  - "module organization"
  - "code style"
---

# TMNL Common Conventions

## Overview

TMNL maintains strict conventions for code organization, naming, and documentation. This skill codifies patterns observed across the codebase to ensure consistency.

**Mandatory Conventions** (Non-negotiable):
1. Schema discipline — All domain types use Effect Schema
2. Typography 12px floor — No text smaller than 12px
3. Atom-as-State doctrine — No Effect.Ref for React consumers
4. Dependency audit — Grep before cutting imports

---

## Pattern 1: Library Module Structure

**When:** Creating a new library at `src/lib/{feature}/`

### Standard Directory Layout

```
src/lib/{feature}/
├── index.ts              # Barrel export (required)
├── types.ts              # TypeScript types (UI props, configs)
├── schemas/              # Effect Schema definitions
│   └── index.ts
├── services/             # Effect.Service implementations
│   ├── index.ts
│   └── {Feature}Service.ts
├── atoms/                # effect-atom definitions
│   └── index.ts
├── hooks/                # React hooks
│   └── use{Feature}.ts
├── components/           # React components (if UI-heavy)
│   └── {Component}.tsx
├── machines/             # XState machines (if stateful)
│   └── {feature}-machine.ts
├── v1/, v2/              # Version directories (for evolution)
└── CLAUDE.{feature}.md   # Agent handoff documentation
```

### When to Use Each Directory

| Directory | When to Create |
|-----------|----------------|
| `services/` | Multiple Effect services, or single complex service |
| `service.ts` (root) | Single simple service (e.g., `src/lib/commands/service.ts`) |
| `atoms/` | effect-atom state management |
| `hooks/` | Multiple React hooks |
| `use{Feature}.tsx` (root) | Single hook |
| `schemas/` | Domain types requiring validation |
| `types.ts` | UI props, configs, non-validated types |
| `machines/` | XState state machines |
| `v1/`, `v2/` | Major version evolution (not breaking changes) |

---

## Pattern 2: Barrel File (index.ts) Structure

**When:** Every `src/lib/{feature}/` directory requires a barrel export.

### Standard Format

```typescript
/**
 * {Feature} Library
 *
 * {Brief description}
 *
 * @example
 * ```tsx
 * import { Component, useFeature } from '@/lib/{feature}'
 * ```
 */

// ═══════════════════════════════════════════════════════════════════════════
// CORE EXPORTS
// ═══════════════════════════════════════════════════════════════════════════

export { MainComponent } from './components/Main'
export { FeatureService } from './services'

// ═══════════════════════════════════════════════════════════════════════════
// SCHEMAS
// ═══════════════════════════════════════════════════════════════════════════

export * from './schemas'

// ═══════════════════════════════════════════════════════════════════════════
// ATOMS (effect-atom)
// ═══════════════════════════════════════════════════════════════════════════

export {
  stateAtom,
  configAtom,
  operationsAtom,
} from './atoms'

// ═══════════════════════════════════════════════════════════════════════════
// REACT HOOKS
// ═══════════════════════════════════════════════════════════════════════════

export { useFeature, useFeatureState } from './hooks'

// ═══════════════════════════════════════════════════════════════════════════
// TYPES
// ═══════════════════════════════════════════════════════════════════════════

export type { FeatureConfig, FeatureState } from './types'
```

### Section Separators

Use **box-drawing characters** for major sections:

```typescript
// ═══════════════════════════════════════════════════════════════════════════
// SECTION NAME (all caps)
// ═══════════════════════════════════════════════════════════════════════════
```

Use **simple dashes** for subsections:

```typescript
// ───────────────────────────────────────────────────────────────────────────
// Subsection name
// ───────────────────────────────────────────────────────────────────────────
```

### Version Re-exports

For modules with v1/v2:

```typescript
// Default exports from v1
export * from './v1'

// Explicit v2 namespace
export * as v2 from './v2'
```

Usage:
```typescript
import { Slider } from '@/lib/slider'         // v1 (default)
import { Slider } from '@/lib/slider/v2'      // v2 (explicit)
```

---

## Pattern 3: Naming Conventions

### Atoms

| Pattern | Example | Usage |
|---------|---------|-------|
| `{noun}Atom` | `resultsAtom` | State atom |
| `{noun}sAtom` | `layersAtom` | Collection atom |
| `{verb}Atom` | `computedAtom` | Derived/computed atom |
| `{feature}OpsAtom` | `layerOpsAtom` | Operation atoms (mutations) |
| `{verb}Op` | `searchOp`, `clearOp` | Individual operation |

### Services

| Pattern | Example | Usage |
|---------|---------|-------|
| `{Feature}Service` | `DataManagerService` | Effect.Service class |
| `{Feature}ServiceShape` | `ChannelServiceShape` | Interface type |
| `{Behavior}Behavior` | `LinearBehavior`, `DecibelBehavior` | Strategy pattern |

### Hooks

| Pattern | Example | Usage |
|---------|---------|-------|
| `use{Feature}` | `useSlider` | Main feature hook |
| `use{Feature}Value` | `useSliderValue` | Read-only value hook |
| `use{Feature}State` | `useMinibufferState` | State + updater |
| `use{Feature}Ops` | `useOverlayOps` | Operations only |
| `useAtom{Feature}` | `useAtomValue` | Atom-specific |

### Components

| Pattern | Example | Usage |
|---------|---------|-------|
| `{Name}.tsx` | `Slider.tsx` | Component file |
| `{Name}Props` | `SliderProps` | Props interface |
| `{Name}Context` | `DataGridContext` | Context type |
| `{Name}Provider` | `CommandProvider` | Context provider |

### Machines

| Pattern | Example | Usage |
|---------|---------|-------|
| `{feature}Machine` | `minibufferMachine` | XState machine |
| `{Feature}Machine` | `MinibufferMachine` | Type alias |
| `{Feature}Actor` | `MinibufferActor` | ActorRef type |

---

## Pattern 4: Comment Styles

### File Header (JSDoc)

```typescript
/**
 * {Module Name} — {Brief description}
 *
 * {Longer description if needed}
 *
 * @example
 * ```tsx
 * // Usage example
 * ```
 */
```

### Architectural Notes

For non-obvious design decisions:

```typescript
// ARCHITECTURAL NOTE:
// CommandProvider lives here (commands/), not in minibuffer/.
// Minibuffer is a generic prompt engine. Commands USES minibuffer, not the reverse.
```

### TODO/FIXME

```typescript
// TODO(prime): Migrate to v2 API after EPOCH-0003
// FIXME: This breaks when input is empty
// HACK: Workaround for WSLg rendering bug
```

---

## Pattern 5: Types vs Schemas

### When to Use `types.ts`

- React component props
- UI configuration
- Local function parameters
- Types that don't need runtime validation

```typescript
// src/lib/slider/v1/types.ts
export interface SliderProps {
  value: number
  onChange: (value: number) => void
  min?: number
  max?: number
}

export interface SliderConfig {
  min: number
  max: number
  step: number
  defaultValue: number
}
```

### When to Use `schemas/`

- Domain types requiring validation
- Event payloads
- API responses
- Discriminated unions with pattern matching
- EventLog integration

```typescript
// src/lib/overlays/schemas/core.ts
import { Schema } from 'effect'

export const OverlayId = Schema.String.pipe(
  Schema.brand('OverlayId')
)
export type OverlayId = typeof OverlayId.Type

export const OverlayOpened = Schema.TaggedStruct('OverlayOpened', {
  id: OverlayId,
  timestamp: Schema.DateFromSelf,
})
```

---

## Pattern 6: Test File Organization

### Location Patterns

| Pattern | Example | When |
|---------|---------|------|
| `__tests__/` directory | `src/lib/stx/__tests__/` | Multiple test files |
| `.test.ts` suffix | `service.test.ts` | Single test file |
| `.bun.test.ts` suffix | `eventlog-integration.bun.test.ts` | Bun-specific |

### Test Naming

```typescript
// src/lib/feature/__tests__/feature.test.ts
describe('FeatureService', () => {
  describe('operation', () => {
    it('does X when Y', () => { ... })
    it('fails with Z when W', () => { ... })
  })
})
```

### Effect Service Tests

Use `@effect/vitest` with `it.effect()`:

```typescript
import { describe, it } from '@effect/vitest'

describe('MyService', () => {
  it.effect('returns data', () =>
    Effect.gen(function* () {
      const service = yield* MyService
      const result = yield* service.getData()
      expect(result).toBeDefined()
    }).pipe(Effect.provide(MyService.Default))
  )
})
```

### Atom Tests

Use `Registry.make()`:

```typescript
it('atom updates', () => {
  const r = Registry.make()
  expect(r.get(counterAtom)).toBe(0)
  r.set(counterAtom, 1)
  expect(r.get(counterAtom)).toBe(1)
})
```

---

## Pattern 7: Documentation Files

### Per-Module Documentation

| File | Purpose | Audience |
|------|---------|----------|
| `CLAUDE.{feature}.md` | Agent handoff | AI assistants |
| `README.md` | User-facing docs | Developers |
| `ARCHITECTURE.md` | Deep design analysis | Architects |
| `AGENTS.{feature}.md` | Agent-specific notes | AI assistants |

### CLAUDE.{feature}.md Structure

```markdown
# {Feature} — Claude Context

## Overview
{Brief description}

## Key Files
- `service.ts` — Main service implementation
- `atoms/index.ts` — Reactive state

## Patterns Used
- Effect.Service<>() for DI
- Atom.runtime() for state

## Gotchas
- Don't use X because Y
- Always Z before W

## Related Skills
- effect-patterns
- effect-atom-integration
```

---

## Pattern 8: Service File Patterns

### Single Service (Root Level)

```typescript
// src/lib/commands/service.ts

/**
 * TMNL Commands — Effect Service
 */

// ───────────────────────────────────────────────────────────────────────────
// Atoms (Reactive State)
// ───────────────────────────────────────────────────────────────────────────

export const commandsAtom = Atom.make<ReadonlyMap<string, Command>>(new Map())

// ───────────────────────────────────────────────────────────────────────────
// Service Implementation
// ───────────────────────────────────────────────────────────────────────────

export class CommandService extends Effect.Service<CommandService>()('app/CommandService', {
  effect: Effect.gen(function* () {
    // ...
  }),
}) {}
```

### Multiple Services (Directory)

```
src/lib/overlays/services/
├── index.ts              # Re-exports all services
├── OverlayRegistry.ts    # Registry service
├── PortHub.ts            # Port management
└── EventDispatcher.ts    # Event dispatch
```

---

## Anti-Patterns

### 1. Barrel File Without Sections

```typescript
// WRONG — Unorganized exports
export * from './components'
export * from './hooks'
export * from './types'
export * from './atoms'

// CORRECT — Sectioned exports
// ═══════════════════════════════════════════════════════════════════════════
// COMPONENTS
// ═══════════════════════════════════════════════════════════════════════════
export { Slider } from './components/Slider'

// ═══════════════════════════════════════════════════════════════════════════
// HOOKS
// ═══════════════════════════════════════════════════════════════════════════
export { useSlider } from './hooks/useSlider'
```

### 2. Types in Wrong Location

```typescript
// WRONG — Domain type without Schema
// src/lib/feature/types.ts
export interface UserEvent {
  _tag: 'UserCreated'
  id: string
  name: string
}

// CORRECT — Domain type with Schema
// src/lib/feature/schemas/events.ts
export const UserCreated = Schema.TaggedStruct('UserCreated', {
  id: Schema.String,
  name: Schema.NonEmptyString,
})
```

### 3. Inconsistent Naming

```typescript
// WRONG — Mixed naming styles
export const user_state_atom = Atom.make(...)  // snake_case
export const UseUserHook = () => { ... }       // PascalCase for hook
export const userservice = Effect.Service()    // no separator

// CORRECT — Consistent camelCase with type suffix
export const userStateAtom = Atom.make(...)
export const useUser = () => { ... }
export const UserService = Effect.Service()
```

### 4. Missing JSDoc on Exports

```typescript
// WRONG — No documentation
export const searchOp = runtimeAtom.fn<string>()(...)

// CORRECT — JSDoc on public exports
/**
 * Search operation. Triggers search with given query.
 *
 * @param query - Search query string
 * @returns Effect that updates resultsAtom
 */
export const searchOp = runtimeAtom.fn<string>()(...)
```

---

## Checklist: New Module Creation

When creating `src/lib/{feature}/`:

- [ ] Create `index.ts` with JSDoc header and sectioned exports
- [ ] Create `types.ts` for non-domain types (UI props, configs)
- [ ] Create `schemas/` for domain types using Effect Schema
- [ ] Create `services/` (or `service.ts`) with Effect.Service<>()
- [ ] Create `atoms/index.ts` with Atom definitions
- [ ] Create `hooks/` with React hooks
- [ ] Use section comments: `// ═══════...`
- [ ] Add ARCHITECTURAL NOTE for non-obvious decisions
- [ ] Create `CLAUDE.{feature}.md` for agent handoff
- [ ] Prefer `Atom.make<T>()` over `Effect.Ref<T>` for React
- [ ] Test with `@effect/vitest` for services, `Registry.make()` for atoms

---

## Canonical Examples

| Convention | Best Example | File |
|------------|--------------|------|
| Barrel file | Overlays | `src/lib/overlays/index.ts` |
| Service pattern | Commands | `src/lib/commands/service.ts` |
| Atom organization | Slider | `src/lib/slider/v1/atoms/index.ts` |
| Schema usage | Commands | `src/lib/commands/types.ts` |
| Hook naming | Commands | `src/lib/commands/useCommandWire.tsx` |
| Version strategy | Slider | `src/lib/slider/index.ts` |
| Test organization | STX | `src/lib/stx/__tests__/` |

---

## Integration Points

- **tmnl-file-organization** — Directory structure details
- **effect-patterns** — Service definition patterns
- **effect-atom-integration** — Atom patterns
- **tmnl-typography-discipline** — Typography rules
- **effect-schema-mastery** — Schema patterns
