---
name: tmnl-file-organization
description: Navigate TMNL's directory structure, understand lib/ vs components/, locate testbeds, services, atoms, and follow naming conventions
triggers:
  - where is
  - file structure
  - directory organization
  - find component
  - find service
  - naming convention
---

# TMNL File Organization

Navigate TMNL's sophisticated modular architecture with confidence. This skill maps the directory structure, explains the lib/ vs components/ split, and guides you to the right file for any task.

## Overview

TMNL follows a **strict separation of concerns**:
- `src/lib/` — Reusable logic, services, atoms, hooks (framework-agnostic)
- `src/components/` — React UI components (framework-specific)
- `src/components/testbed/` — Isolated component demonstrations at `/testbed/*` routes
- `assets/documents/` — Architecture docs, ADRs, design artifacts
- `.edin/` — EDIN methodology files (patterns, testing, service docs)
- `.agents/` — Session journals and context files

## Canonical Sources

### Primary Navigation Map

```
packages/tmnl/
├── src/
│   ├── lib/                    # Logic layer (Effect services, atoms, utilities)
│   │   ├── <domain>/
│   │   │   ├── v1/             # Versioned implementations
│   │   │   ├── v2/
│   │   │   ├── services/       # Effect.Service definitions
│   │   │   ├── atoms/          # effect-atom state atoms
│   │   │   ├── hooks/          # React hooks consuming atoms/services
│   │   │   ├── types.ts        # TypeScript interfaces
│   │   │   ├── index.ts        # Public exports
│   │   │   └── *.md            # Domain-specific docs (ARCHITECTURE, CLAUDE, README)
│   │   └── ...
│   ├── components/             # Presentation layer (React components)
│   │   ├── testbed/            # Testbed demonstrations
│   │   ├── <domain>/           # Domain-specific UI
│   │   ├── primitives/         # Base UI building blocks
│   │   ├── ui/                 # shadcn/ui components
│   │   └── ...
│   └── pages/                  # Route components
├── assets/
│   └── documents/              # Architecture docs, ADRs
├── .edin/                      # EDIN patterns (EFFECT_PATTERNS, TESTING, etc)
├── .agents/                    # Session journals
└── .beads/                     # Issue tracking database
```

### Submodules Reference

Located at `../../submodules/` (from `packages/tmnl`):

```
submodules/
├── effect/                     # Effect-TS core library
│   └── packages/*/test/        # Canonical Effect test patterns
├── effect-atom/                # Reactive atoms for Effect
│   └── packages/atom/test/     # Atom test patterns
├── website/                    # Effect documentation (human-authored)
│   └── content/src/content/docs/
├── ag-grid/                    # AG-Grid source
├── anime/                      # anime.js animation library
├── GSAP/                       # GSAP animation library
└── xstate/                     # XState state machines
```

## Patterns

### lib/ Structure Pattern

Every `src/lib/<domain>/` follows this canonical layout:

```
src/lib/<domain>/
├── v1/                         # Current stable version
│   ├── index.ts                # Public API exports
│   ├── types.ts                # TypeScript types/interfaces
│   ├── services/               # Effect.Service implementations
│   │   └── <ServiceName>.ts
│   ├── atoms/                  # effect-atom state atoms
│   │   └── index.ts
│   ├── hooks/                  # React hooks (useAtomValue, custom hooks)
│   │   └── use<Domain>.ts
│   ├── components/             # (rare) domain-specific components
│   └── <other>/                # kernels, effects, traits, etc.
├── v2/                         # Experimental/next version
├── ARCHITECTURE.md             # Deep technical design doc
├── CLAUDE.<domain>.md          # Agent handoff guide
├── README.md                   # User-facing quick reference
└── index.ts                    # Version-agnostic public exports
```

**Versioning Convention**:
- `v1/` — Production-ready, stable API
- `v2/` — Experimental, breaking changes expected
- Root `index.ts` — Delegates to current version (usually `v1`)

### components/ Structure Pattern

```
src/components/<domain>/
├── <ComponentName>.tsx         # Main component file
├── components/                 # Subcomponents (if complex)
│   ├── <SubComponent>.tsx
│   └── index.ts
├── <context>.tsx               # React Context (if needed)
└── index.ts                    # Public exports
```

**Key Differences from lib/**:
- Components are **React-specific** (JSX/TSX files)
- Components **consume** lib services/atoms via hooks
- No direct Effect.Service definitions (use `src/lib/`)

### Testbed Pattern

Testbeds demonstrate components in isolation at `/testbed/<feature>` routes.

**Location**: `src/components/testbed/<Feature>Testbed.tsx`

**Examples**:
- `DataManagerTestbed.tsx` → `/testbed/data-manager`
- `SliderV2Testbed.tsx` → `/testbed/slider`
- `AnimationTestbed.tsx` → `/testbed`
- `VariablesTestbed.tsx` → `/testbed/variables`

**Route Registration**: In `src/router.tsx`, add:
```tsx
<Route path="/testbed/<feature>" element={<FeatureTestbed />} />
```

### Service Pattern (Effect.Service)

**Location**: `src/lib/<domain>/services/<ServiceName>.ts`

**Structure**:
```typescript
import { Context, Effect, Layer } from "effect";

export class MyService extends Context.Tag("tmnl/<domain>/MyService")<
  MyService,
  MyServiceInterface
>() {
  static Default = Layer.succeed(this, {
    // implementation
  });
}
```

**Usage in Atoms**:
```typescript
// src/lib/<domain>/atoms/index.ts
export const myRuntimeAtom = Atom.runtime(
  Layer.mergeAll(MyService.Default, OtherService.Default)
);

export const myAtom = myRuntimeAtom.atom(
  Effect.gen(function* () {
    const service = yield* MyService;
    return yield* service.someMethod();
  })
);
```

### Atom Pattern (effect-atom)

**Location**: `src/lib/<domain>/atoms/index.ts`

**Standard Atoms**:
```typescript
import { Atom } from "@effect-atom/atom-react";
import { Effect } from "effect";

// Runtime atom combines service layers
export const runtimeAtom = Atom.runtime(
  Layer.mergeAll(ServiceA.Default, ServiceB.Default)
);

// Derived atom reads from service
export const stateAtom = runtimeAtom.atom(
  Effect.gen(function* () {
    const service = yield* ServiceA;
    return yield* service.getState();
  })
);

// Operation atom mutates state
export const opsAtom = {
  doAction: runtimeAtom.fn(
    Effect.gen(function* (input: string) {
      const service = yield* ServiceA;
      yield* service.performAction(input);
    })
  ),
};
```

**Usage in React**:
```tsx
import { useAtomValue } from "@effect-atom/atom-react";
import { stateAtom, opsAtom } from "@/lib/<domain>/atoms";

function MyComponent() {
  const stateResult = useAtomValue(stateAtom);
  const doAction = opsAtom.doAction;

  const state = Result.isSuccess(stateResult) ? stateResult.value : null;

  return <button onClick={() => doAction("input")}>Act</button>;
}
```

### Hook Pattern

**Location**: `src/lib/<domain>/hooks/use<Domain>.ts`

**Purpose**: Encapsulate atom consumption with cleaner API

```typescript
import { useAtomValue } from "@effect-atom/atom-react";
import { stateAtom, opsAtom } from "../atoms";

export function useDomain() {
  const stateResult = useAtomValue(stateAtom);
  const state = Result.isSuccess(stateResult) ? stateResult.value : null;

  return {
    state,
    isLoading: Result.isPending(stateResult),
    error: Result.isFailure(stateResult) ? stateResult.cause : null,
    doAction: opsAtom.doAction,
  };
}
```

## Examples

### Example 1: Finding a Service

**Task**: Locate the DataManager service

**Process**:
1. Check `src/lib/data-manager/` (domain directory)
2. Open `v1/DataManager.ts` (service file)
3. Check `v1/atoms/index.ts` for runtime atom
4. Check `v1/hooks/useDataManager.ts` for React hook

**Files**:
- Service: `src/lib/data-manager/v1/DataManager.ts`
- Atoms: `src/lib/data-manager/v1/atoms/index.ts`
- Hook: `src/lib/data-manager/v1/hooks/useDataManager.ts`
- Types: `src/lib/data-manager/v1/types.ts`

### Example 2: Finding a Testbed

**Task**: View the slider testbed demonstration

**Process**:
1. Check `src/components/testbed/` directory
2. Find `SliderV2Testbed.tsx`
3. Visit `/testbed/slider` route in browser

**File**: `src/components/testbed/SliderV2Testbed.tsx`

### Example 3: Finding Architecture Docs

**Task**: Understand DataManager architecture

**Process**:
1. Check `src/lib/data-manager/ARCHITECTURE.md` (deep technical)
2. Check `src/lib/data-manager/CLAUDE.data-manager.md` (agent guide)
3. Check `src/lib/data-manager/README.md` (quick reference)

**Files**:
- Architecture: `src/lib/data-manager/ARCHITECTURE.md`
- Agent Guide: `src/lib/data-manager/CLAUDE.data-manager.md`
- Quick Ref: `src/lib/data-manager/README.md`

### Example 4: Finding Effect Patterns

**Task**: Learn how to test Effect services

**Process**:
1. Check `.edin/EFFECT_TESTING_PATTERNS.md` (TMNL-specific patterns)
2. Check `../../submodules/effect/packages/*/test/` (canonical examples)
3. Check `.edin/EFFECT_PATTERNS.md` (comprehensive registry)

**Files**:
- TMNL Patterns: `.edin/EFFECT_TESTING_PATTERNS.md`
- Canonical Tests: `../../submodules/effect/packages/sql-sqlite-bun/test/Client.test.ts`
- Pattern Registry: `.edin/EFFECT_PATTERNS.md`

### Example 5: Finding AG-Grid Integration

**Task**: Locate AG-Grid theme tokens and custom renderers

**Process**:
1. Check `src/lib/data-grid/theme/tokens.ts` (design tokens)
2. Check `src/lib/data-grid/renderers/` (custom cell renderers)
3. Check `src/lib/data-grid/variants/` (theme variants)
4. Check `assets/documents/AG_GRID_THEMING_ARCHITECTURE.md` (deep dive)

**Files**:
- Tokens: `src/lib/data-grid/theme/tokens.ts`
- Renderers: `src/lib/data-grid/renderers/IdCellRenderer.tsx`
- Variants: `src/lib/data-grid/variants/tmnl-dense-dark.ts`
- Docs: `assets/documents/AG_GRID_THEMING_ARCHITECTURE.md`

## Anti-Patterns

### ❌ DON'T: Mix Logic in Components

```tsx
// WRONG: Service logic in component
function MyComponent() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Complex business logic here
    const result = doComplexCalculation();
    setData(result);
  }, []);
}
```

**✅ DO**: Extract to lib/ service/atom
```typescript
// src/lib/my-domain/services/MyService.ts
export class MyService extends Context.Tag(...) {}

// src/lib/my-domain/atoms/index.ts
export const dataAtom = runtimeAtom.atom(
  Effect.gen(function* () {
    const service = yield* MyService;
    return yield* service.calculate();
  })
);

// Component consumes atom
function MyComponent() {
  const dataResult = useAtomValue(dataAtom);
  const data = Result.isSuccess(dataResult) ? dataResult.value : [];
}
```

### ❌ DON'T: Create Atoms in Component Scope

```tsx
// WRONG: Atom defined inside component
function MyComponent() {
  const myAtom = Atom.make(0); // Recreated on every render!
}
```

**✅ DO**: Define atoms at module level or in `atoms/index.ts`
```typescript
// src/lib/my-domain/atoms/index.ts
export const myAtom = Atom.make(0);

// Component uses stable reference
function MyComponent() {
  const value = useAtomValue(myAtom);
}
```

### ❌ DON'T: Use useState for Cross-Component State

```tsx
// WRONG: Prop drilling useState
function Parent() {
  const [state, setState] = useState(0);
  return <Child state={state} setState={setState} />;
}
```

**✅ DO**: Use atoms for shared state
```typescript
// src/lib/my-domain/atoms/index.ts
export const sharedAtom = Atom.make(0);

// Both components consume atom
function Parent() {
  const value = useAtomValue(sharedAtom);
}
function Child() {
  const value = useAtomValue(sharedAtom);
}
```

### ❌ DON'T: Mix Versioned and Unversioned Code

```typescript
// WRONG: Importing from v1 directly
import { MyService } from "@/lib/my-domain/v1/services/MyService";
```

**✅ DO**: Import from version-agnostic index
```typescript
// CORRECT: Import from root index
import { MyService } from "@/lib/my-domain";
// Root index.ts delegates to current version (v1)
```

### ❌ DON'T: Put Effect.Service in components/

```tsx
// WRONG: Service in components/
// src/components/my-ui/MyService.ts
export class MyService extends Context.Tag(...) {}
```

**✅ DO**: Services belong in lib/
```typescript
// CORRECT: Service in lib/
// src/lib/my-domain/services/MyService.ts
export class MyService extends Context.Tag(...) {}
```

## Quick Reference

### File Location Cheatsheet

| What You're Looking For | Where to Find It |
|-------------------------|------------------|
| Effect Service | `src/lib/<domain>/services/<Service>.ts` |
| effect-atom atoms | `src/lib/<domain>/atoms/index.ts` |
| React hooks | `src/lib/<domain>/hooks/use<Domain>.ts` |
| React components | `src/components/<domain>/<Component>.tsx` |
| Testbed demos | `src/components/testbed/<Feature>Testbed.tsx` |
| Architecture docs | `src/lib/<domain>/ARCHITECTURE.md` or `assets/documents/` |
| Effect patterns | `.edin/EFFECT_PATTERNS.md` |
| Testing patterns | `.edin/EFFECT_TESTING_PATTERNS.md` |
| Effect tests (canonical) | `../../submodules/effect/packages/*/test/` |
| Effect docs (human) | `../../submodules/website/content/src/content/docs/` |
| Session journals | `.agents/val/journal/<date>.md` |

### Common Commands

```bash
# Find a component
find src/components -name "*MyComponent*"

# Find a service
find src/lib -name "*Service.ts"

# Find all testbeds
ls src/components/testbed/

# Find architecture docs
find assets/documents -name "*.md"

# Find EDIN patterns
ls .edin/

# Check submodule docs
ls ../../submodules/website/content/src/content/docs/docs/
```
