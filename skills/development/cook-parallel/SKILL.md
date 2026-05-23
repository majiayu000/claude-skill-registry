---
name: cook-parallel
version: 1.0.0
description: '[Implementation] Parallel implementation - multiple tasks simultaneously'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/understand-code-first-protocol.md` before executing.

> **Skill Variant:** Variant of `/cook` — parallel multi-task implementation with subagents.

## Quick Summary

**Goal:** Implement multiple independent tasks simultaneously using parallel fullstack-developer subagents.

**Workflow:**
1. **Plan** — Create plan with parallel phases and strict file ownership
2. **Dispatch** — Launch fullstack-developer subagents per phase
3. **Merge** — Integrate all changes and verify
4. **Review** — Run code-simplifier and review-changes

**Key Rules:**
- Phases must have non-overlapping file ownership
- User approval required before dispatching subagents
- Break work into todo tasks; add final self-review task

Execute these tasks in parallel for maximum efficiency:
<tasks>$ARGUMENTS</tasks>

**Mode:** PARALLEL - Multiple subagents working concurrently.

## Workflow

### 1. Task Decomposition

- Analyze tasks for independence
- Group into parallelizable work units
- Identify dependencies between units
- Create dependency graph
- **External Memory**: Write task analysis to `.ai/workspace/analysis/{task-name}.analysis.md`. Re-read before parallel dispatch.

### 2. Parallel Research (if needed)

Launch multiple `researcher` subagents simultaneously:

```
Task A research ──┐
Task B research ──┼──► Synthesis
Task C research ──┘
```

### 3. Parallel Planning

- Use `planner` subagent with synthesized research
- Create plan with parallel-safe phases
- Mark file ownership boundaries (prevent conflicts)

### 4. Parallel Implementation

Launch multiple `fullstack-developer` subagents:

```
Phase 1 (Backend API) ──┐
Phase 2 (Frontend UI) ──┼──► Integration
Phase 3 (Tests)       ──┘
```

**Critical:** Each subagent must stay within file ownership boundaries.

### 5. Integration & Testing

- Merge parallel outputs
- Use `tester` subagent for integration tests
- Use `debugger` if integration issues found

### 6. Review & Report

- Use `code-reviewer` for final review
- Consolidate all changes
- Report to user

## Parallelization Rules

| Rule                 | Description                                    |
| -------------------- | ---------------------------------------------- |
| **File Ownership**   | Each subagent owns specific files - no overlap |
| **Dependency Order** | Respect dependency graph                       |
| **Max Concurrent**   | 3 subagents max to prevent conflicts           |
| **Sync Points**      | Integration checkpoints between phases         |

## When to Use

- Multi-component features (backend + frontend)
- Large refactoring across independent modules
- Parallel test writing
- Documentation updates alongside code

## Example Task Split

```
"Add user authentication with login UI"
├── Backend API (subagent 1)
│   ├── auth-controller.ts
│   └── auth-service.ts
├── Frontend UI (subagent 2)
│   ├── login-page.component.ts
│   └── login-form.component.ts
└── Tests (subagent 3)
    ├── auth.spec.ts
    └── login.e2e.ts
```

## Trade-offs

| Aspect       | Parallel             | Sequential |
| ------------ | -------------------- | ---------- |
| Speed        | ~2-3x faster         | Baseline   |
| Coordination | Higher complexity    | Simple     |
| Conflicts    | Risk of merge issues | None       |
| Context      | Split across agents  | Unified    |

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
