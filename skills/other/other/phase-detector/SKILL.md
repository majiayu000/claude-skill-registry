---
name: phase-detector
description: Use when determining task phase - analyzes task file to identify Phase 1, 2, or 3 for a specific task
version: 3.0.0
user-invocable: false
allowed-tools: Read, Glob
---

# Phase Detector

Analyze a task file to determine its current development phase.

## Key Concept

**Phases apply to TASKS, not projects.** A project has requirements (gathered once), then contains multiple tasks. Each task independently progresses through phases.

## Activation

Activate when:
- Invoked by `project-orchestrator` agent
- Checking status of a specific task
- "What phase is this task in?"
- Determining next action for a task

## Phase Definitions (Per Task)

| Phase | Focus | Code? |
|-------|-------|-------|
| 1 - Research | Understand requirements, research solutions | NO |
| 2 - Architecture | Design approach, patterns, decisions | NO |
| 3 - Implementation | Build with TDD, interactive coding | YES |

## Workflow

### 1. Identify Task

Get task name from:
- User request
- Current in_progress task
- project_state.md "Current Task" field

### 2. Locate Task Directory (v3.0.0)

Check for task directory at:
```
{project_path}/implementation_process/in_progress/{task_name}/
```

If not found, check:
```
{project_path}/implementation_process/completed/{task_name}/
```

If neither exists, check for **v2.x single file** (backward compatibility):
```
{project_path}/implementation_process/in_progress/{task_name}.md
{project_path}/implementation_process/completed/{task_name}.md
```

If nothing found, task hasn't started yet → Phase 0 (Not Started)

### 3. Analyze Task Content

**v3.0.0 Folder Structure:**

Use `Bash` to check for phase files:
```bash
# Check which phase files exist
[ -f "{task_name}/task.md" ] && echo "tracker"
[ -f "{task_name}/research.md" ] && echo "research"
[ -f "{task_name}/architecture.md" ] && echo "architecture"
[ -f "{task_name}/implementation.md" ] && echo "implementation"
```

Then use `Read` on `{task_name}/task.md` to check:

**Phase 1 Complete Indicators:**
- [ ] `research.md` file exists
- [ ] Phase Status shows "[x] Phase 1: Research"
- [ ] Link to research.md present

**Phase 2 Complete Indicators:**
- [ ] `architecture.md` file exists
- [ ] Phase Status shows "[x] Phase 2: Architecture"
- [ ] Link to architecture.md present

**Phase 3 Progress Indicators:**
- [ ] `implementation.md` file exists
- [ ] Phase Status shows "[ ] Phase 3: Implementation" (in progress)
- [ ] Some acceptance criteria may be checked

**v2.x Single File (backward compatibility):**

If single `.md` file found, check for sections:
- `## Research` section exists → Phase 1 complete
- `## Architecture` section exists → Phase 2 complete
- `## Implementation` section exists → Phase 3 in progress

### 4. Determine Phase

```
Task file doesn't exist?
→ Phase 0: Not Started - "Create task and begin research"

Task file exists but no Research section?
→ Phase 1: Research - "Research this task"

Research complete but no Architecture section?
→ Phase 2: Architecture - "Design architecture for this task"

Architecture complete?
→ Phase 3: Implementation - "Implement this task"

All checkboxes complete?
→ Done - "Complete this task"
```

### 5. Return Result

Format output as:
```
## Task Phase: {task_name}

**Phase:** {0/1/2/3} - {Not Started/Research/Architecture/Implementation}
**Status:** {Not Started/In Progress/Complete}

### Evidence
| Section | Found | Content |
|---------|-------|---------|
| Research | Yes/No | {summary or "Empty"} |
| Architecture | Yes/No | {summary or "Empty"} |
| Implementation | Yes/No | {progress or "Empty"} |

### Next Action
{What to do next for this task}

### Command
{Suggested command to run}
```

## Project-Level Status

When checking overall project status, summarize all tasks:

```
## Project: {project_name}

### Requirements
{Complete / Not gathered}

### Task Summary
| Task | Phase | Status | Next Action |
|------|-------|--------|-------------|
| {task1} | 3 | In Progress | Continue implementation |
| {task2} | 1 | In Progress | Complete research |
| {task3} | 0 | Queued | Start research |

### Completed Tasks
- {task_a} ✓
- {task_b} ✓
```

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No task specified | List all tasks with their phases |
| Task not found | Offer to create it |
| Task in completed/ | Report as done |
| Multiple tasks in progress | Show all, ask which to focus on |

## Stop Points

STOP if:
- No task specified and multiple tasks exist (ask which one)
- Task file has unexpected structure
- Phase is ambiguous (ask user to clarify)
