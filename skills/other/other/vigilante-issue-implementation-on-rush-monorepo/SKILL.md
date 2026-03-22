---
name: vigilante-issue-implementation-on-rush-monorepo
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for a watched Rush monorepo. Use the provided worktree, respect repository instructions, comment on the issue as work progresses, and report failures back to GitHub.
---

# Vigilante Rush Monorepo Issue Implementation

## Overview
Implement one GitHub issue from Vigilante dispatch through validated code changes, a pushed branch, and an opened pull request from the provided worktree. Always work inside the assigned worktree, respect repository instructions, and keep the GitHub issue updated with start, plan, progress, PR, and failure comments.

## Rush Focus
- Read the repo/process context supplied in the prompt before changing code.
- Confirm Rush signals such as `rush.json`, project folders, and workspace roots before choosing commands.
- Identify the smallest affected package or app scope first and keep that scope explicit in validation and progress updates.
- Prefer Rush-native commands and repo-defined scripts over generic workspace guesses.
- If the affected package or app needs local services, call the bundled `vigilante-local-service-dependencies` skill and prefer the repository's `docker-compose-launch` flow when it exists.

## Workflow
1. Inspect issue and repository constraints
- Read the issue details supplied by Vigilante and confirm the issue scope before coding.
- Read development constraints from repository markdown files before making changes:
  - `AGENTS.md` when present
  - `README.md`
  - other root or package-specific docs that affect touched files
- If repository instructions conflict, follow the more specific instruction.

2. Announce session start on GitHub
- Post a comment on the issue as soon as work begins using `vigilante gh issue comment`.
- Include that Vigilante launched the session, the working branch, and that implementation is in progress.

3. Post an implementation plan early
- After inspecting the issue and repository constraints, post a concise implementation plan to the issue using `vigilante gh issue comment`.
- The plan comment should name the likely Rush package or app scope when it is already clear, or state that scope detection is the next step.

4. Implement inside the assigned worktree only
- Use only the provided worktree path.
- Never edit the root checkout when a worktree was assigned.
- Keep changes scoped to the issue.
- Prefer native repository tooling and avoid unnecessary new dependencies.
- When multiple Rush projects exist, determine the relevant package or app before making broad edits.

5. Validate incrementally with Rush-compatible commands
- Prefer targeted Rush validation for the affected package or app, such as repo-defined `rush test`, `rush build`, `rushx`, phased commands, or package-level scripts invoked through Rush-compatible flows.
- Avoid full-repo validation unless the repository workflow requires it or targeted validation is unavailable.
- If validation fails, determine whether the problem is in the code, test setup, or environment before retrying.

6. Commit, push, and open a pull request
- Commit only issue-relevant changes in the assigned branch.
- Push the assigned branch to the remote.
- Open a pull request targeting the repository default branch unless repository instructions say otherwise.

7. Report progress and failures clearly
- Use `vigilante gh issue comment` for progress updates, milestone updates, PR creation, and execution failures.
- Keep comments concise, factual, and tied to real progress.
