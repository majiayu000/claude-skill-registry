---
name: wordpress-site-dna
description: Archaeological analysis of WordPress sites. Detects all page builders, audits plugins (active vs dead weight), maps content structure, finds orphaned shortcodes, measures performance, and assesses security posture. Use when user says "analyze my wordpress site", "wordpress site audit", "site dna", or "check my wordpress health".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
---

# WordPress Site DNA

Archaeological analysis of WordPress installations. Detects all page builders, audits plugins, maps content structure, finds orphaned shortcodes, and provides health score with prioritized fixes.

## What This Skill Does

Scans your entire WordPress installation and provides:
- Page builder detection (all 11 supported: Elementor, Divi, Bricks, etc.)
- Plugin audit (active, inactive, abandoned)
- Content structure mapping
- Orphaned shortcode detection
- Performance indicators
- Security posture assessment
- Health score (0-100) with prioritized recommendations

## Requirements

- Respira for WordPress plugin installed
- MCP connection active (desktop or WebMCP)
- Read-only access (no changes made)

## How to Use

### Trigger Phrases
- "analyze my wordpress site"
- "wordpress site dna"
- "run site audit"
- "check my wordpress health"

### What Happens

1. **Scans site architecture:**
   - WordPress version and configuration
   - Active theme and child themes
   - All installed plugins (active and inactive)
   - Page builder usage across pages

2. **Analyzes content:**
   - Posts, pages, custom post types count
   - Builder usage per content type
   - Orphaned shortcodes from deleted plugins
   - Content distribution

3. **Checks performance indicators:**
   - Database size and bloat
   - Revision count
   - Transient buildup
   - Auto-draft accumulation

4. **Assesses security:**
   - WordPress version currency
   - Plugin update status
   - Common security issues
   - User role configuration

5. **Generates health score:**
   - Critical issues (immediate attention)
   - High priority (fix soon)
   - Medium priority (optimization)
   - Low priority (nice to have)

## Output Format

Provides comprehensive report with:
- Overall health score (0-100)
- Critical issues flagged
- Prioritized recommendation list
- Specific fix workflows using Respira duplicate-first approach

For detailed example output, see `references/example-output.md`

## Safety Model

- **100% read-only** - makes no changes to your site
- **No destructive operations** - only analyzes and reports
- **Duplicate-first recommendations** - all fix workflows use duplicates

## Technical Details

Uses these Respira MCP tools:
- `wordpress_get_site_info` - WordPress version, URL, settings
- `wordpress_list_plugins` - all installed plugins
- `wordpress_get_theme_info` - active theme details
- `wordpress_list_pages` - scan all pages
- `wordpress_list_posts` - scan all posts
- `wordpress_detect_page_builder` - identify builders per page
- `wordpress_get_database_stats` - size, bloat, revisions

For complete tool reference, see `references/mcp-tools.md`

## Related Skills

- Technical Debt Audit - focuses on cleanup opportunities
- SEO & AEO Amplifier - optimizes for search visibility
- WordPress AI Image Optimizer - optimizes media library

---

Built by Respira for WordPress
https://respira.press
