---
name: migrate-oxygen-to-breakdance
description: Full-site migration from Oxygen Builder to Breakdance (same Soflyy lineage, smoothest possible builder swap). Audits every Oxygen page, maps components to Breakdance equivalents, builds a migration plan for approval, and converts pages via duplicates so the live site stays untouched. Use when user says "migrate Oxygen to Breakdance", "switch from Oxygen to Breakdance", or "replace Oxygen with Breakdance".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: migration
---

# Migrate Oxygen to Breakdance

Full-site migration from Oxygen Builder to Breakdance. Audits every Oxygen-built page, maps components to their Breakdance equivalents, builds a migration plan for approval, and executes page-by-page conversion — all through duplicates so your live site stays untouched. Use this skill whenever someone mentions migrating from Oxygen to Breakdance, switching from Oxygen to Breakdance, converting Oxygen pages to Breakdance, or replacing Oxygen with Breakdance.

## What This Skill Does

Oxygen and Breakdance share the same developer lineage (Soflyy), which makes this one of the smoothest builder migrations available. Many component concepts, naming conventions, and architectural decisions carry over directly. However, the underlying storage formats are completely different — Oxygen uses JSON shortcodes in `ct_builder_shortcodes` while Breakdance uses its own post_meta format — so content must still be extracted, mapped, and re-encoded.

This skill reads every Oxygen page, extracts the builder content, translates each component to its Breakdance equivalent, and writes the result to duplicate pages in Breakdance format — giving you a complete parallel version of your site to review before going live.

**Handles:**
- Section → Breakdance Section mapping
- Container/Div → Breakdance Div mapping
- Heading, Text, Image, Button, Video, Icon components
- Flexbox layout settings (direction, alignment, gap, wrap)
- Column/grid structures
- Custom CSS classes and inline styles
- Link elements and CTAs
- Code blocks and custom HTML

## What This Skill Does NOT Do

- Migrate Oxygen's Global Styles or Style Sheets — Breakdance uses its own global styling system
- Convert Oxygen conditions (visibility rules) — Breakdance has its own conditions system that must be configured separately
- Migrate Oxygen's custom PHP/code block logic — flagged for manual porting
- Recreate Oxygen templates (headers, footers, archives) — Breakdance templates must be rebuilt using its template system
- Transfer WooCommerce builder templates — product/shop templates need separate handling
- Guarantee pixel-perfect visual parity — some spacing/sizing will need fine-tuning

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Oxygen Builder active on the source site
- Breakdance installed on the target site (can be the same site)
- Read access to scan Oxygen content
- Write access to create duplicates with Breakdance content

## Trigger Phrase

- "migrate oxygen to breakdance"

## Alternative Triggers

- "convert oxygen to breakdance"
- "switch from oxygen to breakdance"
- "move oxygen pages to breakdance"
- "replace oxygen with breakdance"
- "oxygen to breakdance migration"
- "upgrade oxygen to breakdance"

## Builder Technical Context

**Source: Oxygen Builder**
- Content stored in post_meta key `ct_builder_shortcodes`
- JSON-based structure encoding nested components
- Read via `wordpress_extract_builder_content` with `builder=oxygen`
- Components: `ct_section`, `ct_div`, `ct_headline`, `ct_text_block`, `ct_image`, `ct_link_button`, etc.

**Target: Breakdance**
- Content stored in post_meta
- Write via `wordpress_inject_builder_content` with `builder=breakdance`
- Elements: `EssentialElements\Section`, `EssentialElements\Div`, `EssentialElements\Heading`, `EssentialElements\Text`, `EssentialElements\Image`, `EssentialElements\Button`, etc.

## Execution Workflow

### Phase 1: Pre-Migration Audit

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Detect Oxygen presence via `wordpress_get_builder_info` or `wordpress_list_plugins`.
3. Inventory all Oxygen-built content:
   - `wordpress_list_pages` and `wordpress_list_posts` — identify all content
   - `wordpress_find_builder_targets` with `builder=oxygen` — find Oxygen-managed pages
4. For each Oxygen page, extract content:
   - `wordpress_extract_builder_content` with `builder=oxygen`
   - Catalog: component types used, nesting depth, custom CSS, dynamic data usage, code blocks
5. Produce an **Audit Report**:
   - Total pages/posts using Oxygen
   - Component type frequency (how many sections, headings, images, etc.)
   - Complexity flags (custom PHP, conditions, dynamic data, WooCommerce templates)
   - Estimated migration difficulty per page (simple / moderate / complex)

### Phase 2: Migration Plan

Present a structured migration plan:

```
## Oxygen → Breakdance Migration Plan

### Site Overview
- Total Oxygen pages: X
- Simple pages (direct mapping): X
- Moderate pages (some manual review needed): X
- Complex pages (significant manual work): X

### Component Mapping
| Oxygen Component | Breakdance Equivalent | Notes |
|---|---|---|
| ct_section | Section | Direct mapping — same developer lineage |
| ct_div | Div | Direct mapping |
| ct_headline | Heading | Direct mapping |
| ... | ... | ... |

### Migration Order
1. [Page Title] — Simple — estimated 2 min
2. [Page Title] — Moderate — estimated 5 min
...

### Items Requiring Manual Attention
- [Page X] — Custom PHP code block
- [Page Y] — Oxygen condition logic
- Global Styles — must be recreated in Breakdance Global Settings
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

1. Extract Oxygen content via `wordpress_extract_builder_content` with `builder=oxygen`
2. Map each Oxygen component to its Breakdance equivalent:
   - Translate component types (ct_section → Section, ct_div → Div, etc.)
   - Convert layout properties (flexbox settings, spacing, sizing)
   - Map CSS classes and inline styles
   - Preserve text content, image URLs, link targets
   - Flag any unmappable components (custom PHP, conditions) with inline comments
3. Build the Breakdance content structure
4. Create a duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
5. Inject Breakdance content via `wordpress_inject_builder_content` with `builder=breakdance`
6. Log the migration result (success, warnings, manual review items)

### Phase 4: Post-Migration Verification

1. Summarize all migrated pages with status:
   - Clean migrations (no issues)
   - Migrations with warnings (flagged items needing review)
   - Failed migrations (if any)
2. List all manual review items:
   - Custom PHP code blocks that need porting
   - Dynamic data references that need reconnecting
   - Oxygen conditions that need rebuilding in Breakdance
3. Provide review instructions:
   - Where to find duplicates in WordPress admin
   - How to preview Breakdance pages
   - How to delete duplicates if not wanted

## Safety Model

- Read-only analysis first — full Oxygen content audit before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published Oxygen content
- Never auto-publishes duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all original Oxygen content untouched

## Honest Disclaimer

This skill converts Oxygen page structures to Breakdance format and creates duplicates for review.

It cannot:
- Guarantee pixel-perfect visual parity between builders
- Migrate Oxygen Global Styles or conditions automatically
- Convert custom PHP code blocks to Breakdance equivalents
- Handle WooCommerce template migrations
- Replace a thorough manual QA pass on every page

It can:
- Leverage the shared developer lineage for high-fidelity component mapping
- Map 85-95% of standard Oxygen components to Breakdance equivalents
- Preserve content, images, links, and layout structure
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
- `skill_slug = migrate-oxygen-to-breakdance`
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
https://respira.press/skills/migrate-oxygen-to-breakdance
