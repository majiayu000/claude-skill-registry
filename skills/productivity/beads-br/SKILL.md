---
name: beads-br
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: >-
  Local-first issue tracker (beads_rust) for AI agents. Use when tracking tasks,
  managing dependencies, finding ready work, or syncing issues to git via JSONL.
practices:
- pragmatic-programmer
---
<!-- TOC: Critical Rules | Quick Workflow | Essential Commands | bv Integration | References -->

# beads-br — Beads Rust Issue Tracker

> **Non-invasive:** br NEVER runs git commands. Sync and commit are YOUR responsibility.

## Critical Rules for Agents

| Rule | Why |
|------|-----|
| **ALWAYS use `--json`** | Structured output for parsing |
| **NEVER run bare `bv`** | Blocks session in TUI mode |
| **Sync is EXPLICIT** | `br sync --flush-only` after changes |
| **Git is YOUR job** | br only touches `.beads/` directory |
| **No cycles allowed** | `br dep cycles` must return empty |

## Private-ledger repos — the persist_intent port contract

Some repos declare a **private bead ledger** separated from the public source
tree. The agentops repo is the canonical case; an agent that loads only this
skill (without the repo CLAUDE.md) must still honor these invariants:

| Invariant | Rule |
|---|---|
| **Indirection** | Invoke as `BEADS_DIR=$PWD/_beads br <cmd>` — the ledger lives at `_beads/`, not `.beads/` (legacy `.beads/` holds retired tracker config; `br init` there would clobber it). |
| **Private repo** | `_beads/` is its **own git repository** (separate remote). Sync = `git -C _beads push`. |
| **Never leak** | never run `git add _beads` in the host repo — bead bodies carry private context; the host repo is public and gitignores the ledger. |
| **bd is retired** | because the bd/Dolt remote-server lane was retired (2026-06-11) — do not run `bd` in a br repo; it appears only in explicitly-marked legacy notes. |
| **Prefix filter** | to prevent cross-project leakage in shared DBs, filter queries by the repo's issue prefix (e.g. `ag-`) before trusting `br ready` output. |

This section is the `persist_intent` port contract: the skill that persists
intent owns the rules that keep that intent private and uncorrupted.

## Quick Workflow

```bash
# 1. Find work
br ready --json

# 2. Claim it
br update bd-abc123 --status in_progress

# 3. Do work...

# 4. Complete
br close bd-abc123 --reason "Implemented X"

# 5. Sync to git (EXPLICIT!)
br sync --flush-only
git add .beads/ && git commit -m "feat: X (bd-abc123)"
```

## Essential Commands

```bash
# Lifecycle
br init                              # Initialize .beads/
br create "Title" -p 1 -t task       # Create (priority 0-4)
br update <id> --status in_progress  # Claim work
br close <id> --reason "Done"        # Complete
br reopen <id>                       # Reopen if needed

# Querying (always use --json for agents)
br ready --json                      # Actionable work (not blocked)
br list --json                       # All issues
br blocked --json                    # What's blocked
br search "keyword"                  # Full-text search
br show <id> --json                  # Issue details

# Dependencies
br dep add <child> <parent>          # child depends on parent
br dep cycles                        # MUST be empty!
br dep tree <id>                     # Visualize dependencies

# Sync (EXPLICIT - never automatic)
br sync --flush-only                 # DB → JSONL (before git commit)
br sync --import-only                # JSONL → DB (after git pull)

# System
br doctor                            # Health check
br config --list                     # Show configuration
```

## Priority Scale

| Priority | Meaning |
|----------|---------|
| 0 | Critical |
| 1 | High |
| 2 | Medium (default) |
| 3 | Low |
| 4 | Backlog |

## bv Integration

**CRITICAL:** Never run bare `bv` — it launches interactive TUI and blocks.

```bash
# Always use --robot-* flags:
bv --robot-next                      # Single top pick
bv --robot-triage                    # Full triage
bv --robot-plan                      # Parallel execution tracks
bv --robot-insights | jq '.Cycles'   # Check graph health
```

## Agent Mail Coordination

Use bead ID as thread_id for multi-agent coordination:

```python
file_reservation_paths(..., reason="bd-123")
send_message(..., thread_id="bd-123", subject="[bd-123] Starting...")
# Work...
br close bd-123 --reason "Completed"
release_file_reservations(...)
```

## Session Ending Pattern

```bash
git pull --rebase
br sync --flush-only
git add .beads/ && git commit -m "Update issues"
git push
git status  # Verify clean
```

## Issue-Lifecycle Discipline

Folded from the retired `beads` umbrella (ag-ez7y6) — operating doctrine, not
the command surface above. These keep the tracker graph honest across sessions:

- **Live reads are authoritative.** Treat live `br show` / `br ready` / `br list`
  output as the source of truth for current tracker state. Do NOT treat the
  exported `issues.jsonl` as the primary decision source when live `br` data is
  available — the JSONL is a git-friendly export artifact, refreshed on
  `br sync --flush-only`.
- **Scoped closure proof on every close.** `br close <id> --reason` must name the
  touched files (or explicit no-file evidence artifact), the validation
  command(s) run, and the parent-reconciliation outcome. Never close a child
  bead with a generic reason like "done" or "implemented".
- **Reconcile the parent in the same session.** After closing or materially
  updating a child bead, reconcile the open parent: update stale "remaining gap"
  notes immediately, and close the parent when the child resolved its last real
  gap.
- **Narrow the umbrella issue before implementing.** If `br ready` surfaces a
  broad umbrella bead, do not implement against vague parent wording — first
  narrow the remaining gap into an execution-ready child bead, land the child,
  then reconcile the parent.
- **Normalize stale queue items instead of skipping them.** Rewrite broad or
  partially-absorbed beads to the actual remaining gap rather than silently
  passing over them.

## Anti-Patterns

- Running `br sync` without `--flush-only` or `--import-only`
- Forgetting sync before git commit
- Creating circular dependencies
- Running bare `bv`
- Assuming auto-commit behavior

## Storage

```
.beads/
├── beads.db        # SQLite (primary)
├── issues.jsonl    # Git-friendly export
└── config.yaml     # Optional config
```

## Troubleshooting

```bash
br doctor                    # Full diagnostics
br dep cycles                # Must be empty
br config --list             # Check settings
```

**Worktree error** (`'main' is already checked out`):
```bash
git branch beads-sync main
br config set sync.branch beads-sync
```

---

## References

| Topic | File |
|-------|------|
| Full command reference | [COMMANDS.md](references/COMMANDS.md) |
| Configuration details | [CONFIG.md](references/CONFIG.md) |
| Troubleshooting guide | [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) |
| Multi-agent patterns | [INTEGRATION.md](references/INTEGRATION.md) |
