---
name: html-to-bricks
description: "Convert raw HTML/CSS into native Bricks Builder elements. Maps colors, typography, and spacing to your design system tokens so the result is drift-resistant. ACSS class mapping when ACSS is installed."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# HTML to Bricks Builder

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** migration
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + Bricks Builder active + MCP server

---

## Description

Convert raw HTML/CSS — pasted from a design export, a Figma extraction, an existing landing page on another platform, or a competitor's source code — into native Bricks Builder elements. Not a screenshot-to-builder pass; this is a structural conversion that respects Bricks' element schemas, ACSS classes (if installed), and the site's design system.

Resolves [open feature request: HTML to Bricks Builder]. Uses the existing `respira_convert_html_to_builder` MCP tool, with a Bricks-specific workflow layered on top.

---

## When to Use

- A designer hands you HTML/CSS from a Webflow export, a Framer export, or a CodePen
- You're rebuilding a competitor's landing page (legally — don't copy proprietary work) and want to start from their structure
- You have an old static HTML page you want to bring into your live Bricks-powered site
- You're prototyping a section in HTML and want to land it in Bricks for further editing

---

## Trigger Phrases

- "convert this html to bricks"
- "import this design into bricks"
- "paste html into bricks"
- "html to bricks"
- "turn this html into a bricks page"
- "bring this codepen into bricks"

---

## Execution Workflow

### Step 1 — Verify Bricks is active

Call `respira_get_builder_info`. If the active builder is NOT Bricks, stop and tell the user: *"This skill targets Bricks Builder. Your active builder is {X}. Use the generic `convert html to builder` workflow instead, or switch the active builder."*

If Bricks is active, capture its version.

### Step 2 — Confirm site + target page

Call `respira_get_active_site`. Ask:

- *"Convert the HTML into a new page (I'll create it), or into an existing page (you tell me which)?"*
- If existing: confirm the page ID and remind the user that a SafeEdit duplicate will be created.

### Step 3 — Pull design system if present

Call `respira_get_option('respira_design_system')`. If present, capture colors, typography, spacing tokens. The conversion will map raw CSS values (e.g. `#2563EB`) to design system tokens (e.g. `primary`) so the converted page is drift-resistant.

### Step 4 — Accept the HTML input

Three input modes:

- **Mode A — pasted in the conversation.** The user pastes raw HTML directly.
- **Mode B — URL.** The user gives a public URL; fetch the HTML via WebFetch or `/browse`. **Do NOT silently re-host external assets**; flag external images so the user can decide to mirror them.
- **Mode C — file.** The user uploads or references a local HTML file path.

In all modes, also accept inline `<style>` blocks and external `<link rel=stylesheet>` references. For external stylesheets, fetch their text content.

### Step 5 — Run the conversion

Call `respira_convert_html_to_builder` with `builder=bricks`, the HTML, the CSS, and the design-system context.

The MCP tool returns a Bricks element tree. Each element has a `name` (Bricks element type — `section`, `block`, `container`, `heading`, `text-basic`, `button`, `image`, etc.) and `settings` matching the Bricks schema.

### Step 6 — Map raw values to design system tokens

For each element in the tree:

- If `settings.color` is a hex value matching one of the design system colors, replace with a token reference
- If `settings.typography.font-family` matches the design system heading or body family, replace with a token reference
- If `settings.padding`, `settings.margin`, `settings.gap` are pixel values matching the design system spacing scale, replace with token references

This step is the difference between a one-off conversion and a maintainable page. After the conversion, if the user updates the design system, the converted page reflects it.

### Step 7 — ACSS class mapping (if ACSS detected)

Call `respira_get_option('automatic_css_settings')` or check the active theme for ACSS. If ACSS is installed:

- Map common CSS patterns to ACSS classes
- `padding: 96px 24px` → ACSS section padding utility
- `max-width: 1280px; margin: 0 auto` → ACSS container class
- Heading font sizes → ACSS heading scale classes

This is optional and gated on ACSS being present. If ACSS isn't installed, fall through to inline settings.

### Step 8 — Inject into the page

For a new page: call `respira_build_page` with the Bricks element tree as the page body.

For an existing page: call `respira_create_page_duplicate` first (SafeEdit), then `respira_inject_builder_content` against the duplicate.

Output the new (or duplicate) page URL.

### Step 9 — Verify

Open the new page in the Bricks editor (the URL pattern is `/?bricks=run&page_id={id}`). Visually verify:

- All sections render
- Typography looks correct
- Colors map to design system tokens
- Spacing is consistent
- Images load (warn if any external image URLs were preserved unmirrored)

If anything is off, the user can refine in the Bricks editor directly. Common issues to flag:

- HTML elements Bricks doesn't have a 1:1 mapping for (e.g. `<details>` collapsible → mapped to Bricks accordion)
- Forms — HTML `<form>` doesn't convert into Bricks Form element 1:1. Flag and ask the user to wire the form fields manually.
- Custom animations — CSS keyframes don't convert. Flag.

---

## Hard rules

- **Bricks-only.** This skill is locked to Bricks. For other builders, use the generic `convert_html_to_builder` workflow.
- **Never inject HTML directly into the page body.** If the conversion can't map an HTML element to a Bricks element, the skill must report the failure and let the user decide. Do not fall back to a "code block" element that pastes raw HTML — that recreates the do-not-write-raw-HTML failure mode.
- **External assets are flagged, not mirrored.** Don't silently download external images and side-load them. Flag them so the user explicitly decides to mirror.
- **Always SafeEdit on existing pages.** Never convert HTML into a live page directly. Duplicate first.
- **Design system tokens take precedence over raw values.** When a CSS hex matches a design system color, use the token. Always.

---

## Telemetry

Records: site URL hash, Bricks version, HTML input size (bytes), elements converted count, design system bound, ACSS detected, success/failure, total duration. No HTML content, no element names, no page IDs sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
