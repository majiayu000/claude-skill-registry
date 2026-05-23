---
name: migrate-wpbakery-to-gutenberg
description: Converts WPBakery Page Builder (formerly Visual Composer) pages to native Gutenberg blocks. Parses WPBakery shortcodes from post_content, maps each element to its closest core block equivalent, generates a migration plan for approval, and writes clean block markup to the target pages. Use when user says "migrate WPBakery to Gutenberg", "drop WPBakery for native blocks", or "modernize a legacy WPBakery WordPress site".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate WPBakery to Gutenberg

Converts WPBakery Page Builder (formerly Visual Composer) pages to native Gutenberg blocks. Parses WPBakery's shortcode-based content from post_content, maps each element to its closest core block equivalent, generates a migration plan for approval, and writes clean block markup to the target pages. Use this skill whenever someone wants to move from WPBakery to Gutenberg, eliminate the WPBakery dependency, switch to native blocks, or modernize an older WordPress site still running WPBakery.

## What This Skill Does

WPBakery is one of the oldest and most widely-installed WordPress page builders — millions of sites still run it. It stores content as shortcodes in `post_content` using the `[vc_*]` prefix. The good news: WPBakery's shortcode structure is relatively straightforward compared to Divi's encoding complexities. The challenge: many WPBakery sites are older and may use deprecated elements, custom shortcodes from themes, or VC-specific plugins that add nonstandard elements.

This skill parses the WPBakery shortcode tree, extracts content and settings, and generates equivalent Gutenberg blocks. The result is clean, modern WordPress content free from shortcode dependencies.

**Handles:**
- vc_row/vc_column → Columns and Column blocks
- vc_column_text → Paragraph blocks (preserving HTML)
- vc_single_image → Image block
- vc_btn/vc_button → Buttons block
- vc_video → Video or Embed block
- vc_separator/vc_text_separator → Separator block
- vc_empty_space → Spacer block
- vc_row_inner/vc_column_inner → nested Columns blocks
- vc_custom_heading → Heading block
- vc_gallery/vc_images_carousel → Gallery block
- vc_toggle → Details block (WP 6.3+)
- vc_accordion/vc_accordion_tab → Group with Details blocks
- vc_tabs/vc_tab → Group blocks with headings
- vc_raw_html/vc_raw_js → Custom HTML block
- vc_icon → Paragraph with icon (or HTML block)
- vc_gmaps → Custom HTML block with embed
- vc_progress_bar → HTML approximation
- vc_wp_* widgets → corresponding WordPress widget blocks

**Preserves:**
- All text content and HTML formatting within vc_column_text
- Image URLs, alt text, link targets
- Heading text and hierarchy
- Button labels, URLs, and basic styles
- Video embed URLs
- Gallery image collections
- Code/HTML block contents
- CSS classes applied via `el_class` attribute
- Custom element IDs via `el_id` attribute

## What This Skill Does NOT Do

- **Theme-bundled WPBakery elements** — Many themes add custom WPBakery elements (portfolio grids, team members, testimonial carousels, etc.). These are theme-specific and cannot be auto-mapped. They are flagged for manual recreation.
- **WPBakery addons** — Ultimate Addons for WPBakery, Starter Templates, etc. add proprietary shortcodes that are flagged, not converted.
- **vc_grid/vc_masonry_grid** — Post grid elements with complex query settings need manual recreation using Query Loop block or a posts plugin.
- **Design options** — WPBakery's Design Options panel (accessed via `css` attribute containing encoded CSS) stores background, border, padding as a single encoded string. Basic properties are extracted; complex combinations may be simplified.
- **Frontend editor layouts** — Some WPBakery designs rely on the frontend editor's pixel-precise positioning which has no block equivalent.
- **WooCommerce elements** — vc_wp_product, cart, and checkout elements need WooCommerce blocks.
- **Revolution Slider, Layer Slider** — Often bundled with WPBakery themes but are separate plugins.
- **Templates** — WPBakery saved templates are not migrated as reusable blocks automatically.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- WPBakery Page Builder plugin active (to ensure shortcodes render/parse)
- WordPress 6.0+ (6.3+ recommended for Details block)
- A block-compatible theme (often needed since WPBakery sites tend to run older themes)
- Read access to scan WPBakery content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate wpbakery to gutenberg"

## Alternative Triggers

- "convert wpbakery to blocks"
- "switch from wpbakery to gutenberg"
- "migrate visual composer to gutenberg"
- "remove wpbakery"
- "rebuild wpbakery pages with blocks"
- "wpbakery to block editor"
- "decommission wpbakery"
- "get rid of visual composer"

## Source Builder: WPBakery

WPBakery stores content as shortcodes in `post_content`:

```
[vc_row full_width="stretch_row" css=".vc_custom_123{padding-top:40px}"]
  [vc_column width="1/2" el_class="my-class"]
    [vc_column_text]
      <h2>Welcome</h2>
      <p>Content with <strong>formatting</strong>.</p>
    [/vc_column_text]
    [vc_single_image image="456" img_size="large" alignment="center"]
  [/vc_column]
  [vc_column width="1/2"]
    [vc_btn title="Learn More" style="flat" color="primary" link="url:https%3A%2F%2Fexample.com"]
  [/vc_column]
[/vc_row]
```

Key WPBakery specifics:
- **Row/column structure**: `[vc_row]` → `[vc_column width="1/2"]` → elements
- **Column widths as fractions**: `1/1`, `1/2`, `1/3`, `2/3`, `1/4`, `3/4`, `1/6`, `5/6`
- **Inner rows**: `[vc_row_inner][vc_column_inner]` for nested layouts
- **CSS attribute**: Encoded CSS from Design Options panel — e.g., `css=".vc_custom_12345{background-color:#f5f5f5;padding:20px}"`
- **Link encoding**: URLs in button/link elements use percent-encoding — `url:https%3A%2F%2F...||target:_blank`
- **Full-width modes**: `full_width` attribute: `stretch_row`, `stretch_row_content`, `stretch_row_content_no_spaces`
- **Element classes**: `el_class` for custom CSS classes, `el_id` for IDs
- **Templates**: Saved as separate post type, referenced by ID

Read WPBakery content via `wordpress_extract_builder_content` with `builder=wpbakery`.

## Target: Gutenberg (Block Editor)

Gutenberg stores content in `post_content` as HTML with block delimiters:

```html
<!-- wp:columns -->
<div class="wp-block-columns">
  <!-- wp:column {"width":"50%"} -->
  <div class="wp-block-column" style="flex-basis:50%">
    <!-- wp:heading {"level":2} -->
    <h2 class="wp-block-heading">Welcome</h2>
    <!-- /wp:heading -->
    <!-- wp:paragraph -->
    <p>Content with <strong>formatting</strong>.</p>
    <!-- /wp:paragraph -->
  </div>
  <!-- /wp:column -->
</div>
<!-- /wp:columns -->
```

Key Gutenberg specifics:
- Block attributes in opening comment JSON
- Column widths as percentages
- Inline styles via `style` attribute
- Everything in `post_content`

Write Gutenberg content via `wordpress_update_page` or `wordpress_update_post` targeting the `content` field.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm WPBakery is active via `wordpress_list_plugins`.
3. Check WordPress version (6.0+ required, 6.3+ ideal).
4. Identify active theme — note if it bundles WPBakery and adds custom elements.
5. Scan all content for WPBakery usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - Check builder via `wordpress_get_builder_info`
6. Extract WPBakery content via `wordpress_extract_builder_content` with `builder=wpbakery`
7. Build inventory:
   - Total pages/posts using WPBakery
   - Element types used (frequency count)
   - Theme-specific custom elements (flagged)
   - Third-party addon elements (flagged)
   - vc_grid/masonry elements (flagged)
   - Design Options CSS complexity
   - Complexity per page (simple/moderate/complex)
   - Encoded links that need decoding

### Phase 2: Migration Plan

```
## WPBakery → Gutenberg Migration Plan

### Site Context
WPBakery sites are often older WordPress installations. Consider this migration
as a modernization opportunity — not just a builder swap.

### Theme Note
[If theme bundles WPBakery]: Your theme ([theme name]) bundles WPBakery
and likely adds custom elements. These theme-specific elements (X found)
will need manual recreation. Consider whether this theme should also
be updated to a modern block theme.

### Site Inventory
- Total WPBakery pages: X
- Total elements to convert: X
- Direct block equivalents: X (Y%)
- Approximate equivalents: X (Y%)
- Manual recreation needed: X (Y%)

### Element Mapping Summary
| WPBakery Element    | Gutenberg Block  | Fidelity  |
|--------------------|-----------------|-----------|
| vc_column_text     | wp:paragraph    | Exact     |
| vc_single_image    | wp:image        | Exact     |
| vc_custom_heading  | wp:heading      | Exact     |
| vc_btn             | wp:buttons      | Close     |
| vc_row/vc_column   | wp:columns      | Close     |
| vc_gallery         | wp:gallery      | Close     |
| vc_toggle          | wp:details      | Close     |
| vc_grid            | wp:query        | Manual    |
| [theme element]    | —               | Manual    |

### Design Options Analysis
- Pages with simple Design Options: X (colors and padding — auto-mapped)
- Pages with complex Design Options: X (gradients, borders — partially mapped)

### Page-by-Page Plan
1. **[Page Title]** — X elements, [complexity]
2. ...
```

Ask for confirmation:
> WPBakery → Gutenberg is a modernization step. Pages will be cleaner and faster.
> 1. Migrate all pages
> 2. Migrate specific pages
> 3. Start with a test page (recommended for sites with theme-bundled elements)
> 4. Just keep this plan

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read WPBakery content via `wordpress_extract_builder_content` with `builder=wpbakery`
2. Parse the shortcode tree:
   - Identify vc_row → vc_column → element hierarchy
   - Decode CSS from Design Options attribute
   - Decode link URLs from WPBakery's percent-encoding format
   - Handle vc_row_inner/vc_column_inner nesting
3. Map each element:
   - `vc_row` → `<!-- wp:columns -->` (check `full_width` for alignment)
   - `vc_column` → `<!-- wp:column {"width":"X%"} -->` (convert fractions: 1/2→50%, 1/3→33.33%, etc.)
   - `vc_column_text` → Parse inner HTML, split into appropriate blocks:
     - `<h2>` → `<!-- wp:heading {"level":2} -->`
     - `<p>` → `<!-- wp:paragraph -->`
     - `<ul>/<ol>` → `<!-- wp:list -->`
   - `vc_single_image` → `<!-- wp:image {"id":N,"sizeSlug":"large"} -->`
   - `vc_btn` → `<!-- wp:buttons -->` (decode URL, map style/color)
   - `vc_custom_heading` → `<!-- wp:heading -->` (extract tag, text, alignment)
   - Map Design Options CSS to block style attributes where possible
   - Apply `el_class` as `className` in block attributes
   - Apply `el_id` as `anchor` in block attributes
   - Flag unmappable elements with `<!-- MIGRATION NOTE: ... -->`
4. Assemble block markup
5. Create duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
6. Write via `wordpress_update_page` or `wordpress_update_post`
7. Report: elements converted, flagged, layout notes

### Phase 4: Post-Migration Verification

1. Summarize all migrations
2. For each migrated page:
   - Link to edit in Gutenberg
   - Flagged items
   - Design Options settings that were simplified
3. Post-migration checklist:
   - [ ] Open each duplicate in block editor — verify all blocks are valid
   - [ ] Check that vc_column_text HTML parsed into correct block types
   - [ ] Verify images (check that image IDs still resolve)
   - [ ] Test all buttons (decoded URLs working correctly)
   - [ ] Check responsive preview
   - [ ] Recreate theme-bundled custom elements manually
   - [ ] Set up any needed block patterns for repeated layouts
   - [ ] Consider theme modernization if using an older WPBakery-bundled theme
   - [ ] Test page speed (expect significant improvement)
   - [ ] Search for any remaining vc_ shortcode remnants

## Safety Model

- Read-only analysis first — full content scan before any changes
- Explicit user confirmation required before creating duplicates
- Original WPBakery pages are never modified or deleted
- All migrated content goes to draft duplicates only
- Never auto-publishes migrated pages
- Creates a snapshot before migration begins (when available)
- Provides clear rollback path (delete duplicates)
- Warns about theme-bundled element dependencies

## Honest Disclaimer

This skill converts WPBakery page content to Gutenberg blocks and creates draft duplicates for review.

It cannot:
- Convert theme-specific custom WPBakery elements
- Migrate WPBakery addon plugin elements
- Perfectly translate complex Design Options CSS
- Convert post grids (vc_grid) to Query Loop automatically
- Handle Revolution Slider or other bundled plugins
- Replace visual review and manual adjustment

It can:
- Convert 70-85% of standard WPBakery elements to clean blocks
- Parse and decode WPBakery's URL encoding and CSS attributes
- Handle nested row/column structures including inner rows
- Split vc_column_text HTML into proper individual blocks
- Dramatically reduce page weight and load time
- Modernize older WordPress sites
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
- `skill_slug = migrate-wpbakery-to-gutenberg`
- site/version context
- duration and success
- pages migrated, blocks created, elements flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (audit site structure and theme before modernizing)
- Internal Link Builder (verify links post-migration)
- SEO & AEO Amplifier (verify SEO post-migration)
- Technical Debt Audit (find WPBakery shortcode remnants and outdated theme code)

---

Built by Respira Team
https://respira.press/skills/migrate-wpbakery-to-gutenberg
