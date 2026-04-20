---
name: seo-aeo-amplifier
description: Comprehensive on-page SEO and Answer Engine Optimization audit with automated duplicate creation and intelligent schema markup generation. Scans all content, detects issues (missing titles, weak meta, poor headings, missing alt text), generates schema (Article, FAQ, HowTo, Product, etc), creates optimized duplicates. Use when user says "amplify my seo and aeo", "optimize for search engines", "run seo audit", "improve search visibility", or "scan for seo opportunities".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: performance
---

# SEO & AEO Amplifier

Comprehensive on-page SEO and Answer Engine Optimization (AEO) audit and auto-fix system. Scans all content, detects issues, generates intelligent schema markup, and creates optimized duplicates for review.

## What This Skill Does

**Detects on-page SEO issues:**
- Missing or weak title tags and meta descriptions
- Poor heading structure (multiple H1s, skipped levels)
- Missing image alt text
- Thin content (pages under 300 words)
- Broken internal links
- Orphaned pages (no internal links to them)
- Non-descriptive URL slugs

**Identifies AEO opportunities:**
- Content that answers questions but lacks FAQ schema
- Missing structured data (Article, HowTo, Product, Event, Video, Review)
- Content not formatted for featured snippets
- Missing table of contents on long-form content
- No clear Q&A structure for "People Also Ask"

**Generates schema markup:**
- Article, FAQ, HowTo, Product, Event, Video, Review, Breadcrumb, Organization schema
- Intelligent selection based on content type
- JSON-LD format (works with any SEO plugin)

**Auto-creates optimized duplicates:**
- Asks for user approval first
- Creates duplicates with all fixes applied
- Updates titles, meta descriptions, headings
- Adds missing alt text
- Inserts appropriate schema markup
- Provides before/after comparison

## Requirements

- Respira for WordPress plugin installed
- MCP connection active
- WooCommerce add-on (optional - for Product schema)

## How to Use

### Trigger Phrases
- "amplify my seo and aeo"
- "optimize my site for search engines"
- "run seo aeo audit"
- "improve my search visibility"
- "scan for seo opportunities"

### Workflow

**Phase 1: Comprehensive Audit**
1. Scans all published pages and posts
2. Detects installed SEO plugins (Yoast, Rank Math)
3. Analyzes content for SEO issues
4. Identifies AEO opportunities
5. Scores each page by opportunity (high/medium/low)
6. Generates comprehensive report

**Phase 2: User Decision**
Presents report and asks:
> "I found [X] pages with SEO/AEO improvement opportunities. Would you like me to create optimized duplicates for all of them?"

**Phase 3: Auto-Fix (if approved)**
7. Creates duplicate for each page with issues
8. Applies all fixes to duplicates
9. Inserts JSON-LD schema markup
10. Provides before/after comparison
11. User reviews and approves to publish

For detailed workflow and example output, see `references/workflow-details.md`

## SEO Plugin Integration

**Works with:**
- Yoast SEO - reads existing meta, populates Yoast fields on duplicates
- Rank Math - reads existing meta, populates Rank Math fields
- No plugin - adds meta tags directly, fully functional

Schema markup inserted as JSON-LD works alongside any plugin.

## Honest Disclaimer

This skill **identifies** SEO and AEO opportunities and **creates optimized duplicates**. You review and approve before anything goes live.

**What this skill CANNOT do:**
- Guarantee higher rankings (SEO is competitive)
- Fix technical SEO issues (site speed, server config)
- Write entirely new content (expands/optimizes existing)
- Automatically publish changes (you review first)

**What this skill CAN do:**
- Identify every on-page SEO issue across your entire site
- Generate intelligent schema markup based on content analysis
- Create optimized duplicates with all fixes applied
- Provide before/after comparisons for transparency

## Safety Model

- **Read-only audit** - initial scan makes no changes
- **User confirmation required** - asks before creating duplicates
- **Duplicate-first** - all fixes applied to duplicates, never live pages
- **Approval required** - you review every change before publishing
- **Rollback ready** - can delete all duplicates and start over

## Technical Details

Uses these Respira MCP tools:
- `wordpress_list_pages` / `wordpress_list_posts` - scan content
- `wordpress_get_page` / `wordpress_get_post` - read content
- `wordpress_detect_page_builder` - identify builder for extraction
- `wordpress_list_media` - check image alt text
- `wordpress_list_plugins` - detect Yoast, Rank Math
- `wordpress_create_duplicate` - create duplicates
- `wordpress_update_page` / `wordpress_update_post` - apply fixes

For complete tool reference and schema markup details, see `references/technical-details.md`

## Related Skills

- WordPress AI Image Optimizer - optimizes images for speed and SEO
- WordPress Site DNA - comprehensive site analysis
- Mobile Experience Report - mobile SEO and UX

---

Built by Respira for WordPress
https://respira.press
