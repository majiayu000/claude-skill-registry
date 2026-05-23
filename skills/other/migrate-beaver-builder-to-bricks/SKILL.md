---
name: migrate-beaver-builder-to-bricks
description: Full-site migration from Beaver Builder to Bricks Builder. Audits every Beaver Builder page, maps modules to Bricks equivalents, builds a migration plan for approval, and converts pages to Bricks JSON via duplicates so the live site stays untouched. Use when user says "migrate Beaver Builder to Bricks", "switch from BB to Bricks", "convert Beaver Builder pages to Bricks", or "replace Beaver Builder with Bricks".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Beaver Builder to Bricks

Full-site migration from Beaver Builder to Bricks Builder. Audits every Beaver Builder page, maps modules to their Bricks equivalents, builds a migration plan for approval, and executes page-by-page conversion into Bricks' JSON format — all through duplicates so your live site stays untouched. Use this skill whenever someone mentions migrating from Beaver Builder to Bricks, switching from BB to Bricks, converting Beaver Builder pages to Bricks, or replacing Beaver Builder with Bricks.

## What This Skill Does

Beaver Builder and Bricks are both visual page builders, but they differ significantly in architecture. Beaver Builder uses a module-based system with rows, columns, and modules stored in `_fl_builder_data`. Bricks uses a more modern, flexbox-first approach with sections, containers, and elements stored as a JSON array in `_bricks_page_content_2`. The migration requires translating BB's row/column grid into Bricks' container model and mapping each module to its Bricks element equivalent.

This skill reads every Beaver Builder page, extracts the module structure, translates each row/column/module to its Bricks equivalent, and writes the result to duplicate pages in Bricks format — giving you a complete parallel version of your site to review before going live.

**Handles:**
- Row → Bricks Section mapping
- Column structures → Bricks Container with flex layout
- Text Editor module → Bricks Text / Heading elements
- Photo module → Bricks Image element
- Button module → Bricks Button element
- Video module → Bricks Video element
- HTML module → Bricks Code element
- Heading module → Bricks Heading element
- Separator module → Bricks Divider element
- Icon module → Bricks Icon element
- Call to Action module → Bricks Container + child elements
- Custom CSS classes and inline styles

## What This Skill Does NOT Do

- Migrate Beaver Builder's saved rows/modules library — these must be recreated in Bricks
- Convert Beaver Themer layouts (headers, footers, archives) — Bricks templates must be built separately
- Replicate exact Beaver Builder animations/effects — Bricks has its own interaction system
- Migrate third-party Beaver Builder add-on modules (PowerPack, UABB, etc.) — flagged for manual handling
- Convert BB's global rows to Bricks' template system — different architectural concept
- Guarantee pixel-perfect visual parity — different rendering engines produce different output

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Beaver Builder active on the source site
- Bricks Builder installed on the target site (can be the same site)
- Read access to scan Beaver Builder content
- Write access to create duplicates with Bricks content

## Trigger Phrase

- "migrate beaver builder to bricks"

## Alternative Triggers

- "convert beaver builder to bricks"
- "switch from bb to bricks"
- "move beaver builder pages to bricks"
- "replace beaver builder with bricks"
- "beaver builder to bricks migration"
- "migrate bb to bricks"

## Builder Technical Context

**Source: Beaver Builder**
- Content stored in post_meta keys `_fl_builder_data` and `_fl_builder_data_settings`
- Module-based structure with rows → columns → modules hierarchy
- Read via `wordpress_extract_builder_content` with `builder=beaver` or `builder=beaver-builder`
- Module types: `rich-text`, `photo`, `button`, `heading`, `html`, `video`, `icon`, `separator`, `callout`, `cta`, `numbers`, `content-slider`, etc.

**Target: Bricks Builder**
- Content stored in post_meta key `_bricks_page_content_2` as a JSON array
- Each element is an object with `id`, `name`, `parent`, `settings`, `children`
- Write via `wordpress_inject_builder_content` with `builder=bricks`
- Elements: `section`, `container`, `heading`, `text`, `image`, `button`, `video`, `code`, `divider`, `icon`, etc.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Detect Beaver Builder presence via `wordpress_get_builder_info` or `wordpress_list_plugins`.
3. Inventory all Beaver Builder content:
   - `wordpress_list_pages` and `wordpress_list_posts` — identify all content
   - `wordpress_find_builder_targets` with `builder=beaver` — find BB-managed pages
4. For each BB page, extract content:
   - `wordpress_extract_builder_content` with `builder=beaver`
   - Catalog: module types used, row/column structures, custom CSS, third-party modules, saved rows/modules
5. Produce an **Audit Report**:
   - Total pages/posts using Beaver Builder
   - Module type frequency (how many text editors, photos, buttons, etc.)
   - Column layout patterns (common row structures)
   - Complexity flags (third-party modules, Beaver Themer, custom CSS, animations)
   - Estimated migration difficulty per page (simple / moderate / complex)

### Phase 2: Migration Plan

Present a structured migration plan:

```
## Beaver Builder → Bricks Migration Plan

### Site Overview
- Total Beaver Builder pages: X
- Simple pages (direct mapping): X
- Moderate pages (some manual review needed): X
- Complex pages (significant manual work): X

### Module-to-Element Mapping
| BB Module | Bricks Element | Notes |
|---|---|---|
| Row | Section | BB row maps to Bricks section |
| Column | Container | Flex-based layout in Bricks |
| Text Editor | Text / Heading | Content parsed into elements |
| Photo | Image | Direct mapping |
| Button | Button | Direct mapping |
| ... | ... | ... |

### Migration Order
1. [Page Title] — Simple — estimated 2 min
2. [Page Title] — Moderate — estimated 5 min
...

### Items Requiring Manual Attention
- [Page X] — PowerPack Tabs module (no direct Bricks equivalent)
- [Page Y] — Content slider (needs Bricks slider setup)
- Beaver Themer layouts — must be rebuilt as Bricks templates
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
2. Map the row/column/module hierarchy to Bricks elements:
   - Rows → Bricks `section` elements
   - Columns → Bricks `container` elements with flex layout settings
   - Text Editor → Parse into `text` and `heading` elements
   - Photo → `image` element with src, alt, caption
   - Button → `button` element with text, link, style
   - HTML → `code` element
   - Map CSS classes and inline styles to Bricks settings
   - Preserve text content, image URLs, link targets
   - Flag any unmappable modules with comment annotations
3. Build the Bricks JSON array structure
4. Create a duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Inject Bricks content via `wordpress_inject_builder_content` with `builder=bricks`
6. Log the migration result (success, warnings, manual review items)

### Phase 4: Post-Migration Verification

1. Summarize all migrated pages with status:
   - Clean migrations (no issues)
   - Migrations with warnings (flagged items needing review)
   - Failed migrations (if any)
2. List all manual review items:
   - Third-party modules that need manual replacement
   - Content sliders or advanced layouts needing Bricks-native rebuilds
   - Custom CSS that needs to be added to Bricks element styles
   - Beaver Themer layouts that need separate rebuilding in Bricks
3. Provide review instructions:
   - Where to find duplicates in WordPress admin
   - How to preview Bricks pages
   - How to delete duplicates if not wanted

## Safety Model

- Read-only analysis first — full Beaver Builder content audit before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published Beaver Builder content
- Never auto-publishes duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all original Beaver Builder content untouched

## Honest Disclaimer

This skill converts Beaver Builder page structures to Bricks format and creates duplicates for review.

It cannot:
- Guarantee pixel-perfect visual parity between builders
- Migrate Beaver Themer layouts automatically
- Convert third-party BB add-on modules to Bricks equivalents
- Replicate BB animations in Bricks interactions
- Replace a thorough manual QA pass on every page

It can:
- Map 75-85% of standard Beaver Builder modules to Bricks elements
- Translate row/column grids to Bricks' modern flexbox containers
- Preserve content, images, links, and layout structure
- Move you to a more modern builder architecture
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
- `wordpress_inject_builder_content`
- `wordpress_create_page_duplicate`
- `wordpress_create_post_duplicate`
- `wordpress_read_page`
- `wordpress_read_post`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = migrate-beaver-builder-to-bricks`
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
https://respira.press/skills/migrate-beaver-builder-to-bricks
