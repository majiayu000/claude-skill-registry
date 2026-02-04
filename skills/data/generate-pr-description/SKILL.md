---
name: generate-pr-description
description: Generate a structured PR description from the diff. Fetches the diff, analyzes changes, and optionally applies the description.
user-invocable: true
arguments: "<PR number or URL>"
---

# Generate PR Description

Generate a structured pull request description by analyzing the diff.

## Steps

1. Fetch the PR diff using `gh pr diff <PR>`.
2. Fetch the PR title using `gh pr view <PR> --json title --jq .title`.
3. Analyze the diff and generate a description with these sections:
   - **## Summary** — 1-2 sentences on purpose and motivation
   - **## Changes** — bulleted list of logical changes
   - **## Testing** — suggested verification steps
4. Show the generated description to the user.
5. Ask the user if they want to apply it to the PR.
6. If confirmed, apply via `gh pr edit <PR> --body "<description>"`.

## Guidelines

- Keep descriptions under 500 words
- Use present tense ("Add", "Fix", "Update")
- Focus on intent and impact, not line-by-line details
- Do not repeat the PR title — provide additional context
