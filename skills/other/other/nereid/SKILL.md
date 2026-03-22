---
name: nereid
description: Collaborate in Nereid Mermaid sessions via MCP using AST-first, probe-refine workflows for sequence diagrams, flowcharts, xrefs, routes, and walkthroughs. Use when exploring or editing diagrams with a human watching live in TUI, and when coordinating attention through `attention.*`, `follow_ai.*`, and `selection.*`.
---

# Nereid MCP Collaboration

Collaborate on Mermaid-backed diagrams in a live, shared TUI/MCP session. Keep context small, edits structured, and attention explicit.

## Collaboration Contract

Assume co-presence by default:
- The user can see diagram updates in real time.
- The user can see where the agent is focused.
- The agent should steer attention visually, then speak briefly.

Drive collaboration with this state model:
- `attention.human.read`: read the human cursor/attention in TUI.
- `attention.agent.read`: read the agent spotlight object.
- `attention.agent.set`: move the agent spotlight to one object.
- `attention.agent.clear`: clear the agent spotlight.
- `follow_ai.read` / `follow_ai.set`: read or toggle whether TUI follows agent spotlight.
- `selection.read` / `selection.update`: shared working-set selection (multi-object).

Treat these as separate concerns:
- Human attention: what the person is looking at.
- Agent attention: what the agent wants to emphasize now.
- Selection: short-term working set for batch reasoning/edits.
- Follow-AI: whether the TUI camera/cursor tracks agent spotlight.

## Core Principles

- Treat AST as source of truth; rendered text and Mermaid text are projections.
- Session files (`nereid-session.meta.json`, `diagrams/*.mmd`, `walkthroughs/*.wt.json`) are app-managed snapshots and can be rewritten frequently while Nereid runs.
- Use canonical `ObjectRef` everywhere:
  `d:<diagram_id>/<seq|flow>/<participant|message|node|edge>/<object_id>`.
- Prefer small reads first (`diagram.stat`, `diagram.get_slice`, `diagram.diff`, `walkthrough.diff`).
- Use typed query tools (`seq.*`, `flow.*`, `xref.*`, `route.find`) before large snapshots.
- Gate edits with `base_rev` and keep ops minimal.
- Record evidence as refs (xrefs and walkthrough nodes) so reasoning is resumable.
- Keep dangling xrefs visible as TODO artifacts unless asked to clean them.

## Execution Discipline

- Use MCP tools as the only source of truth.
- Do not inspect `src/`, `tests/`, `docs/`, or `data/` to answer runtime collaboration questions.
- Make the first relevant MCP call immediately after reading the user prompt.
- Prefer direct MCP execution over schema/code exploration.
- If payload shape is unclear, call the tool once and adapt from validation errors.
- Use shell/file probing only when the user explicitly asks for file-level inspection or storage debugging.

## Tool Groups

- Diagram lifecycle and target: `diagram.list`, `diagram.open`, `diagram.delete`, `diagram.current`, `diagram.create_from_mermaid`
- Diagram reads: `diagram.stat`, `diagram.get_slice`, `diagram.diff`, `diagram.read`, `diagram.get_ast`, `diagram.render_text`
- Diagram mutation: `diagram.propose_ops`, `diagram.apply_ops`
- Walkthrough lifecycle and target: `walkthrough.list`, `walkthrough.open`, `walkthrough.current`
- Walkthrough reads: `walkthrough.stat`, `walkthrough.diff`, `walkthrough.read`, `walkthrough.get_node`, `walkthrough.render_text`
- Walkthrough mutation: `walkthrough.apply_ops`
- Collaboration state: `attention.human.read`, `attention.agent.read`, `attention.agent.set`, `attention.agent.clear`, `follow_ai.read`, `follow_ai.set`, `selection.read`, `selection.update`, `view.read_state`
- Cross-diagram mapping: `xref.list`, `xref.neighbors`, `xref.add`, `xref.remove`
- Object inspection: `object.read`
- Query helpers (route): `route.find`
- Query helpers (sequence): `seq.messages`, `seq.search`, `seq.trace`
- Query helpers (flow): `flow.reachable`, `flow.paths`, `flow.cycles`, `flow.unreachable`, `flow.dead_ends`, `flow.degrees`

## Default Operating Loop

1. Resolve target:
   - `diagram.current` -> `diagram.list` -> `diagram.open`.
   - `walkthrough.current` -> `walkthrough.list` -> `walkthrough.open`.
   - if no diagram exists yet, bootstrap with `diagram.create_from_mermaid`.
2. Read live collab state:
   - `attention.human.read`, `attention.agent.read`, `follow_ai.read`, `selection.read`.
3. Probe local context:
   - `diagram.stat`, `diagram.get_slice`, then one or two typed queries.
4. Steer visual attention:
   - `attention.agent.set` to the object currently being discussed.
   - keep chat short while attention marker carries micro-guidance.
5. Propose and apply minimal edits:
   - `diagram.propose_ops` -> `diagram.apply_ops`.
   - `walkthrough.apply_ops` for walkthrough refinement.
6. Refresh with deltas:
   - `diagram.diff` / `walkthrough.diff` (avoid full re-read unless needed).

## Live Co-Presence Rules

- Use spotlight-first communication: set `attention.agent.set` before explaining a local change.
- Move spotlight when changing topic; clear it when complete.
- Keep narration compact when user is actively watching the diagram.
- Skip spotlight changes for quick query-only answers unless orientation is needed.
- Use `selection.update` for temporary multi-object working sets, not as a focus proxy.
- For create/switch-only requests, stop after `diagram.create_from_mermaid` (and optional
  `attention.agent.set`); avoid extra `diagram.stat`, `diagram.render_text`, or `flow.*` probes
  unless the user asks for inspection/debugging.

## Tool Contracts (Input/Output)

### `diagram.create_from_mermaid`
Input:
```json
{
  "mermaid": "flowchart TD\n  A --> B",
  "diagram_id": "d-my-flow",
  "name": "My Flow",
  "make_active": true
}
```
Output:
```json
{
  "diagram": {
    "diagram_id": "d-my-flow",
    "name": "My Flow",
    "kind": "flowchart",
    "rev": 0
  },
  "active_diagram_id": "d-my-flow"
}
```

### `diagram.delete`
Input:
```json
{
  "diagram_id": "d-my-flow"
}
```
Output:
```json
{
  "deleted_diagram_id": "d-my-flow",
  "active_diagram_id": "d-next"
}
```

### `diagram.get_slice`
Input:
```json
{
  "diagram_id": "d-flow",
  "center_ref": "d:d-flow/flow/node/n:a",
  "radius": 1,
  "depth": 1,
  "filters": {
    "include_categories": ["flow/node", "flow/edge"],
    "exclude_categories": []
  }
}
```
Output:
```json
{
  "objects": ["d:d-flow/flow/node/n:a", "d:d-flow/flow/node/n:b"],
  "edges": ["d:d-flow/flow/edge/e:ab"]
}
```

### `diagram.apply_ops`
Input:
```json
{
  "diagram_id": "d-seq",
  "base_rev": 3,
  "ops": []
}
```
Output:
```json
{
  "new_rev": 4,
  "applied": 1,
  "delta": { "added": [], "removed": [], "updated": [] }
}
```

### `walkthrough.apply_ops`
Input:
```json
{
  "walkthrough_id": "w:1",
  "base_rev": 0,
  "ops": []
}
```
Output:
```json
{
  "new_rev": 1,
  "applied": 1,
  "delta": { "added": [], "removed": [], "updated": [] }
}
```

### `object.read`
Input:
```json
{ "object_ref": "d:d-seq/seq/block/b:0000" }
```
Output:
```json
{
  "objects": [
    {
      "object_ref": "d:d-seq/seq/block/b:0000",
      "object": {
        "type": "seq_block",
        "kind": "alt",
        "header": "guard",
        "section_ids": ["sec:0000:00", "sec:0000:01"],
        "child_block_ids": []
      }
    },
    {
      "object_ref": "d:d-seq/seq/section/sec:0000:00",
      "object": {
        "type": "seq_section",
        "kind": "main",
        "header": "ok",
        "message_ids": ["m:0000"]
      }
    }
  ],
  "context": {}
}
```

### `attention.human.read`
Input:
```json
{}
```
Output:
```json
{
  "object_ref": "d:d-auth-flow/flow/node/n:authorize",
  "diagram_id": "d-auth-flow"
}
```

### `attention.agent.read`
Input:
```json
{}
```
Output:
```json
{
  "object_ref": "d:d-auth-flow/flow/node/n:authorize",
  "diagram_id": "d-auth-flow"
}
```

### `attention.agent.set`
Input:
```json
{
  "object_ref": "d:d-auth-flow/flow/node/n:authorize"
}
```
Output:
```json
{
  "object_ref": "d:d-auth-flow/flow/node/n:authorize",
  "diagram_id": "d-auth-flow"
}
```

### `attention.agent.clear`
Input:
```json
{}
```
Output:
```json
{
  "cleared": 1
}
```

### `follow_ai.read`
Input:
```json
{}
```
Output:
```json
{
  "enabled": true
}
```

### `follow_ai.set`
Input:
```json
{
  "enabled": true
}
```
Output:
```json
{
  "enabled": true
}
```

### `selection.update`
Input:
```json
{
  "object_refs": [
    "d:d-auth-flow/flow/node/n:start",
    "d:d-auth-flow/flow/node/n:authorize"
  ],
  "mode": "replace"
}
```
Output:
```json
{
  "applied": [
    "d:d-auth-flow/flow/node/n:authorize",
    "d:d-auth-flow/flow/node/n:start"
  ],
  "ignored": []
}
```

## Probe-and-Refine on Charts

Use a shallow, typed exploration loop:
1. Anchor on one object (`attention.human.read` or explicit `object_ref`).
2. Pull local structure with `diagram.get_slice`.
3. Ask one typed question (`seq.*`, `flow.*`, `xref.*`, `route.find`).
4. Shift agent spotlight to next object if needed.
5. Repeat until ambiguity is resolved.

Escalate to global reads (`diagram.read`, `diagram.get_ast`, `diagram.render_text`) only when local probes are insufficient.

## Mutation Discipline

- Use `diagram.propose_ops` before `diagram.apply_ops` for non-trivial edits.
- Keep op batches minimal and scoped to one local intent.
- Use stable IDs for all new objects.
- Re-read `diagram.stat` or `diagram.diff` after apply to confirm resulting rev/state.

## Walkthrough and Evidence Artifacts

Build walkthroughs as resumable breadcrumbs:
- Add concise nodes with evidence refs (`refs`).
- Keep node titles short; put detail in `body_md`.
- Link nodes incrementally as understanding grows.
- Update walkthroughs after edits instead of re-deriving from scratch.

Use xrefs to preserve cross-diagram semantics:
- `xref.add` for implementation/expansion links.
- `xref.list` and `xref.neighbors` for map and traversal.
- Surface dangling xrefs explicitly for follow-up.

## Conflict Recovery

When mutation fails due to stale `base_rev`:
1. call `diagram.diff` or `walkthrough.diff` from last known rev,
2. rebase ops on `current_rev`,
3. retry with updated `base_rev`.

If diff history window is exhausted, fetch a fresh snapshot (`diagram.read` or `walkthrough.read`) and resume delta-first flow.

## Reporting Discipline

Report only what the user needs:
- include target (`diagram_id`/`walkthrough_id`) and revision movement (`base_rev` -> `new_rev`),
- include concise deltas and key refs,
- avoid full AST/text dumps unless requested,
- in live sessions, avoid narrating every micro-step already visible in TUI.

## MCP Playbook Companion

Use `references/mcp-playbooks.md` for extra payload templates. Keep this file as the primary protocol and behavior contract.
