---
name: pick-next-shell
description: "Pick the next shell whose dependencies are satisfied and carry it through planning and implementation: expand, refine, self-improve, implement. Use when the user asks to \"pick next shell\", \"next shell\", \"continue project\", \"what's next\", \"next implementation step\", or \"continue with the plan\"."
---

# Pick Next Shell

Pick the next shell from `.turbo/shells/` whose dependencies are satisfied, then carry it through expansion and implementation: expand → refine → self-improve → implement.

## Task Tracking

At the start, use `update_plan` to track each step:

1. Scan shells and pick next
2. Run `$expand-shell` skill
3. Run `$refine-plan` skill
4. Run `$self-improve` skill
5. Mark plan ready
6. Run `$implement-plan` skill

## Step 1: Scan Shells and Pick Next

Check terminal conditions first:

- **No shells and no plans** — nothing to pick; stop
- **No shells, but plans exist with `status: done` for all** — the project is complete; stop
- **No shells, but plans exist with a non-`done` status** — there are unfinished plans; stop

If shells exist in `.turbo/shells/`, glob `.turbo/shells/*.md` and read each file's YAML frontmatter. A shell's `depends_on` entry is satisfied when `.turbo/plans/<dep-slug>.md` exists with `status: done` in its frontmatter.

- **Candidates** — shells whose `depends_on` are all satisfied
- **Blocked** — shells with one or more unsatisfied `depends_on`

If there are no candidates (everything is blocked), report which shells are blocked and which dependencies they're waiting on, then stop.

If multiple candidates exist, pick the one with the lowest shell number (from the `NN-` prefix `$draft-shells` gives each file). If ambiguous, use `request_user_input` to let the user choose.

State the picked shell path and its dependencies before continuing.

## Step 2: Run `$expand-shell` Skill

Run the `$expand-shell` skill, passing the shell file path. Capture the resulting plan path for Step 3.

## Step 3: Run `$refine-plan` Skill

Run the `$refine-plan` skill with the plan path from Step 2.

## Step 4: Run `$self-improve` Skill

Run the `$self-improve` skill to compound planning learnings.

## Step 5: Mark Plan Ready

Update the plan's YAML frontmatter to `status: ready`.

## Step 6: Run `$implement-plan` Skill

Present a brief summary of the finished plan: the essence of what it builds and the key decisions behind it, short enough to read at a glance so the user does not have to open the full plan file. When the plan delivers user-facing value, also present a short list of user stories capturing what someone gains from it. Skip the stories for changes with no user-facing gain, such as internal refactors or infrastructure work. Fit both to the plan rather than a fixed template.

Then run the `$implement-plan` skill with the plan path from Step 2.

Then update or check the active plan and proceed to any remaining task.

## Rules

- Do not edit plan files directly. Revisions go through `$refine-plan`.
- Never modify the spec file.
- If a shell file is missing or has invalid frontmatter, halt and report.
