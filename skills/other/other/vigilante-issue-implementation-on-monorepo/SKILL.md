---
name: vigilante-issue-implementation-on-monorepo
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for a watched monorepo. Use the provided worktree, respect repository instructions, comment on the issue as work progresses, and report failures back to GitHub.
---

# Vigilante Monorepo Issue Implementation

## Overview
Implement one GitHub issue from Vigilante dispatch through validated code changes, a pushed branch, and an opened pull request from the provided worktree. Always work inside the assigned worktree, respect repository instructions, and keep the GitHub issue updated with start, plan, progress, PR, and failure comments.

## Monorepo Focus
- Read the repo/process context supplied in the prompt before changing code.
- Read the detected monorepo stack and shared local-service contract from the prompt before choosing commands.
- Limit edits to the packages, apps, or shared modules required for the issue.
- Prefer targeted validation for the touched workspace scope before broader monorepo validation.
- Avoid unrelated cross-package refactors unless they are required to complete the issue safely.

## Workflow
1. Inspect issue and repository constraints
- Read the issue details supplied by Vigilante and confirm the issue scope before coding.
- Read development constraints from repository markdown files before making changes:
  - `AGENTS.md` when present
  - `README.md`
  - other root or area-specific docs that affect touched files
- If repository instructions conflict, follow the more specific instruction.

2. Announce session start on GitHub
- Post a comment on the issue as soon as work begins using `vigilante gh issue comment`.
- Include that Vigilante launched the session, the working branch, and that implementation is in progress.

3. Post an implementation plan early
- After inspecting the issue and repository constraints, post a concise implementation plan to the issue using `vigilante gh issue comment`.
- The plan comment should describe the intended development steps before substantial coding work begins.

4. Implement inside the assigned worktree only
- Use only the provided worktree path.
- Never edit the root checkout when a worktree was assigned.
- Keep changes scoped to the issue.
- Prefer native repository tooling and avoid unnecessary new dependencies.
- If the affected workspace needs local services, call the bundled `vigilante-local-service-dependencies` skill and reuse its structured output before creating workspace-specific ad hoc service setup.
- When containerized local services are still needed after that analysis, use the shared `docker-compose-launch` contract from the prompt so service startup remains scoped to the assigned worktree.

5. Validate incrementally
- Run the most relevant package/app/workspace checks first, then expand only if needed.
- If validation fails, determine whether the problem is in the code, test setup, or environment before retrying.

6. Commit, push, and open a pull request
- Commit only issue-relevant changes in the assigned branch.
- Push the assigned branch to the remote.
- Open a pull request targeting the repository default branch unless repository instructions say otherwise.

7. Report progress and failures clearly
- Use `vigilante gh issue comment` for progress updates, milestone updates, PR creation, and execution failures.
- Keep comments concise, factual, and tied to real progress.
