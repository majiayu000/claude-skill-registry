---
name: skill-refresh
description: Manage Claude Code resources - terminate orphaned processes and clean up ~/.claude/ directory
allowed-tools: Bash, AskUserQuestion
---

# Refresh Skill (Direct Execution)

Direct execution skill for managing Claude Code resources. Performs two operations:
1. **Process cleanup**: Identify and terminate orphaned Claude Code processes
2. **Directory cleanup**: Clean up accumulated files in ~/.claude/

This skill executes inline without spawning a subagent.

## Execution

### Step 1: Parse Arguments

Extract flags from command input:
- `--dry-run`: Preview mode
- `--force`: Skip confirmation, use 8-hour default

```bash
# Parse from command input
dry_run=false
force=false
if [[ "$*" == *"--dry-run"* ]]; then
  dry_run=true
fi
if [[ "$*" == *"--force"* ]]; then
  force=true
fi
```

### Step 2: Run Process Cleanup

Execute process cleanup script:

```bash
.claude/scripts/claude-refresh.sh $( [ "$force" = true ] && echo "--force" )
```

Store process cleanup output for display.

### Step 3: Clean Orphaned Postflight Markers

Clean any orphaned postflight coordination files from the specs directory. These files should normally be cleaned up by skills after postflight completes, but may be left behind if a process is interrupted.

```bash
echo ""
echo "=== Cleaning Orphaned Postflight Markers ==="
echo ""

# Find orphaned postflight markers (older than 1 hour)
orphaned_pending=$(find specs -maxdepth 3 -name ".postflight-pending" -mmin +60 -type f 2>/dev/null)
orphaned_guard=$(find specs -maxdepth 3 -name ".postflight-loop-guard" -mmin +60 -type f 2>/dev/null)

# Also check for legacy global markers
legacy_pending=""
legacy_guard=""
if [ -f "specs/.postflight-pending" ]; then
    legacy_pending="specs/.postflight-pending"
fi
if [ -f "specs/.postflight-loop-guard" ]; then
    legacy_guard="specs/.postflight-loop-guard"
fi

if [ -n "$orphaned_pending" ] || [ -n "$orphaned_guard" ] || [ -n "$legacy_pending" ] || [ -n "$legacy_guard" ]; then
    if [ "$dry_run" = true ]; then
        echo "Would delete the following orphaned markers:"
        [ -n "$orphaned_pending" ] && echo "$orphaned_pending"
        [ -n "$orphaned_guard" ] && echo "$orphaned_guard"
        [ -n "$legacy_pending" ] && echo "$legacy_pending"
        [ -n "$legacy_guard" ] && echo "$legacy_guard"
    else
        # Delete orphaned task-scoped markers
        find specs -maxdepth 3 -name ".postflight-pending" -mmin +60 -delete 2>/dev/null
        find specs -maxdepth 3 -name ".postflight-loop-guard" -mmin +60 -delete 2>/dev/null

        # Delete legacy global markers
        rm -f specs/.postflight-pending 2>/dev/null
        rm -f specs/.postflight-loop-guard 2>/dev/null

        echo "Cleaned orphaned postflight markers."
    fi
else
    echo "No orphaned postflight markers found."
fi
```

### Step 4: Run Directory Survey

Show current directory status without cleaning yet:

```bash
.claude/scripts/claude-cleanup.sh
```

This displays:
- Current ~/.claude/ directory size
- Breakdown by directory
- Space that can be reclaimed

### Step 5: Execute Based on Mode

#### Dry-Run Mode

If `--dry-run` is set:

```bash
echo ""
echo "=== DRY RUN MODE ==="
echo "Showing 8-hour cleanup preview..."
echo ""
.claude/scripts/claude-cleanup.sh --dry-run --age 8
```

Exit after showing preview.

#### Force Mode

If `--force` is set:

```bash
echo ""
echo "=== EXECUTING CLEANUP (8-hour default) ==="
echo ""
.claude/scripts/claude-cleanup.sh --force --age 8
```

Show results and exit.

#### Interactive Mode (Default)

If neither flag is set:

1. Check if cleanup candidates exist (claude-cleanup.sh exits with code 1 if candidates found)

2. If no candidates, display message and exit:
```
No cleanup candidates found within default thresholds.
All files are either protected or recently modified.
```

3. If candidates exist, prompt user for age selection:

```json
{
  "question": "Select cleanup age threshold:",
  "header": "Age Threshold",
  "multiSelect": false,
  "options": [
    {
      "label": "8 hours (default)",
      "description": "Remove files older than 8 hours - aggressive cleanup"
    },
    {
      "label": "2 days",
      "description": "Remove files older than 2 days - conservative cleanup"
    },
    {
      "label": "Clean slate",
      "description": "Remove everything except safety margin (1 hour)"
    }
  ]
}
```

4. Map user selection to age parameter:
   - "8 hours (default)" → `--age 8`
   - "2 days" → `--age 48`
   - "Clean slate" → `--age 0`

5. Execute cleanup with selected age:

```bash
case "$selection" in
  "8 hours (default)")
    .claude/scripts/claude-cleanup.sh --force --age 8
    ;;
  "2 days")
    .claude/scripts/claude-cleanup.sh --force --age 48
    ;;
  "Clean slate")
    .claude/scripts/claude-cleanup.sh --force --age 0
    ;;
esac
```

6. Display cleanup results

---

## Example Execution Flows

### Interactive Flow

```bash
# User runs: /refresh

# Output:
Claude Code Refresh
===================

No orphaned processes found.
All 3 Claude processes are active sessions.

---

Claude Code Directory Cleanup
=============================

Target: ~/.claude/

Current total size: 7.3 GB

Scanning directories...

Directory                   Total    Cleanable    Files
----------                -------   ----------    -----
projects/                  7.0 GB       6.5 GB      980
debug/                   151.0 MB     140.0 MB      650
...

TOTAL                      7.3 GB       6.7 GB     5577

Space that can be reclaimed: 6.7 GB

# Prompt appears:
[Age Threshold]
Select cleanup age threshold:
  1. 8 hours (default) - Remove files older than 8 hours
  2. 2 days - Remove files older than 2 days
  3. Clean slate - Remove everything except safety margin

# User selects option 1

# Cleanup executes:
Cleanup Complete
================
Deleted: 5577 files
Failed:  0 files
Space reclaimed: 6.7 GB

New total size: 600.0 MB
```

### Dry-Run Flow

```bash
# User runs: /refresh --dry-run

# Shows survey, then:
=== DRY RUN MODE ===
Showing 8-hour cleanup preview...

Would delete: 5577 files
Would reclaim: 6.7 GB

Dry Run Summary
===============
No changes made.
```

### Force Flow

```bash
# User runs: /refresh --force

# Shows survey, then immediately:
=== EXECUTING CLEANUP (8-hour default) ===

Cleanup Complete
================
Deleted: 5577 files
Space reclaimed: 6.7 GB
```

---

## Safety Measures

### Protected Files (Never Deleted)

- `sessions-index.json` (in each project directory)
- `settings.json`
- `.credentials.json`
- `history.jsonl`

### Safety Margin

Files modified within the last hour are **never deleted**, regardless of age threshold.

### Process Safety

- Only targets orphaned processes (TTY = "?")
- Never kills active sessions
- Excludes current process tree

---

## Error Handling

### Scripts Not Found

If scripts don't exist:
```
Error: Cleanup scripts not found at .claude/scripts/
Please ensure claude-refresh.sh and claude-cleanup.sh are installed.
```

### Permission Denied

If kill/delete fails due to permissions:
```
Warning: Some operations failed due to insufficient permissions.
Failed files: 5
Successfully deleted: 5572 files
```

### No ~/.claude/ Directory

If directory doesn't exist:
```
Error: ~/.claude/ directory not found.
Nothing to clean up.
```
