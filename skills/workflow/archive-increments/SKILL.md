---
name: archive-increments
description: Intelligent increment archiving expert that analyzes age, status, and activity to recommend archiving. Use when workspace has too many increments, cleaning up completed work, or organizing the _archive folder. Follows the 10-10-10 rule for workspace organization.
---

# Increment Archive Manager

Expert at keeping the `.specweave/increments/` folder clean and organized through intelligent archiving.

## Core Knowledge

### Archiving Philosophy

**The 10-10-10 Rule**:
- **10 Active**: Keep last 10 increments readily accessible
- **10 Days**: Archive increments inactive for >10 days
- **10 Seconds**: Archive operation should take <10 seconds

### Archive Structure

```
.specweave/increments/
├── 0023-0032 (Active)          ← Last 10 increments
├── _archive/                   ← Completed/old increments
│   ├── 0001-0022              ← Historical increments
│   └── 0029                   ← Abandoned experiments
└── _abandoned/                 ← Failed/obsolete increments
```

### Smart Detection Rules

#### Never Archive
- **Active increments** (status: active)
- **Paused increments** (status: paused) - may resume
- **Recent increments** (last 10 by default)
- **Increments with open GitHub/JIRA/ADO issues**
- **Increments with uncommitted changes**

#### Always Archive
- **Completed >60 days ago**
- **No activity >30 days** (and status: completed)
- **Superseded increments** (replaced by newer version)
- **Failed experiments** (after confirmation)

#### Smart Grouping
- **Release groups**: Archive all v0.7.x after v0.8.0 ships
- **Feature groups**: Archive related increments together
- **Time-based**: Quarter/month-based archiving

## Usage Patterns

### Keep Workspace Clean
```bash
# Interactive archiving - prompts for confirmation
/sw:archive-increments

# Keep only last 5 increments
/sw:archive-increments --keep-last 5

# Archive all completed increments
/sw:archive-increments --archive-completed
```

### Prepare for Release
```bash
# Archive all pre-release increments
/sw:archive-increments --pattern "v0.7"

# Archive by date range
/sw:archive-increments --older-than 30d
```

### Restore from Archive
```bash
# List archived increments
/sw:archive-increments --list-archived

# Restore specific increment
/sw:archive-increments --restore 0015
```

## Configuration

### Default Settings
```json
{
  "archiving": {
    "keepLast": 10,              // Keep last 10 increments
    "autoArchive": false,        // Manual by default
    "archiveAfterDays": 60,      // Archive after 60 days
    "preserveActive": true,      // Never archive active
    "archiveCompleted": false    // Manual control
  }
}
```

### Aggressive Cleanup
```json
{
  "archiving": {
    "keepLast": 5,               // Minimal workspace
    "autoArchive": true,         // Auto-archive on completion
    "archiveAfterDays": 14,      // Archive after 2 weeks
    "archiveCompleted": true     // Auto-archive completed
  }
}
```

## Archive Statistics

### Current State Analysis
When asked about archiving, I analyze:
- Number of active increments
- Age of oldest active increment
- Total size of increments folder
- Number of completed increments
- External sync status

### Recommendations
Based on analysis, I suggest:
- **Overcrowded** (>20 active): Archive all but last 10
- **Stale** (many >30 days old): Archive by age
- **Post-release**: Archive previous version increments
- **Large size** (>100MB): Archive largest completed increments

## Safety Features

### Pre-Archive Checks
1. **Metadata validation**: Check increment status
2. **External sync**: Verify no open issues
3. **Git status**: Check for uncommitted changes
4. **Dependencies**: Check if referenced by active increments
5. **User confirmation**: Show what will be archived

### Archive Operations
- **Atomic moves**: Use fs.move with overwrite protection
- **Preserve structure**: Maintain full increment structure
- **Update references**: Fix links in living docs
- **Reversible**: Easy restore from archive
- **Audit trail**: Log all archive operations

## Smart Suggestions

### When to Archive
- **After major release**: Archive all pre-release increments
- **Quarterly cleanup**: Archive increments >3 months old
- **Before new project phase**: Archive previous phase work
- **Low disk space**: Archive largest completed increments

### Archive Patterns
- **By version**: `--pattern "v0.7"` (all v0.7.x increments)
- **By feature**: `--pattern "auth|login"` (auth-related)
- **By date**: `--older-than 30d` (time-based)
- **By status**: `--archive-completed` (all completed)

## Integration Points

### Status Line
- Shows "23-32 (10 active, 22 archived)" format
- Warns when >15 active increments
- Suggests archiving when appropriate

### Increment Commands
- `/sw:done` can trigger auto-archive
- `/sw:status` shows archive statistics
- `/sw:next` considers archived increments

### Living Docs
- Archive preserves living docs references
- Restore updates living docs links
- Archive included in docs statistics

## Best Practices

1. **Regular Cleanup**: Archive monthly or after releases
2. **Keep Recent**: Always keep last 5-10 increments
3. **Preserve Active**: Never force-archive active work
4. **Group Related**: Archive feature groups together
5. **Document Reasons**: Add archive notes for context

## Quick Reference

```bash
# Archive old increments
/sw:archive-increments --older-than 30d

# Keep workspace minimal
/sw:archive-increments --keep-last 5

# Archive after release
/sw:archive-increments --pattern "pre-release"

# Restore for reference
/sw:archive-increments --restore 0015

# Check archive stats
/sw:archive-increments --stats
```
## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/archive-increments.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

