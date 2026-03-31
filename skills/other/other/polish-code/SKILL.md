---
name: polish-code
description: "Stage, format, lint, test, simplify, review, smoke test, and re-run itself until stable. Use when the user asks to \"polish code\", \"refine code\", \"iterate on code quality\", \"simplify and review loop\", \"clean up, test, and review loop\", or \"run the polish loop\"."
---

# Polish Code

## Task Tracking

At the start of every invocation (including re-runs from Step 8), use `TaskCreate` to create a task for each step:

1. Run `/stage` skill
2. Deterministic cleanup
3. Run `/simplify-code` skill
4. Run `/review-code` skill
5. Run `/evaluate-findings` skill
6. Run `/apply-findings` skill
7. Run `/smoke-test` skill
8. Re-run `/polish-code` skill if changed

## Step 1: Run `/stage` Skill

Run the `/stage` skill.

## Step 2: Deterministic Cleanup

Run the project's formatter first, then the linter. Fix any lint errors or warnings that the formatter did not resolve. If the project has a combined format+lint script, use that.

Run the project's test suite to confirm nothing is broken. If tests fail, run the `/investigate` skill to diagnose the root cause, apply the suggested fix, and re-run tests. If investigation cannot identify a root cause, stop and report with investigation findings.

Stage all changes made in this step before continuing.

## Step 3: Run `/simplify-code` Skill

Run the `/simplify-code` skill. The diff command is `git diff --cached`.

Stage all changes made in this step before continuing.

## Step 4: Run `/review-code` Skill

Run the `/review-code` skill. The diff command is `git diff --cached`.

Always run this step even if Step 3 made no changes.

## Step 5: Run `/evaluate-findings` Skill

Run the `/evaluate-findings` skill on the results from Steps 3 and 4.

If zero actionable findings survive evaluation, skip to Step 7.

## Step 6: Run `/apply-findings` Skill

Run the `/apply-findings` skill on the evaluated results.

Stage all changes made in this step before continuing.

## Step 7: Run `/smoke-test` Skill

Run the `/smoke-test` skill to produce the smoke test plan. Delegate test execution to a subagent using the Agent tool (`model: "opus"`, do not set `run_in_background`). Pass the plan and the diff command (`git diff --cached`) to the subagent.

If any test fails, fix the issues and stage the fixes.

## Step 8: Re-run `/polish-code` Skill if Changed

Check whether any file was edited during Steps 3-7. Any edit counts, regardless of how small or mechanical it seems. A one-line doc comment fix, a renamed variable, a reformatted import, a smoke test fix — all count.

If any file was edited, run `/polish-code` again using the Skill tool. Scope the diff command to only the files modified in the previous iteration: use `git diff --cached -- <file1> <file2> ...` as the diff command for `/simplify-code` and `/review-code`. Smoke test scope remains unchanged (full feature scope, not file-narrowed). Cap at 3 total iterations (the initial run plus up to 2 additional runs) to prevent runaway loops.

The re-invocation is a full, fresh run of this skill. Every step (1-8) executes with its own task tracking and skill invocations. "Scoped to modified files" only affects the diff command passed to `/simplify-code` and `/review-code`. It does not affect which steps run or whether skills are invoked.

Do NOT:
- Skip steps because the changes are "minor", "mechanical", or "cleanup"
- Use the Agent tool to substitute for `/simplify-code`, `/review-code`, or any other skill
- Skip task tracking because "this is just iteration 2"
- Rationalize that review "would produce the same findings" or "has already been addressed"

## Rules

- Every step must run in every iteration. No change is "self-evidently correct" or "mechanical" enough to skip review. Simplify findings do not substitute for review. Passing tests do not substitute for lint. Each step catches different issues. Context window concerns are not a reason to skip steps. Never rationalize skipping a later step because an earlier step produced thorough results — each step uses distinct agents with non-overlapping review criteria, and "the prior step covered it" is always wrong. This applies equally to iteration 1 and all subsequent iterations.
- Never collapse steps 3–6 into fewer steps. `/simplify-code` and `/review-code` use different review agents with different focus areas — running one does NOT cover the other. `/evaluate-findings` is a judgment gate that must run before `/apply-findings` applies any changes. Each step must invoke its designated skill via the Skill tool, not be replaced by inline reasoning or agent calls that "seem equivalent."
- Re-invocations from Step 8 are full runs, not lighter-weight passes. See Step 8 for the anti-patterns that must be avoided.
