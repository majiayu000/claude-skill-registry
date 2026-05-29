---
name: permission-fix
description: Write operations for fixing and managing Claude Code permissions - add, remove, consolidate, ensure, apply-fixes.
allowed-tools: Read, Bash, Glob
---

# Permission Fix Skill

**PURPOSE**: Write operations for fixing and managing Claude Code permissions.

**COMPLEMENTARY SKILL**: Use `plan-marshall:permission-doctor` for read-only analysis before applying fixes.

## Script Reference

| Script | Notation | Purpose |
|--------|----------|---------|
| permission-fix | `plan-marshall:permission-fix:permission-fix` | Write operations for permissions |

## Operations

### apply-fixes - Apply Safe Fixes

Normalize paths, remove duplicates, sort, and add default permissions.

```bash
python3 .plan/execute-script.py plan-marshall:permission-fix:permission-fix apply-fixes \
  --settings ~/.claude/settings.json \
  --dry-run
```

**Output (JSON)**:
```json
{
  "duplicates_removed": 2,
  "paths_fixed": 1,
  "defaults_added": ["Edit(.plan/**)", "Write(.plan/**)"],
  "sorted": true,
  "changes_made": true,
  "dry_run": true
}
```

### add - Add Permission

Add a single permission to settings.

```bash
python3 .plan/execute-script.py plan-marshall:permission-fix:permission-fix add \
  --permission "Bash(docker:*)" \
  --target project
```

**Output (JSON)**:
```json
{
  "success": true,
  "action": "added",
  "settings_file": "/path/to/.claude/settings.json"
}
```

### remove - Remove Permission

Remove a single permission from settings.

```bash
python3 .plan/execute-script.py plan-marshall:permission-fix:permission-fix remove \
  --permission "Bash(docker:*)" \
  --target project
```

**Output (JSON)**:
```json
{
  "success": true,
  "action": "removed",
  "settings_file": "/path/to/.claude/settings.json"
}
```

### ensure - Ensure Permissions Exist

Ensure multiple permissions exist (add missing, skip existing).

```bash
python3 .plan/execute-script.py plan-marshall:permission-fix:permission-fix ensure \
  --permissions "Bash(git:*),Bash(npm:*),Bash(docker:*)" \
  --target global
```

**Output (JSON)**:
```json
{
  "success": true,
  "added": ["Bash(docker:*)"],
  "already_exists": ["Bash(git:*)", "Bash(npm:*)"],
  "added_count": 1,
  "total_permissions": 45
}
```

### consolidate - Consolidate Timestamped Permissions

Replace timestamped permissions with wildcards.

```bash
python3 .plan/execute-script.py plan-marshall:permission-fix:permission-fix consolidate \
  --settings ~/.claude/settings.json \
  --dry-run
```

**Output (JSON)**:
```json
{
  "consolidated": 5,
  "removed": ["Read(target/output-2024-01-01.log)", "..."],
  "wildcards_added": ["Read(target/output-*.log)"],
  "dry_run": true
}
```

### ensure-wildcards - Ensure Marketplace Wildcards

Ensure all marketplace bundle wildcards exist in settings.

```bash
python3 .plan/execute-script.py plan-marshall:permission-fix:permission-fix ensure-wildcards \
  --settings ~/.claude/settings.json \
  --marketplace-json marketplace/.claude-plugin/marketplace.json \
  --dry-run
```

**Output (JSON)**:
```json
{
  "added": ["Skill(new-bundle:*)", "SlashCommand(/new-bundle:*)"],
  "already_present": 14,
  "total": 16,
  "dry_run": true
}
```

## Target Selection

Both `add`, `remove`, and `ensure` support `--target`:

| Target | File |
|--------|------|
| `global` | `~/.claude/settings.json` |
| `project` | `.claude/settings.json` or `.claude/settings.local.json` |

## Dry Run

All write operations support `--dry-run` to preview changes without modifying files.

## Integration with Permission Doctor

Recommended workflow:

1. **Analyze first**: Use `permission-doctor detect-redundant` or `detect-suspicious`
2. **Review findings**: Check the analysis output
3. **Apply fixes**: Use `permission-fix apply-fixes` or specific operations
4. **Verify**: Re-run analysis to confirm fixes

## Default Permissions

`apply-fixes` automatically adds these if missing:

| Permission | Reason |
|------------|--------|
| `Edit(.plan/**)` | Plan file modifications |
| `Write(.plan/**)` | Plan file creation |
| `Read(~/.claude/plugins/cache/**)` | Skills reference files via relative paths |

## Error Handling

All operations return JSON with error details:

```json
{
  "error": "Settings file not found: /path/to/settings.json",
  "success": false
}
```
