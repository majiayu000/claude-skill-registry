---
name: claude-cleaner
description: Diagnose slow Claude Code startup and guide cleanup. Use /bluera-base:clean to run.
---

# Claude Code Cleaner

Diagnose and fix slow Claude Code startup caused by accumulated configuration files.

## GLOBAL IMPACT WARNING

**This command modifies `~/.claude` - Claude Code's configuration directory.**

| Risk | Consequence |
|------|-------------|
| **Kills running plugins** | Clearing cache invalidates all cached plugins MID-SESSION. Hooks stop working immediately. |
| **Global scope** | Changes affect EVERY project, not just the current one |
| **Can corrupt config** | Bad writes to settings.json or .claude.json can break Claude entirely |

### Backup Location

All backups are stored in: **`~/.claude-backups/`**

```text
~/.claude-backups/
├── 2025-01-18T15-30-00/
│   ├── manifest.json          # What was backed up and why
│   ├── claude.json            # If auth-config was reset
│   └── projects.tgz           # If sessions were pruned
├── 2025-01-17T10-00-00/
│   └── ...
└── latest -> 2025-01-18T15-30-00/  # Symlink to most recent
```

### EXCLUDED FROM TEST-PLUGIN

**DO NOT** test this command via `/test-plugin`. It is explicitly excluded because:

- Running it automatically could destroy the session running the tests
- There's no safe way to test "delete files from ~/.claude" in CI

## When to Use

- Claude Code takes a long time to start
- Disk space is low due to `~/.claude` growth
- Performance degrades over time
- Error messages about Grove timeout or PowerShell

## Modes

| Mode | Purpose |
|------|---------|
| `/clean` | Interactive wizard with guided cleanup |
| `/clean scan` | Read-only scan, no changes |
| `/clean fix <action>` | Single action with preview and confirmation |
| `/clean backups list` | List available backups |
| `/clean backups restore <timestamp>` | Restore from a backup |

## Available Actions

| Action | Safety | Description |
|--------|--------|-------------|
| `DELETE-plugin-cache` | CAUTION | Remove plugin cache (plugins re-download on use) |
| `DELETE-old-sessions` | DESTRUCTIVE | Delete session files older than N days |
| `DELETE-debug-logs` | SAFE | Delete debug log files older than N days |
| `DELETE-auth-config` | DESTRUCTIVE | Backup and disable ~/.claude.json (requires re-login) |
| `disable-nonessential` | CAUTION | Set CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 |
| `set-cleanup-period` | SAFE | Set auto-cleanup period in settings.json |

## CRITICAL SAFETY PROTOCOL

### 1. ALWAYS Use AskUserQuestion Before Destructive Actions

```text
WRONG: Just run the command
python3 cc-cleaner-fix.py DELETE-plugin-cache --confirm

RIGHT: Preview first, ask, then confirm
1. python3 cc-cleaner-fix.py DELETE-plugin-cache       # Preview
2. Show preview to user with AskUserQuestion
3. Only if user confirms:
   python3 cc-cleaner-fix.py DELETE-plugin-cache --confirm
```

### 2. Show File Preview Before Any Deletion

Present to user:

- Exact file paths that will be deleted
- Size of each file/directory
- Age of files (for session/log cleanup)
- Total size to be freed
- Backup location

### 3. Verify Backup Before Confirming Success

After running with `--confirm`, check:

- Backup directory exists in `~/.claude-backups/`
- manifest.json was created
- Report backup path to user with restore command

## Interactive Workflow (`/clean`)

### Step 1: Warning Banner

Display the global impact warning prominently.

### Step 2: Run Scan

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-scan.py" --json
```

Parse JSON to get:

- `metrics`: sizes and file counts
- `findings`: issues found with risk levels
- `actions`: recommended actions with file previews

### Step 3: Display Results

Show:

- Total `~/.claude` size
- `~/.claude.json` size
- Findings table with [CRITICAL], [HIGH], [MEDIUM], [LOW] labels
- File counts and sizes for each finding

### Step 4: User Selects Actions

Use AskUserQuestion with multiSelect to let user choose which actions:

```text
Header: "Select Actions"
Question: "Which issues do you want to fix? (Backups created for all)"
Options (multiSelect: true):
  - "DELETE-plugin-cache (2.1 GB) - plugins re-download on use"
  - "DELETE-old-sessions (156 MB) - removes sessions >30 days"
  - "DELETE-debug-logs (45 MB)"
```

### Step 5: Preview Selected Actions

For each selected action, show detailed preview:

```text
Preview of DELETE-plugin-cache:

Files to be deleted:
  ~/.claude/plugins/cache/bluera/bluera-base/0.14.0  (180 MB)
  ~/.claude/plugins/cache/bluera/bluera-knowledge/0.17.1  (1.9 GB)
  ... (10 more plugins)

Total: 12 plugins, 2.1 GB
Backup: ~/.claude-backups/2025-01-18T15-30-00/
```

### Step 6: Final Confirmation

Use AskUserQuestion:

```text
Header: "Confirm Deletion"
Question: "Delete 2.3 GB across 2 actions? Backup will be created first."
Options:
  - "Yes, backup and delete"
  - "No, cancel everything"
```

### Step 7: Execute with Progress

```bash
# For each confirmed action:
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-fix.py" <action> --confirm --json
```

Report results:

- What was deleted
- Size freed
- Backup location
- Restore command

## Scan Mode (`/clean scan`)

Read-only scan:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-scan.py"
```

If issues found, suggest:

- `/clean` for interactive cleanup
- `/clean fix <action>` for specific fixes

## Fix Mode (`/clean fix <action>`)

Single action with preview and confirmation:

```bash
# Step 1: Preview (default - no --confirm)
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-fix.py" <action> --json

# Step 2: Show preview to user via AskUserQuestion

# Step 3: Execute (only after user confirms)
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-fix.py" <action> --confirm --json
```

Options:

- `--days N`: Days threshold for session/log cleanup (default: 30 for sessions, 14 for logs)
- `--json`: Output JSON for parsing
- `--confirm`: Actually execute (preview mode by default)

## Backup Management

### List Backups

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-fix.py" list-backups --json
```

Shows all backups with:

- Timestamp
- Action that created it
- Size
- Files backed up

### Restore from Backup

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/cc-cleaner-fix.py" restore-backup --timestamp 2025-01-18T15-30-00
```

Restores all files from the specified backup.

## Common Issues

### Plugin Cache Bloat (GB+ common)

**Symptoms**: Massive `~/.claude/plugins/cache` directory

**Cause**: Plugin cache accumulates multiple versions

**Fix**: `DELETE-plugin-cache` - plugins re-download on next use

**Warning**: Running plugins will break mid-session!

### Projects Directory Bloat

**Symptoms**: Large `~/.claude/projects` with many files

**Cause**: Session files accumulate over time

**Fix**:

- `set-cleanup-period --days 7` - auto-delete old sessions at startup
- `DELETE-old-sessions --days 30` - manual cleanup with backup

### Large ~/.claude.json

**Symptoms**: `~/.claude.json` grows to MB/GB

**Cause**: History accumulates

**Fix**: `DELETE-auth-config` - backup and disable (requires re-login)

### Grove Timeout Errors

**Symptoms**: Debug logs show "Grove notice config" timeout

**Cause**: Network configuration issues

**Fix**: `disable-nonessential` - disable non-essential network traffic

## Risk Levels

| Level | Meaning | Example Actions |
|-------|---------|-----------------|
| **SAFE** | No risk of data loss | DELETE-debug-logs, set-cleanup-period |
| **CAUTION** | May affect running session | DELETE-plugin-cache, disable-nonessential |
| **DESTRUCTIVE** | Deletes user data | DELETE-old-sessions, DELETE-auth-config |

## Typical Sizes

| Path | Normal | Concerning | Critical |
|------|--------|------------|----------|
| `~/.claude` total | <1GB | >5GB | >20GB |
| `~/.claude.json` | <100KB | >5MB | >100MB |
| `plugins/cache` | <100MB | >1GB | >10GB |
| `projects/` | <500MB | >2GB | >10GB |

## File Locations

```text
~/.claude/                    # Main config directory
├── settings.json             # User settings
├── plugins/cache/            # Plugin cache (safe to delete)
├── projects/                 # Session files per project
├── debug/                    # Debug logs
└── CLAUDE.md                 # User's global memory file

~/.claude.json                # Authentication & history

~/.claude-backups/            # Centralized backup location
├── YYYY-MM-DDTHH-MM-SS/      # Timestamped backup directories
│   ├── manifest.json         # Backup metadata
│   └── ...                   # Backed up files
└── latest -> ...             # Symlink to most recent
```

## Environment Variables

- `CLAUDE_CONFIG_DIR`: Override `~/.claude` location
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`: Disable telemetry
