---
name: bake-site-compare
description: Compare production WordPress sites against their baked static versions to find differences. Use when testing Bake deployments, checking for missing assets, broken styles, console errors, or any visual/functional discrepancies between production and static sites. Triggers on requests to compare sites, verify bake output, check for differences, or test static deployments.
---

# Bake Site Comparison

Compare a production WordPress site against its baked static version to ensure they're visually and functionally identical.

## Prerequisites

- Browser automation MCP must be available (Playwright or claude-in-chrome)
- Access to the bake.kdl config file at `/Users/coreyja/Projects/bake/bake.kdl`

## Workflow

### 1. Parse Site Configuration

Read `/Users/coreyja/Projects/bake/bake.kdl` to get:
- **Production URL**: The `production` field (e.g., `https://theconnectedapproach.com`)
- **Baked URL**: The `alternative-hosts` entry ending in `.lavenderiguana.live` (e.g., `tca.lavenderiguana.live`)
- **CDN Allowlist**: External domains that should NOT be rewritten (important for checking asset loading)

If user specifies a site name (e.g., "tca", "lavenderiguana"), use that site's config. Otherwise, ask which site to compare.

### 2. Discover All Pages

Get all pages to compare using one of:
- Fetch and parse `/sitemap.xml` from production site
- Fetch and parse `/sitemap_index.xml` if it's a sitemap index
- Include key pages: `/`, `/contact/`, and any pages from sitemap

### 3. Compare Each Page

For each page, compare production vs baked version:

#### Visual Comparison
1. Navigate to production URL in one tab
2. Navigate to corresponding baked URL in another tab
3. Take screenshots of both
4. Scroll down incrementally, taking screenshots at each section
5. Note any visual differences (missing images, broken layouts, different text)

#### Network Analysis
1. Check for 404 errors on the baked site
2. Check for failed resource loads (CSS, JS, images, fonts)
3. Compare network requests - anything loading on production but failing on baked

#### Console Errors
1. Capture console errors/warnings from both sites
2. Flag any errors unique to the baked version

#### Specific Checks

**FontAwesome Icons:**
```javascript
// Check if FontAwesome icons are rendering
document.querySelectorAll('[class*="fa-"]').length
// Check FontAwesome stylesheets loaded
Array.from(document.styleSheets).filter(s => s.href?.includes('fontawesome')).map(s => s.href)
```

**Lazy-Loaded Images:**
```javascript
// Check for images with data-src/data-srcset (WordPress lazy loading)
document.querySelectorAll('img[data-src], img[data-srcset]').length
// Verify actual src is populated after scroll
document.querySelectorAll('img').forEach(img => {
  if (img.dataset.src && !img.src.includes(img.dataset.src)) {
    console.log('Lazy image not loaded:', img.dataset.src);
  }
});
```

**Background Images:**
```javascript
// Check for elements with background-image in inline styles
document.querySelectorAll('[style*="background"]').length
// Check Elementor data-settings for background images
document.querySelectorAll('[data-settings]').forEach(el => {
  const settings = JSON.parse(el.dataset.settings || '{}');
  if (settings.background_image) console.log('BG:', settings.background_image);
});
```

**Elementor Forms:**
```javascript
// Check if Elementor Pro frontend config exists and has correct ajaxurl
window.ElementorProFrontendConfig?.ajaxurl
// On baked sites, this should point to the form handler service, not WordPress
```

**External Resources:**
```javascript
// Check if CDN resources are loading (should NOT be rewritten to /external/)
Array.from(document.querySelectorAll('link[href], script[src]'))
  .filter(el => (el.href || el.src)?.includes('/external/'))
  .map(el => el.href || el.src)
```

### 4. Document Findings

For each difference found, record:
- Page URL (both production and baked)
- Type of issue (visual, network, console, specific check)
- Screenshot or evidence
- Severity (blocking vs cosmetic)

### 5. Create Linear Issues

For each significant issue, create a Linear issue in the Bake project:

```
Team: Bake (or appropriate team)
Title: [BAKE-XXX] Brief description of the issue
Labels: bug, site-comparison
Description:
  - Production URL: [url]
  - Baked URL: [url]
  - Issue: [detailed description]
  - Evidence: [screenshot/console output/network log]
  - Affected pages: [list if multiple]
```

Group related issues (e.g., if the same asset is missing on multiple pages, create one issue).

## Known Issue Patterns

### FontAwesome Icons Not Rendering
- **Cause**: CDN URLs being rewritten to `/external/` paths when they should be allowed
- **Check**: Verify domain is in `cdn-allowlist` in bake.kdl
- **Issue prefix**: BAKE-018

### Lazy-Loaded Images Missing
- **Cause**: `data-src`/`data-srcset` attributes not being processed
- **Check**: Compare img element attributes between production and baked
- **Issue prefix**: BAKE-022

### CSS Background Images Missing
- **Cause**: Inline styles or Elementor data-settings JSON not being parsed
- **Check**: Look for missing hero sections, client logos, background patterns
- **Issue prefix**: BAKE-023

### Elementor Forms Not Working
- **Cause**: `ajaxurl` pointing to WordPress instead of form handler
- **Check**: Verify `ElementorProFrontendConfig.ajaxurl` value
- **Issue prefix**: BAKE-019

### External Domain Assets 404
- **Cause**: External URLs rewritten but not downloaded to correct path
- **Check**: Network tab for 404s on `/external/` paths
- **Issue prefix**: BAKE-021

## Output Format

After comparison, provide a summary:

```
## Site Comparison Results: [site-name]
Production: [url]
Baked: [url]

### Pages Checked: X

### Issues Found: Y
- [Issue 1]: Brief description (Linear: BAKE-XXX)
- [Issue 2]: Brief description (Linear: BAKE-XXX)

### All Clear:
- FontAwesome: OK/Issues
- Lazy Images: OK/Issues
- Background Images: OK/Issues
- Forms: OK/Issues
- Console Errors: OK/Issues
- Network 404s: OK/Issues

### Linear Issues Created:
- BAKE-XXX: [title]
- BAKE-YYY: [title]
```
