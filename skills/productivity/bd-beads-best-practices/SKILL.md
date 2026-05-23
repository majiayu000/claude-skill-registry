---
name: bd-beads-best-practices
description: Beads (bd) best practices and operating workflow for creating, updating, and executing issues with dependencies. Use when setting up bd in a repo, creating/updating bd issues or prompts/templates, running bd hygiene (doctor/upgrade/cleanup/compact/sync), or coordinating agent workflows with bd.
---

# Bd Beads Best Practices

## Overview
Use this skill to run bd with consistent, dependency-aware workflows and keep databases healthy while coordinating agents.

## Workflow Decision Tree
- If creating or updating issues, follow **Issue Creation / Update** and load `references/fields-and-commands.md`.
- If executing work, follow **Task Execution Loop**.
- If maintaining bd health or sync, follow **Hygiene & Sync**.
- If the repo has local rules (worktrees, special flags), follow `AGENTS.md` and repo docs first.

## Issue Creation / Update
1) Check repo rules (required flags like `--no-daemon`, `npx bd`, or worktree usage).
2) Discover supported fields for this CLI version:
   - `bd --help`
   - `bd create --help`
   - `bd update --help`
   - `bd close --help`
3) Build a quick per-session checklist of supported fields.
4) Populate all applicable fields (type, priority, description, acceptance, design, estimate, external-ref, labels, assignee, deps, parent, waits-for/gates).
5) Add dependencies explicitly (blocks, related, parent-child, discovered-from).
6) Verify structure with `bd dep tree`, `bd ready`, or `bd list --pretty`.

## Task Execution Loop
1) Run `bd ready` and pick the highest-priority unblocked issue.
2) Claim it with `bd update <id> --status in_progress`.
3) Read details with `bd show <id>` and follow **Files** + **QA Evidence** sections.
4) Implement, test, and capture QA evidence.
5) Close with `bd close <id> --reason "..."` and record close notes.
6) Commit and push after all checks pass (if repo workflow requires it).
7) Create follow-up issues for newly discovered work, including improvements to this skill or prompts/system guidance.

## Hygiene & Sync
- Run `bd doctor` regularly; use `--fix` when safe.
- Keep the issue set small using `bd admin cleanup` or `bd admin compact`.
- Track version changes with `bd upgrade status/review/ack`.
- Use `bd sync` or `bd hooks` for git-based auto-sync unless the repo forbids it.

## Doctor Warning Remediation (common)
- **DB version behind CLI**: run `bd migrate`, then re-run `bd doctor`.
- **CLI behind latest**: upgrade (`curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash`), then re-run `bd doctor` and `bd migrate` if prompted.
- **DB ↔ JSONL count mismatch**: run `bd doctor --fix` or `bd sync --import-only`; re-run `bd doctor` to confirm.
- **Stale molecules**: run `bd mol stale`, review, then `bd close <id>` for each complete-but-unclosed molecule.
- **Daemon version mismatch**: run `bd daemon killall` (or `bd daemon restart`) to align daemon with current CLI.
- **Version tracking stale**: run `bd upgrade review`, then `bd upgrade ack`.
- **Git working tree dirty**: commit or stash changes; follow repo rules (often `git pull --rebase` then `git push`).
- **Stale closed issues**: run `bd doctor --fix` or `bd admin cleanup --force` (use `--dry-run` first).

## Worktree Guard (only if repo requires it)
1) Start a task worktree (`./scripts/task-worktree.sh start <worker> <task-id>`).
2) Verify before edits (`./scripts/task-worktree.sh verify <task-id>`).
3) Check in-progress tasks to avoid file conflicts.
4) Finish with `./scripts/task-worktree.sh finish <worker> <task-id>`.

## Guardrails
- Prefer repo-local instructions over this skill when they conflict.
- Avoid destructive operations without explicit need; use `--dry-run` first.
- Use `--json` when required by repo automation or prompts.

## References
- Load `references/fields-and-commands.md` for command/field notes and current CLI flags.
