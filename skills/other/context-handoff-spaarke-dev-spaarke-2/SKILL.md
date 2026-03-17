---
description: Save working state before compaction or session end for reliable recovery
tags: [context, compaction, handoff, state, recovery, checkpoint]
techStack: [all]
appliesTo: ["save progress", "context handoff", "before compaction", "checkpoint"]
alwaysApply: false
---

# context-handoff

> **Category**: Operations
> **Last Updated**: January 2026

---

## Purpose

**Ensure reliable context recovery across compaction and session boundaries.**

This skill creates a checkpoint of working state that enables another Claude instance (or the same instance post-compaction) to continue work without loss. It addresses the critical gap where automatic or manual compaction can occur without state being persisted.

**Key Principle**: After this skill runs, `current-task.md` alone should contain everything needed to continue work.

---

## When to Use

### Manual Triggers
- User says "save my progress" or "save state"
- User is about to run `/compact`
- User is ending a session mid-task
- User requests `/context-handoff` or `/checkpoint` (alias)

### Proactive Triggers (Claude Should Self-Invoke)
- Context usage approaches 70% (check with `/context`)
- Before a large operation that might push context over limits
- After completing significant work that should be checkpointed
- When switching between projects

### Automatic Detection (Claude Should Monitor)
- Long-running tasks (> 30 minutes of work)
- After every 3-5 completed task steps
- After creating or modifying many files

---

## Workflow

### Step 1: Identify Current Work Context

```
DETERMINE active project:
  - Check if in a project worktree
  - Check git branch name (feature/{project-name})
  - Check recent file modifications under projects/
  - If ambiguous: Ask user

IF no active project:
  → "No active project detected. Nothing to checkpoint."
  → STOP

LOCATE current-task.md:
  - Path: projects/{project-name}/current-task.md
  - IF missing: Create from template
```

### Step 2: Capture Critical State

**This is the minimum state required for recovery. Be concise.**

```
CAPTURE (in memory first):

1. TASK IDENTIFICATION
   - Task ID (from current work or current-task.md)
   - Task file path
   - Task title
   - Current phase

2. PROGRESS STATE
   - Completed steps (numbered list)
   - Current step number and description
   - Step progress (e.g., "Step 4 of 7, sub-step 2 of 3")

3. FILES MODIFIED (this session only)
   - List all files created or modified
   - Brief purpose for each
   - Mark any uncommitted changes

4. DECISIONS MADE (this session only)
   - Key implementation choices
   - Why each decision was made
   - Any alternatives considered

5. NEXT ACTION (CRITICAL - must be explicit)
   - Exact next step to take
   - Any preconditions
   - Files to reference
```

### Step 3: Update current-task.md

**Structure the update with Quick Recovery at top:**

```markdown
# Current Task State - {Project Name}

> **Last Updated**: {YYYY-MM-DD HH:MM} (by context-handoff)
> **Recovery**: Read "Quick Recovery" section first

---

## Quick Recovery (READ THIS FIRST)

| Field | Value |
|-------|-------|
| **Task** | {NNN} - {Title} |
| **Step** | {N} of {Total}: {Step description} |
| **Status** | {in-progress / blocked} |
| **Next Action** | {Explicit next action to take} |

### Files Modified This Session
- `{path}` - {purpose}
- `{path}` - {purpose}

### Critical Context
{1-3 sentences of essential context for continuation}

---

## Full State (Detailed)

[... rest of current-task.md content ...]
```

### Step 4: Verify and Report

```
VERIFY current-task.md is complete:
  - Quick Recovery section has all fields
  - Next Action is explicit (not vague)
  - Files Modified matches actual changes
  - Timestamp is updated

OPTIONAL: Commit the checkpoint
  IF uncommitted changes exist:
    → "Do you want me to commit the state checkpoint? [y/n]"
    IF yes:
      git add projects/{project-name}/current-task.md
      git commit -m "checkpoint: save state for {task-id}"

REPORT to user:
  "✅ Context checkpoint saved to current-task.md

   Task: {task-id} - {title}
   Step: {N} of {total}
   Next: {next action}

   Ready for /compact or session end.
   To resume: 'continue task' or 'where was I?'"
```

---

## Quick Recovery Format

**The "Quick Recovery" section must answer these questions in < 30 seconds:**

1. **What task am I on?** → Task ID, title, phase
2. **Where in the task?** → Step N of M
3. **What files did I touch?** → Files modified list
4. **What do I do next?** → Explicit next action

Example:
```markdown
## Quick Recovery (READ THIS FIRST)

| Field | Value |
|-------|-------|
| **Task** | 045 - Deploy to Production |
| **Step** | 4 of 7: Configure Azure credentials |
| **Status** | in-progress |
| **Next Action** | Test deployment with: `az webapp deploy --slot staging` |

### Files Modified This Session
- `infrastructure/bicep/stacks/model2-full.bicep` - Added AI Search config
- `src/server/api/Sprk.Bff.Api/Program.cs` - Registered RagService

### Critical Context
OIDC federated identity configured. Staging deployment succeeded.
Need to verify health checks before promoting to production.
```

---

## Integration with Other Skills

### Before Compaction Flow
```
User: "I need to compact"
     ↓
Claude: [Invokes context-handoff]
     ↓
Claude: "✅ State saved. Ready for /compact."
     ↓
User: /compact
     ↓
[Compaction occurs]
     ↓
User: "Where was I?"
     ↓
Claude: [Invokes project-continue]
     ↓
Claude: Reads Quick Recovery section, continues work
```

### During Long Tasks
```
[Claude working on task]
     ↓
[After completing step 5 of 8]
     ↓
Claude: [Proactively invokes context-handoff]
     ↓
Claude: "Checkpoint saved. Continuing with step 6..."
```

### With project-continue
```
context-handoff: Creates checkpoint → current-task.md
project-continue: Reads checkpoint → restores context
```

---

## Proactive Checkpoint Guidelines

**When to self-checkpoint (Claude should do this automatically):**

| Condition | Action |
|-----------|--------|
| Completed a task step | Update current-task.md completed steps |
| Modified 5+ files | Run full context-handoff |
| Made significant decision | Log in current-task.md decisions |
| 30+ minutes of work | Run full context-handoff |
| Before large operation | Run full context-handoff |
| Context feels "heavy" | Check /context, consider checkpoint |

---

## Error Handling

| Situation | Response |
|-----------|----------|
| No active project | "No project context to save. Working on ad-hoc tasks?" |
| current-task.md missing | Create from template, populate with current state |
| Can't determine current task | Ask user: "Which task are you working on?" |
| Conflicting state in file | Ask user: "current-task.md shows task X, but you seem to be on Y. Which is correct?" |
| Git commit fails | "Checkpoint saved but not committed. Commit manually if needed." |

---

## Examples

### Example 1: Manual Pre-Compaction

```
User: "I need to compact, save my progress first"

Claude: [Runs context-handoff]

Output:
  "✅ Context checkpoint saved to current-task.md

   Task: 032 - Implement Email Export
   Step: 3 of 5: Create EmailExportService
   Next: Implement SendEmailAsync method using Graph API

   Files modified:
   - Services/Ai/Export/IEmailExportService.cs - Created interface
   - Services/Ai/Export/EmailExportService.cs - Started implementation

   Ready for /compact. To resume: 'continue task' or 'where was I?'"
```

### Example 2: Proactive Checkpoint

```
[Claude just completed step 5 of 8]

Claude: "Step 5 complete. Let me checkpoint progress..."

[Runs context-handoff silently]

Claude: "✅ Progress saved. Continuing with Step 6: Add unit tests..."
```

### Example 3: End of Session

```
User: "I'm done for today"

Claude: [Runs context-handoff]

Output:
  "✅ Session state saved.

   Task 013 at Step 4 of 6.
   Next session: Say 'continue task 013' or 'where was I?'

   Good night!"
```

---

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `project-continue` | Reads what context-handoff writes |
| `task-execute` | Should call context-handoff after steps |
| `push-to-github` | Can commit checkpoint as part of workflow |

---

## Tips for AI

- **Be proactive** - Don't wait for user to ask; checkpoint after significant work
- **Keep Quick Recovery minimal** - Recovery should take < 30 seconds to read
- **Next Action must be explicit** - "Continue working" is NOT explicit; "Run `dotnet test`" IS explicit
- **Timestamp is critical** - Always update Last Updated when checkpointing
- **Don't overwrite history** - Move detailed history to "Full State" section, not delete
- **Files Modified is session-scoped** - Reset when task changes, not accumulate forever
- **Verify before reporting** - Actually read back current-task.md to confirm save worked

---

## Post-Compaction Recovery

When Claude Code resumes after compaction:

1. **User says anything** → Check if there's active project context
2. **Find current-task.md** → Read Quick Recovery section
3. **Load minimal context** → Just enough to continue
4. **Report state** → "Recovered: Task X, Step Y, Next: Z"
5. **Load full context** → Via project-continue if needed

This can be automatic if the user's first message is work-related, or explicit via "where was I?".

---

*This skill ensures no work is lost across context boundaries.*
