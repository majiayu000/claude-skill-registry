---
name: collab-cleanup
description: Close out a collab session - archive or delete design artifacts
user-invocable: false
---

# Collab Cleanup

## Browser-Based Questions

When a collab session is active, use `render_ui` for all user interactions.

**Component selection:**
| Question Type | Component |
|--------------|-----------|
| Yes/No | Card with action buttons |
| Choose 1 of 2-5 | RadioGroup |
| Choose 1 of 6+ | MultipleChoice |
| Free text | TextInput or TextArea |

**Example - Yes/No:**
```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "ui": {
    "type": "Card",
    "props": { "title": "<question context>" },
    "children": [{ "type": "Markdown", "props": { "content": "<question>" } }],
    "actions": [
      { "id": "yes", "label": "Yes", "primary": true },
      { "id": "no", "label": "No" }
    ]
  },
  "blocking": true
}
```

**Terminal prompts only when:** No collab session exists (pre-session selection).

## Overview

Close a collab session after development is complete. Offers choices to archive design artifacts, delete them, or keep the session open for reference.

**Announce at start:** "I'm using the collab-cleanup skill to close this session."

## Workflow

### Step 1: Identify Current Session

1. Call `mcp__plugin_mermaid-collab_mermaid__list_sessions` to get all sessions across projects:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__list_sessions
   Args: {}
   ```
2. Filter results to current project (match `project` field against absolute cwd path)
3. If sessions found for current project:
   - For each session, fetch phase via `mcp__plugin_mermaid-collab_mermaid__get_session_state`:
     ```
     Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
     Args: { "project": "<cwd>", "session": "<session-name>" }
     ```
   - Display list with phases:
     ```
     Sessions in this project:
     1. glowing-sunny-mesa (phase: rough-draft)
     2. bright-calm-river (phase: implementation)
     ```
   - Ask: "Which session to clean up?" (or if only one, confirm it)
4. If no sessions for current project:
   - Display: "No collab sessions found in this project."
   - Exit

### Step 2: Show Session Summary

Display session details:

```
Session: [name]
Template: [feature/bugfix/refactor/spike]
Phase: [current phase]

Artifacts:
- Documents: [list .md files]
- Diagrams: [list .mmd files]
```

### Step 3: Ask User Choice

```
What would you like to do with the design artifacts?

1. Archive - Copy to docs/designs/[session-name]/
2. Delete - Remove without saving
3. Keep - Leave session in place, exit without cleanup
4. Archive & Continue - Archive with timestamp, reset session for new work
```

### Step 4: Execute Choice

**If Archive:**
1. Create `docs/designs/[session-name]/` directory
2. Copy all documents including per-item documents:
   - `.collab/[session]/documents/design.md`
   - `.collab/[session]/documents/interface-item-*.md`
   - `.collab/[session]/documents/pseudocode-item-*.md`
   - `.collab/[session]/documents/skeleton-item-*.md`
3. Copy `.collab/[session]/diagrams/*` to `docs/designs/[session-name]/`
4. Delete `.collab/[session]/` folder
5. Report what was archived (including count of per-item documents)

**If Delete:**
1. Confirm: "Delete session [name]? This cannot be undone."
   ```
   1. Yes, delete
   2. No, go back
   ```
2. If **1 (Yes)**: Delete `.collab/[session]/` folder
3. If **2 (No)**: Return to Step 3

**If Keep:**
1. Exit without changes
2. Remind user: "Session kept open. Run `/collab-cleanup` when ready to close."

**If Archive & Continue:**
1. Generate timestamp: `[session-name]-[YYYY-MM-DD-HHmmss]`
2. Create archive directory: `docs/designs/[session-name]-[timestamp]/`
3. Copy `.collab/[session]/documents/*` to archive directory
4. Copy `.collab/[session]/diagrams/*` to archive directory
5. Clear Work Items section in `.collab/[session]/documents/design.md`:
   - Keep "## Session Context" and its content intact
   - Replace "## Work Items" section with empty placeholder
6. Reset collab state via MCP:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
   Args: {
     "project": "<absolute-path-to-cwd>",
     "session": "<session-name>",
     "phase": "brainstorming",
     "currentItem": null
   }
   ```
   Note: `lastActivity` is automatically updated by the MCP tool.
7. Report: "Session `[name]` archived to `docs/designs/[name]-[timestamp]/`. Session reset for new work."
8. Loop back to `gather-session-goals` skill to start work on new items

### Step 5: Confirm

Display completion message:

- Archive: "Session `[name]` archived to `docs/designs/[name]/`"
- Delete: "Session `[name]` deleted."
- Keep: "Session `[name]` kept open."
- Archive & Continue: "Session `[name]` archived to `docs/designs/[name]-[timestamp]/`. Ready for new work items."

## Integration

**Called by:**
- `finishing-a-development-branch` skill at completion
- User directly via `/collab-cleanup` command

**Collab workflow position:**
```
collab → brainstorming → rough-draft → executing-plans → finishing-a-development-branch → collab-cleanup
                                                                                              ↑
                                                                                        (you are here)
```

## Common Mistakes

### Archiving without checking contents
- **Problem:** Archived files might be incomplete or contain sensitive info
- **Fix:** Always show session summary before archiving

### Deleting active session
- **Problem:** User accidentally deletes session they're still working on
- **Fix:** Confirm deletion, check if phase is not "implementation"

## Red Flags

**Never:**
- Delete without confirmation
- Archive to a location that already exists (overwrite)
- Clean up if there are pending verification issues

**Always:**
- Show session summary before action
- Confirm destructive actions
- Report what was done
