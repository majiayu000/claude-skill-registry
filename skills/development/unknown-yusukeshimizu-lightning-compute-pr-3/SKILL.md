---
name: lcp-execplan
description: Create and maintain ExecPlans for complex work (design-to-implementation) following the repo's ExecPlan standard.
metadata:
  short-description: ExecPlan workflow (design → implementation)
---

Use this skill when the task is a complex feature, a significant refactor, or has ambiguous requirements that benefit from a living plan.

## Source of truth

The ExecPlan standard for this repo is in:

- `.codex/skills/lcp-execplan/references/PLANS.md`

## Workflow

1. Read the full reference `PLANS.md` above (it is intentionally strict).
2. Create a single ExecPlan file as instructed (formatting rules matter).
3. Keep the ExecPlan as a living document: update Progress/Decisions/Discoveries as you implement.
4. Do not ask the user for “next steps” mid-execution; proceed milestone by milestone.

## Acceptance

An ExecPlan is done only when it enables a complete novice (with only the repo + the plan) to reproduce a working, observable outcome.
