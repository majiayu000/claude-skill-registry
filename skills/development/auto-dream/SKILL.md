---
name: auto-dream
description: Background memory consolidation and learning graduation — overnight knowledge lifecycle.
user-invocable: true
command: dream
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
routing:
  triggers:
    - dream
    - consolidate memories
    - clean up memories
    - memory maintenance
    - memory consolidation
    - deduplicate memories
    - graduate learnings
    - promote learnings
  category: meta-tooling
  pairs_with: []
---

Background memory consolidation cycle. Scans memory files, finds stale/duplicate/conflicting entries, consolidates, synthesizes cross-session insights, builds an injection-ready payload for next session start, and writes a dated dream report.

## When to invoke

- User says "run dream", "consolidate memories", "clean up memories", "memory maintenance", "deduplicate memories"
- Cron job at 2 AM nightly via wrapper script: `scripts/auto-dream-cron.sh --execute`
- Manual trigger for testing: `./scripts/auto-dream-cron.sh` (dry-run by default)

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| Debugging failed cron run, silent failure, empty log, wrong exit code | `headless-cron-patterns.md` | Routes to the matching deep reference |
| Setting up or modifying wrapper script (`flock`, `--permission-mode`, `envsubst`, `PIPESTATUS`) | `headless-cron-patterns.md` | Routes to the matching deep reference |
| Budget cap, `--max-budget-usd`, unattended Claude invocation | `headless-cron-patterns.md` | Routes to the matching deep reference |
| Writing, updating, or archiving memory files | `memory-file-operations.md` | Routes to the matching deep reference |
| Updating `MEMORY.md` index, atomic write, `.tmp` rename | `memory-file-operations.md` | Routes to the matching deep reference |
| Staleness detection, duplicate merging, conflict flagging | `memory-file-operations.md` | Routes to the matching deep reference |
| YAML frontmatter structure, `merged_from`, memory file format | `memory-file-operations.md` | Routes to the matching deep reference |
| Testing the dream cycle safely, dry-run validation, output file verification | `dream-cycle-testing.md` | Routes to the matching deep reference |
| Inspecting graduation candidates, snapshot testing, PIPESTATUS in test wrappers | `dream-cycle-testing.md` | Routes to the matching deep reference |
| Reading and interpreting cron run logs, detecting silent failures | `logging-patterns.md` | Routes to the matching deep reference |
| Log rotation, log directory structure, phase completion markers in logs | `logging-patterns.md` | Routes to the matching deep reference |
| `last-dream.md` stale, missing injection payload, cron log empty | `logging-patterns.md` | Routes to the matching deep reference |
| Concurrent dream runs, lockfile already held, duplicate cron invocations | `concurrency.md` | Routes to the matching deep reference |
| `MEMORY.md.tmp` left behind, partial write recovery, atomic rename failure | `concurrency.md` | Routes to the matching deep reference |
| `database is locked`, SQLite WAL mode, `busy_timeout`, concurrent DB access | `concurrency.md` | Routes to the matching deep reference |
| `local changes would be overwritten`, git stash before GRADUATE branch switch | `concurrency.md` | Routes to the matching deep reference |

## Instructions

When invoked interactively (not via cron), read `skills/meta/auto-dream/dream-prompt.md` and execute its phases directly. The prompt is self-contained — it describes the full seven-phase cycle including safety constraints, file paths, and output formats.

For cron invocation: the dream prompt is passed directly to `claude -p` and runs as a standalone headless session with no CLAUDE.md, no hooks, no project context. All instructions are embedded in the prompt.

## Phases

1. **SCAN** — Read all memory files, query learning.db sessions (last 7 days), read recent git log. Write scan document to `~/.claude/state/dream-scan-{date}.md`.
2. **ANALYZE** — Identify stale, duplicate, conflicting memories and cross-session patterns. Write analysis to `~/.claude/state/dream-analysis-{date}.md`.
3. **CONSOLIDATE** — Apply consolidation actions (max 5 changes). Archive stale/merged files, update MEMORY.md atomically.
4. **SYNTHESIZE** — Create insight memories from cross-session patterns (max 2 new memories per cycle).
5. **GRADUATE** — Promote mature learning DB entries (confidence >= 0.9, 3+ observations) into agent/skill files as permanent failure modes. Commits on `dream/graduate-YYYY-MM-DD` branch for human review. Max 3 per cycle. (ADR-159)
6. **SELECT** — Build injection-ready payload for session start. Write to `~/.claude/state/dream-injection-{project-hash}.md`.
7. **REPORT** — Write dream summary to `~/.claude/state/last-dream.md`.

## Safety constraints (always enforced)

- Never delete files — archive to `memory/archive/`, never `rm`
- Write the REPORT before executing any CONSOLIDATE filesystem operations
- Maximum 5 memory changes per cycle — excess items deferred to next cycle
- Flag conflicts for human review, never auto-resolve
- Preserve YAML frontmatter when merging; use `merged_from` field for provenance
- In dry-run mode (the default), CONSOLIDATE, SYNTHESIZE, and GRADUATE describe proposed changes only — no filesystem writes or git operations. The wrapper script sets `DREAM_DRY_RUN_MODE=yes` which is substituted into the prompt at runtime.
- GRADUATE commits on a feature branch (`dream/graduate-*`), never on main — user reviews and merges
- Maximum 3 graduations per cycle — only entries with confidence >= 0.9 and 3+ observations

## Testing

```bash
# Dry run (read-only, no filesystem changes — dry-run is the default)
./scripts/auto-dream-cron.sh

# Full run (execute consolidation)
./scripts/auto-dream-cron.sh --execute

# Check output
cat ~/.claude/state/last-dream.md

# Check graduation candidates (what dream would graduate)
python3 -c "
import sys; sys.path.insert(0, 'hooks/lib')
from learning_db_v2 import query_graduation_candidates
import json
candidates = query_graduation_candidates()
print(json.dumps(candidates, indent=2))
"

# Check if a graduation branch exists
git branch --list 'dream/graduate-*'

# Verify cron registration
python3 ~/.claude/scripts/crontab-manager.py list
```

## Cost estimate

~$0.09 per nightly run with 50 memory files (~20-30K input tokens at Sonnet pricing). ~$33/year for automated overnight operation. Budget capped at $3.00/run via wrapper script.

## Cron setup

Use `crontab-manager.py` (not raw `crontab -e`) to install. The wrapper script handles PATH, lockfile, logging, budget cap, and dry-run/execute toggle.

```bash
# Preview the cron entry
python3 ~/.claude/scripts/crontab-manager.py add \
  --tag "auto-dream" \
  --schedule "7 2 * * *" \
  --command "/home/feedgen/vexjoy-agent/scripts/auto-dream-cron.sh --execute >> /home/feedgen/vexjoy-agent/cron-logs/auto-dream/cron.log 2>&1" \
  --dry-run

# Install (after dry-run testing passes)
python3 ~/.claude/scripts/crontab-manager.py add \
  --tag "auto-dream" \
  --schedule "7 2 * * *" \
  --command "/home/feedgen/vexjoy-agent/scripts/auto-dream-cron.sh --execute >> /home/feedgen/vexjoy-agent/cron-logs/auto-dream/cron.log 2>&1"

# Verify
python3 ~/.claude/scripts/crontab-manager.py verify --tag auto-dream
```

Note: schedule uses 2:07 AM (off-minute) per cron best practice — avoids load spikes from jobs firing at :00.

## Wrapper script details

`scripts/auto-dream-cron.sh` follows the established headless cron pattern (see `skills/content/reddit-moderate/scripts/reddit-automod-cron.sh`):
- `flock` lockfile prevents concurrent runs
- `--permission-mode auto` (never `--dangerously-skip-permissions`)
- `--max-budget-usd 3.00` caps spend per run
- `--no-session-persistence` for clean headless operation
- `envsubst` templates `dream-prompt.md` with project-specific paths at runtime
- `tee` to timestamped per-run log file
- Dry-run by default, `--execute` for live runs
- Exit code propagation via `PIPESTATUS[0]`

## Reference Loading

Load these references when the task matches the signal:

| Signal / Task | Reference File |
|---------------|----------------|
| Debugging failed cron run, silent failure, empty log, wrong exit code | `references/headless-cron-patterns.md` |
| Setting up or modifying wrapper script (`flock`, `--permission-mode`, `envsubst`, `PIPESTATUS`) | `references/headless-cron-patterns.md` |
| Budget cap, `--max-budget-usd`, unattended Claude invocation | `references/headless-cron-patterns.md` |
| Writing, updating, or archiving memory files | `references/memory-file-operations.md` |
| Updating `MEMORY.md` index, atomic write, `.tmp` rename | `references/memory-file-operations.md` |
| Staleness detection, duplicate merging, conflict flagging | `references/memory-file-operations.md` |
| YAML frontmatter structure, `merged_from`, memory file format | `references/memory-file-operations.md` |
| Testing the dream cycle safely, dry-run validation, output file verification | `references/dream-cycle-testing.md` |
| Inspecting graduation candidates, snapshot testing, PIPESTATUS in test wrappers | `references/dream-cycle-testing.md` |
| Reading and interpreting cron run logs, detecting silent failures | `references/logging-patterns.md` |
| Log rotation, log directory structure, phase completion markers in logs | `references/logging-patterns.md` |
| `last-dream.md` stale, missing injection payload, cron log empty | `references/logging-patterns.md` |
| Concurrent dream runs, lockfile already held, duplicate cron invocations | `references/concurrency.md` |
| `MEMORY.md.tmp` left behind, partial write recovery, atomic rename failure | `references/concurrency.md` |
| `database is locked`, SQLite WAL mode, `busy_timeout`, concurrent DB access | `references/concurrency.md` |
| `local changes would be overwritten`, git stash before GRADUATE branch switch | `references/concurrency.md` |
