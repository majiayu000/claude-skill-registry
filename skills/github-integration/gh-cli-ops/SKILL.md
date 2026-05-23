---
name: gh-cli-ops
description: GitHub CLI (gh) operations for repos, PRs/issues, workflows/runs, secrets/variables, releases/tags, and deployment-related automation. Use when a request involves gh commands, GitHub Actions workflows/runs, secrets or variables, releases, deployments/environments, or coordinating git with GitHub.
---

# Gh Cli Ops

## Overview
Use gh + git to manage GitHub repositories, automation, and releases with repeatable, safe workflows.

## Quick start (context)
1. Use the wrapper so commands are logged: `scripts/ghx auth status`, `scripts/ghx repo view`, `git status -sb`.
2. Identify the task category and use the matching section or the command map in `references/gh-command-map.md`.
3. Prefer JSON output (`--json ... --jq ...`) for scripted reads; ask before destructive changes (delete, merge, release delete, secret overwrite).
4. Review `references/auto-summary.md` to adapt based on recent successes/failures.

## Automation wrapper (required)
- Use `scripts/ghx` for all gh commands to log outcomes to `references/usage-log.jsonl`.
- The wrapper auto-updates `references/auto-summary.md` after each command to capture what worked or failed.
- If you must run `gh` directly (e.g., debugging), run `scripts/track_command.sh gh ...` afterward with the same args.

## Task map
See `references/gh-command-map.md` for a task-to-command mapping and safe defaults.

## Workflows & runs
- Use `gh workflow list/view/run` to inspect or trigger workflows. Ensure the workflow supports `on: workflow_dispatch` before running.
- Provide inputs via `-f`/`-F` or `--json` when needed; confirm expected inputs from the workflow file.
- Use `gh run list/view/watch/rerun/download` to monitor or re-run jobs; use `gh run view --log/--log-failed` for logs.
- For deploys, identify the deploy workflow and trigger it via `gh workflow run` with the correct `--ref` and inputs.
- If `gh workflow run` fails with `HTTP 403` and `Resource not accessible by integration`, check for `GITHUB_TOKEN` or `GH_TOKEN` in the environment. Unset them or replace with a PAT that has workflow permissions, then retry.
- Quick fix for local shells: `GITHUB_TOKEN= gh workflow run "<workflow>" -f key=value` (clears the env var for that command).
- In GitHub Actions, prefer `GH_TOKEN` set to a PAT or GitHub App token when you need to trigger workflows; the default `GITHUB_TOKEN` can be too limited for dispatching other workflows.

## Secrets & variables
- Use `gh secret` for Actions/Dependabot/Codespaces secrets; use `gh variable` for Actions/Dependabot variables.
- Scope to repo/org/environment as needed; check `gh secret set --help` and `gh variable set --help` for scope flags.
- Prefer stdin or `--body` to avoid shell history; confirm overwrite and scope with the user.

## Releases & tags
- Use `gh release list/view/create/download/delete`.
- Prefer `--generate-notes` for release notes when appropriate; confirm tag names and target commits.

## Deployments & environments
- For deployment environments, use environment-scoped secrets/variables (`-e <env>`).
- For deployment history or custom deploy APIs, use `gh api` with `--paginate` and `--jq` as needed.

## PRs, issues, and repo admin
- Use `gh pr` and `gh issue` for everyday collaboration.
- Use `gh repo view/fork/clone/sync` for repo operations.
- Keep git operations (branching, rebasing, pushing) explicit and separate from gh steps.

## API & advanced
- Use `gh api` for endpoints not covered by built-in commands.
- Capture JSON with `gh api ... --jq` or `--paginate` for large lists.

## Troubleshooting auth
- `Resource not accessible by integration` usually means the CLI is using an integration token (often `GITHUB_TOKEN`) that cannot dispatch workflows. Prefer a PAT stored via `gh auth login --with-token` or set `GH_TOKEN` to a PAT with workflow permissions; avoid leaving `GITHUB_TOKEN` exported in local shells.
- `GH_TOKEN`/`GITHUB_TOKEN` environment variables override stored gh auth. If you see unexpected 403s, unset them or replace with a PAT/GitHub App token that has Actions/workflow permissions before retrying.

## Self-improving loop (automated + manual)
Automated (always on when using `scripts/ghx`):
1. Command outcomes are logged to `references/usage-log.jsonl`.
2. `scripts/auto_improve.py` updates `references/auto-summary.md` and can append repeatable learnings to `references/gh-ops-notes.md`.

Manual (when new patterns are discovered):
1. Append new command patterns, flags, or pitfalls to `references/gh-ops-notes.md`.
2. If a command/flag is missing or changed, update `references/gh-command-map.md`.
3. Run `scripts/refresh_gh_reference.sh` to refresh `references/gh-help.md` from the locally installed `gh`.

## Resources
### scripts/
- `scripts/ghx`: wrapper that logs gh command outcomes and triggers auto-summary updates.
- `scripts/track_command.sh`: logs command outcomes to `references/usage-log.jsonl`.
- `scripts/auto_improve.py`: generates `references/auto-summary.md` and auto-notes.
- `scripts/refresh_gh_reference.sh`: regenerate `references/gh-help.md` from local gh help output.

### references/
- `references/gh-command-map.md`: task-to-command map and safe defaults.
- `references/gh-help.md`: auto-generated help snapshot from the local gh version.
- `references/gh-ops-notes.md`: living notes for patterns, pitfalls, and team conventions.
- `references/auto-summary.md`: auto-generated success/failure summary for recent commands.
- `references/usage-log.jsonl`: append-only command log (redacted).
