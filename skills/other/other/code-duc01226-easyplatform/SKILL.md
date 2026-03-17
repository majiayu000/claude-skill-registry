---
name: code
version: 1.0.0
description: '[Implementation] Start coding & testing an existing plan'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

## Quick Summary

**Goal:** Execute an existing implementation plan phase-by-phase with testing, code review, and user approval gates.

**Workflow:**

1. **Plan Detection** — Find latest plan or use provided path, select next incomplete phase
2. **Analysis & Tasks** — Extract tasks from phase file into TaskCreate
3. **Implementation** — Implement step-by-step, run type checks
4. **Testing** — Call tester subagent; must reach 100% pass before proceeding
5. **Code Review** — Call code-reviewer subagent; must reach 0 critical issues
6. **User Approval** — BLOCKING gate: wait for explicit user approval
7. **Finalize** — Update status, docs, and auto-commit

**Key Rules:**

- Tests must be 100% passing (Step 3 gate)
- Critical issues must be 0 (Step 4 gate)
- User must explicitly approve before finalize (Step 5 gate)
- One plan phase per command run

**MUST READ** `CLAUDE.md` then **THINK HARDER** to start working on the following plan:
<plan>$ARGUMENTS</plan>

---

## Step 0: Plan Detection & Phase Selection

**If `$ARGUMENTS` is empty:**

1. Find latest `plan.md` in `./plans`
2. Parse plan for phases and status, auto-select next incomplete (prefer IN_PROGRESS or earliest Planned)

**If `$ARGUMENTS` provided:** Use that plan and detect which phase to work on.

**Output:** `✓ Step 0: [Plan Name] - [Phase Name]`

---

## Workflow Sequence

**Rules:** Follow steps 1-6 in order. Each step requires output marker `✓ Step N:`. Mark each complete in TaskCreate before proceeding. Do not skip steps.

---

## Step 1: Analysis & Task Extraction

Read plan file completely. Map dependencies. List ambiguities. Identify required skills and activate from catalog. If the plan references analysis files in `.ai/workspace/analysis/`, re-read them before implementation.

**TaskCreate Initialization:**

- Initialize TaskCreate with `Step 0: [Plan Name] - [Phase Name]` and all steps (1-6)
- Read phase file, look for tasks/steps/phases/sections/numbered/bulleted lists
- Convert to TaskCreate tasks with UNIQUE names:
    - Phase Implementation tasks → Step 2.X (Step 2.1, Step 2.2, etc.)
    - Phase Testing tasks → Step 3.X
    - Phase Code Review tasks → Step 4.X

**Output:** `✓ Step 1: Found [N] tasks across [M] phases - Ambiguities: [list or "none"]`

---

## Step 2: Implementation

Implement selected plan phase step-by-step following extracted tasks. Mark tasks complete as done. For UI work, call `ui-ux-designer` subagent. Run type checking and compile to verify.

**Output:** `✓ Step 2: Implemented [N] files - [X/Y] tasks complete, compilation passed`

---

## Step 3: Testing

Call `tester` subagent. If ANY tests fail: STOP, call `debugger` subagent, fix, re-run. Repeat until 100% pass.

**Testing standards:** Unit tests may use mocks. Integration tests use test environment. Forbidden: commenting out tests, changing assertions to pass, TODO/FIXME to defer fixes.

**Output:** `✓ Step 3: Tests [X/X passed] - All requirements met`

**Validation:** If X ≠ total, Step 3 INCOMPLETE - do not proceed.

---

## Step 4: Code Review

Call `code-reviewer` subagent. If critical issues found: STOP, fix, re-run `tester`, re-run `code-reviewer`. Repeat until no critical issues.

**Output:** `✓ Step 4: Code reviewed - [0] critical issues`

**Validation:** If critical issues > 0, Step 4 INCOMPLETE - do not proceed.

---

## Step 5: User Approval ⏸ BLOCKING GATE

Present summary (3-5 bullets): what implemented, tests passed, code review outcome.

**Ask user explicitly:** "Phase implementation complete. All tests pass, code reviewed. Approve changes?"

**Stop and wait** - do not proceed until user responds.

**Output:** `✓ Step 5: User approved - Ready to complete`

---

## Step 6: Finalize

**Prerequisites:** User approved in Step 5.

1. **STATUS UPDATE (PARALLEL):**
    - Call `project-manager` subagent to update plan status
    - Call `docs-manager` subagent to update documentation

2. **ONBOARDING CHECK:** Detect onboarding requirements + generate summary.

3. **AUTO-COMMIT:** Call `git-manager` subagent. Run only if Steps 1-2 successful + User approved + Tests passed.

**Output:** `✓ Step 6: Finalize - Status updated - Git committed`

---

## Critical Enforcement Rules

**Step output format:** `✓ Step [N]: [Brief status] - [Key metrics]`

**TaskCreate tracking required:** Initialize at Step 0, mark each step complete before next.

**Mandatory subagent calls:** Step 3: `tester` | Step 4: `code-reviewer` | Step 6: `project-manager` AND `docs-manager` AND `git-manager`

**Blocking gates:**

- Step 3: Tests must be 100% passing
- Step 4: Critical issues must be 0
- Step 5: User must explicitly approve

Do not skip steps. Do not proceed if validation fails. Do not assume approval without user response. One plan phase per command run.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
