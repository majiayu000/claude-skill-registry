---
name: ASCII Visualizer
description: Use when visualizing architecture, data flows, or system diagrams in text. Creates ASCII visualizer diagrams for plans, workflows, and structures.
version: 1.0.0
context: inherit
tags: [ascii, visualization, diagrams, architecture, 2025]
author: SkillForge
user-invocable: false
---

# ASCII Visualizer Skill

Create clear ASCII visualizations for explaining complex concepts.

## Box-Drawing Characters

**IMPORTANT:** Use a fixed-width (monospace) font for proper rendering.

```
┌─┐│└─┘  Standard weight
┏━┓┃┗━┛  Heavy weight
├─┤┬┴    Connectors
╔═╗║╚═╝  Double lines
```

## Quick Examples

### Architecture
```
┌──────────────┐      ┌──────────────┐
│   Frontend   │─────▶│   Backend    │
│   React 19   │      │   FastAPI    │
└──────────────┘      └───────┬──────┘
                              │
                              ▼
                      ┌──────────────┐
                      │  PostgreSQL  │
                      └──────────────┘
```

### Progress
```
[████████░░] 80% Complete
✅ Design    (2 days)
✅ Backend   (5 days)
🔄 Frontend  (3 days)
⏳ Testing   (pending)
```

See `references/` for complete patterns.

## Related Skills

- `architecture-decision-record` - Document decisions that ASCII diagrams help visualize
- `brainstorming` - Use visualizations to explore and communicate ideas
- `explore` - Visualize codebase structure during exploration

## Capability Details

### architecture-diagrams
**Keywords:** architecture, diagram, system design, components, flow
**Solves:**
- How do I visualize system architecture?
- Show component relationships with ASCII
- Explain system design visually
- Create architecture diagrams in documentation

### workflows
**Keywords:** workflow, process, steps, pipeline, flowchart
**Solves:**
- How do I visualize process flow?
- Show step-by-step workflow with ASCII
- Explain pipeline stages visually
- Document multi-agent workflows

### comparisons
**Keywords:** compare, vs, before after, metrics, changes
**Solves:**
- How do I compare two options visually?
- Show before/after metrics
- Display progress comparison
- Visualize A/B testing results

### file-trees
**Keywords:** file tree, directory, structure, folder hierarchy
**Solves:**
- How do I show directory structure?
- Visualize file hierarchy with ASCII
- Explain codebase organization
- Document project structure

### progress-tracking
**Keywords:** progress, status, completion, percentage, metrics
**Solves:**
- How do I show progress visually?
- Create progress bars with ASCII
- Display completion status
- Track task completion metrics
