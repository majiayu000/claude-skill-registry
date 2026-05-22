---
name: migrate-wpbakery-to-bricks
description: Converts WPBakery Page Builder pages (the legacy ThemeForest-bundled vc_* shortcode format) to Bricks Builder. Parses WPBakery shortcodes from post_content, maps each element to its Bricks equivalent, generates a migration plan for approval, and writes clean Bricks JSON to the target pages. Use when user says "migrate WPBakery to Bricks", "modernize a WPBakery site with Bricks", or "switch from WPBakery to Bricks".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate WPBakery to Bricks

Converts WPBakery Page Builder pages to Bricks Builder. Parses WPBakery's shortcode-based content from post_content, maps each element to its Bricks equivalent, generates a migration plan for approval, and writes clean Bricks JSON to the target pages. Use this skill whenever someone wants to move from WPBakery to Bricks, modernize an older WPBakery site with Bricks, or switch page builders from WPBakery/Visual Composer to Bricks.

## What This Skill Does

WPBakery is one of the most common legacy page builders — it comes bundled with thousands of ThemeForest themes and millions of sites still use it. Moving to Bricks is a significant modernization: from shortcode-based content in `post_content` to clean JSON in `_bricks_page_content_2`, from heavy frontend CSS/JS to Bricks' lightweight rendering, and from an aging interface to a modern visual editor.

This skill handles the format translation — parsing WPBakery's `[vc_*]` shortcodes, decoding its URL encoding and Design Options CSS, and generating proper Bricks JSON with correct element hierarchies and settings.

**Handles:**
- vc_row/vc_column → Bricks Section/Container elements
- vc_column_text → Bricks Text Basic element (parsed for headings, paragraphs)
- vc_single_image → Bricks Image element
- vc_btn/vc_button → Bricks Button element
- vc_video → Bricks Video element
- vc_separator → Bricks Divider element
- vc_empty_space → Bricks spacing (via container padding or dedicated spacer)
- vc_custom_heading → Bricks Heading element
- vc_gallery/vc_images_carousel → Bricks Gallery/Carousel element
- vc_toggle → Bricks Accordion item
- vc_accordion → Bricks Accordion element
- vc_tabs → Bricks Tabs element
- vc_raw_html/vc_raw_js → Bricks Code element
- vc_icon → Bricks Icon element
- vc_gmaps → Bricks Map element
- vc_progress_bar → Bricks Progress Bar element
- vc_row_inner/vc_column_inner → nested Bricks containers
- Design Options CSS → Bricks settings (background, padding, border)
- el_class/el_id → Bricks custom CSS classes and attributes

**Preserves:**
- All text content and HTML formatting
- Image URLs, alt text, captions
- Typography where explicitly set
- Color values from Design Options
- Spacing from Design Options
- Background colors and images
- Button labels, URLs, targets
- Video embed URLs
- Gallery image sets
- CSS classes (el_class) and IDs (el_id)

## What This Skill Does NOT Do

- **Theme-bundled custom elements** — Many ThemeForest themes add custom WPBakery elements (team member, portfolio, testimonial, pricing, etc.). These are theme-specific shortcodes with no Bricks equivalent. They are flagged for manual recreation.
- **WPBakery addons** — Ultimate Addons for WPBakery, Starter Templates, Starter Sites, and other addon plugins add proprietary elements that cannot be auto-mapped.
- **vc_grid/vc_masonry_grid** — Post grid elements with complex queries. These need Bricks' Query Loop or posts element configured manually.
- **Revolution Slider / Layer Slider** — Often bundled with WPBakery themes but are separate plugins outside migration scope.
- **Complex Design Options** — WPBakery encodes CSS in a single attribute string. Background gradients, complex border configurations, and CSS filters may be partially extracted.
- **Frontend editor positioning** — Pixel-precise layouts from WPBakery's frontend editor may need spacing adjustment.
- **Templates** — WPBakery saved templates are not auto-converted to Bricks templates.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- WPBakery Page Builder plugin active (to ensure shortcodes are parseable)
- Bricks theme installed and active (to write target content)
- Read access to scan WPBakery content
- Write access to create duplicates with Bricks content

## Trigger Phrase

- "migrate wpbakery to bricks"

## Alternative Triggers

- "convert wpbakery to bricks"
- "switch from wpbakery to bricks"
- "migrate visual composer to bricks"
- "rebuild wpbakery pages in bricks"
- "move from wpbakery to bricks"
- "replace wpbakery with bricks"
- "modernize visual composer site"

## Source Builder: WPBakery

WPBakery stores content as shortcodes in `post_content`:

```
[vc_row full_width="stretch_row" css=".vc_custom_123{padding:40px;background:#f5f5f5}"]
  [vc_column width="1/2" el_class="custom-class"]
    [vc_column_text]
      <h2>Heading</h2>
      <p>Paragraph content.</p>
    [/vc_column_text]
    [vc_single_image image="456" img_size="large"]
  [/vc_column]
  [vc_column width="1/2"]
    [vc_btn title="Click" style="flat" link="url:https%3A%2F%2Fexample.com||target:_blank"]
  [/vc_column]
[/vc_row]
```

Key WPBakery specifics:
- **Column widths as fractions**: `1/1`, `1/2`, `1/3`, `2/3`, `1/4`, `3/4`, `1/6`, `5/6`
- **Inner rows**: `[vc_row_inner][vc_column_inner]` for nesting
- **CSS attribute**: Encoded Design Options — `.vc_custom_XXXXX{property:value;...}`
- **Link encoding**: `url:https%3A%2F%2F...|title:...|target:_blank|rel:nofollow`
- **Full-width**: `full_width` attribute controls row stretching
- **el_class / el_id**: Custom CSS class and ID attributes
- **Image references**: By attachment ID (not URL)

Read WPBakery content via `wordpress_extract_builder_content` with `builder=wpbakery`.

## Target Builder: Bricks

Bricks stores content in `_bricks_page_content_2` as a JSON array:

```json
[
  { "id": "abc123", "name": "section", "parent": 0, "settings": {...} },
  { "id": "def456", "name": "container", "parent": "abc123", "settings": {...} },
  { "id": "ghi789", "name": "text-basic", "parent": "def456", "settings": { "text": "<p>...</p>" } }
]
```

Key Bricks specifics:
- Elements: `section`, `container`, `heading`, `text-basic`, `image`, `button`, `video`, `icon`
- Parent-child via `parent` field
- IDs are short alphanumeric strings
- Responsive via `_breakpoints`

Write Bricks content via `wordpress_inject_builder_content` with `builder=bricks`.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm WPBakery is active via `wordpress_list_plugins`.
3. Confirm Bricks theme is installed via `wordpress_get_site_context`.
4. Identify active theme — note if it bundles WPBakery and adds custom elements.
5. Scan all content for WPBakery usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - Check builder via `wordpress_get_builder_info`
6. Extract content via `wordpress_extract_builder_content` with `builder=wpbakery`
7. Build inventory:
   - Total WPBakery pages/posts
   - Element types (frequency count)
   - Theme-bundled custom elements (flagged)
   - Addon elements (flagged)
   - Grid/masonry elements (flagged)
   - Design Options complexity
   - Inner row nesting depth
   - Complexity per page

### Phase 2: Migration Plan

```
## WPBakery → Bricks Migration Plan

### Modernization Context
This migration moves your site from legacy shortcode-based content to Bricks'
modern JSON format. Expect significantly faster page loads and a much better
editing experience. Bricks also means switching your theme — plan for header,
footer, and template setup.

### Theme-Bundled Elements
[If applicable]: Your theme ([name]) bundles WPBakery and adds X custom
elements. These cannot be auto-migrated and are flagged below.

### Site Inventory
- Total WPBakery pages: X
- Total elements to convert: X
- Auto-convertible: X (Y%)
- Manual attention: X (Y%)

### Element → Bricks Mapping
| WPBakery Element    | Bricks Element | Status |
|--------------------|---------------|--------|
| vc_column_text     | text-basic    | Auto   |
| vc_single_image    | image         | Auto   |
| vc_custom_heading  | heading       | Auto   |
| vc_btn             | button        | Auto   |
| vc_gallery         | gallery       | Auto   |
| vc_accordion       | accordion     | Auto   |
| vc_tabs            | tabs          | Auto   |
| vc_toggle          | accordion     | Auto   |
| vc_grid            | —             | Manual |
| [theme element]    | —             | Manual |

### Design Options Extraction
- Simple Design Options (color + padding): X pages — fully extracted
- Complex Design Options (gradients, borders): X pages — partially extracted

### Page-by-Page Plan
1. **[Page Title]** — X elements, [complexity]
2. ...
```

Ask for confirmation:
> Ready to modernize? Your WPBakery pages stay untouched — I'll create Bricks duplicates.
> 1. Migrate all pages
> 2. Migrate specific pages
> 3. Start with a test page (recommended for theme-bundled WPBakery sites)
> 4. Just keep this plan

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read WPBakery content via `wordpress_extract_builder_content` with `builder=wpbakery`
2. Parse the shortcode tree:
   - Build vc_row → vc_column → element hierarchy
   - Handle vc_row_inner/vc_column_inner nesting
   - Decode Design Options CSS from `css` attribute
   - Decode link URLs from WPBakery's encoding format
   - Resolve image attachment IDs
3. Generate Bricks JSON array:
   - `vc_row` → `section` element (check `full_width` for layout mode)
   - `vc_column` → `container` element with flex width
     - Convert fractions: `1/2`→50%, `1/3`→33.33%, `2/3`→66.66%, `1/4`→25%, etc.
   - Map each element:
     - `vc_column_text` → `text-basic` (preserve HTML, or split into heading + text-basic)
     - `vc_single_image` → `image` (resolve attachment ID to URL, map alt, size)
     - `vc_btn` → `button` (decode URL, map label, style, color)
     - `vc_custom_heading` → `heading` (map text, tag, alignment)
     - `vc_gallery` → `gallery` (resolve image IDs)
     - `vc_accordion` → `accordion` (map items with titles and content)
     - `vc_tabs` → `tabs` (map tab titles and content)
   - Apply Design Options: background → settings background, padding → settings padding
   - Apply el_class → Bricks CSS classes setting
   - Generate unique IDs and proper parent references
   - Flag unmappable elements
4. Create duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Write Bricks JSON via `wordpress_inject_builder_content` with `builder=bricks`
6. Report status

### Phase 4: Post-Migration Verification

1. Summarize migrations:
   - Pages migrated, elements created, items flagged
2. For each migrated page:
   - Link to Bricks editor
   - Flagged items
   - Design Options notes (what was extracted vs. simplified)
3. Post-migration checklist:
   - [ ] Open each duplicate in Bricks editor
   - [ ] Verify section/container layout structure
   - [ ] Check column widths match intended proportions
   - [ ] Verify images load (attachment ID resolution)
   - [ ] Test button links (URL decoding)
   - [ ] Check responsive views
   - [ ] Recreate theme-bundled custom elements
   - [ ] Set up Bricks templates for header/footer/archive
   - [ ] Review gallery and carousel elements
   - [ ] Compare with WPBakery original
   - [ ] Celebrate the speed improvement

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

This skill converts WPBakery page content to Bricks format and creates draft duplicates for review.

It cannot:
- Convert theme-bundled custom WPBakery elements
- Migrate WPBakery addon plugin elements
- Perfectly extract all Design Options CSS
- Convert post grids to Bricks Query Loop automatically
- Handle Revolution Slider or other bundled plugins
- Replace visual QA and manual review

It can:
- Convert 75-90% of standard WPBakery elements to Bricks equivalents
- Parse and decode WPBakery's CSS and URL encoding
- Handle nested inner row/column structures
- Resolve image attachment IDs to proper URLs
- Modernize legacy content to Bricks' clean JSON format
- Dramatically improve page load performance
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
- `skill_slug = migrate-wpbakery-to-bricks`
- site/version context
- duration and success
- pages migrated, elements created, elements flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (audit site structure and theme dependencies before migrating)
- Internal Link Builder (verify links post-migration)
- SEO & AEO Amplifier (verify SEO post-migration)
- Technical Debt Audit (find WPBakery shortcode remnants and legacy theme code)

---

Built by Respira Team
https://respira.press/skills/migrate-wpbakery-to-bricks
