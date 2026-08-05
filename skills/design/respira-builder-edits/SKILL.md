---
name: respira-builder-edits
description: Use for any in-page content edit on a WordPress site with a page builder. Covers finding elements, applying surgical edits, duplicating before large changes, and verifying the result. Works across Elementor 3 + 4, Divi 4 + 5, Beaver Builder, Bricks, Oxygen Classic, Oxygen 6, Breakdance, WPBakery, Uncode, and Gutenberg.
metadata:
  short-description: Safe, builder-native in-page editing across all supported builders
  version: 1.2.0
  updated_at: 2026-05-17
  respira_min_version: 7.1.0
---

# Respira Builder Edits

## Common Mistakes

| Mistake | Correct approach |
|---|---|
| Using `respira_update_page` to change a heading, image, or button | Use `respira_find_element` then `respira_update_element`. The page tool replaces the whole body and the builder loses every node. |
| Calling `respira_update_page` without checking `respira_get_builder_info` | Always identify the builder first. Update_page destroys builder JSON on builder-managed pages. |
| Editing raw builder JSON by guessing field names | Read the current structure with `respira_read_page`, `respira_find_element`, or `respira_get_builder_inline_schemas` before writing. |
| Making large changes without a snapshot | Always call `respira_create_page_duplicate` before multi-element edits. |
| Assuming Divi 5 uses the same field as Divi 4 | Divi 4 stores shortcodes in `post_content`. Divi 5 stores blocks plus a per-node `attrs._nodeId` minted by the complexifier. By-id matching needs the `_nodeId` fallback (added in v7.0.30). |
| Passing nested Divi 5 payloads through `children` only | Divi 5 also accepts Divi-vocabulary aliases `rows / cols / modules` (folded in v7.0.32). Pre-v7.0.32 these silently dropped. |
| Using a non-existent Beaver Builder module type | The `content_field_map` covers Heading, Text, Button, Image, HTML, Video, Sidebar, and Box (added in v7.0.13). Unknown types fall through without an error. |
| Passing flat `updates` like `{"button_text": "Go"}` | Pass either flat OR `{settings: {button_text: "Go"}}`. v7.0.16 deep-merges both into the settings object. v7.0.19 extended this through Divi 4. v7.0.29 extended it through `update_module` and `apply_builder_patch`. |
| Skipping `respira_get_page_outline` for "what is on this page" reads | The outline is lighter than `extract_builder_content` and ships per-row child counts plus a primary heading. Use it before deciding which element to edit. |

## Inputs

- The page or post URL, ID, or slug.
- A description of what to change (text, image URL, color, style, link).
- The builder in use, or unknown. Auto-detect with `respira_get_builder_info`.

## Workflow

1. **Understand the site.** Call `respira_get_site_context` and `respira_get_builder_info` if you haven't already.
2. **Understand the page.** Call `respira_get_page_outline` for a fast structural read, or `respira_find_element` if you already know what to target.
3. **Create a snapshot.** `respira_create_page_duplicate` before any edit that touches more than one element or that you're not 100% sure of.
4. **Find the element.** `respira_find_element` with the most specific selector available: text content, CSS class, widget type, or element ID. Bricks 2.3.x + Divi 5 surface both `id` and `attrs._nodeId`; either works.
5. **Apply the edit.** `respira_update_element` with only the fields that change. For multi-element edits on the same page, prefer `respira_batch_update`.
6. **Verify.** Re-read the element and confirm the change is reflected. For Divi 5, also check the front-end if it's a CSS or style-driven change because the renderer has its own paths.
7. **Report.** Tell the user what changed and where.

## Builder-specific notes

- **Elementor 3.** Content lives in `_elementor_data`. Each widget has `id`, `widgetType`, and `settings`. The base path is mature.
- **Elementor 4 (Atomic Elements).** v7.1 added end-to-end write support across 9 atomic widgets (`e-heading`, `e-paragraph`, `e-button`, `e-image`, `e-svg`, `e-divider`, `e-youtube`, `e-self-hosted-video`, `e-component`) plus 11 atomic layout containers (`e-flexbox`, `e-div-block`, `e-grid`, the `e-tabs` family, the `e-form` family). Pre-v7.1 every atomic write returned 422 `respira_elementor_atomic_write_unsupported`. The v4 normaliser lifts shorthand to the canonical `$$type` envelopes; the v4 validator catches malformed nodes before they hit the DB. Unsupported atomic types still refuse fast with `supported_widgets` in the error body.
- **Divi 4.** Shortcodes in `post_content`. v7.0.19 + v7.0.29 fixed update_element, batch_update, apply_builder_patch, remove_element, inject_builder_content, and update_module. The kses bypass survives so `<script>` and `<style>` inside `et_pb_code` are preserved. Custom post types are supported.
- **Divi 5.** Blocks plus `attrs._nodeId`. v7.0.16 fixed the background overlay key (`overlay.enable` is what the renderer reads). v7.0.28 fixed the number-counter typed envelope and the button text colour dual-write. v7.0.30 added the `_nodeId` fallback for id matching. v7.0.32 added the children-aliases fold (`rows`, `cols`, `modules`) plus a hard-error on silent child drops.
- **Beaver Builder.** v7.0.13 added Box module mappings. v7.0.16 fixed typed-node normalisation (`{type:'row', columns:[…]}`). v7.0.17 defaults missing column `size` to "100" so columns render full-width when the agent omits it. v7.0.25 fixed the top-level font-field stdClass fatal. v7.0.26 expanded that to typography containers. Custom HTML in modules survives the kses bypass.
- **Bricks.** v7.0.23 fixed page-settings deep-merge and the CSS regen API. v7.0.24 closed the file-mode CSS regen gap. v7.0.26 fixed global-class id resolution and the `EDITABLE` route collision that was clobbering the registry. v7.0.27 unified settings normalisation: null deletes, `_background.color` and `_color` string lift to `{hex, raw}`, typography keys migrate into `_typography`, `_gap` fans out to `_columnGap` + `_rowGap`.
- **Oxygen Classic.** v7.0.18 added the root-wrapped `_ct_builder_json` shape (`{id:0, name:"root", depth:0, children:[…]}`). Legacy bare-array pages self-heal on next read. v7.0.17 wraps inject in `try/catch \Throwable` so third-party plugins hooked into `oxy_save_ct_builder_json_meta` no longer fatal the REST request.
- **Oxygen 6.** Storage is `_oxygen_data`, a different format from Classic. v7.0.7 brought deep-intelligence parity.
- **Breakdance.** v7.0.20 added `resolve_breakdance_properties()` for every shape an agent emits. v7.0.21 added `nest_breakdance_content_section()` for the 15 element types whose renderer reads `content.content.*`. v7.0.22 fixed append unwrap and the replace-confirmation gate.
- **WPBakery + Uncode.** v7.0.31 added the Uncode adapter pack (`uncode_*` and `tdb_*` shortcodes as first-class elements), pagination on `find_builder_targets`, populated labels via decoded content-bearing attrs, and `respira_get_page_outline` plus `respira_get_builder_inline_schemas`. Filterable via `respira_wpbakery_shortcode_prefixes` for site-specific extensions.

## Rules

- Never use `respira_update_page` for content edits. It replaces the entire page body and the builder treats the result as a single text blob.
- Never guess builder JSON field names. Read first, then write.
- Always run `respira_get_site_context` plus `respira_get_builder_info` before the first edit on a page you haven't touched in the current session.
- For Divi 5, when matching by id, expect both `id` and `attrs._nodeId` to resolve.
- For Bricks file-mode CSS (cssLoading=file), v7.0.24 primes the front-end state so per-element rules emit correctly. No workaround needed.
- When the builder is unknown, call `respira_get_builder_info` and wait for confirmation before editing.

## Verification

After every edit:

1. Call `respira_find_element` with the same selector used before the edit.
2. Confirm the changed field matches the intended value.
3. If the element is not found or unchanged, check whether `respira_update_element` returned an error or a structured soft-fail.

For batch edits:

1. Use `respira_diff_snapshots` to compare the before / after snapshot.
2. Confirm all changed elements are reflected; flag any that are missing.

## Escalation

Stop and ask the user if:

- `respira_get_builder_info` returns an unknown or unsupported builder.
- `respira_update_element` returns a soft-fail on a Bricks, Oxygen, or Breakdance element after the v7.0.x fixes have been applied.
- The page is protected by a WAF or security plugin that blocks the REST endpoint. `respira_diagnose_connection` detects Cloudflare-edge write blocks.
- The edit would touch more than 20 elements. Confirm scope before proceeding.

## Example

Goal: change the hero heading text from "Welcome" to "Get started today."

```
1. respira_get_builder_info        → Elementor 3.21, supported
2. respira_get_page_outline        → 4 sections, hero is row 0, primary heading "Welcome"
3. respira_create_page_duplicate   → snapshot ID abc123
4. respira_find_element            → selector: text="Welcome", type: heading
   Result: element ID e7a2, widgetType: heading, settings.title: "Welcome"
5. respira_update_element          → element ID e7a2, settings.title: "Get started today."
6. respira_find_element            → element ID e7a2
   Result: settings.title: "Get started today." ✓
```
