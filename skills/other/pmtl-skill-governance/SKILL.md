---
name: pmtl-skill-governance
description: PMTL_VN governance skill for designing, auditing, and evolving repo-local skills so they behave like reusable operational modules instead of one-off prompt notes.
---

# PMTL Skill Governance

## Purpose

Keep the PMTL skill system aligned with the repo taxonomy and the operating model `scope -> skill -> execute -> verify -> evolve`.

## Use When

- Creating a new repo-local skill.
- Auditing whether an existing skill is still only prompt prose.
- Consolidating overlapping skills or legacy aliases.
- Adding missing verification, templates, gotchas, or changelog notes to a skill.

## Required Inputs

- The target skill name or the subset of skills under review.
- The taxonomy slot the skill should belong to.
- The repeated task, failure mode, or workflow the skill must serve.

## Expected Output

- A skill folder with a usable `SKILL.md`.
- Supporting assets where needed: `references/`, `scripts/`, `templates/`, `verification/`, `examples/`.
- Evolution assets: `gotchas.md` and `changelog.md`.
- An audit result that shows what is still missing.

## Execution Approach

1. Confirm the taxonomy slot in `docs/architecture/skills-taxonomy.md`.
2. Start from `templates/SKILL.template.md` instead of free-writing a long prompt.
3. Add executable or reusable assets before adding more prose.
4. Attach a verification checklist and at least one evolution artifact.
5. Run `py infra/tools/codex_actions.py skill-audit` and record the gaps.

## Quality Criteria

- One skill owns one operational job.
- The folder contains enough context to reuse without re-explaining the task.
- Verification is explicit and repeatable.
- The skill teaches from past failures instead of forgetting them.
- Routing stays clear; new skills do not overlap existing taxonomy slots without a reason.

## Verification

- Run `py infra/tools/codex_actions.py skill-audit`.
- Check `verification/checklist.md` before treating the skill as complete.
- If the skill runs commands, prefer a wrapper in `scripts/` or `infra/tools/codex_actions.py`.

## Edge Cases

- Legacy compatibility skills may intentionally stay lighter than canonical skills.
- Design-library skills can keep dense references, but still need a clear trigger and routing note.
- If two skills overlap, merge or demote one to compatibility instead of keeping both canonical.

## References

- `templates/SKILL.template.md`
- `verification/checklist.md`
- `examples/sample-skill-outline.md`
- `gotchas.md`
- `changelog.md`
