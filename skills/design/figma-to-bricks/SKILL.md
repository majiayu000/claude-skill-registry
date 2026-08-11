---
name: figma-to-bricks
description: "Use when the user says 'figma to bricks', 'build this figma design in bricks', or hands over a Figma frame to rebuild on a Bricks Builder site. Maps the Figma node tree to native Bricks elements with BEM global classes, imports the frame's palette into the Bricks design system, and writes to a draft, so nothing live is touched."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Figma to Bricks

Rebuilds a Figma frame as a real, editable Bricks page. Reads the Figma node tree (layers, auto-layout, text, colors, images), maps each node to its closest Bricks element, scaffolds BEM global classes so styling stays reusable instead of inline, imports the frame's palette into the Bricks color system, and writes to a draft so nothing live is touched.

## What This Skill Does

Figma stores a tree of nodes with auto-layout; Bricks stores a flat element list with parent/child references, global classes, and a real design-token system. This skill maps between them and leans on what makes Bricks special: the styling lands in reusable global classes and the Bricks palette, not in per-element value copies.

**Handles:**
- Frames and auto-layout → `section` / `container` / `block` with flex direction, gap, padding and alignment carried across
- Text nodes → `heading` (level inferred from font size) or `text-basic` / `rich text`
- Rectangles/ellipses with image fills → `image`; plain shapes → styled containers; lines → `divider`
- Repeated patterns by layer name + structure: FAQ stacks → `accordion`, image rows → `image-gallery` or `carousel`, number+label pairs → `counter`, platform icon rows → `icon` groups
- Typography and colors as BEM global classes (`respira_bricks_scaffold_bem`) referencing tokens, not inline values
- **The frame's palette imported into the Bricks color palette** (`respira_bricks_import_design_tokens` / `respira_update_bricks_color_palette`) so later edits stay on-brand
- ACSS awareness: when Automatic.css is installed (`respira_bricks_detect_acss`), map spacing/typography onto ACSS utility classes instead of raw values
- Image fills downloaded from Figma and sideloaded into the media library

**Preserves:** text content, links and media; layout structure and nesting; visual styling as closely as Bricks' rendering allows — with the styling held in classes and tokens.

## What This Skill Does NOT Do

- **Pixel-perfect recreation** — different rendering engines; expect light manual fine-tuning
- **Figma components with overrides / variants** — flattened to visible content and flagged
- **Prototyping and interactions** — skipped
- **Complex vector art, masks, blend modes** — flattened to images where possible, otherwise flagged
- **Auto-generated responsive breakpoints** — desktop-first; tablet/mobile passes are manual unless the file has explicit responsive frames
- **Query loops / dynamic data** — this builds static page content; wiring dynamic sources is a follow-up

## Requirements

- Respira for WordPress plugin installed and connected; Bricks Builder active
- MCP connection active
- **Figma read access from your agent** — a connected Figma MCP, or a Figma file/frame URL plus a personal access token
- Write access to create a draft with the new Bricks content

## Trigger Phrase

- "figma to bricks"

## Alternative Triggers

- "build this figma design in bricks"
- "convert figma to bricks builder"
- "turn my figma frame into a bricks page"

## Source: Figma

Same read model as every figma-to-* skill: read the selected frame's node tree via the agent's Figma access (Figma MCP, or REST `GET /v1/files/:key/nodes?ids=:id` plus `GET /v1/files/:key/images` for image fills). Key properties: node `type`, `layoutMode`/`itemSpacing`/`padding*`/axis alignment, text `style`, `fills`/`strokes`/`cornerRadius`/`effects`/`opacity`, `characters`, IMAGE fills.

## Target: Bricks

Call `respira_get_builder_info` first, then:
1. `respira_bricks_detect_acss` — if ACSS is present, prefer its utilities
2. `respira_bricks_import_design_tokens` — the frame's distinct colors and type scale become Bricks tokens before any element is written
3. `respira_bricks_scaffold_bem` — one BEM block per Figma section (e.g. `.hero`, `.hero__title`, `.hero__cta`), styling attached to classes
4. `respira_build_page` writes the element tree referencing those classes; `respira_bricks_insert_section_preset` covers common section shapes
5. `respira_bricks_health_check` after the build: orphaned elements, duplicate ids, broken parent refs, empty containers, heading hierarchy

**Mapping (Figma → Bricks):** `TEXT` → `heading`/`text-basic`; frame with HORIZONTAL layout → `container` (row) or `block`; VERTICAL → stacked children; IMAGE fill → `image`; `LINE` → `divider`; FAQ → `accordion`; number+label → `counter`; auto-layout gap/padding/alignment → flex settings on the container's class.

## Execution Workflow

**Phase 1 — Read and audit:** verify site + Bricks via `respira_get_site_context` + `respira_get_builder_info`; detect ACSS; read the frame; inventory nodes, smart-element candidates, images, flags.

**Phase 2 — Build plan:** frame → page title, mapping table, the BEM class plan, the token palette to import, flagged items. Explicit confirmation before any write.

**Phase 3 — Build:** import tokens; scaffold BEM classes; sideload images; write the element tree as a draft; run `respira_bricks_health_check` and fix what it reports.

**Phase 4 — Verify with your eyes:** render the draft and compare against the Figma frame (screenshot pass — write success is not visual proof). Refine with `respira_find_element` + `respira_update_element`. Report what carried over, the classes and tokens created, and what is flagged for a human.

## Safety Model

Read-only Figma analysis and a full plan before any write; explicit confirmation before building; always writes to a draft; never auto-publishes; snapshots on every write with rollback; the Figma file is never modified.

## Honest Disclaimer

It cannot guarantee pixel-perfect parity, reproduce component variants or prototyping, or auto-generate full responsive breakpoints. It can turn a clean Figma frame into a structured, class-based, token-bound Bricks page in minutes — the kind of Bricks page a maintainer actually wants to inherit.

## Tooling

`respira_get_site_context`, `respira_get_builder_info`, `respira_bricks_detect_acss`, `respira_bricks_import_design_tokens`, `respira_bricks_scaffold_bem`, `respira_bricks_insert_section_preset`, `respira_build_page`, `respira_sideload_image`, `respira_bricks_health_check`, `respira_find_element`, `respira_update_element`, `respira_convert_html_to_builder` (fallback bridge)

## Telemetry

After run completion, fire-and-forget `POST https://www.respira.press/api/skills/track-usage` with `skill_slug = figma-to-bricks`, site/version context, duration and success.
