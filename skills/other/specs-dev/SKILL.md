---
name: specs-dev
description: Plan-first development workflow with review gates. Use when implementing features, refactoring, or any task requiring structured planning, iterative implementation with reviews, and clean commits. Triggers on requests like "implement feature X", "plan and build", "spec-driven development", or when user wants disciplined, reviewed code changes.
---

# Specs-Dev Workflow

A disciplined, review-gated development workflow ensuring quality through structured planning and iterative implementation.

## When to Use

- Implementing new features
- Complex refactoring
- Any task requiring planning before coding
- When user requests "plan first" or "spec-driven" approach
- Multi-file changes that benefit from review gates

## Workflow Overview

| Phase             | Purpose                       | Exit Criteria                |
| ----------------- | ----------------------------- | ---------------------------- |
| 1. Discovery      | Understand requirements       | User approves summary        |
| 2. Planning       | Create reviewed plan          | Plan reviewed and approved   |
| 3. Implementation | Iterative coding with reviews | All tasks complete, reviewed |
| 4. Completion     | Final validation              | Tests pass, docs updated     |

## Phase 1: Discovery

**Goal:** Reach shared understanding before planning.

1. Interpret the request — state initial understanding
2. Ask clarifying questions (goals, constraints, success criteria, out-of-scope)
3. Iterate — reflect answers, tighten understanding
4. Summarize — present final requirements

**Gate A:** "Do I understand correctly? Should I proceed to create the plan?" — Wait for approval.

## Phase 2: Planning

**Goal:** Create a comprehensive, reviewed implementation plan.

1. Draft plan using `references/templates/plan.md`
2. Review loop with reviewer (max 3 rounds) — see `references/agents/reviewer.md`
3. Integrate feedback, iterate until approved
4. **Gate B:** Present to user, wait for approval
5. Create session: `.agents/sessions/{YYYY-MM-DD}-{feature-name}/`
6. Save `plan.md` and `tasks.md` (use `references/templates/`)

Quality gates: see `references/gates.md`

## Phase 3: Implementation

**Goal:** Implement tasks iteratively with approval-gated review loops.

> ⚠️ **MANDATORY: You MUST follow `references/loop.md`** — Read and execute the implementation loop exactly as specified. Do not skip or deviate from the defined state machine.

**Summary:** For each task:

```
IMPLEMENTING → VALIDATING → REVIEWING → loop until approved → COMMITTING → DOCUMENTING → NEXT TASK
```

**Required Steps:**

1. **Read `references/loop.md`** before starting any implementation
2. Follow the state machine transitions exactly
3. Complete each state's requirements before transitioning
4. Max 3 iterations per task before escalating to user
5. Subagents: `references/agents/worker.md`, `references/agents/reviewer.md`

Quality gates: see `references/gates.md`

## Phase 4: Completion

**Goal:** Final validation and wrap-up.

1. Run full test suite
2. Update `plan.md` with results, final status, known issues
3. Verify all tasks complete in `tasks.md`
4. Summarize completed work, risks, outcomes
5. Confirm with user — session ready for merge/release

Quality gates: see `references/gates.md`

## Subagent Delegation

**Reviewer** — Plan reviews, code reviews:

```
Context: references/agents/reviewer.md
Task: Review [plan/code] for completeness, security, performance, patterns
```

**Worker** — Focused implementation:

```
Context: references/agents/worker.md
Task: Implement [objective] in [files] with [acceptance criteria]
```

## Session Structure

```
.agents/sessions/{YYYY-MM-DD}-{feature-name}/
├── plan.md      # Strategic plan
└── tasks.md     # Tactical tasks
```

## References

```
references/
├── loop.md          # Phase 3 state machine, steps, fix routing
├── gates.md         # Quality gates for all phases
├── help.md          # Common issues, best practices
├── agents/
│   ├── reviewer.md  # Reviewer subagent context
│   └── worker.md    # Worker subagent context
└── templates/
    ├── plan.md      # Plan document template
    └── tasks.md     # Tasks document template
```

| File                 | When to Read                      |
| -------------------- | --------------------------------- |
| `loop.md`            | Phase 3 (MANDATORY — must follow) |
| `agents/reviewer.md` | Plan/code reviews                 |
| `agents/worker.md`   | Task implementation               |
| `templates/plan.md`  | Phase 2                           |
| `templates/tasks.md` | Phase 2                           |
| `gates.md`           | Each phase exit                   |
| `help.md`            | When stuck                        |
