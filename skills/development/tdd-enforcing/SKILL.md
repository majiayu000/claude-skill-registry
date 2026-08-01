---
name: tdd-enforcing
description: 'Use when implementing features, fixing bugs, or making code changes.
  Ensures scope is defined before coding, then enforces RED → GREEN → REFACTOR test
  discipline. Triggers: ''implement'', ''add'', ''build'''
---

---
name: tdd-enforcing
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

**Source of truth:** See Story 1 in `.safeword-project/specs/feature-stateful-bdd-flow.md` for full detection algorithm rationale.

### Step 1: Identify Level

**Work levels:**

| Level   | Name           | Meaning                   | Process    |
| ------- | -------------- | ------------------------- | ---------- |
| patch   | Quick fix      | Typo, config, trivial bug | Direct fix |
| task    | Bounded work   | Single observable change  | TDD        |
| feature | New capability | Multiple scenarios needed | BDD        |

Follow this decision tree. Stop at first match:

```
Is this explicitly a bug fix, typo, or config change?
├─ Yes → patch (direct fix, no test unless regression-prone)
└─ No ↓

Does request mention "feature", "add", "implement", "support", "build"?
├─ No → task (TDD with E2E test)
└─ Yes ↓

Will it require 3+ files AND (new state OR multiple user flows)?
├─ Yes → feature (BDD) — hand off to safeword-bdd skill
└─ No / Unsure ↓

Can ONE E2E test cover the observable change?
├─ Yes → task (TDD with E2E test)
└─ No → feature (BDD) — hand off to safeword-bdd skill

Fallback: task. User can `/bdd` to override.
```

**Detection signals:**

| Signal        | task (TDD)                | feature (BDD)                   |
| ------------- | ------------------------- | ------------------------------- |
| Files touched | 1-2 files                 | 3+ files                        |
| Test count    | 1 E2E test sufficient     | Multiple scenarios needed       |
| State changes | None or trivial           | New state machine / transitions |
| User flows    | Single path               | Multiple paths / branching      |
| Keywords      | "change", "fix", "update" | "add", "implement", "feature"   |

**Examples:**

| Request                      | Level   | Why                       |
| ---------------------------- | ------- | ------------------------- |
| "Change button color to red" | task    | 1 file, 1 test, no state  |
| "Fix login error message"    | task    | 1-2 files, 1 test         |
| "Add dark mode toggle"       | feature | 3+ files, new state       |
| "Add user authentication"    | feature | Many files, state machine |

**Announcement (always):**

After detection, announce:

- patch: "Patch. Fixing directly."
- task: "Task. Writing tests first. `/bdd` to override."
- feature: "Feature. Defining behaviors first. `/tdd` to override."

### Step 2: Check/Create Artifacts

| Level       | Required Artifacts                                              | Test Location                   |
| ----------- | --------------------------------------------------------------- | ------------------------------- |
| **feature** | Feature Spec + Test Definitions (+ Design Doc if 3+ components) | `test-definitions/feature-*.md` |
| **task**    | Task Spec                                                       | Inline in spec                  |
| **patch**   | Task Spec (minimal)                                             | Existing tests                  |

**Locations:**

- Specs: `.safeword/planning/specs/`
- Test definitions: `.safeword/planning/test-definitions/`

**Templates:**

- feature: @./.safeword/templates/feature-spec-template.md
- task/patch: @./.safeword/templates/task-spec-template.md
- Test Definitions: @./.safeword/templates/test-definitions-feature.md

### Exit Criteria

- [ ] Level identified (patch/task/feature)
- [ ] Spec exists with "Out of Scope" defined
- [ ] feature: Test definitions file exists
- [ ] task: Test scenarios in spec
- [ ] patch: Existing test coverage confirmed

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

## Test List (once per slice)

Before starting RED/GREEN/REFACTOR, write the tests you expect for this slice.

| Source                                  | Action                                              |
| --------------------------------------- | --------------------------------------------------- |
| Test-definitions file exists (feature)? | Copy relevant tests from file                       |
| Test scenarios in spec (task)?          | Copy from spec                                      |
| Neither exists?                         | Write 3-7 tests: happy path, edge cases, error case |

---

## Micro-Design (if 2+ new files)

Sketch function signatures and data shapes. 10 lines max—more means you need a design doc first.

---

## Spike (if uncertain)

| Unknown?                         | Action                          |
| -------------------------------- | ------------------------------- |
| New library, unclear feasibility | 30-60 min spike, throwaway code |
| Familiar patterns                | Skip                            |

---

## Phase 1: RED

**Iron Law:** NO IMPLEMENTATION UNTIL TEST FAILS FOR THE RIGHT REASON

**Protocol:**

1. Pick ONE test from spec (task) or test definitions (feature)
2. Write test code
3. Run test
4. Verify: fails because behavior missing (not syntax error)
5. Commit: `test: [behavior]`

**For patch:** No new test needed. Confirm existing tests pass, then proceed to Phase 2.

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
Run: bun run test                   "Tests should pass now"
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

**Purpose:** Improve code structure while keeping behavior identical.

**Iron Law:** TESTS MUST PASS BEFORE AND AFTER EVERY CHANGE

### When to Refactor

| Smell                     | Action                            |
| ------------------------- | --------------------------------- |
| Duplication introduced    | Extract shared function/constant  |
| Unclear name              | Rename to reveal intent           |
| Long function (>20 lines) | Extract helper                    |
| Magic number/string       | Extract constant                  |
| Complex conditional       | Extract to named function         |
| No obvious improvements   | Skip refactor, proceed to Phase 4 |

### Protocol

1. **Verify GREEN:** Run tests → must pass
2. **Pick ONE refactoring** from table above
3. **Make the change**
4. **Verify still GREEN:** Run tests → must pass
5. **Commit:** `refactor: [what improved]`
6. **Repeat** if more smells exist

### Exit Criteria

- [ ] Tests pass before AND after each change
- [ ] Code cleaner (or no changes needed)
- [ ] Each refactoring committed separately

### NOT Allowed

| Don't                       | Why                              |
| --------------------------- | -------------------------------- |
| Add new behavior            | That's Phase 1 (new test needed) |
| Change test assertions      | You're changing the spec         |
| Add "just in case" code     | YAGNI                            |
| Batch multiple refactorings | One change → test → commit       |
| Skip verification           | "Should still work" isn't proof  |

### Revert Protocol

If tests fail after refactoring:

```bash
git checkout -- <changed-files>
```

Then: Try a smaller refactoring, or skip and move to Phase 4.

---

## Phase 4: ITERATE

```text
More tests in spec/test-definitions?
├─ Yes → Return to Phase 1
└─ No → All "Done When" / AC checked?
        ├─ Yes → Complete
        └─ No → Update spec, return to Phase 0
```

For feature: Update test definition status (✅/⏭️/❌/🔴) as tests pass.

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

**feature** ("Add VIP discount"):
Phase 0: feature → create spec + test defs → Phase 1: write test → FAIL → commit → Phase 2: implement → PASS → commit → Phase 3: clean up → Phase 4: more tests? → repeat

**task** ("Fix login timeout"):
Phase 0: task → create task spec → Phase 1: write failing test → commit → Phase 2: fix → PASS → commit → Phase 3: clean up if needed → Phase 4: done

**patch** ("Fix typo"):
Phase 0: patch → create minimal spec → Phase 1: no new test (existing tests cover) → Phase 2: fix typo → tests PASS → commit → done

**Why patch needs a spec:** "Fix typo" can become "refactor error handling" without explicit "Out of Scope".

---

## Integration

| Scenario                | Handoff             |
| ----------------------- | ------------------- |
| Test fails unexpectedly | → debugging skill   |
| Review needed           | → quality-reviewing |
| Scope expanding         | → Update spec first |

---

## Related

- @./.safeword/guides/planning-guide.md
- @./.safeword/guides/testing-guide.md
