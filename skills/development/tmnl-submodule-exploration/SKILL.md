---
name: tmnl-submodule-exploration
description: Navigate Effect, effect-atom, and website submodules to find canonical sources, test examples, and human-authored documentation
triggers:
  - submodule
  - effect submodule
  - effect-atom submodule
  - website submodule
  - canonical example
  - test example
  - find test pattern
---

# TMNL Submodule Exploration

Navigate TMNL's submodule library with precision. This skill guides you through effect, effect-atom, and website submodules to find canonical sources, test patterns, and human-authored documentation.

## Overview

TMNL includes **essential libraries as git submodules** for reference and pattern validation:
- **effect** — Effect-TS core library (canonical test patterns)
- **effect-atom** — Reactive atoms for Effect (atom test patterns)
- **website** — Effect documentation (human-authored, battle-tested)
- **ag-grid, anime, GSAP, xstate** — UI/animation libraries (reference implementations)

**Location**: `../../submodules/` (from `packages/tmnl`)

**Prime Directive**: When validating patterns, **prefer website submodule over deepwiki** — it's human-authored and contains battle-tested patterns.

## Canonical Sources

### Submodule Directory Structure

```
../../submodules/
├── effect/                     # Effect-TS core library
│   ├── packages/
│   │   ├── effect/             # Core Effect runtime
│   │   ├── sql-sqlite-bun/     # SQLite integration (Bun)
│   │   ├── sql-drizzle/        # Drizzle ORM integration
│   │   ├── sql-kysely/         # Kysely query builder
│   │   ├── sql-mssql/          # MS SQL integration
│   │   ├── sql-libsql/         # LibSQL integration
│   │   └── experimental/       # Experimental features
│   └── scripts/
│
├── effect-atom/                # Reactive atoms for Effect
│   └── packages/
│       ├── atom/               # Core atom library
│       │   └── test/           # Atom test patterns
│       ├── atom-react/         # React bindings
│       └── atom-vue/           # Vue bindings
│
├── website/                    # Effect documentation
│   └── content/
│       └── src/content/docs/
│           └── docs/           # Human-authored documentation
│               ├── introduction/
│               ├── guides/
│               ├── concurrency/
│               ├── state-management/
│               ├── stream/
│               ├── schema/
│               └── additional-resources/
│
├── ag-grid/                    # AG-Grid data grid library
├── anime/                      # anime.js animation library
├── GSAP/                       # GSAP animation library
├── xstate/                     # XState state machines
└── ...                         # Other submodules
```

### Effect Submodule

**Location**: `../../submodules/effect/`

**Key Directories**:

**Test Examples** (Canonical Patterns):
- `packages/effect/test/` — Core Effect tests
- `packages/sql-sqlite-bun/test/` — SQLite client tests (Bun runtime)
- `packages/sql-drizzle/test/` — Drizzle ORM integration tests
- `packages/sql-kysely/test/` — Kysely query builder tests
- `packages/sql-mssql/test/` — MS SQL client tests
- `packages/sql-libsql/test/` — LibSQL client tests

**Source Code**:
- `packages/effect/src/` — Effect runtime source
- `packages/sql/src/` — Base SQL abstraction
- `packages/platform/src/` — Platform services
- `packages/experimental/src/` — EventLog, DevTools, etc.

**Test File Naming Convention**:
- `*.test.ts` — Main test files (use `@effect/vitest`)
- `*.spec.ts` — Rare, used for specific test types
- `examples/*.test.ts` — Example-driven tests

### effect-atom Submodule

**Location**: `../../submodules/effect-atom/`

**Key Directories**:

**Test Examples** (Canonical Patterns):
- `packages/atom/test/Atom.test.ts` — Atom creation, derivation, subscriptions
- `packages/atom/test/AtomRef.test.ts` — AtomRef patterns (mutable refs in atoms)
- `packages/atom/test/AtomRpc.test.ts` — RPC patterns for atoms
- `packages/atom/test/Result.test.ts` — Result handling in atoms
- `packages/atom-react/test/` — React integration tests
- `packages/atom-vue/test/` — Vue integration tests

**Source Code**:
- `packages/atom/src/` — Core atom implementation
- `packages/atom-react/src/` — React hooks (`useAtom`, `useAtomValue`, etc.)

**Test Pattern**:
- Uses standard `it()` (not `it.effect()`)
- Uses `Registry.make()` for atom testing
- Example:
  ```typescript
  it("should update atom value", () => {
    const r = Registry.make();
    const atom = Atom.make(0);

    r.set(atom, 42);
    expect(r.get(atom)).toBe(42);
  });
  ```

### website Submodule

**Location**: `../../submodules/website/`

**Key Directories**:

**Human-Authored Documentation**:
- `content/src/content/docs/docs/` — Main documentation directory

**Categories**:

| Category | Path | Topics |
|----------|------|--------|
| **Introduction** | `docs/introduction/` | What is Effect, quick start |
| **Guides** | `docs/guides/` | Best practices, migration guides |
| **Concurrency** | `docs/concurrency/` | Fibers, queues, semaphores, deferred |
| **State Management** | `docs/state-management/` | Ref, SynchronizedRef, SubscriptionRef |
| **Streams** | `docs/stream/` | Creating, consuming, transforming streams |
| **Schema** | `docs/schema/` | Schema definition, validation, encoding |
| **Additional Resources** | `docs/additional-resources/` | Effect vs FP-TS, myths, API reference |

**File Format**: `.mdx` (Markdown with JSX components)

**Why This Matters**: These docs are **human-authored by the Effect team** — they represent battle-tested patterns, not AI inference.

### Other Submodules

**ag-grid** (`../../submodules/ag-grid/`):
- Grid component source code
- Custom renderer examples
- Theme system reference

**anime** (`../../submodules/anime/`):
- anime.js v4 source
- Animation examples
- SVG manipulation patterns

**GSAP** (`../../submodules/GSAP/`):
- GSAP core source
- Timeline examples
- Plugin reference

**xstate** (`../../submodules/xstate/`):
- State machine examples
- TypeScript patterns
- React integration

## Patterns

### Finding Effect Test Patterns

**Goal**: Learn how to test an Effect service with SQL integration

**Process**:
1. Navigate to Effect submodule: `cd ../../submodules/effect`
2. Find SQL test examples: `find packages/sql-sqlite-bun/test -name "*.test.ts"`
3. Read canonical test: `cat packages/sql-sqlite-bun/test/Client.test.ts`

**Key Observations**:
```typescript
import { it } from "@effect/vitest";
import { Effect } from "effect";

it.effect("should query database", () =>
  Effect.gen(function* () {
    const client = yield* SqliteClient;
    const rows = yield* client.query("SELECT * FROM users");
    expect(rows).toHaveLength(3);
  }).pipe(Effect.provide(TestLayer))
);
```

**Patterns Learned**:
- Use `it.effect()` for tests returning Effect
- Use `Effect.gen` for generator-style code
- Provide layers with `Effect.provide()`

### Finding effect-atom Test Patterns

**Goal**: Learn how to test atoms with subscriptions

**Process**:
1. Navigate to effect-atom submodule: `cd ../../submodules/effect-atom`
2. Find atom tests: `find packages/atom/test -name "*.test.ts"`
3. Read canonical test: `cat packages/atom/test/Atom.test.ts`

**Key Observations**:
```typescript
import { Atom, Registry } from "@effect-atom/atom";

it("should subscribe to atom changes", () => {
  const r = Registry.make();
  const atom = Atom.make(0);

  const values: number[] = [];
  r.subscribe(atom, (value) => values.push(value));

  r.set(atom, 1);
  r.set(atom, 2);

  expect(values).toEqual([0, 1, 2]);
});
```

**Patterns Learned**:
- Use `Registry.make()` for testing atoms
- Use `r.get()`, `r.set()`, `r.subscribe()` for atom operations
- Regular `it()` tests (not `it.effect()`)

### Finding Effect Documentation

**Goal**: Understand how to use Effect.Ref for mutable state

**Process**:
1. Navigate to website submodule: `cd ../../submodules/website`
2. Find state management docs: `ls content/src/content/docs/docs/state-management/`
3. Read Ref documentation: `cat content/src/content/docs/docs/state-management/ref.mdx`

**Key Insights**:
- Ref is for **mutable state within Effect runtime**
- Created with `Ref.make(initialValue)`
- Updated with `Ref.set()`, `Ref.update()`, `Ref.modify()`
- Contrast with **Atoms** which are for **React-observable state**

### Finding AG-Grid Examples

**Goal**: Learn how to create custom cell renderers

**Process**:
1. Navigate to AG-Grid submodule: `cd ../../submodules/ag-grid`
2. Find cell renderer examples: `find . -name "*CellRenderer*" -type f | head -10`
3. Read examples to understand registration and API

**Key Insights**:
- Custom renderers must be registered in `components` prop
- Renderers receive `params` with `value`, `data`, `node`, etc.

### Cross-Referencing Patterns

**Scenario**: Implementing a stream with backpressure

**Process**:
1. **Check TMNL docs**: `cat .edin/EFFECT_PATTERNS.md` (search for "stream")
2. **Check website submodule**: `cat ../../submodules/website/content/src/content/docs/docs/stream/*.mdx`
3. **Check Effect tests**: `find ../../submodules/effect/packages -name "*stream*.test.ts"`
4. **Synthesize pattern** from all three sources

**Result**: Comprehensive understanding from TMNL-specific patterns + canonical docs + test examples.

## Examples

### Example 1: Learning Effect.Service Pattern

**Question**: How do I define an Effect service with dependencies?

**Exploration Path**:
1. **Website submodule**:
   ```bash
   cd ../../submodules/website
   find . -name "*context*.mdx" | xargs grep -l "Context.Tag"
   ```
   Result: `content/src/content/docs/docs/guides/context-management.mdx`

2. **Effect tests**:
   ```bash
   cd ../../submodules/effect
   grep -r "Context.Tag" packages/sql-sqlite-bun/test/ | head -5
   ```
   Result: `packages/sql-sqlite-bun/test/Client.test.ts` shows service usage

3. **TMNL patterns**:
   ```bash
   cat .edin/EFFECT_SERVICE_PATTERNS.md
   ```
   Result: Service definition template

**Combined Learning**: Service definition syntax + test provisioning + TMNL conventions.

### Example 2: Understanding Atom.runtime()

**Question**: How do I create a runtime atom for Effect services?

**Exploration Path**:
1. **effect-atom source**:
   ```bash
   cd ../../submodules/effect-atom
   grep -r "Atom.runtime" packages/atom/src/
   ```
   Result: Implementation in `packages/atom/src/Atom.ts`

2. **TMNL examples**:
   ```bash
   cd packages/tmnl
   grep -r "Atom.runtime" src/lib/*/atoms/
   ```
   Result: `src/lib/data-manager/v1/atoms/index.ts` shows usage pattern

3. **effect-atom tests**:
   ```bash
   cd ../../submodules/effect-atom
   grep -r "runtime" packages/atom/test/
   ```
   Result: Runtime atom tests (if any)

**Combined Learning**: Implementation details + TMNL usage patterns + test validation.

### Example 3: Validating Schema Pattern

**Question**: Should I use `Schema.Struct` or `Schema.TaggedStruct`?

**Exploration Path**:
1. **TMNL directive**:
   ```bash
   cat CLAUDE.md | grep -A 20 "Schema Discipline"
   ```
   Result: Use `TaggedStruct` for discriminated data

2. **Website submodule**:
   ```bash
   cd ../../submodules/website
   cat content/src/content/docs/docs/schema/*.mdx | grep "TaggedStruct"
   ```
   Result: Documentation on when to use tagged unions

3. **Effect source**:
   ```bash
   cd ../../submodules/effect
   grep -r "TaggedStruct" packages/effect/src/Schema.ts
   ```
   Result: Implementation and type signature

**Combined Learning**: TMNL convention + canonical docs + implementation details.

### Example 4: Finding SQL Transaction Pattern

**Question**: How do I run multiple SQL queries in a transaction?

**Exploration Path**:
1. **Effect SQL tests**:
   ```bash
   cd ../../submodules/effect/packages/sql-sqlite-bun/test
   grep -n "transaction" Client.test.ts
   ```
   Result: Transaction test examples

2. **Website submodule**:
   ```bash
   cd ../../submodules/website
   find . -name "*sql*.mdx" | xargs grep -l "transaction"
   ```
   Result: SQL documentation with transaction patterns

3. **TMNL patterns**:
   ```bash
   cat .edin/EFFECT_SQL_SQLITE_PATTERNS.md
   ```
   Result: TMNL-specific SQL patterns

**Combined Learning**: Test examples + documentation + TMNL conventions.

### Example 5: Understanding Stream Operators

**Question**: How do I filter and map a stream?

**Exploration Path**:
1. **Website submodule**:
   ```bash
   cd ../../submodules/website
   cat content/src/content/docs/docs/stream/consuming-streams.mdx
   ```
   Result: Stream operator documentation

2. **Effect tests**:
   ```bash
   cd ../../submodules/effect/packages
   find . -name "*stream*.test.ts" | xargs grep "pipe.*filter.*map"
   ```
   Result: Test examples combining operators

3. **TMNL examples**:
   ```bash
   cd packages/tmnl
   grep -r "Stream.filter" src/lib/
   ```
   Result: TMNL usage patterns

**Combined Learning**: Documentation + test examples + TMNL usage.

## Anti-Patterns

### ❌ DON'T: Ask deepwiki Before Checking Submodules

```bash
# WRONG: Go straight to AI agent
deepwiki ask "How do I use Effect.Ref?"

# RIGHT: Check human-authored docs first
cd ../../submodules/website
cat content/src/content/docs/docs/state-management/ref.mdx
```

**Why**: AI inference may be outdated or incorrect. Human-authored docs are canonical.

### ❌ DON'T: Trust Outdated Test Examples

```bash
# WRONG: Read any test file without checking age
cat ../../submodules/effect/packages/old-package/test/Old.test.ts

# RIGHT: Check recent packages (sql-sqlite-bun, sql-drizzle)
cat ../../submodules/effect/packages/sql-sqlite-bun/test/Client.test.ts
```

**Why**: Effect evolves rapidly. Recent packages have modern patterns.

### ❌ DON'T: Assume All Submodules Are Relevant

```bash
# WRONG: Explore every submodule for every question
ls ../../submodules/

# RIGHT: Focus on effect, effect-atom, website for Effect questions
cd ../../submodules/effect
cd ../../submodules/effect-atom
cd ../../submodules/website
```

**Why**: Not all submodules are equally important. Prioritize core libraries.

### ❌ DON'T: Skip Cross-Referencing

```bash
# WRONG: Read only one source
cat ../../submodules/website/content/src/content/docs/docs/stream/consuming-streams.mdx

# RIGHT: Cross-reference with tests and TMNL patterns
cat ../../submodules/website/content/src/content/docs/docs/stream/consuming-streams.mdx
find ../../submodules/effect/packages -name "*stream*.test.ts" | xargs grep "filter"
cat .edin/EFFECT_PATTERNS.md | grep -A 10 "Stream"
```

**Why**: Multiple perspectives ensure comprehensive understanding.

### ❌ DON'T: Modify Submodule Files

```bash
# WRONG: Edit submodule files directly
vim ../../submodules/effect/packages/effect/src/Effect.ts

# RIGHT: Reference only, implement in TMNL
cat ../../submodules/effect/packages/effect/src/Effect.ts
# Then implement in src/lib/my-domain/
```

**Why**: Submodules are read-only references. Changes should be in TMNL codebase.

## Quick Reference

### Submodule Navigation Cheatsheet

| Goal | Submodule | Path | Command |
|------|-----------|------|---------|
| Effect test patterns | effect | `packages/*/test/` | `find ../../submodules/effect/packages -name "*.test.ts"` |
| Atom test patterns | effect-atom | `packages/atom/test/` | `ls ../../submodules/effect-atom/packages/atom/test/` |
| Effect documentation | website | `content/src/content/docs/docs/` | `find ../../submodules/website -name "*.mdx"` |
| SQL patterns | effect | `packages/sql-*/test/` | `find ../../submodules/effect/packages -name "*sql*.test.ts"` |
| Stream patterns | website | `docs/stream/` | `ls ../../submodules/website/content/src/content/docs/docs/stream/` |
| Schema patterns | website | `docs/schema/` | `ls ../../submodules/website/content/src/content/docs/docs/schema/` |

### Common Commands

```bash
# Navigate to submodules directory
cd ../../submodules

# List all submodules
ls

# Find all Effect test files
find effect/packages -name "*.test.ts" | head -20

# Find all effect-atom test files
find effect-atom/packages/atom/test -name "*.test.ts"

# Find all website documentation files
find website/content/src/content/docs/docs -name "*.mdx" | head -20

# Search for specific pattern in Effect tests
grep -r "Effect.gen" effect/packages/sql-sqlite-bun/test/

# Search for specific topic in website docs
grep -r "Ref.make" website/content/src/content/docs/docs/state-management/

# Find AG-Grid examples
find ag-grid -name "*Renderer*" -type f | head -10

# Check submodule git status (should be clean)
cd effect && git status

# Update submodule to latest (use sparingly)
cd effect && git pull origin main
```

### Effect Test Pattern Reference

**SQL Client Test** (`sql-sqlite-bun/test/Client.test.ts`):
```typescript
import { it } from "@effect/vitest";
import { SqliteClient } from "@effect/sql-sqlite-bun";

it.effect("should query users", () =>
  Effect.gen(function* () {
    const client = yield* SqliteClient;
    const rows = yield* client.query("SELECT * FROM users");
    expect(rows).toHaveLength(3);
  }).pipe(Effect.provide(TestLayer))
);
```

**Atom Test** (`atom/test/Atom.test.ts`):
```typescript
import { Atom, Registry } from "@effect-atom/atom";

it("should derive atom", () => {
  const r = Registry.make();
  const source = Atom.make(1);
  const derived = Atom.make((get) => get(source) * 2);

  expect(r.get(derived)).toBe(2);
  r.set(source, 5);
  expect(r.get(derived)).toBe(10);
});
```

### Website Documentation Categories

```bash
# Introduction
../../submodules/website/content/src/content/docs/docs/introduction/

# Concurrency (Fibers, Queue, Semaphore)
../../submodules/website/content/src/content/docs/docs/concurrency/

# State Management (Ref, SynchronizedRef)
../../submodules/website/content/src/content/docs/docs/state-management/

# Streams
../../submodules/website/content/src/content/docs/docs/stream/

# Schema
../../submodules/website/content/src/content/docs/docs/schema/

# Additional Resources (Effect vs FP-TS, myths)
../../submodules/website/content/src/content/docs/docs/additional-resources/
```

### Validation Workflow

**When implementing a new pattern**:
1. **Check TMNL docs**: `.edin/EFFECT_PATTERNS.md`, `CLAUDE.md`
2. **Check website submodule**: `../../submodules/website/content/src/content/docs/docs/`
3. **Check Effect tests**: `../../submodules/effect/packages/*/test/`
4. **Check effect-atom tests**: `../../submodules/effect-atom/packages/atom/test/`
5. **Synthesize**: Combine insights from all sources
6. **Implement**: Write code following validated patterns
7. **Document**: Update `.edin/EFFECT_PATTERNS.md` if new pattern emerges

**Golden Rule**: Human-authored docs (website submodule) > Canonical tests (effect/effect-atom submodules) > AI inference (deepwiki).
