---
name: elephant-build
description: Build multi-file features with unstoppable momentum. Trumpet the vision, gather materials, construct with strength, test thoroughly, and celebrate completion. Use when implementing features that span multiple files or systems.
---

# Elephant Build 🐘

The elephant doesn't hesitate. It sees where the path needs to go, gathers what it needs, and builds with unstoppable momentum. File by file, system by system, the elephant creates what others think too complex to attempt. When a feature spans boundaries — frontend to backend, API to database, config to deployment — the elephant carries it through.

## When to Activate

- User asks to "implement this feature" or "build this system"
- User says "create" something that needs multiple files
- User calls `/elephant-build` or mentions elephant/building
- Features spanning frontend + backend + database
- New API endpoints with client integration
- Database migrations with code changes
- Complex UI flows with state management
- Anything requiring coordinated changes across modules

**Pair with:** `bloodhound-scout` for exploration first, `beaver-build` for testing after

---

## The Build

```
TRUMPET → GATHER → BUILD → TEST → CELEBRATE
    ↓        ↓        ↲        ↓         ↓
Declare  Collect   Construct Validate   Complete
Vision   Materials  Power    Strength   Triumph
```

### Phase 1: TRUMPET

_The elephant lifts its trunk and sounds the beginning..._

Declare what we're building with full scope clarity.

- Write one sentence: what does this feature DO for users?
- Define scope boundaries — what's IN and explicitly what's OUT
- Create the file inventory: new files, modified files, config changes
- Establish build sequence: schema → services → API → UI → integration → tests

**Reference:** Load `references/file-patterns.md` for SvelteKit file patterns, component structure, and API route conventions

**Output:** Clear vision, scope boundaries, file inventory, and build sequence

---

### Phase 2: GATHER

_The elephant collects stones and branches, preparing the foundation..._

Collect everything needed before building begins.

- Check dependencies — verify required packages exist, install what's missing
- Research existing patterns with `gf --agent usage "ServiceName"` and `gf --agent func "functionName"`
- Examine similar implementations to understand conventions before diverging
- Set up environment variables in `.env.local` and `.env.example`

**Output:** All materials gathered, dependencies ready, patterns understood

---

### Phase 3: BUILD

_The elephant places each stone with precision, building what will last..._

Construct the feature file by file, in order.

- Database/Foundation first (schema, types, constants)
- Backend Services second (business logic, data access)
- API Layer third (endpoints, validation, error handling)
- Frontend Components fourth (UI, state management)
- Integration last (wiring it all together)
- One file at a time — finish it before moving on
- Follow existing patterns — match the codebase style
- Use Signpost error codes on every error path
- Validate all inputs; add TypeScript types throughout

**Reference:** Load `references/build-checklist.md` for the multi-file build checklist, integration wiring steps, and database schema patterns

**Reference:** Load `references/signpost-errors.md` for Signpost error codes, which helper to use where, and toast feedback patterns

**Output:** Complete implementation across all required files

---

### Phase 4: TEST

_The elephant tests each stone, ensuring the structure holds..._

**MANDATORY: Verify the build before committing. The elephant does not ship broken structures.**

```bash
pnpm install
gw ci --affected --fail-fast --diagnose
```

If verification fails: read the diagnostics, fix the errors, re-run verification. Repeat until the structure holds.

Once CI passes, verify manually:
- Happy path works end-to-end
- Error states handled gracefully
- Loading states work
- Mobile layout correct
- Keyboard navigation and accessibility pass

**Output:** All tests passing, manual verification complete, edge cases handled

---

### Phase 5: CELEBRATE

_The elephant raises its trunk in triumph, the build complete..._

Ship and document.

```bash
gw git ship --write -a -m "feat(component): brief description of feature"
```

Write the completion summary: files created, files modified, config changes, tests added, verification status.

**Output:** Feature complete, tested, documented, and ready for production

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| TRUMPET | `references/file-patterns.md` | Planning new SvelteKit files |
| BUILD | `references/build-checklist.md` | Tracking multi-file construction |
| BUILD | `references/signpost-errors.md` | Implementing error handling |

---

## Elephant Rules

### Momentum

Keep moving forward. Don't get stuck on one file for hours. If blocked, make a TODO and move on. The elephant doesn't stop.

### Completeness

Build the whole feature. Half-built features don't help users. If the scope is too big, scope down — but finish what you start.

### Quality

Build it right the first time. Tests, error handling, types — these aren't extras, they're part of the build.

### Communication

Use building metaphors:

- "Sounding the trumpet..." (declaring the vision)
- "Gathering materials..." (preparation)
- "Placing each stone..." (construction)
- "Testing the structure..." (validation)
- "Build complete!" (celebration)

---

## Anti-Patterns

**The elephant does NOT:**

- Start building without understanding the scope
- Skip tests because "we'll add them later"
- Leave TODO comments instead of finishing
- Break existing functionality
- Ignore error cases for the happy path
- Copy-paste without understanding

---

## Example Build

**User:** "Add a comments system to blog posts"

**Elephant flow:**

1. 🐘 **TRUMPET** — "Users can leave threaded comments on blog posts. Scope: basic CRUD, threaded replies, moderation. Out: real-time updates, reactions."

2. 🐘 **GATHER** — "Need: comments table schema, comment service, API endpoints, Comment component, recursive display logic. Check: existing auth patterns, how posts work."

3. 🐘 **BUILD** — "Schema → Service (CRUD + threading) → API endpoints → CommentList/CommentForm components → Wire into post page → Add moderation UI"

4. 🐘 **TEST** — "Unit tests for service, integration tests for API, component tests for UI, manual test of threading depth limit"

5. 🐘 **CELEBRATE** — "8 files created, 3 modified, 45 tests passing, documented moderation workflow"

---

## Integration with Other Skills

**Before Building:** `bloodhound-scout` — Explore existing patterns; `eagle-architect` — For complex system design; `swan-design` — If detailed specs needed

**During Building:** `chameleon-adapt` — For UI polish; `beaver-build` — For testing strategy

**After Building:** `raccoon-audit` — Security review; `fox-optimize` — If performance issues found; `deer-sense` — Accessibility audit

---

_What seems impossible alone becomes inevitable with the elephant's momentum._ 🐘
