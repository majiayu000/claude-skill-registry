---
name: migrate-brizy-to-gutenberg
description: Full-site migration from Brizy Builder to the WordPress block editor (Gutenberg). Audits every Brizy-built page, maps components to native block equivalents, builds a migration plan for approval, and converts pages to native block markup via duplicates so the live site stays untouched. Use when user says "migrate Brizy to Gutenberg", "switch from Brizy to blocks", "convert Brizy pages to the block editor", or "move from Brizy to native WordPress".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Brizy to Gutenberg

Full-site migration from Brizy Builder to the WordPress block editor (Gutenberg). Audits every Brizy-built page, maps components to their Gutenberg block equivalents, builds a migration plan for approval, and executes page-by-page conversion into native block markup — all through duplicates so your live site stays untouched. Use this skill whenever someone mentions migrating from Brizy to Gutenberg, switching from Brizy to blocks, converting Brizy pages to the block editor, or moving away from Brizy to native WordPress.

## What This Skill Does

Brizy uses a proprietary content format with its own component system, storing data in `brizy_post_uid` and related custom meta fields. Gutenberg uses a flat block structure in `post_content` with HTML comment delimiters. The migration requires extracting Brizy's custom format, identifying each component type, and translating it to equivalent core Gutenberg blocks.

This skill reads every Brizy page, extracts the builder content, translates each component to its Gutenberg block equivalent, and writes the result to duplicate pages in native block markup — giving you a complete parallel version of your site to review before going live.

**Handles:**
- Section → Group block mapping
- Row/Column → Columns/Column block mapping
- Text components → Paragraph/Heading blocks
- Image components → Image block
- Button components → Buttons/Button block
- Video components → Video/Embed block
- Icon components → basic equivalents
- Spacer/Divider → Spacer/Separator blocks
- Map component → basic embed fallback
- Form elements → flagged for manual handling (Contact Form 7 or similar)
- Custom HTML/embed content

## What This Skill Does NOT Do

- Migrate Brizy's global styling system — must be recreated in theme settings or Global Styles
- Convert Brizy popup designs — Gutenberg has no native popup system
- Replicate Brizy's built-in form submissions — a separate form plugin is needed
- Migrate Brizy Cloud templates or synced content
- Convert Brizy Pro dynamic content features — flagged for manual handling
- Preserve Brizy's hover effects and animations — Gutenberg has limited animation support
- Guarantee pixel-perfect visual parity — different rendering approaches

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Brizy Builder active on the source site
- Read access to scan Brizy content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate brizy to gutenberg"

## Alternative Triggers

- "convert brizy to blocks"
- "switch from brizy to gutenberg"
- "move brizy to block editor"
- "replace brizy with gutenberg"
- "brizy to wordpress blocks"
- "migrate brizy to native wordpress"

## Builder Technical Context

**Source: Brizy**
- Content stored in post_meta key `brizy_post_uid` and Brizy's custom format
- Proprietary component structure with sections, rows, columns, and elements
- Read via `wordpress_extract_builder_content` with `builder=brizy`
- Components: sections, rows, columns, text, image, button, video, icon, spacer, map, form, embed, etc.

**Target: Gutenberg (Block Editor)**
- Content stored in `post_content` as HTML with block comment delimiters
- Format: `<!-- wp:paragraph --><p>Text</p><!-- /wp:paragraph -->`
- Write via standard WordPress content tools (`wordpress_update_page` / `wordpress_update_post`)
- Core blocks: `paragraph`, `heading`, `image`, `buttons`, `columns`, `group`, `html`, `video`, `separator`, `spacer`, `embed`, etc.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Detect Brizy presence via `wordpress_get_builder_info` or `wordpress_list_plugins`.
3. Inventory all Brizy-built content:
   - `wordpress_list_pages` and `wordpress_list_posts` — identify all content
   - `wordpress_find_builder_targets` with `builder=brizy` — find Brizy-managed pages
4. For each Brizy page, extract content:
   - `wordpress_extract_builder_content` with `builder=brizy`
   - Catalog: component types used, nesting depth, popups, forms, dynamic content usage
5. Produce an **Audit Report**:
   - Total pages/posts using Brizy
   - Component type frequency (how many sections, text blocks, images, etc.)
   - Complexity flags (popups, forms, dynamic content, Brizy Pro features)
   - Estimated migration difficulty per page (simple / moderate / complex)

### Phase 2: Migration Plan

Present a structured migration plan:

```
## Brizy → Gutenberg Migration Plan

### Site Overview
- Total Brizy pages: X
- Simple pages (direct mapping): X
- Moderate pages (some manual review needed): X
- Complex pages (significant manual work): X

### Component Mapping
| Brizy Component | Gutenberg Block | Notes |
|---|---|---|
| Section | Group | Container mapping |
| Row / Columns | Columns / Column | Layout structure |
| Text | Paragraph / Heading | Content parsed into blocks |
| Image | Image | Direct mapping |
| Button | Buttons > Button | Wrapped in container |
| ... | ... | ... |

### Migration Order
1. [Page Title] — Simple — estimated 2 min
2. [Page Title] — Moderate — estimated 5 min
...

### Items Requiring Manual Attention
- [Page X] — Brizy popup (no Gutenberg equivalent)
- [Page Y] — Brizy form (needs form plugin replacement)
- Global styles — must be configured in theme settings
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

1. Extract Brizy content via `wordpress_extract_builder_content` with `builder=brizy`
2. Map each Brizy component to Gutenberg blocks:
   - Sections → `<!-- wp:group -->` blocks
   - Rows/Columns → `<!-- wp:columns -->` with `<!-- wp:column -->` children
   - Text → Parse into `<!-- wp:paragraph -->` and `<!-- wp:heading -->` blocks
   - Image → `<!-- wp:image -->` with src, alt, caption
   - Button → `<!-- wp:buttons -->` wrapper with `<!-- wp:button -->` child
   - Video → `<!-- wp:video -->` or `<!-- wp:embed -->` block
   - Spacer → `<!-- wp:spacer -->` block
   - Custom HTML → `<!-- wp:html -->` block
   - Preserve text content, image URLs, link targets
   - Flag unmappable components with `<!-- wp:paragraph --><p>[MIGRATION NOTE: ...]</p><!-- /wp:paragraph -->`
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
   - Popups that need a separate popup plugin solution
   - Forms that need a WordPress form plugin (Contact Form 7, WPForms, etc.)
   - Dynamic content that needs reconnecting
   - Brizy Pro features that have no Gutenberg equivalent
3. Provide review instructions:
   - Where to find duplicates in WordPress admin
   - How to preview pages in the block editor
   - How to delete duplicates if not wanted

## Safety Model

- Read-only analysis first — full Brizy content audit before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published Brizy content
- Never auto-publishes duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all original Brizy content untouched

## Honest Disclaimer

This skill converts Brizy page structures to Gutenberg block markup and creates duplicates for review.

It cannot:
- Guarantee pixel-perfect visual parity between builders
- Migrate Brizy popups or forms automatically
- Convert Brizy Pro dynamic content features
- Replicate hover effects or animations
- Replace a thorough manual QA pass on every page

It can:
- Map 65-80% of standard Brizy components to core Gutenberg blocks
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
- `skill_slug = migrate-brizy-to-gutenberg`
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
https://respira.press/skills/migrate-brizy-to-gutenberg
