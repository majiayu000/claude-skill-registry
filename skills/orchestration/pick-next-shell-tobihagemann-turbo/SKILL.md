---
name: pick-next-shell
description: "Pick the next shell whose dependencies are satisfied and carry it through planning: expand, refine, self-improve, halt. Use when the user asks to \"pick next shell\", \"next shell\", \"continue project\", \"what's next\", \"next implementation step\", or \"continue with the plan\"."
---

# Pick Next Shell

Pick the next shell from `.turbo/shells/` whose dependencies are satisfied, then carry it through the planning pipeline: expand → refine → self-improve → halt.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Scan shells and pick next
2. Run `/expand-shell` skill
3. Run `/refine-plan` skill
4. Run `/self-improve` skill
5. Mark plan ready
6. Summarize and halt

## Step 1: Scan Shells and Pick Next

Check terminal conditions first:

- **No shells and no plans** — nothing to pick; stop
- **No shells, but plans exist with `status: done` for all** — the project is complete; stop
- **No shells, but plans exist with a non-`done` status** — there are unfinished plans; stop

If shells exist in `.turbo/shells/`, glob `.turbo/shells/*.md` and read each file's YAML frontmatter. A shell's `depends_on` entry is satisfied when `.turbo/plans/<dep-slug>.md` exists with `status: done` in its frontmatter.

- **Candidates** — shells whose `depends_on` are all satisfied
- **Blocked** — shells with one or more unsatisfied `depends_on`

If there are no candidates (everything is blocked), report which shells are blocked and which dependencies they're waiting on, then stop.

If multiple candidates exist, pick the one with the lowest shell number (from the `NN-` prefix `/draft-shells` gives each file). If ambiguous, use `AskUserQuestion` to let the user choose.

State the picked shell path and its dependencies before continuing.

## Step 2: Run `/expand-shell` Skill

Run the `/expand-shell` skill, passing the shell file path. Capture the resulting plan path for Step 3.

## Step 3: Run `/refine-plan` Skill

Run the `/refine-plan` skill with the plan path from Step 2.

## Step 4: Run `/self-improve` Skill

Run the `/self-improve` skill to compound planning learnings.

## Step 5: Mark Plan Ready

Update the plan's YAML frontmatter to `status: ready`.

## Step 6: Summarize and Halt

Present a brief summary of the finished plan: the essence of what it builds and the key decisions behind it, short enough to read at a glance so the user does not have to open the full plan file. Fit the summary to the plan rather than a fixed template.

Then halt with this message:

> Plan ready at `<plan path>`.
>
> Planning context is likely full, and the plan is comprehensive enough to continue fresh. Run `/clear`, then `/implement-plan <slug>` to implement. After that, run `/pick-next-shell` again for the next shell.

## Rules

- Do not edit plan files directly. Revisions go through `/refine-plan`.
- Never modify the spec file.
- Do not attempt to auto-implement. The user drives implementation with `/implement-plan` in a fresh session.
- If a shell file is missing or has invalid frontmatter, halt and report.
