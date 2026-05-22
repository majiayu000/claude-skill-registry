---
name: brainstorming-clarifying
description: The CLARIFYING phase discusses each item one at a time to fully understand requirements
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# CLARIFYING Phase

The CLARIFYING phase discusses each item one at a time to fully understand requirements before designing.

## Purpose

- Discuss ONE item at a time (never batch multiple items)
- Ask questions to refine each item
- Ensure all requirements are captured
- Confirm nothing else needs discussion

## Process

1. **Present first item:**
   - State the item clearly
   - Ask clarifying questions about it

2. **For each item:**
   - Ask questions to refine understanding
   - Prefer multiple choice questions when possible
   - One question at a time
   - Wait for answer before next question

3. **After each item is discussed:**
   - Summarize understanding
   - Move to next item

4. **After all items discussed:**
   - Ask: "Is there anything else?"
   - Only proceed when user confirms nothing else

## Single-Item Mode (CLARIFYING)

When `currentItem` is set in collab-state.json:

- Ask questions about this specific item (one at a time)
- Do NOT explore other items or expand scope
- Ask: "Is there anything else about this item?"

## Incremental Design Doc Updates

After each substantive user answer during CLARIFYING phase:

1. Output: "Updating [field] for Item [N]..."
2. Read current design doc via MCP
3. Update the relevant field (Problem/Goal, Approach, Success Criteria, or Decisions)
4. Write updated doc via MCP
5. Output: "Updated [field] for Item [N]"

This ensures context survives compaction - the design doc is the persistent record.

## Question Best Practices

**Prefer multiple choice:**
```
Which approach do you prefer?

1. Option A - [brief description]
2. Option B - [brief description]
3. Other (please specify)
```

**Use browser-based questions when collab session active:**

```
Tool: mcp__plugin_mermaid-collab_mermaid__render_ui
Args: {
  "project": "<absolute-path-to-cwd>",
  "session": "<session-name>",
  "ui": {
    "type": "Card",
    "props": { "title": "Select an option" },
    "children": [{
      "type": "MultipleChoice",
      "props": {
        "options": [
          { "value": "1", "label": "Option 1" },
          { "value": "2", "label": "Option 2" }
        ],
        "name": "choice"
      }
    }],
    "actions": [{ "id": "submit", "label": "Submit", "primary": true }]
  },
  "blocking": true
}
```

## Auto-Decomposition Check

**REQUIRED** before transitioning to DESIGNING, for each work item:

1. **Analyze item scope:**
   - Count affected files mentioned in approach
   - Count distinct concerns (auth, API, UI, tests, etc.)
   - Estimate number of tasks

2. **If item looks large (any of these triggers):**
   - More than 5-6 files affected
   - More than 2 distinct concerns
   - Would result in more than 10 tasks

3. **Present decomposition proposal:**
   ```
   This item looks large:
   - Files: [N] affected
   - Concerns: [list distinct areas]
   - Estimated tasks: [N]

   I see [N] pieces:
   1. [Sub-component 1]: [files/concern]
   2. [Sub-component 2]: [files/concern]
   3. [Sub-component 3]: [files/concern]

   Split into separate work items?

   1. Yes - split into [N] items (Recommended for complex work)
   2. No - keep as single item
   ```

4. **If user selects 1 (Yes):**
   - Create new work items in design doc for each sub-component
   - Mark original item as superseded
   - Continue CLARIFYING with new items

5. **If user selects 2 (No):**
   - Keep as single item
   - Proceed to DESIGNING

**Why auto-decomposition matters:**
- Smaller items create smaller per-item documents
- Smaller documents reduce context bloat
- Parallel execution of independent items

## Exit Criteria

- Each item discussed individually (not batched)
- Asked "Is there anything else?"
- User confirmed nothing else to discuss

## Transition to DESIGNING

**Prerequisites:**
- Each item discussed individually (not batched)
- Asked "Is there anything else?"
- User confirmed nothing else to discuss

**Announce:** "All items clarified. Now let me present the design approach."

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "brainstorming-clarifying" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
