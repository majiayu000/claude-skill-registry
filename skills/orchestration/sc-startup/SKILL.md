---
name: sc-startup
version: 0.8.0
description: "Run repo startup: prompt load, checklist sync, optional PR triage, worktree hygiene, and CI pull. Best-effort with structured status."
entry_point: /sc-startup
---

# sc-startup Skill

Thin orchestration for the `/sc-startup` command. Validates config, launches background agents, aggregates statuses, and emits a concise startup report. Delegates all heavy lifting to agents via Agent Runner (registry enforced, audited).

## Command
- `/sc-startup [--pr] [--pull] [--fast] [--readonly]`
- `/sc-startup --init` (config discovery and guided setup)

## Agents
- `ci-pr-agent` (PR list/fix; list-only when `--readonly`)
- `sc-worktree-scan` / `sc-worktree-cleanup` (worktree hygiene; scan-only when `--readonly`)
- `ci-automation` (pull-only master → develop; must complete before checklist updates)
- `sc-checklist-status` (report/update checklist; report-only when `--readonly`; no auto-commit)
- `sc-startup-init` (detection-only: config presence, candidates, package detection; returns fenced JSON with YAML payload)

## Flow (best-effort)
1. If `--init`: Agent Runner → `sc-startup-init` (detection-only). Parse results, use AskQuestion to fill missing/ambiguous settings (prompt path, checklist path, worktree-scan, pr-enabled, worktree-enabled). If not `--readonly`, write `.claude/sc-startup.yaml`; otherwise show synthesized YAML. Then continue.
2. Load `.claude/sc-startup.yaml`; validate required keys and enabled feature dependencies. Fail closed with `DEPENDENCY.MISSING` if enabled package absent.
3. If `--fast`: read startup prompt only, summarize role, exit (no agents/checklist).
4. If `--pr` and enabled: Agent Runner → `ci-pr-agent` (`--list --fix`, or list-only when `--readonly`).
5. If worktree scan/cleanup enabled in config: Agent Runner → `sc-worktree-{scan|cleanup}` (scan/report-only when `--readonly`).
6. If `--pull`: Agent Runner → `ci-automation` (pull-only master → develop); wait for completion before checklist updates.
7. Agent Runner → `sc-checklist-status` (default update; report-only when `--readonly`). Checklist changes stay in workspace (no commit).
8. Read startup prompt + checklist (post-update). Aggregate task statuses in deterministic order; never abort on agent errors/timeouts.
9. Emit concise report: prompt summary, checklist deltas, PR/worktree/CI outcomes, partial failures, and next steps.

If `sc-checklist-status` reports `VALIDATION.INVALID_PATH` (path escape), explicitly flag it as a warning/issue in the final report (include the word "warning" or "issue").

## Config (`.claude/sc-startup.yaml`)
- `startup-prompt` (string, required)
- `check-list` (string, required)
- `worktree-scan` (string: `scan|cleanup|none|""`)
- `pr-enabled` (bool, optional; must be false if PR package absent)
- `worktree-enabled` (bool, optional; must be false if worktree package absent)

## Safety
- Path safety: repo-root-relative only.
- Default mutating; `--readonly` forces report-only everywhere.
- No auto-commit of checklist changes.
- Dependency validation required before launch; fail closed if missing.
- Logging: Agent Runner audit logs under `.claude/state/logs/sc-startup/`; prune after ~14 days.

## Output Contract
- Aggregate per-task status objects `{agent_id, status: success|failure|timeout|partial, results, error?}` plus narrative summary.
- Agents return fenced JSON minimal envelope; treat malformed/unfenced JSON as failure status.
- Dependency failure format (example):
  ```json
  {
    "success": false,
    "data": null,
    "error": {
      "code": "DEPENDENCY.MISSING",
      "message": "Feature 'pr' enabled but required agent 'ci-pr-agent' is not installed",
      "recoverable": true,
      "suggested_action": "Install ci-pr-agent or set pr-enabled: false in .claude/sc-startup.yaml"
    }
  }
  ```
