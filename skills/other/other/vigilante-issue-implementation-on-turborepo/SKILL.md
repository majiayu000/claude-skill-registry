---
name: vigilante-issue-implementation-on-turborepo
description: Implement a GitHub issue end-to-end when Vigilante dispatches work for a pnpm/workspace-based Turborepo. Use the provided worktree, respect repository instructions, comment on the issue as work progresses, and report failures back to GitHub.
---

# Vigilante Turborepo Issue Implementation

## Overview
Implement one GitHub issue from Vigilante dispatch through validated code changes, a pushed branch, and an opened pull request from the provided worktree. Always work inside the assigned worktree, respect repository instructions, and keep the GitHub issue updated with start, plan, progress, PR, and failure comments.

## Turborepo Focus
- Read the repo/process context supplied in the prompt before changing code.
- Confirm the repository is Turborepo-shaped by checking for `turbo.json` plus workspace markers such as `pnpm-workspace.yaml` or root `package.json` workspaces.
- Select the smallest relevant workspace scope for the issue instead of working across the full monorepo by default.
- Prefer the app or package directly named in the issue; otherwise infer the most likely scope from touched routes, ownership docs, script names, and common roots such as `apps/*` and `packages/*`.
- State which workspace or workspaces were selected and why in progress comments or terminal summaries.

## Workspace Selection
- Inspect `turbo.json`, root `package.json`, `pnpm-workspace.yaml`, and the top-level workspace folders before making edits.
- Look for issue clues in app names, package names, paths, scripts, domain terms, and repository docs.
- If multiple workspaces are plausible, start with the narrowest one that can fully implement and validate the issue.
- Only expand to additional workspaces when shared packages, integration flows, or cross-app contracts make that necessary.

## Workflow
1. Inspect issue and repository constraints
- Read the issue details supplied by Vigilante and confirm the issue scope before coding.
- Read development constraints from repository markdown files before making changes:
  - `AGENTS.md` when present
  - `README.md`
  - workspace-level docs for the selected app/package when present
- If repository instructions conflict, follow the more specific instruction.

2. Announce session start on GitHub
- Post a comment on the issue as soon as work begins using `vigilante gh issue comment`.
- Include that Vigilante launched the session, the working branch, and that implementation is in progress.

3. Post an implementation plan early
- After inspecting the issue and repository constraints, post a concise implementation plan to the issue using `vigilante gh issue comment`.
- Mention the initial workspace target or the short list of candidate workspaces when that scope is already known.

4. Implement inside the assigned worktree only
- Use only the provided worktree path.
- Never edit the root checkout when a worktree was assigned.
- Keep changes scoped to the issue.
- Prefer repo-defined scripts and Turborepo tasks over invented command sequences.
- Use workspace-aware commands such as `pnpm --filter <workspace> ...`, workspace-local scripts, or `turbo run <task> --filter=<workspace>` instead of repo-wide commands when possible.
- If the selected workspace needs local database services, call the bundled `vigilante-local-service-dependencies` skill before ad hoc setup, and use `docker-compose-launch` when the repository exposes that flow.

5. Validate incrementally
- Run the smallest relevant workspace-aware checks first for install, lint, build, test, typecheck, or app verification.
- Prefer commands already defined in `package.json`, workspace manifests, or `turbo.json`.
- Expand validation scope only when the changed package affects shared dependencies, downstream apps, or integration behavior.
- If validation fails, determine whether the problem is in the code, test setup, or environment before retrying.

6. Commit, push, and open a pull request
- Commit only issue-relevant changes in the assigned branch.
- Push the assigned branch to the remote.
- Open a pull request targeting the repository default branch unless repository instructions say otherwise.

7. Report progress and failures clearly
- Use `vigilante gh issue comment` for progress updates, milestone updates, PR creation, and execution failures.
- Keep comments concise, factual, and tied to real progress.
- Include the selected workspace scope in milestone updates when that information helps reviewers follow the implementation.
