---
name: migrate-visual-composer-to-gutenberg
description: Full-site migration from Visual Composer Website Builder (the modern VCV format) to the WordPress block editor (Gutenberg). Audits every VCV page, maps elements to native block equivalents, builds a migration plan for approval, and converts pages to native block markup via duplicates so the live site stays untouched. Use when user says "migrate Visual Composer to Gutenberg", "switch from VCV to blocks", or "convert Visual Composer pages to the block editor".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Visual Composer to Gutenberg

Full-site migration from Visual Composer (WPBakery) to the WordPress block editor (Gutenberg). Audits every Visual Composer page, maps elements to their Gutenberg block equivalents, builds a migration plan for approval, and executes page-by-page conversion into native block markup — all through duplicates so your live site stays untouched. Use this skill whenever someone mentions migrating from Visual Composer to Gutenberg, switching from WPBakery to blocks, converting Visual Composer pages to the block editor, or moving away from Visual Composer to native WordPress.

## What This Skill Does

Visual Composer (now WPBakery Page Builder in its classic form, and Visual Composer Website Builder in its newer form) stores content in post_meta using VCV's custom JSON format. It has been one of the most widely-used WordPress page builders, bundled with thousands of themes. Gutenberg uses a flat block structure in `post_content` with HTML comment delimiters. The migration is moderate: Visual Composer's row/column grid and standard elements translate to Gutenberg, but the ecosystem of third-party VC add-ons and theme-bundled custom elements is vast and varied.

This skill reads every Visual Composer page, extracts the builder content, translates each element to its Gutenberg block equivalent, and writes the result to duplicate pages in native block markup — giving you a complete parallel version of your site to review before going live.

**Handles:**
- vc_row → Group block mapping
- vc_column → Columns/Column block mapping
- vc_column_text → Paragraph/Heading blocks
- vc_single_image → Image block
- vc_btn / vc_button → Buttons/Button block
- vc_video → Video/Embed block
- vc_separator / vc_text_separator → Separator block
- vc_raw_html → Custom HTML block
- vc_empty_space → Spacer block
- vc_custom_heading → Heading block
- vc_row_inner / vc_column_inner → nested Columns blocks
- vc_toggle (FAQ-style) → basic heading + paragraph (flagged for Details block)
- vc_tabs / vc_accordion → basic content fallback (flagged for manual enhancement)

## What This Skill Does NOT Do

- Migrate Visual Composer's Design Options (box shadows, borders, gradients) 1:1 — Gutenberg has different styling capabilities
- Convert third-party VC add-on elements (Ultimate Addons, Starter Sites, theme-specific elements) — flagged for manual handling
- Migrate Visual Composer's template library — must be rebuilt in Gutenberg
- Convert WPBakery's frontend editor custom CSS — must be moved to theme/Additional CSS
- Handle the newer Visual Composer Website Builder (vcwb) — this skill targets the classic VCV/WPBakery format
- Replicate VC's parallax backgrounds or scroll effects — Gutenberg has limited support
- Guarantee pixel-perfect visual parity — different rendering approaches

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Visual Composer / WPBakery active on the source site
- Read access to scan Visual Composer content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate visual composer to gutenberg"

## Alternative Triggers

- "convert visual composer to blocks"
- "switch from wpbakery to gutenberg"
- "move visual composer to block editor"
- "replace wpbakery with gutenberg"
- "visual composer to wordpress blocks"
- "migrate wpbakery to native wordpress"
- "convert vc to gutenberg"

## Builder Technical Context

**Source: Visual Composer**
- Content stored in post_meta using VCV's custom JSON format
- Shortcode-based structure in classic mode: `[vc_row][vc_column][vc_column_text]...[/vc_column_text][/vc_column][/vc_row]`
- Read via `wordpress_extract_builder_content` with `builder=visual-composer`
- Elements: `vc_row`, `vc_column`, `vc_column_text`, `vc_single_image`, `vc_btn`, `vc_video`, `vc_separator`, `vc_raw_html`, `vc_empty_space`, `vc_custom_heading`, `vc_toggle`, `vc_tabs`, `vc_accordion`, `vc_row_inner`, `vc_column_inner`, etc.

**Target: Gutenberg (Block Editor)**
- Content stored in `post_content` as HTML with block comment delimiters
- Format: `<!-- wp:paragraph --><p>Text</p><!-- /wp:paragraph -->`
- Write via standard WordPress content tools (`wordpress_update_page` / `wordpress_update_post`)
- Core blocks: `paragraph`, `heading`, `image`, `buttons`, `columns`, `group`, `html`, `video`, `separator`, `spacer`, `embed`, etc.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Detect Visual Composer presence via `wordpress_get_builder_info` or `wordpress_list_plugins`.
3. Inventory all Visual Composer content:
   - `wordpress_list_pages` and `wordpress_list_posts` — identify all content
   - `wordpress_find_builder_targets` with `builder=visual-composer` — find VC-managed pages
4. For each VC page, extract content:
   - `wordpress_extract_builder_content` with `builder=visual-composer`
   - Catalog: element types used, nesting depth, third-party elements, Design Options usage, custom CSS
5. Produce an **Audit Report**:
   - Total pages/posts using Visual Composer
   - Element type frequency (how many rows, columns, text blocks, images, etc.)
   - Third-party element inventory (elements not in core VC)
   - Complexity flags (nested rows, custom CSS, parallax, third-party add-ons)
   - Estimated migration difficulty per page (simple / moderate / complex)

### Phase 2: Migration Plan

Present a structured migration plan:

```
## Visual Composer → Gutenberg Migration Plan

### Site Overview
- Total Visual Composer pages: X
- Simple pages (direct mapping): X
- Moderate pages (some manual review needed): X
- Complex pages (significant manual work): X

### Element Mapping
| VC Element | Gutenberg Block | Notes |
|---|---|---|
| vc_row | Group | Container mapping |
| vc_column | Columns / Column | Width ratios preserved where possible |
| vc_column_text | Paragraph / Heading | Rich text parsed into blocks |
| vc_single_image | Image | Direct mapping |
| vc_btn | Buttons > Button | Wrapped in container |
| vc_empty_space | Spacer | Height preserved |
| vc_raw_html | Custom HTML | Direct mapping |
| vc_tabs | [MANUAL] | Content migrated, tabs need plugin |
| ... | ... | ... |

### Migration Order
1. [Page Title] — Simple — estimated 2 min
2. [Page Title] — Moderate — estimated 5 min
...

### Items Requiring Manual Attention
- [Page X] — Ultimate Addons carousel (no core equivalent)
- [Page Y] — Theme-specific VC element
- [Page Z] — Custom CSS in Design Options
- VC template library — must be rebuilt in Gutenberg
```

Then ask:

> Here's the migration plan. Would you like me to:
> 1. Migrate all pages (creates duplicates for review)
> 2. Migrate only simple pages first
> 3. Migrate specific pages you choose
> 4. Just keep this as a reference — no changes

Wait for explicit confirmation before proceeding.

### Phase 3: Page-by-Page Migration

For each approved page:

1. Extract Visual Composer content via `wordpress_extract_builder_content` with `builder=visual-composer`
2. Map each VC element to Gutenberg blocks:
   - vc_row → `<!-- wp:group -->` blocks
   - vc_column → `<!-- wp:columns -->` with `<!-- wp:column -->` children (map width attributes)
   - vc_column_text → Parse rich text into `<!-- wp:paragraph -->` and `<!-- wp:heading -->` blocks
   - vc_single_image → `<!-- wp:image -->` with src, alt, caption
   - vc_btn → `<!-- wp:buttons -->` wrapper with `<!-- wp:button -->` child
   - vc_video → `<!-- wp:embed -->` block with video URL
   - vc_separator → `<!-- wp:separator -->` block
   - vc_empty_space → `<!-- wp:spacer -->` block with height
   - vc_raw_html → `<!-- wp:html -->` block
   - vc_custom_heading → `<!-- wp:heading -->` block with level and alignment
   - vc_row_inner/vc_column_inner → nested `<!-- wp:columns -->` blocks
   - Preserve text content, image URLs, link targets
   - Flag unmappable elements with `<!-- wp:paragraph --><p>[MIGRATION NOTE: ...]</p><!-- /wp:paragraph -->`
3. Assemble the complete Gutenberg block markup
4. Create a duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Update the duplicate's `post_content` with the Gutenberg markup via `wordpress_update_page` or `wordpress_update_post`
6. Log the migration result (success, warnings, manual review items)

### Phase 4: Post-Migration Verification

1. Summarize all migrated pages with status:
   - Clean migrations (no issues)
   - Migrations with warnings (flagged items needing review)
   - Failed migrations (if any)
2. List all manual review items:
   - Third-party VC add-on elements that need manual replacement
   - Tabs/Accordions that may benefit from a block plugin
   - Design Options CSS that needs to be moved to theme/Additional CSS
   - Parallax backgrounds that need alternative implementation
   - VC template library items to rebuild
3. Provide review instructions:
   - Where to find duplicates in WordPress admin
   - How to preview pages in the block editor
   - How to delete duplicates if not wanted

## Safety Model

- Read-only analysis first — full Visual Composer content audit before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published Visual Composer content
- Never auto-publishes duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all original Visual Composer content untouched

## Honest Disclaimer

This skill converts Visual Composer page structures to Gutenberg block markup and creates duplicates for review.

It cannot:
- Guarantee pixel-perfect visual parity between builders
- Migrate third-party VC add-on elements automatically
- Convert Design Options CSS to Gutenberg styles
- Handle the newer Visual Composer Website Builder format
- Replace a thorough manual QA pass on every page

It can:
- Map 70-85% of core Visual Composer elements to Gutenberg blocks
- Preserve content, images, links, and basic layout structure
- Handle nested row/column structures
- Move you off a legacy builder dependency to native WordPress
- Save days of manual rebuild work
- Identify exactly what needs manual attention

## Tooling

**Core WordPress tools**
- `wordpress_get_site_context`
- `wordpress_get_builder_info`
- `wordpress_list_pages`
- `wordpress_list_posts`
- `wordpress_list_plugins`
- `wordpress_find_builder_targets`
- `wordpress_extract_builder_content`
- `wordpress_create_page_duplicate`
- `wordpress_create_post_duplicate`
- `wordpress_update_page`
- `wordpress_update_post`
- `wordpress_read_page`
- `wordpress_read_post`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = migrate-visual-composer-to-gutenberg`
- site/version context
- duration and success
- pages audited, pages migrated, warnings count
- tools used

Never block user flow on telemetry failure.

## Related Skills

- WordPress Site DNA (understand site structure before migrating)
- Technical Debt Audit (clean up before or after migration)
- SEO & AEO Amplifier (verify SEO preservation post-migration)

---

Built by Respira Team
https://respira.press/skills/migrate-visual-composer-to-gutenberg
