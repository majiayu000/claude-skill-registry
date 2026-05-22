---
name: website-audit
description: A comprehensive auditing suite for the JupitLunar website. It performs deep scans for broken links, console errors, accessibility issues, SEO compliance, and feature verification. Use this when the user asks to "audit the website", "check for broken links", "verify features", or "do a health check".
---

# Website Audit Skill

This skill provides a complete auditing toolkit for the JupitLunar website. It combines internal unit tests with a dynamic crawler to ensure the site is healthy, performant, and error-free.

## Capabilities

1.  **Dynamic Crawler (`audit-scout.js`)**:
    *   🕷️ **Link Checking**: Crawls the entire site to find broken internal and external links.
    *   🚨 **Error Detection**: Captures runtime console errors and unhandled exceptions on every page.
    *   🖼️ **Asset Validation**: Checks for missing images and broken media.
    *   ⚡ **Performance**: specific page load checks.

2.  **System Health Suite (Existing Tests)**:
    *   Utilization of the robust `npm run test:all` suite covering SEO, API, Admin, and Search.

## How to Use

### 1. The Full "Deep" Audit

This is the recommended command for a complete checkup. It runs the system tests AND the dynamic crawler.

**Prerequisite**: Ensure the local development server is running on `http://localhost:3001`.

```bash
# Start the server in a separate terminal if not running
# npm run dev -- -p 3001

# Run the full audit
cd nextjs-project
node ../.agent/skills/website-audit/scripts/audit-scout.js
```

### 2. Audit specific features

If you only want to check specific aspects:

**Check SEO Rules:**
```bash
node scripts/test-seo.js
```

**Check API Endpoints:**
```bash
node scripts/test-api.js
```

**Check Analytics:**
```bash
node scripts/test-analytics.js
```

### 3. Browser Verification (Final Step)

After automated tools accept the build, use the `browser_subagent` to perform a "sanity check" that mimics real user behavior. Automated crawlers can miss visual bugs or interaction issues.

**Instructions for the Agent:**

1.  **Launch Browser**: Open `http://localhost:3001`.
2.  **Navigation Check**: Click through the main navigation menu items (Home, Features, Pricing, About, etc.) to ensure pages render visually correct.
3.  **Interaction Check**:
    -   Click a few "Call to Action" buttons.
    -   Test a simple form (e.g., newsletter signup) if safe/idempotent.
    -   Verify that no "Application Error" overlays appear.
4.  **Visual Confirmation**: Take a screenshot if something looks suspicious.

## Interpreting Results

The `audit-scout.js` will generate a report in the console (and optionally a JSON file).

- **🔴 CRITICAL**: 404s on internal pages, 500 API errors, React hydration errors.
- **🟡 WARNING**: Slow page loads, missing alt text, non-critical console warnings.
- **🟢 PASS**: All checks passed.
