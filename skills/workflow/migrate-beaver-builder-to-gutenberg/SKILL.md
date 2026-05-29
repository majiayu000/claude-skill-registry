---
name: migrate-beaver-builder-to-gutenberg
description: Full-site migration from Beaver Builder to the WordPress block editor (Gutenberg). Audits every Beaver Builder page, maps modules to native block equivalents, builds a migration plan for approval, and converts pages to native block markup via duplicates so the live site stays untouched. Use when user says "migrate Beaver Builder to Gutenberg", "switch from Beaver Builder to blocks", "convert Beaver Builder pages to the block editor", or "move from Beaver Builder to native WordPress".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Beaver Builder to Gutenberg

Full-site migration from Beaver Builder to the WordPress block editor (Gutenberg). Audits every Beaver Builder page, maps modules to their Gutenberg block equivalents, builds a migration plan for approval, and executes page-by-page conversion into native block markup — all through duplicates so your live site stays untouched. Use this skill whenever someone mentions migrating from Beaver Builder to Gutenberg, switching from Beaver Builder to blocks, converting Beaver Builder pages to the block editor, or moving away from Beaver Builder to native WordPress.

## What This Skill Does

Beaver Builder uses a module-based architecture with rows, columns, and modules stored in `_fl_builder_data` and `_fl_builder_data_settings`. Gutenberg uses a flat block structure in `post_content` with HTML comments as block delimiters. The architectural gap is moderate — Beaver Builder's row/column grid must be translated to Gutenberg's Group, Columns, and Column blocks, while individual modules map to core blocks.

This skill reads every Beaver Builder page, extracts the module structure, translates each row/column/module to its Gutenberg block equivalent, and writes the result to duplicate pages in native block markup — giving you a complete parallel version of your site to review before going live.

**Handles:**
- Row → Group block mapping
- Column layouts → Columns/Column block mapping
- Text Editor module → Paragraph/Heading blocks
- Photo module → Image block
- Button module → Buttons/Button block
- Video module → Video/Embed block
- HTML module → Custom HTML block
- Heading module → Heading block
- Icon/Icon Group modules → basic equivalents
- Separator module → Separator block
- Content slider → basic markup (flagged for enhancement)
- Call to Action module → Group + Heading + Paragraph + Button blocks

## What This Skill Does NOT Do

- Migrate Beaver Builder's saved rows/modules library — these are separate entities
- Convert Beaver Themer layouts (headers, footers, archives, parts) — these must be rebuilt as block template parts or theme templates
- Replicate exact Beaver Builder animations/effects — Gutenberg has limited animation support
- Migrate advanced modules from third-party Beaver Builder add-ons (PowerPack, UABB, etc.) — flagged for manual handling
- Preserve exact column width percentages in all cases — Gutenberg columns have different width constraints
- Guarantee pixel-perfect visual parity — the block editor renders differently than Beaver Builder

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Beaver Builder active on the source site
- Read access to scan Beaver Builder content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate beaver builder to gutenberg"

## Alternative Triggers

- "convert beaver builder to blocks"
- "switch from beaver builder to gutenberg"
- "move beaver builder to block editor"
- "replace beaver builder with gutenberg"
- "beaver builder to wordpress blocks"
- "migrate bb to gutenberg"

## Builder Technical Context

**Source: Beaver Builder**
- Content stored in post_meta keys `_fl_builder_data` and `_fl_builder_data_settings`
- Module-based structure with rows → columns → modules hierarchy
- Read via `wordpress_extract_builder_content` with `builder=beaver` or `builder=beaver-builder`
- Module types: `rich-text`, `photo`, `button`, `heading`, `html`, `video`, `icon`, `separator`, `callout`, `cta`, `numbers`, `content-slider`, etc.

**Target: Gutenberg (Block Editor)**
- Content stored in `post_content` as HTML with block comment delimiters
- Format: `<!-- wp:paragraph --><p>Text</p><!-- /wp:paragraph -->`
- Write via standard WordPress content tools (`wordpress_update_page` / `wordpress_update_post`)
- Core blocks: `paragraph`, `heading`, `image`, `buttons`, `columns`, `group`, `html`, `video`, `separator`, `embed`, etc.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Detect Beaver Builder presence via `wordpress_get_builder_info` or `wordpress_list_plugins`.
3. Inventory all Beaver Builder content:
   - `wordpress_list_pages` and `wordpress_list_posts` — identify all content
   - `wordpress_find_builder_targets` with `builder=beaver` — find BB-managed pages
4. For each BB page, extract content:
   - `wordpress_extract_builder_content` with `builder=beaver`
   - Catalog: module types used, row/column structures, custom CSS, third-party modules, saved rows/modules referenced
5. Produce an **Audit Report**:
   - Total pages/posts using Beaver Builder
   - Module type frequency (how many text editors, photos, buttons, etc.)
   - Column layout patterns (common row structures)
   - Complexity flags (third-party modules, Beaver Themer, custom CSS, animations)
   - Estimated migration difficulty per page (simple / moderate / complex)

### Phase 2: Migration Plan

Present a structured migration plan:

```
## Beaver Builder → Gutenberg Migration Plan

### Site Overview
- Total Beaver Builder pages: X
- Simple pages (direct mapping): X
- Moderate pages (some manual review needed): X
- Complex pages (significant manual work): X

### Module Mapping
| BB Module | Gutenberg Block | Notes |
|---|---|---|
| Text Editor | Paragraph / Heading | Content parsed into appropriate blocks |
| Photo | Image | Direct mapping |
| Button | Buttons > Button | Wrapped in Buttons container |
| Row (2 col) | Columns (2 col) | Width ratios preserved where possible |
| ... | ... | ... |

### Migration Order
1. [Page Title] — Simple — estimated 2 min
2. [Page Title] — Moderate — estimated 5 min
...

### Items Requiring Manual Attention
- [Page X] — PowerPack module (no core block equivalent)
- [Page Y] — Content slider (basic fallback only)
- Beaver Themer layouts — must be rebuilt as block templates
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

1. Extract Beaver Builder content via `wordpress_extract_builder_content` with `builder=beaver`
2. Map the row/column/module hierarchy to Gutenberg blocks:
   - Rows → `<!-- wp:group -->` blocks
   - Columns → `<!-- wp:columns -->` with `<!-- wp:column -->` children
   - Text Editor → Parse rich text into `<!-- wp:paragraph -->` and `<!-- wp:heading -->` blocks
   - Photo → `<!-- wp:image -->` with src, alt, caption
   - Button → `<!-- wp:buttons -->` wrapper with `<!-- wp:button -->` child
   - HTML → `<!-- wp:html -->` block
   - Preserve text content, image URLs, link targets, heading levels
   - Flag any unmappable modules with `<!-- wp:paragraph --><p>[MIGRATION NOTE: ...]</p><!-- /wp:paragraph -->`
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
   - Third-party modules that need manual replacement
   - Content sliders or advanced layouts that need enhancement
   - Custom CSS that needs to be moved to theme/Additional CSS
   - Beaver Themer layouts that need separate rebuilding
3. Provide review instructions:
   - Where to find duplicates in WordPress admin
   - How to preview pages in the block editor
   - How to delete duplicates if not wanted

## Safety Model

- Read-only analysis first — full Beaver Builder content audit before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published Beaver Builder content
- Never auto-publishes duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all original Beaver Builder content untouched

## Honest Disclaimer

This skill converts Beaver Builder page structures to Gutenberg block markup and creates duplicates for review.

It cannot:
- Guarantee pixel-perfect visual parity between builders
- Migrate Beaver Themer layouts automatically
- Convert third-party BB add-on modules
- Replicate animations or advanced effects
- Replace a thorough manual QA pass on every page

It can:
- Map 70-85% of standard Beaver Builder modules to core Gutenberg blocks
- Preserve content, images, links, and basic layout structure
- Move you off a third-party builder dependency to native WordPress
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
- `skill_slug = migrate-beaver-builder-to-gutenberg`
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
https://respira.press/skills/migrate-beaver-builder-to-gutenberg
