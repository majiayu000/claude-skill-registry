---
name: walkthrough
description: Generate interactive HTML walkthroughs with clickable Mermaid diagrams (flowcharts and ER diagrams) that explain codebase features, flows, architecture, and database schemas. Use when asked to "walkthrough", "explain this flow", "how does X work", "trace the code path", "annotated diagram", "code walkthrough", "explain the architecture of", "walk me through", "database schema", "explain the tables", "data model".
---

# Codebase Walkthrough Generator

Generate interactive HTML files with clickable Mermaid diagrams that give new developers a **quick mental model** of how a feature or system works. The goal is fast onboarding — a rough map of concepts and connections, not a code reference. Each walkthrough should be readable in under 2 minutes.

**Always dark mode.** Every walkthrough uses a pure black background (`#000000`), white text, and purple accents. Never generate light-mode walkthroughs.

## Workflow

### Step 1: Understand the scope

Clarify what the user wants explained:
- A specific feature flow (e.g., "how does canvas drawing work")
- A data flow (e.g., "how does state flow from composable to component")
- An architectural overview (e.g., "how are features organized")
- A request lifecycle (e.g., "what happens when a user clicks draw")
- A database schema (e.g., "explain the tables and relationships")
- A data model (e.g., "how is user data structured")

Frame the walkthrough as a **mental model for someone new**. Think: "What are the 5-12 key concepts, and how do they connect?"

If the request is vague, ask one clarifying question. Otherwise proceed.

### Step 2: Explore the codebase with parallel subagents

**Always read real source files before generating.** Never fabricate code paths.

**Use the Task tool to delegate exploration to subagents.** This keeps the main context clean for HTML generation and parallelizes the research phase.

#### 2a. Identify areas to explore

Do a quick Glob/Grep yourself (1-2 calls max) to identify the relevant directories and file groups. Then split the exploration into 2-4 independent research tasks.

#### 2b. Launch parallel Explore subagents

Use `Task` with `subagent_type: "Explore"` to launch multiple agents **in a single message** (parallel). Each agent should investigate one area and report back the **purpose and connections** of each piece — not code dumps.

**Give each subagent a focused prompt that asks it to return a structured report with:**
- What the piece does (purpose) and why it exists (role in the system)
- How it connects to other pieces (imports, calls, data flow)
- A suggested node ID (camelCase) and plain-English label (e.g., "Drawing Interaction", not "useDrawingInteraction()")
- The primary file path(s)
- **Only if truly illuminating**: a single key code snippet (max 5 lines) — most nodes should have no code

**Tell each subagent to format its report as a list of nodes like this:**

```
NODE: drawingInteraction
  label: Drawing Interaction
  file: app/features/tools/useDrawingInteraction.ts
  purpose: Converts pointer events into shape data. This is the bridge between raw mouse input and the element model.
  connects_to: canvasRenderer (feeds shape data), toolState (reads active tool)
  key_snippet (optional):
    const element = createElement(tool, startPoint, currentPoint)
    lang: typescript
```

Note: Most nodes should NOT include a snippet. Only include one when it's the single most illuminating piece — a key type definition, the core 3-line algorithm, etc.

**Example: splitting a "drawing tool" walkthrough into subagents:**

```
Subagent 1: "Explore user input handling"
→ Read tool selection, pointer event handling
→ Report: purpose of each piece, how they connect

Subagent 2: "Explore rendering pipeline"
→ Read canvas rendering, scene management
→ Report: what renders elements, how it gets triggered

Subagent 3: "Explore element model and state"
→ Read element types, state management
→ Report: how elements are stored, what shape they have
```

**Do NOT read the files yourself** — let the subagents do it. Your job is to orchestrate and then synthesize their results into the HTML.

#### 2c. Synthesize subagent results (no more file reads)

Once all subagents return, you have everything needed. **Do NOT read any more files or launch more subagents.** Go directly to Steps 3-4.

Combine subagent findings into:
1. **Node list** — ID, plain-English label, primary file(s), 1-2 sentence description, optional code snippet + lang
2. **Edge list** — which nodes connect, with plain verb labels ("triggers", "feeds into", "produces")
3. **Subgraph groupings** — 2-4 groups with approachable labels ("User Input", "Processing", "Output")

**Keep to 5-12 nodes total.** Each node represents a *concept*, not a function. Group related functions into a single node. If you have more than 12 nodes, merge related ones.

If a subagent's report is missing info for a node, drop that node rather than reading files yourself.

### Step 3: Choose the diagram type

Pick the Mermaid diagram type based on the topic:

| Topic | Diagram Type | Mermaid Syntax |
|-------|-------------|----------------|
| Feature flows, request lifecycles, architecture | **Flowchart** | `graph TD` / `graph LR` |
| Database schemas, table relationships, data models | **ER Diagram** | `erDiagram` |
| Mixed (API flow + DB schema) | **Both** — render two diagrams side by side or stacked | Flowchart + ER |

**Diagram sizing**: Keep to **5-12 nodes** grouped into **2-4 subgraphs**. This keeps the diagram scannable at a glance.

#### Flowchart (`graph TD` / `graph LR`)

**Direction**: Use `graph TD` (top-down) for hierarchical flows, `graph LR` (left-right) for sequential pipelines.

**Node types** (styled by category):
| Type | Style | Use for |
|------|-------|---------|
| `component` | Purple-500 | Vue components, pages |
| `composable` | Purple-600 | Composables, hooks |
| `utility` | Purple-700 | Utils, helpers, pure functions |
| `external` | Gray-600 | Libraries, browser APIs, external services |
| `event` | Purple-200 | Events, user actions, triggers |
| `data` | Purple-600 | Stores, state, data structures |

**Subgraphs**: Group related nodes into 2-4 subgraphs with approachable mental-model labels (e.g., "User Input", "Core Logic", "Visual Output") — not technical layer names.

**Node IDs**: Use descriptive camelCase IDs that map to the detail data (e.g., `drawingInteraction`, `canvasRenderer`).

**Node labels in Mermaid**: Use plain-English labels — "Drawing Interaction", "Canvas Rendering" — not function names or file names.

**Edges**: Label with plain verbs — "triggers", "feeds into", "reads", "produces", "watches". Not API method names.

#### ER Diagram (`erDiagram`)

Use for database-related walkthroughs: schema design, table relationships, migrations, data models.

**Syntax**:
```
erDiagram
    USERS {
        string id PK
        string email UK
        string name
        timestamp created_at
    }
    TEAMS {
        string id PK
        string name
        string owner_id FK
    }
    TEAM_MEMBERS {
        string team_id FK
        string user_id FK
        string role
    }
    USERS ||--o{ TEAM_MEMBERS : "joins"
    TEAMS ||--o{ TEAM_MEMBERS : "has"
    USERS ||--o{ TEAMS : "owns"
```

**Relationship cardinality**:
| Syntax | Meaning |
|--------|---------|
| `\|\|--o{` | One to many |
| `\|\|--\|\|` | One to one |
| `}o--o{` | Many to many |
| `\|\|--o\|` | One to zero-or-one |

**Column markers**: `PK` (primary key), `FK` (foreign key), `UK` (unique).

**Click handlers on ER diagrams**: Entities in ER diagrams don't natively support Mermaid `click` callbacks. Instead, add click listeners manually after render via `querySelectorAll('.entityLabel')` — see html-patterns.md for the pattern.

### Step 4: Generate the HTML file

Create a single self-contained HTML file following the patterns in [references/html-patterns.md](references/html-patterns.md).

**File location**: Write to the project root as `walkthrough-{topic}.html` (e.g., `walkthrough-canvas-drawing.html`). Use kebab-case for the topic slug.

**Architecture**: The HTML uses `<script type="module">` (native ES modules) — **not** Babel. This means:
- Template literals (backticks) work fine — use them freely for multi-line strings
- Shiki is imported via ESM and highlights code at startup
- React/ReactDOM are loaded as UMD globals, accessed as `window.React` / `window.ReactDOM`
- No JSX — use `React.createElement()` for all component rendering

**Required elements**:
1. Title and subtitle describing the walkthrough scope
2. **TL;DR summary** — 2-3 sentences rendered above the diagram as a visible card. A new dev reads this first, then explores.
3. Mermaid flowchart with clickable nodes (5-12 nodes)
4. Node detail panel showing: 1-2 sentence description, file path(s), optional code snippet
5. Legend showing node type color coding

**Node detail data** — for each node, include:
```js
nodeId: {
  title: "Drawing Interaction",
  description: "Converts pointer events into shape data. This is the bridge between raw mouse input and the element model.",
  files: ["app/features/tools/useDrawingInteraction.ts"],
  // Optional — only include if it's the single most illuminating snippet
  code: `const element = createElement(tool, startPoint, currentPoint)`,
  lang: "typescript",
}
```

Key points:
- `description` = 1-2 plain-text sentences. Answer "what is this?" and "why does it exist?" Not "how does it work internally?"
- `code` = **optional**. Only include if it's the single most illuminating snippet. Max 5 lines. Most nodes should have no code.
- `lang` = Shiki language identifier. Only needed if `code` is present.
- `files` = array of `"path"` or `"path:lines"` strings.

**After writing the file**, open it in the user's browser:
```bash
open walkthrough-{topic}.html    # macOS
```

## Mermaid Conventions

### Click binding
Use Mermaid's callback syntax to make nodes interactive:
```
click nodeId nodeClickHandler "View details"
```

Where `nodeClickHandler` is a global JS function defined in the HTML.

### Subgraph naming
Use approachable mental-model labels:
```
subgraph user_input["User Input"]
subgraph core_logic["Core Logic"]
subgraph visual_output["Visual Output"]
```

### Edge labels
Use plain verbs:
```
A -->|"triggers"| B
A -.->|"watches"| C
A ==>|"produces"| D
```

Use `-->` for direct calls, `-.->` for reactive/watch relationships, `==>` for events/emissions.

## Quality Checklist

Before finishing, verify:
- [ ] Diagram has **5-12 nodes** (not more)
- [ ] Every node label is plain English (no function signatures or file names)
- [ ] No node description exceeds 2 sentences
- [ ] Code snippets are absent or ≤5 lines (most nodes have no code)
- [ ] TL;DR summary is present and ≤3 sentences
- [ ] Every node maps to a real file in the codebase
- [ ] Code snippets (where present) are actual code, not fabricated
- [ ] File paths are correct and relative to project root
- [ ] The flowchart accurately represents the real code flow
- [ ] Clicking any node shows its detail panel
- [ ] The diagram renders without Mermaid syntax errors
- [ ] The HTML file opens correctly in a browser
- [ ] Subgraph labels are approachable ("User Input") not technical ("Composable Layer")
- [ ] Edge labels are plain verbs ("triggers") not method names ("handlePointerDown()")

## References

- [references/html-patterns.md](references/html-patterns.md) — Complete HTML template, CSS, and JavaScript patterns
