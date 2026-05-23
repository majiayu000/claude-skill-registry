---
name: html-visual
version: 0.0.1
category: design-frontend
description: "Generate an interactive single-file HTML visualization (mockup, wireframe, ERD, flowchart, chart, slides, architecture diagram, dashboard, timeline, mindmap, kanban, table)."
argument-hint: "[type] <content>"
---

## Input

```text
$ARGUMENTS
```

## Instructions

Visualize the user's request as an **interactive single HTML file**.
First, read `references/common-rules.md` to review common rules.

### Type Determination

Determine the type from the first argument (`$0`).

| Argument | Type | Filename Pattern |
|----------|------|-----------------|
| `mockup` | UI mockup (high-fidelity) | `mockup-{name}.html` |
| `wireframe` | Wireframe (low-fidelity, hand-drawn style) | `wireframe-{name}.html` |
| `erd` | ERD | `erd-{name}.html` |
| `flow` | Flowchart / Sequence diagram | `flow-{name}.html` |
| `chart` | Data chart | `chart-{name}.html` |
| `slides` | Presentation | `slides-{name}.html` |
| `arch` | Architecture diagram | `arch-{name}.html` |
| `dashboard` | Composite dashboard | `dashboard-{name}.html` |
| `timeline` | Timeline / Gantt chart | `timeline-{name}.html` |
| `mindmap` | Mindmap | `mindmap-{name}.html` |
| `kanban` | Kanban board | `kanban-{name}.html` |
| `table` | Interactive data table | `table-{name}.html` |

**No match**: Infer the type from the request content. If unable to infer, ask the user.
When inferred, use `visual-{name}.html` as the filename.

**`{name}` rule**: Extract the core noun from the request and convert to kebab-case. e.g., "user login form" → `login-form`, "payment flow" → `payment-flow`.

### Input Handling

- **File path provided**: Read and analyze the file, then visualize.
  e.g., `/html-visual erd schema.prisma` → Analyze the Prisma schema to auto-generate ERD
- **Existing HTML modification**: Read and modify the existing file. Do not recreate from scratch.
- **Natural language only**: Infer the type, then generate.

### Context Gathering

- **Description is sufficient**: Generate immediately (e.g., "simple login form mockup")
- **Project code reference needed**: Read code/schema/API first (e.g., "our project's ERD", "current payment flow")
- Criterion: If the request contains project context references like "our", "current", "project's", read the code first.

### Type-Specific Guides

#### mockup
- Device frame: Actual device frame shape for mobile/tablet UI
- Multiple screens: Side-by-side layout + screen labels
- Placeholder data: Realistic data matching project context
- Tab/swipe for screen transitions

#### wireframe
- Hand-drawn (sketch) style: Slightly irregular lines, hand-drawn feel
- Black-and-white or grayscale. Minimal color
- Text areas shown as gray blocks (no "Lorem ipsum")
- Focus on layout and information structure, exclude visual details

#### erd
- Entity boxes with attribute lists. Distinguish PK/FK
- Relationship lines: 1:1, 1:N, N:M notation. Auto-track on node drag
- Include relationship type legend

#### flow
- Node types: Start/End (circle), Process (rectangle), Decision (diamond)
- Directional arrows. Auto-track on node drag
- Display branch conditions on connection lines

#### chart
- Auto-select appropriate chart type for the data (bar, line, pie, scatter, etc.)
- Axis labels + units, hover tooltips, legend
- Use Chart.js or D3.js

#### slides
- Reveal.js CDN-based
- Slide transition animations
- Code block highlighting (highlight.js)
- Speaker notes support (toggle with S key)

#### arch
- Separate system components by layer/zone (Frontend / Backend / DB / External)
- Label communication lines with protocols (HTTP, gRPC, pub/sub, etc.)
- Zoom/pan support
- D3.js force-directed or direct SVG generation

#### dashboard
- Arrange multiple charts/metrics in grid layout
- KPI cards at the top (numbers + change rates)
- Cross-chart interaction: Click one → filter others

#### timeline
- Horizontal or vertical timeline
- Event nodes + date labels
- Zoom/scroll for period navigation
- Use Mermaid gantt or D3.js

#### mindmap
- Radial expansion from center node
- Node collapse/expand
- Use Mermaid mindmap or direct SVG generation

#### kanban
- Columns: TODO / In Progress / Done (customizable)
- Drag and drop cards between columns
- Display labels/tags on cards

#### table
- Sort by clicking column headers (ascending/descending)
- Search/filter at the top
- Pagination or virtual scroll
- Cell highlight, row selection

### Procedure

1. **Identify type + target**. Ask if ambiguous. Read the file if a path is provided.
2. **Context gathering decision**. Determine if project context is needed. If so, read relevant code/docs.
3. **Read `references/common-rules.md`**. Review common principles, aesthetics, CDN, and error prevention rules.
4. **Read `references/html-boilerplate.md`**. Start from the base HTML template.
5. **Generate HTML following the type-specific guide**.
6. **Validate**: Review the generated HTML.
   - No smart quotes (curly quotes) in HTML attributes
   - No unclosed tags
   - No overlapping nodes/elements
   - If issues found, fix and re-validate
7. **Instruct to `open {filename}`**.
