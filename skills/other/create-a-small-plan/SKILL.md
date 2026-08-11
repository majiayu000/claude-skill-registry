---
name: create-a-small-plan
description: Create a small Prime Agent plan before implementation. Use for small scoped repo changes needing 1 to 3 planning questions and one reviewer or criticizer refinement pass; exclude direct implementation-only, factual/explanation, trivial command-only, or explicit no-plan requests.
---

# Create A Small Plan

Use this skill when the user wants a compact plan before a repository change.

## Setup

1. Read `../_shared/references/prime-planning-workflow.md`, `../_shared/references/state-and-config.md`, and `../_shared/references/plan-artifact-template.md`.
2. Initialize state with `python3 scripts/optim_plans.py init --repo <target-repo> --topic <topic> --plan-level create-a-small-plan --request-text <original-request>`.
3. Use `.git/optim-plans` for controller state and `docs/optim-plans/YYYY-MM-DD-topic/` for public artifacts.

## Depth Contract

- Inspect the target Git repo read-only before the first product question.
- Ask 1 to 3 planning questions, one at a time.
- Use the standard choice prompt format: recommended first, `Other` second-last, `Auto-complete` last.
- Ask the mandatory final scope confirmation before writing `PLAN_v1.md`.
- Write `PLAN_v1.md` under `docs/optim-plans/YYYY-MM-DD-topic/`.
- Run exactly one reviewer or criticizer refinement round unless the user explicitly accepts the plan for native execution.
- After that one refinement round, revise to `PLAN_v2.md` if needed, then ask the native execution handoff question without `Auto-complete`.

## Fit

Choose this level for a change limited to a few local files, clear ownership, low architectural risk, and focused verification.

Escalate to `create-a-plan` when the plan needs external API semantics, dependency behavior, compatibility research, cross-module design, or more than three meaningful decisions.
