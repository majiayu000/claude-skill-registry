---
name: build-oxygen6-page
description: "Use when building or rebuilding a page, header, footer, or template on an Oxygen 6 (Jenga) site, or when a previous attempt produced a blank page, one raw HTML block, or 'Unknown element'. Hands the agent the Oxygen 6 element schemas and the Template Content Area rule. Not for Oxygen Classic."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: workflow
---

# Build an Oxygen 6 Page

**Version:** 1.0.0
**Updated:** 2026-06-16
**Category:** workflow
**Status:** stable
**Requires:** Respira for WordPress plugin (7.4.10+) + MCP server, on a site running Oxygen 6 (Jenga)
**Telemetry endpoint:** https://www.respira.press/api/skills/track-usage

---

## Description

A focused recipe for building or rebuilding pages on **Oxygen 6** (codename Jenga, the Breakdance-based engine), the right way: as native, editable Oxygen elements, not a wall of raw HTML. Oxygen 6 is a different builder from Oxygen Classic, and its structure (separate header, footer, and template post types, a Template Content Area element, an `_oxygen_data` node tree) trips up agents that have not been told how it works. This skill hands you that structure up front so you stop rediscovering it every run and stop falling back to a single HTML code block.

Run this when you are about to build or rebuild a page, or a whole site, on an Oxygen 6 install.

---

## When to Use

- Building a new page on an Oxygen 6 site.
- Rebuilding an existing site into Oxygen 6 (for example from a Beaver Builder or Elementor source).
- A previous attempt produced a blank page, a single HTML/code block, or "Unknown element" / "This content cannot be displayed".
- Editing the site header, footer, or a template.

Do not use this for Oxygen Classic (the `ct_*` shortcode builder); that is a different engine.

---

## How Oxygen 6 is structured (read this first)

- **Pages**: a page's layout is a node tree stored in the `_oxygen_data` post meta. You never hand-write that JSON. You pass simplified `type` + `settings` to `build_page` / `inject_builder_content` and Respira maps them onto the real native classes (`OxygenElements\*`, and `EssentialElements\*` when the "Breakdance Elements for Oxygen" add-on is active).
- **Header / Footer / Templates are separate post types**: `oxygen_header`, `oxygen_footer`, `oxygen_template`. Edit the existing header and footer posts. Do not delete them and re-inline a header and footer into every page.
- **Templates need a Template Content Area**: an `oxygen_template` must contain a Template Content Area element (`OxygenElements\TemplateContentArea`) at the spot where the page body should render. Do **not** use a Post Content element on Oxygen 6 — it errors and the page cannot be edited. This is the single most common Oxygen 6 mistake.

## The native element vocabulary

Author with these simplified types (Respira maps each to the correct native element):

`section`, `row`, `column`, `heading` (settings: `text`, `level` h1-h6), `text`, `rich-text`, `button` (settings: `text`, `url`), `image` (settings: `url`), `icon`, `video`, and `code` (a raw HTML snippet — use ONLY for a genuine embed, never for a whole page).

Call `respira_get_builder_info` first. On an Oxygen 6 site it returns an `oxygen6` block with the exact per-element schemas and this structure playbook, current for the site.

## Steps

1. **Confirm the builder.** Run `respira_get_builder_info`. Verify it reports Oxygen 6 and read the `oxygen6` block (element schemas + structure).
2. **Read before you write.** For an existing page, extract its current tree so you append to or amend the real structure instead of overwriting it. For a rebuild, read the source content.
3. **Build native, section by section.** Compose a tree of the simplified types above: a `section` holding `heading` / `text` / `button` / `image`, etc. Use a real `heading` with a `level` for titles, never a styled text block. **Never** put a whole page or section into a single `code` block.
4. **Write it.** Use `build_page` for a new page or `inject_builder_content` for an existing one (with `mode: "append"` to add without overwriting, or an explicit replace confirmation to overwrite). Pass `builder: "oxygen"`.
5. **Verify it landed.** Re-read the page and confirm the elements are present and render. If a write reports success but the page reads back empty, that is a persistence problem on the host, not a content problem — report it rather than retrying blindly.
6. **Header / footer / template.** If the layout needs a shared header or footer, edit the existing `oxygen_header` / `oxygen_footer` posts. If you touch a template, make sure a Template Content Area element is present.

## Anti-patterns (do not do these)

- Dumping the whole page into one HTML/code element. It is not editable and defeats the builder.
- Using a Post Content element in a template on Oxygen 6.
- Deleting the global header/footer and inlining markup per page.
- Retrying the same write after a "success but blank" result. Surface it instead.
