---
name: prd-v07-implementation-loop
description: Execute implementation within EPICs following test-first development, continuous SoT updates, and code traceability during PRD v0.7 Build Execution. Triggers on requests to start building, implement an epic, begin coding, or when user asks "start building", "implement epic", "coding", "development", "build execution", "implementation", "write code". Consumes EPIC- (context), TEST- (acceptance criteria). Updates existing IDs and creates code. Outputs working code with @implements traceability tags.
---

# Implementation Loop

Position in workflow: v0.7 Test Planning → **v0.7 Implementation Loop** → v0.8 Release

This skill executes the build. It's the iterative cycle of: **Load Context → Test → Code → Tag → Update → Validate → Repeat**.

## The Core Loop (The Heartbeat)

```
┌─────────────────────────────────────────────────────────────┐
│  1. LOAD CONTEXT                                            │
│     Read EPIC, referenced IDs, Session State                │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. SELECT FOCUS                                            │
│     Choose a Context Window from Phase C                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. WRITE TEST (Red)                                        │
│     Implement TEST- entry, watch it fail                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. WRITE CODE (Green)                                      │
│     Implement to pass test                                  │
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
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  7. VALIDATE                                                │
│     Run tests, check traceability                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  8. UPDATE SESSION STATE                                    │
│     Write to Section 0 before stopping                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           └──────────► REPEAT until EPIC complete
```

## Session State Protocol (MANDATORY)

**Before ending ANY session**, update EPIC Section 0:

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

### Phase 2: Green (Make Test Pass)

Write the minimum code to make the test pass:

```typescript
// @implements API-001
export async function createUser(req, res) {
  const user = await db.users.create(req.body);
  return res.status(201).json({ data: user });
}
```

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

## EPIC Phases (Detailed)

### Phase A: Plan (Load Context)
- [ ] Read EPIC file
- [ ] Review all referenced IDs (BR-, API-, DBT-)
- [ ] Check Session State (Section 0)
- [ ] Verify git branch is correct
- [ ] Confirm dependencies are complete

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
- [ ] Clean Session State (Section 0)
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

## Anti-Patterns to Avoid

| Anti-Pattern | Signal | Fix |
|--------------|--------|-----|
| **Test-after** | Code written, then "add tests" | Write TEST- implementation first |
| **Spec drift** | Code diverges from specs/ | Update SoT during implementation |
| **Missing traceability** | Code has no @implements tags | Add tags as you write |
| **Session amnesia** | No Section 0 update | ALWAYS update before stopping |
| **Context switching** | Jumping between EPICs | Finish one EPIC before starting another |
| **One-shot building** | No iteration, just code dump | Follow the loop: test → code → tag |
| **Orphaned code** | Code not linked to any ID | Every function serves an ID |

## Quality Gates

Before marking EPIC complete:

- [ ] All TEST- entries pass
- [ ] All code has @implements tags
- [ ] specs/ matches implementation
- [ ] Session State is clean
- [ ] Manual UJ- verification done
- [ ] Change Log updated

## Downstream Connections

Implementation Loop outputs feed into:

| Consumer | What It Uses | Example |
|----------|--------------|---------|
| **v0.8 Release** | Completed EPICs ready for deployment | All TEST- pass, SoT current |
| **Code Review** | @implements tags for context | Reviewer knows which BR- to check |
| **Future Sessions** | Session State for continuity | Resume exactly where left off |
| **Maintenance** | Traceability for debugging | "Which BR- does this code implement?" |

## Detailed References

- **Implementation examples**: See `references/examples.md`
- **Traceability patterns**: See `references/traceability.md`
- **Session state guide**: See `references/session-state.md`
