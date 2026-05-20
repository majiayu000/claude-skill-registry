---
name: task-mover
description: "[Task Mgmt] A Skill that syncs task status in Docs/Task/{StepName}_Task.md by moving tasks between sections (Backlog, Worker1, Worker2, Worker3, Review, Done) with priority-aware management for multi-agent parallel development. AI agent MUST invoke this skill AUTOMATICALLY when (1) starting work on a task - move to assigned Worker, (2) AI completing work - move to Review (NOT Done). CRITICAL - AI CANNOT move to Done or Backlog. Only User/Reviewer can move tasks to Done or Backlog. (user)"
---

# Task Mover

Sync task document status when workflow state changes in multi-worker parallel development.

## Trigger Conditions

### AI Allowed Actions

| Agent Action | Target Section | Checkbox | Pre-requisite |
|--------------|----------------|----------|---------------|
| Agent 1 starting work | Worker1 | `- [ ]` | Run `task-segmentation` first |
| Agent 2 starting work | Worker2 | `- [ ]` | Run `task-segmentation` first |
| Agent 3 starting work | Worker3 | `- [ ]` | Run `task-segmentation` first |
| **AI completed work** | **Review** | `- [ ]` | **AI MUST stop here** |

### User/Reviewer Only Actions (AI FORBIDDEN)

| Action | Target Section | Checkbox | Who |
|--------|----------------|----------|-----|
| User verified task | Done | `- [x]` | User/Reviewer ONLY |
| User defers task | Backlog | `- [ ]` | User ONLY |

## Section Structure

```markdown
## Backlog      - Queued, not prioritized
## Worker1      - Agent 1 working (separate git branch)
## Worker2      - Agent 2 working (separate git branch)
## Worker3      - Agent 3 working (separate git branch)
## Review       - Done, awaiting user review
## Done         - Completed and verified
```

## Movement Rules

1. When moving to Done: `- [ ]` → `- [x]`
2. When moving from Done: `- [x]` → `- [ ]`
3. Subtasks move with parent
4. Preserve metadata (#tags, !priority, Deadline)

## Priority-aware Management

| Priority | Processing Order | Recommended Action |
|----------|------------------|-------------------|
| `!high` | Top priority | Move to Worker immediately if possible |
| `!medium` | Normal processing | Process in order |
| `!low` | Low priority | Process after other tasks are complete |

## ⚠️ CRITICAL: Format Protection

**Absolute Rules:**
- NEVER modify existing Task document structure
- PRESERVE priority tags (`!high`, `!medium`, `!low`) when moving tasks
- NEVER change section order, table structure, or markdown format
- ONLY move task lines between sections and update checkbox state

## ⚠️ CRITICAL: Task Document Format Rules

**Strict Format Requirements:**
- Subtasks MUST use exactly 2-space indentation (no more, no less)
- NO intermediate grouping headers (e.g., `### Phase 1`, `#### Step A`) are allowed
- Task hierarchy is flat: Parent task → Subtasks (2-space indent) ONLY
- When moving tasks, preserve the 2-space indent for all subtasks

## ⛔ CRITICAL: Duplicate Section Prevention

**Before ANY edit, verify document structure:**

1. **Read entire file first** - Check existing section headers
2. **Count section occurrences** - Each section (`## Backlog`, `## Worker1`, etc.) MUST appear exactly ONCE
3. **If duplicates found** - STOP and fix by merging duplicate sections

**Detection Pattern:**
```
## Review    ← First occurrence (KEEP)
...tasks...
## Done      ← First occurrence (KEEP)
...tasks...
## Review    ← DUPLICATE (REMOVE - merge tasks to first ## Review)
## Done      ← DUPLICATE (REMOVE - merge tasks to first ## Done)
```

**Fix Procedure:**
1. Identify all duplicate sections
2. Merge tasks from duplicate sections into first occurrence
3. Delete duplicate section headers and empty lines
4. Verify only ONE of each section exists

## Workflow

1. **Read entire Task file** - Verify no duplicate sections exist
2. Identify task being worked on
3. **Check task priority** (prioritize `!high` tasks)
4. Determine new status from agent action
5. **If moving to Worker1/Worker2/Worker3**: Run `task-segmentation` first
6. Locate task block (partial title match)
7. Move to target section (preserve all metadata)
8. Update checkbox if needed
9. **Before saving** - Verify no duplicate sections created
10. Save file

## ⛔ CRITICAL: AI FORBIDDEN ACTIONS

**AI MUST NEVER perform these actions:**

```
❌ AI CANNOT move Review → Done
❌ AI CANNOT move Review → Backlog
❌ AI CANNOT move Worker → Done directly
❌ AI CANNOT move Worker → Backlog directly

✅ AI CAN: Backlog → Worker (when starting work)
✅ AI CAN: Worker → Review (when completing work)
```

**AI Workflow When Completing Work:**
1. AI completes work → Move from Worker → **Review**
2. **AI MUST STOP HERE** - Leave task in Review
3. User/Reviewer verifies and moves Review → Done

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `task-segmentation` | BEFORE moving task to Worker, segment subtasks into granular items |
| `task-add` | When discovering new work items during implementation |