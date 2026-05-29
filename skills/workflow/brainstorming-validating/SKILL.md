---
name: brainstorming-validating
description: The VALIDATING phase runs the completeness gate to ensure design is ready for implementation
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# VALIDATING Phase

The VALIDATING phase runs the completeness gate to ensure the design is ready for implementation.

## Purpose

- Verify all required sections are present
- Check for completeness and clarity
- Ensure no TBDs or ambiguous items remain
- Gate the transition to rough-draft

## Required Sections

The design doc must contain all of these:

- [ ] **Problem/Goal** - Clear statement of what we're solving and why
- [ ] **Key Decisions** - At least one documented decision with rationale
- [ ] **At least one diagram** - Visual representation of architecture, flow, or UI
- [ ] **Success Criteria** - Measurable, testable criteria (not "works well")
- [ ] **Out of Scope** - Explicit boundaries on what this work does NOT include

## Gate Check Process

```bash
# Read design doc
cat .collab/<name>/documents/design.md

# Verify each required section exists and has content
# If any section is missing or empty, do NOT proceed
```

For each section, verify:
1. Section header exists
2. Section has substantive content (not just placeholder text)
3. Content is specific, not vague

## Single-Item Mode (VALIDATING)

When `currentItem` is set in collab-state.json:

Check item has all required fields filled:
- Problem/Goal filled
- Approach filled
- Success Criteria filled

**If validation fails:** Return to DESIGNING to fill gaps

**If validation passes:**

1. Mark item as documented in workItems:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
   Args: { "project": "<cwd>", "session": "<session>" }
   ```

   Update the item's status in workItems array:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
   Args: {
     "project": "<cwd>",
     "session": "<session>",
     "workItems": [<updated array with item status changed to "documented">]
   }
   ```

2. Update design doc status:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__patch_document
   Args: {
     "project": "<cwd>",
     "session": "<session>",
     "id": "design",
     "old_string": "### Item N: <title>\n**Type:** <type>\n**Status:** pending",
     "new_string": "### Item N: <title>\n**Type:** <type>\n**Status:** documented"
   }
   ```

3. Display: "Item documented. Returning to work item loop."

**Important:** In single-item mode, do NOT:
- Run the full completeness gate
- Transition to rough-draft

## If Gate Fails

1. Identify which sections are incomplete
2. List the specific gaps found
3. Return to DESIGNING phase to fill gaps
4. Do NOT proceed to rough-draft until all sections pass

**Example failure message:**
```
Completeness gate failed:

Missing or incomplete:
- [ ] Key Decisions - No decisions documented
- [ ] Out of Scope - Section is empty

Returning to DESIGNING phase to address these gaps.
```

## If Gate Passes

Show summary and ask for confirmation:

```
Brainstorming complete. Design covers:
- [Bullet 1: key topic from design]
- [Bullet 2: key topic from design]
- [Bullet 3: key topic from design]

Ready to move to rough-draft?

1. Yes
2. No
```

**Response handling:**
- **1 (Yes)**: Transition to rough-draft (invoke brainstorming-transition skill)
- **2 (No)**: Ask what else needs to be explored, return to appropriate phase

## Browser-Based Confirmation

When collab session is active, use render_ui for the confirmation:

```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Confirm" },
    "children": [{
      "type": "Markdown",
      "props": { "content": "Do you want to proceed?" }
    }],
    "actions": [
      { "id": "yes", "label": "Yes", "primary": true },
      { "id": "no", "label": "No" }
    ]
  },
  "blocking": true
}
```

Response: `{ "action": "yes" }` or `{ "action": "no" }`

## Exit Criteria

- All required sections present and complete
- No TBDs or "figure out later" items
- User confirmed ready to proceed

## Transition to Rough-Draft

**Prerequisites:**
- Completeness checklist passed
- User confirmed ready

**Announce:** "Completeness gate passed. Transitioning to rough-draft skill."

**Invoke skill:** brainstorming-transition

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "brainstorming-validating" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
