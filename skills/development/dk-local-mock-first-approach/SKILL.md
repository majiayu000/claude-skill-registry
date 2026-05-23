---
name: dk-local-mock-first-approach
description: "Mock-first, layer-by-layer feature development. Instead of building a feature end-to-end and hoping the interface works, start by mocking at the user-facing surface with realistic data, get user acceptance on the experience, then deepen one complexity layer at a time with TDD. Everything is anchored on disk so work survives across sessions. Use whenever building a new feature, adding significant UI, planning a multi-layer change, or when the user mentions 'mock first', 'let me see it first', 'prototype this', 'simulate this feature', 'build this layer by layer', or /dk-local-mock-first-approach."
argument-hint: "[feature description or area to mock]"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-local-mock-first-approach — Mock-First, Layer-by-Layer Feature Development

The traditional approach — build the plumbing, wire the API, then hope the UI works — inverts the feedback loop. You discover experience problems *after* committing to implementation choices. This skill inverts the flow: validate the experience first with realistic mocks, then progressively replace mocks with real code, one complexity layer at a time.

**Why this matters**: A feature that "works" but feels wrong is more expensive to fix than one that was never built. Mock-first means the human curates the *experience* before any plumbing exists. This directly serves the philosophy tenet of **Taste as a Filter** — the system produces options, the human filters. And **Good Enough** — you don't over-engineer layers that haven't been validated yet.

## Context

<feature_context> $ARGUMENTS </feature_context>

If the context above is empty or unclear, ask the user:
1. What feature or change are you building?
2. Which user-facing interfaces does it touch? (UI pages, CLI output, API responses that drive UI)
3. Where should the workspace live? (suggest `docs/mock-first/<feature-slug>/`)

## The Workspace

Everything lives on disk. The workspace is the product, not temp files — it's the organized record of what was mocked, what was accepted, and what's been deepened. It also serves as the resumption anchor: if the conversation compacts or a new session starts, the workspace contains everything needed to continue.

```
docs/mock-first/<feature-slug>/
├── tracker.md                  # Live state (the resumption anchor)
├── surface/
│   ├── interface-map.md        # All user-facing interfaces this feature touches
│   ├── mock-data/              # Actual mock data files (JSON, fixtures, factories)
│   ├── mock-components/        # Mock UI components, stubs, or test pages (if applicable)
│   ├── states.md               # All UI/interface states catalogued
│   └── acceptance.md           # User's acceptance notes + screenshots
├── layer-1/
│   ├── boundary.md             # What this layer is, where the complexity boundary sits
│   ├── test-plan.md            # TDD: tests to write before implementation
│   ├── changes.md              # What changed (files, diffs)
│   └── verification.md         # Tests pass + interface still works
├── layer-2/
│   └── ...
└── summary.md                  # Written when feature ships (or when pausing long-term)
```

### tracker.md template

This file is the single source of truth. Read it at the start of every session or phase transition.

```markdown
# Mock-First: [feature name]

## Feature
What we're building: [one line]
Interfaces affected: [list of UI pages, components, CLI commands]
Workspace: [path to this directory]

## Current State
Phase: [exploring | mocking | accepting | deepening-layer-N | shipped]
Current layer: [surface | layer-N]
Mock data quality: [shallow | realistic | production-grade]

## Layer Progression
- surface: [status] — [what was mocked, acceptance verdict]
- layer-1: [status] — [what was deepened, test results]
- layer-2: [status] — [...]

## Decisions Log
- [Date]: [Decision and rationale — things the user accepted, rejected, or modified]

## What We've Learned
- [Accumulated insights — edge cases discovered, states that were missing, etc.]

## Next
[What to do next, or "SHIPPED: [date]"]
```

## The Process

### Phase 0: EXPLORE & MAP

Before writing any mock, understand the full scope of what the user will see and touch.

**Step 1: Map the interaction surface.**

Spawn a haiku explorer to identify all user-facing interfaces this feature affects. Not plumbing (services, utilities, middleware) — the points where a human's eyes and hands meet the system.

```
Task(model: haiku, subagent_type: Explore)

Explore the codebase to map all user-facing interfaces that would be affected by: [feature description]

For each interface found, note:
1. File path and component/page name
2. What the user currently sees/does there
3. What would change with the new feature
4. Data dependencies — what data does this interface need?

Focus only on interfaces the user directly interacts with (UI components, pages, CLI output, API responses that drive UI). Skip internal services, utilities, middleware.
```

**Step 2: Catalogue the states.**

Every interface has more states than "happy path." Before mocking, enumerate them. Write to `surface/states.md`:

```markdown
# Interface States for [Feature]

## [Interface/Component 1]
- **Happy path**: [description]
- **Empty state**: [no data yet — what does the user see?]
- **Loading state**: [data is being fetched]
- **Error state**: [API failed, validation failed, permission denied]
- **Edge cases**: [long text, many items, zero items, special characters]
- **Partial state**: [some data loaded, some pending]
- **Transition states**: [between actions — optimistic updates, confirmation dialogs]

## [Interface/Component 2]
- ...
```

This catalogue is critical — it prevents the classic mock-first pitfall of building a beautiful happy path and discovering the edge cases only during real implementation.

**Step 3: Write the interface map.**

Write `surface/interface-map.md` summarizing what was found. This becomes the feature's north star — everything built should trace back to something on this map.

**Step 4: Initialize tracker.md** with Phase set to `mocking`.

### Phase 1: MOCK AT THE SURFACE

Build the feature's user-facing experience using only mock data. The goal is: the user can see, click, and evaluate the full feature without any backend/service/persistence changes.

**Principles for good mocks:**

1. **Realistic, not shallow.** Mock data should include edge cases: long names, missing optional fields, various status combinations, timestamps at interesting boundaries. If your mock data is `{ name: "Test User", email: "test@test.com" }`, it's too shallow. Use data that exercises the states catalogue from Phase 0.

2. **Complex enough to surface problems.** If the feature involves a list, mock 50 items, not 3. If it involves a form, mock validation errors. If it involves a workflow, mock every transition.

3. **Isolated at a clean boundary.** The mock boundary should be where data enters the interface — typically at the API call layer, the state management layer, or a data provider. This lets you swap mocks for real data later without touching the interface code.

4. **Self-contained.** Another developer (or a future session) should be able to run the mocked version without setting up the full backend. Document how to run the mocked version in `surface/acceptance.md`.

**How to build the mocks:**

For **frontend features**:
- Create mock data files in `surface/mock-data/` (JSON, TypeScript fixtures, factory functions)
- If the project uses a data-fetching layer (React Query, SWR, custom hooks), mock at that boundary
- If the project has a component library, build with real components + mock data
- Consider using a mock route or feature flag to toggle mock mode

For **CLI features**:
- Create mock output fixtures in `surface/mock-data/`
- Build the output formatting/display logic with mock data piped in
- The user should be able to run the CLI and see realistic output

For **API-driven features**:
- Create mock response fixtures
- Wire them into the consumer (frontend, CLI) at the fetch boundary

**After building mocks, write the mock data to disk** in `surface/mock-data/`. This is reference material for later — when deepening, you'll compare real data against these mocks to ensure nothing was lost.

### Phase 2: ACCEPTANCE GATE

This is the **Taste as a Filter** moment. The user evaluates the mocked experience and decides if it's right before any real implementation starts.

Present the mocked feature to the user. Ask them to evaluate:

1. **Does the happy path feel right?** Is this the experience you imagined?
2. **Are the edge cases handled?** Walk through the states catalogue — does each state make sense?
3. **What's missing?** States, interactions, or data you didn't anticipate?
4. **What's wrong?** Layout, flow, information hierarchy, wording?

Capture their feedback in `surface/acceptance.md`:

```markdown
# Acceptance: [Feature Name]

## Date: [YYYY-MM-DD]

## Verdict: [ACCEPTED / ACCEPTED WITH CHANGES / REJECTED]

## What works
- [Specific things the user approved]

## What needs to change
- [Specific changes requested, with priority]

## Missing states/scenarios discovered
- [Things not in the original states catalogue]

## How to run the mocked version
[Exact commands or steps to see the mocked feature]
```

If changes are needed, iterate on the mocks before proceeding. This is cheap — you're only changing mock data and interface code, not unwinding real implementation.

**Only proceed to Phase 3 after acceptance.** This gate is the whole point. Deepening a feature the user hasn't validated wastes real implementation effort.

### Phase 3: DEEPEN — Layer by Layer

Now the real implementation begins, but controlled. Each layer:
1. Identifies a legitimate complexity boundary
2. Writes failing tests first (TDD)
3. Replaces mocks with real code at that boundary
4. Verifies the interface still works as accepted

**What is a "layer"?**

Not a function call depth. A layer is a legitimate complexity boundary — a place where the nature of the work changes, where new categories of problems can emerge, where different expertise or thinking is required.

Read `references/layer-deepening.md` for detailed examples, but the general pattern:

| Layer | What you're replacing | New complexity introduced |
|-------|----------------------|--------------------------|
| Surface | Nothing — mocks only | UX, layout, interaction design |
| Layer 1 | Mock data → real state management | State transitions, optimistic updates, caching |
| Layer 2 | Mock API → real API calls | Network errors, auth, pagination, rate limits |
| Layer 3 | Mock service → real business logic | Validation rules, edge cases, domain invariants |
| Layer 4 | Mock persistence → real DB | Migrations, queries, transactions, data integrity |
| Layer 5 | Mock externals → real external services | Timeouts, retries, API changes, cost |

Not every feature has 5 layers. Some have 2. The point is to identify where the complexity changes character, not to artificially create layers.

**For each layer:**

**Step 1: Document the boundary** — Write `layer-N/boundary.md`:
```markdown
# Layer N: [Name]

## What's being replaced
[Which mocks are being swapped for real code]

## New complexity this introduces
[What categories of problems can now occur that couldn't before]

## Files affected
[List of files that will change]

## Risk assessment
[What could break, what's the blast radius]
```

**Step 2: Write failing tests (TDD)** — Write `layer-N/test-plan.md` first, then write the actual test files:
```markdown
# Test Plan: Layer N

## Tests to write
- [ ] [Test 1: description — what it proves]
- [ ] [Test 2: description — what it proves]
- [ ] [Edge case test: description]
- [ ] [Error case test: description]

## What these tests replace
[Which mock behaviors are now being tested for real]
```

Run the tests. They must fail. A test that passes before implementation is suspicious — either the mock boundary was wrong or the test isn't testing what you think.

**Step 3: Implement** — Replace mocks with real code at this layer only. Don't reach ahead into deeper layers.

**Step 4: Verify** — Write `layer-N/verification.md`:
```markdown
# Verification: Layer N

## Tests
- [x] All new tests pass
- [x] All existing tests still pass
- [ ] No regressions in previously accepted interface behavior

## Interface check
[Does the user-facing experience still match what was accepted in Phase 2?]
[If anything changed, note it here — even if it's "better"]

## Mock boundary moved to
[Where are mocks now? What's the new mock boundary for the next layer?]
```

**Step 5: Update tracker.md** — Record the layer completion, update current state.

**Step 6: Mini-acceptance** — If this layer changed anything the user can see (even subtly — like real data replacing mock data), show the user and confirm it still meets acceptance.

Repeat for each layer until the feature is fully implemented.

### Phase 4: SHIP

When all layers are deepened and the feature works end-to-end with real code:

1. Run the full test suite
2. Do a final live verification with the user
3. Write `summary.md`:

```markdown
# Summary: [Feature Name]

## Result
Started: [date]
Shipped: [date]
Layers deepened: [N]
Total iterations on mocks: [count]

## Architecture decisions
- [Key decisions made during deepening, with rationale]

## What the mocks caught early
- [Problems discovered during mock phase that would have been expensive to find later]

## Layer progression
- Surface: [what was mocked, key insights]
- Layer 1: [what was deepened, surprises]
- ...

## If revisiting later
[Context needed to understand why things are built this way]
```

4. Update tracker.md status to `shipped`
5. Consider running `/dk-compound` to capture any reusable learnings

## Context Management Rules

Same discipline as dk-close-the-loop — the workspace is the memory, not the conversation:

1. **Never paste full mock data or test files into the conversation.** They live on disk. Subagents read them from disk.

2. **The user sees summaries, not data.** After each phase, report in 3-5 lines: what happened, what was found, what's next. They can dig into the workspace for details.

3. **tracker.md is the resumption point.** New session? Read tracker.md first. It tells you exactly where you are and what to do next.

4. **One layer at a time.** Resist the urge to deepen two layers simultaneously. If you change two boundaries at once and something breaks, you don't know which layer caused it. This directly follows the CLAUDE.md principle: "Change one thing at a time."

5. **Mock data is a first-class artifact.** Don't delete mock data after deepening — it serves as documentation of the intended behavior and as test fixtures. Move it to `surface/mock-data/` if it doesn't already live there.

## When NOT to use this skill

- **Single-file bug fixes** — just fix the bug
- **Purely backend changes with no interface impact** — no interface to mock
- **Config changes, dependency updates, refactoring** — no new user-facing behavior
- **Changes where the interface is already clear and validated** — skip straight to TDD

The skill is for features where the *experience* needs validation before the *implementation* begins. If you already know exactly what the user should see, you don't need to mock it first.
