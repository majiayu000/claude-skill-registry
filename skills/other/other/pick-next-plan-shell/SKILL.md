---
name: pick-next-plan-shell
description: "Pick the next ready plan shell and carry it through planning: expand, refine, self-improve, halt. Use when the user asks to \"pick next plan shell\", \"next shell\", \"continue project\", \"what's next\", \"next implementation step\", or \"continue with the plan\"."
---

# Pick Next Plan Shell

Pick the next draft plan shell from `.turbo/plans/` by reading YAML frontmatter, then carry it through the planning pipeline: expand → refine → self-improve → halt.

## Task Tracking

At the start, use `TaskCreate` to create a task for each step:

1. Scan shells and pick next
2. Run `/expand-plan-shell` skill
3. Run `/refine-plan` skill
4. Run `/self-improve` skill
5. Halt with next-step instructions

## Step 1: Scan Shells and Pick Next

Glob `.turbo/plans/*.md` and read each file's YAML frontmatter. Filter to files with `type: shell`. Categorize each shell:

- **Draft** — `status: draft`. Candidate if all `depends_on` entries have `status: done`.
- **Ready** — `status: ready`. Already expanded. Re-enter the pipeline at Step 3 (refine).
- **In-progress** — `status: in-progress`. Implementation started. Suggest running `/implement-plan` with its path and stop.
- **Done** — `status: done`. Completed. Skip.

**Priority order for picking:**

1. Any shell with `status: ready` — re-enter at Step 3
2. Any shell with `status: draft` whose `depends_on` are all `done` — start at Step 2
3. Nothing actionable — see terminal conditions below

If multiple candidates exist at the same priority level, pick the one with the lowest shell number (from the `NN` in the filename). If ambiguous, use `AskUserQuestion` to let the user choose.

State the picked shell path, its status, and dependencies before continuing.

**If no shell files exist**, tell the user to run `/turboplan` for a new task (which routes to `/draft-spec` + `/draft-plan-shells` for complex projects) and stop.

**If all shells are `done`**, report completion:

> All shells are done. The project is complete.

**If remaining shells are blocked**, report which shells are blocked and which dependencies they're waiting on.

## Step 2: Run `/expand-plan-shell` Skill

Run the `/expand-plan-shell` skill, passing the shell file path. `/expand-plan-shell` sets the shell's status to `ready` on completion.

## Step 3: Run `/refine-plan` Skill

Run the `/refine-plan` skill, passing the expanded plan path. Loops until the plan stabilizes.

## Step 4: Run `/self-improve` Skill

Run the `/self-improve` skill to compound planning learnings.

## Step 5: Halt with Next-Step Instructions

Halt with this message:

> Plan ready at `<plan path>`.
>
> Planning context is likely full, and the plan is comprehensive enough to continue fresh. Run `/clear`, then `/implement-plan <slug>` to implement. After that, run `/pick-next-plan-shell` again for the next shell.

## Rules

- For draft shells, all pipeline steps run. Ready shells re-enter at Step 3, skipping Step 2.
- Do not edit plan files directly. Revisions go through `/refine-plan` or `/expand-plan-shell`.
- Never modify the spec file.
- Do not pre-verify Consumes or refresh surveys here. `/expand-plan-shell` handles that.
- Do not attempt to auto-implement. The user drives implementation with `/implement-plan` in a fresh session.
- If a shell file is missing or has invalid frontmatter, halt and report.
