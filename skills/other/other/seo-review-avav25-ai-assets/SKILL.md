---
name: seo-review
description: SEO review workflow — technical SEO audit, meta tags, structured data validation, Core Web Vitals, crawlability, indexability, AI search readiness. Applies SEO Engineer role. Use standalone or as part of feature/docs workflows.
allowed-tools: Read, Grep, Glob, Bash
argument-hint: [URL or page path]
---

# SEO Review

Systematic SEO audit for public-facing pages. Checks crawlability, indexability, on-page SEO, structured data, Core Web Vitals, and AI search readiness. Applies `Agent(seo-engineer)` for all steps.

Works standalone or as a sub-workflow called by `/docs`, `/feature-dev`, or `/bugfix`.

## 1. Define Scope

Ask the user (or extract from parent workflow):

- **Target pages**: Specific URLs, page group, or entire site
- **Environment**: Local dev / staging / production
- **Review type**: Full audit / metadata only / structured data / performance / AI search
- **Constraints**: What must not change (URL structure, navigation, etc.)

## 2. Apply Roles

Apply `Agent(seo-engineer)` as primary role.

If implementation changes are needed, delegate to:

| Change Type | Delegate To |
|---|---|
| Frontend code (meta tags, JSON-LD, components) | `Agent(frontend-engineer)` |
| Content / copy improvements | `Agent(content-writer)` |
| Server config (redirects, headers, robots.txt) | `Agent(devops-engineer)` |
| Architecture changes (URL structure, routing) | `Agent(solution-architect)` |

## 3. Baseline Audit

Run automated checks before making changes.

### 3a. Crawlability

Check the following (read project files or use browser/curl):

- `robots.txt` — allows important pages, `Sitemap:` directive present
- XML sitemap — includes all indexable pages, excludes non-indexable
- No orphaned pages (all pages reachable via internal links)
- Navigation uses crawlable `<a href>` links
- No crawl traps (infinite URL parameters, calendar widgets)

### 3b. Indexability

- No accidental `noindex` on public pages
- Canonical tags point to correct URLs
- No canonical conflicts (canonical vs redirects vs internal links)
- Pages return 200 status codes (check for soft 404s)
- Critical content rendered server-side (SSR/SSG), not client-only

### 3c. On-Page SEO

For each target page:

| Element | Check |
|---|---|
| Title tag | Unique, descriptive, matches page intent |
| Meta description | Unique, compelling, relevant |
| H1 | Exactly one per page, matches topic |
| Heading hierarchy | Logical H1→H2→H3 |
| Image alt text | Descriptive for all meaningful images |
| Internal links | Present, descriptive anchor text |
| Outbound links | Qualified with `rel` attributes where needed |

### 3d. Structured Data

- JSON-LD present where applicable:
  - `Organization` / `WebSite` on homepage
  - `Article` / `BlogPosting` on blog posts
  - `BreadcrumbList` for navigation
  - `FAQ` where genuinely useful
  - `Product`, `Review`, `HowTo` where applicable
- Structured data matches visible page content (no misleading markup)
- Validate with [Rich Results Test](https://search.google.com/test/rich-results)

### 3e. Core Web Vitals

| Metric | Target | Tool |
|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | PageSpeed Insights |
| INP (Interaction to Next Paint) | < 200ms | PageSpeed Insights |
| CLS (Cumulative Layout Shift) | < 0.1 | PageSpeed Insights |

### 3f. Mobile Optimization

- Responsive design across viewports
- Tap targets ≥ 48×48px
- No horizontal scrolling
- Font size ≥ 16px body text
- No intrusive interstitials

### 3g. AI Search Readiness

- Pages crawlable and well-structured (SSR/SSG, semantic HTML)
- Content is clear, factual, and authoritative
- Structured data present and accurate
- `llms.txt` present (optional, experimental — not a ranking factor)
- Pages indexed and snippet-eligible (prerequisite for AI features)

## 4. Present Findings

Compile audit results:

```
## SEO Audit Report

### Pages Reviewed: [count]

### Critical Issues (blocking indexing/ranking)
- [ ] [issue] — [affected page] — [fix]

### Warnings (affecting quality/performance)
- [ ] [issue] — [affected page] — [fix]

### Opportunities (improvements)
- [ ] [opportunity] — [affected page] — [recommendation]

### Scores
- Crawlability: [OK / issues found]
- Indexability: [OK / issues found]
- On-Page SEO: [OK / issues found]
- Structured Data: [OK / missing / errors]
- Core Web Vitals: [LCP: Xs, INP: Xms, CLS: X.XX]
- Mobile: [OK / issues found]
- AI Search: [OK / opportunities]
```

Wait for user to review and approve which fixes to implement.

## 5. Implement Fixes

For approved fixes:

1. **Metadata changes** (title, description, OG tags) — implement directly or delegate to `Agent(frontend-engineer)`
2. **Structured data** (JSON-LD) — implement directly or delegate to `Agent(frontend-engineer)`
3. **Content changes** — delegate to `Agent(content-writer)`
4. **Server config** (redirects, headers) — delegate to `Agent(devops-engineer)`
5. **Performance fixes** (image optimization, lazy loading, critical CSS) — delegate to `Agent(frontend-engineer)`

Follow `Agent(seo-engineer)` standards for all changes. No black-hat techniques.

## 6. Verify

Re-run relevant checks from Step 3 for changed pages:

- [ ] Fixed issues no longer present
- [ ] No new issues introduced
- [ ] Structured data validates (Rich Results Test)
- [ ] Pages still indexable (no accidental noindex)
- [ ] Core Web Vitals within targets
- [ ] No broken links introduced

## 7. Summary

```
## SEO Review Summary
- **Scope**: [pages/environment reviewed]
- **Issues found**: [critical: X, warnings: X, opportunities: X]
- **Fixes applied**:
  - [fix 1] — [page]
  - [fix 2] — [page]
- **Delegated to**: [roles involved]
- **Verification**: [pass/fail per check]
- **Monitoring**: [what to watch — Search Console, PageSpeed, etc.]
- **Follow-ups**: [items for future attention]
```

## Integration

- **Roles**: `Agent(seo-engineer)` (primary), `Agent(frontend-engineer)` (implementation), `Agent(content-writer)` (content fixes)
- **Called by**: `/feature-dev` (SEO-relevant features), `/docs` (public content)
