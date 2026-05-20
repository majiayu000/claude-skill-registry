---
name: plantuml
description: "Create, edit, and render PlantUML diagrams. Triggers on: architecture diagrams, flowcharts, sequence diagrams, data models, state machines, visual documentation."
argument-hint: "[create|edit|render] [description or file path]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent
---

Infer the operation mode from `$ARGUMENTS`:

| Pattern | Mode | Example |
|---------|------|---------|
| `create ...` | Create new diagram | `create sequence diagram for contract ingestion` |
| `edit <path> ...` | Modify existing diagram | `edit docs/diagrams/data-model-0.puml add user table` |
| `render <path>` | Re-render `.puml` to image | `render docs/diagrams/api-structure-0.puml` |
| `render all` | Re-render all `.puml` files | `render all` |
| _(anything else)_ | Create (default) | `contract lifecycle state machine` |

---

## Step 0: Setup

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
mkdir -p "$REPO_ROOT/docs/diagrams"
```

Check if `docs/diagrams/theme.puml` exists. If not, copy the theme from `assets/theme.puml` in this skill's directory to `$REPO_ROOT/docs/diagrams/theme.puml`. **Never duplicate skinparams inline** — always use the shared theme.

---

## Mode: CREATE

### 1. Understand the Request

Parse `$ARGUMENTS` for diagram type, subject, and scope. If the request is vague, read relevant source code first — use Glob/Grep to find modules, then Read key files.

### 2. Choose Diagram Type

Read `references/diagram-types.md` for the full type guide and per-type conventions. Quick decision:

| Use Case | Type |
|----------|------|
| Multi-service message flow | Sequence |
| Model fields, table structure | Class/Entity |
| Pipeline, branching logic | Activity |
| Status lifecycle, transitions | State |
| System boundaries, layers | Component |

### 3. Design Before Coding

Before writing any PlantUML, plan:

1. **What is the architectural story?** Not "added a service" but "introduced a bidirectional sync with normalized constraints"
2. **What would confuse a new team member?** That's what the diagram should clarify
3. **Key design decisions** — constraints, validation gates, data transformations
4. **List exact elements** with real names from the code (target 6-12, hard max 15 — split if more)
5. **List exact arrows** with labels describing data/actions
6. **Identify groupings** by architectural boundary

### 4. Determine Filename

```bash
ls docs/diagrams/*.puml 2>/dev/null | sort -V
```

Convention: `{topic}-{n}.puml` where `{n}` increments from 0. Image: `{topic}-{n}.png` or `.svg`.

### 5. Write the `.puml` File

Every diagram follows this skeleton:

```plantuml
@startuml
' Title: [Concept — Pattern/Insight]
' Created: [YYYY-MM-DD]
!include theme.puml

title Concept Name — Key Insight

' --- Elements ---
' [diagram body — see references/diagram-types.md for per-type conventions]

' --- Legend (only when 2+ color-coded groups are used) ---
legend right
  | Color | Layer |
  |<#DBEAFE> | API / Input |
  |<#EDE9FE> | Service / Logic |
  |<#D1FAE5> | Storage / Data |
end legend

center footer Generated on YYYY-MM-DD

@enduml
```

**Rules:**
- Always `!include theme.puml` — never inline skinparams
- Title = **concept + insight**, not just feature name
- Legend only when 2+ color groups; only list layers actually present
- Name every arrow with the actual method/field/action
- Max 2-3 notes per diagram, explaining non-obvious *why*
- See `references/color-palette.md` for the full layer→color mapping

### 6. Render

Use the render script from this skill's `scripts/` directory:

```bash
bash scripts/render.sh docs/diagrams/{topic}-{n}.puml        # PNG (default)
bash scripts/render.sh docs/diagrams/{topic}-{n}.puml --svg   # SVG (better for docs/GitHub)
bash scripts/render.sh --all                                   # All diagrams
```

The script validates that `plantuml` is installed, checks files exist, and reports errors per file.

### 7. Self-Review

Read the rendered image and verify:
1. All labels readable — no truncated text, no overlapping
2. Arrows have meaningful labels
3. Color coding consistent — same layer = same color
4. Legend matches diagram
5. Footer present with date
6. Notes explain non-obvious decisions
7. **The diagram teaches something** — a new team member learns from it

If any check fails, edit and re-render. Up to 3 attempts.

### 8. Report

Tell the user: source path (`.puml`), image path (`.png`/`.svg`), what it shows and why this type was chosen, and the re-render command for future manual edits.

> **Quick mode:** If the user explicitly asks for a quick sketch or informal diagram, skip the legend, footer, and self-review steps. Still use the theme.

---

## Mode: EDIT

1. Read the existing `.puml` file and understand its structure
2. Plan changes — preserve existing style and conventions
3. Apply edits, preserving: `!include theme.puml`, title (update if scope changed), footer (update date), legend (update if layers changed)
4. Render and self-review (Steps 6-8 from CREATE)

---

## Mode: RENDER

```bash
bash scripts/render.sh docs/diagrams/{file}.puml         # Single file
bash scripts/render.sh docs/diagrams/{file}.puml --svg    # Single file, SVG
bash scripts/render.sh --all                               # All diagrams
```

Report which files were rendered and any errors.

---

## Gotchas

| Mistake | Why it's bad | Do this instead |
|---------|-------------|-----------------|
| Generic "API → Service → DB" boxes | Anyone can read the file tree | Specific class names, method calls, field names |
| Unlabeled arrows | Meaningless connections | Every arrow labeled with data/action |
| 20+ elements crammed together | Unreadable | Split into focused diagrams, 6-12 elements each |
| Inline skinparams | Style drift across diagrams | `!include theme.puml` |
| Title = feature name ("QA Module") | Doesn't teach anything | Title = concept + insight ("QA Session — RAG Pipeline Flow") |
| Notes saying "this is the database" | Restating the obvious | Notes explaining constraints and *why* decisions were made |
| Dumping entire table schemas | Noise | Only fields relevant to the story |
