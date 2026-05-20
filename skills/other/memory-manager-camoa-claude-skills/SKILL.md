---
name: memory-manager
description: Use after completing any phase activity - updates project_state.md, project registry, ensures files are in correct locations, maintains lean memory
version: 3.0.0
user-invocable: false
---

# Memory Manager

Maintain clean and organized project memory.

## Activation

Activate when:
- After completing any phase activity (research, design, implementation)
- After task completion
- When project state seems inconsistent
- Periodic maintenance requested
- "Clean up project files" or "Update project state"

## Workflow

### 1. Load Current State

Use `Read` on `{project_path}/project_state.md`

Extract:
- Current phase
- Last updated date
- Current focus
- Progress summary

### 2. Scan Project Files

**v3.0.0 Folder Structure Support:**

Use `Bash` with `ls -d` to inventory task directories:
```bash
# List task directories (not .md files)
ls -d {project_path}/implementation_process/in_progress/*/ 2>/dev/null
ls -d {project_path}/implementation_process/completed/*/ 2>/dev/null
```

For each task directory found, check for:
- `task.md` (main tracker) - required
- `research.md` (Phase 1 content) - optional
- `architecture.md` (Phase 2 content) - optional
- `implementation.md` (Phase 3 content) - optional

Also scan architecture folder:
```
{project_path}/architecture/*.md
```

Count:
- Component architectures (architecture/*.md)
- In-progress tasks (directories in in_progress/)
- Completed tasks (directories in completed/)

**Backward Compatibility:**

If `*.md` files found (not directories), warn:
```
⚠️  Old v2.x format detected: {count} single-file tasks

Run `/drupal-dev-framework:migrate-tasks` to upgrade to v3.0.0 folder structure.
```

### 3. Detect Inconsistencies

Check for issues:

| Issue | Detection | Fix |
|-------|-----------|-----|
| Empty files | File size = 0 | Ask to delete or populate |
| Orphaned tasks | Task in wrong folder | Move to correct location |
| Stale state | project_state.md outdated | Update current focus |
| Missing files | Referenced but not found | Create or update reference |

### 4. Update project_state.md

Use `Edit` to update:

```markdown
# {Project Name}

**Updated:** {today's date}
**Phase:** {detected phase}
**Status:** {current status}
**Path:** {project_path}

## Overview
{Keep existing or update based on recent work}

## Progress
- Phase 1 (Research): {Complete/In Progress} - {count} research files
- Phase 2 (Architecture): {Complete/In Progress} - {count} component files
- Phase 3 (Implementation): {X}/{Y} tasks complete

## Current Focus
{What's actively being worked on}

## Key Decisions
| Date | Decision | Rationale |
|------|----------|-----------|
{add new decisions, keep old ones}

## Next Steps
1. {Immediate next action}
2. {Following action}
```

### 5. Organize Files

If files are misplaced, use `Bash` to move:

**v3.0.0 Folder Structure:**
```bash
# Move completed task directory from in_progress
mv "{project_path}/implementation_process/in_progress/{task_name}/" \
   "{project_path}/implementation_process/completed/{task_name}/"
```

**v2.x Single Files (backward compatibility):**
```bash
# Move completed task file from in_progress
mv "{project_path}/implementation_process/in_progress/{task_name}.md" \
   "{project_path}/implementation_process/completed/{task_name}.md"
```

### 6. Clean Up

Ask before deleting anything:
```
Found {count} empty/orphaned files:
- {file 1}
- {file 2}

Delete these? (yes/no/review each)
```

### 7. Update Project Registry

Update the registry at `~/.claude/drupal-dev-framework/active_projects.json`:

1. Read the registry file
2. Find this project by path
3. Update:
   - `lastAccessed`: today's date
   - `status`: "active" or "archived" if all tasks complete
4. Write the updated registry

If project not in registry, offer to add it:
```
This project is not in the registry.
Add it for easier access next time? (yes/no)
```

### 8. Report

Show summary:
```
Memory cleanup complete:

Files scanned: {count}
Issues found: {count}
Issues fixed: {count}

Current state:
- Phase: {phase}
- Architecture files: {count}
- Tasks in progress: {count}
- Tasks completed: {count}

project_state.md updated.
Registry updated.
```

## Lean Memory Principles

Follow these rules:
- **One source of truth** - don't duplicate information
- **Summarize, don't copy** - reference external files
- **Archive, don't delete** - move to completed/, not trash
- **Update in place** - no versioned copies (main.md, not main_v2.md)

## Stop Points

STOP and wait for user:
- Before deleting any files
- Before major reorganization
- After presenting cleanup summary
