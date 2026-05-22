---
name: building
description: "Execute whiteboard plans through gated phases with subagent dispatch. Require feature branch. Each phase goes through DISCOVERY -> PRE-GATE (pseudocode) -> IMPLEMENT -> POST-GATE (reviewer) -> CHECKPOINT. Produce per-phase commits, execution log, and working code with tests. Use after /code-foundations:whiteboarding to implement saved plans. Triggers on: build it, execute plan, implement the whiteboard, run the plan."
---

# Skill: building

**Load Plan → Checklist → Execute → Verify → Report**

---

## Quick Reference

| Phase | Goal | Output |
|-------|------|--------|
| LOAD | Read plan file | Parsed implementation checklist |
| SETUP | Initialize tracking | TodoWrite populated |
| EXECUTE | Implement each section | Working code |
| VERIFY | Run tests, confirm completion | All tests pass |
| REPORT | Update plan, summarize | Execution log |

---

## Crisis Invariants - NEVER SKIP

| Check | Why Non-Negotiable |
|-------|-------------------|
| **Feature branch required** | Multi-phase commits on main = no rollback, polluted history |
| **Load plan before coding** | No plan = no checklist = forgotten tasks |
| **One section at a time** | Parallel sections = merge conflicts + lost context |
| **PRE-GATE before implementation** | No pseudocode = coding without design = rework |
| **POST-GATE before checkpoint** | No verification = bugs escape to next phase |
| **Reviewer agent per phase** | Self-review is blind; fresh agent catches issues |
| **Mark complete only when gates pass** | Premature completion = unverified work shipped |
| **Update execution log** | Log enables debugging failed builds |

---

## Phase 1: LOAD (Read Plan File)

### Branch Gate (MANDATORY - First Check)

**Before anything else, verify branch status:**

```bash
git branch --show-current
git status
```

| Current Branch | Action |
|----------------|--------|
| `main` or `master` | **STOP.** Create feature branch first. |
| Feature branch, clean | Proceed |
| Feature branch, dirty | Ask: "Uncommitted changes. Stash, commit, or abort?" |

**If on main/master:**
```
You're on [main]. Building requires a feature branch for safe multi-phase commits.

Create branch now?
- [ ] Yes, create: feature/<plan-topic>
- [ ] Yes, create: <custom-name>
- [ ] No, abort building
```

```bash
git checkout -b feature/<plan-topic>
```

**This gate is NON-NEGOTIABLE.** Do not proceed on main/master under any circumstances.

---

### Locate Plan

If plan path provided:
```bash
cat docs/plans/<provided-path>.md
```

If no path, list available:
```bash
ls -la docs/plans/*.md | head -20
```

Ask user: "Which plan should I execute?"

### Parse Plan Structure

Extract from plan file:
1. **Context** - What we're building
2. **Approach** - How we're building it
3. **Phases** - Implementation sections
4. **Test Coverage** - What level of tests required (100%, backend only, etc.)
5. **Test Plan** - Specific verification criteria

**If Test Coverage is missing:** Default to "100% coverage" and inform user.

### Verify Plan is Ready

Check plan status:
- `Status: ready` → Proceed
- `Status: in-progress` → Resume from last checkpoint
- `Status: complete` → Ask: "Plan already complete. Re-execute or archive?"
- `Status: blocked` → Show blockers, ask how to proceed

---

## Phase 2: SETUP (Initialize Tracking)

### Convert Plan to TodoWrite

Transform each plan phase into todos:

```
Plan Phase 1: Database Schema
- [ ] Create migration file
- [ ] Define User table
- [ ] Define Session table

↓ Becomes ↓

TodoWrite([
  {content: "Create migration file", status: "pending", activeForm: "Creating migration file"},
  {content: "Define User table", status: "pending", activeForm: "Defining User table"},
  {content: "Define Session table", status: "pending", activeForm: "Defining Session table"}
])
```

### Update Plan Status

```markdown
**Status:** in-progress
**Started:** YYYY-MM-DD HH:MM
**Current Phase:** 1
```

---

## Phase 3: EXECUTE (Implement Sections)

### CRITICAL: DO NOT DO ANYTHING DIRECTLY

**You MUST dispatch subagents for ALL work. DO NOT:**
- Read/explore code files directly during building
- Edit code files directly during building
- Skip DISCOVERY subagent
- Skip PRE-GATE pseudocode
- Skip POST-GATE reviewer agent
- Proceed after reviewer returns FAIL

**The gates are BLOCKING, not advisory. All exploration and implementation is done by subagents.**

### Execution Loop - Gated

For each phase, execute this **mandatory** sequence:

```
┌──────────────────────────────────────────────────────────┐
│  DISCOVERY (via subagent - DO NOT explore directly)      │
│  ├─ Task tool → dispatch Explore subagent                │
│  ├─ Subagent reads files, understands current state      │
│  └─ Returns: findings, gaps, what exists vs plan         │
│                                                          │
│  ⛔ STOP: Cannot proceed until discovery complete        │
├──────────────────────────────────────────────────────────┤
│  PRE-GATE (BLOCKS IMPLEMENTATION)                        │
│  ├─ Skill(cc-pseudocode-programming) → pseudocode        │
│  ├─ Skill(aposd-designing-deep-modules) → design review  │
│  └─ CONFIRM: Pseudocode exists? Design passed?           │
│                                                          │
│  ⛔ STOP: Cannot proceed until PRE-GATE checklist TRUE   │
├──────────────────────────────────────────────────────────┤
│  IMPLEMENT (via subagent - DO NOT code directly)         │
│  ├─ Task tool → dispatch implementation subagent         │
│  ├─ Wait for subagent DONE                               │
│  └─ Run tests to verify                                  │
├──────────────────────────────────────────────────────────┤
│  POST-GATE (BLOCKS CHECKPOINT)                           │
│  ├─ Skill(aposd-verifying-correctness)                   │
│  ├─ Skill(cc-defensive-programming)                      │
│  ├─ Task tool → dispatch reviewer agent                  │
│  └─ Wait for PASS                                        │
│                                                          │
│  ⛔ STOP: Cannot proceed until reviewer returns PASS     │
├──────────────────────────────────────────────────────────┤
│  CHECKPOINT (Only after PASS)                            │
│  ├─ Commit with phase summary                            │
│  └─ Update execution log                                 │
└──────────────────────────────────────────────────────────┘
```

---

### DISCOVERY (MANDATORY - VIA SUBAGENT)

## STOP. YOU CANNOT EXPLORE CODE DIRECTLY.

**Dispatch an Explore subagent that writes findings to a file:**

```
Task tool:
- subagent_type: "Explore"
- description: "Discovery for Phase N"
- prompt: |
    Explore the codebase to understand what exists for Phase N.

    ## Phase N: [name]
    [paste phase description and file list from plan]

    ## Questions to Answer
    1. Do the files listed in the plan exist?
    2. What is the current implementation state?
    3. What already exists vs what needs to be built?
    4. Are there any gaps between plan assumptions and reality?

    ## OUTPUT REQUIREMENT
    Write your findings to: docs/building/<plan-name>-phase-N-discovery.md

    Use this format:
    ```markdown
    # Discovery: Phase N - [name]

    ## Files Found
    - [list existing files relevant to this phase]

    ## Current State
    [summary of what already exists]

    ## Gaps
    [differences between plan and reality]

    ## Recommendation
    [BUILD | SKIP | UPDATE_PLAN]
    [what actually needs to be done]
    ```

    Return only: "Discovery written to docs/building/<plan-name>-phase-N-discovery.md"
```

**Wait for Explore subagent to complete.**

**After discovery:**
1. Read the discovery file (quick scan, not full context load)
2. If SKIP recommended - mark phase complete, proceed to next
3. If UPDATE_PLAN recommended - pause and ask user
4. If BUILD recommended - proceed to PRE-GATE

---

### PRE-GATE (MANDATORY - VIA SUBAGENT)

## STOP. YOU CANNOT WRITE CODE UNTIL THIS GATE PASSES.

**Dispatch a PRE-GATE subagent that writes pseudocode to a file:**

```
Task tool:
- subagent_type: "general-purpose"
- description: "PRE-GATE for Phase N"
- prompt: |
    You are the PRE-GATE agent for Phase N.

    ## STOP - Load Skills First
    Before proceeding, load these skills using the Skill tool:
    - [ ] `cc-pseudocode-programming`
    - [ ] `aposd-designing-deep-modules`

    ## Inputs
    - Discovery file: docs/building/<plan-name>-phase-N-discovery.md
    - Plan file: docs/plans/<plan-name>.md
    - Phase: N - [name]

    ## Your Tasks
    1. Read the discovery file to understand current state
    2. Read the plan file to understand requirements for Phase N
    3. Use cc-pseudocode-programming to write pseudocode
    4. Use aposd-designing-deep-modules to review design (if new modules)

    ## OUTPUT REQUIREMENT
    Write your pseudocode to: docs/building/<plan-name>-phase-N-pseudocode.md

    Use this format:
    ```markdown
    # Pseudocode: Phase N - [name]

    ## Files to Create/Modify
    - [list from discovery + plan]

    ## Pseudocode

    ### [file1.ext]
    [pseudocode for file 1]

    ### [file2.ext]
    [pseudocode for file 2]

    ## Design Notes
    [any design decisions, interface choices, information hiding]

    ## PRE-GATE Status
    - [x] Pseudocode complete
    - [x] Design reviewed (if applicable)
    - [ ] Ready for implementation
    ```

    Return only: "PRE-GATE complete. Pseudocode written to docs/building/<plan-name>-phase-N-pseudocode.md"
```

**Wait for PRE-GATE subagent to complete.**

**After PRE-GATE:**
1. Verify the pseudocode file exists
2. Quick scan - does it cover all tasks in phase?
3. If incomplete, re-dispatch PRE-GATE agent
4. If complete, proceed to IMPLEMENT

---

### IMPLEMENT (ONLY AFTER PRE-GATE PASSES)

## STOP. Confirm PRE-GATE passed before proceeding.

**Dispatch implementation agent with file references** - DO NOT implement directly:

```
Task tool:
- subagent_type: "code-foundations:implementation-agent"
- description: "Implement Phase N"
- prompt: |
    Implement Phase N of the building plan.

    ## Input Files (READ THESE FIRST)
    - Discovery: docs/building/<plan-name>-phase-N-discovery.md
    - Pseudocode: docs/building/<plan-name>-phase-N-pseudocode.md
    - Plan: docs/plans/<plan-name>.md (Phase N section)

    ## Your Tasks
    1. Read the discovery file - understand current state
    2. Read the pseudocode file - this is your implementation spec
    3. Implement exactly what the pseudocode specifies
    4. Run tests after each file change

    Return: DONE with files changed, or BLOCKED with issue.
```

**Why file-based handoff:**
- Main context stays clean (no pseudocode bloat)
- Implementation agent has full context via files
- Artifacts are persistent and reviewable
- Enables resume if interrupted

**Wait for subagent to complete before proceeding.**

**After subagent returns:**

1. Verify subagent returned DONE (not BLOCKED)
2. Run tests to confirm implementation works
3. If BLOCKED, debug and re-dispatch or escalate

---

### POST-GATE (MANDATORY - VIA SUBAGENT)

## STOP. YOU CANNOT COMMIT UNTIL THIS GATE PASSES.

**Dispatch a reviewer agent with file references:**

Choose reviewer based on phase focus:

| Phase Focus | Use Agent |
|-------------|-----------|
| General implementation | `code-foundations:correctness-reviewer` |
| Error handling heavy | `code-foundations:defensive-reviewer` |
| Design/architecture | `code-foundations:quality-reviewer` |
| Performance critical | `code-foundations:performance-reviewer` |

```
Task tool:
- subagent_type: "code-foundations:correctness-reviewer"
- description: "POST-GATE for Phase N"
- prompt: |
    Review Phase N implementation.

    ## Input Files (READ THESE FIRST)
    - Discovery: docs/building/<plan-name>-phase-N-discovery.md
    - Pseudocode: docs/building/<plan-name>-phase-N-pseudocode.md
    - Plan: docs/plans/<plan-name>.md (Phase N section)

    ## Files Changed
    [list files from implementation subagent]

    ## Review Checklist
    1. Does implementation match pseudocode?
    2. Are all requirements from plan covered?
    3. Any deviations from spec?
    4. **Test coverage matches plan level** (check Test Coverage field in plan)
    5. Run your skill checklists (loaded via Skill tool)

    ## OUTPUT REQUIREMENT
    Write your review to: docs/building/<plan-name>-phase-N-review.md

    Use this format:
    ```markdown
    # Review: Phase N - [name]

    ## Verdict: PASS | FAIL

    ## Checklist
    - [x] Implementation matches pseudocode
    - [x] Requirements covered
    - [x] Defensive programming applied
    - [x] Correctness verified

    ## Issues (if FAIL)
    1. [issue description]
       - File: [path:line]
       - Fix: [what to do]

    ## Notes
    [any observations]
    ```

    Return: "POST-GATE [PASS|FAIL]. Review written to docs/building/<plan-name>-phase-N-review.md"
```

**Wait for reviewer agent response.**

**After POST-GATE:**
1. Read the review file
2. If PASS - proceed to CHECKPOINT
3. If FAIL - fix issues and re-run POST-GATE

**You CANNOT proceed to CHECKPOINT until reviewer returns PASS.**

---

### CHECKPOINT (Only After Gates Pass)

```bash
git add .
git commit -m "Phase N: [name]

- [summary of what was implemented]
- PRE-GATE: pseudocode reviewed
- POST-GATE: verification passed, reviewer approved"
```

Update plan file execution log:
```markdown
### Phase N: [Name]
- [x] PRE-GATE: Pseudocode complete
- [x] Task 1 - Completed
- [x] Task 2 - Completed
- [x] POST-GATE: Verification passed
- [x] POST-GATE: Reviewer approved
Commit: [hash]
```

**State:** "Phase N complete. All gates passed. Proceeding to Phase N+1."

---

### Gate Failure Protocol

If any gate fails:

| Gate | Failure | Action |
|------|---------|--------|
| PRE-GATE | Pseudocode unclear | Refine pseudocode, re-run gate |
| PRE-GATE | Design issues | Redesign, re-run gate |
| POST-GATE | Verification fails | Fix code, re-run POST-GATE |
| POST-GATE | Reviewer finds issues | Fix issues, re-run reviewer |

**You CANNOT proceed to next phase until current phase passes all gates.**

---

## Phase 4: VERIFY (Full Test Suite)

### Test Coverage Check

Read the **Test Coverage** field from the plan:

| Level | Verification |
|-------|--------------|
| **100%** | Unit tests for ALL new code + integration tests |
| **Backend only** | Server-side tests only, skip frontend |
| **Backend + frontend** | Tests for both layers |
| **None** | Skip test verification (warn: technical debt) |
| **Per-phase** | Check each phase's test notes |

**If coverage falls short:** FAIL verification, require tests before proceeding.

### Pre-Completion Checks

- [ ] All plan phases marked complete
- [ ] **Test coverage matches plan level**
- [ ] All tests pass (unit + integration as required)
- [ ] No skipped tasks
- [ ] Code compiles without warnings

### Run Test Plan

Execute each item from plan's Test Plan section:

```bash
# Unit tests
npm test  # or equivalent

# Integration tests (if specified)
npm run test:integration

# Manual verification (prompt user)
```

### Verification Gate

| Condition | Action |
|-----------|--------|
| All tests pass, coverage met | Proceed to REPORT |
| Tests fail | Debug, fix, re-verify |
| Tests missing (but required by coverage level) | Write tests, then re-verify |
| Coverage = None | Warn "Skipping tests per plan. Technical debt noted." and proceed |

---

## Phase 5: REPORT (Update Plan + Summarize)

### Update Plan File

```markdown
**Status:** complete
**Completed:** YYYY-MM-DD HH:MM
**Duration:** [time from start to complete]

---

## Execution Log

### Phase 1: [Name]
- [x] Task 1 - Completed YYYY-MM-DD HH:MM
- [x] Task 2 - Completed YYYY-MM-DD HH:MM
Commit: [hash]
Notes: [any issues encountered]

### Phase 2: [Name]
...
```

### Summary Output

```markdown
# Build Complete

**Plan:** [plan name]
**Phases Completed:** N/N
**Tests:** All passing

## What Was Built
- [summary of implemented features]

## Files Changed
- `path/to/file.ts` - [what changed]
- ...

## Commits
- [hash] Phase 1: [name]
- [hash] Phase 2: [name]
- ...

## Next Steps
- [any follow-up tasks identified]
- [documentation to update]
```

---

## Error Handling

### Build Failure Protocol

If implementation fails:

1. **Stop immediately** - Don't proceed to next task
2. **Document failure** in execution log:
   ```markdown
   ### Phase N: [Name]
   - [x] Task 1 - Complete
   - [ ] Task 2 - **FAILED**
     Error: [description]
     Attempted: [what was tried]
   ```
3. **Update plan status:** `Status: blocked`
4. **Ask user:**
   - "Task failed. Options: (A) Debug now, (B) Skip and continue, (C) Pause build"

### Resume Protocol

When resuming blocked plan:

1. Read execution log
2. Find last successful checkpoint
3. Show: "Resuming from Phase N, Task M. Last failure: [description]"
4. Ask: "Ready to retry, or should we discuss the blocker first?"

---

## Anti-Rationalization Table

| Rationalization | Reality |
|-----------------|---------|
| "I'll mark it complete and fix later" | Incomplete = incomplete. Fix now or don't mark done. |
| "Tests are slow, skip for now" | Untested code = unknown bugs shipped |
| "This task is done enough" | Either done or not done. No partial credit. |
| "I'll commit all phases at once" | Per-phase commits enable rollback |
| "The plan is outdated, I'll improvise" | Update the plan, don't abandon it |
| "User said ship it, skip verification" | Broken code shipped = worse than delay |
| "I remember what the plan said" | Read the plan file. Memory is unreliable. |
| "This extra feature fits naturally" | Not in plan = not in this build. Add to backlog. |
| "PRE-GATE is overkill for simple code" | Simple code has highest error rates. PRE-GATE catches design issues before they're coded. |
| "I can review my own code" | Self-review is blind to your own assumptions. Dispatch reviewer agent. |
| "POST-GATE is slowing me down" | POST-GATE catches issues BEFORE they propagate. Fix now = faster than fix later. |
| "Reviewer agent is redundant" | You implemented the code; reviewer agent has fresh perspective. Different context = different bugs caught. |
| "Gates passed last phase, skip this one" | Each phase is independent. Past gates don't predict current quality. |
| "I'll just commit to main, it's faster" | Multi-phase builds on main = no rollback. Feature branch is mandatory. |
| "It's a small change, main is fine" | Small changes grow. Branch now or regret later. |
| "I can implement faster than dispatching" | Direct implementation skips quality gates. Subagent ensures fresh context. |
| "Pseudocode is overkill, I know what to do" | You know NOW. The subagent doesn't. Pseudocode is the contract. |
| "The subagent will figure it out" | Subagent needs explicit pseudocode. No pseudocode = garbage implementation. |
| "I'll just quickly read the files myself" | Direct exploration pollutes your context. Discovery subagent returns only what's relevant. |
| "Discovery is overkill for a simple phase" | Plan assumptions often mismatch reality. Discovery catches this before wasted work. |
| "I already know this codebase" | Your context is stale. Discovery subagent has fresh eyes and finds what changed. |
| "I'll tell the subagent to invoke a skill" | Subagents can't invoke skills (fresh context). Use specialized agent types instead. |
| "general-purpose is fine for review" | Specialized reviewer agents have skills built-in. Use `code-foundations:*-reviewer`. |

---

## Pressure Testing Scenarios

### Scenario 1: Plan and Reality Diverge

**Situation:** During implementation, you discover the plan is wrong or incomplete.

**Response:**
1. Stop current task
2. Update plan file with discovery
3. Ask user: "Plan says X, but I found Y. Should I: (A) Update plan and continue, (B) Continue with current plan, (C) Pause for re-planning?"

### Scenario 2: Tests Fail After Implementation

**Situation:** Code is written, but tests fail.

**Response:**
1. Do NOT mark phase complete
2. Debug test failure
3. Fix code (not tests, unless tests are wrong)
4. Re-run tests
5. Only proceed when tests pass

### Scenario 3: Scope Creep

**Situation:** You see an opportunity to add a "quick improvement" not in the plan.

**Response:** "I noticed [opportunity]. This isn't in the current plan. Should I:
- Add to this plan (extends timeline)
- Add to backlog (future work)
- Skip entirely"

---

## Integration with /code-foundations:whiteboarding

### Expected Flow

```
/code-foundations:whiteboarding "user story"
  ↓
[Socratic questions]
[2-3 approaches]
[Detailed sections]
[Save to docs/plans/YYYY-MM-DD-topic.md]
  ↓
[Optional: Refresh context window]
  ↓
/code-foundations:building docs/plans/YYYY-MM-DD-topic.md
  ↓
[Checklist execution]
[Tests pass]
[Summary report]
```

### Context Refresh Benefits

Starting fresh session before /code-foundations:building:
- Full context window for implementation
- No planning discussion cluttering context
- Plan file contains all necessary information

---

## Chaining

- **RECEIVES FROM:** whiteboarding (via plan file), user with plan path
- **CHAINS TO:** code-foundations skills during execution
- **RELATED:** oberexec, aposd-verifying-correctness, cc-quality-practices
