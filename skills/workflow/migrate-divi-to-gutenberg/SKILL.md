---
name: migrate-divi-to-gutenberg
description: Converts Divi-built WordPress pages to native Gutenberg blocks. Parses Divi's shortcode tree from post_content, maps each module to its closest core block equivalent, generates a migration plan for approval, and writes clean block markup to the target pages. Use when user says "migrate Divi to Gutenberg", "switch from Divi to native blocks", "remove Divi dependency", or "rebuild Divi pages in the block editor".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Divi to Gutenberg

Converts Divi-built WordPress pages to native Gutenberg blocks. Parses Divi's shortcode-based content from post_content, maps each module to its closest core block equivalent, generates a migration plan for approval, and writes clean block markup to the target pages. Use this skill whenever someone wants to move from Divi to Gutenberg, eliminate the Divi dependency, switch to native blocks, or simplify their WordPress stack by removing Elegant Themes' builder.

## What This Skill Does

Divi stores everything as nested shortcodes directly in `post_content` — a fundamentally different approach from JSON-based builders. The content is a hierarchy of `[et_pb_section]`, `[et_pb_row]`, `[et_pb_column]`, and `[et_pb_module]` shortcodes with settings as attributes. Converting this to Gutenberg blocks means parsing that shortcode tree, extracting content and settings, and generating the equivalent `<!-- wp:block -->` markup.

This is one of the more complex migrations because Divi shortcodes often contain escaped HTML, base64-encoded content, and deeply nested attribute strings that need careful parsing.

**Handles:**
- et_pb_section → Group block with layout settings
- et_pb_row/et_pb_column → Columns and Column blocks
- et_pb_text → Paragraph blocks (with inline HTML preserved)
- et_pb_blurb → Group block with Image + Heading + Paragraph
- et_pb_image → Image block
- et_pb_button → Buttons block
- et_pb_video → Video or Embed block
- et_pb_divider → Separator block
- et_pb_slider/et_pb_slide → Gallery or Group blocks (simplified)
- et_pb_accordion/et_pb_accordion_item → Details blocks (WP 6.3+)
- et_pb_tabs/et_pb_tab → Group with heading blocks
- et_pb_toggle → Details block (WP 6.3+)
- et_pb_code → Custom HTML block
- et_pb_sidebar → Widget block
- et_pb_gallery → Gallery block
- et_pb_counters → HTML approximation
- Fullwidth variants (et_pb_fullwidth_*) → full-width Group blocks

**Preserves:**
- All text content and inline HTML formatting
- Image URLs, alt text, and links
- Heading text and hierarchy
- Button labels, URLs, and targets
- Video URLs and embed sources
- List content
- Code block contents
- Basic color settings where Gutenberg supports them

## What This Skill Does NOT Do

- **Divi's visual design layer** — Divi applies extensive CSS through its settings (gradient backgrounds, custom fonts from 800+ Google Fonts choices, box shadows with specific blur/spread, text shadow, filters, transforms). Gutenberg supports some of these; many will be simplified or lost.
- **Specialty sections** — Divi's specialty section layouts (sidebar + content combinations) have no direct Gutenberg equivalent.
- **Global modules** — Stored as `et_pb_layout` post type. These are resolved to inline content during migration; Gutenberg reusable blocks can be created manually afterward.
- **Divi Builder plugin modules** — Modules added by Divi-specific plugins (Divi Toolbox, Divi Supreme, etc.) are flagged.
- **Theme customizer settings** — Divi theme customizer values (global fonts, colors, sizing) don't transfer to block themes.
- **Dynamic content** — Divi's dynamic content features need separate solutions.
- **Contact forms** — et_pb_contact_form needs a forms plugin (WPForms, etc.).
- **Divi Library layouts** — Template library layouts stored in et_pb_layout post type are not auto-migrated.
- **Advanced design settings** — Rounded corners, CSS filters, blend modes, and transforms have limited Gutenberg support.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Divi theme or Divi Builder plugin active (to read source content)
- WordPress 6.0+ (6.3+ recommended for Details block support)
- A block-compatible theme ready for post-migration (if switching from Divi theme)
- Read access to scan Divi content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate divi to gutenberg"

## Alternative Triggers

- "convert divi to blocks"
- "switch from divi to gutenberg"
- "remove divi builder"
- "rebuild divi pages with blocks"
- "divi to block editor"
- "decommission divi"
- "get off divi"

## Source Builder: Divi

Divi stores content as shortcodes in `post_content`. The module structure follows a strict hierarchy:

```
[et_pb_section fb_built="1" _builder_version="4.x"]
  [et_pb_row _builder_version="4.x"]
    [et_pb_column type="4_4" _builder_version="4.x"]
      [et_pb_text _builder_version="4.x"]
        <p>Your content here</p>
      [/et_pb_text]
      [et_pb_image src="image.jpg" alt="Alt text" _builder_version="4.x"][/et_pb_image]
      [et_pb_button button_text="Click Me" button_url="https://..." _builder_version="4.x"][/et_pb_button]
    [/et_pb_column]
  [/et_pb_row]
[/et_pb_section]
```

Key Divi specifics:
- **Section types**: regular, fullwidth, specialty (with predefined column layouts)
- **Column types**: defined by `type` attribute — `4_4` (full), `1_2` (half), `1_3` (third), `2_3` (two-thirds), `1_4` (quarter), `3_4` (three-quarters)
- **Settings as attributes**: `background_color`, `text_orientation`, `custom_margin`, `custom_padding`, etc.
- **Builder version tracking**: `_builder_version` attribute on every element
- **Content encoding**: Text content may contain escaped HTML entities, newline placeholders (`%22`, `%91`, `%93`), and occasional base64
- **Global modules**: Referenced via `global_module` attribute pointing to an `et_pb_layout` post
- **Custom CSS fields**: `custom_css_main_element`, `custom_css_before`, `custom_css_after` attributes

Read Divi content via `wordpress_extract_builder_content` with `builder=divi`.

## Target: Gutenberg (Block Editor)

Gutenberg stores content in `post_content` as HTML with block comment delimiters:

```html
<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
  <!-- wp:heading {"level":2} -->
  <h2 class="wp-block-heading">Title Here</h2>
  <!-- /wp:heading -->
  <!-- wp:paragraph -->
  <p>Content text.</p>
  <!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
```

Key Gutenberg specifics:
- Block attributes in opening comment JSON
- Layout blocks: `wp:group`, `wp:columns`, `wp:column`
- Inline styles via `style` attribute in block JSON
- Columns use percentage widths
- Everything lives in `post_content` — no separate meta

Write Gutenberg content via `wordpress_update_page` or `wordpress_update_post` targeting the `content` field.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm Divi is active (theme or plugin) via `wordpress_list_plugins` and `wordpress_get_site_context`.
3. Check WordPress version (6.0+ required, 6.3+ ideal).
4. **Important**: If using Divi theme (not just plugin), note that the user will need an alternative theme post-migration.
5. Scan all content for Divi usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - For each, check builder via `wordpress_get_builder_info`
6. For each Divi page, extract content via `wordpress_extract_builder_content` with `builder=divi`
7. Build an inventory:
   - Total pages/posts using Divi
   - Module types used (frequency count)
   - Specialty sections detected (high complexity)
   - Global modules referenced
   - Third-party Divi modules
   - Content encoding issues found
   - Complexity per page (simple/moderate/complex)

### Phase 2: Migration Plan

Present a plan that sets realistic expectations:

```
## Divi → Gutenberg Migration Plan

### Important Context
Divi and Gutenberg have very different design philosophies. Divi offers
extensive visual customization through its settings panel; Gutenberg
prioritizes clean, semantic content. Expect simpler but faster-loading pages.

If you are using the Divi theme (not just the plugin), you will need a
block-compatible theme (e.g., Twenty Twenty-Four, Astra, Kadence).

### Site Inventory
- Total Divi pages: X
- Total modules to convert: X
- Direct equivalents: X (Y%)
- Approximate equivalents: X (Y%)
- Manual recreation needed: X (Y%)

### Module Mapping Summary
| Divi Module       | Gutenberg Block  | Fidelity     |
|------------------|-----------------|--------------|
| et_pb_text       | wp:paragraph    | Exact        |
| et_pb_image      | wp:image        | Exact        |
| et_pb_blurb      | wp:group combo  | Approximate  |
| et_pb_slider     | wp:group/gallery| Simplified   |
| et_pb_contact    | —               | Manual       |

### Shortcode Parsing Notes
- [Any encoding issues found]
- [Specialty sections that need layout interpretation]
- [Global modules that will be inlined]

### Page-by-Page Plan
1. **[Page Title]** — X modules, [complexity]
2. ...
```

Ask for confirmation:
> Divi → Gutenberg is a significant simplification. Pages will be cleaner but less visually elaborate.
> 1. Migrate all pages
> 2. Migrate specific pages
> 3. Start with a test page (strongly recommended)
> 4. Just keep this plan

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read full Divi content via `wordpress_extract_builder_content` with `builder=divi`
2. Parse the Divi shortcode tree:
   - Identify section/row/column hierarchy
   - Decode any encoded content (HTML entities, percent-encoding)
   - Resolve global module references to inline content
3. Map each module:
   - `et_pb_section` → `<!-- wp:group -->` (with full-width if fullwidth section)
   - `et_pb_row` + `et_pb_column` → `<!-- wp:columns -->` + `<!-- wp:column {"width":"X%"} -->`
   - Column type mapping: `4_4`→100%, `1_2`→50%, `1_3`→33.33%, `2_3`→66.66%, `1_4`→25%, `3_4`→75%
   - `et_pb_text` → `<!-- wp:paragraph -->` (or multiple blocks if content has headings)
   - `et_pb_blurb` → Group containing Image + Heading + Paragraph
   - `et_pb_image` → `<!-- wp:image -->`
   - `et_pb_button` → `<!-- wp:buttons --><!-- wp:button -->`
   - Map background colors to Group block style attributes
   - Flag unmappable modules with `<!-- MIGRATION NOTE: ... -->`
4. Assemble complete block markup
5. Create duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
6. Write to duplicate via `wordpress_update_page` or `wordpress_update_post`
7. Report: modules converted, items flagged, layout changes made

### Phase 4: Post-Migration Verification

1. Summarize all migrations
2. For each migrated page:
   - Link to edit in Gutenberg
   - Flagged items
   - Layout simplification notes
3. Post-migration checklist:
   - [ ] Open each duplicate in block editor — verify blocks parse correctly
   - [ ] Check responsive preview
   - [ ] Verify all images and media
   - [ ] Test links and buttons
   - [ ] Recreate forms with a dedicated forms plugin
   - [ ] Recreate sliders if needed (or use a block-based slider)
   - [ ] Plan theme switch if on Divi theme (do this after all pages are verified)
   - [ ] Check page speed improvement
   - [ ] Review for Divi shortcode remnants in content

## Safety Model

- Read-only analysis first — full content scan before any changes
- Explicit user confirmation required before creating duplicates
- Original Divi pages are never modified or deleted
- All migrated content goes to draft duplicates only
- Never auto-publishes migrated pages
- Creates a snapshot before migration begins (when available)
- Provides clear rollback path (delete duplicates)
- Warns about theme dependency if using Divi theme

## Honest Disclaimer

This skill converts Divi page content to Gutenberg blocks and creates draft duplicates for review.

It cannot:
- Replicate Divi's visual design precision in Gutenberg
- Convert specialty section layouts perfectly
- Migrate contact forms, sliders, or animations
- Handle third-party Divi plugin modules
- Switch your theme for you (if on Divi theme)
- Replace manual review and fine-tuning

It can:
- Convert 60-75% of standard Divi modules to clean blocks
- Extract all text, images, and links from shortcode markup
- Eliminate Divi dependency for simpler pages
- Dramatically improve page load speed
- Parse complex Divi shortcode encoding
- Provide a clear map of manual work needed
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
- `wordpress_find_builder_targets`
- `wordpress_create_page_duplicate`
- `wordpress_create_post_duplicate`
- `wordpress_update_page`
- `wordpress_update_post`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = migrate-divi-to-gutenberg`
- site/version context
- duration and success
- pages migrated, blocks created, modules flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (understand site structure and theme dependency before migrating)
- Internal Link Builder (verify internal links post-migration)
- SEO & AEO Amplifier (verify SEO preservation post-migration)
- Technical Debt Audit (find and clean Divi shortcode remnants)

---

Built by Respira Team
https://respira.press/skills/migrate-divi-to-gutenberg
