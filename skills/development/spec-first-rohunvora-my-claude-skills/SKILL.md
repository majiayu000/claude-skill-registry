---
name: spec-first
description: Use when building anything non-trivial. Enforces a spec → plan → execute → verify loop that prevents "looks right" failures. Creates spec.md, todo.md, and decisions.md before writing code.
---

# Spec-First Development

A structured workflow for LLM-assisted coding that delays implementation until decisions are explicit.

## When This Activates

- "Build X" or "Create Y" (new features/projects)
- "Implement..." (non-trivial functionality)
- "Add a feature that..." (multi-step work)
- Any request requiring 3+ files or unclear requirements

## When to Skip

- Single-file changes under 50 lines
- Typo fixes, log additions, config tweaks
- User explicitly says "just do it" or "quick fix"

## Core Principles

1. **Delay implementation until tradeoffs are explicit** — Use conversation to clarify constraints, compare options, surface risks. Only then write code.

2. **Treat the model like a junior engineer with infinite typing speed** — Provide structure: clear interfaces, small tasks, explicit acceptance criteria. Code is cheap; understanding and correctness are scarce.

3. **Specs beat prompts** — For anything non-trivial, create a durable artifact (spec file) that can be re-fed, diffed, and reused across sessions.

4. **Generated code is disposable; tests are not** — Assume rewrites. Design for easy replacement: small modules, minimal coupling, clean seams, strong tests.

5. **The model is over-confident; reality is the judge** — Everything important gets verified by execution: tests, linters, typecheckers, reproducible builds.

## The 6-Stage Workflow

### Stage A: Frame the Problem (conversation mode)

**Goal:** Decide before you implement.

Prompts that work:
- "List 3 viable approaches. Compare on: complexity, failure modes, testability, future change, time to first demo."
- "What assumptions are you making? Which ones are risky?"
- "Propose a minimal version that can be deleted later without regret."

**Output:** Decision notes for `decisions.md`

### Stage B: Write spec.md (freeze decisions)

**Goal:** Turn decisions into unambiguous requirements.

```markdown
# spec.md

## Purpose
One paragraph: what this is for.

## Non-Goals
Explicitly state what you are NOT building.

## Interfaces
Inputs/outputs, data types, file formats, API endpoints, CLI commands.

## Key Decisions
Libraries, architecture, persistence choices, constraints.

## Edge Cases and Failure Modes
Timeouts, retries, partial failures, invalid input, concurrency, idempotency.

## Acceptance Criteria
Bullet list of testable statements. Avoid "should be fast."
Prefer: "processes 1k items under 2s on M1 Mac."

## Test Plan
Unit/integration boundaries, fixtures, golden files, what must be mocked.
```

### Stage C: Generate todo.md (planning mode)

**Goal:** Stepwise checklist where each step has a verification command.

```markdown
# todo.md

- [ ] Add project scaffolding (build/run/test commands)
  Verify: `npm run build && npm test`

- [ ] Implement module X with interface Y
  Verify: `npm test -- --grep "module X"`

- [ ] Add tests for edge cases A/B/C
  Verify: `npm test -- --grep "edge cases"`

- [ ] Wire integration
  Verify: `npm run integration`

- [ ] Add docs
  Verify: `npm run docs && open docs/index.html`
```

Each item must be independently checkable. This prevents "looks right" progress.

### Stage D: Execute Changes (implementation mode)

**Goal:** Small diffs, frequent verification, controlled context.

Rules:
- One logical change per step
- Keep focus on one interface at a time
- After each change: run verification command, paste actual output back
- Commit early and often

For large codebases:
- Provide only relevant files plus spec/todo
- If summarizing repo, do it once and keep as reusable artifact

### Stage E: Verify and Review (adversarial mode)

**Goal:** Force the model to try to break its own work.

Prompts:
- "Act as a hostile reviewer. Find correctness bugs, not style nits. List concrete failing scenarios."
- "Given these acceptance criteria, which are not actually satisfied? Be specific."
- "Propose 5 tests that would fail if the implementation is wrong."

### Stage F: Decide What Lasts

**Goal:** Keep the system easy to delete and rewrite.

Heuristics:
- Keep "policy" (business rules) separate from "mechanism" (I/O, DB, HTTP)
- Prefer shallow abstractions that can be removed without cascade
- Invest in tests and fixtures more than clever architecture

## The Three-File Convention

Keep at the root of every project:

```
spec.md      # what/why/constraints
todo.md      # steps + verification commands
decisions.md # tradeoffs, rejected options, assumptions
```

## Agent Readiness Checklist (IMPACT)

Before running autonomous/agentic execution, verify:

| Dimension | Question | If No... |
|-----------|----------|----------|
| **Intent** | Do you have acceptance criteria and a test harness? | Don't run agent |
| **Memory** | Do you have durable artifacts (spec/todo) so it can resume? | It will thrash |
| **Planning** | Can it produce/update a plan with checkpoints? | It will improvise badly |
| **Authority** | Is what it can do restricted (edit, test, commit)? | Too risky |
| **Control Flow** | Does it decide next step based on tool output? | It's just generating blobs |
| **Tools** | Does it have minimum necessary tooling and nothing extra? | Attack surface too large |

Approve at meaningful checkpoints (end of todo item, after test suite passes), not every micro-step.

## Prompt Patterns

**Authoritarian (for correctness):**
```
Edit these files: [paths]
Interface: [exact signatures]
Acceptance criteria: [list]
Required tests: [list]
Don't change anything else.
```

**Options and tradeoffs (for design):**
```
Give me 3 options and a recommendation.
Make the recommendation conditional on constraints A/B/C.
```

**Context discipline (for large codebases):**
```
Only use the files I provided.
If you need more context, ask for a specific file and explain why.
```

**Make it provable:**
```
Add a test that fails on the buggy version and passes on the correct one.
```

## Output Format

When this skill activates, produce:

```
SPEC-FIRST WORKFLOW

STAGE A - FRAMING:
[3 approaches with tradeoffs]
[Recommendation]

STAGE B - SPEC:
[Draft spec.md content]

STAGE C - TODO:
[Draft todo.md with verification commands]

Ready to proceed to Stage D (execution)?
```
