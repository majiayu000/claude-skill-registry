---
name: playwright-responsive-screenshots
description: |
  Captures screenshots at multiple viewport breakpoints for responsive design validation and
  documentation. Use when you need to test responsive layouts, validate mobile/tablet/desktop
  views, document design system breakpoints, or create visual regression test baselines.
  Triggers on "test responsive design", "screenshot at breakpoints", "capture mobile and
  desktop views", "responsive design testing", or "multi-device screenshots". Works with
  Playwright MCP tools (browser_navigate, browser_resize, browser_take_screenshot).

---

# Playwright Responsive Screenshots

## Quick Start

Capture screenshots across standard breakpoints in one command:

```
Capture responsive screenshots of https://example.com at mobile, tablet, and desktop breakpoints
```

This skill automates:
- Browser window resizing to standard breakpoints
- Layout settling wait times
- Full-page screenshot capture
- Organized file naming with breakpoint identifiers
- Optional comparison report generation

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. Standard Breakpoints
4. Instructions
   4.1. Basic Screenshot Capture
   4.2. Custom Breakpoints
   4.3. Multiple Pages
   4.4. With Comparison Report
5. Supporting Files
6. Expected Outcomes
7. Requirements
8. Red Flags to Avoid

## When to Use This Skill

**Explicit Triggers:**
- "Test responsive design for [URL]"
- "Screenshot at breakpoints"
- "Capture mobile and desktop views of [page]"
- "Validate responsive layout"
- "Generate screenshots for design review"

**Implicit Triggers:**
- User mentions testing across devices
- Request for multi-device validation
- Need to document responsive behavior
- Visual regression testing setup
- Design system breakpoint validation

**Debugging Scenarios:**
- Layout breaks at certain viewport widths
- Media query verification needed
- CSS breakpoint testing
- Responsive component validation

## What This Skill Does

This skill provides an automated workflow for capturing screenshots at multiple viewport sizes:

1. **Define breakpoints** - Use standard or custom viewport dimensions
2. **Navigate to target** - Open the URL in Playwright browser
3. **Resize and capture** - For each breakpoint: resize window, wait for layout, screenshot
4. **Organize output** - Name files with breakpoint identifiers (e.g., `homepage-mobile.png`)
5. **Generate report** - Optional comparison table with screenshot paths

**Key Benefits:**
- Consistent viewport sizes across captures
- Proper layout settling before screenshots
- Organized file naming convention
- Full-page screenshots by default
- Reproducible test results

## Standard Breakpoints

This skill uses industry-standard breakpoints by default:

| Device Category | Width × Height | Common Devices |
|----------------|----------------|----------------|
| **Mobile** | 375 × 667 | iPhone SE, iPhone 12/13/14 |
| **Tablet** | 768 × 1024 | iPad, iPad Mini, Android tablets |
| **Desktop** | 1920 × 1080 | Standard HD desktop/laptop |

**Breakpoint Selection Rationale:**
- Mobile: Most common iPhone viewport (covers ~40% of mobile traffic)
- Tablet: Standard iPad portrait orientation
- Desktop: 1080p standard (most common desktop resolution)

**When to Use Custom Breakpoints:**
- Testing specific device models
- Validating custom media query breakpoints
- Client-specific device requirements
- Edge case viewport testing (ultra-wide, small tablets, etc.)

## Instructions

### 4.1. Basic Screenshot Capture

**Workflow:**

1. **Define target and breakpoints**
   ```
   URL: https://example.com/page
   Breakpoints: mobile, tablet, desktop (standard)
   ```

2. **Navigate to page**
   - Use `browser_navigate` to open URL
   - Verify page loads successfully

3. **For each breakpoint:**
   - **Resize browser window** using `browser_resize`
   - **Wait for layout to settle** using `browser_wait_for` (1 second minimum)
   - **Capture full-page screenshot** using `browser_take_screenshot` with `fullPage: true`
   - **Name file descriptively**: `{page-name}-{breakpoint}.png`

4. **Organize screenshots**
   - Save to predictable location (e.g., `screenshots/`)
   - Group by page or breakpoint as appropriate

5. **Confirm completion**
   - Report number of screenshots captured
   - List file paths for user verification

**Example:**
```
User: "Capture responsive screenshots of https://myapp.dev/dashboard"

Assistant workflow:
1. browser_navigate to https://myapp.dev/dashboard
2. browser_resize(375, 667) → wait 1s → browser_take_screenshot("dashboard-mobile.png", fullPage: true)
3. browser_resize(768, 1024) → wait 1s → browser_take_screenshot("dashboard-tablet.png", fullPage: true)
4. browser_resize(1920, 1080) → wait 1s → browser_take_screenshot("dashboard-desktop.png", fullPage: true)
5. Report: "Captured 3 screenshots: dashboard-mobile.png, dashboard-tablet.png, dashboard-desktop.png"
```

### 4.2. Custom Breakpoints

**When user specifies custom viewport sizes:**

1. **Parse breakpoint specifications**
   - Accept formats: "414x896" or "414 x 896" or "width: 414, height: 896"
   - Validate dimensions are reasonable (width 200-3840, height 200-2160)

2. **Name custom breakpoints descriptively**
   - Use width for identifier: "homepage-414w.png"
   - Or use user-provided labels: "homepage-iphone14pro.png"

3. **Follow same workflow**
   - Navigate → Resize → Wait → Capture
   - Apply 1-second wait minimum after resize

**Example:**
```
User: "Screenshot https://app.com at 414x896 (iPhone 14 Pro) and 393x851 (Pixel 7)"

Assistant workflow:
1. browser_navigate to https://app.com
2. browser_resize(414, 896) → wait 1s → browser_take_screenshot("app-iphone14pro.png", fullPage: true)
3. browser_resize(393, 851) → wait 1s → browser_take_screenshot("app-pixel7.png", fullPage: true)
```

### 4.3. Multiple Pages

**For testing multiple pages at standard breakpoints:**

1. **Create page list**
   - Extract page names from URLs for file naming
   - Examples: "/dashboard" → "dashboard", "/settings/profile" → "settings-profile"

2. **Nested loop structure**
   - Outer loop: pages
   - Inner loop: breakpoints
   - Alternative: breakpoints outer, pages inner (user preference)

3. **Naming convention**
   - `{page-name}-{breakpoint}.png`
   - Example: `dashboard-mobile.png`, `dashboard-tablet.png`, `settings-mobile.png`

4. **Optimize navigation**
   - Navigate once per page (before breakpoint loop)
   - Resize/capture without re-navigating

**Example:**
```
User: "Capture responsive screenshots for /home, /products, and /about pages on https://shop.com"

Assistant workflow:
For each page in ["/home", "/products", "/about"]:
  1. browser_navigate to https://shop.com{page}
  2. For each breakpoint in [mobile, tablet, desktop]:
     - browser_resize(width, height)
     - browser_wait_for(1 second)
     - browser_take_screenshot("{page-name}-{breakpoint}.png", fullPage: true)

Result: 9 screenshots (3 pages × 3 breakpoints)
```

### 4.4. With Comparison Report

**Generate markdown report after screenshot capture:**

1. Capture screenshots (as above)
2. Create markdown table with embedded images and metadata
3. Save to `screenshots/report.md` (or user-specified location)
4. Include timestamp, URL, dimensions, and layout notes

See `examples/examples.md` for full report template example.

## Supporting Files

### references/playwright-api.md

Playwright MCP tool reference for screenshot operations:
- `browser_navigate` - Navigation and URL handling
- `browser_resize` - Viewport dimension control
- `browser_wait_for` - Waiting strategies for layout settling
- `browser_take_screenshot` - Screenshot capture options

### examples/examples.md

Comprehensive screenshot capture examples:
- Standard breakpoint captures
- Custom device viewports
- Multi-page workflows
- Report generation
- Edge cases (ultra-wide, mobile landscape, etc.)

### scripts/validate_screenshots.py

Python utility to validate screenshot dimensions match expected breakpoints.

## Expected Outcomes

### Successful Screenshot Capture

```
✅ Responsive Screenshots Captured

URL: https://example.com/homepage
Breakpoints: mobile, tablet, desktop
Pages: 1

Screenshots:
  ✓ homepage-mobile.png (375×667, 234KB)
  ✓ homepage-tablet.png (768×1024, 512KB)
  ✓ homepage-desktop.png (1920×1080, 1.2MB)

Location: /Users/username/screenshots/
Total time: 8.3 seconds

All screenshots captured successfully. Full-page screenshots enabled.
```

### With Comparison Report

```
✅ Responsive Screenshots Captured with Report

URL: https://shop.com
Breakpoints: mobile, tablet, desktop
Pages: 3 (/home, /products, /about)

Screenshots: 9 total
  ✓ home-mobile.png, home-tablet.png, home-desktop.png
  ✓ products-mobile.png, products-tablet.png, products-desktop.png
  ✓ about-mobile.png, about-tablet.png, about-desktop.png

Report: screenshots/report.md

View comparison report for side-by-side layout analysis.
```

### Validation Failure

```
❌ Screenshot Capture Failed

URL: https://broken-site.com
Issue: Page failed to load (timeout after 30s)

Breakpoint progress:
  ✗ mobile - not attempted (navigation failed)
  ✗ tablet - not attempted
  ✗ desktop - not attempted

Recommendation: Verify URL is accessible and site is responding.
```

## Requirements

**Playwright MCP Tools:**
- `browser_navigate` - Navigate to URLs
- `browser_resize` - Set viewport dimensions
- `browser_wait_for` - Wait for layout settling
- `browser_take_screenshot` - Capture screenshots

**Browser Requirements:**
- Playwright browser installed and configured
- Sufficient viewport size support (minimum 200×200, maximum 3840×2160)

**File System:**
- Write permissions for screenshot output directory
- Sufficient disk space (estimate ~1-2MB per desktop screenshot)

**Network:**
- Access to target URLs
- Stable connection for page loading

## Red Flags to Avoid

1. ❌ **Skipping layout settling wait** - Always wait minimum 1s after resize
2. ❌ **Not using fullPage: true** - Missing content below fold
3. ❌ **Inconsistent file naming** - Use `{page-name}-{breakpoint}.png`
4. ❌ **Unreasonable viewport dimensions** - Validate 200-3840 width, 200-2160 height
5. ❌ **Re-navigating for each breakpoint** - Navigate once, resize in loop
6. ❌ **Ignoring page load failures** - Verify navigation success first
7. ❌ **Missing screenshot organization** - Use dedicated output directory
8. ❌ **Not reporting file locations** - Provide absolute paths
9. ❌ **Forgetting viewport height** - Always specify both width and height
10. ❌ **Not validating custom breakpoints** - Parse and validate dimensions

## Notes

**Performance:** Adjust wait times (500ms static, 1s standard, 2-3s SPAs). Navigate once per page.
**Breakpoints:** Use actual device viewports, not arbitrary sizes. Document custom breakpoints.
**Quality:** PNG for UI (lossless), JPEG for photos (smaller). Screenshots serve as visual regression baselines.