---
name: draft-plan
description: "Produce an implementation plan at .turbo/plans/<slug>.md. Use when the user asks to \"draft a plan\", \"draft the plan\", \"write an implementation plan\", \"plan this change\", \"create an implementation plan\", \"fill in the shell\", \"expand the shell\", or needs a first-draft plan file before refinement."
---

# Draft Plan

Produce an implementation plan at `.turbo/plans/<slug>.md`.

If a **shell file path** was passed, read [references/fill-in-mode.md](references/fill-in-mode.md) and follow its steps. Otherwise, read [references/full-mode.md](references/full-mode.md) and follow its steps.

## Rules

- Never skip the pattern survey.
- Never skip decision escalation before drafting.
- The plan file is the only output. Do not write code, scaffolding, or other project files.
- Do not run `/review-plan` or any review skills here.
- Do not embed task tracking, skill loading, or `/finalize` invocation in the plan file.
