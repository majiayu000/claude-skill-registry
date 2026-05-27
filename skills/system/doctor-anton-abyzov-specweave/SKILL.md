---
description: Run installation health diagnostics - detect ghost commands, stale cache, hash mismatches, and namespace pollution. Use when saying "doctor", "health check", "diagnose installation", or "check installation".
argument-hint: "[--fix] [--verbose]"
---

# Doctor - Installation Health Scanner

## Project Overrides

!`s="doctor"; for d in .specweave/skill-memories .claude/skill-memories "$HOME/.claude/skill-memories"; do p="$d/$s.md"; [ -f "$p" ] && awk '/^## Learnings$/{ok=1;next}/^## /{ok=0}ok' "$p" && break; done 2>/dev/null; true`

## Project Context

!`.specweave/scripts/skill-context.sh doctor 2>/dev/null; true`

Run SpecWeave installation health diagnostics to detect and fix common issues.

## Usage

```
/sw:doctor [--fix] [--verbose]
```

**Flags**: `--fix` (auto-remediate safe issues) | `--verbose` (show details)

## What It Checks

1. **Ghost slash commands** - PLUGIN.md, README.md, FRESHNESS.md leaked into `~/.claude/commands/` appearing as phantom slash commands
2. **Stale cache directories** - Orphaned `temp_local_*` dirs from interrupted plugin installs
3. **Lockfile integrity** - SHA mismatch between `vskill.lock` and installed commands
4. **Command namespace pollution** - Internal .md files (knowledge-base/, lib/, templates/) treated as commands

## Execution

**Step 1**: Check if `specweave` CLI is available:

```bash
which specweave 2>/dev/null || echo "NOT_FOUND"
```

If NOT_FOUND, tell the user: "SpecWeave CLI not found. Install with: `npm install -g specweave`"

**Step 2**: Run the doctor command. Parse the arguments from the user:

- If `--fix` passed: `specweave doctor --fix --verbose`
- If `--verbose` passed: `specweave doctor --verbose`
- Default: `specweave doctor --verbose`

```bash
specweave doctor --verbose
```

**Step 3**: Present the output in a readable format. Highlight:
- Any `warn` or `fail` status items
- Suggested fix commands
- If issues found, recommend running with `--fix` flag

## Fix Mode

With `--fix`, the doctor will:
- Delete ghost .md files from `~/.claude/commands/`
- Remove orphaned `temp_local_*` cache directories
- Delete namespace-polluting .md files from internal dirs
- Suggest (not auto-run) `specweave refresh-plugins` for hash mismatches

All fixes are **idempotent** and **safe** (only deletes within `~/.claude/`).

ARGUMENTS: $ARGUMENTS
