---
name: refine-plan
description: "Iteratively review and revise an implementation plan until no new findings survive evaluation. Runs /review-plan, /evaluate-findings, /apply-findings, then re-runs itself until stable. Use when the user asks to \"refine the plan\", \"refine this plan\", \"iterate on the plan\", \"tighten the plan\", or \"improve the plan\"."
---

# Refine Plan

Loop the plan review pipeline over a plan file until no new findings are accepted. Writes back to the plan file in place.

## Task Tracking

At the start of every invocation (including re-runs from Step 5), use `TaskCreate` to create a task for each step:

1. Resolve the plan file
2. Run `/review-plan` skill
3. Run `/evaluate-findings` skill
4. Run `/apply-findings` skill
5. Re-run `/refine-plan` skill if changed

## Step 1: Resolve the Plan File

Determine which plan file to refine using these rules in order:

1. **Explicit path** — If an absolute or relative path was passed, use it
2. **Explicit slug** — If a slug was passed (e.g., `add-image-cache`), resolve to `.turbo/plans/<slug>.md`
3. **Single file** — Glob `.turbo/plans/*.md`, excluding shell files (see shell detection below). If exactly one non-shell file exists, use it
4. **Most recent** — If multiple non-shell files exist, use the most recently modified
5. **Legacy fallback** — If `.turbo/plans/` does not exist but `.turbo/plan.md` exists, use it
6. **Nothing found** — If no plan file exists, tell the user to run `/turboplan` (for a new task) or `/pick-next-prompt` (for an existing prompt plan) and stop

If multiple files exist and the most-recent choice is non-obvious (e.g., several plans were modified within the same minute), use `AskUserQuestion` to let the user pick from the candidates.

### Shell Detection

A file is a **shell** when it contains `## Produces`, `## Consumes`, and `## Covers Spec Requirements` AND does NOT contain `## Pattern Survey`.

If the resolved file is a shell, halt with:

> `<path>` is a shell plan from `/draft-prompt-plan`. Run `/pick-next-prompt` to expand it before refining.

State the resolved plan path before continuing.

## Step 2: Run `/review-plan` Skill

Run the `/review-plan` skill on the resolved plan file. Pass the full plan text.

Always run this step even if the plan looks polished.

## Step 3: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the review findings from Step 2.

If zero actionable findings survive evaluation, skip to the end and report the plan as stable.

## Step 4: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results. The target file is the plan file resolved in Step 1. Apply accepted findings by editing the plan in place.

## Step 5: Re-run `/refine-plan` Skill if Changed

Check whether the plan file was edited during Step 4. Any edit counts.

**If changes were made**, run `/refine-plan` again using the Skill tool, passing the resolved plan path.

**If changes were made but you believe re-running is unnecessary**, use `AskUserQuestion` to ask for skip permission. Do not skip silently.

**If this is iteration 3 and changes were still made**, the hard cap is reached. Use `AskUserQuestion` to tell the user that 3 iterations were not enough to stabilize, summarize what is still changing, and offer two options: continue for another iteration, or escalate to `/consult-oracle` for a different perspective on the remaining issues.

The re-invocation is a full, fresh run of this skill. Every step (1-5) executes with its own task tracking and skill invocations.

## Rules

- Every step must run in every iteration. `/evaluate-findings` is a judgment gate that must run before `/apply-findings` touches the plan. Each step must invoke its designated skill via the Skill tool.
- Re-invocations from Step 5 are full runs with fresh task tracking and complete skill invocations.
- The plan file is the only file that should change.
- If `/review-plan` returns no findings on the first pass, report the plan as stable and stop.
