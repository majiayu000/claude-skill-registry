---
name: figma-sub-agents
description: "Orchestrator guide for delegating Figma MCP phases to specialized sub-agents. Use when a Figma task is large enough to risk context overflow — component sets with 8+ variants, unknown tree depth, or sessions expected to exceed 100 tool calls. Supports both serial discovery and parallel build/style phases."
---

# Figma MCP Sub-Agent Orchestration

Large Figma sessions hit three problems in a single-agent context: **context pressure** (large node tree responses), **attention drift** (losing track of which nodes are done after 30+ sequential calls), and **error pollution** (9 retries of a failing tool consuming planning context). Sub-agents solve this by giving each phase its own clean context window.

The primary tool for reading nodes is **`get`**, which returns structured YAML (FSGN format) with deduplicated variable/style/component defs and a `tokenEstimate` in the meta. It accepts `nodeId` (single) or `nodeIds` (multiple, fetched in parallel).

Sub-agents also enable **parallel execution**: multiple agents can modify different parts of the Figma document simultaneously, with plugin-level concurrency control ensuring safety.

**Available sub-agents:**
- **Discovery** (`figma-discovery` agent) — read-only exploration, always runs serial
- **Builder** (general-purpose agent) — creates/clones node structures, can run in parallel
- **Styler** (general-purpose agent) — applies variables and text styles, can run in parallel

---

## When to Use Sub-Agents

### Discovery — delegate when **any** of these are true:
- Target component set has **8+ variants**
- Frame tree depth is unknown or likely > 4 levels
- This is the first time seeing this Figma file in the session
- A `get` response has `tokenEstimate > 8000` even at `detail=structure`
- You need both a full text node inventory AND a variable binding audit in the same pass

**Skip it when** you already have the node IDs and structure, the target has < 20 children, or you only need one piece of info (just call the tool directly).

### Builder/Styler — delegate when:
- Build spec has **5+ nodes** to create or clone
- Binding plan has **20+ variable bindings** or text style assignments
- Work can be partitioned into **independent node subtrees** (different variants, different sections)
- You want to parallelize to reduce wall-clock time

---

## Execution Protocol

### Channel Setup (always do this first)

1. **Orchestrator joins the channel first.** Call `join_channel` (no args) before spawning any sub-agent.
2. **Pass the channel name explicitly** in every sub-agent prompt. Do not let sub-agents auto-discover — this avoids race conditions.
3. **Check `status` first** in every sub-agent result — if `"blocked"`, surface the error to the user and stop.

### Serial Phases (must be in order)

```
Discovery → Planning → Building → Styling → Verification
```

Discovery always runs alone. Planning happens in the orchestrator. Verification happens in the orchestrator.

### Parallel Execution (within Building or Styling phases)

The Figma plugin has concurrency control that makes parallel agent execution safe:
- **Node-level write locks** prevent two agents from writing to the same node simultaneously
- **Global mutex** serializes tree-mutation operations (`create`, `delete_multiple_nodes`, etc.)
- **Concurrency cap** (max 6 in-flight operations) prevents Figma CPU budget exhaustion

**Rules for parallel sub-agents:**

1. **Partition by node subtree.** Each agent operates on a **disjoint set of nodes**. Partition by variant, by section, or by component — never assign the same node to two agents.
2. **Don't mix phases.** Don't run a Builder and Styler in parallel — build everything first, then style everything. The Styler needs the nodes to exist before it can bind variables.
3. **Use `run_in_background: true`** on the Agent tool to launch parallel agents. You will be notified when each completes.
4. **All agents share one channel.** Sub-agents share the parent's MCP server and WebSocket connection. Request ID correlation handles response routing — no multi-channel needed.
5. **Verify after parallel phases.** After all parallel agents complete, call `get(nodeId, detail="structure")` on the parent to confirm the expected structure.
6. **Max 3 parallel agents** for build/style phases. More than 3 creates diminishing returns and risks hitting the plugin's concurrency cap (6 in-flight operations, ~2 per agent).

### Partitioning Strategies

**By variant** (most common): Each agent handles a disjoint set of variants within a component set.
```
Agent A: Build/style variants for State=Loading  (nodes A1-A5)
Agent B: Build/style variants for State=Empty    (nodes B1-B5)
Agent C: Build/style variants for State=Selection (nodes C1-C5)
```

**By section**: Each agent handles a different top-level section of the page.
```
Agent A: Build Header component set
Agent B: Build Sidebar component set
Agent C: Build Footer component set
```

**By operation type** (for styling): Each agent handles a different type of binding.
```
Agent A: Bind all color variables
Agent B: Apply all text styles
Agent C: Bind all spacing/radius variables
```
Note: this only works if each node gets only ONE type of binding per agent. If a node needs both a color variable and a text style, assign that node to ONE agent that does both.

---

## Discovery Sub-Agent

The agent definition lives at `.claude/agents/figma-discovery.md`. It has:
- A read-only tool set (no create/modify tools)
- A system prompt with its full workflow and output schema

**Tools available to the agent:** `join_channel`, `get`, `scan_text_nodes`, `get_local_variables`, `get_styles`, `get_local_components` (plus `ToolSearch` to load them). Note: `get_main_component` is no longer needed — `get` includes component metadata in `defs.components`.

### Spawning the Agent

Use the Agent tool with `subagent_type: "figma-discovery"`. The prompt only needs task-specific parameters — no system prompt needed.

```
Agent(
  subagent_type: "figma-discovery",
  description: "Discover <component name> structure",
  prompt: JSON.stringify({
    channelName: "<from your join_channel call>",
    nodeId: "<target component set or frame ID>",
    description: "Map DataViews component set",
    include: ["text_nodes", "variables", "text_styles"],
    nameFilter: "DataRow"   // omit if not filtering components
  })
)
```

Valid `include` values: `text_nodes`, `variables`, `text_styles`, `components`.

### Using the Result

The agent's final message is JSON. Parse it immediately:

```
const discovery = JSON.parse(agentResult);

if (discovery.status === "blocked") {
  // Surface to user: discovery.error + discovery.recommendation
  // Do NOT proceed to build/style phases
} else {
  // discovery.component_set.variants[].id → parentId values for create/clone calls
  // discovery.component_sets_in_frame     → all component sets when target is a FRAME (pick one to deep-map)
  // discovery.text_nodes[]                → input for apply (variables, textStyleId)
  // discovery.unbound_nodes               → if >= 20, a Styler phase is needed; null = unknown
  // discovery.variables                   → sanity-check tokens are loaded
  // discovery.summary                     → user-facing status message
  //
  // Variant children now include:
  //   layoutMode       → auto-layout direction (if active)
  //   boundVariables   → list of bound field names (e.g. ["fill", "cornerRadius"])
  //   componentName/Id → resolved for INSTANCE nodes via defs.components in FSGN
}
```

### Output Schema Reference

**Success:**
```json
{
  "status": "success",
  "component_sets_in_frame": [
    { "id": "...", "name": "DataViews", "type": "COMPONENT_SET", "variantCount": 16 },
    { "id": "...", "name": "DataForm", "type": "COMPONENT_SET", "variantCount": 2 }
  ],
  "component_set": {
    "id": "...",
    "name": "...",
    "variant_properties": ["Layout", "State"],
    "variants": [
      {
        "id": "...",
        "name": "Layout=List, State=Default",
        "children": [
          { "id": "...", "name": "Header", "type": "FRAME", "layoutMode": "HORIZONTAL", "boundVariables": ["fill", "cornerRadius"] },
          { "id": "...", "name": "Row 1", "type": "INSTANCE", "componentName": "_Dataviews/Table/Row", "componentId": "2254:11156", "boundVariables": [] }
        ]
      }
    ]
  },
  "text_nodes": [
    { "id": "...", "name": "Title", "parentVariantId": "16547:36681", "content": "Activity", "style": "Heading MD", "fills_variable": null }
  ],
  "variables": {
    "collections": ["Primitives", "Semantic"],
    "total_count": 84,
    "by_collection": {
      "Semantic": [
        { "id": "VariableID:15613:5786", "name": "gray-700", "type": "COLOR" },
        { "id": "VariableID:15613:5784", "name": "surface-primary", "type": "COLOR" }
      ]
    }
  },
  "text_styles": [
    { "name": "Heading MD", "id": "S:5a04abc..." },
    { "name": "Body SM", "id": "S:7b12def..." }
  ],
  "unbound_nodes": 47,
  "summary": "4 variants exist. 47 nodes have no variable bindings. 12 text nodes have no text style."
}
```

**Blocked:**
```json
{
  "status": "blocked",
  "error": "get timed out twice",
  "last_tool": "get",
  "recommendation": "Call join_channel again — connection may have dropped"
}
```

---

## Builder Sub-Agent

Creates or clones node structures. Uses general-purpose agent type (not a custom agent definition — the prompt contains all instructions).

### Spawning

```
Agent(
  description: "Build [description] variants",
  run_in_background: true,  // for parallel execution
  prompt: `You are a Figma Builder agent. The WebSocket channel is already joined —
call join_channel with channelName "${channelName}" as your first action.

YOUR ASSIGNED NODES (do NOT touch anything outside this list):
${JSON.stringify(assignedNodes)}

WHAT TO BUILD:
${buildSpec}

RULES:
- Use create for complex structures (reduces many calls to 1)
- Use clone_node + clone_and_modify when duplicating existing patterns
- Use create with type="INSTANCE" and componentId for reusing library parts
- After creating nodes, verify with get(nodeId, detail="structure") that structure matches spec
- Return JSON: {"status": "success", "created_nodes": [...ids], "summary": "..."}
- If any tool fails twice on the same call, stop and return: {"status": "blocked", "error": "...", "last_tool": "...", "recommendation": "..."}
`
)
```

### When to Parallelize Builders

- Multiple independent variants to create (e.g., 4 State variants each with the same structure)
- Multiple independent component sets to build
- Large `create` specs that don't share parent nodes

### Output

```json
{
  "status": "success",
  "created_nodes": ["16547:36700", "16547:36701", "16547:36702"],
  "summary": "Created 3 Loading state variants with 4 children each"
}
```

---

## Styler Sub-Agent

Applies variable bindings and text styles. Uses general-purpose agent type.

### Pre-flight with get

Before spawning Styler agents, the orchestrator can call `get(nodeId, detail="full")` on the built subtree. The FSGN `defs` section lists all variables and styles already present; `variableBindings` on each node shows what's already bound. This makes the binding plan explicit — pass it directly to the Styler via `VARIABLE BINDINGS TO APPLY`.

### Spawning

```
Agent(
  description: "Style [description] variants",
  run_in_background: true,  // for parallel execution
  prompt: `You are a Figma Styler agent. The WebSocket channel is already joined —
call join_channel with channelName "${channelName}" as your first action.

YOUR ASSIGNED NODES (do NOT touch anything outside this list):
${JSON.stringify(assignedNodes)}

VARIABLE BINDINGS TO APPLY:
${JSON.stringify(bindings)}

TEXT STYLE ASSIGNMENTS:
${JSON.stringify(textStyles)}

RULES:
- Use apply() with variables field to bind design tokens to node properties (supports flat list or nested tree)
- Use apply() with textStyleId to apply text styles (deduplicates font loading automatically)
- Process in order: variable bindings first, then text styles
- After applying, verify a sample node with get(nodeId, detail="full") to confirm bindings took
- Return JSON: {"status": "success", "bindings_applied": N, "styles_applied": N, "summary": "..."}
- If any tool fails twice on the same call, stop and return blocked status
`
)
```

### When to Parallelize Stylers

- 40+ bindings to apply across different node subtrees
- Multiple variants that each need independent styling
- Different sections of a page with no shared nodes

### Binding Plan Format

The orchestrator prepares a binding plan from Discovery output and passes it to each Styler:

```json
{
  "bindings": [
    { "nodeId": "16547:36700", "field": "fill", "variableId": "VariableID:15613:5786" },
    { "nodeId": "16547:36701", "field": "cornerRadius", "variableId": "VariableID:15613:5800" }
  ],
  "textStyles": [
    { "nodeId": "16547:36710", "styleId": "S:5a04abc..." },
    { "nodeId": "16547:36711", "styleId": "S:7b12def..." }
  ]
}
```

### Output

```json
{
  "status": "success",
  "bindings_applied": 22,
  "styles_applied": 8,
  "summary": "Applied 22 variable bindings and 8 text styles to Loading variants"
}
```

---

## Parallel Session Example

```
TIME    ORCHESTRATOR              BUILDER-A             BUILDER-B
─────   ────────────              ─────────             ─────────
0:00    join_channel
0:01    → Discovery agent
0:03    ← discovery JSON
0:04    Plan: partition by State
0:05    → Builder A (Loading)     create ──►
0:05    → Builder B (Empty)                             create ──►
        [both run_in_background]
0:07                              ◄── done              ◄── done
0:08    verify structure

TIME    ORCHESTRATOR              STYLER-A              STYLER-B
─────   ────────────              ────────              ────────
0:09    → Styler A (Loading)      batch_bind ──►
0:09    → Styler B (Empty)                              batch_bind ──►
        [both run_in_background]
0:11                              ◄── done              ◄── done
0:12    verify bindings
0:13    Report to user
```

**Estimated speedup:** For a 16-variant component set with 130+ variable bindings:
- Serial: ~36 minutes
- Parallel (3 agents): ~19 minutes (~1.9x speedup)

The speedup scales with workload size. Design system builds with 50+ components see larger gains because build and style phases dominate.

---

**Post-session**: After completing a large Figma session (50+ tool calls), run `/analyze-session` to capture efficiency metrics, error patterns, and improvement recommendations.
