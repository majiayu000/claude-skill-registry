---
name: mermaid-diagramming
type: standard
depth: extended
description: >-
  Generates Mermaid v11+ diagrams with YAML frontmatter, ELK layout, and Dracula theming across 22
  types: flowcharts, sequence diagrams, state machines, ER diagrams, class diagrams, mindmaps,
  block diagrams, journey maps, requirement diagrams, pie charts, quadrant charts, sankey diagrams,
  XY charts, radar charts, gantt charts, treemaps, C4 architecture, architecture-beta,
  packet-beta, timelines, gitgraph, and kanban boards. Use when visualizing logic flows, system
  architecture, state transitions, data relationships, temporal sequences, user journeys, project
  timelines, network protocols, or any structured diagram requiring theming, classDef styling, and
  WCAG 2.1 accessibility with accTitle and accDescr annotations.
---

# [H1][MERMAID-DIAGRAMMING]
>**Dictum:** *Modern Mermaid syntax produces consistent, styled diagrams.*

<br>

Mermaid v11+ diagram creation with frontmatter YAML, ELK layout, Dracula palette. 22 diagram types across 5 semantic categories.

**Scope:**
- *Create:* New diagrams from requirements. Select category, load syntax reference, apply styling.
- *Reference:* Syntax lookup for nodes, edges, relationships, charts, architecture.

**Domain Navigation:**
- *[CONFIG]* — Frontmatter YAML, ELK 5-phase layout, direction, limits. Load FIRST for all diagrams.
- *[STYLING]* — Theme presets, themeVariables, classDef, linkStyle, palette. Load for visual customization.
- *[GRAPH]* — Flowchart, mindmap, block. Load for: decision trees, hierarchies, system decomposition.
- *[INTERACTION]* — Sequence, journey. Load for: protocols, request-response, user experience.
- *[MODELING]* — State, ER, class, requirement. Load for: FSM, data models, OOP structure, traceability.
- *[CHARTS]* — Pie, quadrant, sankey, xy, radar, gantt, treemap. Load for: data visualization, project timelines.
- *[ARCHITECTURE]* — C4, architecture-beta, packet-beta, timeline, gitgraph, kanban. Load for: system views, infrastructure, network protocols, version control flow, project boards.

---
## [1][INSTRUCTIONS]
>**Dictum:** *Progressive loading optimizes context.*

<br>

**Required Tasks:**
1. Read [→global-config.md](./references/global-config.md): Frontmatter YAML, ELK layout (required for ALL diagrams).
2. Read [→styling.md](./references/styling.md): Theme, classDef, palette.
3. Select diagram category per §2 table, load corresponding syntax reference.

[REFERENCE]: [→index.md](./references/index.md) — Complete file listing.

**Guidance:**
- `Config First` — Frontmatter YAML must precede diagram declaration. Mermaid parses config before nodes.
- `ELK Layout` — ELK provides comprehensive graph layout via five algorithmic phases: cycle breaking, layering, crossing minimization, node placement, edge routing.
- `Look Options` — Three visual modes: `neo` (default modern), `classic` (traditional), `handDrawn` (sketch aesthetic). Set via `look:` in frontmatter.

**Best-Practices:**
- *Load Sequence* — global-config.md → styling.md → {category}.md → compose. Never skip configuration.
- *Frontmatter Only* — `%%{init:...}%%` directives deprecated v10.5.0. Use YAML frontmatter exclusively.

---
## [2][DIAGRAM_SELECTION]
>**Dictum:** *Category determines semantic structure.*

<br>

| [CATEGORY]   | [TYPES]                                              | [REFERENCE]                                      |
| :----------- | ---------------------------------------------------- | ------------------------------------------------ |
| Graph        | flowchart, mindmap, block                            | [→graph.md](./references/graph.md)               |
| Interaction  | sequence, journey                                    | [→interaction.md](./references/interaction.md)   |
| Modeling     | state, ER, class, requirement                        | [→modeling.md](./references/modeling.md)         |
| Charts       | pie, quadrant, sankey, xy, radar, gantt, treemap     | [→charts.md](./references/charts.md)             |
| Architecture | C4, architecture, packet, timeline, gitgraph, kanban | [→architecture.md](./references/architecture.md) |

**Type Headers:**

| [INDEX] | [TYPE]       | [HEADER]             | [DIR] | [CATEGORY]   |
| :-----: | ------------ | -------------------- | :---: | ------------ |
|   [1]   | Flowchart    | `flowchart LR`       |  LR   | Graph        |
|   [2]   | Mindmap      | `mindmap`            |   —   | Graph        |
|   [3]   | Block        | `block-beta`         |   —   | Graph        |
|   [4]   | Sequence     | `sequenceDiagram`    |  TB   | Interaction  |
|   [5]   | Journey      | `journey`            |   —   | Interaction  |
|   [6]   | State        | `stateDiagram-v2`    |  TB   | Modeling     |
|   [7]   | ER           | `erDiagram`          |  LR   | Modeling     |
|   [8]   | Class        | `classDiagram`       |  TB   | Modeling     |
|   [9]   | Requirement  | `requirementDiagram` |   —   | Modeling     |
|  [10]   | Pie          | `pie`                |   —   | Charts       |
|  [11]   | Quadrant     | `quadrantChart`      |   —   | Charts       |
|  [12]   | Sankey       | `sankey-beta`        |   —   | Charts       |
|  [13]   | XY           | `xychart-beta`       |   —   | Charts       |
|  [14]   | Radar        | `radar-beta`         |   —   | Charts       |
|  [15]   | Gantt        | `gantt`              |   —   | Charts       |
|  [16]   | Treemap      | `treemap-beta`       |   —   | Charts       |
|  [17]   | C4           | `C4Context`          |   —   | Architecture |
|  [18]   | Architecture | `architecture-beta`  |   —   | Architecture |
|  [19]   | Packet       | `packet-beta`        |   —   | Architecture |
|  [20]   | Timeline     | `timeline`           |   —   | Architecture |
|  [21]   | GitGraph     | `gitGraph`           |   —   | Architecture |
|  [22]   | Kanban       | `kanban`             |   —   | Architecture |

**Guidance:**
- `LR Default` — Horizontal flow matches reading order. Sequence/State force TB implicitly.
- `Beta Status` — block, sankey, xy, radar, treemap, architecture, packet, kanban are beta; syntax may change.

**Best-Practices:**
- *Category Match* — Select by primary concern: flow→Graph, time→Interaction, structure→Modeling, data→Charts, system→Architecture.

---
## [3][VALIDATION]
>**Dictum:** *Gates prevent rendering failures.*

<br>

[VERIFY] Before diagram creation:
- [ ] Frontmatter: valid YAML with `config:` key (before diagram declaration).
- [ ] Direction: LR for flowchart/ER, implicit TB for sequence/state.
- [ ] Reserved words avoided: `end`, `default`, `subgraph`, `class` in node IDs.
- [ ] classDef: placed at diagram end, after node definitions.
- [ ] Accessibility: accTitle/accDescr present after diagram type.

[REFERENCE]: [→validation.md](./references/validation.md) — Full validation checklists and anti-patterns.
