---
name: figma-design
version: 1.0.0
description: '[Frontend] Extract design context from Figma URLs via MCP, REST API, or screenshot fallback. Produces structured design tokens, component inventory, and layout specs for design-spec consumption. Triggers on figma url, figma design, extract figma, figma to code.'
allowed-tools: Read, Write, Grep, Glob, AskUserQuestion
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting.

## Quick Summary

**Goal:** Extract structured design context from Figma designs for downstream use by `design-spec` and planning skills.

**Workflow:**

1. **Detect Input** — Parse Figma URL, extract file key + node ID
2. **Select Extraction Method** — 4-level fallback chain
3. **Extract Context** — Design tokens, components, layout, typography
4. **Output Artifact** — Structured markdown for design-spec consumption

**Key Rules:**

### Frontend/UI Context (if applicable)

When this task involves frontend or UI changes, **MUST READ** `.claude/skills/shared/ui-system-context.md` and the following docs:

- Component patterns: `docs/project-reference/frontend-patterns-reference.md`
- Styling/BEM guide: `docs/project-reference/scss-styling-guide.md`
- Design system tokens: `docs/project-reference/design-system/README.md`

- Always try highest-fidelity method first, fallback gracefully
- Output must be consumable by `design-spec` and `ui-wireframe-protocol`
- Keep extraction under 5K tokens per design

## Extraction Fallback Chain

### Level 1: Official Figma MCP (Best Fidelity)

Check if MCP tools available: look for `get_design_context` in tool list.

If available:

1. `get_design_context` — structured layout, components, tokens, constraints
2. `get_screenshot` — visual reference image
3. `get_code_connect_map` — map Figma components to code components

### Level 2: GLips Figma-Context-MCP (Good Fidelity)

Check if GLips MCP tools available (look for figma-context tools).

If available:

1. Extract file metadata, frame structure, component list
2. Limited to read-only operations

### Level 3: Figma REST API (Manual)

If `FIGMA_ACCESS_TOKEN` environment variable exists:

1. Call `GET /v1/files/{file_key}/nodes?ids={node_id}` via bash script
2. Parse response for: component names, styles, layout properties
3. Limited — no screenshot, no Code Connect

### Level 4: Screenshot + ai-multimodal (Always Available)

If no MCP and no API token:

1. Ask user via `AskUserQuestion`: "Please screenshot the Figma frame and paste here"
2. Analyze via `ai-multimodal` skill with design extraction prompts
3. Extract: approximate colors, fonts, spacing, layout, components

## Output Format

Save to `team-artifacts/design-specs/{YYMMDD}-figma-extract-{slug}.md`:

```markdown
# Figma Design Extract: {Name}

**Source:** {Figma URL}
**Method:** {MCP Level 1 | MCP Level 2 | REST API | Screenshot}
**Date:** {YYMMDD}

## Design Tokens

| Category   | Token     | Value                |
| ---------- | --------- | -------------------- |
| Color      | Primary   | {hex}                |
| Color      | Secondary | {hex}                |
| Typography | Heading   | {font, size, weight} |
| Spacing    | Base      | {px}                 |

## Component Inventory

- **{ComponentName}** — {description}, variants: {list}

## Layout

{ASCII wireframe per ui-wireframe-protocol}

## Responsive

{Breakpoint behavior if detectable}
```

## When to Use

- Figma URL detected in PBI, design-spec, or user prompt
- Called by `design-spec` when Figma URL is present
- Called by `planning` skill during Design Context Extraction step

## When NOT to Use

- No Figma URL present — skip, proceed to `design-spec` directly
- Hand-drawn wireframe — use `wireframe-to-spec` instead
- Screenshot of existing app — use `design-screenshot` instead

## See Also

- `references/figma-mcp-setup.md` — MCP server setup guide (created in Phase 09)
- `.claude/skills/planning/references/figma-integration.md` — integration protocol
- `.claude/hooks/figma-context-extractor.cjs` — URL detection hook
