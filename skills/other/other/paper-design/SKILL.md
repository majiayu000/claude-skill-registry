---
name: paper-design
description: >
  This skill should be used when designing UI in Paper Design (app.paper.design),
  reading or writing Paper documents via MCP, converting Paper designs to React/Tailwind
  code, importing HTML/CSS into Paper, syncing design tokens, or choosing between Paper
  and Pencil for a design task. Triggers on Paper, paper.design, DOM-based design,
  design-to-code, HTML-to-design, Paper MCP, Paper artboard, prototype,
  mockup, layout, export design, convert design. Pairs with minoan-frontend-design
  for creative direction and shadcn for component library.
argument-hint: "[artboard name, action, or 'health-check']"
---

Read and write designs in Paper via MCP. Paper is a DOM-based design tool — designs are HTML/CSS structures that Claude reads and writes natively.

## Prerequisites

Paper Desktop must be running before starting Claude Code. The app auto-starts an MCP server at `http://127.0.0.1:29979/mcp`. Run `python3 ~/.claude/skills/paper-design/scripts/health-check.py` to verify connection. If the MCP server is not registered, run `bash ~/.claude/skills/paper-design/scripts/setup.sh`.

## Paper vs Pencil

Use Paper for design-to-code, code-to-design, and rapid prototyping (native DOM). Use Pencil for reusable design systems, existing `.pen` files, and presentations. Full comparison: `references/paper-vs-pencil.md`

## Workflow

Every Paper interaction follows four phases: Orient, Create, Verify, Export.

### 1. Orient

Read document state before making changes. Call `get_basic_info` for file name, page name, artboard list. Call `get_tree_summary` with an optional depth limit for structure overview. Call `get_selection` when the user says "this element" or "the selected thing."

### 2. Create

Two paths depending on direction:

**Design from scratch:**
1. `find_placement` — find empty canvas space for new artboard
2. `create_artboard` — common sizes: Desktop (1440x900), Tablet (768x1024), Mobile (375x812)
3. `start_working_on_nodes` — lock the artboard (shows progress indicator to user)
4. `write_html` — write semantic HTML with inline styles or Tailwind classes
5. `finish_working_on_nodes` — release the lock

**Modify existing design:**
1. `get_node_info` or `get_children` — understand the target node's structure
2. `start_working_on_nodes` — lock before modifying
3. `write_html` (replace content), `update_styles` (targeted CSS changes), or `set_text_content` (text-only)
4. `finish_working_on_nodes` — release the lock

`write_html` replaces the entire content of the target node. To update part of a design, target a specific child node, not the artboard root.

### 3. Verify

Call `get_screenshot` after every write operation to verify visual results. DOM correctness does not guarantee visual correctness. Scale options: 1x (default) or 2x for detail inspection.

### 4. Export

**Design to code:** `get_jsx` exports a node as React + Tailwind JSX. Post-process if the project uses plain CSS. Combine with `get_computed_styles` to extract design tokens (colors, spacing, typography). Check `get_font_family_info` to verify font availability before shipping.

**Responsive variants:** `duplicate_nodes` to clone a desktop artboard, then resize and adjust layout for tablet/mobile breakpoints.

## Working Indicators

`start_working_on_nodes` and `finish_working_on_nodes` are locks, not advisories. Starting prevents the user from editing those nodes simultaneously. **Forgetting to call `finish_working_on_nodes` locks the user out.** Always pair them. Call `finish` even if an error occurs mid-workflow.

## Integration

When `minoan-frontend-design` is active, use it for creative direction (aesthetic, typography, color, spatial composition), then translate that direction into Paper artboards via `write_html`. The design lives in Paper; the code lives in the project. `get_jsx` bridges them.

When `shadcn` is active, extract Paper design tokens via `get_computed_styles` and map them to shadcn's OKLCH CSS variables. Or reverse: read the project's shadcn theme, apply as Paper styles via `update_styles`.

## References

Consult `references/` on demand:
- `tool-reference.md` — All 21 MCP tools with usage patterns and gotchas. Read for any Paper MCP operation.
- `workflow-patterns.md` — 7 detailed workflow recipes. Read when starting a multi-step design task.
- `paper-vs-pencil.md` — Decision matrix across 10 dimensions. Read when choosing between design tools.
