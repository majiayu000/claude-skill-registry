---
name: testing
description: Write, configure, and run unit + integration tests using project-independent best practices; detect tooling; triage failures/flakes; keep a compact Testing State Capsule.
metadata:
  short-description: Unit + integration testing best practices
---

# Testing

Help the agent add and improve unit/integration tests across languages and frameworks, while staying aligned with repo-specific conventions.

## Core rules
- Follow the closest in-scope `AGENTS.md` instructions first.
- If present, follow `docs/testing-policy.md`.
- Prefer the smallest, fastest test that proves the change; expand only if needed by policy/risk.
- Do not invent test commands: discover how the repo runs tests, then reuse it.
- Keep tests deterministic: no network calls, no real time dependence, no order dependence, no shared global state.
- Ask clarifying questions only when they unblock forward progress; otherwise proceed with explicit assumptions.
- While this skill is active, keep a short **Testing State Capsule** updated in every reply.
- If the task continues across turns, keep following this skill; if context was reset/compacted, re-invoke `$testing` and restate the state capsule.

## Clarifying loop (no fixed turn limit)
If test tooling/requirements are unclear:
1) Ask the minimum set of questions that unblock an immediate next action.
2) If the user cannot answer, propose reasonable assumptions and continue (clearly marked), preserving easy rollback.
3) After each user answer, restate the updated state capsule and continue.

## Workflow (repeatable)
1) Read project context (`AGENTS.md`, `docs/testing-policy.md`, README/CONTRIBUTING/CI config).
2) Discover test tooling and commands (see `references/tooling-discovery.md`).
3) Choose the right layer:
   - Unit: pure logic and edge cases; fast; isolated.
   - Integration: cross-module boundaries and real dependency behavior; realistic setup.
4) Draft a small test plan (use `assets/test-plan-template.md` and/or `assets/test-matrix.csv` as needed).
5) Implement tests with minimal coupling and clear naming (see `references/unit-testing.md`, `references/integration-testing.md`).
6) Run the narrowest relevant tests, then expand per policy/risk.
7) If failures are flaky or environment-related, follow `references/flaky-tests.md`.

## Output requirements (when this skill is used)
- Always include exact commands you ran (or will run) and the observed output snippets that matter.
- Always update the **Testing State Capsule** (keep it short).
- When making assumptions, label them and provide the easiest validation step.

### Testing State Capsule (template)
Keep this block up to date and near the end of each reply:

```text
[Testing State Capsule]
Goal:
Repo signals (runner/framework):
Unit command(s):
Integration command(s):
Env/deps (DB/containers/fixtures):
Assumptions:
Last result:
Next action:
Open questions:
```

## References
- `references/principles.md`
- `references/tooling-discovery.md`
- `references/unit-testing.md`
- `references/integration-testing.md`
- `references/flaky-tests.md`

## Assets
- `assets/test-plan-template.md`
- `assets/test-matrix.csv`
