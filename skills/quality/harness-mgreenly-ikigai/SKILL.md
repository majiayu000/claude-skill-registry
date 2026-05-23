---
name: harness
description: Automated quality check loops with escalation and fix sub-agents
---

# Harness

Automated fix loops. Each harness runs a make target, spawns sub-agents to fix failures, commits on success, reverts on exhaustion.

**Pattern:** `.claude/harness/<name>/run` + `fix.prompt.md`

**Escalation:** sonnet:think → opus:think → opus:ultrathink

**History:** Each harness maintains `history.md` for cross-attempt learning. Truncated per-file, accumulates across escalation. Agents append summaries after each attempt so higher-level models can avoid repeating failed approaches.

**CLI:** `.claude/scripts/check-<name>` symlinks to harness run scripts

**Commands:** `/check-<name>` runs the corresponding harness with `--no-spinner`

**Quality:** `quality/run` orchestrates all harnesses in sequence until stable

## Running check-* Skills

When invoking check-* skills via Bash:

- **Timeout:** Use 60 minute timeout (`timeout: 3600000`)
- **Foreground:** Always run in foreground (never use `run_in_background`)
- **Blocking:** No output until completion—do not tail or monitor, just wait
- **Output format:** Structured JSON: `{"ok": true/false, "items": [...]}`
