---
name: roadmap-task-adder
description: "{{ 𝛀𝛀𝛀 }} Add a task to a project roadmap with correct ID, dependency wiring, and graph integrity. Use this skill whenever the user wants to add a task, feature, or work item to a roadmap — even if they just say 'add this to the roadmap', 'put this in the plan', or 'track this as a task'. Handles task ID assignment, section placement, dependency edges in both directions, and ensures no task is left as an unconnected island."
model: opus
---

# Roadmap Task Adder

Adds a well-formed task to an existing project roadmap. The job is not just appending a line — it's placing the task correctly in the dependency graph, wiring its relationships, and leaving the roadmap in a coherent state.

---

## Step 1 — Locate the roadmap

Check in this order:

1. **User specified a path** — use it directly
2. **`.claude/roadmaps.json`** — parse if present. One entry: use it. Multiple: list and ask.
3. **`docs/roadmaps/` directory** — list `.md` files. One file: use it. Multiple: ask.
4. **Fallback** — `Grep` for `classDef.*mile` to find roadmap files elsewhere.

Read the full roadmap file before proceeding. You need to understand the existing task graph before you can add to it.

---

## Step 2 — Understand what the user wants to add

Extract from the user's description:

- **Task description** — what does this task involve?
- **Milestone** — which milestone does it belong to? If unclear, ask.
- **Category** — which 2–3 letter category prefix fits? Look at existing categories in that milestone.
- **Dependencies** — does this task require anything to be done first? Does it unblock anything that currently exists?

If any of these are ambiguous, ask before proceeding. A badly placed task is worse than a delayed one.

---

## Step 3 — Assign a task ID

Read the existing tasks in the target milestone and category. Find the highest sequence number used for that category, then assign `next = highest + 1`.

Format: `{Milestone}{Category}.{Seq}` — e.g. `2TI.15`, `1WA.4`

Sub-tasks use alpha suffix: `2TI.15a`, `2TI.15b`

**Never reuse an ID**, even if a task was removed.

---

## Step 4 — Identify dependencies

### Incoming dependencies (what this task depends on)

Scan existing tasks for ones that this new task logically requires. Candidates:
- Tasks the user explicitly mentioned
- Tasks whose descriptions suggest they're prerequisites
- Any task marked `:::open` that this task logically extends

If the task has incoming dependencies, it goes in the **Blocked** section (or **To Do** if all its dependencies are already completed).

### Outgoing dependencies (what this task enables)

Scan existing tasks for ones that would be unblocked or directly enabled by this new task. Ask yourself: does completing this task change the status of any existing task in the Blocked section?

If yes, you'll need to add this task as a dependency to those tasks' descriptions and add the corresponding edges to the Mermaid diagram.

---

## Step 5 — Graph integrity checks

Before writing anything, verify:

### Orphan check
A task is orphaned if it has no dependency edges at all — nothing flows into it, nothing flows out of it. This is a warning, not a blocker. Some tasks genuinely stand alone (e.g. a one-off spike, an independent refactor).

If the new task would be orphaned:
- Warn the user: *"This task has no connections to the existing graph. Is that intentional?"*
- Suggest the most plausible connection based on the task description
- Proceed with the user's call

### Childless check
A task is "childless" if nothing depends on it — it's a leaf node with no known successors. This is fine for near-future work, but for tasks that clearly enable further work, it's worth capturing that potential.

If the new task is childless and its nature suggests it unlocks future work:
- Create a placeholder child task in the appropriate future milestone (or the same milestone if relevant)
- Placeholder format: `- [ ] {NewID}. {Unlocked capability} *(placeholder — depends on {NewTaskID})*`
- Place it in the **Blocked** section
- Add the dependency edge in the Mermaid diagram
- Tell the user what placeholder was created and why

Don't create placeholders for tasks that are obviously terminal (e.g. "deploy to production", "write final release notes").

---

## Step 6 — Determine section placement

| Condition | Section |
|-----------|---------|
| All dependencies completed (`[x]`) | **To Do** |
| Has incomplete dependencies | **Blocked** |
| User says work has started | **In Progress** |
| Work is already done | **Completed** |

Default to **Blocked** if uncertain — it's easy to move up.

---

## Step 7 — Prepare the proposal

Do not edit the file yet. Present the proposal:

```
New task: {ID}. {Description}
Milestone: {N} — {Milestone Name}
Section: {Blocked / To Do / In Progress}
Dependencies (in): {list of task IDs, or "none"}
Dependencies (out): {list of task IDs this enables, or "none"}
Placeholder child: {ID and description, or "none"}

Graph changes:
  + node: {ID}["`*{ID}*<br/>**{Category}**<br/>{short desc}`"]:::{open|blocked}
  + edges: {list of new edges}
  ~ modified: {any existing task descriptions updated with new dependency clause}
```

Then ask: *"Does this look right? I'll write to the roadmap on your say-so."*

---

## Step 8 — Write to the roadmap

Once approved:

1. **Add the task line** in the correct section under the correct milestone anchor
   ```markdown
   - [ ] {ID}. {Description} — **depends on {IDs}**
   ```
   Omit the depends clause if there are no incoming dependencies.

2. **Update any existing tasks** whose descriptions now need `— **depends on {NewID}**` added

3. **Update the Mermaid Progress Map** (at `<a name="map">`):
   - Add the node definition
   - Add all new edges
   - If the new task has no incoming dependencies, use `:::open`; otherwise omit (defaults to `:::blocked`)
   - If any existing task's blockers are now all resolved, add `:::open` to it

4. **Add any placeholder child task** in the appropriate section and Mermaid diagram

---

## Step 9 — Confirm

Report:
- Task ID and description added
- Section placed in
- Dependency edges added (list)
- Any existing tasks modified
- Any placeholder tasks created
- Orphan warning if applicable

---

## Conventions

These match the existing roadmap format — never deviate:

- Task line: `- [ ] {ID}. {Description}`
- Dependency clause: ` — **depends on {ID}, {ID}**`
- Completed task: `- [x] {ID}. {Description}`
- Mermaid node: `{ID}["`*{ID}*<br/>**{Category}**<br/>{short desc}`"]`
- Classes: `:::open` (no blockers), default/`:::blocked` (has blockers), `:::mile` (milestone node)
- Edges: `{A} --> {B}` (A must complete before B can start)
