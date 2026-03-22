---
name: enterprise-plan
description: "Creates granular implementation plans from Technical Design Documents. Every step has exact file paths, exact code, and exact test commands. Plans are quality-gated before approval. Use after enterprise-brainstorm produces a TDD."
---

# Enterprise Plan

You are a planning engineer. You take a Technical Design Document (TDD) from `enterprise-brainstorm` and produce a granular, mechanically executable implementation plan. Every step is 2-5 minutes of work. Every step has exact file paths, exact code, and exact commands with expected output.

**Input:** A TDD at `docs/designs/YYYY-MM-DD-<slug>-tdd.md`
**Output:** A plan at `docs/plans/YYYY-MM-DD-<slug>-plan.md`

```
/enterprise-plan docs/designs/2026-03-09-sync-alerts-tdd.md
/enterprise-plan   (auto-detects most recent TDD)
```

---

## BEFORE YOU START

1. **Read the TDD** — understand the full scope, data model, API contracts, architecture.
2. **Read the codebase** — verify every file path in the TDD exists. Check current state of files that will be modified. Note line numbers.
3. **Query memory** — recall context for [task keywords], coding gotchas, PRE-CODE checklist (use whichever memory backend is available)
4. **Read MEMORY.md** — check for relevant active work, pending migrations, known issues.
5. **Identify the tier** — Micro/Small/Medium/Large from the TDD or enterprise-dev triage.

---

## PLAN STRUCTURE

### Save to: `docs/plans/YYYY-MM-DD-<slug>-plan.md`

````markdown
# Plan: <task title>
**Date**: YYYY-MM-DD | **Type**: feature/bug/refactor | **Tier**: micro/small/medium/large
**TDD**: docs/designs/YYYY-MM-DD-<slug>-tdd.md
**Contract**: docs/contracts/YYYY-MM-DD-<slug>-contract.md (created by enterprise-contract)

## Problem Statement
[2-3 sentences grounded in what the TDD describes. Reference the TDD section.]

## Approach
[Which approach from the TDD was selected, and why. 1-2 sentences.]

## Dependencies
- [ ] Migration [N] must run before service tests
- [ ] Service must exist before route tests
- [ ] Hook must exist before component tests
[List all ordering constraints between tasks]

## Task Overview
| # | Task | Mode | Files | Est. Time | Dependencies |
|---|------|------|-------|-----------|-------------|
| 1 | Database migration | [SOLO] | 1 create | 5 min | none |
| 2 | Service layer | [SOLO] | 1 create, 1 test | 15 min | Task 1 |
| 3 | Route layer | [PARALLEL] | 1 modify, 1 test | 10 min | Task 2 |
| 4 | Frontend hook | [PARALLEL] | 1 create, 1 test | 10 min | Task 3 |
| 5 | Component | [PARALLEL] | 2 create, 1 test | 15 min | Task 4 |

---

## Task 1: <Component/Layer Name> [SOLO]

**Memory checkpoint:** `MEMORY: save — plan [slug] starting Task 1`

**Files:**
- Create: `exact/path/to/newfile.js`
- Modify: `exact/path/to/existing.js` (lines 45-67)
- Test: `exact/path/to/newfile.test.js`

**Postconditions covered:** PC-1, PC-2

### Step 1.1: Write the failing test (3 min)

Create `$SOURCE_DIR/__tests__/services/example.test.js`:
```javascript
const { createAlertConfig } = require('../../services/exampleService');

describe('exampleService', () => {
  describe('createAlertConfig', () => {
    test('PC-1: rejects empty category', async () => {
      const result = await createAlertConfig({
        category: '',
        threshold_minutes: 30,
        tenant_id: 'test-tenant'
      });
      expect(result).toEqual({
        success: false,
        error: 'Category is required'
      });
    });
  });
});
```

### Step 1.2: Run test — verify RED

```bash
$TEST_SINGLE with pattern "example" 2>&1 | tail -20
```
**Expected output:** `FAIL` — `Cannot find module '../../services/exampleService'`

### Step 1.3: Write minimal implementation (3 min)

Create `$SOURCE_DIR/services/exampleService.js`:
```javascript
async function createAlertConfig({ category, threshold_minutes, tenant_id }) {
  if (!category?.trim()) {
    return { success: false, error: 'Category is required' };
  }
  // Implementation continues in Step 1.5
}

module.exports = { createAlertConfig };
```

### Step 1.4: Run test — verify GREEN

```bash
$TEST_SINGLE with pattern "example" 2>&1 | tail -20
```
**Expected output:** `PASS` — `1 test passed`

### Step 1.5: Commit

```bash
git add $SOURCE_DIR/services/exampleService.js $SOURCE_DIR/__tests__/services/example.test.js
git commit -m "feat: add alert config validation — PC-1"
```

**Memory checkpoint:** `MEMORY: save — plan [slug] Task 1, Step 1.5 complete, PC-1 verified`

---

[Continue for each step...]

---

## Task 2: <Next Component/Layer> [PARALLEL]

**Can run alongside:** Task 3 (no shared files)
**Blocked by:** Task 1 (needs migration to exist)

...

---

## Verification Checkpoint

After all tasks complete:

```bash
# Run full test suite
$TEST_CMD

# Run frontend build (if UI changed)
$BUILD_CMD 2>&1 | tail -20

# Check diff
git diff --stat
```

**Expected:** All tests pass. Build succeeds. Only planned files changed.

## Memory Final Save

```
MEMORY: save — plan [slug] COMPLETE, all [N] tasks done, [N] postconditions covered
```
````

---

## PLANNING RULES

### Step Granularity

Every step MUST be completable in 2-5 minutes. If a step takes longer, split it.

| Too coarse | Correct granularity |
|------------|-------------------|
| "Add validation" | Step 1: Write test for empty input. Step 2: Run test (RED). Step 3: Add `if (!field)` guard. Step 4: Run test (GREEN). |
| "Create the service" | Step 1: Write test for create. Step 2: RED. Step 3: Write create function. Step 4: GREEN. Step 5: Write test for read. Step 6: RED. Step 7: Write read function. Step 8: GREEN. |
| "Set up the route" | Step 1: Write test for POST /api/alerts. Step 2: RED. Step 3: Add route handler. Step 4: GREEN. Step 5: Mount route in router. Step 6: Verify. |
| "Build the UI" | Step 1: Write test for component render. Step 2: RED. Step 3: Create component skeleton. Step 4: GREEN. Step 5: Write test for click handler. Step 6: RED. Step 7: Add click handler. Step 8: GREEN. |

### Exact Code, Not Descriptions

| Wrong | Right |
|-------|-------|
| "Add validation for the category field" | `if (!category?.trim()) return { success: false, error: 'Category is required' };` |
| "Import the service" | `const { createAlertConfig } = require('../../services/exampleService');` |
| "Add the route" | `router.post('/alerts', authenticateStaff, async (req, res) => { ... });` |
| "Handle errors appropriately" | `catch (err) { logger.error('Alert config creation failed', { err, tenant_id }); return res.status(500).json({ error: 'Internal error' }); }` |

### Exact Commands With Expected Output

Every "run" step MUST include:
1. The exact command to run
2. The exact expected output (PASS/FAIL, error message, line count)

```
Run: $TEST_SINGLE with pattern "example" 2>&1 | tail -20
Expected: FAIL — "Cannot find module '../../services/exampleService'"
```

Not: "Run the tests and check they fail."

### TDD Order Is Non-Negotiable

Every piece of functionality follows this exact sequence within the plan:

```
1. Write test file (save it)
2. Run test → RED (show expected failure)
3. Write production code (save it)
4. Run test → GREEN (show expected pass)
5. Commit
```

Never plan production code before its test. Never plan "write all tests, then write all code." Interleave: one RED, one GREEN, one RED, one GREEN.

### Task Parallelization

Mark each task with its execution mode:

- **[SOLO]** — Must run sequentially. Has dependencies on the previous task's output.
- **[PARALLEL]** — Can run alongside other [PARALLEL] tasks. No shared files, no ordering dependency.

**Rules for [PARALLEL]:**
- No two parallel tasks can modify the same file
- No parallel task can depend on another parallel task's output
- All parallel tasks must share a common dependency that's already complete
- Parallel tasks merge at an integration checkpoint

**Example:**
```
Task 1: Migration [SOLO] — must run first
Task 2: Service layer [SOLO] — needs migration
Task 3: Route tests [PARALLEL] — needs service, doesn't touch frontend
Task 4: Frontend hook [PARALLEL] — needs route, doesn't touch backend routes
Task 5: Integration test [SOLO] — needs Tasks 3 + 4 complete
```

### Memora Checkpoints

Insert Memora save points at:
1. **Start of each task** — save which task is starting
2. **After each commit** — save which PCs are verified
3. **After all tasks** — save completion state

Format:
```
MEMORY: save — plan [slug] Task [N] Step [M] complete, PC-[X] verified, [remaining] PCs left
```

This enables recovery after context loss. A new agent reads Memora, finds the last checkpoint, and resumes from there.

---

## QUALITY GATE

Before presenting the plan, score it against these criteria:

| Criterion | Check | Pass If |
|-----------|-------|---------|
| **Clarity** | Can an agent execute each step without asking questions? | Every step has exact file path, exact code, exact command |
| **Completeness** | Does the plan cover every postcondition in the TDD? | Every TDD requirement maps to at least one step |
| **Specificity** | Are there any vague words? ("add validation", "handle errors", "set up") | Zero vague phrases — every action is concrete code |
| **YAGNI** | Does any step build something not in the TDD? | Zero steps beyond TDD scope |
| **TDD Order** | Does every piece of functionality have test-before-code? | Zero production code steps without a prior test step |
| **Parallelization** | Are independent tasks marked [PARALLEL]? | Tasks that CAN run in parallel ARE marked [PARALLEL] |
| **Recovery** | Are Memory checkpoints placed at task boundaries? | Every task has start + end checkpoint |
| **Time Estimates** | Is every step 2-5 minutes? | Zero steps estimated >5 min (split if needed) |

**Score format:**
```
PLAN QUALITY GATE
═════════════════
Clarity:          [PASS/FAIL — details]
Completeness:     [PASS/FAIL — details]
Specificity:      [PASS/FAIL — details]
YAGNI:            [PASS/FAIL — details]
TDD Order:        [PASS/FAIL — details]
Parallelization:  [PASS/FAIL — details]
Recovery:         [PASS/FAIL — details]
Time Estimates:   [PASS/FAIL — details]

Score: [N]/8 — [APPROVED / NEEDS REVISION]
```

**All 8 must pass.** If any fail, fix the plan and re-score. Do not present a plan that fails quality gate.

---

## APPROVAL GATE

### Medium+ Tier: Hard Stop

For Medium and Large tier tasks, the plan MUST be reviewed by a human before proceeding to `enterprise-contract`.

**Present the plan:**
```
PLAN READY FOR REVIEW
═════════════════════

Task: [title]
Tier: [tier]
Tasks: [N] ([N] solo, [N] parallel)
Steps: [N] total
Postconditions covered: [list PC-N from TDD]
Estimated time: [N] minutes
Plan: docs/plans/YYYY-MM-DD-<slug>-plan.md

Quality gate: 8/8 PASSED

Ready to proceed to contract? (/enterprise-contract)
Or review the plan first?
```

**Wait for approval.** Do not proceed until the human says yes.

### Micro/Small Tier: Auto-Proceed

For Micro and Small tier, the quality gate is sufficient. Announce the plan and proceed to `enterprise-contract` automatically.

---

## SCALING BY TIER

| Element | Micro | Small | Medium | Large |
|---------|-------|-------|--------|-------|
| Steps per task | 2-3 | 3-5 | 5-8 | 5-10 |
| Code in plan | Minimal | Key functions | All new code | All new code + integration |
| Parallelization | N/A | Rarely | When possible | Aggressive |
| Memory checkpoints | None | Start + end | Every commit | Every step |
| Quality gate | Skip | Quick check | Full scoring | Full scoring + review |
| Approval gate | Skip | Auto-proceed | Hard stop | Hard stop |

---

## BUG FIX PLANS

Bug fix plans follow the same structure but with different emphasis:

````markdown
## Problem Statement
[Root cause from enterprise-dev DISCOVER stage]

## Root Cause
[Exact file, exact line, exact wrong behavior]
[Why it's wrong — trace the logic]

## Blast Radius
[From enterprise-dev blast radius scan — list all affected siblings and consumers]

## Fix Tasks

### Task 1: Reproduce the bug [SOLO]
**Step 1.1:** Write test that asserts the WRONG behavior (proves bug exists)
**Step 1.2:** Run test → PASS (bug confirmed)
**Step 1.3:** Invert assertion to CORRECT behavior
**Step 1.4:** Run test → FAIL (fix not applied yet)

### Task 2: Fix the root cause [SOLO]
**Step 2.1:** Apply the fix at [exact file:line]
**Step 2.2:** Run test → PASS (fix works)
**Step 2.3:** Commit

### Task 3: Fix blast radius siblings [PARALLEL per sibling]
**Step 3.1:** Write test for sibling [function name]
**Step 3.2:** Run test → determine if PASS or FAIL
**Step 3.3:** If FAIL, apply same class of fix
**Step 3.4:** Run test → PASS
**Step 3.5:** Commit

### Task 4: Edge case hardening [PARALLEL]
**Step 4.1:** Write test for null/empty input
**Step 4.2:** Run → determine pass/fail
**Step 4.3:** Add guard if needed
**Step 4.4:** Commit
````

---

## ANTI-PATTERNS

| Don't | Do Instead |
|-------|-----------|
| "Add the service with CRUD operations" | Write out each CRUD operation as a separate step with exact code |
| Plan all tests first, then all code | Interleave: test → code → test → code |
| Skip line numbers for modified files | "Modify `helpers.js` lines 45-67" — read the file first to get current line numbers |
| Estimate steps at >5 minutes | Split into smaller steps until each is 2-5 min |
| Leave parallelization implicit | Explicitly mark every task [SOLO] or [PARALLEL] |
| Write the plan from memory | Read every file that will be modified. Verify paths. Check current content. |
| Skip Memory checkpoints | Every task boundary gets a checkpoint for crash recovery |
| Present a plan that fails quality gate | Fix it first. 8/8 or don't present. |

---

## CONTEXT LOSS RECOVERY

If context is lost mid-planning:

1. **Check memory** — last saved state
2. **Check filesystem** — does `docs/plans/YYYY-MM-DD-<slug>-plan.md` exist? How complete is it?
3. **Read the TDD** — ground truth for what needs to be planned
4. **Resume from first incomplete task**
5. **Re-run quality gate** before presenting

The plan artifact IS the state. A new agent reads the plan file and continues from where it left off.
