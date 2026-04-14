---
name: review-code
description: "Full code review: launches `/review-test-coverage`, `/review-correctness`, `/review-security`, `/review-quality`, `/review-api-usage`, and `/peer-review` in parallel and returns combined findings. Use when the user asks to \"review my code\", \"full code review\", \"review my changes\", or wants a comprehensive code review."
---

# Review Code

Run six AI code reviews in parallel and return combined findings.

## Step 1: Determine the Scope

Determine what to review:

- If a specific **diff command** was provided (e.g., `git diff --cached`), use that.
- If a **file list or directory** was provided, review those files directly.
- If **neither** was provided, default to diffing against the repository's default branch (detect via `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`).

## Step 2: Compose the Peer-Review Prompt

Read the SKILL.md of each review skill listed below and extract their review criteria and "what to look for" sections:

- `/review-test-coverage`
- `/review-correctness`
- `/review-security`
- `/review-quality`
- `/review-api-usage`

Compose a single comprehensive review prompt covering all dimensions with the diff command from Step 1. Be verbose about what to check so the peer reviewer has full context. Structure the prompt using `<task>`, `<dig_deeper_nudge>`, and `<structured_output_contract>` XML tags, consistent with the `/peer-review` interface.

## Step 3: Run Six Reviews in Parallel

Launch six Agent tool calls in a single message so they run concurrently (`model: "opus"`, do not set `run_in_background`). Each agent's prompt includes the scope from Step 1 and instructs it to invoke its assigned skill via the Skill tool:

- `/review-test-coverage`
- `/review-correctness`
- `/review-security`
- `/review-quality`
- `/review-api-usage`
- `/peer-review` — pass the pre-composed prompt from Step 2

## Step 4: Aggregate Combined Findings

Wait for all six agents to complete. Aggregate their findings with attribution (reviewer name, file path, description).

Check your task list for remaining tasks and proceed.

## Rules

- If any reviewer is unavailable or returns malformed output, proceed with findings from the remaining reviewers.
- Present findings in file order to minimize context switching.
