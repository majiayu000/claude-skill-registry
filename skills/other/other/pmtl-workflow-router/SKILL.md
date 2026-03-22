---
name: pmtl-workflow-router
description: PMTL_VN workflow routing layer. Use when a task needs the right combination of repo-local PMTL skills, Superpowers workflow skills, and generic tool skills without making the user remember the skill names.
---

# PMTL Workflow Router

## Purpose

Own routing for multi-step PMTL work so the agent picks the right skill stack in the right order instead of guessing from a crowded global skill list.

## Use When

- Starting a new task in this repo and the correct skill is not obvious.
- The task spans multiple phases such as design, implementation, review, or verification.
- The user describes intent like "plan this", "debug this", "review this", or "ship this safely" without naming a skill.

## Required Inputs

- The task intent such as feature, bug, review, verification, design, or incident.
- The touched area when known such as `apps/web`, `apps/api`, auth, search, UI, or infra.
- Whether the user wants a workflow phase like brainstorming, TDD, code review, or subagent execution.

## Expected Output

- A clear routing decision that names the canonical PMTL skill, any paired Superpowers workflow skill, and any generic tool skill if needed.
- No duplicate policy loading from global skills when repo-local PMTL skills already own the behavior.

## Execution Approach

1. Start with repo intent, not tool availability.
2. Route to the canonical PMTL skill first using `references/routing-map.md`.
3. Pair with Superpowers when the task needs workflow discipline such as brainstorming, plans, TDD, debugging, subagent execution, or review.
4. Add a global tool skill only when the task needs external tooling or platform-specific mechanics.
5. Finish by attaching the right verification skill before treating the task as complete.

## Quality Criteria

- Repo-local PMTL skills stay the source of truth for PMTL behavior.
- Superpowers stays generic and workflow-oriented.
- Global skills stay tool-oriented and do not override repo policy.
- Compatibility aliases are not the default routing target.

## Verification

- Recheck the selected path against `references/routing-map.md`.
- Confirm the task names at least one canonical PMTL skill when the task changes repo code or docs.
- Pair with `pmtl-verify-quality-gate` after meaningful repo changes.

## Edge Cases

- If the user explicitly names a legacy compatibility skill, honor it but prefer the canonical replacement in the final routing note.
- If the task is purely tool-driven such as browser automation, use the generic tool skill directly after confirming no PMTL repo policy is being changed.
- If the task is outside this repo, do not force PMTL skills.

## References

- `references/routing-map.md`
- `verification/checklist.md`
- `../pmtl-skill-governance/SKILL.md`
- `../../../docs/agent-cheatsheet.md`

