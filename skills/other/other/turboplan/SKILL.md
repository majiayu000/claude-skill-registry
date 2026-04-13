---
name: turboplan
description: "Analyze task complexity and route to a planning mode. Produces a plan file at .turbo/plans/<slug>.md. Use when the user asks to \"turboplan\", \"run turboplan\", \"plan this task\", \"turbo plan mode\", \"plan and implement\", or \"use turboplan instead of plan mode\"."
---

# Turboplan

Analyze task complexity and route to a planning mode.

Categorize the user-supplied task along these dimensions using subjective judgment:

- **Scope**: single feature / single subsystem vs multi-feature / multi-subsystem
- **Stakes**: one-off change vs long-lived project with architectural implications
- **Unknowns**: clear approach vs needs exploration and product decisions

Route to one of four outcomes:

| Category | Criteria | Route |
|---|---|---|
| **Trivial** | A true one-line edit: typo fix, single rename, single config tweak. | Tell the user turboplan is overkill and suggest editing directly. Halt. |
| **Small** | Fits a single implementation session, touches one or two related subsystems, no major architectural decisions left. | Read [references/small-task-mode.md](references/small-task-mode.md) and follow its steps. |
| **Complex** | Spans multiple subsystems, requires multiple implementation sessions, or has architectural decisions that need a spec-level discussion before planning begins. | Read [references/complex-project-mode.md](references/complex-project-mode.md) and follow its steps. |
| **Borderline** | Falls between two categories. | Use `AskUserQuestion` to confirm the route, then proceed as above. |

State the chosen route before handing off to the reference file.

## Rules

- Diff size, perceived task simplicity, and context window concerns are not reasons to skip the chosen mode's phases.
