---
name: cp
description: Local verify-commit-push wrapper for Codex. Use only when the user explicitly says `/cp` or clearly asks to finish the current work by running the relevant local checks, staging intended files explicitly, committing on the current branch, and pushing. This workflow may commit directly to `main` or `master` when that is the repo's chosen operating model.
---

# Cp

Use this as a thin finish mode after implementation is done.

`cp` is the local gate before push: verify first, then commit and push the intended changes on the current branch.

## Default Flow

1. Inspect:
- `git status`
- current branch
- intended files for this task
- recent commit message style if needed
2. Run the closest local verification to the repo's normal safety checks before committing.
- Prefer repo-native commands over invented ones.
- Prefer the narrowest safe checks first: changed-file lint/format checks, affected package tests, or targeted builds.
- If the repo's only reliable gate is broader, run the broader command.
3. If a broad local check fails because of unrelated dirty files outside the intended change set, stop and report that clearly instead of fixing or staging those unrelated files.
4. Stage only the intended files explicitly.
5. If a commit message was not provided, generate a concise conventional commit message that matches the repo style.
6. Commit on the current branch.
- Committing directly to `main` or `master` is allowed when that is the repo or user's chosen workflow.
- If the repo explicitly requires short-lived branches, follow that instead.
7. Push the current branch.
- If upstream is missing, push with upstream tracking.

## Rules

- Never use `git add .`, `git add -A`, or similar broad staging.
- Never commit unrelated local changes from other tasks or sessions.
- Never commit secrets, `.env` files, credentials, or generated noise by accident.
- Never silently skip verification; state what ran and what was skipped.
- Never force push unless the user explicitly asks for it.
- Do not create or require a PR unless the user explicitly asks for one.

## Good Targets

- "/cp"
- "커밋하고 푸시해줘"
- "메인에 올려"
- "이제 검증하고 바로 푸시해"

## Avoid

- Do not use this for "just commit" or "just push" if the user clearly asked for only one of those actions.
- Do not infer permission to push a different branch than the current one.
- Do not hide skipped or excluded files; mention them briefly if they matter.

## Finish

Return:
- branch pushed
- verification run or skipped
- commit message
- commit hash
- intentionally excluded files if any
