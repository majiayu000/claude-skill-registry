---
name: marketplace-sync
description: Synchronize marketplace permissions - generate wildcards, manage executor permissions, and migrate to executor pattern.
allowed-tools: Read, Bash, Glob
---

# Marketplace Sync Skill

**PURPOSE**: Synchronize Claude Code permissions with marketplace bundles and manage the executor permission pattern.

## Script Reference

| Script | Notation | Purpose |
|--------|----------|---------|
| marketplace-sync | `plan-marshall:marketplace-sync:marketplace-sync` | Marketplace permission synchronization |

## Operations

### generate-wildcards - Generate Permission Wildcards

Generate Skill and SlashCommand wildcards from marketplace inventory.

```bash
# Read inventory from stdin
python3 .plan/execute-script.py plan-marshall:marketplace-inventory:scan-marketplace-inventory \
  --scope marketplace --resource-types skills,commands | \
python3 .plan/execute-script.py plan-marshall:marketplace-sync:marketplace-sync generate-wildcards

# Or from file
python3 .plan/execute-script.py plan-marshall:marketplace-sync:marketplace-sync generate-wildcards \
  --input inventory.json
```

**Output (JSON)**:
```json
{
  "statistics": {
    "bundles_scanned": 8,
    "skills_found": 28,
    "commands_found": 39,
    "wildcards_generated": 22
  },
  "permissions": {
    "skill_wildcards": ["Skill(pm-dev-builder:*)", "Skill(pm-workflow:*)"],
    "command_bundle_wildcards": ["SlashCommand(/pm-dev-builder:*)", "SlashCommand(/pm-workflow:*)"],
    "command_shortform": ["SlashCommand(/java-create:*)"]
  }
}
```

### ensure-executor - Ensure Executor Permission

Ensure the executor permission exists in settings.

```bash
python3 .plan/execute-script.py plan-marshall:marketplace-sync:marketplace-sync ensure-executor \
  --target global \
  --dry-run
```

**Output (JSON)**:
```json
{
  "executor_permission": "Bash(python3 .plan/execute-script.py *)",
  "settings_file": "/Users/name/.claude/settings.json",
  "action": "added",
  "success": true
}
```

### cleanup-scripts - Remove Redundant Script Permissions

Remove individual script path permissions (redundant with executor pattern).

```bash
python3 .plan/execute-script.py plan-marshall:marketplace-sync:marketplace-sync cleanup-scripts \
  --target global \
  --remove-broad-python \
  --dry-run
```

**Output (JSON)**:
```json
{
  "individual_script_permissions": ["Bash(python3 /path/to/scripts/foo.py:*)"],
  "individual_count": 5,
  "broad_python_found": true,
  "broad_python_removed": true,
  "action": "would_remove",
  "total_would_remove": 6
}
```

### migrate-executor - Full Migration to Executor Pattern

Complete migration: add executor permission + cleanup redundant permissions.

```bash
python3 .plan/execute-script.py plan-marshall:marketplace-sync:marketplace-sync migrate-executor \
  --target global \
  --remove-broad-python \
  --dry-run
```

**Output (JSON)**:
```json
{
  "success": true,
  "dry_run": true,
  "executor": {
    "permission": "Bash(python3 .plan/execute-script.py *)",
    "action": "added"
  },
  "cleanup": {
    "individual_removed": 5,
    "broad_python_removed": true
  },
  "summary": "Migrated to executor-only pattern: 1 permission replaces 5 individual script permissions"
}
```

## Executor Permission Pattern

The executor pattern uses a single permission for all marketplace scripts:
- `Bash(python3 .plan/execute-script.py *)`

This replaces individual script path permissions because the executor invokes scripts via subprocess (not checked by Claude Code permissions).

### Benefits
- **Single permission** instead of N permissions (one per script)
- **Automatic coverage** for new scripts when executor is regenerated
- **No permission prompts** when adding new skills/commands

### Migration Path
1. Run `ensure-executor` to add the executor permission
2. Run `cleanup-scripts` to remove redundant individual permissions
3. Or run `migrate-executor` to do both in one step

## Target Selection

| Target | File |
|--------|------|
| `global` | `~/.claude/settings.json` |
| `project` | `.claude/settings.json` or `.claude/settings.local.json` |

## Integration with Plan Marshall

The `plan-marshall` skill uses this during setup:

1. **Step 2: Generate Executor** - Creates `.plan/execute-script.py`
2. **Ensure Executor Permission** - Adds `Bash(python3 .plan/execute-script.py *)` to global settings

```bash
python3 .plan/execute-script.py plan-marshall:marketplace-sync:marketplace-sync ensure-executor \
  --target global
```

## Error Handling

All operations return JSON with error details:

```json
{
  "error": "Settings file not found: /path/to/settings.json",
  "success": false
}
```
