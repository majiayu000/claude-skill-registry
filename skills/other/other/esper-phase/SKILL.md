---
name: esper:phase
description: Define the next development phase. Archives the current phase's completed plans, bumps current_phase, interviews the user about the new phase scope, and creates a backlog of feature plans.
---

You are defining the next development phase.

The user's initial prompt (if any): $ARGUMENTS

## Step 1: Check setup

Run `esperkit config check`. If it exits non-zero, tell the user to run `/esper:init` first and stop.

Run `esperkit config get current_phase` to get the current phase (e.g. `"004-exploration-and-review-skills"`).

## Step 2: Verify current phase is complete

Run `esperkit plan list --dir pending --phase <current_phase> --format json` and `esperkit plan list --dir active --phase <current_phase> --format json`.

Check if any plans are returned.

If any matching plans remain, stop:
> "Phase <current_phase> still has unfinished plans. Complete them with `/esper:apply` and `/esper:finish` before starting a new phase."

## Step 3: Read context

Read:
- `.esper/CONSTITUTION.md` — project principles and scope
- `.esper/phases/<current_phase>.md` — what was just completed

For the retrospective summary of what was shipped:
- If the phase file contains a `## Shipped Plans` section, use it directly — it is already a compact per-plan summary.
- If the section is absent (older phase that predates this feature), fall back to: `esperkit plan list --dir done --phase <current_phase> --format json` and extract titles.

Summarize for the user: "Phase <N> (<title>) is complete. You shipped: [list from Shipped Plans or done list]."

## Step 3b: Read explorations

Run `esperkit exploration list --format json`. If the output is an empty array (`[]`), skip this step silently.

If explorations exist, list them for the user with their titles and a one-line summary from each file. Use `AskUserQuestion` to ask: "These explorations are on file. Which ones (if any) should inform this next phase?" Allow multi-select.

Selected explorations will be read in full and used as input during the interview and plan decomposition steps. After the phase is fully defined (Step 8), archive each selected exploration by running `esperkit exploration archive <filename>` so they don't resurface in future phases.

If no explorations exist, skip this step silently.

## Step 4: Interview for the new phase

Use `AskUserQuestion` in 2 rounds:

**Round 1 — Scope:**
- What does this next phase deliver? What is the goal?
- What is explicitly in scope for this phase?
- What is deferred (not this phase)?
- What are the acceptance criteria — how do we know this phase is done?

**Round 2 — Retrospective** (skip if $ARGUMENTS already covers these):
- Anything from the previous phase to revisit or carry forward?
- Any new technical constraints or architectural decisions for this phase?

## Step 5: Archive current phase plans

Run `esperkit plan archive <current_phase>` to move all done plans for the phase to `archived/<current_phase>/`.

Print: "Archived completed plans to `.esper/plans/archived/<current_phase>/`"

## Step 6: Compute the next phase number and update config

Parse `current_phase` to get the next phase number:
- Extract the zero-padded numeric prefix (e.g. `004` from `004-exploration-and-review-skills`)
- Increment by 1 and zero-pad to 3 digits (e.g. `004` → `005`)

The new phase slug will be `<NNN>-<kebab-slug>` where `<kebab-slug>` is derived from the phase title chosen during the interview (e.g. title "Better Testing" → `005-better-testing`).

Run `esperkit config set current_phase <new_phase>` to update the current phase.

## Step 7: Write the new phase file

Create `.esper/phases/<new_phase>.md` (e.g. `.esper/phases/005-better-testing.md`):

```markdown
---
phase: <new_phase>
title: <title from interview>
status: active
---

# Phase <N>: <title>

## Goal
[What this phase delivers and why it matters]

## In Scope
- [deliverable or feature]

## Out of Scope (deferred)
- [explicitly deferred item]

## Acceptance Criteria
- [ ] [measurable criterion]

## Phase Notes
[Retrospective findings from the previous phase that inform this one]
```

## Step 8: Decompose into backlog plans

Break the new phase into atomic tasks — each task is one PR worth of work.

All plans in this phase get:
- `type: "feature"` (for fix-type items, the user can run `/esper:fix` separately)
- `phase: <new_phase>`
- `branch: feature/<new_phase>`

Run `esperkit plan next-id` to get the next available plan ID. Continue incrementing for each subsequent plan.

Write `.esper/plans/pending/NNN-slug.md` for each plan:

```markdown
---
id: NNN
title: [task title]
status: pending
type: feature
priority: [1 = blocking, 2 = normal, 3 = low]
phase: <new_phase>
branch: feature/<new_phase>
created: [today YYYY-MM-DD]
---

# [Task title]

## Context
[What exists in the codebase relevant to this task]

## Approach
[Step-by-step implementation plan]

## Files to change
- [file path] ([create/modify] — [why])

## Verification
- Run: [test command or "manual"]
- Expected: [what passing looks like]
- Edge cases: [anything non-obvious]
```

Run `esperkit config get backlog_mode`. If the output is `github`, create ONE GitHub issue for the entire phase (not per plan — features are batched into one phase PR):
```bash
gh issue create --title "Phase <N>: <phase title>" --body "<phase goal and scope summary>"
```
Store the returned issue number as `gh_issue: <number>` in the phase file frontmatter (`.esper/phases/<new_phase>.md`).

Then, create sub-issues for each plan file written above:
```bash
esperkit plan create-sub-issue <filename>
```
This creates a GitHub issue for each plan and links it as a sub-issue of the phase's parent issue. Run this for every plan file created in Step 8.

## Step 9: Summary

Print:
- "Phase <N> defined: <title>"
- "<X> plans created in `.esper/plans/pending/`"
- Next steps: "Run `/esper:backlog` to review, then `/esper:apply` to start building."
