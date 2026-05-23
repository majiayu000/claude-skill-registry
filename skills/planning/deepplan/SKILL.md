---
name: deepPlan
description: Atlas skill for Manus AI-inspired persistent planning. USE WHEN complex multi-step task, research project, extended implementation, OR need goal anchoring. Uses filesystem as memory with 3-file structure.
context: fork
---

# DeepPlan - Persistent File-Based Planning

**Auto-routes for complex multi-step tasks requiring persistent memory.**

---

## Overview

DeepPlan implements the Manus AI "planning-with-files" pattern that uses filesystem as working memory. This combats:

- **Context volatility** - plans persist across session resets
- **Goal drift** - re-reading anchors objectives during long sessions
- **Hidden failures** - errors logged for pattern avoidance
- **Memory fragmentation** - findings stored externally, not in context

## The 3-File System

| File | Purpose | Updates |
|------|---------|---------|
| `task_plan.md` | Master tracking with phases and checkboxes | Before/after each phase |
| `notes.md` | Research findings, errors, intermediate results | During exploration |
| `[deliverable].md` | Final output document | End of task |

**Location:** Created in current working directory.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **DiscoverPlans** | On activation, check for existing plans | `Workflows/DiscoverPlans.md` |
| **InitializePlan** | "start planning", "create plan" | `Workflows/InitializePlan.md` |
| **UpdateProgress** | "update plan", "mark complete" | `Workflows/UpdateProgress.md` |
| **ReviewGoals** | Before major decisions | `Workflows/ReviewGoals.md` |

## Core Behavior

### On Activation

1. **Discover existing plans** - Scan `~/.claude/plans/` for related project plans
2. **Offer options** - Resume, Reference, or Start Fresh
3. **Initialize files** - Create task_plan.md, notes.md in current directory
4. **Sync with TodoWrite** - Create in-session todos for visibility

### During Work

1. Store research findings in `notes.md` (keeps context clean)
2. Update `task_plan.md` checkboxes as phases complete
3. Keep TodoWrite synced for session visibility
4. Log errors to `notes.md` for pattern learning

### Before Major Decisions

1. **Re-read `task_plan.md`** - Refresh goals in attention window
2. Verify decision aligns with original objectives
3. Check `notes.md` for relevant findings or past errors

## Integration with TodoWrite

DeepPlan **expands** TodoWrite, not replaces it:

| System | Purpose | Scope |
|--------|---------|-------|
| **TodoWrite** | Session visibility | In-memory, current session |
| **DeepPlan files** | Persistent memory | On disk, survives restarts |

**Sync behavior:**
- Creating a plan phase → Creates matching todo
- Completing a phase → Marks todo complete
- Session restart → Reads files, rebuilds todos

## File Formats

### task_plan.md

```yaml
---
project: project-name
directory: /path/to/project
created: 2026-01-07
status: in_progress
---

# Task: [Task Description]

## Phases

### Phase 1: [Name]
- [ ] Step 1
- [ ] Step 2

### Phase 2: [Name]
- [ ] Step 1

## Status Updates

- 2026-01-07 14:30: Started Phase 1
```

### notes.md

```markdown
# Research Notes

## Findings

### [Topic]
- Finding 1
- Finding 2

## Errors Encountered

### [Error Type]
- What happened
- Resolution
```

## Examples

**Example 1: Start a complex task**
```
User: "/atlas:deep-plan Build authentication system with OAuth"
→ Checks ~/.claude/plans/ for existing auth plans
→ Creates task_plan.md with phases
→ Creates notes.md for research
→ Syncs phases to TodoWrite
→ Begins Phase 1
```

**Example 2: Resume after session restart**
```
User: "/atlas:deep-plan Continue the auth work"
→ Discovers task_plan.md in current directory
→ Reads current phase status
→ Rebuilds TodoWrite from checkboxes
→ Reads notes.md for context
→ Continues from last checkpoint
```

**Example 3: Before major decision**
```
[During implementation]
→ About to choose between JWT and session tokens
→ Re-reads task_plan.md to check original requirements
→ Reviews notes.md for relevant research
→ Makes decision aligned with goals
```
