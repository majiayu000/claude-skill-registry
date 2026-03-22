---
name: enterprise-build
description: "Strict TDD implementation following the contract. Write test first, watch it fail, write minimal code to pass. No production code without a failing test. Interleave RED→GREEN cycles — one test, one piece of code, repeat. Supports Solo, Subagent, and Swarm execution modes."
---

# Enterprise Build

You are implementing code from a contract. Every postcondition becomes a test. Every test is written BEFORE the code it tests. This is non-negotiable.

---

## THE IRON LAW

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.** Not "keep as reference." Not "adapt it." Delete.

---

## ARTIFACT VALIDATION (Before Starting)

Before writing ANY code, verify upstream artifacts exist:

```bash
# 1. Contract must exist and be LOCKED
CONTRACT=$(ls docs/contracts/*contract* 2>/dev/null | head -1)
if [ -z "$CONTRACT" ]; then
  echo "BLOCKED: No contract found. Run /enterprise-contract first."
  exit 1
fi
grep -q "LOCKED" "$CONTRACT" || echo "BLOCKED: Contract exists but is not LOCKED."

# 2. Plan must exist
PLAN=$(ls docs/plans/*plan* 2>/dev/null | head -1)
if [ -z "$PLAN" ]; then
  echo "BLOCKED: No plan found. Run /enterprise-plan first."
  exit 1
fi
```

**If either check fails: STOP.** Do not write code without a locked contract.

---

## STACK RESOLUTION

Read `.claude/enterprise-state/stack-profile.json` at skill start. Extract:
- `$TEST_CMD` = `commands.test_all`
- `$TEST_SINGLE` = `commands.test_single`
- `$TEST_FRAMEWORK` = `commands.test_framework`
- `$SOURCE_DIR` = `structure.source_dirs.backend`
- `$TENANT_FIELD` = `multi_tenancy.field`
- `$TENANT_ENABLED` = `multi_tenancy.enabled`

If no profile exists: BLOCKED — run /enterprise-discover first.

---

## GREENFIELD BOOTSTRAP (First Test Ever)

If the codebase has NO existing tests for the module you're building:

1. **Check test infrastructure**:
   ```bash
   $TEST_FRAMEWORK --version 2>/dev/null || echo "Test framework not installed"
   ls jest.config* 2>/dev/null || echo "No jest config found"
   ```

2. **If missing, create minimal test setup**:
   ```javascript
   // Verify test infrastructure works before TDD
   test('test infrastructure works', () => {
     expect(1 + 1).toBe(2);
   });
   ```

3. **Run it**: `$TEST_SINGLE` with pattern "infrastructure"
4. **Only after it passes**: proceed with normal TDD sequence

This prevents wasting a RED→GREEN cycle on "Jest isn't configured" instead of "feature is missing."

---

## CONTEXT PRESERVATION (Before Starting)

Before writing any code:

1. **Save session state** (use whichever memory backend is available — Memora MCP, Muninn MCP, or filesystem fallback to `docs/handovers/`):
   ```
   MEMORY: save task context — TDD: [slug], contract: [path], current PC: PC-1
   ```
2. **Verify the save** if using an MCP backend — recall to confirm persistence
3. **Read contract postconditions** — these are your task list
4. **Read the plan** — this tells you the order and exact code
5. **Check memory for prior context** if resuming after context loss

---

## EXECUTION MODES

### Solo Mode (Single Agent)

Execute the TDD sequence yourself. Self-review acceptable for Micro/Small tier.

### Subagent Mode (Fresh Agent Per Task)

For each task in the plan:

**1. Spawn implementer agent** with this exact handoff:
```
TASK: [task title from plan]
TIER: [micro/small/medium/large]
POSTCONDITIONS: [list PC-X entries this task must satisfy]
CONTRACT (full text):
  [paste the full contract — NOT a file path. Agents can't read paths from other worktrees]
FILES TO CHANGE:
  [exact file paths from the plan]
TEST PATTERNS:
  [paste 1-2 existing test examples from the codebase so the agent matches style]
TDD SEQUENCE:
  Write test → Run RED → Write code → Run GREEN → Commit
  No production code without a failing test first.
CODEBASE CONTEXT:
  [key imports, function signatures, data shapes the agent will need]
```

**2. Implementer returns code + tests**

**3. Spawn spec-reviewer agent:**
```
REVIEW TYPE: Spec Compliance
CONTRACT: [paste full contract]
CHANGED FILES: [list from implementer]
CHECK: For each PC-X, does a test exist that verifies the EXACT postcondition?
  - Is the assertion testing the right thing (not just that code runs)?
  - Does the test name reference the PC number?
  - Would the test FAIL if the postcondition were violated?
VERDICT: SPEC PASS or SPEC FAIL with specific failures
```
Loop until spec reviewer returns SPEC PASS.

**4. Spawn quality-reviewer agent:**
```
REVIEW TYPE: Code Quality
CHANGED FILES: [list from implementer]
CHECK:
  - File sizes (<400 lines)
  - Tenant isolation (if $TENANT_ENABLED: every query has $TENANT_FIELD)
  - Parameterized queries (no string concatenation)
  - Import resolution (every import exists)
  - No debug artifacts (console.log, TODO, etc.)
  - Security (auth middleware, input validation)
  - Pattern compliance (follows existing codebase patterns)
VERDICT: QUALITY PASS or QUALITY FAIL with specific failures
```
Loop until quality reviewer returns QUALITY PASS.

**5. Move to next task**

**Critical:** Spec compliance BEFORE code quality. Wrong order = failure.

### Swarm Mode (Persistent Teammates)

For Large tier with independent workstreams:
1. Create team with named roles (e.g., "api-builder", "frontend-builder", "test-writer")
2. Create shared task list from plan with dependency markers
3. Teammates claim tasks from queue, execute TDD sequence
4. Dependency blocking: task B waits until task A completes
5. Integration checkpoint after all parallel streams complete

---

## THE TDD SEQUENCE (Per Postcondition)

This is mechanical. Follow exactly.

### Step 1: WRITE the test

One test. One behavior. One postcondition.

```javascript
test('PC-1: clicking customer opens CustomerDetailModal', () => {
  // Arrange: set up the scenario
  // Act: perform the action
  // Assert: verify the postcondition
});
```

Save the test file.

### Step 2: RUN the test — show RED

```bash
$TEST_SINGLE --testPathPattern="<pattern>" 2>&1 | tail -20
```

**You MUST see the test FAIL.** Paste the failure output.

If the test PASSES → you wrote a useless test. Delete it. Write one that tests something missing.
If the test ERRORS (syntax, import) → fix the test until it fails for the RIGHT reason (missing feature, not missing import).

### Step 3: WRITE minimal production code

Make the test pass. Nothing more. No "while I'm here" additions.

**Before writing:**
- Verify every import exists (read the file)
- Verify every function signature matches
- Verify data shapes match the contract's consumer map

### Step 4: RUN the test — show GREEN

```bash
$TEST_SINGLE --testPathPattern="<pattern>" 2>&1 | tail -20
```

**You MUST see the test PASS.** Paste the pass output.

If it FAILS → fix the production code (not the test).

### Step 5: REFACTOR (if needed)

Improve code quality without changing behavior. Run tests again — still green.

### Step 6: COMMIT

```bash
git add -A && git commit -m "feat: [what this unit does]"
```

### Step 7: SAVE PROGRESS (memory + JSON)

Save progress to both memory and the JSON postcondition registry:

```
MEMORY: save task progress — [slug] PC-[N] complete, [N] remaining
```

Update the postcondition registry JSON to mark this PC as passing:
```bash
node -e "
  const fs = require('fs');
  const f = '.claude/enterprise-state/<slug>-postconditions.json';
  const r = JSON.parse(fs.readFileSync(f));
  const pc = r.postconditions.find(p => p.id === 'PC-<N>');
  if (pc) { pc.passes = true; pc.last_verified = new Date().toISOString(); }
  fs.writeFileSync(f, JSON.stringify(r, null, 2));
"
```

**Only set `passes: true` AFTER the test runner output confirms the test passed.** Do not set it based on belief or expectation — evidence only.

Also update the pipeline state at BUILD start and completion:
```bash
# At BUILD start:
node -e "
  const fs = require('fs');
  const f = '.claude/enterprise-state/<slug>.json';
  const s = JSON.parse(fs.readFileSync(f));
  s.stages.build.status = 'in_progress';
  s.stages.build.started_at = new Date().toISOString();
  fs.writeFileSync(f, JSON.stringify(s, null, 2));
"

# At BUILD completion (all PCs green):
node -e "
  const fs = require('fs');
  const f = '.claude/enterprise-state/<slug>.json';
  const s = JSON.parse(fs.readFileSync(f));
  s.stages.build.status = 'complete';
  s.stages.build.completed_at = new Date().toISOString();
  fs.writeFileSync(f, JSON.stringify(s, null, 2));
"
```

### Step 8: REPEAT for next postcondition

---

## IMPLEMENTATION ORDER

1. **Migration first** (if needed) — `IF NOT EXISTS`, `TIMESTAMPTZ`, `$TENANT_FIELD` (if `$TENANT_ENABLED`)
2. **Backend tests + code** — service layer, then routes
3. **Frontend tests + code** — hooks, then components
4. **Integration checkpoint** — everything wires together

Do NOT write all tests first then all code. Interleave: RED → GREEN → RED → GREEN.

### Frontend Testing Guidance

For React/frontend TDD patterns, read `references/frontend-testing.md`. It covers:
- Component testing with React Testing Library (render, interact, assert)
- Hook testing with `renderHook`
- E2E testing with Playwright
- What NOT to test (don't test library internals or CSS)
- Frontend-specific RED→GREEN cycle examples
- Common gotchas (act() warnings, async updates, mock boundaries)

---

## BUILD RULES

- **Read before import** — verify every function exists, signature matches, return type is right
- **Scope lock** — implement ONLY what the contract specifies
- **No god files** — 400 line soft limit. Approaching it? Extract first.
- **Existing patterns** — use what the codebase already uses
- **Permission checks** — every new write endpoint needs auth + permission scoping
- **Multi-tenant** — if `$TENANT_ENABLED`: every INSERT needs `$TENANT_FIELD`, every query scopes to tenant
- **Verify every consumer** — after changing a data source, read every file that consumes it

---

## RATIONALIZATIONS THAT MEAN STOP

| Thought | Reality |
|---------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "I already know the fix" | Prove it by writing the test first. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test is hard to write" | Hard to test = hard to use. Fix the design. |
| "TDD slows me down" | TDD is faster than debugging. Every time. |
| "Just this once" | There is no "just this once." |

---

## BUG FIX TDD SEQUENCE

For bugs, the sequence proves three things: bug existed, test catches it, fix resolves it.

1. Write test that **reproduces the bug** (assert the WRONG behavior)
2. Run it — watch it PASS (proving the bug exists)
3. Invert the assertion to **correct behavior**
4. Run it — watch it FAIL (proving the fix isn't applied yet)
5. Write the fix
6. Run it — watch it PASS (proving the fix works)

---

## CONTEXT LOSS RECOVERY

If context is lost mid-build:

1. **Check JSON state first**: `cat .claude/enterprise-state/<slug>-postconditions.json` — shows exactly which PCs pass and which are still pending
2. **Check pipeline state**: `cat .claude/enterprise-state/<slug>.json` — confirms you're in BUILD stage
3. **Check memory** for semantic context about decisions made
4. **Read the contract** — postconditions are the task list
5. **Run existing tests** — verify the JSON state matches reality
6. **Resume from first PC where `"passes": false`**
7. **Save progress after each PC** to both memory and JSON

The JSON postcondition registry is the authoritative state. A new agent reads it and knows exactly where to resume.
