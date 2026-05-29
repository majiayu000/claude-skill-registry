---
name: user-config-management
description: Central authority for managing Claude Code user configuration directories (~/.claude/ and ~/.claude.json). Covers storage cleanup, backup/restore, reset workflows, MCP server preservation, history management, plan management, session statistics, and configuration health auditing. Delegates to docs-management skill for official documentation. Use when managing user config, cleaning up storage, backing up settings, resetting Claude Code, or auditing configuration health.
allowed-tools: Read, Glob, Grep, Skill, Bash
---

# User Configuration Management

## MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Code user configuration:**
>
> 1. **INVOKE** `docs-management` skill for official documentation
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses on official documentation + this skill's custom references
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill for official docs?
- [ ] Did I check this skill's references for custom workflows?
- [ ] Is my response based on official docs (settings, MCP) + skill references (reset, backup)?

If ANY checkbox is unchecked, STOP and complete the missing steps.

---

## Overview

Central authority for managing Claude Code's user configuration directories. This skill provides:

1. **Keyword registry** for efficient docs-management queries
2. **Custom workflows** not covered by official docs (reset, backup/restore, drift detection)
3. **Command inventory** linking to existing cleanup commands
4. **Cross-platform guidance** for path handling

**Architecture:** Hybrid delegation - official docs via docs-management, custom workflows via skill references.

## When to Use This Skill

**Keywords:** user config, ~/.claude, .claude.json, cleanup, storage, backup, restore, reset, MCP servers, history, plans, sessions, debug logs, prune, audit, drift detection

**Use this skill when:**

- Managing ~/.claude/ directory contents
- Cleaning up storage (sessions, agents, debug, cache)
- Backing up or restoring configuration
- Resetting Claude Code while preserving MCP servers
- Searching command history
- Managing plan files
- Viewing session statistics
- Auditing configuration health
- Detecting structure drift after updates

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill:

### Configuration Files

| Topic | Keywords |
| --- | --- |
| Settings Overview | "settings", "settings.json", "configuration files" |
| User Settings | "user settings", "~/.claude/settings.json" |
| Global Config | ".claude.json", "global config", "mcpServers" |
| MCP Servers | "MCP servers", "mcpServers", "user-level MCP" |

### Retention & Cleanup

| Topic | Keywords |
| --- | --- |
| Retention Setting | "cleanupPeriodDays", "session retention", "auto-cleanup" |
| Session Cleanup | "sessions", "project sessions", "session files" |
| Debug Logs | "debug", "debug transcripts", "debugging" |

### Storage Locations

| Topic | Keywords |
| --- | --- |
| Storage Structure | "~/.claude", "storage directory", "claude folder" |
| Projects Directory | "projects", "project sessions", "session storage" |
| Plugins Directory | "plugins", "plugin cache", "installed plugins" |

## Quick Decision Tree

**What do you want to do?**

1. **Check storage usage** -> Run `/user-config:storage` (was `/check-claude-storage`)
2. **Clean up sessions** -> Run `/user-config:cleanup-sessions` (was `/cleanup-sessions`)
3. **Clean up agents** -> Run `/user-config:cleanup-agents` (was `/cleanup-agents`)
4. **Clean up debug logs** -> Run `/user-config:cleanup-debug` (was `/cleanup-debug`)
5. **Comprehensive cleanup** -> Run `/user-config:prune` (was `/prune-cache`)
6. **Nuclear cleanup (everything)** -> Run `/user-config:prune --nuclear`
7. **Backup configuration** -> Run `/user-config:backup`
8. **Restore from backup** -> Run `/user-config:restore`
9. **Reset (preserve MCP)** -> Run `/user-config:reset` - See [reset-workflow.md](references/reset-workflow.md)
10. **Search history** -> Run `/user-config:history`
11. **Manage plans** -> Run `/user-config:plans`
12. **Audit config health** -> Run `/user-config:audit`
13. **View session stats** -> Run `/user-config:session-stats`
14. **View MCP servers** -> Run `/user-config:mcp`
15. **Reset plugins (nuclear)** -> Run `/user-config:reset-plugins` - Complete plugin reset

## Directory Structure Reference

### ~/.claude/ Directory (13 Concepts)

| Directory/File | Purpose | Cleanup Safe | Command |
| --- | --- | --- | --- |
| `projects/` | Session files per project | Yes (old files) | `/user-config:cleanup-sessions` |
| `debug/` | Debug transcripts | Yes (old files) | `/user-config:cleanup-debug` |
| `plugins/` | Installed plugin cache | No (use /plugin) | `/plugin uninstall` |
| `file-history/` | Edit undo history | **No** (loses undo) | Never auto-clean |
| `plans/` | Saved execution plans | Yes (old files) | `/user-config:plans` |
| `shell-snapshots/` | Shell state captures | Yes | `/user-config:prune` |
| `todos/` | Todo list state | Yes (old files) | `/user-config:prune` |
| `statsig/` | Feature flag cache | Always safe | `/user-config:prune` |
| `ide/` | IDE lock files | Yes (stale) | `/user-config:audit` |
| `session-env/` | Session environment | Yes | `/user-config:prune` |
| `settings.json` | User settings | **Never** | Manual only |
| `history.jsonl` | Command history | Usually keep | `/user-config:history` |
| `.credentials.json` | OAuth tokens | **Never backup** | Manual only |

### ~/ Root Files (3 Concepts)

| File | Purpose | Backup Priority |
| --- | --- | --- |
| `.claude.json` | Global config (mcpServers, OAuth, flags) | **Critical** (mcpServers) |
| `CLAUDE.md` | User-level instructions | High |
| `.claudeignore` | User-level ignore patterns | Medium |

**IMPORTANT:** There is NO `~/.mcp.json` file. User-scope MCP servers go in `~/.claude.json` under the `mcpServers` field.

## Command Inventory

All commands consolidated under `/user-config:*` namespace:

### Cleanup Commands (Migrated)

| New Command | Was | Purpose |
| --- | --- | --- |
| `/user-config:cleanup-agents` | `/cleanup-agents` | Agent transcript cleanup (7d default) |
| `/user-config:cleanup-debug` | `/cleanup-debug` | Debug log cleanup (7d default) |
| `/user-config:cleanup-sessions` | `/cleanup-sessions` | Session file cleanup (7d default) |
| `/user-config:prune` | `/prune-cache` | Comprehensive cleanup (--nuclear) |
| `/user-config:cleanup-hook-logs` | `/cleanup-hook-logs` | Hook log cleanup (30d default) |
| `/user-config:storage` | `/check-claude-storage` | Storage analysis |
| `/user-config:session-stats` | `/session-stats` | Session statistics |

### New Commands

| Command | Purpose | Priority |
| --- | --- | --- |
| `/user-config:status` | Unified overview of all config | P0 |
| `/user-config:reset` | Backup MCP -> Wipe -> Restore workflow | P0 |
| `/user-config:audit` | Structure drift detection | P0 |
| `/user-config:backup` | Full backup to ~/.claude-backups/ | P1 |
| `/user-config:restore` | Restore from backup | P1 |
| `/user-config:history` | Search/export command history | P1 |
| `/user-config:plans` | List/view/archive plan files | P1 |
| `/user-config:global` | View/edit ~/.claude.json safely | P1 |
| `/user-config:mcp` | List/export MCP server configs | P1 |
| `/user-config:reset-plugins` | Complete plugin reset (cache + registry + settings) | P1 |

**Backward Compatibility:** Old command names work but show deprecation notice.

## Custom Workflows (Skill-Owned)

These workflows are NOT in official documentation - they are custom features:

### Reset Workflow (MCP Preservation)

For users who want a fresh start but need to preserve MCP server configs.

**Full guide:** [references/reset-workflow.md](references/reset-workflow.md)

**Quick summary:**

1. Backup: Extract mcpServers from ~/.claude.json
2. Backup: Copy settings.json (optional)
3. User wipes ~/.claude/ and ~/.claude.json
4. User relaunches Claude Code (creates fresh config)
5. Restore: Inject mcpServers into new ~/.claude.json

### Backup/Restore Workflow

For full configuration backup and restore.

**Full guide:** [references/backup-restore.md](references/backup-restore.md)

**Backup location:** `~/.claude-backups/backup-YYYY-MM-DD-HHmmss/`

### Drift Detection

Detect when Claude Code updates change the config structure.

**Full guide:** [references/known-structure.yaml](references/known-structure.yaml)

**Mechanism:** Compare actual ~/.claude/ against known structure manifest.

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "How do I clean up old sessions?"

1. Check command inventory (this skill)
2. Direct to: /user-config:cleanup-sessions
3. If user needs more detail, query docs-management: "cleanupPeriodDays", "session retention"
```

### Reset/Backup Pattern

```text
User asks: "I want to reset Claude Code but keep my MCP servers"

1. Load this skill's references/reset-workflow.md
2. Query docs-management for: "mcpServers", ".claude.json"
3. Guide user through reset workflow
```

### Troubleshooting Pattern

```text
User reports: "Storage is using too much disk space"

1. Run /user-config:storage for analysis
2. Recommend specific cleanup commands based on results
3. If needed, query docs-management for retention settings
```

## Cross-Platform Path Handling

All commands must handle paths cross-platform:

**Python:**

```python
from pathlib import Path
claude_dir = Path.home() / ".claude"
claude_json = Path.home() / ".claude.json"
backup_dir = Path.home() / ".claude-backups"
```

**Bash:**

```bash
CLAUDE_DIR="$HOME/.claude"
CLAUDE_JSON="$HOME/.claude.json"
BACKUP_DIR="$HOME/.claude-backups"
```

**Never hardcode:**

- `C:\Users\USERNAME\.claude\`
- `/Users/USERNAME/.claude/`
- `/home/USERNAME/.claude/`

## Retention Settings

### Official Setting (via docs-management)

**`cleanupPeriodDays`** in settings.json:

- Sessions inactive > N days deleted at startup
- Default: 30 days
- Setting to 0 = immediate deletion

Query docs-management: "cleanupPeriodDays", "session retention"

### Command Defaults

> **Note:** For official retention settings (like `cleanupPeriodDays`), query
> `docs-management: "cleanupPeriodDays session retention"`. The defaults below
> are this plugin's command defaults, not Claude Code's official defaults.

| Command | Default Retention |
| --- | --- |
| Cleanup commands | 7 days |
| Hook logs | 30 days |
| File history | Never auto-clean (dangerous) |

## Troubleshooting Quick Reference

| Issue | Solution |
| --- | --- |
| Storage too large | Run `/user-config:storage` then cleanup commands |
| Lost MCP servers after reset | Use `/user-config:reset` workflow (backs up first) |
| Unknown files in ~/.claude | Run `/user-config:audit` for drift detection |
| Can't find old session | Use `/user-config:history` to search |
| Need to restore config | Use `/user-config:restore` from backup |
| "Another Claude process running" | `/user-config:prune --nuclear` clears stale locks |

## Auditing Configuration

This skill provides validation criteria used by the `user-config-auditor` agent.

### Audit Checks

| Category | Checks |
| --- | --- |
| JSON Validity | All .json files parse correctly |
| Orphaned Files | Sessions without projects, stale locks |
| Security | No exposed API keys in settings |
| Structure | Known vs unknown directories/files |
| Cross-References | Todos reference valid sessions |

### Related Agent

The `user-config-auditor` agent performs formal audits:

- Uses this skill's known-structure.yaml for drift detection
- Validates JSON syntax
- Checks for orphaned/stale files
- Generates structured audit reports

## References

**Custom References (skill-owned):**

- [known-structure.yaml](references/known-structure.yaml) - Structure manifest for drift detection
- [reset-workflow.md](references/reset-workflow.md) - MCP preservation reset guide
- [backup-restore.md](references/backup-restore.md) - Backup/restore procedures
- [command-inventory.md](references/command-inventory.md) - Full command reference

**Official Documentation (via docs-management):**

- Query: "settings", "settings.json" - Settings structure
- Query: "mcpServers", ".claude.json" - MCP server configuration
- Query: "cleanupPeriodDays" - Retention settings

## Version History

- **v1.0.0** (2025-12-30): Initial release
  - Consolidated command namespace (user-config:*)
  - Reset workflow with MCP preservation
  - Drift detection manifest
  - Pure delegation for official docs
  - Custom references for plugin-specific features

---

## Last Updated

**Date:** 2025-12-30
**Model:** claude-opus-4-5-20251101
