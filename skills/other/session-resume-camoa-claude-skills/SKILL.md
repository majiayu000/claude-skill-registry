---
name: session-resume
description: "Use when resuming work on existing project - lists registered projects, reads project_state.md, summarizes current state, identifies where to continue. Trigger: 'pick up where I left off', 'continue project', 'what was I working on', 'resume session'."
version: 1.2.0
allowed-tools: Read, Glob, Bash
---

# Session Resume

Restore context when starting a new session on an existing project.

## Current Branch
!`git branch --show-current 2>/dev/null`

## Activation

Activate when:
- Starting a new Claude session on existing project
- User says "Resume work on X" or "Continue X project"
- User provides project path for existing project
- "Where did we leave off?"

## Workflow

### 1. Locate Project

**First, check the project registry:**

Use `Read` on `~/.claude/drupal-dev-framework/active_projects.json`

If registry exists and has projects, show:
```
## Registered Projects

| # | Name | Phase | Last Accessed | Path |
|---|------|-------|---------------|------|
| 1 | {name} | Phase {N} | {date} | {path} |
| 2 | {name} | Phase {N} | {date} | {path} |

Enter number to resume, or 'new' for unregistered project:
```

If project path provided directly, use it.

If registry doesn't exist or is empty:
```
No registered projects found.

Enter the project path or name:
```

### 2. Load Project State

Use `Read` on `{project_path}/project_state.md`

If file not found:
```
No project_state.md found at {path}.

Options:
1. Different path
2. Initialize new project here
3. Cancel

Your choice:
```

### 3. Detect Current Phase

Invoke `phase-detector` skill to determine phase.

### 4. Load Current Focus

From project_state.md, extract:
- Current phase
- Current focus
- Recent key decisions
- Next steps listed

### 5. Scan Active Work

Use `Glob` to find:
```
{project_path}/implementation_process/in_progress/*.md
```

If tasks in progress, use `Read` on each to get:
- Task name
- Status
- Last progress notes

### 6. Present Resume Summary

Format as:
```
## Resuming: {Project Name}

### Project Path
{full_path}

### Current Phase
Phase {N} - {Research/Architecture/Implementation}

### Last Session Summary
{From project_state.md Current Focus}

### Key Decisions Made
- {Decision 1}
- {Decision 2}

### Where We Left Off
{Description of last activity}

### Active Tasks
| Task | Status | Progress |
|------|--------|----------|
| {task 1} | In Progress | {last note} |

### Suggested Next Action
{Based on project state and phase}

---
Ready to continue? What would you like to work on?
```

### 7. Load Task Context (If In Implementation)

If Phase 3 and tasks in progress, ask:
```
Active task: {task_name}

Load full context for this task? (yes/different task/overview first)
```

If yes, invoke `task-context-loader` for that task.

### 8. Update Registry

Update the project's `lastAccessed` date in `~/.claude/drupal-dev-framework/active_projects.json`.

Also update the `phase` field if it has changed based on phase detection.

### 9. Set Up Session

After user confirms direction:
- Load relevant architecture files
- Load relevant guides (if configured)
- Invoke appropriate skill for chosen activity

## Quick Resume

For rapid context restoration:
```
Quick resume: {project_name}
- Phase: {N}
- Focus: {current_focus}
- Active task: {task or "none"}
- Next: {suggested action}

Continue with {suggested action}? (yes/other)
```

## Stop Points

STOP and wait for user:
- After asking for project path (if not provided)
- After presenting resume summary
- After asking which task to continue
- Before loading full task context
