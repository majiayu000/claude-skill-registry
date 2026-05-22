---
name: browser-screenshot
description: This skill should be used when users need to capture screenshots of web pages. It supports full-page screenshots, viewport-specific captures, responsive screenshots across multiple device sizes, and element-specific screenshots. Use this skill for visual testing, documentation, design reviews, or any task requiring automated browser screenshots.
---

# Browser Screenshot

## Overview

Capture screenshots of web pages using Playwright with support for full-page capture, custom viewport sizes, responsive testing across multiple devices, and element-specific screenshots.

## When to Use This Skill

Use this skill when users request:
- Screenshots of web pages or URLs
- Visual testing across different screen sizes (mobile, tablet, desktop)
- Full-page captures including content below the fold
- Screenshots of specific page elements
- Documentation requiring webpage visuals
- Automated screenshot generation for reporting or testing

## Prerequisites

Before using this skill, ensure Playwright is installed:

```bash
pip install playwright
playwright install chromium
```

For other browsers (optional):
```bash
playwright install firefox
playwright install webkit
```

## Core Capabilities

### 1. Basic Screenshot

To capture a standard screenshot of a webpage:

```bash
python scripts/screenshot.py <URL> <output-path>
```

**Example:**
```bash
python scripts/screenshot.py https://example.com screenshot.png
```

This captures a viewport screenshot at the default size (1920x1080) with network idle waiting enabled.

### 2. Full-Page Screenshot

To capture the entire scrollable page content:

```bash
python scripts/screenshot.py <URL> <output-path> --full-page
```

**Example:**
```bash
python scripts/screenshot.py https://example.com/blog/post full-page.png --full-page
```

This is particularly useful for:
- Long articles or blog posts
- Landing pages with multiple sections
- Documentation pages
- Any page where content extends beyond the initial viewport

### 3. Custom Viewport Size

To capture screenshots at specific dimensions:

```bash
python scripts/screenshot.py <URL> <output-path> --width <WIDTH> --height <HEIGHT>
```

**Example:**
```bash
python scripts/screenshot.py https://example.com mobile-view.png --width 375 --height 667
```

Use custom viewports for:
- Testing specific device dimensions
- Matching design mockup sizes
- Custom resolution requirements

### 4. Responsive Screenshots (Multiple Viewports)

To capture the same page across multiple viewport sizes in a single command:

```bash
python scripts/screenshot.py <URL> <output-directory> --responsive <viewport1> <viewport2> ...
```

**Available viewport presets:**
- `mobile` - 375x667 (iPhone SE)
- `mobile-large` - 414x896 (iPhone 11)
- `tablet` - 768x1024 (iPad)
- `desktop-small` - 1366x768 (720p)
- `desktop` - 1920x1080 (1080p)

**Example:**
```bash
python scripts/screenshot.py https://example.com screenshots/ --responsive mobile tablet desktop
```

This creates three files in the `screenshots/` directory:
- `mobile.png`
- `tablet.png`
- `desktop.png`

Custom viewports can also be used with the `WIDTHxHEIGHT` format:
```bash
python scripts/screenshot.py https://example.com screenshots/ --responsive 1024x768 1440x900 mobile
```

### 5. Element-Specific Screenshot

To capture only a specific element on the page:

```bash
python scripts/screenshot.py <URL> <output-path> --element "<CSS-selector>"
```

**Example:**
```bash
python scripts/screenshot.py https://example.com header.png --element "header.main-header"
python scripts/screenshot.py https://example.com chart.png --element "#sales-chart"
```

Use element screenshots for:
- Isolating specific UI components
- Capturing charts or graphs
- Documenting individual page sections

### 6. Wait Conditions

Control when the screenshot is captured using various wait conditions:

**Wait for Network Idle (default):**
```bash
python scripts/screenshot.py https://example.com output.png
```

**Disable network idle waiting (faster, but may miss dynamic content):**
```bash
python scripts/screenshot.py https://example.com output.png --no-wait-network-idle
```

**Wait for a specific element to appear:**
```bash
python scripts/screenshot.py https://example.com output.png --wait-for-selector ".content-loaded"
```

**Add a custom delay:**
```bash
python scripts/screenshot.py https://example.com output.png --delay 2000
```

These options can be combined:
```bash
python scripts/screenshot.py https://example.com output.png --wait-for-selector ".main-content" --delay 1000
```

### 7. Browser Selection

By default, Chromium is used. To use a different browser:

```bash
python scripts/screenshot.py <URL> <output-path> --browser firefox
python scripts/screenshot.py <URL> <output-path> --browser webkit
```

## Common Usage Patterns

### Visual Regression Testing

Capture screenshots across multiple viewports for comparison:
```bash
python scripts/screenshot.py https://staging.example.com screenshots/staging/ --responsive mobile tablet desktop --full-page
python scripts/screenshot.py https://prod.example.com screenshots/prod/ --responsive mobile tablet desktop --full-page
```

### Documentation Generation

Capture specific UI components for documentation:
```bash
python scripts/screenshot.py https://app.example.com login-form.png --element "form.login"
python scripts/screenshot.py https://app.example.com dashboard.png --element "#dashboard-container"
```

### Design Review

Capture full pages with wait conditions for dynamic content:
```bash
python scripts/screenshot.py https://example.com design-review.png --full-page --wait-for-selector ".hero-animation-complete" --delay 500
```

### Responsive Design Testing

Test a new landing page across all common devices:
```bash
python scripts/screenshot.py https://example.com/new-landing responsive-test/ --responsive mobile mobile-large tablet desktop-small desktop --full-page
```

## Quick Reference

**Command structure:**
```bash
python scripts/screenshot.py <URL> <output> [options]
```

**Common options:**
- `-f, --full-page` - Capture entire scrollable page
- `-w, --width` - Viewport width in pixels
- `-h, --height` - Viewport height in pixels
- `-r, --responsive` - Multiple viewport captures
- `-e, --element` - Screenshot specific element
- `--wait-for-selector` - Wait for CSS selector
- `-d, --delay` - Delay in milliseconds
- `-b, --browser` - Browser choice (chromium/firefox/webkit)
- `--no-wait-network-idle` - Skip network idle wait

**Get full help:**
```bash
python scripts/screenshot.py --help
```

## Implementation Approach

When users request screenshots:

1. Determine the screenshot type needed (viewport, full-page, responsive, or element-specific)
2. Identify any wait conditions required (network idle, specific selectors, delays)
3. Select appropriate viewport size(s) or use responsive mode for multiple sizes
4. Construct the command with appropriate options
5. Execute the script using the Bash tool
6. Verify the output file(s) were created successfully
7. Inform the user of the screenshot location(s)

For complex scenarios involving multiple pages or repeated screenshots, consider creating a wrapper script that calls `screenshot.py` multiple times with different parameters.

## Troubleshooting

**Common issues:**

- **"Playwright not found"**: Run `pip install playwright && playwright install chromium`
- **Element not found**: Verify the CSS selector is correct; use `--wait-for-selector` if the element loads dynamically
- **Blank screenshots**: Increase `--delay` or ensure `--wait-for-network-idle` (default) is enabled
- **Timeout errors**: The page may be taking too long to load; try `--no-wait-network-idle` or increase timeout in the script if needed
- **Browser not found**: Run `playwright install <browser-name>` for the desired browser

## Resources

### scripts/screenshot.py

The main screenshot tool that handles all screenshot operations using Playwright. The script can be executed directly without loading into context, though reading it may be helpful for understanding capabilities or making environment-specific adjustments.
