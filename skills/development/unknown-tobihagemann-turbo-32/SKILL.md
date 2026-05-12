---
name: implement
description: "Load code-style rules, make the change described by the current context, then run /finalize for QA and commit. Use for ad-hoc changes when no plan file or improvements backlog governs the work, and when the user asks to \"just implement\", \"implement directly\", \"implement without a plan\", or \"apply the change\"."
---

# Implement

Standard implementation flow: load style rules, make the change, run post-implementation QA.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Run `/code-style` skill
2. Make the change
3. Run verification
4. Run `/finalize` skill

## Step 1: Run `/code-style` Skill

Run the `/code-style` skill to load mirror, reuse, and symmetry rules before editing.

## Step 2: Make the Change

Apply the change described by the current context — the user request, a prior skill's task description, or an improvement entry. Keep the edit scoped to what the context describes. If the scope balloons beyond what the context specified, stop and confirm scope before continuing.

## Step 3: Run Verification

If a Verification section is in conversation context (e.g., from a plan file), execute the commands, smoke checks, or MCP tool invocations it specifies. If a check fails, run the `/investigate` skill. If a check is blocked by a dependency, unclear requirement, or environmental issue, use `AskUserQuestion` to surface the blocker and let the user choose how to proceed. If no Verification section is in context, skip this step.

## Step 4: Run `/finalize` Skill

Run the `/finalize` skill.

Then use the TaskList tool and proceed to any remaining task.

## Rules

- Defer `git commit`, `git push`, and PR creation to Step 4.
- Don't reference `.turbo/` content (filenames, IDs, headings) in code or comments. `.turbo/` is gitignored, so these references would be opaque to anyone reading without local copies.
