---
name: review-code
description: "Full code review: launches `/review-test-coverage`, `/review-correctness`, `/review-security`, `/review-quality`, `/review-api-usage`, and `/peer-review-code` in parallel and returns combined findings. Use when the user asks to \"review my code\", \"full code review\", \"review my changes\", or wants a comprehensive code review."
---

# Review Code

Run six AI code reviews in parallel and return combined findings.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`), use that.
- If a **file list or directory** was provided, review those files directly.
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`).

## Step 2: Run Six Reviews in Parallel

Launch one agent per skill in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`). Each agent runs its assigned skill with the scope from Step 1:

- `/review-test-coverage`
- `/review-correctness`
- `/review-security`
- `/review-quality`
- `/review-api-usage`
- `/peer-review-code`

## Step 3: Return Combined Findings

Wait for all six agents to complete. Aggregate their findings with attribution (reviewer name, file path, description) and return them to the caller.

The caller determines what to do with the findings (evaluate, apply, or present to the user).

## Rules

- If any reviewer is unavailable or returns malformed output, proceed with findings from the remaining reviewers.
- Present findings in file order to minimize context switching.
