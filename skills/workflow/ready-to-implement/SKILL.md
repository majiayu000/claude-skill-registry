---
name: ready-to-implement
description: Validate design completion and transition to implementation phase
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read, Glob, Grep
user-invocable: false
---

# Ready to Implement

## Collab Session Required

Before proceeding, check for active collab session:

1. Check if `.collab/` directory exists
2. Check if any session folders exist within
3. If no session found:
   ```
   No active collab session found.

   Use /collab to start a session first.
   ```
   **STOP** - do not proceed with this skill.

4. If multiple sessions exist, check `COLLAB_SESSION_PATH` env var or ask user which session.

## Overview

Validates that all work items are documented and transitions from brainstorming to implementation phase.

**Core principle:** No implementation without complete work item documentation.

**Announce at start:** "I'm using the ready-to-implement skill to validate design completion."

## When to Use

Use this skill when:
- Work item loop is complete and you want to verify all items are documented
- Resuming a session (collab skill always routes through here)
- You want to transition from brainstorming to rough-draft phase

## When NOT to Use

Do NOT use this skill when:
- No collab session is active (use `/collab` first)
- Design document does not exist yet (use `/collab` to start a session)
- Already in implementation phase (use `/executing-plans` instead)

## Behavior

1. Find active collab session
2. Read design document
3. Parse Work Items section for "### Item N:" sections
4. Check each item's Status field (pending vs documented)
5. If pending items exist: list them and return to work item loop
6. If all documented: show summary and ask user confirmation
7. On confirm: update state.phase to "rough-draft/interface" and invoke rough-draft

## Implementation

When invoked, follow these steps:

### Step 1: Find Active Session

```bash
# List collab sessions
ls -d .collab/*/ 2>/dev/null | xargs -I{} basename {}
```

If no sessions exist, report: "No active collab sessions found."

If multiple sessions exist, ask user which session to check.

### Step 2: Read Design Document

Use the MCP tool to get the design document:

```
Tool: mcp__plugin_mermaid-collab_mermaid__get_document
Args: { "project": "<project-path>", "session": "<session-name>", "id": "design" }
```

Or read from filesystem:

```bash
cat .collab/<session-name>/documents/design.md
```

### Step 3: Parse Work Items

Look for the "## Work Items" section in the design document.

**Parse each item by finding "### Item N:" sections:**

For each `### Item N: <title>` section, extract:
- `number`: The item number N
- `title`: The text after "Item N:"
- `type`: The value from `**Type:**` field
- `status`: The value from `**Status:**` field (pending or documented)

**Example work items section:**

```markdown
## Work Items

### Item 1: Refactor database layer
**Type:** refactor
**Status:** documented
**Problem/Goal:** ...
**Approach:** ...
**Success Criteria:** ...
**Decisions:** ...

---

### Item 2: Add user authentication
**Type:** feature
**Status:** pending
**Problem/Goal:**
**Approach:**
**Success Criteria:**
**Decisions:**
```

### Step 4: Check Status and Report Results

**If any items have `Status: pending`:**

```
Work items still need documentation:

- [ ] Item 2: Add user authentication (pending)
- [ ] Item 4: Fix login redirect bug (pending)

Returning to work item loop...
```

**Return to collab skill** - the work item loop will continue processing pending items.

Do NOT transition to rough-draft phase.

**If all items have `Status: documented`:**

```
All work items documented:

- [x] Item 1: Refactor database layer (documented)
- [x] Item 2: Add user authentication (documented)
- [x] Item 3: Fix login redirect bug (documented)

Ready to proceed to rough-draft?

1. Yes
2. No
```

### Step 5: Transition to Rough-Draft

On user confirmation (selects **1**):

**Update collab-state via MCP:**

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "phase": "rough-draft/interface"
}
```
Note: `lastActivity` is automatically updated by the MCP tool.

**Invoke rough-draft skill:**

```
Transitioning to rough-draft phase...
```

Then invoke the rough-draft skill to begin implementation planning.

**If user declines:**

```
Returning to work item loop for more work...
```

Return to collab skill to continue the work item loop.

## Error Handling

**No collab session found:**
```
No active collab session found.
Start a new session with /collab first.
```

**Design document not found:**
```
Design document not found at .collab/<session>/documents/design.md
Ensure a collab session has been started properly.
```

**No Work Items section found:**
```
No Work Items section found in design document.
The session may not have gathered goals yet.
Returning to collab skill...
```

**Already in implementation:**
```
Session "<session-name>" is already in implementation phase.
Current phase: implementation
Use /executing-plans to continue.
```

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

## Integration

**Called by:**
- collab skill (after work item loop completes)
- collab skill (on session resume - always routes through here)
- User directly via `/ready-to-implement` command

**Returns to:**
- **collab skill** - When pending items exist (continues work item loop)

**Transitions to:**
- **rough-draft** skill - When all items documented and user confirms

**Related skills:**
- **collab** - Session management and work item loop
- **gather-session-goals** - Collects work items at session start
- **brainstorming** - Documents feature/refactor/spike items
- **systematic-debugging** - Documents bugfix items

**Collab Workflow Chain:**
```
collab --> gather-session-goals --> work item loop --> ready-to-implement --> rough-draft
                                           ^                  |
                                           |                  | (if pending)
                                           +------------------+
```

This skill acts as the central checkpoint for all resumes and pre-implementation validation, ensuring no implementation begins without complete work item documentation.

## Quick Reference

```
/ready-to-implement

1. Finds active collab session
2. Reads design document
3. Parses Work Items section for "### Item N:" sections
4. Checks each item's **Status:** field
5. If pending items: lists them, returns to work item loop
6. If all documented: asks confirmation, then invokes rough-draft
```

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "ready-to-implement" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
