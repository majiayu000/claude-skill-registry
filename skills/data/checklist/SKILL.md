---
name: checklist
description: Manage project checklist (view, add, check, edit)
allowed-tools: [Read, Write, Edit, AskUserQuestion]
---

# Project Checklist

Manage a simple markdown checklist that Claude is reminded about at session start.

**Current checklist:**
!`cat "${CLAUDE_PROJECT_DIR:-.}/.bluera/bluera-base/checklist.md" 2>/dev/null || echo "_No checklist exists yet. Use 'add' to create one._"`

---

## File Location

`.bluera/bluera-base/checklist.md` - Committed to repo (shared with team)

## File Format

Standard markdown with checkbox syntax:

```markdown
# Project Checklist

## Category Name
[ ] Unchecked item
[x] Checked item

## Another Category
[ ] Another item
```

## Subcommands

### show (default)

Read and display the checklist. If no checklist exists, inform the user.

### add \<item\>

Append a new unchecked item to the checklist:

1. If checklist doesn't exist, create it with a header
2. Append `[ ] <item>` to the end of the file
3. Display the updated checklist

### check \<item\>

Mark an item as complete:

1. Read the checklist
2. Find the item (fuzzy match on text)
3. Change `[ ]` to `[x]` for that line
4. Display the updated checklist

If multiple items match, ask user to clarify.

### edit

Tell the user the file path so they can edit directly:

```text
Checklist location: .bluera/bluera-base/checklist.md

You can edit this file directly with any text editor.
Format: [ ] for unchecked, [x] for checked items.
```

## Session Reminder

When a session starts, if the checklist has unchecked items, Claude receives a reminder in context showing the pending items. This happens automatically via the `checklist-remind.sh` hook.

## Algorithm

1. Parse the subcommand from arguments
2. Execute the appropriate action:
   - `show`: Read and display `.bluera/bluera-base/checklist.md`
   - `add`: Append item, create file if needed
   - `check`: Find and mark item complete
   - `edit`: Display file path for manual editing
3. For `add` and `check`, show updated checklist after modification
