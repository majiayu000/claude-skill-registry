---
name: obsidian-mermaid-expert
description: Mermaid diagram plugin expertise for flowcharts and diagrams
category: Session Knowledge
---

# Skill: obsidian-mermaid-expert

## What I do

I provide expertise in creating Mermaid diagrams within Obsidian, transforming technical concepts and workflows into clear, version-controllable visual documentation.

## When to use me

- When documenting system architecture or component relationships in the knowledge base.
- When visualising complex logic, decision trees, or algorithm control flows.
- When creating sequence diagrams for API interactions or object-oriented message passing.
- When mapping state machines, lifecycles, or business processes.
- When designing database schemas (ER diagrams) or class structures.
- When project timelines require Gantt charts or branch strategies require Git graphs.

## Core principles

1. **Declarative Clarity**: Describe *what* the structure is, not *how* to draw it. Focus on relationships and logical grouping.
2. **Atomic Modularity**: Prefer multiple focused diagrams over a single monolithic "god-diagram". Split complexity across notes using sub-headings or linked files.
3. **Progressive Disclosure**: Use subgraphs and clear labelling to hide implementation details until necessary. Start with high-level flows before diving into sub-processes.
4. **Consistency**: Use uniform node shapes (e.g., diamonds for decisions, rectangles for processes) and consistent terminology that matches the codebase.

## Diagram types

### Flowchart
Used for process flows, decision trees, and algorithm logic.
- **Direction**: `TD` (Top-Down) or `LR` (Left-Right)
- **Example**: `A[Start] --> B{Valid?} --> C[Process]`

### Sequence Diagram
Visualises object interactions and message passing.
- **Example**: `C->>S: Request` then `S-->>C: Response`

### State Diagram
Ideal for object lifecycles and workflow transitions.
- **Example**: `[*] --> Idle --> Busy --> [*]`

### Class Diagram
Useful for documenting interfaces and OO structures.
- **Example**: `class Repository { +Save() +Find() }`

### Entity-Relationship Diagram (ERD)
Standard for database schema documentation.
- **Example**: `USER ||--o{ POST : "writes"`

### Gantt Chart & Git Graph
Used for project management and branch strategy visualisations.
- **Gantt**: `gantt`, `section`, `task name :a1, 2024-01-01, 30d`
- **GitGraph**: `gitGraph`, `commit`, `branch`, `merge`

## Obsidian-specific considerations

- **Theme Compatibility**: Mermaid adapts to dark/light themes. Use `classDef` for semantic styling.
- **Rendering Limits**: Large diagrams (100+ nodes) may lag. Break into subgraphs or separate files.
- **Interactivity**: Link nodes to notes: `click NodeID "[[Other Note]]"`
- **Live Preview**: Verify in Reading mode; syntax errors prevent rendering.
- **Multi-line node labels**: `\n` does NOT create a newline in Obsidian's Mermaid renderer. Use `<br/>` inside **quoted** strings instead:
  - ✅ Correct: `A["first line<br/>second line"]`
  - ❌ Wrong: `A[first line\nsecond line]`

## When to use Mermaid vs alternatives

- **Mermaid**: Technical documentation, architecture, logic flows, state machines
- **ChartJS**: Data visualisations, bar/line charts, statistics
- **Canvas**: Non-linear brainstorming, spatial layouts
- **DataViewJS**: Dynamic tables from vault metadata

## Anti-patterns to avoid

❌ **Using `\n` for newlines in node labels**: `A[label\nsecond line]` renders literally as `label\nsecond line` in Obsidian. Use `<br/>` inside quoted strings: `A["label<br/>second line"]`.
❌ **Monolithic Diagrams**: Trying to fit an entire system into one `flowchart`. It becomes unreadable.
❌ **Missing Labels**: Using `A --> B` without describing the transition or relationship.
❌ **Inconsistent Naming**: Mixing `CamelCase` and `snake_case` in node IDs or labels.
❌ **Over-styling**: Using too many custom colours that clash with the user's Obsidian theme.
❌ **Deep Nesting**: Subgraphs inside subgraphs inside subgraphs (max 2 levels recommended).

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Session-Knowledge/Obsidian Mermaid Expert.md`

## Related skills

- `architecture` – Mapping system components.
- `documentation-writing` – Enhancing prose with visual aids.
- `obsidian-structure` – Organising diagrams within the PARA framework.
- `domain-modeling` – Using ERDs and Class diagrams to define domains.
