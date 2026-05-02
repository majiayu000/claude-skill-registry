---
name: palace-diagram
description: 'Generate visual diagrams of palace structure, knowledge topology, and synapse connectivity.'
version: 1.9.3
alwaysApply: false
category: visualization
tags:
- memory
- visualization
- mermaid
- diagram
- graph
dependencies:
- memory-palace-architect
usage_patterns:
- palace-visualization
- knowledge-topology
complexity: intermediate
model_hint: standard
estimated_tokens: 400
---

# Palace Diagram

Generate Mermaid and ASCII diagrams from the knowledge
graph, showing palace structure, entity relationships,
synapse connectivity, and tier assignments.

> **Status: unwired**. As of v1.9.4, no command or agent
> invokes `Skill(memory-palace:palace-diagram)`. The skill
> defines the contract but the integration into `/palace`
> (e.g. as `/palace diagram <palace-id>`) is pending. Use
> the `palace_manager.py` script directly until the wiring
> lands. Tracked for follow-up in the April 2026 skill audit.

## When To Use

- Inspecting palace structure after creation or migration
- Understanding knowledge topology and connections
- Identifying strong and weak synapses (heatmap)
- Reviewing entity relationships and triples
- Getting an ASCII overview for inline display

## When NOT To Use

- Creating palaces: use memory-palace-architect
- Searching knowledge: use knowledge-locator
- Code architecture diagrams: use cartograph

## Diagram Types

| Type | Format | Description |
|------|--------|-------------|
| Palace map | Mermaid flowchart | Rooms as subgraphs, entities as nodes, synapses as edges |
| Entity graph | Mermaid flowchart | Single entity's connections and triples |
| Synapse heatmap | Mermaid flowchart | Edge styling by strength (thick=strong, dotted=weak) |
| ASCII overview | Text | Box-drawing palace layout with entity counts |

## Workflow

1. **Identify palace** by ID or name
2. **Choose diagram type** based on what you want to see
3. **Generate diagram** using `PalaceRenderer`
4. **Render** via Mermaid Chart MCP (for Mermaid) or
   display inline (for ASCII)

## Usage

### Palace Map
```python
from memory_palace.knowledge_graph import KnowledgeGraph
from memory_palace.palace_renderer import PalaceRenderer

graph = KnowledgeGraph("path/to/knowledge_graph.db")
renderer = PalaceRenderer(graph)
mermaid = renderer.palace_map("palace_id")
```

Then call `mcp__claude_ai_Mermaid_Chart__validate_and_render_mermaid_diagram`
with the generated Mermaid string.

### ASCII Overview
```python
ascii_art = renderer.ascii_overview("palace_id")
print(ascii_art)
```

### Entity Graph
```python
mermaid = renderer.entity_graph("entity_id")
```

### Synapse Heatmap
```python
mermaid = renderer.synapse_heatmap("palace_id")
```

## Edge Styling

| Strength | Style | Meaning |
|----------|-------|---------|
| >= 0.7 | `==>` (thick) | Strong connection |
| >= 0.4 | `-->` (normal) | Medium connection |
| < 0.4 | `-.->` (dotted) | Weak connection |

## Integration

Works with:

- `memory-palace-architect`: visualize after palace creation
- `knowledge-locator`: display search results as graph
- `graph-analyzer`: tier-informed node sizing
