---
name: sync-tasks
description: Sync tasks.md with actual completion status (GitHub issue or reality check)
---

# Sync Tasks Status

**Purpose**: Fix tasks.md when it's out of sync with reality (GitHub issue, git history, or actual files).

**Use When**:
- `/progress` shows wrong completion %
- GitHub issue says 24/24 but tasks.md says 1/24
- After manually completing work without updating tasks.md

---

## How It Works

1. **Detect Active Increment**
   - Find increment in-progress
   - Check if tasks.md exists

2. **Compare Sources**
   - **tasks.md**: Current status
   - **GitHub issue** (if synced): Checklist status
   - **Git history**: What files were actually changed/created
   - **File system**: What files exist

3. **Show Diff**
   ```
   Sync Status Check:

   tasks.md:       5/24 complete (21%)
   GitHub #4:      24/24 complete (100%) ✓ TRUTH
   Git commits:    24 task commits found

   Mismatch detected! tasks.md is stale.
   ```

4. **Offer Fix**
   ```
   Options:
   1. Auto-sync from GitHub issue (recommended)
   2. Auto-sync from git history
   3. Manual review (show each task)
   4. Cancel
   ```

5. **Update tasks.md**
   - Mark completed tasks as [x]
   - Update progress counters
   - Commit changes

---

## Usage

```bash
# Auto-detect and sync
/sw:sync-tasks

# Sync specific increment
/sw:sync-tasks 0007

# Force sync from GitHub (skip git check)
/sw:sync-tasks --source=github

# Dry run (show what would change)
/sw:sync-tasks --dry-run
```

---

## Implementation Steps

### Step 1: Find Active Increment

```bash
ACTIVE_INCREMENT=$(find .specweave/increments -name "tasks.md" -exec grep -l "Status: In Progress" {} \; | head -1)

if [[ -z "$ACTIVE_INCREMENT" ]]; then
    echo "No active increment found"
    exit 0
fi

INCREMENT_DIR=$(dirname "$ACTIVE_INCREMENT")
INCREMENT_ID=$(basename "$INCREMENT_DIR" | grep -oE "^[0-9]+")
```

### Step 2: Get GitHub Issue Status (if exists)

```bash
# Check if GitHub sync is enabled
GITHUB_ISSUE=$(grep "github-issue:" "$INCREMENT_DIR/spec.md" | cut -d':' -f2 | tr -d ' ')

if [[ -n "$GITHUB_ISSUE" ]]; then
    # Fetch issue body
    ISSUE_BODY=$(gh issue view "$GITHUB_ISSUE" --json body --jq '.body')

    # Count completed checkboxes
    GH_TOTAL=$(echo "$ISSUE_BODY" | grep -c "^- \[")
    GH_COMPLETE=$(echo "$ISSUE_BODY" | grep -c "^- \[x\]")

    echo "GitHub Issue #$GITHUB_ISSUE: $GH_COMPLETE/$GH_TOTAL complete"
else
    echo "No GitHub issue linked (skipping GitHub sync)"
fi
```

### Step 3: Get tasks.md Status

```bash
TASKS_TOTAL=$(grep -c "^#### T-" "$INCREMENT_DIR/tasks.md")
TASKS_COMPLETE=$(grep -A1 "^#### T-" "$INCREMENT_DIR/tasks.md" | grep -c "\*\*Status\*\*: \[x\] completed")

echo "tasks.md: $TASKS_COMPLETE/$TASKS_TOTAL complete"
```

### Step 4: Detect Mismatch

```bash
if [[ "$GH_COMPLETE" -ne "$TASKS_COMPLETE" ]]; then
    echo "⚠️ Mismatch detected!"
    echo "  GitHub:    $GH_COMPLETE/$GH_TOTAL"
    echo "  tasks.md:  $TASKS_COMPLETE/$TASKS_TOTAL"
    echo ""

    # Offer to sync
    read -p "Sync tasks.md from GitHub issue? (y/n): " CONFIRM

    if [[ "$CONFIRM" == "y" ]]; then
        sync_from_github "$INCREMENT_DIR" "$GITHUB_ISSUE"
    fi
else
    echo "✓ tasks.md is in sync with GitHub issue"
fi
```

### Step 5: Sync From GitHub

```bash
sync_from_github() {
    local increment_dir="$1"
    local github_issue="$2"

    # Parse GitHub issue checklist
    gh issue view "$github_issue" --json body --jq '.body' | while IFS= read -r line; do
        if [[ "$line" =~ ^\-\ \[x\]\ (T-[0-9]{3}) ]]; then
            # Task is complete in GitHub, mark in tasks.md
            TASK_ID="${BASH_REMATCH[1]}"
            mark_task_complete "$increment_dir" "$TASK_ID"
        fi
    done

    # Recalculate progress
    recalculate_progress "$increment_dir"

    echo "✓ Synced tasks.md from GitHub issue #$github_issue"
}

mark_task_complete() {
    local increment_dir="$1"
    local task_id="$2"

    # Find task and update status
    sed -i '' "/^#### $task_id:/,/^\*\*Status\*\*:/ s/\*\*Status\*\*: \[ \] pending/\*\*Status\*\*: [x] completed/" "$increment_dir/tasks.md"
}

recalculate_progress() {
    local increment_dir="$1"

    local total=$(grep -c "^#### T-" "$increment_dir/tasks.md")
    local completed=$(grep -A1 "^#### T-" "$increment_dir/tasks.md" | grep -c "\*\*Status\*\*: \[x\] completed")
    local progress=$((completed * 100 / total))

    # Update header
    sed -i '' "s/\*\*Completed\*\*: [0-9]*/\*\*Completed\*\*: $completed/" "$increment_dir/tasks.md"
    sed -i '' "s/\*\*Progress\*\*: [0-9]*%/\*\*Progress\*\*: $progress%/" "$increment_dir/tasks.md"

    echo "✓ Progress updated: $completed/$total ($progress%)"
}
```

---

## Example Output

```
🔄 Syncing tasks.md status...

Active Increment: 0007-smart-increment-discipline

Status Comparison:
├─ tasks.md:      1/24 complete (4%)
├─ GitHub #4:     24/24 complete (100%)
└─ Mismatch:      23 tasks out of sync ⚠️

Sync Source:
✓ GitHub issue #4 (most reliable)

Updating tasks.md...
├─ T-001: [ ] → [x] ✓
├─ T-002: [ ] → [x] ✓
├─ T-003: [ ] → [x] ✓
...
└─ T-024: [ ] → [x] ✓

Progress recalculated:
├─ Completed: 1 → 24
├─ Progress: 4% → 100%
└─ Status: In Progress → Complete

✓ tasks.md synced successfully!

Next: Run /sw:progress to verify
```

---

## Integration with Other Commands

### /sw:progress
```bash
# Check sync status before showing progress
/sw:sync-tasks --validate
# If out of sync, warn user
```

### /sw:validate
```bash
# Validate tasks.md is in sync
/sw:sync-tasks --validate
# Fail validation if mismatch detected
```

### /sw:done
```bash
# Ensure tasks.md is current before closing
/sw:sync-tasks --auto
# Auto-sync if needed, then proceed
```

---

## Success Criteria

- ✅ Detects when tasks.md is out of sync
- ✅ Syncs from GitHub issue (if available)
- ✅ Syncs from git history (fallback)
- ✅ Updates progress counters accurately
- ✅ Commits changes with clear message
- ✅ Integrates with /sw:progress, /sw:validate, /sw:done

---

**This command ensures `/progress` and `/done` always show accurate status!**
