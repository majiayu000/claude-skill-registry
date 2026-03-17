---
name: code-parallel
version: 1.0.0
description: '[Implementation] Execute parallel or sequential phases based on plan structure'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

> **Skill Variant:** Variant of `/code` — parallel phase execution from a plan.

## Quick Summary

**Goal:** Execute implementation phases from an existing plan using parallel fullstack-developer subagents.

**Workflow:**
1. **Load** — Read the implementation plan and identify parallel phases
2. **Dispatch** — Launch subagents per phase with strict file ownership
3. **Merge** — Integrate results and verify

**Key Rules:**
- Requires an existing plan file as input
- Each subagent owns specific files; no cross-boundary edits
- Sequential phases must wait for dependencies

Execute plan: <plan>$ARGUMENTS</plan>

**IMPORTANT:** Activate needed skills. Ensure token efficiency. Sacrifice grammar for concision.

## Workflow

### 1. Plan Analysis

- Read `plan.md` from given path
- **Check for:** Dependency graph, Execution strategy, Parallelization Info, File Ownership matrix
- **Decision:** IF parallel-executable → Step 2A, ELSE → Step 2B
- **External Memory**: Re-read any `.ai/workspace/analysis/` files referenced in the plan before dispatching to parallel agents.

### 2A. Parallel Execution

1. Parse execution strategy (which phases concurrent/sequential, file ownership)
2. Launch multiple `fullstack-developer` agents simultaneously for parallel phases
    - Pass: phase file path, environment info, file ownership boundaries
3. Wait for parallel group completion, verify no conflicts
4. Execute sequential phases (one agent per phase after dependencies)
5. Proceed to Step 3

### 2B. Sequential Execution

Follow `./.claude/workflows/primary-workflow.md`:

1. Use main agent step by step
2. Read `plan.md`, implement phases one by one
3. Use `project-manager` for progress updates
4. Use `ui-ux-designer` for frontend
5. Run type checking after each phase
6. Proceed to Step 3

### 3. Testing

- Use `tester` for full suite (NO fake data/mocks)
- If fail: `debugger` → fix → repeat

### 4. Code Review

- Use `code-reviewer` for all changes
- If critical: fix → retest

### 5. Project Management & Docs

- If approved: `project-manager` + `docs-manager` in parallel (update plans, docs, roadmap)
- If rejected: fix → repeat

### 6. Onboarding

- Guide user step by step (1 question at a time)

### 7. Final Report

- Summary, guide, next steps
- Ask to commit (use `git-manager` if yes)

**Examples:**

- Parallel: "Phases 1-3 parallel, then 4" → Launch 3 agents → Wait → Launch 1 agent
- Sequential: "Phase 1 → 2 → 3" → Main agent implements each phase

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
