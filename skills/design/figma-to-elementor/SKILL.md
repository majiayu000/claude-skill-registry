---
name: figma-to-elementor
description: "Use when the user says 'figma to elementor', 'build this figma design in elementor', or hands over a Figma frame to rebuild in WordPress. Maps the Figma node tree to Elementor widgets and containers and writes clean Elementor JSON into a draft duplicate, so nothing live is touched."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Figma to Elementor

Rebuilds a Figma frame as a real, editable Elementor page on your WordPress site. Reads the Figma node tree (layers, auto-layout, text, colors, images), maps each node to its closest Elementor widget or container, generates a build plan for approval, and writes clean Elementor JSON to a draft duplicate so nothing live is touched. Use this skill whenever someone wants to turn a Figma design into an Elementor page, build a Figma mockup in Elementor, or hand a design off to WordPress without rebuilding it by hand.

## What This Skill Does

Figma and Elementor describe a layout in very different ways. Figma stores a tree of nodes (frames, text, shapes, images) with auto-layout, constraints, and design tokens; Elementor stores a nested JSON tree in `_elementor_data` of sections/columns (or flex containers) and widgets. This skill bridges that gap by reading every Figma node, understanding its role, and recreating it as the right Elementor element with matching styling.

**Handles:**
- Frames and auto-layout → Elementor flex containers (or section/column on older sites): direction, gap, padding, alignment
- Text nodes → Heading (level inferred from font size) or Text Editor widgets
- Rectangles/ellipses with image fills → Image widgets; plain shapes → containers; vectors/icons → Image or Icon
- Lines → Divider widgets
- Repeated card/list patterns → recognised by layer name + structure: FAQ → Accordion, image rows → Gallery/Carousel, number+label → Counter, icon rows → Social Icons
- Typography (font family, size, weight, line-height, letter-spacing, transform, alignment)
- Colors (solid fills with opacity; linear/radial gradients with stops and angle)
- Spacing (padding, gaps), borders, border-radius (per-corner), box shadows, opacity
- Image fills downloaded from Figma and sideloaded into the WordPress media library
- The Figma color palette mapped to Elementor global colors so the design system carries over

**Preserves:**
- Text content, links, and media
- Layout structure and nesting (with junk single-child wrappers collapsed)
- The visual styling listed above, as closely as Elementor's rendering allows

## What This Skill Does NOT Do

- **Pixel-perfect recreation** — Elementor renders with the browser box model, not Figma's canvas. Spacing and alignment land close but expect light manual fine-tuning.
- **Figma components with overrides / variants** — instances are flattened to inline content; component logic and variant swapping are flagged, not reproduced.
- **Prototyping and interactions** — Figma's click-throughs, smart-animate, and overlays have no Elementor equivalent and are skipped.
- **Complex vector art, masks, and blend modes** — exported as flattened images where possible, otherwise flagged.
- **Auto-generated responsive breakpoints** — the build targets desktop from the frame; tablet/mobile are noted for manual adjustment unless the design provides explicit responsive frames.
- **Theme builder parts** — headers, footers, archive/single templates are out of scope; this builds page content.
- **Fetching Figma for you without access** — you must have Figma read access available to your agent (see Requirements).

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Elementor active on the target site (to write the page)
- **Figma read access from your agent** — either a connected Figma MCP, or a Figma file/frame URL plus a Figma personal access token you can paste
- Write access to create a draft duplicate with the new Elementor content

## Trigger Phrase

- "figma to elementor"

## Alternative Triggers

- "build this figma design in elementor"
- "convert figma to elementor"
- "turn my figma frame into an elementor page"
- "rebuild this figma mockup in wordpress with elementor"
- "import figma into elementor"

## Source: Figma

Figma exposes a design as a tree of nodes. Read it with whatever Figma access the agent has: a connected Figma MCP, or the Figma REST API (`GET /v1/files/:key/nodes?ids=:id` for the selected frame, `GET /v1/files/:key/images` to export image fills) using a personal access token.

Key node shapes to read:
- `type`: `FRAME`, `GROUP`, `TEXT`, `RECTANGLE`, `ELLIPSE`, `VECTOR`, `LINE`, `COMPONENT`, `INSTANCE`
- `layoutMode` (`HORIZONTAL`/`VERTICAL`/none), `itemSpacing`, `paddingLeft/Right/Top/Bottom`, `primaryAxisAlignItems`, `counterAxisAlignItems`, `layoutSizingHorizontal/Vertical` (`FILL`/`FIXED`/`HUG`)
- `style` for text: `fontFamily`, `fontSize`, `fontWeight`, `lineHeightPx`/`lineHeightPercent`, `letterSpacing`, `textAlignHorizontal`, `textCase`, `textDecoration`
- `fills` (SOLID with `color` + `opacity`; gradients with `gradientStops` + `gradientHandlePositions`), `strokes` + `strokeWeight`, `cornerRadius`/`rectangleCornerRadii`, `effects` (DROP_SHADOW/INNER_SHADOW), `opacity`
- `characters` (text content), and IMAGE fills (mark for download)

Pick one top-level frame at a time. Each direct child of that frame becomes an independently editable Elementor section/container.

## Target: Elementor

Respira writes Elementor as a simplified tree of `{ type, widget, settings, elements }`, which the plugin normalizes/validates into real `_elementor_data` (v3 sections/columns or v4 atomic flex containers, auto-detected). You never hand-write raw Elementor JSON — you describe the tree and Respira emits the canonical shape.

- Containers: `{ type: "container", settings: {...}, elements: [...] }` (flex) or `section` + `column` on v3 sites
- Widgets: `{ type: "widget", widget: "heading", settings: { title: "..." } }`, `text-editor` (`editor`), `image`, `button`, `icon`, `divider`, `accordion`, `image-gallery`, `image-carousel`, `counter`, `social-icons`
- Write with `respira_build_page` (whole frame → page) or `respira_inject_builder_content` (append sections); `respira_convert_html_to_builder` is a fallback bridge; `respira_find_element`/`respira_update_element` for refinement.

## Mapping (Figma → Elementor)

**Node type:**
- `TEXT` → `heading` if it reads like a heading (large/bold), else `text-editor`. Infer heading level by font size: ≥48 h1, ≥36 h2, ≥28 h3, ≥20 h4, ≥16 h5, else h6.
- `FRAME`/`GROUP`/auto-layout → `container` (flex). Flatten groups with no fills/strokes/effects; keep groups that carry styling.
- `RECTANGLE`/`ELLIPSE` with an IMAGE fill → `image`; otherwise → styled `container`.
- `VECTOR`/shape → `image` (export from Figma) or `icon`; `LINE` → `divider`.
- `INSTANCE`/`COMPONENT` → treated as a container; flag if it relies on overrides/variants.

**Auto-layout → flex container:**
- `layoutMode` HORIZONTAL → row, VERTICAL → column
- `itemSpacing` → gap; `padding*` → padding (per side, linked when equal)
- `primaryAxisAlignItems` → justify-content, `counterAxisAlignItems` → align-items (MIN→flex-start, CENTER→center, MAX→flex-end, SPACE_BETWEEN→space-between)
- child `layoutSizing` FILL → flex-grow, FIXED → fixed size, HUG → shrink-to-fit

**Typography → Elementor typography controls:** family, size (px), weight, line-height (px or %), letter-spacing, text-transform, text-decoration, alignment.

**Color:** solid fill → text/background color (+ opacity when <1). Gradient → gradient type (linear/radial), color stops with positions, and an angle computed from `gradientHandlePositions`.

**Box:** `strokes`+`strokeWeight` → border; `cornerRadius`/`rectangleCornerRadii` → border-radius (per-corner when provided); `effects` → box-shadow (offset/blur/spread/color); `opacity` → element opacity.

**Smart widgets (by layer name + structure):** a list whose items each hold a title + body → Accordion; a row that is ≥70% images → Gallery or Carousel (by layer name); a number + label pair → Counter; a row of 2+ icon shapes whose names match platforms → Social Icons. When unsure, fall back to plain containers + widgets.

**Images:** collect IMAGE fills, export from Figma, sideload with `respira_sideload_image`, and set the resulting media on the Elementor image widget/background.

**Design system:** map the frame's distinct fill colors to Elementor global colors (primary/secondary/accent/text) so later edits stay on-brand.

## Execution Workflow

### Phase 1: Read and audit
1. Verify Respira + MCP via `respira_get_site_context`; confirm Elementor is active via `respira_list_plugins`. If not connected, stop and show setup guidance.
2. Read the chosen Figma frame's node tree via the agent's Figma access.
3. Build an inventory: node-type counts, smart-widget candidates, image fills to download, and flagged items (components with overrides, complex vectors/masks, prototyping, gradients beyond linear/radial).

### Phase 2: Build plan
Present a short plan and get confirmation:
- Which frame → which new page title
- Mapping summary table (Figma node → Elementor element, Auto/Manual)
- Flagged items needing manual attention
- The global-color palette that will be created

> Ready to build? I'll create a **draft duplicate / new draft page** and write the Elementor version there. Nothing live is touched.
> 1. Build the whole frame
> 2. Build section by section (review as we go)
> 3. Just keep this plan

### Phase 3: Build
For the approved frame:
1. Take a snapshot when available (`respira_get_snapshot`) and create a draft target with `respira_create_page_duplicate` (or a new draft page).
2. Map the Figma tree to the simplified Elementor tree using the mapping above; collapse empty wrappers.
3. Sideload images (`respira_sideload_image`) and set them on the matching widgets.
4. Create/align global colors so the palette carries over.
5. Write with `respira_build_page` (or `respira_inject_builder_content` section by section). Annotate any unmapped node with a clear migration note.
6. Report status for the frame before moving on.

### Phase 4: Verify
1. Summarize: sections/widgets built, images imported, items flagged.
2. Provide the wp-admin/Elementor editor link to the draft.
3. Give a checklist: open in the Elementor editor, check tablet/mobile, confirm images load, test links/buttons, review flagged items, compare against the Figma frame.

## Safety Model

- Read-only Figma analysis and a full plan before any write
- Explicit confirmation before building
- Always writes to a **draft duplicate / new draft** — never an existing live page
- Never auto-publishes
- Snapshot before write when available; rollback path is to delete the draft
- Original Figma file is read-only and never modified

## Honest Disclaimer

This skill rebuilds a Figma frame as an editable Elementor draft page.

It cannot:
- Guarantee pixel-perfect parity (different rendering engines)
- Reproduce Figma components/variants, prototyping, or complex masks/effects
- Auto-generate full responsive breakpoints from a single desktop frame
- Replace manual QA in the Elementor editor

It can:
- Turn a clean, auto-layout Figma frame into a structured Elementor page in minutes
- Preserve text, images, layout, typography, and color
- Carry the palette into Elementor global colors
- Flag exactly what needs a human, and keep everything live completely safe

## Tooling

**Figma read** (agent-side): a connected Figma MCP, or the Figma REST API with a personal access token.

**Respira tools**
- `respira_get_site_context`
- `respira_list_plugins`
- `respira_get_builder_info`
- `respira_create_page_duplicate`
- `respira_get_snapshot`
- `respira_sideload_image`
- `respira_build_page`
- `respira_inject_builder_content`
- `respira_convert_html_to_builder`
- `respira_find_element`
- `respira_update_element`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = figma-to-elementor`
- site/version context
- duration and success
- frames built, widgets created, images imported, items flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- Design System Synthesizer (turn the imported palette/type into a site-wide system)
- HTML to Bricks (the same idea for a different target builder)
- SEO & AEO Amplifier (optimize the new page once it is built)
- WordPress Site DNA (understand the target site before importing)

---

Built by Respira Team
https://respira.press/skills/figma-to-elementor
