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
6. **Nothing found** — If no plan file exists, tell the user to run `/turboplan` (for a new task) or `/pick-next-plan-shell` (for existing shells) and stop

If multiple files exist and the most-recent choice is non-obvious (e.g., several plans were modified within the same minute), use `AskUserQuestion` to let the user pick from the candidates.

### Shell Detection

Read the file's YAML frontmatter. A file is a **draft shell** when it has `type: shell` and `status: draft`.

If the resolved file is a draft shell, halt with:

> `<path>` is a draft shell that needs expansion first. Run `/pick-next-plan-shell` to expand and implement it.

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

**If changes were made**, classify what Step 4 edited:

- **Structural edits** (added or removed steps, new or removed design decisions, rewired dependencies between steps, changed testing strategy) — run `/refine-plan` again via the Skill tool, passing the resolved plan path. If the round contains both structural and prose-only edits, treat it as structural and re-run automatically.
- **Prose-only edits only** (reworded sentences in place, fixed stale examples, clarified existing text without changing meaning) — output a summary of what changed, then use `AskUserQuestion` to ask whether to run one more round or stop here. Do not silently continue or silently stop.

**If changes were made but you believe re-running is unnecessary**, use `AskUserQuestion` to ask for skip permission. Do not skip silently.

**If this is iteration 3 and changes were still made**, the hard cap is reached. This replaces the classification gate above. Output a summary of what is still changing and whether it is structural or prose-only. Then use `AskUserQuestion` to offer three options: continue for another iteration, stop here and accept the plan as-is, or escalate to `/consult-oracle` for a different perspective on the remaining issues.

The re-invocation is a full, fresh run of this skill. Every step (1-5) executes with its own task tracking and skill invocations.

Check your task list for remaining tasks and proceed.

## Rules

- Every step must run in every iteration. `/evaluate-findings` is a judgment gate that must run before `/apply-findings` touches the plan. Each step must invoke its designated skill via the Skill tool.
- Re-invocations from Step 5 are full runs with fresh task tracking and complete skill invocations.
- The plan file is the only file that should change.
- If `/review-plan` returns no findings on the first pass, report the plan as stable and stop.
