---
name: create-a-big-plan
description: Create a large Prime Agent plan before implementation. Use for open-ended or high-risk repo efforts needing 10 or more planning questions, web research, reviewer or criticizer subagents, and refinement until convergence; exclude direct implementation-only, factual/explanation, trivial command-only, or explicit no-plan requests.
---

# Create A Big Plan

Use this skill when the user wants a large, high-risk, or open-ended plan before a repository change.

## Setup

1. Read `../_shared/references/prime-planning-workflow.md`, `../_shared/references/state-and-config.md`, and `../_shared/references/plan-artifact-template.md`.
2. Initialize state with `python3 scripts/optim_plans.py init --repo <target-repo> --topic <topic> --plan-level create-a-big-plan --request-text <original-request>`.
3. Use `.git/optim-plans` for controller state and `docs/optim-plans/YYYY-MM-DD-topic/` for public artifacts.

## Depth Contract

- Inspect the target Git repo read-only before the first product question.
- Ask at least 10 planning questions, one at a time. There is no maximum; stop only when the decision tree is resolved.
- Use web research during both brainstorming and refinement when outside facts, patterns, or ecosystem constraints matter.
- Use the standard choice prompt format: recommended first, `Other` second-last, `Auto-complete` last.
- Ask the mandatory final scope confirmation before writing `PLAN_v1.md`.
- Write `PLAN_v1.md` under `docs/optim-plans/YYYY-MM-DD-topic/`.
- Run reviewer or criticizer refinement until convergence while high-priority findings, unresolved criticizer questions, or evidence gaps remain.
- In each refinement round, surface at most five high-priority comments or questions.
- After convergence or user acceptance, ask the native execution handoff question without `Auto-complete`.

## Fit

Choose this level for new systems, large feature surfaces, cross-repository work, open-ended architecture, safety-sensitive changes, unclear workflows, or plans where the shape is not yet known.

Use `reference-before-plan` instead when downloaded external projects, papers, articles, or documentation must be studied before planning choices are safe.
