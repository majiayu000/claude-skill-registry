---
name: ai-plan
description: "Use when an approved spec exists and needs to be broken into executable tasks with agent assignments. Creates the implementation plan that /ai-dispatch executes."
effort: max
argument-hint: "[spec-NNN or topic]"
---


# Plan

## Purpose

Implementation planning skill. Takes an approved spec (from `/ai-brainstorm` or manual creation) and produces a phased execution plan with bite-sized tasks, agent assignments, and gate criteria. The plan is the contract that `/ai-dispatch` executes.

HARD GATE: user must approve the plan before `/ai-dispatch` can run.

## When to Use

- After `/ai-brainstorm` produces an approved spec
- When a spec exists but plan.md has placeholder content
- When re-planning is needed (plan failed, scope changed)

## Process

1. **Read spec** -- load `specs/spec.md`
2. **Read context** -- `docs/solution-intent.md` section 7 (roadmap), `decision-store.json` (constraints)
3. **Explore codebase** -- understand current architecture, patterns, and affected files
4. **Classify pipeline** -- select full/standard/hotfix/trivial based on change scope
5. **Decompose into tasks** -- bite-sized (2-5 min each), single-agent, single-concern
6. **Assign agents** -- capability-match each task to the right agent
7. **Order phases** -- define phase boundaries and gate criteria
8. **Review plan** -- self-review with spec-reviewer pattern (max 2 iterations)
9. **Write artifacts** -- persist plan.md via Write tool to `specs/plan.md`
10. **STOP** -- present plan. User runs `/ai-dispatch` to execute.

## Pipeline Classification

| Pipeline | Trigger | Steps |
|----------|---------|-------|
| `full` | New feature, refactor, >5 files | discover, architecture, risk, test-plan, spec, dispatch |
| `standard` | Enhancement, 3-5 files | discover, risk, spec, dispatch |
| `hotfix` | Bug fix, security patch, <3 files | discover, risk, spec, dispatch |
| `trivial` | Typo, comment, single-line | spec, dispatch |

Override: `/ai-plan --pipeline=hotfix`.

## Task Decomposition Rules

Each task MUST be:

- **Bite-sized**: completable in 2-5 minutes by an agent
- **Single-agent**: assigned to exactly one agent (build, verify, guard)
- **Single-concern**: does one thing (not "implement feature AND write tests")
- **Verifiable**: has a clear done condition (test passes, lint clean, file exists)
- **Ordered**: dependencies are explicit (T-3 blocked by T-2)

**TDD enforcement**: for features needing tests, always produce paired tasks:
- `T-N: Write failing tests for [feature]` (RED) -- assigned to build/test mode
- `T-N+1: Implement [feature] to pass tests` (GREEN, blocked by T-N) -- assigned to build/code mode, constraint: "DO NOT modify test files from T-N"

## Agent Assignment

| Agent | Capabilities | Assign when... |
|-------|-------------|----------------|
| `build` | Code read-write, tests, debug | Implementation, test writing, bug fixes |
| `verify` | Read-only scanning, 7 modes | Quality checks, security scans, gap analysis |
| `guard` | Advisory, drift detection | Pre-dispatch governance checks |

## Plan Artifacts

### plan.md

```markdown
# Plan: spec-NNN [title]

## Pipeline: [full|standard|hotfix|trivial]
## Phases: N
## Tasks: N (build: N, verify: N, guard: N)

### Phase 1: [name]
**Gate**: [what must be true before Phase 2 starts]
- T-1.1: [task description] (agent: build)
- T-1.2: [task description] (agent: build)

### Phase 2: [name]
**Gate**: [what must be true before Phase 3 starts]
...
```

## Common Mistakes

- Tasks too large (> 5 min). Split them.
- Missing dependencies between tasks.
- Assigning code-write tasks to verify (verify is read-only).
- Not pairing RED/GREEN tasks for TDD.
- Planning implementation details (plan says WHAT, code says HOW).
- Skipping the review step.

## No-Execution Protocol

`/ai-plan` is planning-only. It MUST NOT:
- Invoke `ai-build agent` or `/ai-dispatch` for task execution
- Modify source code
- Check off implementation tasks as completed

It MAY:
- Write plan.md via Write tool to `specs/plan.md`
- Run codebase exploration (read-only)

## Integration

- **Called by**: user directly, or after `/ai-brainstorm` approval
- **Calls**: `/ai-explore` (codebase context), Write tool (artifact creation)
- **Transitions to**: `/ai-dispatch` (ONLY -- user must invoke explicitly)

$ARGUMENTS
