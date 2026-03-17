---
name: code-auto
version: 1.0.0
description: '[Implementation] [AUTO] Start coding & testing an existing plan (trust me bro)'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

## Quick Summary

**Goal:** Automatically execute an existing plan with testing and code review — no user approval gate (trust mode).

**Workflow:**

1. **Plan Detection** — Find latest plan or use provided path, select next incomplete phase
2. **Analysis & Tasks** — Extract tasks into TaskCreate with step numbering
3. **Implementation** — Implement phase step-by-step, run type checks
4. **Testing** — Tester subagent; must reach 100% pass
5. **Code Review** — Code-reviewer subagent; must reach 0 critical issues
6. **Finalize** — Update status, docs, auto-commit; optionally loop to next phase

**Key Rules:**

- No user approval gate (unlike `/code` which has a blocking Step 5)
- Tests must be 100% passing; critical issues must be 0
- `$ALL_PHASES=Yes` (default) processes all phases in one run
- Never comment out tests or use fake data to pass

**MUST READ** `CLAUDE.md` then **THINK HARDER** to start working on the following plan:
<plan>$ARGUMENTS</plan>

## Arguments

- $PLAN: $1 (Mention specific plan or auto detected, default: latest plan)
- $ALL_PHASES: $2 (`Yes` to finish all phases in one run or `No` to implement phase-by-phase, default: `Yes`)

---

## Step 0: Plan Detection & Phase Selection

**If `$PLAN` is empty:**

1. Find latest `plan.md` in `./plans`
2. Parse plan for phases and status, auto-select next incomplete

**If `$PLAN` provided:** Use that plan and detect which phase to work on.

**Output:** `✓ Step 0: [Plan Name] - [Phase Name]`

---

## Workflow Sequence

**Rules:** Follow steps 1-5 in order. Each step requires output marker `✓ Step N:`. Mark each complete in TaskCreate before proceeding. Do not skip steps.

---

## Step 1: Analysis & Task Extraction

Use `project-manager` agent to read plan file completely. Map dependencies. List ambiguities. Identify required skills. If the plan references analysis files in `.ai/workspace/analysis/`, re-read them before implementation.

**TaskCreate Initialization:**

- Initialize TaskCreate with `Step 0: [Plan Name] - [Phase Name]` and all steps (1-5)
- Read phase file, look for tasks/steps/phases/sections/numbered/bulleted lists
- Convert to TaskCreate tasks with UNIQUE names:
    - Phase Implementation tasks → Step 2.X (Step 2.1, Step 2.2, etc.)
    - Phase Testing tasks → Step 3.X
    - Phase Code Review tasks → Step 4.X

**Output:** `✓ Step 1: Found [N] tasks across [M] phases - Ambiguities: [list or "none"]`

---

## Step 2: Implementation

Implement selected plan phase step-by-step. Mark tasks complete as done. For UI work, call `ui-ux-designer` subagent. Run type checking and compile.

**Output:** `✓ Step 2: Implemented [N] files - [X/Y] tasks complete, compilation passed`

---

## Step 3: Testing

Call `tester` subagent. If ANY tests fail: STOP, call `debugger`, fix, re-run. Repeat until 100% pass.

**Testing standards:** Forbidden: commenting out tests, changing assertions to pass, TODO/FIXME to defer fixes.

**Output:** `✓ Step 3: Tests [X/X passed] - All requirements met`

**Validation:** If X ≠ total, Step 3 INCOMPLETE - do not proceed.

---

## Step 4: Code Review

Call `code-reviewer` subagent. If critical issues found: STOP, fix, re-run `tester`, re-run `code-reviewer`. Repeat until no critical issues.

**Output:** `✓ Step 4: Code reviewed - [0] critical issues`

**Validation:** If critical issues > 0, Step 4 INCOMPLETE - do not proceed.

---

## Step 5: Finalize

1. **STATUS UPDATE (PARALLEL):** Call `project-manager` + `docs-manager` subagents.
2. **ONBOARDING CHECK:** Detect onboarding requirements + generate summary.
3. **AUTO-COMMIT:** Call `git-manager` subagent. Run only if Steps 1-2 successful + Tests passed.

If $ALL_PHASES is `Yes`: proceed to next phase automatically.
If $ALL_PHASES is `No`: ask user before proceeding to next phase.

**If last phase:** Generate summary report. Ask user about `/preview` and `/plan-archive`.

**Output:** `✓ Step 5: Finalize - Status updated - Git committed`

---

## Critical Enforcement Rules

**Step output format:** `✓ Step [N]: [Brief status] - [Key metrics]`

**TaskCreate tracking required:** Initialize at Step 0, mark each step complete before next.

**Mandatory subagent calls:** Step 3: `tester` | Step 4: `code-reviewer` | Step 5: `project-manager` AND `docs-manager` AND `git-manager`

**Blocking gates:**

- Step 3: Tests must be 100% passing
- Step 4: Critical issues must be 0

Do not skip steps. Do not proceed if validation fails. One plan phase per command run.

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
