---
name: refine-prompt-plan
description: "Iteratively review and revise a prompt plan until no new findings survive evaluation. Runs /review-prompt-plan, /evaluate-findings, /apply-findings, then re-runs itself until stable. Use when the user asks to \"refine the prompt plan\", \"refine this prompt plan\", \"iterate on the prompt plan\", \"tighten the prompt plan\", or \"improve the prompt plan\"."
---

# Refine Prompt Plan

Loop the prompt plan review pipeline over a prompt plan index and its shell files until no new findings are accepted. Writes back to the index and shell files in place.

## Task Tracking

At the start of every invocation (including re-runs from Step 5), use `TaskCreate` to create a task for each step:

1. Resolve the prompt plan
2. Run `/review-prompt-plan` skill
3. Run `/evaluate-findings` skill
4. Run `/apply-findings` skill
5. Re-run `/refine-prompt-plan` skill if changed

## Step 1: Resolve the Prompt Plan

Determine which prompt plan index to refine using these rules in order:

1. **Explicit path** — If an absolute or relative path was passed, use it
2. **Explicit slug** — If a slug was passed, resolve to `.turbo/prompt-plans/<slug>.md`
3. **Single file** — Glob `.turbo/prompt-plans/*.md`. If exactly one file exists, use it
4. **Most recent** — If multiple files exist, use the most recently modified
5. **Legacy fallback** — If `.turbo/prompt-plans/` does not exist but `.turbo/prompts.md` exists, use it
6. **Nothing found** — If no prompt plan exists, tell the user to run `/draft-prompt-plan` first and stop

If multiple files exist and the most-recent choice is non-obvious (e.g., several prompt plans were modified within the same minute), use `AskUserQuestion` to let the user pick from the candidates.

Read the resolved index file and extract:

- All shell file paths from `Shell:` fields
- The source spec path from the `Source:` field

Verify that all shell files and the source spec exist. State the resolved index path, the number of shells, and the source spec path before continuing.

## Step 2: Run `/review-prompt-plan` Skill

Run the `/review-prompt-plan` skill, passing the index path. It reads the index, all shells, and the source spec, then checks wiring invariants (Produces, Consumes, Covers Spec Requirements) across all shells and returns combined findings.

Always run this step even if the prompt plan looks polished.

## Step 3: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the review findings from Step 2.

If zero actionable findings survive evaluation, skip to the end and report the prompt plan as stable.

## Step 4: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results. Target files are the index and/or shell files resolved in Step 1. Apply accepted findings by editing the affected files in place.

## Step 5: Re-run `/refine-prompt-plan` Skill if Changed

Check whether any prompt plan file (index or shells) was edited during Step 4. Any edit to any file counts.

**If changes were made**, run `/refine-prompt-plan` again using the Skill tool, passing the resolved index path.

**If changes were made but you believe re-running is unnecessary**, use `AskUserQuestion` to ask for skip permission. Do not skip silently.

**If this is iteration 3 and changes were still made**, the hard cap is reached. Use `AskUserQuestion` to tell the user that 3 iterations were not enough to stabilize, summarize what is still changing, and offer two options: continue for another iteration, or escalate to `/consult-oracle` for a different perspective on the remaining issues.

The re-invocation is a full, fresh run of this skill. Every step (1-5) executes with its own task tracking and skill invocations.

## Rules

- Every step must run in every iteration. `/evaluate-findings` is a judgment gate that must run before `/apply-findings` touches the prompt plan. Each step must invoke its designated skill via the Skill tool.
- Re-invocations from Step 5 are full runs with fresh task tracking and complete skill invocations.
- The index and shell files are the only files that should change. Do not modify the source spec.
- If `/review-prompt-plan` returns no findings on the first pass, report the prompt plan as stable and stop.
