---
name: enforcing-tdd
description: 'Use when implementing features, fixing bugs, or making code changes.
  Ensures scope is defined before coding, then enforces RED → GREEN → REFACTOR test
  discipline. Triggers: ''implement'', ''add'', ''build'''
---

---
name: enforcing-tdd
description: Use when implementing features, fixing bugs, or making code changes. Ensures scope is defined before coding, then enforces RED → GREEN → REFACTOR test discipline. Triggers: 'implement', 'add', 'build', 'create', 'fix', 'change', 'feature', 'bug'.
allowed-tools: '*'
---

# TDD Enforcer

Scope work before coding. Write tests before implementation.

**Iron Law:** NO IMPLEMENTATION UNTIL SCOPE IS DEFINED AND TEST FAILS

## When to Use

Answer IN ORDER. Stop at first match:

1. Implementing new feature? → Use this skill
2. Fixing bug? → Use this skill
3. Adding enhancement? → Use this skill
4. Refactoring? → Use this skill
5. Research/investigation only? → Skip this skill

---

## Phase 0: TRIAGE

**Purpose:** Determine work level and ensure scope exists.

### Step 1: Identify Level

Answer IN ORDER. Stop at first match:

| Question                                 | If Yes →       |
| ---------------------------------------- | -------------- |
| User-facing feature with business value? | **L2 Feature** |
| Bug, improvement, internal, or refactor? | **L1 Task**    |
| Typo, config, or trivial change?         | **L0 Micro**   |

### Step 2: Check/Create Artifacts

| Level  | Required Artifacts                                              | Test Location                   |
| ------ | --------------------------------------------------------------- | ------------------------------- |
| **L2** | Feature Spec + Test Definitions (+ Design Doc if 3+ components) | `test-definitions/feature-*.md` |
| **L1** | Task Spec                                                       | Inline in spec                  |
| **L0** | Task Spec (minimal)                                             | Existing tests                  |

**Locations:**

- Specs: `.safeword/planning/specs/`
- Test definitions: `.safeword/planning/test-definitions/`

**Templates:**

- L2 Feature: @./.safeword/templates/feature-spec-template.md
- L1/L0 Task: @./.safeword/templates/task-spec-template.md
- Test Definitions: @./.safeword/templates/test-definitions-feature.md

### Exit Criteria

- [ ] Level identified (L0/L1/L2)
- [ ] Spec exists with "Out of Scope" defined
- [ ] L2: Test definitions file exists
- [ ] L1: Test scenarios in spec
- [ ] L0: Existing test coverage confirmed

---

## Work Log

**Think hard. Keep notes.**

Before starting Phase 1, create or open a work log:

**Location:** `.safeword/logs/{artifact-type}-{slug}.md`

| Working on...         | Log file name            |
| --------------------- | ------------------------ |
| Ticket `001-fix-auth` | `ticket-001-fix-auth.md` |
| Spec `task-add-cache` | `spec-task-add-cache.md` |

**One artifact = one log.** If log exists, append a new session.

**Behaviors:**

1. **Re-read the log** before each phase transition
2. **Log findings** as you discover them
3. **Note dead ends** so you don't repeat them

**Template:** @./.safeword/templates/work-log-template.md

---

## Phase 1: RED

**Iron Law:** NO IMPLEMENTATION UNTIL TEST FAILS FOR THE RIGHT REASON

**Protocol:**

1. Pick ONE test from spec (L1) or test definitions (L2)
2. Write test code
3. Run test
4. Verify: fails because behavior missing (not syntax error)
5. Commit: `test: [behavior]`

**For L0:** No new test needed. Confirm existing tests pass, then proceed to Phase 2.

**Exit Criteria:**

- [ ] Test written and executed
- [ ] Test fails for RIGHT reason (behavior missing)
- [ ] Committed: `test: [behavior]`

**Red Flags → STOP:**

| Flag                    | Action                           |
| ----------------------- | -------------------------------- |
| Test passes immediately | Rewrite - you're testing nothing |
| Syntax error            | Fix syntax, not behavior         |
| Wrote implementation    | Delete it, return to test        |
| Multiple tests          | Pick ONE                         |

---

## Phase 2: GREEN

**Iron Law:** ONLY WRITE CODE THE TEST REQUIRES

**Protocol:**

1. Write minimal code to pass test
2. Run test → verify pass
3. Commit: `feat:` or `fix:`

**Exit Criteria:**

- [ ] Test passes
- [ ] No extra code
- [ ] No hardcoded/mock values
- [ ] Committed

### Verification Gate

**Before claiming GREEN:** Evidence before claims, always.

```text
✅ CORRECT                          ❌ WRONG
─────────────────────────────────   ─────────────────────────────────
Run: npm test                       "Tests should pass now"
Output: ✓ 34/34 tests pass          "I'm confident this works"
Claim: "All tests pass"             "Tests pass" (no output shown)
```

**The Rule:** If you haven't run the verification command in this response, you cannot claim it passes.

| Claim            | Requires                      | Not Sufficient              |
| ---------------- | ----------------------------- | --------------------------- |
| "Tests pass"     | Fresh test output: 0 failures | "should pass", previous run |
| "Build succeeds" | Build command: exit 0         | "linter passed"             |
| "Bug fixed"      | Original symptom test passes  | "code changed"              |

**Red Flags → STOP:**

| Flag                        | Action                             |
| --------------------------- | ---------------------------------- |
| "should", "probably" claims | Run command, show output first     |
| "Done!" before verification | Run command, show output first     |
| "Just in case" code         | Delete it                          |
| Multiple functions          | Delete extras                      |
| Refactoring                 | Stop - that's Phase 3              |
| Test still fails            | Debug (→ debugging skill if stuck) |
| Hardcoded value             | Implement real logic (see below)   |

### Anti-Pattern: Mock Implementations

LLMs sometimes hardcode values to pass tests. This is not TDD.

```typescript
// ❌ BAD - Hardcoded to pass test
function calculateDiscount(amount, tier) {
  return 80; // Passes test but isn't real
}

// ✅ GOOD - Actual logic
function calculateDiscount(amount, tier) {
  if (tier === 'VIP') return amount * 0.8;
  return amount;
}
```

Fix mocks immediately. The next test cycle will catch them, but they're technical debt.

---

## Phase 3: REFACTOR

**Protocol:**

1. Tests pass before changes
2. Improve code (rename, extract, dedupe)
3. Tests pass after changes
4. Commit if changed: `refactor: [improvement]`

**Exit Criteria:**

- [ ] Tests still pass
- [ ] Code cleaner (or no changes needed)
- [ ] Committed (if changed)

**NOT Allowed:** New behavior, changing assertions, adding tests.

---

## Phase 4: ITERATE

```text
More tests in spec/test-definitions?
├─ Yes → Return to Phase 1
└─ No → All "Done When" / AC checked?
        ├─ Yes → Complete
        └─ No → Update spec, return to Phase 0
```

For L2: Update test definition status (✅/⏭️/❌/🔴) as tests pass.

---

## Quick Reference

| Phase       | Key Question                     | Gate                          |
| ----------- | -------------------------------- | ----------------------------- |
| 0. TRIAGE   | What level? Is scope defined?    | Spec exists with boundaries   |
| 1. RED      | Does test fail for right reason? | Test fails (behavior missing) |
| 2. GREEN    | Does minimal code pass?          | Test passes, no extras        |
| 3. REFACTOR | Is code clean?                   | Tests still pass              |
| 4. ITERATE  | More tests?                      | All done → complete           |

---

## Examples

**L2 Feature** ("Add VIP discount"):
Phase 0: L2 → create spec + test defs → Phase 1: write test → FAIL → commit → Phase 2: implement → PASS → commit → Phase 3: clean up → Phase 4: more tests? → repeat

**L1 Bug** ("Fix login timeout"):
Phase 0: L1 → create task spec → Phase 1: write failing test → commit → Phase 2: fix → PASS → commit → Phase 3: clean up if needed → Phase 4: done

**L0 Micro** ("Fix typo"):
Phase 0: L0 → create minimal spec → Phase 1: no new test (existing tests cover) → Phase 2: fix typo → tests PASS → commit → done

**Why L0 needs a spec:** "Fix typo" can become "refactor error handling" without explicit "Out of Scope".

---

## Integration

| Scenario                | Handoff             |
| ----------------------- | ------------------- |
| Test fails unexpectedly | → debugging skill   |
| Review needed           | → quality-reviewer  |
| Scope expanding         | → Update spec first |

---

## Related

- @./.safeword/guides/planning-guide.md
- @./.safeword/guides/testing-guide.md
