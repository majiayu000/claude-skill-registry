---
name: migrate-thrive-architect-to-gutenberg
description: Full-site migration from Thrive Architect to the WordPress block editor (Gutenberg). Audits every Thrive page, maps elements to native block equivalents, builds a migration plan for approval, and converts pages to native block markup via duplicates so the live site stays untouched. Marketing-only Thrive components (Thrive Leads, Ultimatum, Quiz) are flagged for separate replacement. Use when user says "migrate Thrive Architect to Gutenberg", "switch from Thrive to blocks", or "move from Thrive Architect to native WordPress".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Thrive Architect to Gutenberg

Full-site migration from Thrive Architect to the WordPress block editor (Gutenberg). Audits every Thrive-built page, maps elements to their Gutenberg block equivalents, builds a migration plan for approval, and executes page-by-page conversion into native block markup — all through duplicates so your live site stays untouched. Use this skill whenever someone mentions migrating from Thrive Architect to Gutenberg, switching from Thrive to blocks, converting Thrive pages to the block editor, or moving away from Thrive Architect to native WordPress.

## What This Skill Does

Thrive Architect is a conversion-focused page builder with a strong emphasis on marketing elements — lead generation forms, countdown timers, testimonials, and content reveal animations. It stores content in its own custom format. Gutenberg uses a flat block structure in `post_content` with HTML comment delimiters. The migration is moderate in complexity: standard content elements translate well, but Thrive's marketing-specific components have no direct Gutenberg equivalents and require alternative solutions.

This skill reads every Thrive Architect page, extracts the builder content, translates each element to its Gutenberg block equivalent, and writes the result to duplicate pages in native block markup — giving you a complete parallel version of your site to review before going live.

**Handles:**
- Content Box → Group block mapping
- Column layouts → Columns/Column block mapping
- Text elements → Paragraph/Heading blocks
- Image elements → Image block
- Button elements → Buttons/Button block
- Video elements → Video/Embed block
- Divider → Separator block
- Custom HTML/code content
- Background sections → Group block with background styles
- Styled lists → List block
- Blockquote/Testimonial → Quote block (basic mapping)

## What This Skill Does NOT Do

- Migrate Thrive Leads opt-in forms — a separate email marketing/form solution is needed
- Convert Thrive Ultimatum countdown timers — no native Gutenberg equivalent
- Replicate Thrive's content reveal (click-to-expand) functionality
- Migrate Thrive Quiz Builder or Thrive Apprentice integrations
- Convert Thrive-specific A/B test variants — flagged for reference only
- Preserve Thrive's scroll-triggered animations — Gutenberg has limited animation support
- Migrate Thrive landing page templates — must be rebuilt from the Gutenberg block structure
- Guarantee pixel-perfect visual parity — different rendering approaches

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Thrive Architect active on the source site
- Read access to scan Thrive content
- Write access to create duplicates with Gutenberg content

## Trigger Phrase

- "migrate thrive architect to gutenberg"

## Alternative Triggers

- "convert thrive to blocks"
- "switch from thrive architect to gutenberg"
- "move thrive pages to block editor"
- "replace thrive architect with gutenberg"
- "thrive architect to wordpress blocks"
- "migrate thrive to native wordpress"

## Builder Technical Context

**Source: Thrive Architect**
- Content stored via Thrive's custom format in post_meta
- Conversion-focused component library with marketing elements
- Read via `wordpress_extract_builder_content` with `builder=thrive`
- Components: content boxes, columns, text, image, button, video, lead generation, countdown, testimonial, styled list, toggle, tabs, etc.

**Target: Gutenberg (Block Editor)**
- Content stored in `post_content` as HTML with block comment delimiters
- Format: `<!-- wp:paragraph --><p>Text</p><!-- /wp:paragraph -->`
- Write via standard WordPress content tools (`wordpress_update_page` / `wordpress_update_post`)
- Core blocks: `paragraph`, `heading`, `image`, `buttons`, `columns`, `group`, `html`, `video`, `separator`, `quote`, `list`, `embed`, etc.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Detect Thrive Architect presence via `wordpress_get_builder_info` or `wordpress_list_plugins`.
3. Inventory all Thrive-built content:
   - `wordpress_list_pages` and `wordpress_list_posts` — identify all content
   - `wordpress_find_builder_targets` with `builder=thrive` — find Thrive-managed pages
4. For each Thrive page, extract content:
   - `wordpress_extract_builder_content` with `builder=thrive`
   - Catalog: element types used, marketing components (forms, countdowns, testimonials), A/B test variants, custom CSS
5. Produce an **Audit Report**:
   - Total pages/posts using Thrive Architect
   - Element type frequency (how many content boxes, text blocks, images, etc.)
   - Marketing component inventory (lead gen forms, countdowns, quizzes)
   - Complexity flags (Thrive Leads integration, A/B tests, landing pages, Thrive Suite dependencies)
   - Estimated migration difficulty per page (simple / moderate / complex)

### Phase 2: Migration Plan

Present a structured migration plan:

```
## Thrive Architect → Gutenberg Migration Plan

### Site Overview
- Total Thrive pages: X
- Simple pages (direct mapping): X
- Moderate pages (some manual review needed): X
- Complex pages (significant manual work): X

### Element Mapping
| Thrive Element | Gutenberg Block | Notes |
|---|---|---|
| Content Box | Group | Container mapping |
| Columns | Columns / Column | Layout structure |
| Text | Paragraph / Heading | Content parsed into blocks |
| Image | Image | Direct mapping |
| Button | Buttons > Button | Wrapped in container |
| Lead Gen Form | [MANUAL] | Needs form plugin replacement |
| Countdown | [MANUAL] | No native equivalent |
| ... | ... | ... |

### Migration Order
1. [Page Title] — Simple — estimated 2 min
2. [Page Title] — Moderate — estimated 5 min
...

### Items Requiring Manual Attention
- [Page X] — Thrive Leads form (needs replacement with form plugin)
- [Page Y] — Countdown timer (needs plugin or removal)
- [Page Z] — A/B test variant (winning variant migrated, others documented)
- Landing page templates — must be rebuilt in Gutenberg
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

1. Extract Thrive content via `wordpress_extract_builder_content` with `builder=thrive`
2. Map each Thrive element to Gutenberg blocks:
   - Content Boxes → `<!-- wp:group -->` blocks
   - Columns → `<!-- wp:columns -->` with `<!-- wp:column -->` children
   - Text → Parse into `<!-- wp:paragraph -->` and `<!-- wp:heading -->` blocks
   - Image → `<!-- wp:image -->` with src, alt, caption
   - Button → `<!-- wp:buttons -->` wrapper with `<!-- wp:button -->` child
   - Video → `<!-- wp:video -->` or `<!-- wp:embed -->` block
   - Divider → `<!-- wp:separator -->` block
   - Testimonial → `<!-- wp:quote -->` block (basic mapping)
   - Styled List → `<!-- wp:list -->` block
   - Custom HTML → `<!-- wp:html -->` block
   - Preserve text content, image URLs, link targets
   - Flag marketing components with `<!-- wp:paragraph --><p>[MIGRATION NOTE: Thrive Lead Gen form was here — replace with form plugin shortcode]</p><!-- /wp:paragraph -->`
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
   - Lead generation forms that need a replacement plugin (WPForms, Gravity Forms, etc.)
   - Countdown timers that need a countdown plugin or removal
   - Testimonials that may benefit from a testimonial block plugin
   - A/B test data to document before deactivating Thrive
   - Landing pages that need fresh Gutenberg design
3. Provide review instructions:
   - Where to find duplicates in WordPress admin
   - How to preview pages in the block editor
   - How to delete duplicates if not wanted

## Safety Model

- Read-only analysis first — full Thrive Architect content audit before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published Thrive content
- Never auto-publishes duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all original Thrive Architect content untouched

## Honest Disclaimer

This skill converts Thrive Architect page structures to Gutenberg block markup and creates duplicates for review.

It cannot:
- Guarantee pixel-perfect visual parity between builders
- Migrate Thrive Leads forms or countdown timers automatically
- Convert A/B test configurations
- Replicate Thrive's marketing-specific animations and interactions
- Replace a thorough manual QA pass on every page

It can:
- Map 60-75% of standard Thrive elements to core Gutenberg blocks
- Preserve content, images, links, and basic layout structure
- Clearly flag every marketing component that needs manual replacement
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
- `skill_slug = migrate-thrive-architect-to-gutenberg`
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
https://respira.press/skills/migrate-thrive-architect-to-gutenberg
