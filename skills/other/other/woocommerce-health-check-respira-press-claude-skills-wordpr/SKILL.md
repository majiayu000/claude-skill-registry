---
name: woocommerce-health-check
description: WooCommerce configuration diagnostics - identifies checkout problems, cart errors, AJAX mismatches, caching issues, payment gateway setup, SSL enforcement. Revenue-impacting diagnostics. Requires WooCommerce add-on. Use when user says "check my woocommerce health", "audit woocommerce store", "diagnose checkout issues", or "scan my store for problems".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
  requires_addon: woocommerce
---

# WooCommerce Health Check

Identifies WooCommerce configuration issues that impact conversions and revenue: checkout page problems, cart errors, AJAX URL mismatches, caching on checkout pages, payment gateway setup, and SSL on checkout.

## What This Skill Does

Finds:
- Checkout page configuration issues (missing required fields, broken layouts)
- Cart page problems (AJAX errors, empty cart detection failures)
- AJAX URL mismatches (causes "Add to Cart" failures)
- Caching enabled on checkout/cart pages (breaks checkout flow)
- Payment gateway configuration issues
- SSL not enforced on checkout (security risk)
- Shipping zone configuration problems
- Stock management issues

Provides:
- Revenue impact assessment for each issue
- Specific fixes with Respira workflows
- Mobile vs desktop comparison for checkout flow
- Payment gateway verification checklist

## Requirements

- Respira for WordPress plugin installed
- **WooCommerce add-on installed and licensed**
- WooCommerce plugin active on your site
- MCP connection active
- Read-only access (no changes without approval)

## Why WooCommerce Add-on is Required

This skill uses WooCommerce-specific MCP tools only available with the WooCommerce add-on.

Without the WooCommerce add-on, this skill cannot access your store data.

[Get WooCommerce Add-on ->](https://respira.press/addons/woocommerce)

## How to Use

### Trigger Phrases
- "check my woocommerce health"
- "audit my woocommerce store"
- "diagnose woocommerce checkout issues"
- "scan my store for problems"

### What Happens

1. Verifies WooCommerce installation and version
2. Scans checkout and cart pages for configuration issues
3. Tests AJAX endpoints for proper response
4. Checks for caching on checkout/cart pages
5. Verifies payment gateway configuration
6. Confirms SSL enforcement on checkout
7. Reviews shipping zone setup
8. Checks stock management settings
9. Generates revenue-impact scored report

For detailed example output, see `references/example-output.md`

## Honest Disclaimer

This skill **identifies** WooCommerce configuration issues. Fixes require testing on duplicate pages first, then approval before going live.

**What this skill CANNOT do:**
- Automatically fix your checkout flow
- Make instant changes to WooCommerce settings
- Guarantee conversion rate improvements

**What this skill CAN do:**
- Identify revenue-blocking configuration issues
- Provide specific fix workflows with code examples
- Test fixes on duplicates before going live
- Score issues by revenue impact

## Safety Model

- **Read-only scan** - no changes to live store
- **Duplicate-first** - test fixes on duplicate pages
- **Approval required** - review before changes go live
- **Rollback ready** - can revert if anything breaks

## Technical Details

Uses these WooCommerce MCP tools (requires WooCommerce add-on):
- `woocommerce_list_products`
- `woocommerce_list_orders`
- `woocommerce_get_stock_status`
- `woocommerce_sales_report`

Plus WordPress core tools:
- `wordpress_get_page` - scan checkout/cart pages
- `wordpress_list_plugins` - detect caching plugins
- `wordpress_get_theme_info` - check theme compatibility

## Related Skills

- Technical Debt Audit - general site cleanup
- Mobile Experience Report - mobile shopping experience
- WordPress Site DNA - full site archaeology

---

Built by Respira for WordPress
https://respira.press

**Note:** Requires WooCommerce add-on license to access WooCommerce-specific diagnostic tools.
