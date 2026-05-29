---
name: brainstorming-designing
description: The DESIGNING phase presents the design approach in small, validated sections
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# DESIGNING Phase

The DESIGNING phase presents the design approach in small, validated sections.

## Purpose

- Propose and explore different approaches
- Present design in 200-300 word sections
- Get explicit user validation for each section
- Create visual diagrams for architecture and UI

## Process

### 1. Exploring Approaches

Before writing the design:

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

### 2. Presenting Sections

For each section of the design:

1. Write section to design doc with `[PROPOSED]` marker
2. Tell user: "I've added a proposed section: **[Section Name]**"
3. Provide preview link: "Review at: [mermaid-collab preview URL]"
4. Ask: "Accept this section?"
   ```
   1. Accept
   2. Reject
   3. Edit
   ```

**User responses:**
- **1 (Accept)**: Remove `[PROPOSED]` marker, continue to next section
- **2 (Reject)**: Discuss what's wrong, revise the section, repeat from step 1
- **3 (Edit)**: User edits directly in browser, Claude acknowledges changes and continues

### 3. Section Size

- Keep sections to 200-300 words
- One concept per section
- Get validation before moving to next

## Single-Item Mode (DESIGNING)

When `currentItem` is set in collab-state.json:

Update the work item in the design doc with:
- `**Problem/Goal:**` - documented problem/goal
- `**Approach:**` - documented approach
- `**Success Criteria:**` - documented criteria
- `**Decisions:**` - any item-specific decisions

## Checkpoint: Approach Diagram

**REQUIRED** for each proposed approach:

Before presenting an approach to the user, create a diagram visualizing it:

```
Tool: mcp__plugin_mermaid-collab_mermaid__create_diagram
Args: {
  "project": "<cwd>",
  "session": "<session>",
  "name": "approach-N",
  "content": <flowchart/sequence showing the proposed approach>
}
```

Do NOT describe architecture or flow in text alone. Show it visually, then explain.

## Visualizing with Mermaid Collab

When brainstorming involves visual artifacts, use the mermaid-collab server.

**GUI/UI Design (ALWAYS use wireframes):**
- When discussing screens, layouts, or user interfaces -> create wireframe diagrams
- Use `create_diagram(name, content)` with wireframe syntax
- Iterate on wireframes as the design evolves
- Preview with `preview_diagram(id)` so user can see in browser

**Architecture and Flow Design:**
- System architecture -> flowchart diagrams
- Data flow -> sequence or flowchart diagrams
- State machines -> SMACH YAML or state diagrams
- Component relationships -> class or flowchart diagrams

**Design Documents:**
- Use `create_document(name, content)` for design specs
- Iterate on documents with `update_document(id, content)`
- Link related diagrams in the document

**Workflow:**
1. During "Exploring approaches" phase, create diagram(s) to visualize options
2. During "Presenting the design" phase, update diagrams to match validated sections
3. When writing final design doc, embed diagram references

## Design Completeness Checklist

Before moving to VALIDATING, ensure:

- [ ] Every screen/UI has a wireframe in mermaid-collab
- [ ] Every data flow/architecture decision has a diagram
- [ ] No ambiguous language ("should handle errors appropriately" -> specify HOW)
- [ ] No TBD or "figure out later" items
- [ ] Success criteria are measurable, not subjective

## Live Design Doc Updates

When brainstorming within a collab session, update the design document using MCP tools.

**Prefer patch operations for targeted changes:**

For small, targeted edits (updating a single field, adding a bullet point, changing status):

```
Tool: mcp__plugin_mermaid-collab_mermaid__patch_document
Args: {
  "project": "<cwd>",
  "session": "<name>",
  "id": "design",
  "old_string": "<exact text to find>",
  "new_string": "<replacement text>"
}
```

**Use full update only when:**
- Adding entirely new sections
- Restructuring large portions of the document
- Patch fails (old_string not found or matches multiple locations)

**Fallback to full update:**

1. Read current content:
   Tool: mcp__plugin_mermaid-collab_mermaid__get_document
   Args: { "project": "<cwd>", "session": "<name>", "id": "design" }

2. Modify content as needed (add sections, update decisions, etc.)

3. Write updated content:
   Tool: mcp__plugin_mermaid-collab_mermaid__update_document
   Args: { "project": "<cwd>", "session": "<name>", "id": "design", "content": "<full-updated-content>" }

**Important:** Always read before full update to preserve existing content.

## Exit Criteria

- Each section (200-300 words) presented separately
- User validated each section
- All required design areas covered

## Backtracking

Can return to CLARIFYING phase if:
- User raises new questions
- Something doesn't make sense
- Need to gather more context

**Announce:** "Let me go back and clarify that before continuing the design."

## Transition to VALIDATING

**Prerequisites:**
- Each section (200-300 words) presented separately
- User validated each section

**Announce:** "Design sections complete. Let me run the completeness gate."

## Completion

At the end of this skill's work, call complete_skill:

```
Tool: mcp__plugin_mermaid-collab_mermaid__complete_skill
Args: { "project": "<cwd>", "session": "<session>", "skill": "brainstorming-designing" }
```

**Handle response:**
- If `action == "clear"`: Invoke skill: collab-clear
- If `next_skill` is not null: Invoke that skill
- If `next_skill` is null: Workflow complete
