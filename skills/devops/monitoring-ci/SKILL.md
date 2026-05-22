---
name: monitoring-ci
description: Monitor and watch GitHub Actions CI/CD pipeline runs in real time. Use when the user has pushed code and wants to watch the build, check CI status, see if tests passed, monitor a pipeline, or wait for a workflow run to complete. Also use after any `jj git push` or `git push` command. Reports pass/fail with failed job logs. Do NOT use for writing or editing CI workflow YAML files, optimizing CI config, or debugging CI configuration — only for monitoring active runs.
---

# CI Monitor

Watch GitHub Actions CI runs after a push. Auto-detects repo and branch, deduplicates concurrent monitors, reports results.

## Usage

Run the script in the background after pushing:

```bash
uv run ~/.claude/skills/monitoring-ci/ci-monitor.py
```

With explicit branch:

```bash
uv run ~/.claude/skills/monitoring-ci/ci-monitor.py --branch my-feature
```

## How to Invoke from Claude

After a push, run as a background Bash command:

```bash
uv run ~/.claude/skills/monitoring-ci/ci-monitor.py --branch <branch-name>
```

Use `run_in_background: true` so it doesn't block the conversation. Tell the user: "CI monitor running in background — you'll be notified when it completes."

## Features

- **Auto-detects branch**: jj bookmarks first, falls back to git
- **Deduplicates**: sentinel file at `/tmp/{repo}-ci-monitor` prevents double-watching
- **Polls for run**: waits up to 60s for a CI run to appear on the branch
- **Watches until done**: uses `gh run watch --exit-status`
- **Reports failure logs**: on failure, fetches `gh run view --log-failed` (last 3000 chars)
- **Cleans up**: always removes sentinel, even on error

## Exit Codes

- `0` — CI passed (or no run found)
- `1` — CI failed (logs printed)

## Requirements

- `gh` CLI authenticated
- GitHub Actions workflows in the repo
