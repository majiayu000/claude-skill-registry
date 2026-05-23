---
name: phase-breakdown
description: Break down a phase into actionable tasks. Use when user says "rozloz fazi", "breakdown phase", or runs /phase-breakdown.
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion, Task
---

# Phase Breakdown

Orchestrates the breakdown of a phase specification into actionable developer tasks. Wraps the `dotnet-tech-lead` agent workflow into a simple command.

## Usage

```
/phase-breakdown 03              # Break down phase 03 into tasks
/phase-breakdown 03 --validate   # Validate existing breakdown
/phase-breakdown 03 --refresh    # Regenerate tasks (with confirmation)
```

## Arguments

- `$1` - Phase number (e.g., `03`, `3`, `phase-03`)
- `--validate` - Validate existing breakdown instead of creating new
- `--refresh` - Delete existing tasks and regenerate (requires confirmation)
- `$ARGUMENTS` - Full arguments passed to the skill

## Process

### Step 1: Parse Arguments

Extract phase number and mode from arguments:
- Phase number: `03`, `3`, or `phase-03` → normalize to `03`
- Mode: default (create), `--validate`, or `--refresh`

### Step 2: Locate Phase File

Find the phase specification file:

```bash
find specification -type d -name "phase-$PHASE_NUM*" | head -1
```

Expected structure:
```
specification/phase-03-name/
├── phase.md           # Phase specification
└── tasks/             # Task files (may not exist yet)
```

If phase file not found, report error and exit.

### Step 3: Check Existing Tasks

```bash
ls specification/phase-$PHASE_NUM-*/tasks/*.md 2>/dev/null
```

- **Default mode**: If `tasks/` exists with files, ERROR and suggest `--refresh`
- **--validate mode**: If no tasks exist, ERROR
- **--refresh mode**: If tasks exist, ask for confirmation before deleting

### Step 4: Read Phase Specification

Read the phase.md file and extract:
- **Objective**: What this phase accomplishes
- **Scope**: List of deliverables
- **Related Specs**: Links to high-level specifications

### Step 5: Read Related Specs

For each spec referenced in the phase:
1. Read the spec file
2. Extract relevant sections for task generation
3. Note key implementation details

### Step 6: Generate Tasks (Delegate to dotnet-tech-lead Pattern)

**For default/refresh mode**, generate tasks following the `dotnet-tech-lead` pattern:

Use the Task tool to spawn a `dotnet-tech-lead` agent with this prompt:

```
You are breaking down Phase XX for implementation.

## Phase Specification
[Include full phase.md content]

## Related Specs
[Include relevant spec sections]

## Requirements
1. Create tasks that cover ALL scope items
2. Each task should be completable in 1-4 hours
3. Define clear dependencies between tasks
4. Reference specs with specific sections (don't duplicate content)
5. Follow the task template format

Generate the task breakdown and present for approval.
```

### Step 7: User Approval

The agent will present a summary table:

```
📋 Task Summary for Phase XX

| # | ID | Task | Dependencies | Summary |
|---|-----|------|--------------|---------|
| 1 | task-01 | ... | - | ... |
| 2 | task-02 | ... | task-01 | ... |

Related Specs: [list]

👉 Approve or request changes?
```

- If approved → proceed to file creation
- If changes requested → adjust and present again
- NEVER create files without approval

### Step 8: Create Task Files

After approval, create:
1. `tasks/` folder if needed
2. Individual task files: `task-XX.md`
3. Update phase.md with task table

### Step 9: Run sort-tasks

After creating tasks, run the sort-tasks skill:

```bash
node .claude/scripts/sort-tasks.mjs specification/phase-XX-name/tasks/
```

Include the execution order in the final report.

### Step 10: Final Report

```
✅ Phase XX breakdown complete!

Created X tasks:
1. task-01 - [Name]
2. task-02 - [Name] (depends on: task-01)
...

Entry points: task-01, task-03

Next steps:
- /task-status - see current progress
- /start-task 01 - start working on task-01
- /sort-tasks - re-check execution order
```

## Validation Mode (--validate)

When `--validate` is passed:

1. Read all existing task files
2. Compare task scopes against phase scope
3. Check that all scope items are covered
4. Verify spec references are valid
5. Check dependencies are consistent

Report:
```
📋 Validation Report for Phase XX

Coverage:
✅ Scope item 1 - covered by task-02
✅ Scope item 2 - covered by task-01, task-03
⚠️ Scope item 3 - NOT COVERED

Spec References:
✅ aspire-orchestration.md - referenced by task-01, task-02
⚠️ aspire-hybrid.md - referenced in phase but not in tasks

Dependencies:
✅ No circular dependencies
✅ All referenced tasks exist

Overall: X/Y items covered
```

## Refresh Mode (--refresh)

When `--refresh` is passed:

1. Show existing tasks that will be deleted
2. Ask for confirmation: "This will delete X existing tasks. Continue? (y/n)"
3. If confirmed:
   - Delete all files in `tasks/` folder
   - Proceed with normal breakdown flow
4. If declined:
   - Exit without changes

## Error Handling

| Error | Message |
|-------|---------|
| Phase not found | "Phase XX not found. Available: phase-01, phase-02..." |
| Tasks exist (default mode) | "Tasks already exist. Use --refresh to regenerate or --validate to check." |
| No tasks (validate mode) | "No tasks found to validate. Run without --validate first." |
| Invalid phase number | "Invalid phase number. Use format: 03, 3, or phase-03" |

## Safety Rules

1. NEVER create tasks without user approval
2. NEVER delete existing tasks without confirmation
3. ALWAYS reference specs instead of duplicating content
4. ALWAYS run sort-tasks after creating/modifying tasks
5. ALWAYS verify task coverage against phase scope

## Example Session

```
User: /phase-breakdown 03

Claude: 📂 Found phase: specification/phase-03-product/phase.md

Reading phase specification...
- Objective: Implement Product service core
- Scope: 4 items
- Related specs: 2 files

Generating task breakdown...

📋 Task Summary for Phase 03

| # | ID | Task | Dependencies | Summary |
|---|-----|------|--------------|---------|
| 1 | task-01 | Domain Model | - | Product aggregate, entities |
| 2 | task-02 | Repository | task-01 | EF Core implementation |
| 3 | task-03 | Application Layer | task-01 | Commands, queries, handlers |
| 4 | task-04 | API Endpoints | task-02, task-03 | REST controllers |

Related Specs:
- product-service-interface.md
- internal-api-communication.md

👉 Approve or request changes?

User: Approved

Claude: ✅ Phase 03 breakdown complete!

Created 4 tasks in specification/phase-03-product/tasks/

Execution order (topological):
1. task-01 - Domain Model
2. task-02 - Repository (→ task-01)
3. task-03 - Application Layer (→ task-01)
4. task-04 - API Endpoints (→ task-02, task-03)

Entry points: task-01

Next steps:
- /task-status - see current progress
- /start-task 01 - start working on task-01
```
