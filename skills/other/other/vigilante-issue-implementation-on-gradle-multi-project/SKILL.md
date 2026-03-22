---
name: vigilante-issue-implementation-on-gradle-multi-project
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for a watched Gradle multi-project repository. Use the provided worktree, respect repository instructions, comment on the issue as work progresses, and report failures back to GitHub.
---

# Vigilante Gradle Multi-Project Issue Implementation

## Overview
Implement one GitHub issue from Vigilante dispatch through validated code changes, a pushed branch, and an opened pull request from the provided worktree. Always work inside the assigned worktree, respect repository instructions, and keep the GitHub issue updated with start, plan, progress, PR, and failure comments.

## Gradle Multi-Project Focus
- Read the repo/process context supplied in the prompt before changing code.
- Use `settings.gradle` or `settings.gradle.kts`, included project names, and repo docs to identify the relevant Gradle subproject scope before editing.
- Prefer repo-defined Gradle tasks and existing module names over guessed task or path conventions.
- Keep implementation and validation scoped to the affected subproject(s) when possible, then expand only if shared code or integration boundaries require it.
- Avoid JS workspace assumptions that do not apply to Gradle repositories.

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
- The plan comment should describe the Gradle subproject scope and validation approach before substantial coding work begins.

4. Implement inside the assigned worktree only
- Use only the provided worktree path.
- Never edit the root checkout when a worktree was assigned.
- Keep changes scoped to the issue.
- Prefer native repository tooling and avoid unnecessary new dependencies.
- When local databases or other service-backed dependencies are required, call the bundled `vigilante-local-service-dependencies` skill before inventing ad hoc setup.
- If the repository expects `docker-compose-launch` for service-backed development or tests, use that repo-defined flow instead of replacing it with generic compose commands.

5. Validate incrementally
- Run the most relevant Gradle tasks for the affected subproject(s) first, such as repo-defined `test`, `check`, `build`, or narrower module tasks.
- Log the selected subproject(s) and Gradle task scope in issue progress updates when validation starts or changes.
- If validation fails, determine whether the problem is in the code, Gradle task selection, test setup, or environment before retrying.

6. Commit, push, and open a pull request
- Commit only issue-relevant changes in the assigned branch.
- Push the assigned branch to the remote.
- Open a pull request targeting the repository default branch unless repository instructions say otherwise.

7. Report progress and failures clearly
- Use `vigilante gh issue comment` for progress updates, milestone updates, PR creation, and execution failures.
- Keep comments concise, factual, and tied to real progress.
