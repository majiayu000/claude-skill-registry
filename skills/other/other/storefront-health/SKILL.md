---
name: storefront-health
description: Run a storefront performance audit with Lighthouse and Core Web Vitals analysis
user-invocable: true
---

You are helping the team run a performance audit on the Jocko Fuel storefront.

Follow these steps:

### Step 1: Identify Page to Audit

Ask the user which page(s) to audit. Common targets:
- Homepage (jockofuel.com)
- Product listing pages (collections)
- Product detail pages (specific products)
- Cart and checkout flow
- Custom landing pages

If the user says "everything," start with homepage + top 3 traffic pages.

### Step 2: Run Lighthouse Analysis

Delegate to the `performance-auditor` agent to run a Lighthouse audit on each page. Collect scores for:
- **Performance** (target: 90+)
- **Accessibility** (target: 90+)
- **Best Practices** (target: 90+)
- **SEO** (target: 90+)

For each category below target, capture the specific failing audits.

### Step 3: Check Core Web Vitals

Delegate to the `performance-auditor` agent to measure:
- **LCP** (Largest Contentful Paint) — target: < 2.5s
- **INP** (Interaction to Next Paint) — target: < 200ms
- **CLS** (Cumulative Layout Shift) — target: < 0.1
- **TTFB** (Time to First Byte) — target: < 800ms

Flag any metrics in "needs improvement" or "poor" ranges.

### Step 4: Analyze Theme Impact

Delegate to the `theme-analyzer` agent to check:
- Liquid template render complexity
- Unused CSS/JS being loaded
- Image optimization status (format, sizing, lazy loading)
- Font loading strategy

### Step 5: Generate Report

Compile results into a report with:
- **Executive summary**: Overall health score and top 3 issues
- **Scores table**: All Lighthouse scores by page
- **Core Web Vitals table**: All CWV metrics by page
- **Prioritized recommendations**: Ordered by impact and effort
- **Quick wins**: Changes that can be made immediately

### Error Handling

- If a page is behind authentication, ask the user for access or skip that page
- If Lighthouse fails to run, suggest using Chrome DevTools manually and provide instructions
- If metrics vary significantly between runs, note the variance and recommend multiple samples
