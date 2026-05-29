---
name: gather-session-goals
description: Collect and classify work items at the start of a collab session. Invoked by collab skill after creating a new session.
user-invocable: false
model: opus
allowed-tools: mcp__plugin_mermaid-collab_mermaid__*, Read
---

# Gather Session Goals

## Overview

Collect and classify work items at the start of a collab session through iterative questioning.

**Invoked by:** collab skill after creating a new session

**Returns to:** collab skill (which manages the work item loop)

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

## The Process

### Step 1: Open Question

Ask the user: **"What do you want to accomplish this session?"**

Store the initial response. Parse any items mentioned and add them to the work items list with type = "unknown".

### Step 2: Anything Else Loop

After parsing the initial response:

1. Infer type for each item from context:
   - Contains "setup", "install", "configure", "organize", "clean up", "docker", "deploy" → type = "task"
   - Contains "fix", "bug", "broken", "error", "crash", "fail" → type = "bugfix"
   - Contains "add", "new", "create", "implement", "build", "refactor", "clean", "simplify", "restructure", "investigate", "explore", "spike" → type = "code"
   - Otherwise → type = "unknown"

2. Ask: **"Anything else?"**

3. If user provides more items:
   - Parse and infer types
   - Repeat from step 2

4. If user says no/done/that's it:
   - Proceed to Step 3

### Step 3: Classify Unknown Items

For each item still marked as type = "unknown":

Ask: **"What type is '[item title]'?"**
```
1. code
2. bugfix
3. task
```

Set the item type based on user response.

### Step 4: Present Summary

Display the work items for confirmation:

```
Here are the work items for this session:

1. [bugfix] Fix login redirect issue
2. [code] Add user authentication
3. [code] Clean up database layer

Does this list look correct?

1. Yes
2. Add more
3. Remove item
4. Edit item
```

**Handle user responses:**
- **1 (Yes)** - Proceed to Step 5
- **2 (Add more)** - Return to Step 2
- **3 (Remove)** - Ask which item to remove, remove it, return to Step 4
- **4 (Edit)** - Ask which item to edit, update it, return to Step 4

### Step 5: Write Work Items

**Before writing, output:** "Writing work items..."

#### 5a. Write to session state (source of truth for routing)

Build the workItems array and save to session state:

```
Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "workItems": [
    { "number": 1, "title": "<title>", "type": "<code|bugfix|task>", "status": "pending" },
    { "number": 2, "title": "<title>", "type": "<code|bugfix|task>", "status": "pending" },
    ...
  ]
}
```

#### 5b. Create design doc with work items

1. Build the design doc content with Work Items section:

```markdown
# Session: <session-name>

## Session Context
**Out of Scope:** (session-wide boundaries)
**Shared Decisions:** (cross-cutting choices)

---

## Work Items

### Item 1: <title>
**Type:** <type>
**Status:** pending

**Problem/Goal:**

**Approach:**

**Root Cause:** (only if type is bugfix)

**Success Criteria:**

**Decisions:**

---

### Item 2: <title>
...

---

## Diagrams
(auto-synced)
```

2. Create the design doc:
   Tool: mcp__plugin_mermaid-collab_mermaid__create_document
   Args: { "project": "<cwd>", "session": "<session>", "name": "design", "content": "<full-content>" }

   If document already exists, use update_document instead.

After writing, display:

```
Work items saved. Returning to collab workflow.
```

Return control to the collab skill.

## Key Constraints

- **One question at a time** - Never batch multiple questions together
- **Don't skip classification** - Every item must have a type before proceeding
- **Must get explicit confirmation** - User must approve the list before writing to design doc

## Contract

**Preconditions:**
- Collab session exists

**Postconditions:**
- Session state contains `workItems` array (source of truth for routing)
- Design doc contains `## Work Items` section (human-readable view)
- At least one work item defined
- All items have `status: pending`
- User has confirmed the list

**Side effects:**
- Writes `workItems` to session state
- Creates/updates design doc

## Browser-Based Questions

When a collab session is active, prefer `render_ui` for user interactions.

**For item type classification:**
```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Classify item" },
    "children": [
      { "type": "Markdown", "props": { "content": "What type is **[item title]**?" } },
      {
        "type": "RadioGroup",
        "props": {
          "name": "type",
          "options": [
            { "value": "code", "label": "Code (feature, refactor, investigation)" },
            { "value": "bugfix", "label": "Bugfix (fix, error, crash)" },
            { "value": "task", "label": "Task (setup, config, organization)" }
          ]
        }
      }
    ],
    "actions": [{ "id": "classify", "label": "Continue", "primary": true }]
  },
  "blocking": true
}
```

**For work items list confirmation:**
```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Confirm work items" },
    "children": [
      { "type": "Markdown", "props": { "content": "[markdown list of items]" } },
      {
        "type": "RadioGroup",
        "props": {
          "name": "action",
          "options": [
            { "value": "yes", "label": "Yes, this is correct" },
            { "value": "add", "label": "Add more items" },
            { "value": "remove", "label": "Remove an item" },
            { "value": "edit", "label": "Edit an item" }
          ]
        }
      }
    ],
    "actions": [{ "id": "confirm", "label": "Continue", "primary": true }]
  },
  "blocking": true
}
```

## Integration

**Called by:**
- **collab** skill - After session creation

**Returns to:**
- **collab** skill - To start the work item loop

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "gather-session-goals" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
