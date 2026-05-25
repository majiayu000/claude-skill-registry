---
name: resolve-findings
description: "Choose an implementation path (direct or plan) for evaluated findings and dispatch it. Direct path applies fixes directly; plan path runs /turboplan. Use after /evaluate-findings has tagged findings and they need to be implemented, or when the user asks to \"resolve findings\", \"apply evaluated findings\", or \"dispatch findings to implementation\"."
---

# Resolve Findings

Choose a path for evaluated findings and run it. Direct path applies fixes directly; plan path runs `/turboplan`.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Choose path
2. Run the chosen path

## Step 1: Choose Path

Present a summary of accepted findings (Apply verdict): count by complexity (mechanical fixes vs. architectural or design changes). Then use `AskUserQuestion` to let the user choose:

- **Plan** — Run `/turboplan` for drafting, refinement, approval, implementation, and finalize
- **Direct** — Run `/apply-findings`, then `/finalize`

Suggest Plan when findings include complex or architectural changes. Suggest Direct when all findings are mechanical fixes.

## Step 2: Run the Chosen Path

Read the reference file for the confirmed path and follow its phases:

- **Direct path** — [references/direct-path.md](references/direct-path.md)
- **Plan path** — [references/plan-path.md](references/plan-path.md)

State the chosen path before continuing with the reference file.

Then use the TaskList tool and proceed to any remaining task.
