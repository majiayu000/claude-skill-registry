---
name: migrate-elementor-to-gutenberg
description: Converts Elementor-built WordPress pages to native Gutenberg blocks. Reads Elementor's JSON widget tree from post meta, maps each widget to its closest core block equivalent, generates a migration plan for approval, and writes clean block markup to the target pages. Use when user says "migrate Elementor to Gutenberg", "drop Elementor", "switch to native blocks", or "rebuild Elementor pages in the block editor".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Elementor to Gutenberg

Converts Elementor-built WordPress pages to native Gutenberg blocks. Reads Elementor's JSON widget tree from post meta, maps each widget to its closest core block equivalent, generates a migration plan for approval, and writes clean block markup to the target pages. Use this skill whenever someone wants to move from Elementor to Gutenberg, eliminate page builder dependencies, go back to native WordPress blocks, or simplify their tech stack by dropping Elementor.

## What This Skill Does

Moving from Elementor to Gutenberg is one of the most common — and most complex — builder migrations. Elementor stores content as a deeply nested JSON tree in `_elementor_data`, while Gutenberg uses HTML comments (`<!-- wp:block -->`) inline with content in `post_content`. Every layout decision Elementor makes with JSON settings must be translated into block attributes, CSS classes, or Group/Columns block structures.

This skill handles that translation systematically: it reads every Elementor widget, finds the right Gutenberg block, maps settings as closely as possible, and flags anything that needs manual attention. The result is clean, dependency-free WordPress content.

**Handles:**
- Section/Column layouts → Group and Columns blocks with appropriate width settings
- Text Editor → Paragraph blocks (preserving inline formatting)
- Heading → Heading block (h1-h6 mapping)
- Image → Image block (with alt text, caption, link)
- Video → Video or Embed block (YouTube/Vimeo detected)
- Button → Buttons block (with link, style, colors)
- Icon List → List block
- Spacer → Spacer block
- Divider → Separator block
- Google Maps → Custom HTML block with embed
- Tabs, Accordion → Group blocks with Details block (WP 6.3+) or HTML fallback
- Image Gallery → Gallery block
- Counter, Progress Bar → HTML or Group block approximations
- Custom HTML → Custom HTML block (direct transfer)
- Responsive visibility → block-level responsive classes (theme-dependent)

**Preserves:**
- All text content, headings, and inline formatting (bold, italic, links)
- Image URLs, alt text, captions, and link targets
- Button labels, URLs, and target attributes
- Color values applied as block-level styles
- Basic spacing via Spacer blocks
- Heading hierarchy (h1-h6)
- List content and structure
- Embedded media URLs

## What This Skill Does NOT Do

- **Complex multi-column layouts** — Elementor allows pixel-level column width control and nested sections. Gutenberg Columns blocks support percentage widths but with less precision. Complex grid layouts may need manual adjustment or a block-based layout plugin.
- **Elementor Pro widgets** — Posts grid, portfolio, price table, price list, flip box, call to action, and similar Pro widgets have no core Gutenberg equivalent. They are flagged for manual recreation.
- **Third-party addon widgets** — Essential Addons, JetElements, Crocoblock widgets cannot be auto-mapped.
- **Dynamic content** — ACF fields, custom loops, and dynamic tags require separate solutions (ACF blocks, custom block patterns, or Query Loop block).
- **Theme Builder templates** — Headers, footers, archive templates are outside page content scope.
- **Advanced animations** — Motion effects, parallax scrolling, entrance animations have no Gutenberg equivalent.
- **Form widgets** — Elementor forms need a forms plugin replacement (WPForms, Gravity Forms, etc.).
- **Popup content** — Elementor popups are not page content and are excluded.
- **Design fidelity** — Gutenberg is intentionally simpler. Expect a cleaner but less visually identical result. This is a feature, not a bug — you are trading design complexity for simplicity and performance.

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Elementor plugin active (to read source content)
- WordPress 6.0+ (for modern block features; 6.3+ recommended for Details block)
- A block-compatible theme (Twenty Twenty-Three, Astra, Kadence, GeneratePress, etc.)
- Read access to scan Elementor content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate elementor to gutenberg"

## Alternative Triggers

- "convert elementor to blocks"
- "switch from elementor to gutenberg"
- "remove elementor dependency"
- "go back to native wordpress"
- "rebuild elementor pages with blocks"
- "elementor to block editor"
- "decommission elementor"

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
- **Nested sections** (Inner Section widget) create sub-layouts within columns

Read Elementor content via `wordpress_extract_builder_content` with `builder=elementor`.

## Target: Gutenberg (Block Editor)

Gutenberg stores content directly in `post_content` as HTML with block comment delimiters:

```html
<!-- wp:group {"layout":{"type":"constrained"}} -->
<div class="wp-block-group">
  <!-- wp:heading {"level":2} -->
  <h2 class="wp-block-heading">Title Here</h2>
  <!-- /wp:heading -->

  <!-- wp:paragraph -->
  <p>Content here with <strong>formatting</strong>.</p>
  <!-- /wp:paragraph -->
</div>
<!-- /wp:group -->
```

Key Gutenberg specifics:
- Block attributes are JSON in the opening comment: `<!-- wp:image {"id":123,"sizeSlug":"large"} -->`
- Layout blocks: `wp:group`, `wp:columns`, `wp:column`
- Style attributes go in the block JSON: `{"style":{"color":{"background":"#fff"},"spacing":{"padding":{"top":"2rem"}}}}`
- No separate meta storage — everything is in `post_content`
- Columns use percentage widths: `<!-- wp:column {"width":"33.33%"} -->`

Write Gutenberg content via `wordpress_update_page` or `wordpress_update_post` targeting the `content` field.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Confirm Elementor is active via `wordpress_list_plugins`.
3. Check WordPress version (6.0+ required, 6.3+ ideal).
4. Identify active theme — note if it is block-theme compatible.
5. Scan all content for Elementor usage:
   - `wordpress_list_pages` and `wordpress_list_posts`
   - For each, check builder via `wordpress_get_builder_info`
6. For each Elementor page, extract content via `wordpress_extract_builder_content` with `builder=elementor`
7. Build an inventory:
   - Total pages/posts using Elementor
   - Widget types used (frequency count)
   - Pro-only widgets detected
   - Third-party addon widgets detected
   - Dynamic tags and global widgets
   - Layout complexity score per page (nesting depth, column configurations)
   - Estimated migration complexity (simple/moderate/complex)

### Phase 2: Migration Plan

Present a detailed plan acknowledging that Gutenberg migration involves the most interpretation:

```
## Elementor → Gutenberg Migration Plan

### Important Context
Gutenberg is intentionally simpler than Elementor. This migration prioritizes
content preservation and clean markup over pixel-perfect layout recreation.
Some design adjustments will be needed post-migration.

### Site Inventory
- Total Elementor pages: X
- Total widgets to convert: X
- Direct block equivalents: X (Y%)
- Approximate equivalents (layout may differ): X (Y%)
- No equivalent — manual recreation needed: X (Y%)

### Widget Mapping Summary
| Elementor Widget | Gutenberg Block | Fidelity |
|-----------------|----------------|----------|
| heading         | wp:heading     | Exact    |
| text-editor     | wp:paragraph   | Exact    |
| image           | wp:image       | Exact    |
| section+columns | wp:group+columns| Close   |
| tabs            | wp:details (6.3+)| Approx |
| form            | —              | Manual   |

### Layout Simplification Notes
- [Specific notes about how complex Elementor layouts will be simplified]
- [Column configurations that will change]
- [Sections that will become Groups]

### Page-by-Page Plan
1. **[Page Title]** — X widgets, [simple/moderate/complex]
   - Direct conversions: X
   - Approximate conversions: X
   - Manual items: X — [details]
2. ...
```

Ask for confirmation:
> This migration will produce cleaner, faster-loading pages but with simpler layouts than Elementor.
> 1. Migrate all pages
> 2. Migrate specific pages
> 3. Start with a test page (recommended for complex sites)
> 4. Just keep this plan

### Phase 3: Page-by-Page Migration

For each approved page:

1. Read full Elementor content via `wordpress_extract_builder_content` with `builder=elementor`
2. Walk the Elementor JSON tree depth-first:
   - Convert Section → `<!-- wp:group -->` with constrained layout
   - Convert Column structures → `<!-- wp:columns -->` and `<!-- wp:column {"width":"X%"} -->`
   - Convert each widget to appropriate block:
     - `heading` → `<!-- wp:heading {"level":N} --><hN>text</hN><!-- /wp:heading -->`
     - `text-editor` → `<!-- wp:paragraph --><p>text</p><!-- /wp:paragraph -->`
     - `image` → `<!-- wp:image {"id":N,"sizeSlug":"large"} --><figure>...</figure><!-- /wp:image -->`
     - `button` → `<!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button -->...<!-- /wp:button --></div><!-- /wp:buttons -->`
   - Map colors and spacing to block-level `style` attributes where possible
   - Convert background images to Group block background or Cover block
   - Flag unmappable widgets with `<!-- MIGRATION NOTE: [widget type] needs manual recreation -->`
3. Assemble complete block markup with proper nesting and closing tags
4. Create a duplicate page via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Write block content to the duplicate via `wordpress_update_page` or `wordpress_update_post`
6. Report: widgets converted, items flagged, known layout differences

### Phase 4: Post-Migration Verification

1. Summarize all migrations:
   - Pages migrated
   - Widgets converted to blocks
   - Items needing manual attention
   - Layout simplifications made
2. For each migrated page, provide:
   - Link to edit the duplicate in Gutenberg
   - Flagged items requiring manual recreation
   - Layout notes (where the Gutenberg version differs from Elementor)
3. Post-migration checklist:
   - [ ] Open each duplicate in block editor — verify blocks are valid
   - [ ] Check responsive preview (tablet/mobile in block editor)
   - [ ] Verify images, links, and media
   - [ ] Recreate flagged widgets manually (forms, sliders, etc.)
   - [ ] Add any needed block patterns or reusable blocks
   - [ ] Consider a forms plugin replacement for Elementor forms
   - [ ] Test interactive elements
   - [ ] Review page speed improvement (should be noticeable)

## Safety Model

- Read-only analysis first — full content scan before any changes
- Explicit user confirmation required before creating any duplicates
- Original Elementor pages are never modified or deleted
- All migrated content goes to draft duplicates only
- Never auto-publishes migrated pages
- Creates a snapshot before migration begins (when available)
- Provides clear rollback path (delete duplicates)
- Warns about significant layout changes before proceeding

## Honest Disclaimer

This skill converts Elementor page content to Gutenberg blocks and creates draft duplicates for review.

It cannot:
- Replicate Elementor's design precision in Gutenberg
- Auto-convert Pro widgets, addon widgets, or forms
- Migrate dynamic content or theme builder templates
- Replace the need for visual review and manual fine-tuning
- Make Gutenberg do things it was not designed for

It can:
- Convert 60-80% of standard Elementor content to clean blocks
- Eliminate your Elementor dependency for simpler pages
- Dramatically improve page load speed (no Elementor CSS/JS overhead)
- Produce clean, standards-compliant WordPress content
- Give you a clear roadmap for what needs manual attention
- Keep your original pages completely untouched

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
- `skill_slug = migrate-elementor-to-gutenberg`
- site/version context
- duration and success
- pages migrated, blocks created, widgets flagged counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (understand site structure before migrating)
- Internal Link Builder (verify internal links post-migration)
- SEO & AEO Amplifier (verify SEO preservation post-migration)
- Technical Debt Audit (clean up Elementor remnants after full migration)

---

Built by Respira Team
https://respira.press/skills/migrate-elementor-to-gutenberg
