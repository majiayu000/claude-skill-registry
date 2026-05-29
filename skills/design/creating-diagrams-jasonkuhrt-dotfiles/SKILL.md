---
name: creating-diagrams
description: This skill should be used when the user asks to "create a diagram", "draw a flowchart", "visualize the architecture", "show me how X works", "add a diagram to the docs", "create an ASCII diagram", "make a Mermaid chart", or needs visual representation of systems, workflows, data flows, or comparisons. Supports both ASCII (for AI-maintained docs, terminals, code comments) and Mermaid (for rendered markdown).
---

# Creating Diagrams

## Use Cases

Architecture docs, workflows, data flows, comparisons, file trees, sequence diagrams, state machines.

## Operations

### Format Selection

| Format      | Best For                                                 | Renders In         |
| ----------- | -------------------------------------------------------- | ------------------ |
| __ASCII__   | AI-maintained docs, terminals, code comments, git diffs  | Everywhere         |
| __Mermaid__ | Complex auto-layout, dependency trees, sequence diagrams | Markdown renderers |
| __Tables__  | Comparisons, feature matrices                            | Markdown           |

__Key tradeoffs:__

* ASCII: works everywhere, clear git diffs, but manual layout is tedious
* Mermaid: auto-layout, parseable (`@mermaid-js/parser`), but requires renderer

### Creating ASCII Diagrams

Reference `references/ascii-patterns.md` for: box diagrams, flows, file trees, decision branches, sequence diagrams, layered architecture.

### Creating Mermaid Diagrams

Reference `references/mermaid-syntax.md` for: flowcharts, sequence diagrams, state diagrams, class diagrams, Gantt charts.

## CRITICAL

### Right Edge Alignment

__All lines in a boxed diagram must end at the same column.__ Ragged right edges look broken.

__Technique:__

1. Decide width first (e.g., 60 chars)
2. Pad with spaces to hit that width
3. Avoid deep nesting - prefer flat layouts
4. Count characters when unsure

```
WRONG (ragged right edges):
┌───────────────────────────┐
│  Frontend                 │
│  ┌──────┐   ┌───────┐    │
│  │ React│   │ Redux │    │
│  └──────┘   └───────┘│
└───────────────────────────┘
     ↑ inner boxes don't reach right edge

RIGHT (all lines end at same column):
┌──────────────────────────────┐
│  Frontend                    │
│  ┌──────────┐   ┌──────────┐ │
│  │  React   │   │  Redux   │ │
│  └──────────┘   └──────────┘ │
└──────────────────────────────┘
```

## Notes

* Keep within 80-100 columns for terminal compatibility
* Label every box and arrow
* Prefer clarity over detail
* Follow logical flow: left-to-right or top-to-bottom

## Appendix

### Sources

Synthesized from:

* [ascii-visualizer](https://github.com/ArieGoldkin/devPrepAi/tree/main/.claude/skills/ascii-visualizer) by ArieGoldkin
* [Art](https://github.com/vdemeester/home/tree/main/dots/.config/claude/skills/Art) by vdemeester
