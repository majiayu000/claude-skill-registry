---
name: project-pulse
description: "Automated PM sync skill for GitHub-first projects. Use it to sync issue state from GitHub, maintain a local cache cursor, and generate priority/risk reports plus next actions for controller planning."
---

# Project Pulse

## Overview

Use this skill when you need a product-manager and architect view of project health from GitHub issues and PRs.

This skill follows a GitHub-first sync model:
- GitHub is the source of truth.
- Local files are cache and analysis artifacts.

## When To Use

Use this skill for:
- Daily/weekly priority sync.
- Controller planning refresh before autonomous actions.
- Detecting stale issues and priority drift.
- Generating a compact PM report for discussion.
- Converting repo state into an execution plan (what to do next, what can run in parallel, what should be deferred).

Do not use this skill for:
- Code implementation of issues.
- PR review or PR fix execution.

## Workflow

1. Resolve target repo (`owner/repo`) from argument, `PULSE_REPO`, or git remote.
2. Read local pulse artifacts first (`report.json`, `issues-index.json`, `prs-index.json`).
3. If cache is stale, pull issue and PR data from GitHub (`gh issue list`, `gh pr list`).
4. Update local sync state (`sync-state.json`) with latest cursor (`last_max_updated_at`).
5. Generate analysis artifacts:
- `issues/` + `issues-index.json`
- `prs/` + `prs-index.json`
- `report.json`
- `report.md`
- `sync-state.json`
6. Produce planning decisions from report signals:
- Priority plan (`P0/P1/P2` mapping from labels + risk signals)
- Parallel work lanes (independent streams)
- Blockers and preconditions (e.g., failing PR checks before new feature work)
- Suggested next actions for controller triggers

## Default Read Path (Required)

For priority/planning/risk analysis, always use this order:

1. Read `${PULSE_BASE_DIR}/report.json`
2. Read `${PULSE_BASE_DIR}/issues-index.json` and `${PULSE_BASE_DIR}/prs-index.json`
3. Refresh from GitHub only when cache is stale or explicitly forced

Do not start with direct `gh issue list` / `gh pr list` queries when pulse cache is fresh.

## Controller Rule (Required)

When the request is about prioritization, planning, risk, sequencing, or architecture status:

1. Run `project-pulse` first
2. Base conclusions on pulse artifacts
3. Use direct GitHub API reads only as fallback/verification for specific missing fields

## Planning And Design Guidance

Use `report.json` as a decision input, not just a status snapshot.

Decision order:
1. Stabilize execution surface first:
- If `pr_totals.failing_checks > 0`, prioritize PR fixes before opening new implementation threads.
- If `pr_totals.changes_requested > 0`, prioritize review feedback closure to reduce queue latency.
2. Protect top-priority delivery:
- Treat `priority:critical` issues as daily-sync queue.
- Keep WIP bounded; avoid starting medium-priority work while critical queue is growing.
3. Control flow health:
- Use `stale_issues` and `stalled_prs` to detect drift and assign owner/escalation actions.
4. Plan architecture increments:
- Use pulse results to split work into independent lanes (runtime/core, policy/controller, quality/security).
- Avoid coupling unrelated architecture changes in one run.

Suggested controller action mapping:
- `failing_prs` not empty -> trigger `github-pr-fix`
- `ready_to_merge_candidates` not empty -> run merge-policy check or human-review gate
- `priority:critical` issue queue not empty and PR surface stable -> trigger `github-issue-solve`
- no urgent signals -> no-op / wait and continue monitoring

## Script

Run `scripts/pulse.sh`.

Examples:

```bash
# Use current git repo remote
skills/project-pulse/scripts/pulse.sh

# Explicit repo
skills/project-pulse/scripts/pulse.sh holon-run/holon

# Include closed issues in analysis
PULSE_INCLUDE_CLOSED=true skills/project-pulse/scripts/pulse.sh holon-run/holon
```

## Environment Variables

- `PULSE_REPO`: Optional repo override (`owner/repo`).
- `PULSE_INCLUDE_CLOSED`: `true|false` (default `false`).
- `PULSE_MAX_ISSUES`: max fetched issues (default `500`).
- `PULSE_MAX_PRS`: max fetched PRs (default `500`).
- `PULSE_STALE_DAYS`: stale threshold days (default `14`).
- `PULSE_MAX_AGE_MINUTES`: cache freshness threshold in minutes (default `10`).
- `PULSE_FORCE_REFRESH`: `true|false`, bypass cache and force GitHub sync (default `false`).
- `PULSE_BASE_DIR`: base directory for repository-local pulse data (default `$HOME/.holon/project-pulse/<owner>/<repo>`).
- `PULSE_OUT_DIR`: analysis output directory (default `${PULSE_BASE_DIR}`).
- `PULSE_STATE_DIR`: local cache/cursor directory (default `${PULSE_BASE_DIR}`).
- `PULSE_SPLIT_ISSUES`: `true|false`, store issues as one-file-per-issue (default `true`).
- `PULSE_KEEP_RAW_ISSUES`: `true|false`, also keep aggregated `issues.json` (default `false`).
- `PULSE_SPLIT_PRS`: `true|false`, store PRs as one-file-per-PR (default `true`).
- `PULSE_KEEP_RAW_PRS`: `true|false`, also keep aggregated `prs.json` (default `false`).

## Output Contract

- `${PULSE_OUT_DIR}/issues/`: per-issue snapshots (`<number>.json`) when `PULSE_SPLIT_ISSUES=true`.
- `${PULSE_OUT_DIR}/issues-index.json`: compact index for fast scan when `PULSE_SPLIT_ISSUES=true`.
- `${PULSE_OUT_DIR}/issues.json`: aggregated snapshot when `PULSE_SPLIT_ISSUES=false` or `PULSE_KEEP_RAW_ISSUES=true`.
- `${PULSE_OUT_DIR}/prs/`: per-PR snapshots (`<number>.json`) when `PULSE_SPLIT_PRS=true`.
- `${PULSE_OUT_DIR}/prs-index.json`: compact index for fast scan when `PULSE_SPLIT_PRS=true`.
- `${PULSE_OUT_DIR}/prs.json`: aggregated snapshot when `PULSE_SPLIT_PRS=false` or `PULSE_KEEP_RAW_PRS=true`.
- `${PULSE_OUT_DIR}/report.json`: machine-readable PM summary.
- `${PULSE_OUT_DIR}/report.md`: human-readable PM summary.
- `${PULSE_STATE_DIR}/sync-state.json`: latest cursor and sync metadata.

`report.json` includes `next_actions` for direct controller consumption.

Schema details: see `references/report-schema.md`.
Planning usage: see `references/planning-playbook.md`.

## Notes

- Keep write actions (label/comment edits) outside this script by default.
- This skill is analysis-first and safe by default.
