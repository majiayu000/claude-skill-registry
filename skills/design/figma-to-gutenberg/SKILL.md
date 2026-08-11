---
name: figma-to-gutenberg
description: "Use when the user says 'figma to gutenberg', 'figma to blocks', or hands over a Figma frame to rebuild on a WordPress site that uses the block editor. Maps the Figma node tree to core Gutenberg blocks, registers the frame's palette in Global Styles, and writes to a draft, so nothing live is touched."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Figma to Gutenberg

Rebuilds a Figma frame as a real, editable block-editor page — no page builder required. Reads the Figma node tree (layers, auto-layout, text, colors, images), maps each node to core Gutenberg blocks, registers the frame's palette in the site's Global Styles so the design system carries over, and writes to a draft so nothing live is touched. Works on any WordPress 6.6+ site, including block themes.

## What This Skill Does

**Handles:**
- Frames and auto-layout → `core/group` with flex/stack layout (preferred over `core/columns` for row layouts — groups survive later editing and re-reading more faithfully)
- Text nodes → `core/heading` (level inferred from font size) or `core/paragraph`
- Rectangles/ellipses with image fills → `core/image`; lines → `core/separator`; buttons → `core/buttons` + `core/button`
- Repeated patterns by layer name + structure: FAQ stacks → `core/details`, image rows → `core/gallery`, quote-shaped blocks → `core/quote`
- Typography (size, weight, line-height, letter-spacing, alignment) via block supports; families noted for the theme
- Colors: solid fills and gradients on blocks; **the frame's distinct palette registered as named design tokens in Global Styles** (`respira_create_design_token`) so the page references tokens the whole site can reuse
- Spacing from Figma padding/item spacing via block gap and padding supports; per-corner radius and shadows where block supports allow
- Image fills downloaded from Figma and sideloaded into the media library

**Preserves:** text content, links and media; layout structure and nesting; the page stays fully hand-editable in the block editor and Site Editor afterwards.

## What This Skill Does NOT Do

- **Pixel-perfect recreation** — the block editor's styling surface is intentionally narrower than Figma's canvas; complex decorative treatments land as flagged custom-CSS notes or flattened images
- **Figma components with overrides / variants** — flattened to visible content and flagged
- **Prototyping and interactions** — skipped
- **Complex vector art, masks, blend modes** — flattened to images where possible, otherwise flagged
- **Auto-generated responsive breakpoints** — core blocks are intrinsically responsive, but design-specific mobile layouts need a manual pass
- **Theme templates** — headers/footers/archive templates are out of scope; this builds page content

## Requirements

- Respira for WordPress plugin installed and connected; WordPress 6.6+ with the block editor
- MCP connection active
- **Figma read access from your agent** — a connected Figma MCP, or a Figma file/frame URL plus a personal access token
- Write access to create a draft with the new block content

## Trigger Phrase

- "figma to gutenberg"

## Alternative Triggers

- "figma to blocks"
- "build this figma design with core blocks"
- "convert figma to the block editor"

## Source: Figma

Same read model as every figma-to-* skill: read the selected frame's node tree via the agent's Figma access (Figma MCP, or REST `GET /v1/files/:key/nodes?ids=:id` plus `GET /v1/files/:key/images` for image fills). Key properties: node `type`, `layoutMode`/`itemSpacing`/`padding*`/axis alignment, text `style`, `fills`/`strokes`/`cornerRadius`/`effects`/`opacity`, `characters`, IMAGE fills.

## Target: Gutenberg

Call `respira_get_builder_info` first — it lists the registered blocks (theme and plugin blocks included). Author with core blocks by default so the page works on any theme:

**Mapping (Figma → blocks):** `TEXT` → `core/heading` (≥48px h1, ≥36 h2, ≥28 h3, ≥20 h4) or `core/paragraph`; frame with HORIZONTAL layout → `core/group` (flex row) — reach for `core/columns` only when true column semantics are wanted; VERTICAL → `core/group` (stack); IMAGE fill → `core/image`; `LINE` → `core/separator`; CTA pairs → `core/buttons`; FAQ → `core/details`; wide/full sections → group with `align: full` and a background.

Palette: register the frame's colors as design tokens with `respira_create_design_token` (they land in the site's Global Styles), then reference the token slugs in block attributes rather than inlining hex values.

## Execution Workflow

**Phase 1 — Read and audit:** verify the site via `respira_get_site_context` + `respira_get_builder_info`; read the frame; inventory nodes, block candidates, images, flags.

**Phase 2 — Build plan:** frame → page title, mapping table, the palette to register, flagged items. Explicit confirmation before any write.

**Phase 3 — Build:** register tokens; sideload images; write the block tree as a draft with `respira_build_page`; read the page back to confirm the block structure survived (`respira_read_page`).

**Phase 4 — Verify with your eyes:** render the draft and compare against the Figma frame (screenshot pass — write success is not visual proof). Refine with `respira_find_element` + `respira_update_element`. Report what carried over, the tokens registered, and what is flagged for a human.

## Safety Model

Read-only Figma analysis and a full plan before any write; explicit confirmation before building; always writes to a draft; never auto-publishes; snapshots on every write with rollback; the Figma file is never modified.

## Honest Disclaimer

It cannot guarantee pixel-perfect parity, reproduce component variants or prototyping, or replace a manual mobile pass. It can turn a clean Figma frame into a structured page of plain core blocks in minutes — a page any WordPress user can keep editing with nothing installed beyond Respira.

## Tooling

`respira_get_site_context`, `respira_get_builder_info`, `respira_create_design_token`, `respira_list_design_tokens`, `respira_build_page`, `respira_sideload_image`, `respira_read_page`, `respira_find_element`, `respira_update_element`, `respira_convert_html_to_builder` (fallback bridge)

## Telemetry

After run completion, fire-and-forget `POST https://www.respira.press/api/skills/track-usage` with `skill_slug = figma-to-gutenberg`, site/version context, duration and success.
