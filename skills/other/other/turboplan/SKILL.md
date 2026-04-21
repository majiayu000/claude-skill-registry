---
name: turboplan
description: "Analyze task complexity and route to a mode: direct fix for trivial edits, plan file for small tasks, or spec and shells for complex projects. Use when the user asks to \"turboplan\", \"run turboplan\", \"plan this task\", \"turbo plan mode\", \"plan and implement\", or \"use turboplan instead of plan mode\"."
---

# Turboplan

Analyze task complexity and route to an execution mode.

Categorize the user-supplied task along these dimensions using subjective judgment:

- **Scope**: single feature / single subsystem vs multi-feature / multi-subsystem
- **Stakes**: one-off change vs long-lived project with architectural implications
- **Unknowns**: clear approach vs needs exploration and product decisions

Route to one of four outcomes:

| Category | Criteria | Route |
|---|---|---|
| **Trivial** | A true one-line edit: typo fix, single rename, single config tweak. | Read [references/trivial-mode.md](references/trivial-mode.md) and follow its steps. |
| **Small** | Fits a single implementation session, touches one or two related subsystems, no major architectural decisions left. | Read [references/small-task-mode.md](references/small-task-mode.md) and follow its steps. |
| **Complex** | Spans multiple subsystems, requires multiple implementation sessions, or has architectural decisions that need a spec-level discussion before planning begins. | Read [references/complex-project-mode.md](references/complex-project-mode.md) and follow its steps. |
| **Borderline** | Falls between two categories. | Use `AskUserQuestion` to confirm the route, then proceed as above. |

State the chosen route before continuing with the reference file.

## Rules

- Diff size, perceived task simplicity, and context window concerns are not reasons to skip the chosen mode's phases.
