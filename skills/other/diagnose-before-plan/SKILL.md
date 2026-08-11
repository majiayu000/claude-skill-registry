---
name: diagnose-before-plan
description: Diagnose failures before creating a Prime Agent plan. MUST USE for bugs, CI failures, test failures, regressions, incidents, broken behavior, root cause, RCA, or debug-why requests before deciding whether to plan; preserve language, reviewer, and criticizer settings in .git/optim-plans; exclude ordinary feature planning, direct implementation-only, factual/explanation, trivial command-only, or explicit no-plan requests.
---

# Diagnose Before Plan

Use this skill for problem or failure inputs that need diagnosis before planning.

## Setup

1. Read `../_shared/references/prime-planning-workflow.md`, `../_shared/references/state-and-config.md`, and `../_shared/references/plan-artifact-template.md`.
2. Use `.git/optim-plans` for controller state and `docs/optim-plans/YYYY-MM-DD-topic/` for public artifacts.
3. Preserve reviewer and criticizer settings for any selected planning skill.

## Diagnostic Workflow

1. Inspect available evidence first: repository files, logs, tests, command output, stack traces, recent diffs, CI output, environment details, and user-provided symptoms.
2. Produce an in-message RCA summary before asking whether to plan. Use at most 5 Whys. Stop with `unknown` when evidence is insufficient.
3. Ask one choice prompt in the configured language:
   1. `Create the scoped fix plan` - recommended when evidence supports a planning path.
   2. `Stop after RCA` - keep the diagnosis only.
   3. `Other`.
   4. `Auto-complete`.
4. On opt-out, stop after the summary. Do not write `PROBLEM_ANALYSIS.md` on opt-out.
5. On opt-in or `Auto-complete`, select the smallest fitting planning skill and continue with that skill's contract.

## Level Selection

- `create-a-small-plan`: clear root cause, obvious fix shape, few local files, limited risk.
- `create-a-plan`: multi-file fix, external API or dependency behavior, compatibility concerns, or research needed.
- `create-a-big-plan`: cross-system failure, unclear root cause, redesign pressure, or high recoverability risk.

After opt-in, write `PROBLEM_ANALYSIS.md` in the selected run artifact directory before `PLAN_v1.md` and pass the RCA summary into the selected planning skill.
