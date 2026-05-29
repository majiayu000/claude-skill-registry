---
name: update-task-board
description: Manage TASK_BOARD.md by reading project logs and synchronizing task status. Use when tasks are completed, when progress is made, or when needing to sync task tracking. Reads MIGRATION_LOG.md, DEBUG_LOG.md, GIT_LOG.md to assess actual progress and updates TASK_BOARD.md accordingly. Does NOT modify CLAUDE.md or MIGRATION_LOG.md.
---

# Task Board Manager

Manage TASK_BOARD.md by synchronizing it with actual project progress from various log files.

## Core Responsibility

**Manage TASK_BOARD.md ONLY** - This skill:
- ✅ Reads: MIGRATION_LOG.md, DEBUG_LOG.md, GIT_LOG.md, git status
- ✅ Updates: TASK_BOARD.md
- ❌ Does NOT modify: CLAUDE.md, MIGRATION_LOG.md, or other files

**Clear separation:**
- `update-task-board` → Manages TASK_BOARD.md
- `update-migration-log` → Manages MIGRATION_LOG.md only
- CLAUDE.md → Entry point, rarely modified

## When to Use

Use this skill when:
- Completing tasks and need to update task board
- Starting new tasks and want to track them
- Syncing project status after work sessions
- Reviewing overall project progress
- Preparing status reports
- Identifying task-log inconsistencies

## Workflow

### Step 1: Read All Logs

Read project documentation to understand current state:

**Files to read:**
1. **TASK_BOARD.md** - Current task status
2. **MIGRATION_LOG.md** - Migration progress
3. **DEBUG_LOG.md** - Active/resolved issues
4. **GIT_LOG.md** - Recent commits
5. **Git status** - Uncommitted changes

### Step 2: Analyze Progress

Compare documented tasks with actual progress:

**Check for:**
- Completed tasks with log evidence
- In-progress tasks that may be complete
- New tasks mentioned in logs
- Resolved blockers
- Migration progress updates

### Step 3: Update TASK_BOARD.md

Update sections based on analysis:

**Sections:**
- **Completed ✅** - Move finished tasks here
- **In Progress 🚧** - Current work
- **Next Steps 📋** - Upcoming priorities
- **Blockers 🚫** - Issues preventing progress

### Step 4: Verify Consistency

Ensure logs and task board tell consistent story:

**Cross-reference:**
- Migration entries match completed migration tasks
- Resolved DEBUG_LOG issues match removed blockers
- Recent commits relate to completed tasks
- No contradictions

## TASK_BOARD.md Structure

### Task Status Sections

**Completed:**
```markdown
### Completed ✅

**Phase 1: Minimal Migration**
- [x] Task description
- [x] Another completed task

**Phase 2: Refactoring**
- [x] Architecture refactored
```

**In Progress:**
```markdown
### 🚧 In Progress

### Current Focus
- [ ] Task being worked on

### Details
- Subtask details
- Progress notes
```

**Next Steps:**
```markdown
### 📋 Next Steps

### Phase 2 Completion
1. [ ] Task to do next
2. [ ] Another upcoming task

### Phase 3 Planning
1. [ ] Future work
```

**Blockers:**
```markdown
### 🚫 Blockers

**Current:** Description of active blocker

**Resolved:**
- ~~Previous blocker~~ - Fixed YYYY-MM-DD
```

## Log Integration

### MIGRATION_LOG.md

**Extract:**
- Recent migration entries
- Files completed
- Issues encountered

**Actions:**
- Mark migration tasks complete
- Add migration-related blockers
- Update phase progress

### DEBUG_LOG.md

**Extract:**
- Active issues
- Resolved issues
- Issue severity

**Actions:**
- Add significant issues to Blockers
- Remove resolved blockers
- Track debugging tasks

### GIT_LOG.md

**Extract:**
- Recent commits
- Modified files
- Commit patterns

**Actions:**
- Identify completed work
- Cross-reference with tasks
- Add untracked completed work

## Update Patterns

### Task Completion

When log evidence shows task is done:

```markdown
**Before (In Progress):**
- [ ] Implement unified Solver interface

**After (Completed):**
- [x] Implement unified Solver interface
```

Add to appropriate phase section in Completed.

### New Task

When new task identified:

```markdown
### 🚧 In Progress

### Current Focus
- [ ] Fix matplotlib import issues on Windows

### Details
- Identified from DEBUG_LOG.md
- Platform compatibility issue
```

### Blocker Resolution

When blocker is fixed:

```markdown
**Resolved:**
- ~~Dependency conflict numpy/pandas~~ - Fixed 2026-01-03
```

Move from "Current" to "Resolved" in Blockers section.

## Integration with Other Skills

**Works with:**
- `update-migration-log` - Reads MIGRATION_LOG.md for evidence
- `log-debug-issue` - Reads DEBUG_LOG.md for blockers
- `git-log` - Reads GIT_LOG.md for commits
- `build-session-context` - Reads TASK_BOARD.md for status

**Does NOT interfere with:**
- CLAUDE.md management (not this skill's job)
- Migration logging (update-migration-log handles)
- Debug logging (log-debug-issue handles)

## Evidence-Based Updates

**Principles:**
- Only mark complete with log evidence
- Cite sources when updating
- Be conservative - when uncertain, keep in-progress
- Cross-reference multiple logs

**Example:**
```
Task: "Migrate instance.py"
Evidence: MIGRATION_LOG.md entry dated 2026-01-01
Action: Move to Completed ✅ with date reference
```

## Usage Examples

### Example 1: Migration Complete

**Situation:** MIGRATION_LOG.md shows "instance.py migration completed"

**Actions:**
1. Find task in TASK_BOARD.md "In Progress"
2. Move to "Completed" under appropriate phase
3. Mark [x] as complete
4. Update "Last Updated" date in TASK_BOARD.md
5. Update progress metrics

### Example 2: Bug Resolved

**Situation:** DEBUG_LOG.md shows issue marked "Resolved"

**Actions:**
1. Find blocker in TASK_BOARD.md "Blockers" section
2. Move to "Resolved" subsection
3. Add resolution date
4. Update "Last Updated"

### Example 3: New Work Started

**Situation:** GIT_LOG.md shows commits for new feature

**Actions:**
1. Check if task exists in TASK_BOARD.md
2. If not, add to "In Progress" with details
3. If complete, add to "Completed"
4. Update "Last Updated"

## File References

- **Manages:** `.claude/TASK_BOARD.md`
- **Reads:** `.claude/MIGRATION_LOG.md`, `.claude/DEBUG_LOG.md`, `.claude/GIT_LOG.md`
- **Does NOT modify:** `.claude/CLAUDE.md`, `.claude/MIGRATION_LOG.md`

## Maintenance Notes

**Update frequency:**
- After completing tasks
- After work sessions
- Weekly for comprehensive review
- At project milestones

**Keep TASK_BOARD.md:**
- Up to date with logs
- Consistent across sections
- Clear and actionable
- Evidence-based
