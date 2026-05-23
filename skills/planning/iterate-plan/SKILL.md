---
name: iterate-plan
description: Update existing implementation plans through user feedback with thorough research and validation. Also migrates old checkbox-based plans to the new Task tools system. This skill should be used when iterating on implementation plans, updating plans based on new requirements, refining technical approaches in existing plans, migrating old plans to Task tools, or when the user wants to modify a previously created plan file. Triggers on requests like "update the plan", "change the implementation approach", "iterate on this plan", "migrate to new system", or when feedback is provided about an existing plan document.
---

# Iterate Plan

## Overview

This skill enables intelligent iteration on existing implementation plans. Rather than rewriting plans from scratch, it makes surgical, well-researched updates while preserving the plan's existing structure and quality standards.

## Progress Tracking with Task Tools

> **This skill uses Claude Code's native Task tools for progress tracking.**

When iterating on plans, you must keep Tasks synchronized with plan changes:

| Plan Change | Task Action |
|-------------|-------------|
| Add new phase | `TaskCreate` for new phase, update `addBlockedBy` dependencies |
| Remove phase | `TaskUpdate` to mark removed (or delete if not started) |
| Reorder phases | Update `addBlockedBy` relationships |
| Rename phase | `TaskUpdate` to change subject |
| Modify phase scope | `TaskUpdate` to change description |

**Important**: The plan's `task_list_id` in metadata links to its Tasks. Always verify you're updating the correct task list.

## Migrating Old Plans to Task Tools

> **Use this process when a plan lacks `task_list_id` in its metadata.**

Old plans used checkbox-based progress tracking (`[x]` / `[ ]`). The new system uses Task tools. When you encounter an old plan, migrate it.

### Detecting Old Plans

An old plan has:
- No `task_list_id` in YAML frontmatter
- Checkbox-based progress: `- [x] Task completed` / `- [ ] Task pending`
- No reference to Task tools

### Migration Process

**Step M1: Generate task_list_id**

Create an ID from the plan filename:
```
docs/plans/2024-03-15-user-auth.md → plan-2024-03-15-user-auth
docs/plans/api-refactor.md → plan-api-refactor
```

**Step M2: Add metadata to plan**

Add or update the YAML frontmatter:
```yaml
---
task_list_id: plan-2024-03-15-user-auth
migrated_from_checkboxes: true
migration_date: 2026-01-25
---
```

**Step M3: Create Tasks for each phase**

For each phase in the plan:
```
TaskCreate:
  subject: "Phase N: [Phase Name]"
  description: "[Phase objective from plan] - Plan: [plan file path]"
  activeForm: "Implementing Phase N: [Name]"
```

**Step M4: Determine phase status from checkboxes**

Analyze existing checkboxes to determine status:

| Checkbox Pattern | Task Status |
|-----------------|-------------|
| All tasks `[x]` checked | `completed` |
| Some tasks `[x]`, some `[ ]` | `in_progress` |
| All tasks `[ ]` unchecked | `pending` |

```
TaskUpdate:
  taskId: [phase task]
  status: "completed" | "in_progress" | "pending"
```

**Step M5: Set up dependencies**

Create sequential dependencies:
```
TaskUpdate:
  taskId: [phase-2-task]
  addBlockedBy: [phase-1-task]

TaskUpdate:
  taskId: [phase-3-task]
  addBlockedBy: [phase-2-task]
```

**Step M6: Preserve checkboxes as reference**

Do NOT remove checkboxes from the plan. They serve as historical record. Add a note:
```markdown
> **Note**: This plan has been migrated to Task tools for progress tracking.
> Checkboxes below are preserved for reference but progress is now tracked via `TaskList`.
> Task List ID: `plan-2024-03-15-user-auth`
```

### Migration Example

**Before (old plan):**
```markdown
# Implementation Plan: User Authentication

## Phase 1: Database Schema
- [x] Create users table
- [x] Add password hash column
- [x] Create sessions table

## Phase 2: Auth Service
- [x] Implement password hashing
- [ ] Implement login endpoint
- [ ] Implement logout endpoint

## Phase 3: Testing
- [ ] Unit tests for auth service
- [ ] Integration tests
```

**After (migrated plan):**
```markdown
---
task_list_id: plan-user-authentication
migrated_from_checkboxes: true
migration_date: 2026-01-25
---

# Implementation Plan: User Authentication

> **Note**: This plan has been migrated to Task tools for progress tracking.
> Checkboxes below are preserved for reference but progress is now tracked via `TaskList`.
> Task List ID: `plan-user-authentication`

## Phase 1: Database Schema
- [x] Create users table
- [x] Add password hash column
- [x] Create sessions table

## Phase 2: Auth Service
- [x] Implement password hashing
- [ ] Implement login endpoint
- [ ] Implement logout endpoint

## Phase 3: Testing
- [ ] Unit tests for auth service
- [ ] Integration tests
```

**Tasks created:**
```
Tasks (1 done, 2 open):
  ✓ #1 Phase 1: Database Schema
  ● #2 Phase 2: Auth Service (in_progress) › blocked by #1
  ◻ #3 Phase 3: Testing › blocked by #2
```

### When to Migrate

Migrate automatically when:
- User runs `/iterate-plan` on an old plan
- User runs `/implement-plan` on an old plan
- User explicitly asks to "migrate" or "update to new system"

Present migration summary to user:
```
📋 Plan Migration Required

This plan uses the old checkbox-based progress tracking.
I'll migrate it to the new Task tools system.

Phases detected: 3
  - Phase 1: Database Schema (completed - all checkboxes checked)
  - Phase 2: Auth Service (in progress - partial checkboxes)
  - Phase 3: Testing (pending - no checkboxes checked)

Proceed with migration? (Tasks will be created, checkboxes preserved)
```

## Initial Input Handling

Parse the user's request to identify two required elements:

1. **Plan file path** - The location of the existing implementation plan
2. **Requested changes** - What modifications the user wants

Handle these scenarios:

| Scenario | Action |
|----------|--------|
| No plan provided | Ask: "Which plan file should I update?" |
| Plan but no feedback | Ask: "What changes would you like to make to this plan?" |
| Both provided | Proceed to Step 1 |

## Six-Step Iteration Process

### Step 1: Understand the Current Plan

Read the complete plan file and thoroughly understand:
- Overall structure and organization
- Current technical approach and decisions
- Success criteria (both automated and manual)
- Dependencies and relationships between sections
- Any existing constraints or trade-offs documented
- **The `task_list_id` in plan metadata** (links to Task tools progress)

**Check for old plan format:**
```
IF plan has no task_list_id in frontmatter:
  → Plan needs migration (see "Migrating Old Plans to Task Tools")
  → Present migration summary to user
  → Perform migration before proceeding with iteration
```

**Check existing Tasks (for migrated/new plans):**
```
TaskList: View current tasks for this plan
```

Note which phases:
- Are already completed (don't modify completed work without good reason)
- Are in progress (coordinate changes carefully)
- Are pending (safe to modify)
- Are blocked (check what's blocking them)

Document the sections that will likely need modification based on the feedback.

### Step 2: Research If Needed

**Critical**: Only spawn research tasks if the changes require new technical understanding.

When research is necessary, use specialized sub-agents with highly specific instructions:

```
Research Task Template:
- Agent type: codebase-locator | codebase-analyzer | Explore
- Specific directories to examine
- Exact patterns or code to find
- Required output format (file:line references)
```

Research scenarios that warrant sub-agent spawning:
- Changes involve unfamiliar parts of the codebase
- New integrations or dependencies need validation
- Technical feasibility of proposed changes is uncertain
- Alternative approaches need evaluation

**Do NOT research when**:
- Changes are cosmetic or structural (reordering, rewording)
- The modification is already well-understood
- Feedback is about plan formatting, not technical content

### Step 3: Present Understanding Before Changes

Before making any modifications, present:

1. **Interpretation of Feedback**
   - Restate what changes are being requested
   - Confirm understanding of the user's intent

2. **Research Findings** (if research was performed)
   - Key discoveries with file:line references
   - Technical implications for the plan

3. **Planned Modifications**
   - List specific sections that will change
   - Describe the nature of each change
   - Note any sections that will remain unchanged

Wait for user confirmation before proceeding to Step 4.

### Step 4: Make Surgical Edits

Update the plan using Edit tool with these principles:

**Structural Integrity**
- Maintain existing heading hierarchy
- Preserve section organization patterns
- Keep consistent formatting throughout

**Content Quality**
- Ensure changes align with surrounding context
- Update all related sections (e.g., if changing approach, update affected tasks)
- Maintain traceability between requirements and implementation tasks

**Success Criteria Standards**
- **Automated Verification**: Commands that can be run (tests, lints, builds)
- **Manual Verification**: Human-observable behaviors requiring testing
- Never mix these categories; keep them distinctly separated

**Edit Scope**
- Change only what is necessary to address the feedback
- Avoid "while I'm here" improvements unless explicitly requested
- Preserve author's voice and existing explanations where possible

### Step 5: Synchronize Tasks

**Critical**: Keep Tasks aligned with plan changes.

**For added phases:**
```
TaskCreate:
  subject: "Phase N: [New Phase Name]"
  description: "[Phase objective] - Plan: [plan file path]"
  activeForm: "Implementing Phase N: [Name]"

TaskUpdate:
  taskId: [new task]
  addBlockedBy: [previous phase task ID]
```

**For removed phases:**
```
# If phase was never started:
TaskUpdate:
  taskId: [removed task]
  status: "completed"
  description: "[Original description] - REMOVED: [reason]"

# Update dependencies of subsequent phases
TaskUpdate:
  taskId: [next phase]
  addBlockedBy: [new predecessor]
```

**For reordered phases:**
```
# Clear old dependencies and set new ones
TaskUpdate:
  taskId: [moved phase]
  addBlockedBy: [new predecessor IDs]
```

**For renamed/modified phases:**
```
TaskUpdate:
  taskId: [phase task]
  subject: "Phase N: [New Name]"
  description: "[Updated description]"
```

### Step 6: Present Changes and Invite Iteration

After editing, present:

1. **Summary of Changes Made**
   - What was modified in the plan and why
   - Any dependencies that were updated as a result
   - **Task changes made** (added, removed, reordered)

2. **Current Task Status**
   - Show updated TaskList output
   - Highlight any dependency changes

3. **Invitation for Further Iteration**
   - Ask if the changes meet expectations
   - Offer to refine any sections further

## Critical Guidelines

### Be Skeptical
- Question whether changes are truly needed
- Verify technical claims through research, not assumptions
- Challenge feedback that may be based on misunderstanding

### Be Surgical
- Minimize edit scope to exactly what's needed
- Prefer targeted edits over section rewrites
- Preserve existing content that isn't directly affected

### Be Thorough
- Update all sections affected by a change (dependencies, success criteria, etc.)
- Ensure internal consistency after modifications
- Verify no orphaned references remain

### Be Interactive
- Confirm understanding before making changes
- Present planned modifications before execution
- Seek feedback after changes are complete

### Never Update with Open Questions
**Do NOT update the plan with unresolved questions.**

If research reveals ambiguity or multiple valid approaches:
1. Present the options to the user
2. Explain trade-offs for each
3. Wait for direction before proceeding

## Quality Checklist

Before considering iteration complete, verify:

- [ ] All requested changes have been addressed
- [ ] Success criteria remain measurable and categorized (automated vs manual)
- [ ] No broken references or orphaned sections
- [ ] Plan remains internally consistent
- [ ] Technical approach is validated (if changes were technical)
- [ ] **Tasks synchronized** (added/removed/reordered to match plan)
- [ ] **Task dependencies correct** (blockedBy relationships updated)
- [ ] **task_list_id present** in plan metadata (add if missing)
- [ ] User has confirmed the changes meet their needs

**For migrated plans, also verify:**
- [ ] `task_list_id` added to YAML frontmatter
- [ ] `migrated_from_checkboxes: true` in frontmatter
- [ ] Migration note added to plan body
- [ ] Task status matches checkbox state (completed/in_progress/pending)
- [ ] Original checkboxes preserved for reference

## Task Synchronization Rules

| Scenario | Plan Action | Task Action |
|----------|-------------|-------------|
| **Migrate old plan** | Add frontmatter + migration note | TaskCreate for all phases with correct status |
| Add phase between 2 and 3 | Insert new Phase 2.5 (renumber to 3) | TaskCreate + update dependencies |
| Remove phase 3 | Delete phase content | Mark task completed with "REMOVED" note |
| Split phase into two | Create two phases from one | TaskCreate for new, update original |
| Merge two phases | Combine into single phase | Mark one completed with "MERGED" note |
| Change phase order | Reorder in plan | Update all blockedBy relationships |

**Never leave Tasks out of sync with the plan.** The Task list is the source of truth for progress, and the plan is the source of truth for specifications.
