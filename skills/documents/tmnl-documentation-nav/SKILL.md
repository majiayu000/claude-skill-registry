---
name: tmnl-documentation-nav
description: Navigate TMNL's documentation hierarchy - CLAUDE.md sections, .edin/ patterns, assets/documents/ ADRs, and submodule docs
triggers:
  - documentation
  - where are the docs
  - find pattern
  - architecture doc
  - ADR
  - design doc
  - EDIN
---

# TMNL Documentation Navigation

Master TMNL's multi-layered documentation system. This skill maps the documentation hierarchy, explains the purpose of each layer, and guides you to the right doc for any context.

## Overview

TMNL documentation is **stratified by audience and scope**:
- **CLAUDE.md** — Agent operating instructions (you are here)
- **.edin/** — EDIN methodology patterns (Effect, testing, services)
- **assets/documents/** — Architecture ADRs, design artifacts
- **src/lib/<domain>/*.md** — Domain-specific technical docs
- **submodules/website/** — Effect-TS canonical human-authored docs
- **.agents/** — Session journals and operational logs

**Documentation Philosophy**:
- **Agent-first** — CLAUDE.md is the prime directive
- **Pattern-driven** — .edin/ provides reusable templates
- **Architecture-driven** — assets/documents/ captures decisions
- **Domain-driven** — src/lib/ docs live next to code

## Canonical Sources

### CLAUDE.md Structure

**Location**: `packages/tmnl/CLAUDE.md` (root of project)

**Sections** (in order of importance):
1. **PERSONA** — Val's identity, mission, style guide
2. **Dependency Discipline** — Import hygiene, grep-before-cutting
3. **Typography Discipline** — 12px floor, no microscopic text
4. **Schema Discipline** — Effect Schema > raw TypeScript types
5. **Overview** — Project summary, Nix flakes
6. **Submodule Reference** — effect, effect-atom locations
7. **NX Project Configuration** — Script/executor alignment
8. **Nix Module Structure** — Tauri, Rust, Python shells
9. **Development Workflow** — Using Nix shells, mission control
10. **Tauri Window Configuration** — Transparent frameless windows
11. **WSLg Rendering Workarounds** — WebKitGTK compositing fix
12. **Layer System Architecture** — (historical, may be outdated)
13. **Schema Discipline** — Effect Schema patterns (critical)
14. **Animation Library** — animatable() + useAnimatable() patterns
15. **Splash Screen** — Q-Branch Brutalist aesthetic
16. **Conceptual Alignment Protocol** — AskUserQuestion workflow
17. **Effect-ification** — feat/tldraw-drag-reticles status
18. **Slider System** — DAW-grade sliders with behaviors
19. **DataManager Architecture** — EPOCH-0002 service-scoped data
20. **useState → effect-atom Migration** — Atom-as-State pattern
21. **Various Notes** — Install location, UI preservation, etc.

**Key Directives**:
- **Schema Discipline** — All domain types MUST use Effect Schema
- **Typography 12px Floor** — No text below 12px, ever
- **Atom-as-State Pattern** — Atoms are primary state, not Effect.Ref
- **Grep Before Cutting** — Audit all usages before removing imports
- **Use Submodules** — Prefer website submodule over deepwiki

### .edin/ Pattern Files

**Location**: `.edin/` (root of project)

**Primary Files**:

| File | Purpose | When to Use |
|------|---------|-------------|
| `EFFECT_PATTERNS.md` | **Comprehensive pattern registry** | Any Effect-related implementation |
| `EFFECT_SERVICE_PATTERNS.md` | Service definition patterns | Creating Effect.Service classes |
| `EFFECT_TESTING_PATTERNS.md` | Testing with @effect/vitest | Writing Effect tests |
| `EFFECT_SQL_SQLITE_PATTERNS.md` | SQL integration patterns | Database operations |
| `SPIKE_METHODOLOGY.md` | Research spike workflow | Exploring unknowns |
| `README.md` | EDIN overview | Understanding EDIN phases |

**Key Insight**: `.edin/` files are **living documents** — they evolve as patterns emerge.

**Subdirectories**:
- `.edin/epochs/` — Time-boxed implementation records (EPOCH-0001, EPOCH-0002, etc.)
- `.edin/archive/` — Deprecated patterns

### assets/documents/ Architecture Docs

**Location**: `assets/documents/` (root of project)

**Categories**:

**Architecture Decision Records (ADRs)**:
- `INFRASTRUCTURE_ADR_001.md` — Phase 0 infrastructure decisions
- `AG_GRID_THEMING_ARCHITECTURE.md` — AG-Grid theme system deep dive
- `CEW_ARCHITECTURE.md` — Component Event Wire architecture
- `LISTENER_ARCHITECTURE.md` — Event listener patterns

**Design Artifacts**:
- `ARCHITECTURE.md` — High-level system architecture
- `ARCHITECTURE_NOTIONAL_SCENARIOS.md` — Use case scenarios
- `SERVICES_INVENTORY.md` — Catalog of all Effect services
- `TESTBED_CATALOG.md` — Index of testbed demonstrations

**Implementation Guides**:
- `PHASE_0_DEPLOYED.md` — Phase 0 deployment status
- `PHASE_0_IMPLEMENTATION.md` — Implementation steps
- `PHASE_0_READY.md` — Readiness checklist

**Specialized Topics**:
- `ENTITY_MANAGEMENT_KERNEL.md` — Entity state management
- `RAW_EVENTS_PANEL_ARCHITECTURE.md` — Event monitoring UI
- `RAF_STREAM_ARCHITECTURE.md` — requestAnimationFrame streams
- `PERCEPTUAL_MOTION_BLUR.md` — Motion blur animation
- `SECURITY_CONSIDERATIONS.md` — Security guidelines

**Subdirectories**:
- `assets/documents/bufferz/` — Buffer management docs
- `assets/documents/effect/` — Effect-specific deep dives
- `assets/documents/graphql/` — GraphQL integration

### Domain-Specific Docs (src/lib/)

**Location**: `src/lib/<domain>/*.md`

**Three-Tier Documentation Strategy**:

1. **ARCHITECTURE.md** — Deep technical design
   - Data structures, algorithms, decision rationale
   - Service interactions, Effect program flows
   - Performance considerations, edge cases
   - **Audience**: Engineers implementing similar systems

2. **CLAUDE.<domain>.md** — Agent handoff guide
   - Quick reference for common tasks
   - Gotchas, anti-patterns, migration notes
   - **Audience**: AI agents (Val, future assistants)

3. **README.md** — User-facing quick start
   - Installation, basic usage, examples
   - API surface overview
   - **Audience**: Developers using the library

**Examples**:
- `src/lib/data-manager/ARCHITECTURE.md` — Hybrid dispatch, kernel architecture
- `src/lib/data-manager/CLAUDE.data-manager.md` — Agent reference
- `src/lib/data-manager/README.md` — Quick start guide

### Submodule Documentation

**Location**: `../../submodules/` (from `packages/tmnl`)

**Effect-TS Website** (Human-Authored Canonical Docs):
- **Path**: `../../submodules/website/content/src/content/docs/`
- **Structure**:
  - `docs/concurrency/` — Fibers, queues, semaphores
  - `docs/state-management/` — Ref, SynchronizedRef, SubscriptionRef
  - `docs/stream/` — Stream creation, consumption, operators
  - `docs/additional-resources/` — Effect vs FP-TS, myths, API reference

**Effect Core Tests** (Canonical Implementation Patterns):
- **Path**: `../../submodules/effect/packages/*/test/`
- **Examples**:
  - `sql-sqlite-bun/test/Client.test.ts` — SQL client testing
  - `sql-drizzle/test/Sqlite.test.ts` — Drizzle integration
  - `effect/test/Effect.test.ts` — Core Effect patterns

**effect-atom Tests** (Atom Testing Patterns):
- **Path**: `../../submodules/effect-atom/packages/atom/test/`
- **Examples**:
  - `Atom.test.ts` — Atom creation, derivation
  - `AtomRef.test.ts` — AtomRef patterns
  - `Result.test.ts` — Result handling

**Key Insight**: When validating patterns, **prefer website submodule over deepwiki** — it's human-authored and battle-tested.

### Session Journals (.agents/)

**Location**: `.agents/` (root of project)

**Structure**:
```
.agents/
├── index.md                    # Session overview
├── context/                    # Persistent context files
└── val/
    └── journal/
        ├── 2025-12-16.md       # Daily session log
        └── ...
```

**Purpose**: Operational logs for multi-session continuity. Journals capture:
- Tasks completed
- Decisions made
- Open questions
- Next steps

**When to Read**: Starting a new session, resuming work, understanding recent changes.

## Patterns

### Documentation Discovery Flow

**Step 1: Check CLAUDE.md**
- Is there a section addressing your question?
- Does it reference a pattern file or ADR?

**Step 2: Check .edin/ Patterns**
- For Effect-related: `EFFECT_PATTERNS.md`
- For testing: `EFFECT_TESTING_PATTERNS.md`
- For services: `EFFECT_SERVICE_PATTERNS.md`

**Step 3: Check Domain Docs**
- `src/lib/<domain>/ARCHITECTURE.md` (deep dive)
- `src/lib/<domain>/CLAUDE.<domain>.md` (quick ref)

**Step 4: Check assets/documents/**
- ADRs for architectural decisions
- Design artifacts for system-level understanding

**Step 5: Check Submodules**
- `../../submodules/website/` for Effect canonical docs
- `../../submodules/effect/packages/*/test/` for test examples

### Pattern Application Flow

**Scenario**: Implementing a new Effect service

**Process**:
1. Read `CLAUDE.md` → **Schema Discipline** section
2. Read `.edin/EFFECT_SERVICE_PATTERNS.md` → Service definition template
3. Check `assets/documents/SERVICES_INVENTORY.md` → Existing services
4. Check `../../submodules/website/content/src/content/docs/docs/` → Effect Context API
5. Implement following patterns
6. Update `.edin/EFFECT_PATTERNS.md` if new pattern emerges

### Documentation Update Protocol

**When Adding a New Pattern**:
1. Document in domain-specific `ARCHITECTURE.md` (if new domain)
2. Add to `.edin/EFFECT_PATTERNS.md` (if reusable pattern)
3. Update `CLAUDE.md` if it's a **prime directive** (e.g., Schema Discipline)
4. Add to `assets/documents/SERVICES_INVENTORY.md` if it's a service

**When Documenting an ADR**:
1. Create `assets/documents/<TOPIC>_ADR_<number>.md`
2. Reference in relevant domain `ARCHITECTURE.md`
3. Update `CLAUDE.md` if it changes workflow

### Searching Documentation

**By Topic**:
```bash
# Find all mentions of "Effect.Service"
grep -r "Effect.Service" .edin/ assets/documents/ src/lib/

# Find all architecture docs
find . -name "ARCHITECTURE.md"

# Find all agent guides
find . -name "CLAUDE*.md"
```

**By Domain**:
```bash
# Find all data-manager docs
ls src/lib/data-manager/*.md
ls assets/documents/*DATA_MANAGER*.md
grep -r "data-manager" .edin/

# Find all slider docs
ls src/lib/slider/*.md
grep -r "slider" assets/documents/
```

**By Submodule**:
```bash
# Find Effect docs on streams
find ../../submodules/website -name "*stream*.mdx"

# Find Effect tests for SQL
find ../../submodules/effect/packages -name "*sql*.test.ts"
```

## Examples

### Example 1: Understanding Effect Schema Usage

**Question**: How should I define domain types?

**Documentation Path**:
1. `CLAUDE.md` → **Schema Discipline** section
   - Rule: Use `Schema.TaggedStruct` for data, `Schema.TaggedClass` for entities
2. `.edin/EFFECT_PATTERNS.md` → **Schema Patterns** section
   - Examples: `TaggedStruct`, `TaggedClass`, branded types
3. `../../submodules/website/content/src/content/docs/docs/schema/` → Canonical examples

**Result**: All domain types use Effect Schema, no raw TypeScript interfaces.

### Example 2: Learning Effect Testing

**Question**: How do I test Effect services?

**Documentation Path**:
1. `.edin/EFFECT_TESTING_PATTERNS.md` → Testing guide
   - Use `@effect/vitest` with `it.effect()`
2. `../../submodules/effect/packages/sql-sqlite-bun/test/Client.test.ts` → Canonical example
3. `.edin/EFFECT_PATTERNS.md` → **Testing Section**

**Result**: Tests use `it.effect(() => Effect.gen(...))` with proper Layer provisioning.

### Example 3: Understanding DataManager Architecture

**Question**: How does DataManager dispatch work?

**Documentation Path**:
1. `src/lib/data-manager/ARCHITECTURE.md` → Hybrid dispatch design
   - Effect fibers + Web Workers
   - Kernel architecture
2. `src/lib/data-manager/CLAUDE.data-manager.md` → Quick reference
3. `assets/documents/SERVICES_INVENTORY.md` → Service catalog entry

**Result**: DataManager uses hybrid dispatch with SearchKernel wrapping FlexSearch/Linear drivers.

### Example 4: Finding Infrastructure Decisions

**Question**: Why PostgreSQL and NATS for Phase 0?

**Documentation Path**:
1. `assets/documents/INFRASTRUCTURE_ADR_001.md` → Decision record
   - PostgreSQL: Relational queries, JSONB support
   - NATS: Pub/sub messaging, JetStream persistence
2. `assets/documents/PHASE_0_DEPLOYED.md` → Deployment status
3. `CLAUDE.md` → **Overview** section references Nix flakes

**Result**: Phase 0 uses PostgreSQL + NATS via Docker Compose, managed by Nix.

### Example 5: Understanding Atom-as-State Pattern

**Question**: Should I use Effect.Ref or Atoms for state?

**Documentation Path**:
1. `CLAUDE.md` → **useState → effect-atom Migration** section
   - **Atom-as-State Pattern**: Atoms are primary state, not Effect.Ref
2. `.edin/EFFECT_PATTERNS.md` → **Atom Patterns** section
   - Service methods mutate Atoms directly
3. `src/components/testbed/DataManagerTestbed.tsx` → Reference implementation

**Result**: Use Atoms as primary state. Services mutate Atoms directly via `Atom.set`. React subscribes via `useAtomValue`.

## Anti-Patterns

### ❌ DON'T: Rely Only on CLAUDE.md

```
Question: How do I implement a new service?
Wrong Path: Read CLAUDE.md only → incomplete understanding
```

**✅ DO**: Follow the documentation hierarchy
```
1. CLAUDE.md → Schema Discipline section
2. .edin/EFFECT_SERVICE_PATTERNS.md → Service template
3. assets/documents/SERVICES_INVENTORY.md → Examples
4. ../../submodules/website/ → Effect Context API
```

### ❌ DON'T: Trust Outdated Sections in CLAUDE.md

```
CLAUDE.md has a "Layer System Architecture" section from early days.
This may be outdated—check domain-specific docs instead.
```

**✅ DO**: Cross-reference with domain docs
```
1. Check CLAUDE.md for high-level guidance
2. Verify with src/lib/<domain>/ARCHITECTURE.md
3. Check git blame to see when section was last updated
```

### ❌ DON'T: Use deepwiki Before Checking Submodules

```
Question: How do I use Effect.Ref?
Wrong Path: Ask deepwiki → AI-generated answer (not battle-tested)
```

**✅ DO**: Check human-authored docs first
```
1. Check ../../submodules/website/content/src/content/docs/docs/state-management/ref.mdx
2. Check ../../submodules/effect/packages/*/test/ for examples
3. Only use deepwiki if submodule docs don't answer question
```

### ❌ DON'T: Create Documentation in Random Locations

```
Created: src/components/my-feature/ARCHITECTURE.md
Wrong: Architecture docs belong in assets/documents/ or src/lib/
```

**✅ DO**: Follow documentation hierarchy
```
Domain-specific: src/lib/<domain>/ARCHITECTURE.md
System-level: assets/documents/<TOPIC>_ARCHITECTURE.md
Agent guide: src/lib/<domain>/CLAUDE.<domain>.md
```

### ❌ DON'T: Skip Updating .edin/ When Patterns Emerge

```
You discover a new pattern for Effect streams.
Wrong: Keep it in your head, don't document it.
```

**✅ DO**: Update pattern registry
```
1. Add to .edin/EFFECT_PATTERNS.md → **Stream Patterns** section
2. Add example to domain ARCHITECTURE.md
3. Update CLAUDE.md if it's a prime directive
```

## Quick Reference

### Documentation Hierarchy Cheatsheet

| Question Type | Primary Source | Secondary Source |
|---------------|---------------|------------------|
| Prime directives | `CLAUDE.md` | N/A |
| Effect patterns | `.edin/EFFECT_PATTERNS.md` | `../../submodules/website/` |
| Service patterns | `.edin/EFFECT_SERVICE_PATTERNS.md` | `assets/documents/SERVICES_INVENTORY.md` |
| Testing patterns | `.edin/EFFECT_TESTING_PATTERNS.md` | `../../submodules/effect/*/test/` |
| Domain architecture | `src/lib/<domain>/ARCHITECTURE.md` | `assets/documents/` |
| ADRs | `assets/documents/*_ADR_*.md` | `CLAUDE.md` |
| Session context | `.agents/val/journal/<date>.md` | `.agents/index.md` |

### Common Documentation Paths

```bash
# Read prime directives
cat CLAUDE.md

# Read Effect patterns
cat .edin/EFFECT_PATTERNS.md

# Read service patterns
cat .edin/EFFECT_SERVICE_PATTERNS.md

# Read testing patterns
cat .edin/EFFECT_TESTING_PATTERNS.md

# Read domain architecture
cat src/lib/data-manager/ARCHITECTURE.md

# Read ADRs
ls assets/documents/*_ADR_*.md

# Read Effect canonical docs
ls ../../submodules/website/content/src/content/docs/docs/

# Read Effect test examples
find ../../submodules/effect/packages -name "*.test.ts" | head -10

# Read session journals
ls .agents/val/journal/
```

### Documentation Update Commands

```bash
# Add new pattern to registry
vim .edin/EFFECT_PATTERNS.md

# Create new ADR
touch assets/documents/MY_TOPIC_ADR_001.md

# Update services inventory
vim assets/documents/SERVICES_INVENTORY.md

# Create domain architecture doc
touch src/lib/my-domain/ARCHITECTURE.md

# Update CLAUDE.md (use sparingly)
vim CLAUDE.md
```
