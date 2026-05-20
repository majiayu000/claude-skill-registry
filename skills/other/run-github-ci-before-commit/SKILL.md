---
name: run-github-ci-before-commit
description: Use when preparing to commit or push code and you must satisfy GitHub Actions CI requirements first. Enforce repository-scoped pre-commit checks based on workflow files, block commit/push on failures, and verify CI readiness before submitting to GitHub.
---

# Run GitHub CI Before Commit

## Overview

Enforce a hard gate before `git commit` or `git push`: run the same required checks defined by the target repository's GitHub workflow. Never assume the skill folder is the target repository.

## Workflow
1. Resolve target repository.
2. Discover CI requirements from workflow files.
3. Build exact local check list.
4. Execute checks and collect evidence.
5. Block commit/push on failures.
6. Submit to GitHub only after checks pass.
7. Create pull request as the final step when requested.

## Step 1: Resolve Target Repository (Mandatory)
Determine repo in this order:
1. User-explicit path or repo name (highest priority).
2. Current working directory git root (`git rev-parse --show-toplevel`).
3. If not in git repo, stop and ask for target repo path.

Hard rules:
- Do not treat `~/.codex/skills/<skill-name>` as target repo unless user explicitly says so.
- Do not run CI checks in a non-git directory.
- Always print resolved repository path before running checks.

## Step 2: Discover CI Requirements
Read workflow definitions from target repo:
- `.github/workflows/*.yml`
- `.github/workflows/*.yaml`

Prioritize jobs triggered by `push` / `pull_request`.
Extract required quality steps from `run:` commands first.

Focus on jobs that are quality gates for pull requests or pushes:
- lint / format
- typecheck / static analysis
- unit/integration/e2e tests
- build/package validation
- language-specific checks (security scan, migrations validation, etc.)

Ignore deployment-only jobs unless the user asks to run them locally.

If no workflow file exists, derive a best-effort default set from project scripts/toolchain and clearly state this is fallback mode.

## Step 3: Build Local Check List
Build a deterministic ordered list matching CI intent, for example:
1. install dependencies
2. lint/format check
3. typecheck/static analysis
4. tests
5. build

Use repository-native tooling and scripts first (`bun run ...`, `npm run ...`, `pnpm ...`, `yarn ...`, `pytest`, `go test`, etc.).
Do not invent non-existent commands.
If workflow has explicit commands, run those exact commands.

## Step 4: Execute Checks
Run checks in deterministic order and stop at first failure when speed matters, or run all and produce a full failure list when diagnostics matter.

When a command fails:
- capture failing command
- capture key error output
- provide fix direction
- re-run affected checks after fix

## Step 5: Commit/Push Gate Rules
- Never run `git commit` while required checks are failing.
- Never run `git push` while required checks are failing.
- If all required checks pass, proceed with commit flow and then push.
- If the user insists on commit/push with failures, require explicit confirmation and note risk.

## Step 6: Submit to GitHub
When user asks "提交到 GitHub":
1. Verify repo has remote (`git remote -v`).
2. Verify auth (`gh auth status`) when available.
3. Push branch to remote.
4. If workflows exist, optionally check latest run status (`gh run list`, `gh run view`).
5. Report commit SHA, branch, remote URL, and CI status.

## Step 7: Create Pull Request (Final Step)
When user asks to create PR (or asks to complete GitHub submission end-to-end):
1. Confirm base branch and head branch.
2. Ensure branch has been pushed successfully.
3. Create PR with clear title and summary (`gh pr create`).
4. Return PR URL as final delivery artifact.

Hard rules:
- PR creation must happen after required checks pass and after push succeeds.
- If checks fail, do not create PR unless user explicitly overrides risk.

## Output Format
Always report:
1. Resolved target repo path
2. Required checks list (source: workflow/fallback)
3. Executed commands
4. Pass/fail per command
5. Final gate result:
   - `CI Gate: PASS - Safe to commit`
   - `CI Gate: FAIL - Commit blocked`
6. If pushed: repo URL, branch, commit SHA, Actions status
7. If PR created: PR URL, base branch, head branch

## Example Triggers
- "提交前先跑一下 GitHub CI 要求"
- "帮我确认这次改动能过 CI 再 commit"
- "按仓库 CI 规则做 pre-commit 检查"
- "把这个改动提交到 GitHub"
- "创建 PR"

## Guardrails
- Prefer exact CI parity over speed shortcuts.
- Keep command list concise and reproducible.
- If CI has matrix jobs, cover at least the default development target unless user requests full matrix simulation.
- If repository scope is ambiguous, stop and clarify before running checks or pushing.
- If user asks for PR, treat PR creation as the final completion step.
