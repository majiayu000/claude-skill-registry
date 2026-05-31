---
name: turboplan
description: "Analyze task complexity and route to a mode by artifact: direct fix for clear-scope changes, plan file when the approach needs to be written down, or spec and shells for multi-session projects. Use when the user asks to \"turboplan\", \"run turboplan\", \"plan this task\", \"turbo plan mode\", \"plan and implement\", or \"use turboplan instead of plan mode\"."
---

# Turboplan

Analyze task complexity and route to an execution mode.

Categorize the user-supplied task along these dimensions using subjective judgment:

- **Scope**: single feature / single subsystem vs multi-feature / multi-subsystem
- **Stakes**: one-off change vs long-lived project with architectural implications
- **Unknowns**: clear approach vs needs exploration and product decisions

Route to one of three modes (or disambiguate when borderline).

Modes are named by what they produce: no plan, a plan file, or a spec plus shells.

| Mode | Criteria | Route |
|---|---|---|
| **Direct** | Clear scope and a known approach, ready to implement. Goes straight to `/implement`. | Read [references/direct-mode.md](references/direct-mode.md) and follow its steps. |
| **Plan** | The approach warrants writing down before implementing — to survey patterns, align with the user, or survive a fresh session. Fits a single implementation session and touches one or two related subsystems. Produces a plan file. | Read [references/plan-mode.md](references/plan-mode.md) and follow its steps. |
| **Spec** | Spans multiple subsystems, requires multiple implementation sessions, or has architectural decisions that need a spec-level discussion before planning begins. Produces a spec plus shells. | Read [references/spec-mode.md](references/spec-mode.md) and follow its steps. |
| **Borderline** | Falls between two modes. | Use `AskUserQuestion` to confirm the route, then proceed as above. |

State the chosen route before continuing with the reference file.

## Rules

- Diff size, perceived task simplicity, and context window concerns are not reasons to skip the chosen mode's phases.
