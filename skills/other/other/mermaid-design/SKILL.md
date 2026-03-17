---
name: mermaid-design
description: Generate and standardize Mermaid diagrams with deterministic token-based theming from the repository root `mermaid.tokens.json`.
---

# Mermaid Design

Use one token source (`mermaid.tokens.json` at repo root) for all Mermaid outputs.

## Supported diagrams

- `graph`
- `flowchart`
- `sequenceDiagram`
- `classDiagram`
- `stateDiagram`
- `stateDiagram-v2`
- `erDiagram`
- `journey`
- `gantt`
- `pie`
- `mindmap`
- `timeline`
- `gitGraph`
- `quadrantChart`
- `requirementDiagram`
- `kanban`

## Mandatory preflight

1. Resolve repository root.
2. Ensure root `mermaid.tokens.json` exists.
3. If missing, create it using the default token JSON from this file.
4. Load `theme` and `themeVariables` before producing Mermaid output.

## Root token contract

- Path is always root `mermaid.tokens.json`.
- Root file is the source of truth for theme values.
- Every diagram output must include a Mermaid init block using root values.
- If user requests style changes, update root `mermaid.tokens.json` first, then generate diagrams.

## Default root tokens (create when missing)

```json
{
  "theme": "base",
  "themeVariables": {
    "darkMode": false,
    "background": "#f4f4f4",
    "fontFamily": "trebuchet ms, verdana, arial",
    "fontSize": "16px",
    "primaryColor": "#fff4dd",
    "primaryTextColor": "#2f2f2f",
    "primaryBorderColor": "#e7bf67",
    "secondaryColor": "#dff4ff",
    "secondaryTextColor": "#17324d",
    "secondaryBorderColor": "#83c9ee",
    "tertiaryColor": "#e6ffe0",
    "tertiaryTextColor": "#1e4026",
    "tertiaryBorderColor": "#93cc86",
    "lineColor": "#6f7f8a",
    "textColor": "#263746",
    "noteBkgColor": "#fff5ad",
    "noteTextColor": "#333333",
    "noteBorderColor": "#d7c25b",
    "actorBkg": "#fff4dd",
    "actorBorder": "#e7bf67",
    "actorTextColor": "#2f2f2f",
    "signalColor": "#31424f",
    "signalTextColor": "#31424f",
    "activationBkgColor": "#dff4ff",
    "activationBorderColor": "#83c9ee",
    "pie1": "#fff4dd",
    "pie2": "#dff4ff",
    "pie3": "#e6ffe0",
    "pie4": "#ffd9c2",
    "pie5": "#d9e7ff",
    "pie6": "#f9e1ff",
    "pieStrokeColor": "#2f2f2f",
    "pieStrokeWidth": "2px"
  }
}
```

## Workflow

1. Run preflight.
2. Read root token file.
3. Emit one init block in this shape:
   - `%%{init: {"theme":"<theme>","themeVariables":{...}}}%%`
4. Generate requested supported diagram.
5. Avoid one-off inline style overrides unless explicitly requested.

## Failure handling

- If root token file is unreadable or invalid JSON, replace with default tokens and continue.
- If the requested diagram type is unsupported, list supported types and stop.
