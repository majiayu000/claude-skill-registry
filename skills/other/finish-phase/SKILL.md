---
name: finish-phase
description: Manually complete a phase and update phase.md. Use when you want to manually review/edit phase completion, or when auto-detection didn't trigger.
allowed-tools: Bash, Read, Edit, Glob, Grep, AskUserQuestion
---

# Finish Phase

Manually complete a phase by updating its status and scope checklist. Use this when:
- You want to manually review/edit scope checklist before marking complete
- Auto-detection in `/finish-task` didn't trigger (e.g., already on main branch)
- You want to add notes to the phase's Notes section

## Usage

```
/finish-phase 03              # Complete phase 03
/finish-phase 03 --dry-run    # Preview changes without applying
```

## Arguments

- `$1` - Phase number (e.g., `03`, `3`, `phase-03`)
- `--dry-run` - Preview changes without modifying files
- `$ARGUMENTS` - Full arguments passed to the skill

## Process

### Step 1: Parse Arguments

Extract phase number from arguments:
- Phase number: `03`, `3`, or `phase-03` → normalize to `03`

```bash
# Extract phase number
PHASE_NUM=$(echo "$ARGUMENTS" | grep -oE '[0-9]+' | head -1)
PHASE_NUM=$(printf "%02d" "$PHASE_NUM")
```

### Step 2: Locate Phase Directory

Find the phase specification file:

```bash
PHASE_DIR=$(find specification -maxdepth 1 -type d -name "phase-${PHASE_NUM}-*" | head -1)
```

If not found, show available phases and exit.

### Step 3: Check Task Status

Read all tasks in the phase and check their status:

```bash
for task_file in "$PHASE_DIR/tasks/"task-*.md; do
    # Extract status from each task
done
```

Report:
- Total tasks
- Completed tasks
- Pending/in-progress tasks (warn if any)

If there are incomplete tasks, ask user for confirmation:
> "Phase has X incomplete tasks. Are you sure you want to mark the phase as complete?"

### Step 4: Preview Changes

Show what will be changed:

1. **Phase Status** - Current → `✅ completed`
2. **Scope Checklist** - Which items will be checked off based on task names

Display preview:
```
📋 Phase XX Completion Preview

Status: ⚪ pending → ✅ completed

Scope checklist updates:
- [x] SharedKernel package (matched: task-01 SharedKernel)
- [x] Contracts package (matched: task-02 Contracts)
- [ ] Some other item (no match found)

Tasks: 5/5 completed

Apply changes? (y/n)
```

### Step 5: Apply Changes

If user approves (or `--dry-run` not specified):

1. Update phase.md status to `✅ completed`
2. Check off matched scope items
3. Optionally ask if user wants to add notes

### Step 6: Commit Changes

```bash
git add "$PHASE_DIR/phase.md"
git commit -m "[${PHASE_NUM}-00] docs: mark phase as completed" --no-verify
```

### Step 7: Final Report

```
✅ Phase XX marked as completed!

Updated:
- Status: ✅ completed
- Scope: X/Y items checked

Git commit: [XX-00] docs: mark phase as completed

Next steps:
- /task-status - see remaining phases
- /start-task XX - start next phase's first task
```

## Manual Scope Editing

If scope matching isn't accurate, inform user:
> "Some scope items couldn't be automatically matched. You can manually edit the phase.md file to check them off."

Offer to open the file:
> "Would you like me to show you the scope section for manual review?"

## Error Handling

| Error | Message |
|-------|---------|
| Phase not found | "Phase XX not found. Available: phase-01, phase-02..." |
| Already completed | "Phase XX is already marked as completed." |
| No tasks exist | "Phase XX has no tasks. Create tasks first with /phase-breakdown XX" |

## Safety Rules

1. NEVER mark phase complete if user declines after incomplete task warning
2. ALWAYS show preview before making changes
3. ALWAYS commit changes after modifying phase.md
4. NEVER modify task files (only phase.md)

## Example Session

```
User: /finish-phase 01

Claude: 📂 Found phase: specification/phase-01-foundation/phase.md

Checking tasks...
- task-01: ✅ completed
- task-02: ✅ completed
- task-03: ✅ completed
- task-04: ✅ completed
- task-05: ✅ completed

All 5 tasks completed!

📋 Phase 01 Completion Preview

Status: ⚪ pending → ✅ completed

Scope checklist updates:
- [x] SharedKernel package (matched: task-01)
- [x] Contracts package (matched: task-02)
- [x] EShop.Common (matched: task-05)

Apply changes? (y/n)

User: y

Claude: ✅ Phase 01 marked as completed!

Committed: [01-00] docs: mark phase as completed

Next steps:
- /task-status - see remaining phases
- /phase-breakdown 02 - prepare next phase
```
