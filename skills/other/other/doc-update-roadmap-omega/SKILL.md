---
name: doc-update-roadmap-omega
description: "{{ 𝛀𝛀𝛀 }} Update project roadmap task organization"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Bash(git:*)"]
argument-hint: [roadmap filepath (optional)]
---

Maintain the project roadmap at docs/roadmaps/$ARGUMENTS by moving tasks between sections based on completion status and blockers, and keeping mermaid diagrams in sync.

If $ARGUMENTS provided (e.g., "m1", "m2"), process only that milestone; otherwise process all milestones.

## Steps

1. Read `docs/roadmaps/mvp.md`
2. For each milestone (or specified milestone):

   **Move completed tasks:**
   - Scan "In Progress" and "To Do" sections for tasks marked `- [x]`
   - Move completed tasks to "Completed" section
   - Maintain chronological order (most recent completions at bottom)

   **Move unblocked tasks:**
   - Scan "Blocked" section for tasks that are no longer blocked
   - Infer unblocked status from:
     - Tasks they were waiting on are now complete
     - Prerequisite features mentioned in description now exist
     - External blockers no longer apply (use judgment)
   - Move unblocked tasks to "To Do" section

   **Organize "In Progress":**
   - Suggest moving high-priority "To Do" tasks to "In Progress" if:
     - They're logical next steps after current in-progress work
     - They're blocking other tasks
     - They're explicitly marked as urgent/priority
   - Ask user to confirm moves to "In Progress"

3. **Update Progress Map** (single aggregated diagram at `<a name="map">` section):

   **For completed tasks:**
   - Remove the node definition line entirely (e.g., `1WA.12[...]`)
   - Remove all edge relationships involving that task:
     - As source: `1WA.12 --> X` (remove entire line)
     - As target: `X --> 1WA.12` (remove `1WA.12` from the line, keep other targets)
     - In combined edges: `A --> B & 1WA.12 & C` becomes `A --> B & C`
   - If removal leaves a dangling `&`, clean it up

   **For newly unblocked tasks:**
   - Add `:::open` class to tasks that now have no incoming dependencies
   - A task is unblocked when all its blockers are either completed or removed

4. Preserve task numbering:
   - Never renumber existing tasks
   - Task format: `{Milestone}{Category}.{Seq}` (e.g., 1WA.12, 2TI.7)
   - Sub-tasks: alpha suffix (e.g., 2TI.3a, 2TI.3b)
   - New tasks: append with next number in category sequence

5. Report changes:
   - List tasks moved (from → to, with task ID and description)
   - Group by milestone
   - Highlight any tasks suggested for "In Progress"
   - List Progress Map modifications (nodes removed, edges updated, open classes added)

## Notes

- Preserve all markdown structure, headings, and formatting
- Keep checkbox syntax: `- [ ]` (open/in-progress/blocked), `- [x]` (completed)
- Maintain all section anchors: `#m1-doing`, `#m1-todo`, `#m1-blocked`, `#m1-done`
- Use inference for unblocked detection, but be conservative (when uncertain, leave in Blocked)
- Mermaid class definitions at bottom of Progress Map diagram must remain: `classDef default,blocked fill:#f9f;` etc.
