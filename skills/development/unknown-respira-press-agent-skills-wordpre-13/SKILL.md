---
name: technical-debt-audit
description: Identifies technical debt in WordPress sites - orphaned shortcodes from deleted plugins, unused plugins, database bloat, unused media, builder data from inactive builders. Use when user says "analyze technical debt", "scan for orphaned shortcodes", "check for unused plugins", or "find database bloat".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
---

# Technical Debt Audit

Identifies technical debt in WordPress sites: orphaned shortcodes from deleted plugins, plugins never activated, database bloat indicators, unused media, and builder data from inactive builders.

## What This Skill Does

Finds:
- Orphaned shortcodes from deleted or deactivated plugins
- Plugins that were installed but never activated
- Database bloat indicators (revision count, transient count, auto-draft count)
- Unused media files (files not attached to any posts/pages)
- Builder data from inactive page builders

Provides:
- Detailed report with severity scoring (critical, high, medium, low)
- Recommended cleanup workflows
- Respira commands for safe cleanup using duplicate-first workflow
- Estimated space savings and performance impact

## Requirements

- Respira for WordPress plugin installed
- MCP connection active
- Read-only access (no changes without approval)

## How to Use

### Trigger Phrases
- "analyze my site's technical debt"
- "scan for orphaned shortcodes"
- "check for unused plugins"
- "find database bloat"
- "audit technical debt"

### What Happens

1. Scans all posts and pages for shortcodes
2. Cross-references shortcodes with active plugins
3. Identifies orphaned shortcodes
4. Lists inactive plugins and never-activated plugins
5. Checks database for bloat indicators
6. Scans media library for unused files
7. Detects builder data from inactive builders
8. Generates comprehensive report with severity scores

For detailed example output, see `references/example-output.md`

## Honest Disclaimer

This skill **identifies** technical debt. Cleanup requires manual review and approval for each action. Respira's duplicate-first workflow ensures safe testing before any live changes.

**What this skill CANNOT do:**
- Automatically delete anything from your live site
- Bulk cleanup without review
- Make instant "fix all" changes

**What this skill CAN do:**
- Provide detailed inventory of technical debt
- Recommend specific cleanup workflows
- Generate Respira commands for safe duplicate-first cleanup
- Score severity to help prioritize fixes

## Safety Model

- **Read-only scan** - no changes to live site
- **Duplicate-first** - all recommended fixes use duplicate pages
- **Approval required** - you review before any changes go live
- **Rollback ready** - can revert if anything breaks

## Technical Details

Uses these Respira MCP tools:
- `wordpress_list_plugins` - detect installed/active plugins
- `wordpress_list_posts` - scan all posts for shortcodes
- `wordpress_list_pages` - scan all pages for shortcodes
- `wordpress_get_database_stats` - check for bloat indicators
- `wordpress_list_media` - find unused media files
- `wordpress_detect_page_builder` - identify builder data on pages

## Related Skills

- WordPress Site DNA - comprehensive site archaeology
- WooCommerce Health Check - store-specific diagnostics
- Mobile Experience Report - responsive layout analysis

---

Built by Respira for WordPress
https://respira.press
