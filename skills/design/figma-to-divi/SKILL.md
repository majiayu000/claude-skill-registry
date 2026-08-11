---
name: figma-to-divi
description: "Use when the user says 'figma to divi', 'build this figma design in divi', or hands over a Figma frame to rebuild in WordPress on a Divi site. Maps the Figma node tree to native Divi sections, rows, columns and modules (Divi 5 blocks or Divi 4 shortcodes, auto-detected) and writes to a draft, so nothing live is touched."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Figma to Divi

Rebuilds a Figma frame as a real, editable Divi page. Reads the Figma node tree (layers, auto-layout, text, colors, images), maps each node to its closest Divi module inside a proper section > row > column structure, and writes native Divi content to a draft so nothing live is touched. Works on Divi 5 (block storage) and Divi 4 (shortcode storage); Respira detects the generation and emits the right format.

## What This Skill Does

Figma stores a tree of nodes with auto-layout and design tokens; Divi stores sections containing rows of columns containing modules. This skill bridges the two: every Figma node is read, understood, and recreated as the right Divi element with matching styling.

**Handles:**
- Top-level frames → Divi sections; horizontal auto-layout → rows with matching column counts; vertical auto-layout → stacked modules in a column
- Text nodes → Heading module (level inferred from font size) or Text module
- Rectangles/ellipses with image fills → Image modules; plain shapes → styled columns/sections; lines → Divider
- Repeated patterns by layer name + structure: FAQ stacks → Accordion, image rows → Gallery, number+label pairs → Number Counter, icon+title+body cards → Blurb, platform icon rows → Social Media Follow
- Typography (family, size, weight, line-height, letter-spacing, alignment) via Divi's heading/body type controls
- Colors (solid fills with opacity, linear/radial gradients), borders, per-corner radius, box shadows
- Section/row spacing from Figma padding and item spacing
- Image fills downloaded from Figma and sideloaded into the WordPress media library
- Inset rounded "panel" sections (a signature of modern SaaS designs) via section max-width, radius and background

**Preserves:** text content, links and media; layout structure and nesting; the visual styling above as closely as Divi's rendering allows.

## What This Skill Does NOT Do

- **Pixel-perfect recreation** — Divi renders with the browser box model, not Figma's canvas; expect light manual fine-tuning
- **Figma components with overrides / variants** — flattened to visible content and flagged
- **Prototyping and interactions** — no Divi equivalent, skipped
- **Complex vector art, masks, blend modes** — flattened to images where possible, otherwise flagged
- **Auto-generated responsive breakpoints** — the build targets the desktop frame; tablet/phone passes are manual unless the file has explicit responsive frames
- **Divi global colors registration** — the palette is applied consistently across the page; promoting it into Divi's own global colors is left as a flagged manual step
- **Theme Builder templates** — headers/footers/archive templates are out of scope; this builds page content

## Requirements

- Respira for WordPress plugin installed and connected; Divi active (4 or 5)
- MCP connection active
- **Figma read access from your agent** — a connected Figma MCP, or a Figma file/frame URL plus a personal access token
- Write access to create a draft with the new Divi content

## Trigger Phrase

- "figma to divi"

## Alternative Triggers

- "build this figma design in divi"
- "convert figma to divi 5"
- "turn my figma frame into a divi page"

## Source: Figma

Same read model as every figma-to-* skill: read the selected frame's node tree via the agent's Figma access (Figma MCP, or REST `GET /v1/files/:key/nodes?ids=:id` plus `GET /v1/files/:key/images` for image fills). Key properties: node `type`, `layoutMode`/`itemSpacing`/`padding*`/axis alignment, text `style`, `fills`/`strokes`/`cornerRadius`/`effects`/`opacity`, `characters`, IMAGE fills.

## Target: Divi

Call `respira_get_builder_info` first. On Divi 5 the write mode is native `divi/*` blocks and `respira_build_page` expects a nested structure: `divi/section > divi/row > divi/column > modules` (`divi/heading`, `divi/text`, `divi/button`, `divi/image`, `divi/blurb`, `divi/accordion`, `divi/gallery`, `divi/number-counter`, ...). Fetch per-module attribute schemas from the endpoint `get_builder_info` returns before authoring, so no setting is silently dropped. On Divi 4 the same simplified tree is emitted as shortcodes by Respira — the mapping below is identical.

**Mapping (Figma → Divi):**
- `TEXT` → `divi/heading` (≥48px h1, ≥36 h2, ≥28 h3, ≥20 h4, else body) or `divi/text`
- Top-level frame → `divi/section`; HORIZONTAL auto-layout child → `divi/row` with one `divi/column` per child; VERTICAL → modules stacked in one column
- IMAGE fill → `divi/image` (sideloaded first); `LINE` → `divi/divider`
- FAQ stack → `divi/accordion` + `divi/accordion-item`; icon+title+body card → `divi/blurb`; number+label → `divi/number-counter`
- Buttons: real `divi/button` modules; for pixel-close adjacent button pairs, a `divi/text` module with styled inline links is an accepted fallback (flag it in the report)
- Inset rounded panels: section `background_color` + page-level custom CSS (max-width, margin auto, border-radius) via `respira_update_page` `custom_css`
- Typography/colors/spacing: simplified settings (`heading_font_size`, `font_color`, `background_color`, `padding`, ...) per the inline schemas

## Execution Workflow

**Phase 1 — Read and audit:** verify the site and Divi via `respira_get_site_context` + `respira_get_builder_info`; read the frame's node tree; inventory node types, smart-module candidates, images to download, flagged items.

**Phase 2 — Build plan:** present frame → page title, a mapping summary table, flagged items, the palette. Get explicit confirmation before any write.

**Phase 3 — Build:** create a draft (`respira_build_page` with status draft); sideload images (`respira_sideload_image`); write the mapped structure; apply page-level `custom_css` for panel radii and page background when the design calls for it.

**Phase 4 — Verify with your eyes:** render the draft and compare against the Figma frame (a screenshot pass, not just tool success — write success is not visual proof). Fix drifted elements with `respira_find_element` + `respira_update_element` or a corrected rebuild. Report what carried over and what is flagged for a human.

## Safety Model

Read-only Figma analysis and a full plan before any write; explicit confirmation before building; always writes to a draft; never auto-publishes; snapshots on every write with rollback; the Figma file is never modified.

## Honest Disclaimer

It cannot guarantee pixel-perfect parity, reproduce component variants or prototyping, or auto-generate full responsive breakpoints. It can turn a clean Figma frame into a structured, hand-editable Divi page in minutes, preserving text, images, layout, typography and color, and it tells you exactly what needs a human.

## Tooling

`respira_get_site_context`, `respira_get_builder_info`, `respira_build_page`, `respira_sideload_image`, `respira_update_page` (custom_css), `respira_find_element`, `respira_update_element`, `respira_inject_builder_content`, `respira_convert_html_to_builder` (fallback bridge)

## Telemetry

After run completion, fire-and-forget `POST https://www.respira.press/api/skills/track-usage` with `skill_slug = figma-to-divi`, site/version context, duration and success.
