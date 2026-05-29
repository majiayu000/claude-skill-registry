---
name: effect-research
description: Effect-TS specialized research via deepwiki and submodules. Query Effect-TS/effect, tim-smart/effect-atom for verified patterns. Enforces grounded verification before implementation.
model_invoked: true
triggers:
  - "Effect pattern"
  - "Effect-TS"
  - "effect-atom"
  - "Schema pattern"
  - "Layer composition"
  - "Effect.Service"
  - "Atom.runtime"
  - "how does Effect"
  - "current Effect API"
---

# Effect-TS Research Protocol

**Purpose**: Specialized research workflow for Effect-TS, effect-atom, and related ecosystem. Ensures verified patterns before implementation.

## Quick Start: Research Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│  EFFECT RESEARCH WORKFLOW                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. ADMIT UNCERTAINTY                                            │
│     "My Effect knowledge is from May 2025..."                    │
│                                                                  │
│  2. QUERY DEEPWIKI (Verification Style)                          │
│     "Is [PATTERN] still correct for [USE CASE]?"                 │
│     Repos: Effect-TS/effect, tim-smart/effect-atom               │
│                                                                  │
│  3. CROSS-REFERENCE SUBMODULES                                   │
│     ../../submodules/website/  → Human docs (priority)           │
│     ../../submodules/effect/   → Test patterns                   │
│     ../../submodules/effect-atom/ → Atom patterns                │
│                                                                  │
│  4. CHECK CODEBASE PRECEDENT                                     │
│     .edin/EFFECT_PATTERNS.md                                     │
│     src/lib/*/  → Working implementations                        │
│                                                                  │
│  5. IMPLEMENT WITH CONFIDENCE                                    │
│     [VERIFIED] pattern from step 2-4                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## deepwiki Queries for Effect

### Available Repos

| Repo | deepwiki Name | Content |
|------|---------------|---------|
| Effect Core | `Effect-TS/effect` | Effect, Schema, Stream, Layer, etc. |
| effect-atom | `tim-smart/effect-atom` | Atom, Registry, React integration |

### Query Patterns

**Service Definition**:
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "What is the current recommended pattern for defining Effect
             services with Effect.Service<>()? I believe it uses
             double-parenthesis syntax. Is this still accurate?"
```

**Schema Patterns**:
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "For discriminated unions, should I use Schema.TaggedStruct
             or Schema.TaggedClass? When would I choose one over the other?"
```

**Atom Integration**:
```
mcp__deepwiki__ask_question
  repoName: "tim-smart/effect-atom"
  question: "What is the correct way to use Atom.runtime with Effect
             services? I want to create operation atoms that can yield
             services from a Layer."
```

**Stream Patterns**:
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "Is Stream.fromQueue still the recommended way to create
             streams from async sources? What about backpressure handling?"
```

---

## Submodule Deep Dives

### Website Submodule (Human-Authored Docs)

**Location**: `../../submodules/website/content/src/content/docs/docs/`

**Key Directories**:
```
docs/
├── introduction/        # Getting started
├── guides/              # Best practices
├── concurrency/         # Fibers, Queue, Semaphore
├── state-management/    # Ref, SynchronizedRef
├── stream/              # Stream creation, transformation
├── schema/              # Schema definition, validation
└── additional-resources/ # Migration, myths
```

**Common Queries**:
```bash
# Find service documentation
find ../../submodules/website -name "*.mdx" | xargs grep -l "Effect.Service"

# Find schema documentation
cat ../../submodules/website/content/src/content/docs/docs/schema/*.mdx

# Find state management docs
ls ../../submodules/website/content/src/content/docs/docs/state-management/
```

### Effect Submodule (Test Patterns)

**Location**: `../../submodules/effect/packages/`

**Key Test Directories**:
```
packages/
├── effect/test/           # Core Effect tests
├── sql-sqlite-bun/test/   # SQLite integration (modern patterns)
├── sql-drizzle/test/      # Drizzle ORM patterns
├── platform/test/         # Platform services
└── experimental/test/     # EventLog, DevTools
```

**Common Queries**:
```bash
# Find service test patterns
grep -r "Effect.Service" ../../submodules/effect/packages/*/test/

# Find SQL transaction patterns
grep -r "transaction" ../../submodules/effect/packages/sql-sqlite-bun/test/

# Find Stream test patterns
find ../../submodules/effect/packages/effect/test -name "*Stream*"
```

### effect-atom Submodule (Atom Patterns)

**Location**: `../../submodules/effect-atom/packages/atom/`

**Key Files**:
```
packages/atom/
├── src/Atom.ts           # Atom implementation
├── src/Registry.ts       # Registry implementation
├── test/Atom.test.ts     # Atom test patterns
├── test/Result.test.ts   # Result handling
└── test/AtomRpc.test.ts  # RPC patterns
```

**Common Queries**:
```bash
# Atom test patterns
cat ../../submodules/effect-atom/packages/atom/test/Atom.test.ts

# Registry patterns
grep -r "Registry.make" ../../submodules/effect-atom/packages/atom/test/

# React integration
cat ../../submodules/effect-atom/packages/atom-react/src/index.ts
```

---

## Research Templates by Topic

### Topic: Service Definition

```markdown
## Research: Effect Service Definition

**Question**: What's the current pattern for Effect.Service<>()?

**Step 1: deepwiki Verification**
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "I believe Effect.Service<MyService>()('id', { effect, dependencies })
             is the current syntax. Is this accurate? Has anything changed
             regarding service definition in recent versions?"
```

**Step 2: Submodule Cross-Reference**
```bash
# Check website docs
grep -r "Effect.Service" ../../submodules/website/content/src/content/docs/

# Check test patterns
grep -r "Effect.Service" ../../submodules/effect/packages/sql-sqlite-bun/test/
```

**Step 3: Codebase Precedent**
```bash
grep -r "Effect.Service" src/lib/*/
cat .edin/EFFECT_SERVICE_PATTERNS.md
```
```

### Topic: Schema Definition

```markdown
## Research: Schema Patterns

**Question**: TaggedStruct vs TaggedClass - when to use which?

**Step 1: deepwiki Verification**
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "When should I use Schema.TaggedStruct vs Schema.TaggedClass?
             My understanding: TaggedStruct for pure data, TaggedClass
             when I need methods. Is this correct?"
```

**Step 2: Submodule Cross-Reference**
```bash
cat ../../submodules/website/content/src/content/docs/docs/schema/*.mdx
grep -r "TaggedStruct\|TaggedClass" ../../submodules/effect/packages/effect/src/Schema.ts
```
```

### Topic: Atom + React Integration

```markdown
## Research: Atom.runtime Pattern

**Question**: How do I create operation atoms with Atom.runtime?

**Step 1: deepwiki Verification**
```
mcp__deepwiki__ask_question
  repoName: "tim-smart/effect-atom"
  question: "What's the correct way to use Atom.runtime.fn() to create
             operation atoms that can yield Effect services? I want to
             compose a Layer and create callable atoms."
```

**Step 2: Submodule Cross-Reference**
```bash
cat ../../submodules/effect-atom/packages/atom/test/Atom.test.ts
grep -r "runtime" ../../submodules/effect-atom/packages/atom/src/
```

**Step 3: Codebase Precedent**
```bash
grep -r "Atom.runtime\|runtimeAtom" src/lib/*/atoms/
cat src/lib/slider/atoms/index.ts
```
```

### Topic: Stream Patterns

```markdown
## Research: Effect Streams

**Question**: Creating streams from async sources with backpressure

**Step 1: deepwiki Verification**
```
mcp__deepwiki__ask_question
  repoName: "Effect-TS/effect"
  question: "What's the recommended way to create Effect Streams from
             async sources like WebSockets? I'm considering Stream.async
             and Stream.fromQueue. Which handles backpressure better?"
```

**Step 2: Submodule Cross-Reference**
```bash
cat ../../submodules/website/content/src/content/docs/docs/stream/*.mdx
find ../../submodules/effect/packages/effect/test -name "*Stream*" | xargs head -50
```
```

---

## Verification Checklist

Before implementing any Effect pattern:

### Service Patterns
- [ ] Verified Effect.Service<>() syntax via deepwiki
- [ ] Checked submodule test for working example
- [ ] Confirmed dependencies array behavior
- [ ] Verified `.Default` layer generation

### Schema Patterns
- [ ] Verified Schema.* function exists in current API
- [ ] Checked for transform/encode/decode behavior
- [ ] Confirmed branded type syntax
- [ ] Verified with Schema.is runtime check

### Atom Patterns
- [ ] Verified Atom.runtime API via deepwiki
- [ ] Checked effect-atom tests for pattern
- [ ] Confirmed Registry.make() usage
- [ ] Verified React hook compatibility

### Layer Patterns
- [ ] Verified Layer composition functions
- [ ] Checked Layer.mergeAll, Layer.provide order
- [ ] Confirmed dependency resolution
- [ ] Tested with Effect.runPromise

---

## Common Pitfalls

### ❌ Assuming Effect.Ref for React State

```typescript
// WRONG - Don't use Ref when React consumes state
const stateRef = yield* Ref.make(initial)
```

**Correct**: Use Atom.make() when React is the consumer

### ❌ Single-parenthesis Effect.Service

```typescript
// WRONG
class MyService extends Effect.Service<MyService>("id", {}) {}

// CORRECT (double parenthesis)
class MyService extends Effect.Service<MyService>()("id", {}) {}
```

### ❌ Missing `as const` on service returns

```typescript
// WRONG
return { method }

// CORRECT
return { method } as const
```

### ❌ Trusting cached mental models

```
// WRONG
"I know how Effect.Service works..."

// CORRECT
[UNCERTAIN] Let me verify the current Effect.Service API...
```

---

## Integration with Other Skills

| After Research | Use Skill |
|----------------|-----------|
| Service pattern verified | `/effect-service-authoring` |
| Schema pattern verified | `/effect-schema-mastery` |
| Atom pattern verified | `/effect-atom-integration` |
| Stream pattern verified | `/effect-stream-patterns` |
| Match pattern verified | `/effect-match-patterns` |

---

## Quick Commands

```bash
# Research service patterns
mcp__deepwiki__ask_question repoName="Effect-TS/effect" question="Effect.Service current API"

# Research atom patterns
mcp__deepwiki__ask_question repoName="tim-smart/effect-atom" question="Atom.runtime usage"

# Cross-reference website docs
find ../../submodules/website -name "*.mdx" | xargs grep -l "TOPIC"

# Cross-reference test patterns
find ../../submodules/effect/packages -name "*.test.ts" | xargs grep -l "TOPIC"

# Check codebase precedent
grep -r "PATTERN" src/lib/*/
cat .edin/EFFECT_PATTERNS.md
```
