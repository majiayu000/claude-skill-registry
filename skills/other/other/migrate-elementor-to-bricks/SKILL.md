---
name: migrate-elementor-to-bricks
description: Converts Elementor-built WordPress pages to Bricks Builder. Reads Elementor's JSON widget tree from post meta, maps each widget to its closest Bricks element equivalent, generates a migration plan for approval, and writes clean Bricks JSON to the target pages. Use when user says "migrate Elementor to Bricks", "switch from Elementor to Bricks", or "rebuild Elementor pages in Bricks".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Elementor to Bricks

Converts Elementor-built WordPress pages to Bricks Builder. Reads Elementor's JSON widget tree from post meta, maps each widget to its closest Bricks element equivalent, generates a migration plan for approval, and writes clean Bricks JSON to the target pages. Use this skill whenever someone wants to move from Elementor to Bricks, rebuild Elementor pages in Bricks, or switch page builders from Elementor to Bricks.

## What This Skill Does

Elementor and Bricks are both visual page builders, but they store content in fundamentally different formats — Elementor uses a nested JSON widget tree in `_elementor_data`, while Bricks uses a flat-ish JSON array in `_bricks_page_content_2`. This skill bridges that gap by reading every Elementor widget, understanding its purpose, and recreating it as the appropriate Bricks element.

**Handles:**
- Section/Column layouts → Bricks Section/Container elements
- Text Editor, Heading, Image, Video, Button widgets → native Bricks equivalents
- Icon, Icon Box, Image Box, Star Rating → Bricks icon and media elements
- Tabs, Accordion, Toggle → Bricks interactive elements
- Form widgets → Bricks form elements (where available)
- Spacer, Divider, Google Maps → utility element equivalents
- Custom CSS from Elementor's Advanced tab → Bricks custom CSS fields
- Responsive visibility settings → Bricks breakpoint visibility
- Motion effects and entrance animations → Bricks interaction settings (where supported)
- Inner Section nesting → Bricks nested container structure
- Global widget references → resolved to inline content (Bricks templates noted for manual setup)

**Preserves:**
- Content text, images, links, and media references
- Typography settings (font family, size, weight, line-height, letter-spacing)
- Color values (hex, rgb, rgba, CSS variables)
- Spacing (margin, padding) and sizing
- Background images, overlays, gradients
- Border and border-radius settings
- Box shadow values
- Link targets and rel attributes
- CSS classes and IDs

## What This Skill Does NOT Do

- **Third-party Elementor addons** — Widgets from Essential Addons, JetElements, Crocoblock, PowerPack, etc. are flagged for manual migration. The skill cannot map proprietary addon widgets to Bricks equivalents automatically.
- **Elementor Pro dynamic tags** — Dynamic content (ACF fields, custom field displays, loop templates) require Bricks' own dynamic data system, which has different capabilities. These are flagged, not auto-converted.
- **Theme Builder templates** — Elementor's header/footer/archive/single templates use a different storage mechanism. This skill migrates page content, not theme builder templates.
- **Popup/modal content** — Elementor popups are stored separately and are not included in page migration.
- **WooCommerce widgets** — Elementor Pro's product grid, cart, checkout widgets need Bricks' WooCommerce elements configured separately.
- **Pixel-perfect recreation** — Bricks uses a different rendering engine. Spacing and alignment will be close but may need manual fine-tuning.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Elementor plugin active (to read source content)
- Bricks theme installed and active (to write target content)
- Read access to scan Elementor content
- Write access to create duplicates with Bricks content

## Trigger Phrase

- "migrate elementor to bricks"

## Alternative Triggers

- "convert elementor to bricks"
- "switch from elementor to bricks"
- "rebuild elementor pages in bricks"
- "move my site from elementor to bricks"
- "elementor to bricks migration"

## Source Builder: Elementor

Elementor stores page content in the `_elementor_data` post meta field as a JSON string. The structure is a nested tree:

```
Document
  └─ Section (type: "section")
       ├─ settings: { structure, layout, content_width, ... }
       └─ elements: [
            Column (type: "column")
              ├─ settings: { _column_size, ... }
              └─ elements: [
                   Widget (type: "widget", widgetType: "heading")
                     └─ settings: { title, size, header_size, ... }
                 ]
          ]
```

Key Elementor specifics:
- **Widget types** are in the `widgetType` field (e.g., `heading`, `text-editor`, `image`, `button`)
- **Responsive settings** use suffixes: `margin`, `margin_tablet`, `margin_mobile`
- **CSS** is cached in `_elementor_css` post meta — not needed for migration but useful for verification
- **Page settings** in `_elementor_page_settings` (page layout, hide title, etc.)
- **Global widgets** reference a template via `templateID` — must be resolved before mapping

Read Elementor content via `wordpress_extract_builder_content` with `builder=elementor`.

## Target Builder: Bricks

Bricks stores content in `_bricks_page_content_2` as a JSON array. Each element is a flat object with parent references:

```json
[
  { "id": "abc123", "name": "section", "parent": 0, "settings": {...} },
  { "id": "def456", "name": "container", "parent": "abc123", "settings": {...} },
  { "id": "ghi789", "name": "heading", "parent": "def456", "settings": { "tag": "h2", "text": "..." } }
]
```

Key Bricks specifics:
- Elements use `name` (not widgetType): `section`, `container`, `heading`, `text-basic`, `image`, `button`, `video`, `icon`
- Parent-child relationships use `parent` field referencing parent `id`
- IDs are short alphanumeric strings (6 chars typical)
- Settings keys differ from Elementor (e.g., `tag` not `header_size`, `text` not `title`)
- Responsive settings use `_breakpoints` key within settings

Write Bricks content via `wordpress_inject_builder_content` with `builder=bricks`.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm Elementor is active via `wordpress_list_plugins`.
3. Confirm Bricks theme is installed via `wordpress_get_site_context`.
4. Scan all content for Elementor usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - For each, check if built with Elementor via `wordpress_get_builder_info`
5. For each Elementor page, extract content via `wordpress_extract_builder_content` with `builder=elementor`
6. Build an inventory:
   - Total pages/posts using Elementor
   - Widget types used across the site (frequency count)
   - Third-party addon widgets detected (flagged for manual handling)
   - Global widgets referenced
   - Dynamic tags usage
   - Estimated migration complexity per page (simple/moderate/complex)

### Phase 2: Migration Plan

Present a clear migration plan:

```
## Elementor → Bricks Migration Plan

### Site Inventory
- Total Elementor pages: X
- Total widgets to convert: X
- Auto-convertible widgets: X (Y%)
- Manual attention needed: X (Y%)

### Widget Mapping Summary
| Elementor Widget | Bricks Element | Status |
|-----------------|----------------|--------|
| heading         | heading        | Auto   |
| text-editor     | text-basic     | Auto   |
| image           | image          | Auto   |
| [addon widget]  | —              | Manual |

### Page-by-Page Plan
1. **[Page Title]** — X widgets, [simple/moderate/complex]
   - Auto-convertible: X widgets
   - Needs attention: [list any flagged widgets]
2. ...

### Flagged Items (Require Manual Work)
- [List of third-party widgets, dynamic tags, etc.]
```

Ask for confirmation:
> Ready to proceed? I'll create Bricks duplicates of each page — your original Elementor pages stay untouched.
> 1. Migrate all pages
> 2. Migrate specific pages (pick from list)
> 3. Start with a test page first
> 4. Just keep this plan as reference

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read full Elementor content via `wordpress_extract_builder_content` with `builder=elementor`
2. Walk the Elementor JSON tree and map each widget:
   - Convert Section → Bricks `section`
   - Convert Column → Bricks `container` (assign parent)
   - Convert each widget → appropriate Bricks element
   - Map settings: typography, colors, spacing, backgrounds, borders
   - Convert responsive suffixes (`_tablet`, `_mobile`) to Bricks breakpoint format
   - Resolve global widgets to inline content
   - Flag unmappable widgets with `<!-- MIGRATION NOTE: ... -->` comments
3. Generate valid Bricks JSON array with proper `id`, `name`, `parent`, `settings`
4. Create a duplicate page via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Write Bricks content to the duplicate via `wordpress_inject_builder_content` with `builder=bricks`
6. Report status for this page before moving to next

### Phase 4: Post-Migration Verification

1. Summarize all migrations:
   - Pages migrated successfully
   - Total widgets converted
   - Items flagged for manual attention
2. For each migrated page, provide:
   - Link to the Bricks duplicate in wp-admin
   - List of any flagged widgets or settings that need manual review
   - Comparison notes (what was preserved vs. what needs adjustment)
3. Provide a post-migration checklist:
   - [ ] Open each duplicate in Bricks editor and review layout
   - [ ] Check responsive views (tablet, mobile)
   - [ ] Verify all images and media load correctly
   - [ ] Test all links and buttons
   - [ ] Review flagged items and recreate manually
   - [ ] Check forms and interactive elements
   - [ ] Compare side-by-side with Elementor original

## Safety Model

- Read-only analysis first — full Elementor content scan before any changes
- Explicit user confirmation required before creating any duplicates
- Original Elementor pages are never modified or deleted
- All migrated content goes to draft duplicates only
- Never auto-publishes migrated pages
- Creates a snapshot before migration begins (when available)
- Provides clear rollback path (delete duplicates)

## Honest Disclaimer

This skill converts Elementor page content to Bricks Builder format and creates draft duplicates for review.

It cannot:
- Migrate third-party Elementor addon widgets automatically
- Recreate Elementor Pro dynamic tags or loop templates
- Guarantee pixel-perfect visual parity
- Migrate theme builder templates (headers, footers, archives)
- Convert Elementor popups or modal content
- Replace manual QA and visual review

It can:
- Convert 80-90% of standard Elementor widgets to Bricks equivalents
- Preserve text content, images, links, and basic styling
- Save days of manual page rebuilding
- Provide a clear map of what needs manual attention
- Keep your original pages completely safe during the process

## Tooling

**Core WordPress tools**
- `wordpress_get_site_context`
- `wordpress_list_plugins`
- `wordpress_list_pages`
- `wordpress_list_posts`
- `wordpress_read_page`
- `wordpress_read_post`
- `wordpress_get_builder_info`
- `wordpress_extract_builder_content`
- `wordpress_inject_builder_content`
- `wordpress_find_builder_targets`
- `wordpress_create_page_duplicate`
- `wordpress_create_post_duplicate`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = migrate-elementor-to-bricks`
- site/version context
- duration and success
- pages migrated, widgets converted, widgets flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (understand site structure before migrating)
- Internal Link Builder (rebuild internal links after migration)
- SEO & AEO Amplifier (verify SEO preservation post-migration)
- Technical Debt Audit (clean up post-migration)

---

Built by Respira Team
https://respira.press/skills/migrate-elementor-to-bricks
