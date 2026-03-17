---
name: workflow-br-ticket
description: Use this skill when working with Jira tickets (RD-XXXX) to ensure proper task tracking and state persistence in `br`.
---
# Workflow: br Ticket Integration



## When to Use

Invoke this skill whenever:
- A Jira ticket ID (e.g., RD-3891) is mentioned in the conversation
- Starting work on a new ticket
- Resuming work on a ticket from a previous session
- Transitioning between workflow phases (research → PRD → arch → plan → implementation)

## Workflow

### Phase 1: Task Discovery

1. Check if a `br` parent task exists for this ticket:
   ```bash
   br list | grep RD-XXXX
   ```
   Or check by external reference:
   ```bash
   br query "external_ref=RD-XXXX"
   ```

2. **If parent task exists:**
   - Load the task and its children
   - Identify the current active phase (child task in progress)
   - Resume work on that phase

3. **If no parent task exists:**
   - Ask user: "Should I create a br task for RD-XXXX to track this work?"
   - If yes → proceed to Phase 2
   - If no → continue without br tracking

### Phase 2: Parent Task Creation

Create the parent task with:
```bash
br create "RD-XXXX - [Ticket Title]" \
  --type epic \
  --external-ref RD-XXXX \
  --description "Parent task for Jira ticket RD-XXXX"
```

Store parent task ID for creating children.

### Phase 3: Phase Task Creation (User-Validated)

Ask user which phase to start with:
> "Which phase should I start with?
> 1. Research
> 2. PRD (Product Requirements Document)
> 3. Architecture decisions
> 4. Implementation plan
> 5. Implementation"

Create the child task:
```bash
br create "Phase: [Phase Name]" \
  --type task \
  --parent [PARENT_ID] \
  --description "Working on [phase] phase for RD-XXXX"
```

### Phase 4: Working Within Phase (Autonomous)

While working within a phase, you have autonomy to:

✅ **DO (without asking):**
- Update task status: `br update [ID] --status in_progress`
- Add context to description: `br update [ID] --description "..."`
- Mark subtasks complete in metadata
- Log files touched in task metadata
- Record decisions made
- Add blockers encountered
- Update checklist progress

**Metadata Format (JSON in description or via labels):**
```json
{
  "jira_ticket": "RD-XXXX",
  "phase": "research",
  "obsidian_path": "work/tickets/RD-XXXX [Title]/research.md",
  "files_touched": ["src/file.ts"],
  "decisions": ["Decision 1", "Decision 2"],
  "blockers": [],
  "checklist": {
    "task1": "done",
    "task2": "in_progress",
    "task3": "pending"
  }
}
```

### Phase 5: Phase Completion (User-Validated)

When phase is complete:
1. Update status: `br update [ID] --status closed`
2. Ask user: "[Phase] complete. Create next phase task?"
3. Options:
   - "Yes" → Create next sequential phase
   - "Skip to [phase]" → Create specific phase
   - "No" → Pause, parent task stays open

### Phase 6: Ticket Completion (User-Validated)

When all phases complete:
- Ask user: "All phases complete. Close parent task for RD-XXXX?"
- If yes: `br update [PARENT_ID] --status closed`

## Key Principles

1. **Always check for existing tasks first** — Don't duplicate
2. **Ask before creating** — Parent and phase tasks need user approval
3. **Autonomous within phases** — Freely update progress, context, files
4. **Persist state in br** — Files, decisions, blockers, checklist
5. **Link to Obsidian** — Store obsidian_path in metadata
6. **External ref = Jira ticket** — Always set `--external-ref RD-XXXX`

## Quick Reference

| Action | Command | User Approval |
|--------|---------|---------------|
| Check existing | `br list \| grep RD-XXXX` | No |
| Create parent | `br create ... --external-ref RD-XXXX` | ✅ Yes |
| Create phase | `br create ... --parent [ID]` | ✅ Yes |
| Update status | `br update [ID] --status [status]` | No |
| Add context | `br update [ID] --description "..."` | No |
| Close phase | `br update [ID] --status closed` | ✅ Yes |
| Close parent | `br update [ID] --status closed` | ✅ Yes |
| List children | `br list --parent [ID]` | No |
| Show task | `br show [ID]` | No |

## Example Session

**User:** "Let's work on RD-3891"

**Agent:** 
1. Checks: `br list \| grep RD-3891` → No results
2. Asks: "Should I create a br task for RD-3891?"
3. User: "Yes, start with research"
4. Creates parent task #42
5. Creates child task #43 "Phase: Research" with parent #42
6. Works on research, updates metadata with findings
7. Research complete
8. Asks: "Research complete. Create PRD phase task?"
9. User: "Yes"
10. Creates child task #44 "Phase: PRD" with parent #42
11. Continues...
