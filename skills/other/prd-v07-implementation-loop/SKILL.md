---
name: prd-v07-implementation-loop
description: Execute implementation within EPICs following test-first development, continuous SoT updates, and code traceability during PRD v0.7 Build Execution. Triggers on requests to start building, implement an epic, begin coding, or when user asks "start building", "implement epic", "coding", "development", "build execution", "implementation", "write code". Consumes EPIC- (context), TEST- (acceptance criteria). Updates existing IDs and creates code. Outputs working code with @implements traceability tags.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Implementation Loop

Position in workflow: v0.7 Test Planning → **v0.7 Implementation Loop** → v0.8 Release

## Consumes

This skill requires prior work from v0.7 Epic Scoping and v0.7 Test Planning:

- **EPIC-\* entries** (from v0.7 Epic Scoping) — EPIC context, objectives, Context & IDs table, execution plan phases, Session State tracking
- **TEST-\* test specifications** (from v0.7 Test Planning) — Acceptance criteria in Given-When-Then format; tests define "done" for each deliverable
- **API-\* endpoint contracts** (referenced in EPIC Context & IDs) — Implementation targets with request/response shapes, error codes, constraints
- **DBT-\* schema specifications** (referenced in EPIC Context & IDs) — Data model, field types, relationships, constraints to implement
- **BR-\* business rules** (referenced in EPIC Context & IDs) — Product logic constraints to enforce in code
- **Existing SoT files** (if brownfield) — Durable specs that guide implementation without re-research

This skill assumes EPIC- and TEST- entries are complete, with all upstream IDs fully specified.

## Produces

This skill updates/creates:

- **Working code** (implementation of API-, DBT-, BR-, tested against TEST-) — Runnable code with @implements tags tracing back to specifications; passes all TEST- for EPIC
- **Updated SoT entries** (if implementation reveals changes) — When building reveals new constraints or edge cases, update API-/DBT-/BR- entries immediately (not deferred)
- **Session State updates** (EPIC.md Section 1) — "Brain dump" tracking exact stopping point, Next Steps for resume, blockers, decisions, Context
- **Development Graph** (`status/devgraph.json`) — the `@implements`/`@verifies` tags you write are harvested into bridge edges, producing the as-built layer that readiness scores (`implementation_coverage`, `architecture_conformance`) and the **HeartBeat** visualizer renders. Schema: `docs/DEVELOPMENT_GRAPH.md`.

All implementation outputs are **code and live SoT**, not confidence-based. They are:
- **Traceable** (every function tagged with @implements pointing to specification ID)
- **Tested** (all TEST- for EPIC pass before marking phase/EPIC complete)
- **SoT-synchronized** (implementation matches specs/ or specs/ updated to match implementation reality)
- **Session-state-preserved** (Session State section allows seamless resume from exact stopping point)

Example code with traceability (from EPIC-01):
```typescript
// @implements API-001 (POST /users)
// @see BR-001 (email uniqueness), BR-002 (password requirements), DBT-010 (users table)
export async function createUser(req: Request, res: Response) {
  // @implements BR-002 (password validation)
  const passwordResult = validatePassword(req.body.password);
  if (!passwordResult.valid) {
    return res.status(400).json({
      error: { code: 'INVALID_PASSWORD', message: passwordResult.errors[0] }
    });
  }

  // @implements BR-001 (email uniqueness check)
  const existingUser = await db.users.findByEmail(req.body.email);
  if (existingUser) {
    return res.status(409).json({
      error: { code: 'EMAIL_EXISTS', message: 'User already exists' }
    });
  }

  // @implements DBT-010 (users table creation)
  const user = await db.users.create({
    email: req.body.email,
    passwordHash: await hashPassword(req.body.password),
    createdAt: new Date(),
  });

  return res.status(201).json({ data: { id: user.id, email: user.email } });
}
```

Example Session State update (EPIC-01 mid-session):
```markdown
## 1. Session State (The "Brain Dump")
- **Last Action**: Completed API-001–003 implementation; all tests passing. Password reset flow complete.
- **Stopping Point**: src/api/auth/reset.ts:85 — need to add rate limiting per BR-005
- **Next Steps**:
  1. Add rate limiter middleware to password reset endpoint (BR-005)
  2. Update TEST-012 to verify rate limiting (5 attempts per hour)
  3. Run full test suite for EPIC-01
  4. Move to API-005 (verify email endpoint)
- **Blockers**: None
- **Context**: Decided to implement rate limiting in middleware rather than at function level for reuse across endpoints. Using `express-rate-limit`.
- **Decisions Made**: POST /reset-password should return 429 with retry-after header when limit exceeded (API-001 error response spec). Using Redis for distributed rate limit tracking.

### Resume Instructions
> 1. Load EPIC-01 context (done in previous session)
> 2. Create new branch session if needed
> 3. Begin with Step 3 above (add rate limiter middleware)
> 4. When complete, run: `npm run test -- tests/api/auth.test.ts`
> 5. Update this Session State with new stopping point
```

## This skill executes the build. It's the iterative cycle of: **Load Context → Test → Code → Tag → Update → Validate → Repeat**.

## The Core Loop (The Heartbeat)

Each pass leaves a trace: step 5 tags code with `@implements`, and those tags are exactly what the **Development Graph** harvests — so this loop literally produces the pulse the **HeartBeat** visualizer shows (built → 🟢, unbuilt → 🔴, drifted → 🔴). Rerun `readiness.py run` after a Context Window to watch `implementation_coverage` move.

```
┌─────────────────────────────────────────────────────────────┐
│  1. LOAD CONTEXT                                            │
│     Read EPIC, referenced IDs, Session State                │
│     → Can you state this session's goal in one sentence     │
│       with specific IDs? If not, clarify before proceeding. │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SELECT FOCUS                                            │
│     Choose a Context Window from Phase C                    │
│     → Pick the smallest scope that yields a verifiable      │
│       outcome. One TEST- passing > three half-implemented.  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. WRITE TEST (Red)                                        │
│     Implement TEST- entry, watch it fail                    │
│     → Assertions must derive from TEST-/API-/BR- specs.     │
│       Missing detail = spec gap — flag it, don't guess.     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. WRITE CODE (Green)                                      │
│     Implement to pass test                                  │
│     → Minimum code to pass. No TEST- requires it? Don't     │
│       build it. No speculative features or error handling.   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  5. TAG CODE                                                │
│     Add // @implements ID comments                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  6. UPDATE SoT                                              │
│     Update specs/ if implementation reveals changes         │
│     → Only update specs YOUR implementation changed.        │
│       Don't "improve" adjacent specs you happened to read.  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  7. VALIDATE                                                │
│     Run tests, check traceability                           │
│     → Name the specific TEST- IDs that pass. "It works"     │
│       is not validation — cite IDs.                         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  8. UPDATE SESSION STATE                                    │
│     Write to Session State before stopping                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           └──────────► REPEAT until EPIC complete
```

## Session State Protocol (MANDATORY)

**Before ending ANY session**, update the EPIC Session State section:

```markdown
## 0. Session State (The "Brain Dump")
- **Last Action**: [What was just completed]
- **Stopping Point**: [Exact file:line or test failure]
- **Next Steps**: [Exact instructions for next session]
- **Context**: [Key decisions, blockers, open questions]
```

**Good Example:**
```markdown
- **Last Action**: Completed API-002 (login endpoint), all tests passing
- **Stopping Point**: src/api/auth/login.ts:47 — need to add rate limiting
- **Next Steps**:
  1. Add rate limiter middleware per BR-005
  2. Update TEST-008 to verify rate limiting
  3. Move to API-003 (logout)
- **Context**: Decided to use Supabase's built-in rate limiting rather than custom middleware
```

**Assumptions & Ambiguities**: During implementation, log assumptions and ambiguities in the EPIC's structured table (see EPIC template). This makes "Think Before Coding" persistent across sessions.

Example row during implementation:
```
| 3 | API-001 | ASSUMPTION | Response includes created_at field | Spec says "user object" but doesn't enumerate fields | Implemented with created_at; needs spec update |
```

**Bad Example:**
```markdown
- **Last Action**: Working on auth
- **Stopping Point**: Somewhere in the code
- **Next Steps**: Continue
- **Context**: N/A
```

## Code Traceability Protocol

Every major code unit MUST declare which ID it implements:

```typescript
// @implements API-001 (Create User endpoint)
// @see BR-001 (Email uniqueness)
// @see DBT-001 (Users table)
export async function createUser(data: CreateUserInput): Promise<User> {
  // Implementation...
}
```

### Traceability Tag Patterns

| Code Element | Tag Pattern | Example |
|--------------|-------------|---------|
| API handler | `@implements API-XXX` | API endpoint function |
| Business logic | `@implements BR-XXX` | Validation, rules |
| Database model | `@implements DBT-XXX` | Schema definition |
| UI component | `@implements SCR-XXX` | Screen component |
| Test file | `@tests TEST-XXX` | Test implementation |
| Cross-reference | `@see [ID]` | Related specification |

### Example with Full Traceability

```typescript
// @implements API-001 (POST /users)
// @see BR-001 (email uniqueness)
// @see BR-002 (password requirements)
// @see DBT-001 (users table)
export async function createUser(req: Request, res: Response) {
  // @implements BR-002
  const passwordResult = validatePassword(req.body.password);
  if (!passwordResult.valid) {
    return res.status(400).json({ error: passwordResult.errors });
  }

  // @implements BR-001
  const existingUser = await db.users.findByEmail(req.body.email);
  if (existingUser) {
    return res.status(409).json({ error: { code: 'EMAIL_EXISTS' } });
  }

  // @implements DBT-001
  const user = await db.users.create({
    email: req.body.email,
    passwordHash: await hashPassword(req.body.password),
  });

  return res.status(201).json({ data: user });
}
```

## SoT Update Rules

The Source of Truth (`specs/`) must stay in sync with implementation:

| Situation | Action |
|-----------|--------|
| Spec matches implementation | No update needed |
| Implementation reveals new constraint | Add BR- entry to specs/ |
| API shape changed during build | Update API- entry |
| New field needed in schema | Update DBT- entry |
| Spec was wrong/incomplete | Fix spec AND code |
| Discovered edge case | Add to spec, add TEST- |

**Rule**: Update specs **during** implementation, not "later."

**Counter-rule**: Only update specs that YOUR current work directly affects. If you notice that API-020 has a typo while working on API-001, log it in the Assumptions & Ambiguities table for a future session. Do not fix it now. Unplanned spec changes create invisible scope creep and break traceability for any parallel work.

## Context Window Navigation

Work through Context Windows sequentially within an EPIC:

```markdown
## 4. Context Windows

### Window 1: Database Schema ← CURRENT
- [x] Create users table migration
- [x] Add RLS policies
- [ ] Create sessions table
- [ ] Verify schema in studio

### Window 2: API Endpoints
- [ ] Implement API-001 (signup)
- [ ] Implement API-002 (login)
- [ ] Implement API-003 (logout)

### Window 3: UI Integration
- [ ] Build signup form
- [ ] Build login form
- [ ] Add auth state management
```

## Test-First Development (Red-Green-Refactor)

### Phase 1: Red (Write Failing Test)

```typescript
// tests/api/users.test.ts
// @tests TEST-001

describe('POST /api/users', () => {
  it('creates user with valid data', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@example.com', password: 'ValidPass123!' });

    expect(response.status).toBe(201);
    expect(response.body.data.email).toBe('test@example.com');
    // Test FAILS because endpoint doesn't exist yet
  });
});
```

**Constraint**: If the test requires details not in the TEST- spec (response field names, error codes, status codes), look them up in API-/BR- specs. Do not invent them. If the spec lacks the detail, log an AMBIGUITY in the Assumptions & Ambiguities table before proceeding.

### Phase 2: Green (Make Test Pass)

Write the minimum code to make the test pass:

```typescript
// @implements API-001
export async function createUser(req, res) {
  const user = await db.users.create(req.body);
  return res.status(201).json({ data: user });
}
```

**Constraint**: "Minimum code" means literally what makes this one test go green. No additional validation, no extra error handling, no service layer abstractions unless a TEST- requires that behavior. This feels uncomfortable. That is correct.

### Phase 3: Refactor (Improve Code Quality)

Now improve the code while tests stay green:

```typescript
// @implements API-001
// @see BR-001, BR-002
export async function createUser(req, res) {
  const validated = validateUserInput(req.body); // Add validation
  if (!validated.ok) return res.status(400).json(validated.error);

  const user = await userService.create(validated.data); // Extract service
  return res.status(201).json({ data: user });
}
```

**Constraint**: Refactor only code you just wrote. Do not "improve" existing code that was already working. Do not extract abstractions unless you have 3+ concrete uses (not hypothetical future uses). Do not touch files outside the current focus area. See `references/behavioral-examples.md` for detailed good/bad comparisons.

## EPIC Phases (Detailed)

### Phase A: Plan (Load Context)
- [ ] Read EPIC file
- [ ] Review all referenced IDs (BR-, API-, DBT-)
- [ ] Check Session State section
- [ ] Review Assumptions & Ambiguities table for unresolved items
- [ ] Verify git branch is correct
- [ ] Confirm dependencies are complete
- [ ] Can state session goal in one sentence with specific IDs

If you cannot articulate what this session accomplishes in terms of specific TEST- or API- IDs, you are not ready to build. Refine the goal until it names IDs.

### Phase B: Design (Update Specs)
- [ ] Draft/refine any unclear specs
- [ ] Add missing details discovered during planning
- [ ] Create TEST- entries if not done
- [ ] Update EPIC Context & IDs section

### Phase C: Build (Context Windows)
For each Context Window:
- [ ] Select focus area
- [ ] Write tests for this window
- [ ] Implement code
- [ ] Add traceability tags
- [ ] Run tests, verify passing
- [ ] Update Session State

### Phase D: Validate
- [ ] All TEST- entries for this EPIC pass
- [ ] Manual verification of UJ- journeys
- [ ] `@implements` tags present in all major code units
- [ ] No orphaned code (everything traces to an ID)
- [ ] specs/ updated to match implementation

### Phase E: Finish (Harvest)
- [ ] Move useful temp/ notes to specs/ or archive/
- [ ] Verify all specs/ files match final code
- [ ] Clean Session State section
- [ ] Update EPIC state to Complete
- [ ] Log completion in Change Log
- [ ] Commit with message: `feat(EPIC-XX): [summary]`

## Red Flags (Stop and Fix)

| Signal | Action |
|--------|--------|
| Can't write test | Requirement unclear → revisit spec |
| Test keeps failing | Implementation wrong OR spec wrong → investigate |
| Need code outside EPIC scope | Wrong EPIC boundaries → re-scope |
| Lost context mid-session | Load Session State, verify EPIC context |
| Spec and code diverging | Stop, update spec to match reality |
| Test is testing implementation | Rewrite to test behavior |
| Writing code not required by any TEST- | Speculative — remove it, or write the TEST- first |
| Editing files outside current Context Window | Scope creep — note in Assumptions & Ambiguities table, defer |

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Test-after** | Code written, then "add tests" | Write TEST- implementation first |
| **Spec drift** | Code diverges from specs/ | Update SoT during implementation |
| **Missing traceability** | Code has no @implements tags | Add tags as you write |
| **Session amnesia** | No Session State update | ALWAYS update before stopping |
| **Context switching** | Jumping between EPICs | Finish one EPIC before starting another |
| **One-shot building** | No iteration, just code dump | Follow the loop: test → code → tag |
| **Orphaned code** | Code not linked to any ID | Every function serves an ID |
| **Speculative error handling** | try/catch for scenarios no TEST- covers | Remove it. If the scenario matters, write TEST- first. |
| **Drive-by improvements** | "While I was here, I also improved..." | Revert non-essential changes. Note in Assumptions & Ambiguities table. |
| **Vague completion claims** | "Auth is working" without naming IDs | Always cite IDs: "TEST-001 through TEST-005 pass. API-001, API-002 verified." |

## Quality Gates

Before marking EPIC complete:

- [ ] All TEST- entries pass
- [ ] All code has @implements tags
- [ ] specs/ matches implementation
- [ ] Session State is clean
- [ ] Manual UJ- verification done
- [ ] Change Log updated
- [ ] Development Graph green — `status/devgraph.json` rebuilt; `implementation_coverage` ≥ threshold (no scoped spec unbuilt, no `unbuilt_specs` cap) and no `architecture_conformance` violations

## Downstream Connections

Implementation Loop outputs feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.8 Release** | Completed EPICs ready for deployment | All TEST- pass, SoT current |
| **Code Review** | @implements tags for context | Reviewer knows which BR- to check |
| **Readiness (v0.7)** | Development Graph build-vs-blueprint | `implementation_coverage` + `architecture_conformance` from `status/devgraph.json` |
| **HeartBeat** | The Development Graph as a live pulse | Renders built / unbuilt / drifted across the codebase |
| **Future Sessions** | Session State for continuity | Resume exactly where left off |
| **Maintenance** | Traceability for debugging | "Which BR- does this code implement?" |

## Detailed References

- **Implementation examples**: See `references/examples.md`
- **Traceability patterns**: See `references/traceability.md`
- **Session state guide**: See `references/session-state.md`
- **Behavioral examples (good/bad)**: See `references/behavioral-examples.md`
