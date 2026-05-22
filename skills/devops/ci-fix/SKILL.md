---
name: ci-fix
description: "Fix GitHub Actions CI failures using GitHub CLI (gh): inspect runs/logs, identify root cause, patch workflows/code, rerun jobs, and summarize verification. Use when GitHub Actions CI is failing or needs diagnosis."
---

# CI fix (GitHub Actions)

## Goal
- Get CI green quickly with minimal, reviewable diffs.
- Use `gh` to locate failing runs, inspect logs/artifacts, rerun jobs, and confirm the fix.

## Inputs to ask for (if missing)
- Repo (`OWNER/REPO`) and whether this is a PR or branch build.
- Failing run URL/ID (or PR number / branch name).
- What "green" means (required workflows? allowed flaky reruns?).
- Any constraints (no workflow edits, no permission changes, no force-push, etc.).

## Workflow (checklist)
1) Confirm `gh` context
   - Auth: `gh auth status`
   - Repo: `gh repo view --json nameWithOwner -q .nameWithOwner`
   - If needed, add `-R OWNER/REPO` to all commands.
   - If `gh` is not installed or not authenticated, tell the user and ask whether to install/authenticate or proceed by pasting logs/run URLs manually.
2) Find the failing run
   - If you have a run URL, extract the run ID: `.../actions/runs/<id>`.
   - Otherwise:
     - Recent failures: `gh run list --limit 20 --status failure`
     - Branch failures: `gh run list --branch <branch> --limit 20 --status failure`
     - Workflow failures: `gh run list -w <workflow> --limit 20 --status failure`
   - Open in browser: `gh run view <id> --web`
3) Pull the signal from logs
   - Job/step overview: `gh run view <id> --verbose`
   - Failed steps only: `gh run view <id> --log-failed`
   - Full log for a job: `gh run view <id> --log --job <job-id>`
   - Download artifacts: `gh run download <id> -D .artifacts/<id>`
4) Identify root cause (prefer the smallest fix)
   - Use `references/ci-failure-playbook.md` for common patterns and safe fixes.
   - Prefer: deterministic code/config fix > workflow plumbing fix > rerun flake.
5) Implement the fix (minimal diff)
   - Update code/tests/config and/or `.github/workflows/*.yml`.
   - Keep changes scoped to the failing job/step.
   - If changing triggers/permissions/secrets, call out risk and get explicit confirmation.
6) Verify in GitHub Actions
   - Rerun only failures: `gh run rerun <id> --failed`
   - Rerun a specific job (note: job **databaseId**): `gh run view <id> --json jobs --jq '.jobs[] | {name,databaseId,conclusion}'`
   - Watch until done: `gh run watch <id> --compact --exit-status`
   - Manually trigger: `gh workflow run <workflow> --ref <branch>`

## Safety notes
- Avoid `pull_request_target` (and any change that runs untrusted fork code with secrets) unless the user explicitly requests it and understands the security tradeoffs.
- Keep workflow `permissions:` least-privilege; don’t broaden token access “just to make it pass”.

## Deliverable (paste in chat / PR)
- **Summary:** ...
- **Failing run:** <link/id> (job/step)
- **Root cause:** ...
- **Fix:** ...
- **Verification:** commands + new run link/id
- **Notes/risks:** ...
