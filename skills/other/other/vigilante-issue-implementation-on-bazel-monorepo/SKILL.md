---
name: vigilante-issue-implementation-on-bazel-monorepo
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for a Bazel-based monorepo. Use the provided worktree, respect repository instructions, comment on the issue as work progresses, and report failures back to GitHub.
---

# Vigilante Bazel Monorepo Issue Implementation

## Overview
Implement one GitHub issue from Vigilante dispatch through validated code changes, a pushed branch, and an opened pull request from the provided worktree. Always work inside the assigned worktree, respect repository instructions, and keep the GitHub issue updated with start, plan, progress, PR, and failure comments.

## Bazel Focus
- Read the repo/process context supplied in the prompt before changing code, especially Bazel markers and package-root hints.
- Work in terms of Bazel packages and targets rather than generic workspace or repo-wide commands.
- Choose the smallest explainable Bazel target scope that covers the files you touched, then widen only if validation or dependency structure requires it.
- Log which Bazel target or package scope you selected and why.
- Avoid blanket repo-wide Bazel validation unless it is truly required to prove the change.

## Workflow
1. Inspect issue and repository constraints
- Read the issue details supplied by Vigilante and confirm the issue scope before coding.
- Read development constraints from repository markdown files before making changes:
  - `AGENTS.md` when present
  - `README.md`
  - Bazel docs, developer docs, and package-local docs that affect the touched targets
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
- Keep changes scoped to the Bazel packages and source files required for the issue.
- Prefer repo-native Bazel commands such as `bazel test`, `bazel build`, `bazel run`, or documented wrappers.
- If the affected app or test flow needs local database services, invoke `docker-compose-launch` when the repository expects it, or call the bundled `vigilante-local-service-dependencies` skill before inventing ad hoc setup.

5. Validate incrementally
- Start with the smallest relevant Bazel target, package pattern, or documented wrapper command for the touched area.
- Expand to closely related targets only when the first target scope is insufficient or shared code requires it.
- If validation fails, determine whether the problem is in the code, target selection, test setup, or environment before retrying.

6. Commit, push, and open a pull request
- Commit only issue-relevant changes in the assigned branch.
- Push the assigned branch to the remote.
- Open a pull request targeting the repository default branch unless repository instructions say otherwise.

7. Report progress and failures clearly
- Use `vigilante gh issue comment` for progress updates, milestone updates, PR creation, and execution failures.
- Keep comments concise, factual, and tied to real progress.
