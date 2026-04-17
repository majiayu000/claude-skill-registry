---
name: mindnode-ui
description: "Build MindNode-inspired mind mapping interfaces — 8 node shapes, 27+ themes, layout algorithms (horizontal, vertical, radial with D3), keyboard shortcuts, focus mode, dual view. React + xyflow/react v12 + Zustand + Tailwind. Triggers on mind map, visual thinking tool, node-based diagram, brainstorm canvas, MindNode."
---

# MindNode UI

Build mind mapping interfaces inspired by [MindNode](https://www.mindnode.com/) — the Apple-native visual thinking app by IdeasOnCanvas GmbH. This skill encodes MindNode's design system, interaction model, and layout algorithms, adapted for React + ReactFlow + Zustand + Tailwind CSS 3.

## Key Design Principles

- **Visual-first thinking** — spatial canvas for non-linear ideas, outline for linear structure
- **Apple-native aesthetic** — soft rounded elements, generous whitespace, purple accent (#6C63FF)
- **ADHD-friendly** — Focus mode isolates one subtree, Quick Entry captures ideas fast
- **Keyboard-driven** — Tab=child, Return=sibling, arrows=navigate, no mouse required

---

## Quick Reference

### Node Shapes (8)

| Shape | Key | Use Case |
|-------|-----|----------|
| Rounded | Default | General ideas |
| Rectangle | Structured | Facts, definitions |
| Pill | Stadium | Tags, labels |
| Cloud | Organic | Brainstorms |
| Line | Minimal | Subtitles |
| Embedded | Inset | References |
| Hexagon | Process | Decision points |
| Octagon | Warning | Critical items |

### Essential Keyboard Shortcuts

| Action | Mac | Description |
|--------|-----|-------------|
| New child | `Tab` | Add child to selected node |
| New sibling | `Return` | Add sibling after selected |
| New main | `Shift+Return` | Add root-level branch |
| Edit title | `Cmd+Return` | Enter contentEditable mode |
| Navigate | `Arrow keys` | Move between nodes |
| Fold/unfold | `Option+.` | Toggle subtree visibility |
| Cross-link | `Cmd+L` | Connect non-adjacent nodes |
| Mind map view | `Cmd+1` | Switch to canvas view |
| Outline view | `Cmd+2` | Switch to list view |
| Delete | `Backspace` | Remove node, re-parent children |

### Theme Types

| Type | Behavior | Example |
|------|----------|---------|
| Dynamic | Auto light/dark adaptation | Elegant, Fresh |
| Static | Fixed colors | Rainbow, Goth Pastel, Twilight |
| Personal | Extracted from current document | User-defined |

### Layout Directions

| Direction | Root Position | Tree Expands |
|-----------|---------------|-------------|
| Horizontal | Left | Rightward (default) |
| Vertical | Top | Downward |
| Compact | Center | Outward (dense) |
| Radial | Center | All directions (polar) |

---

## Reference Files

Load these on demand based on what aspect of MindNode UI is needed.

### Routing Table

| When working on... | Load |
|---------------------|------|
| Color palette, typography, visual language, Apple aesthetic | [references/design-system.md](references/design-system.md) |
| Node shapes, SVG paths, contentEditable, Node Well | [references/node-types.md](references/node-types.md) |
| Dynamic/static themes, per-level colors, theme gallery | [references/themes.md](references/themes.md) |
| Tree layout, D3 radial, auto-arrange, flexible positioning | [references/layout-algorithms.md](references/layout-algorithms.md) |
| Keyboard shortcuts, focus mode, drag, outline sync | [references/interaction-patterns.md](references/interaction-patterns.md) |
| Dual view (mind map + outline), canvas, connections, export | [references/canvas-and-views.md](references/canvas-and-views.md) |
| ReactFlow custom nodes/edges, Zustand store, performance | [references/reactflow-integration.md](references/reactflow-integration.md) |
| Porting to Project Pilot specifically | [references/project-pilot-porting.md](references/project-pilot-porting.md) |

---

## Key Implementation Patterns

### Node Well (Primary Creation UX)

The plus button appearing on hover/selection that creates a child node. This is MindNode's signature interaction — not a toolbar, not a menu, but a contextual affordance on each node.

→ See [references/node-types.md](references/node-types.md) for implementation details.

### D3 Radial Tree Layout

Compute tree positions with `d3.tree()`, then transform to polar coordinates:
```
x = radius × cos(angle − π/2)
y = radius × sin(angle − π/2)
```

→ See [references/layout-algorithms.md](references/layout-algorithms.md) for full algorithm with code.

### Per-Level Hierarchical Theming

Each theme defines colors per depth level: root (prominent), level 1 (branch colors, cycled from palette), level 2+ (progressively softer). Branch children inherit their parent's color family.

→ See [references/themes.md](references/themes.md) for theme data structures and CSS generation.

### Dual View Sync

Mind map and outline views share a single data model. Changes in either view propagate immediately. Selection state syncs bidirectionally.

→ See [references/canvas-and-views.md](references/canvas-and-views.md) for architecture and data model.

---

## Tech Stack Assumptions

This skill assumes:
- **React 18** with TypeScript
- **@xyflow/react v12** for the canvas (custom nodes, edges, handles)
- **Zustand** for state management (single store with slices)
- **Tailwind CSS 3** with CSS custom properties (`var(--color-*)`)
- **D3** (`d3-hierarchy`, `d3-shape`) for tree layout computation
- **No Framer Motion on ReactFlow nodes** — RF manages transforms, FM would override them

For Project Pilot–specific adaptation, see [references/project-pilot-porting.md](references/project-pilot-porting.md).
