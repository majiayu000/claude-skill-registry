---
name: create-a-plan
description: Create a researched Prime Agent plan before implementation. Use for broad or risky repo changes needing 5 to 10 planning questions, web research, reviewer or criticizer settings, and bounded refinement; exclude direct implementation-only, factual/explanation, trivial command-only, or explicit no-plan requests.
---

# Create A Plan

Use this skill when the user wants a substantive plan before a repository change.

## Setup

1. Read `../_shared/references/prime-planning-workflow.md`, `../_shared/references/state-and-config.md`, and `../_shared/references/plan-artifact-template.md`.
2. Initialize state with `python3 scripts/optim_plans.py init --repo <target-repo> --topic <topic> --plan-level create-a-plan --request-text <original-request>`.
3. Use `.git/optim-plans` for controller state and `docs/optim-plans/YYYY-MM-DD-topic/` for public artifacts.

## Depth Contract

- Inspect the target Git repo read-only before the first product question.
- Ask 5 to 10 planning questions, one at a time.
- Use web research during brainstorming whenever outside library behavior, ecosystem precedent, UX convention, protocol semantics, or compatibility affects the recommendation.
- Use the standard choice prompt format: recommended first, `Other` second-last, `Auto-complete` last.
- Ask the mandatory final scope confirmation before writing `PLAN_v1.md`.
- Write `PLAN_v1.md` under `docs/optim-plans/YYYY-MM-DD-topic/`.
- Run up to five refinement rounds. Continue only for high-priority reviewer findings or unresolved criticizer questions.
- In each refinement round, surface at most five high-priority comments or questions.
- After convergence or user acceptance, ask the native execution handoff question without `Auto-complete`.

## Fit

Choose this level for multi-file changes, architecture boundaries, user-facing workflows, external APIs, dependency upgrades, compatibility risk, or cases where web evidence should shape the plan.

Escalate to `create-a-big-plan` when the problem is open-ended, cross-system, strategically ambiguous, or likely to require more than ten planning decisions.
