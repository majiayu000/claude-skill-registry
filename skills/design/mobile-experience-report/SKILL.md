---
name: mobile-experience-report
description: Mobile layout diagnostics - identifies responsive breakpoint problems, text sizing issues, column stacking failures, element visibility issues, navigation menu behavior. Device-by-device breakdown. Use when user says "check my mobile experience", "audit mobile responsiveness", "scan for mobile layout issues", or "mobile experience report".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
---

# Mobile Experience Report

Identifies mobile layout issues across devices: responsive breakpoint problems, text sizing issues, column stacking failures, element visibility problems, and navigation menu behavior.

## What This Skill Does

Finds:
- Responsive breakpoint issues (desktop layout showing on mobile)
- Text sizing problems (text too small to read comfortably)
- Column stacking failures (columns not stacking on mobile)
- Element visibility issues (hidden buttons, overlapping content)
- Navigation menu problems (hamburger menu not working, menu cut off)
- Image scaling issues (images too large or too small)
- Touch target problems (buttons too small for finger taps)

Provides:
- Device-by-device breakdown (iPhone, Android, tablet)
- Specific pages with issues
- Respira commands for mobile-optimized duplicates
- Before/after viewport simulations

## Requirements

- Respira for WordPress plugin installed
- MCP connection active
- Read-only access (no changes without approval)

## How to Use

### Trigger Phrases
- "check my mobile experience"
- "audit mobile responsiveness"
- "scan for mobile layout issues"
- "test mobile experience"
- "mobile experience report"

### What Happens

1. Scans your site's pages with builder-aware extraction
2. Analyzes CSS for responsive breakpoints
3. Simulates viewport sizes (320px, 375px, 414px, 768px, 1024px)
4. Detects layout issues at each breakpoint
5. Checks touch target sizes (minimum 44x44px)
6. Tests navigation menu behavior
7. Generates device-specific issue report

For detailed example output, see `references/example-output.md`

## Honest Disclaimer

This skill **identifies** mobile layout issues. Fixes are tested on duplicates before applying to live pages.

**What this skill CANNOT do:**
- Automatically fix all responsive issues
- Guarantee pixel-perfect mobile layouts
- Make instant changes to live site

**What this skill CAN do:**
- Provide specific mobile issues by device type
- Generate fix workflows with code examples
- Create mobile-optimized duplicates for testing
- Prioritize fixes by user impact

## Safety Model

- **Read-only scan** - no changes to live site
- **Duplicate-first** - test mobile fixes on duplicate pages
- **Approval required** - review before changes go live
- **Rollback ready** - can revert if anything breaks

## Technical Details

Uses these Respira MCP tools:
- `wordpress_list_pages` - scan all pages
- `wordpress_get_page` - extract content with builder awareness
- `wordpress_detect_page_builder` - identify builder for targeted fixes
- `wordpress_create_duplicate` - create test pages for fixes

Simulates these viewport sizes:
- iPhone SE: 320px width
- iPhone 12/13: 375px width
- iPhone 12/13 Pro Max: 414px width
- iPad: 768px width
- iPad Pro: 1024px width

## Related Skills

- WordPress Site DNA - full site archaeology
- Technical Debt Audit - general cleanup
- WooCommerce Health Check - mobile checkout experience

---

Built by Respira for WordPress
https://respira.press
