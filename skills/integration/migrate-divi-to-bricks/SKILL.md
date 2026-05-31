---
name: migrate-divi-to-bricks
description: Converts Divi-built WordPress pages to Bricks Builder. Parses Divi's shortcode tree from post_content, maps each module to its Bricks element equivalent, generates a migration plan for approval, and writes clean Bricks JSON to the target pages. Use when user says "migrate Divi to Bricks", "replace Divi with Bricks", "switch from Divi to Bricks", or "rebuild Divi pages in Bricks".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Divi to Bricks

Converts Divi-built WordPress pages to Bricks Builder. Parses Divi's shortcode-based content from post_content, maps each module to its Bricks element equivalent, generates a migration plan for approval, and writes clean Bricks JSON to the target pages. Use this skill whenever someone wants to move from Divi to Bricks, replace the Divi Builder with Bricks, or rebuild Divi pages in Bricks.

## What This Skill Does

This is a cross-format migration — Divi stores content as nested shortcodes in `post_content`, while Bricks uses a JSON array in `_bricks_page_content_2`. The skill must parse Divi's shortcode hierarchy, understand each module's purpose and settings, then reconstruct that intent as Bricks elements with proper parent-child relationships and settings.

The format gap makes this complex, but both builders are feature-rich visual editors, so most Divi modules have strong Bricks equivalents. The result is cleaner, faster-rendering content in Bricks' modern architecture.

**Handles:**
- et_pb_section → Bricks Section element
- et_pb_row/et_pb_column → Bricks Container elements (with flex layout)
- et_pb_text → Bricks Text Basic element
- et_pb_blurb → Bricks Icon Box or Container with child elements
- et_pb_image → Bricks Image element
- et_pb_button → Bricks Button element
- et_pb_video → Bricks Video element
- et_pb_heading (via text modules) → Bricks Heading element
- et_pb_divider → Bricks Divider element
- et_pb_accordion/et_pb_toggle → Bricks Accordion element
- et_pb_tabs → Bricks Tabs element
- et_pb_gallery → Bricks Gallery element
- et_pb_slider → Bricks Slider element (close mapping)
- et_pb_pricing_tables → Bricks Pricing Table element
- et_pb_code → Bricks Code element
- et_pb_map → Bricks Map element
- Custom CSS → Bricks custom CSS fields
- Column width ratios → Bricks container flex percentages

**Preserves:**
- All text content and inline HTML formatting
- Image URLs, alt text, and dimensions
- Typography settings (font family, size, weight)
- Color values and gradients
- Spacing (margin, padding) — converted from Divi's format to Bricks'
- Background images and overlays
- Border and shadow settings
- Button labels, URLs, targets
- CSS classes

## What This Skill Does NOT Do

- **Specialty sections** — Divi's specialty section layouts (sidebar + content) need manual layout setup in Bricks.
- **Global modules** — Divi's global modules (`et_pb_layout` post type) are resolved to inline content. Bricks templates must be set up separately.
- **Third-party Divi modules** — Plugins extending Divi (Divi Toolbox, Divi Supreme, etc.) are flagged for manual recreation.
- **Divi theme customizer** — Global fonts, colors, and spacing from the Divi theme customizer don't transfer. These need to be set in Bricks theme settings.
- **Dynamic content** — Divi's dynamic content needs Bricks' dynamic data system configured separately.
- **Contact forms** — et_pb_contact_form needs to be rebuilt using Bricks' form element or a forms plugin.
- **Divi Library layouts** — Stored as `et_pb_layout` post type; not auto-migrated to Bricks templates.
- **Motion effects** — Scroll effects and animations differ between builders.
- **Divi theme dependency** — If using the Divi theme (not just plugin), you are switching to Bricks theme — a complete theme change.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Divi theme or Divi Builder plugin active (to read source content)
- Bricks theme installed and active (to write target content)
- Read access to scan Divi content
- Write access to create duplicates with Bricks content

## Trigger Phrase

- "migrate divi to bricks"

## Alternative Triggers

- "convert divi to bricks"
- "switch from divi to bricks"
- "rebuild divi pages in bricks"
- "move from divi to bricks"
- "divi to bricks migration"
- "replace divi with bricks"

## Source Builder: Divi

Divi stores content as shortcodes in `post_content`. The module structure follows a strict hierarchy:

```
[et_pb_section fb_built="1" _builder_version="4.x"]
  [et_pb_row _builder_version="4.x"]
    [et_pb_column type="4_4" _builder_version="4.x"]
      [et_pb_text _builder_version="4.x"]
        <p>Content here</p>
      [/et_pb_text]
    [/et_pb_column]
  [/et_pb_row]
[/et_pb_section]
```

Key Divi specifics:
- **Section types**: regular, fullwidth, specialty
- **Column types**: `4_4`, `1_2`, `1_3`, `2_3`, `1_4`, `3_4`
- **Settings as attributes**: `background_color`, `custom_margin`, `custom_padding`, `text_orientation`
- **Content encoding**: HTML entities, percent-encoding, occasional base64
- **Global modules**: `global_module` attribute → `et_pb_layout` post type
- **Custom CSS**: `custom_css_main_element`, `custom_css_before`, `custom_css_after`

Read Divi content via `wordpress_extract_builder_content` with `builder=divi`.

## Target Builder: Bricks

Bricks stores content in `_bricks_page_content_2` as a JSON array:

```json
[
  { "id": "abc123", "name": "section", "parent": 0, "settings": {...} },
  { "id": "def456", "name": "container", "parent": "abc123", "settings": {...} },
  { "id": "ghi789", "name": "heading", "parent": "def456", "settings": { "tag": "h2", "text": "..." } }
]
```

Key Bricks specifics:
- Elements use `name` field: `section`, `container`, `heading`, `text-basic`, `image`, `button`
- Parent-child via `parent` field referencing `id`
- IDs are short alphanumeric strings
- Settings use Bricks-specific keys
- Responsive via `_breakpoints` within settings

Write Bricks content via `wordpress_inject_builder_content` with `builder=bricks`.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm Divi is active via `wordpress_list_plugins` and `wordpress_get_site_context`.
3. Confirm Bricks theme is installed via `wordpress_get_site_context`.
4. **Important**: If using Divi theme (not plugin), note this is a full theme switch to Bricks.
5. Scan all content for Divi usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - Check builder via `wordpress_get_builder_info`
6. Extract Divi content via `wordpress_extract_builder_content` with `builder=divi`
7. Build inventory:
   - Total pages/posts using Divi
   - Module types (frequency count)
   - Specialty sections found
   - Global modules referenced
   - Third-party Divi modules
   - Content encoding issues
   - Complexity per page

### Phase 2: Migration Plan

```
## Divi → Bricks Migration Plan

### Theme Transition Note
[If Divi theme is active]: This migration involves switching from the Divi
theme to the Bricks theme. Headers, footers, and global templates will need
to be recreated in Bricks' template system.

### Site Inventory
- Total Divi pages: X
- Total modules to convert: X
- Auto-convertible: X (Y%)
- Manual attention: X (Y%)

### Module → Element Mapping
| Divi Module        | Bricks Element  | Status   |
|-------------------|----------------|----------|
| et_pb_text        | text-basic     | Auto     |
| et_pb_image       | image          | Auto     |
| et_pb_blurb       | icon-box       | Auto     |
| et_pb_button      | button         | Auto     |
| et_pb_slider      | slider         | Auto     |
| et_pb_tabs        | tabs           | Auto     |
| et_pb_accordion   | accordion      | Auto     |
| et_pb_contact     | —              | Manual   |
| [divi addon]      | —              | Manual   |

### Shortcode Parsing Complexity
- Pages with clean shortcodes: X
- Pages with encoded content: X (will decode during migration)
- Pages with specialty sections: X (layout approximation needed)

### Page-by-Page Plan
1. **[Page Title]** — X modules, [complexity]
2. ...
```

Ask for confirmation:
> Bricks offers a modern replacement for Divi with cleaner output. Your originals stay safe.
> 1. Migrate all pages
> 2. Migrate specific pages
> 3. Start with a test page (recommended)
> 4. Just keep this plan

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read Divi content via `wordpress_extract_builder_content` with `builder=divi`
2. Parse the shortcode tree:
   - Identify section → row → column → module hierarchy
   - Decode encoded content (HTML entities, percent-encoding)
   - Resolve global modules to inline content
   - Map column types to percentage widths
3. Build Bricks JSON array:
   - Create `section` element for each `et_pb_section`
   - Create `container` elements for rows/columns with flex layout
   - Map column widths: `4_4`→100%, `1_2`→50%, `1_3`→33.33%, etc.
   - Convert each module → Bricks element:
     - `et_pb_text` → `text-basic` (preserve inner HTML)
     - `et_pb_blurb` → `icon-box` or container with children
     - `et_pb_image` → `image` (map src, alt, title attributes)
     - `et_pb_button` → `button` (map text, URL, style)
   - Map Divi attributes to Bricks settings (colors, spacing, typography)
   - Generate unique IDs and proper parent references
   - Flag unmappable modules with comments
4. Create duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Write Bricks JSON via `wordpress_inject_builder_content` with `builder=bricks`
6. Report status

### Phase 4: Post-Migration Verification

1. Summarize migrations:
   - Pages migrated, elements created, items flagged
2. For each migrated page:
   - Link to Bricks editor
   - Flagged items
   - Layout notes (specialty sections, encoded content)
3. Post-migration checklist:
   - [ ] Open each duplicate in Bricks editor
   - [ ] Verify section/container structure
   - [ ] Check responsive views
   - [ ] Verify images and media
   - [ ] Test links and buttons
   - [ ] Recreate flagged modules
   - [ ] Set up Bricks templates for header/footer (if switching from Divi theme)
   - [ ] Rebuild contact forms using Bricks form element or plugin
   - [ ] Compare with Divi original
   - [ ] Check for any Divi shortcode remnants

## Safety Model

- Read-only analysis first — full content scan before any changes
- Explicit user confirmation required before creating duplicates
- Original Divi pages are never modified or deleted
- All migrated content goes to draft duplicates only
- Never auto-publishes migrated pages
- Creates a snapshot before migration begins (when available)
- Provides clear rollback path (delete duplicates)
- Warns about theme switch implications if using Divi theme

## Honest Disclaimer

This skill converts Divi page content to Bricks format and creates draft duplicates for review.

It cannot:
- Migrate Divi specialty sections with perfect layout fidelity
- Convert global modules to Bricks templates automatically
- Handle third-party Divi plugin modules
- Migrate Divi theme customizer settings
- Replace forms, popups, or animation setup
- Guarantee pixel-perfect results from shortcode-to-JSON conversion

It can:
- Parse complex Divi shortcode hierarchies including encoded content
- Convert 75-85% of standard Divi modules to Bricks elements
- Preserve all text, images, links, and core styling
- Take advantage of Bricks' modern, faster rendering
- Save days of manual page rebuilding
- Flag everything that needs manual attention
- Keep original pages completely safe

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
- `skill_slug = migrate-divi-to-bricks`
- site/version context
- duration and success
- pages migrated, elements created, modules flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (understand site structure and theme before migrating)
- Internal Link Builder (verify internal links post-migration)
- SEO & AEO Amplifier (verify SEO preservation post-migration)
- Technical Debt Audit (find Divi shortcode remnants post-migration)

---

Built by Respira Team
https://respira.press/skills/migrate-divi-to-bricks
