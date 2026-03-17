---
name: seo-audit
description: "Run a full SEO audit on a website. Crawls the site, analyses technical SEO issues, compares with previous crawls, and generates an actionable report. Trigger with 'seo audit', 'audit seo', 'check seo', 'crawl site', or 'seo health check'."
compatibility: claude-code-only
---

# SEO Audit

Run a comprehensive technical SEO audit on a website using Whispering Wombat crawler and Jezweb Brain for client context.

## Required MCP Tools

- **Whispering Wombat**: `whispering_crawls`, `whispering_pages`, `whispering_issues`, `whispering_links`, `whispering_content`
- **Brain** (optional): `brain_site_get`, `brain_issues`

If Whispering Wombat MCP is not connected, inform the user and stop.

## Input

`$ARGUMENTS` should be a domain name or URL (e.g., `abpsychology.au` or `https://www.greenplanetplumbing.com.au`).

If no argument provided, ask the user which site to audit.

## Workflow

### Step 1: Resolve Domain and Get Context

Extract the domain from the input URL. Then:

1. **Brain lookup** (if available): `brain_site_get { domain }` — get client name, platform, previous issues, hosting
2. Note if it's a WordPress site (affects later steps)

### Step 2: Check for Recent Crawl

`whispering_crawls list` — look for a completed crawl of this domain within the last 24 hours.

- If recent crawl exists: reuse it (note the crawl_id)
- If no recent crawl: proceed to Step 3

### Step 3: Start New Crawl

```
whispering_crawls start {
  url: "https://{domain}",
  max_pages: 500,
  respect_robots: true
}
```

Then poll for completion:
```
whispering_crawls get { crawl_id: "..." }
```

Poll every 15 seconds. Typical times: 50 pages ~30s, 200 pages ~2min, 500 pages ~5min.

While waiting, inform the user: "Crawling {domain}... {pages_crawled}/{pages_found} pages"

### Step 4: Gather Analysis Data

Once crawl is complete, gather data in parallel where possible:

1. `whispering_issues overview` — SEO scores, status codes, security, response times
2. `whispering_issues summary` — all issue types with counts
3. `whispering_links stats` — follow/nofollow/broken/empty
4. `whispering_content sitemaps` — sitemap validation
5. `whispering_content structure` — URL tree and depth distribution

### Step 5: Deep Dive on Issues

Based on issues found, gather additional detail:

- If broken links > 0: `whispering_links domains` for external link analysis
- If duplicate content detected: `whispering_content duplicates`
- If WordPress: `whispering_content wordpress`
- If security issues: `whispering_content security`
- For top-traffic pages: `whispering_content pagespeed { url }` (max 3 pages)

### Step 6: Compare with Previous Crawl

`whispering_crawls history { crawl_id }` — get previous crawls.

If a previous completed crawl exists:
```
whispering_crawls compare {
  crawl_id: current_id,
  other_id: previous_id
}
```

Highlight: new issues, resolved issues, pages added/removed.

### Step 7: Generate Report

Output the report in this structure:

```markdown
# SEO Audit: {domain}
**Date**: {date} | **Pages crawled**: {count} | **Client**: {client_name or "N/A"}

## Site Health Summary
- SEO Score: {avg} (Good: {count}, OK: {count}, Poor: {count})
- Response Time: {avg}ms average
- Indexable Pages: {count}/{total}
- Broken Links: {count}
- Security: HSTS {yes/no}, CSP {yes/no}

## Critical Issues
{For each critical issue: description, affected URLs (max 5), how to fix}

## Warnings
{Same format, medium priority}

## Improvements
{Suggestions ranked by impact}

## Changes Since Last Crawl
{If comparison data available: new issues, resolved, pages added/removed}

## WordPress Status
{If WP site: plugin info, WP-specific issues}
```

### Step 8: Log to Brain (Optional)

If Brain is connected and critical issues were found, offer to log them:

```
brain_issues create {
  site_id: "...",
  subject: "SEO: {issue description}",
  description: "Found during SEO audit on {date}...",
  priority: "high",
  category: "seo"
}
```

## SEO Analysis Priorities

### Critical (always report)
- Broken pages (4xx/5xx responses)
- Missing/wrong canonical tags
- Noindex on important pages
- Missing H1 tags
- HTTPS mixed content
- Missing sitemap

### High
- Keyword cannibalisation (duplicate titles/H1s)
- Duplicate URL variants (/, /home, /index.html)
- Slow pages (>3s response)
- Missing meta descriptions on key pages
- Internal nofollow links

### Medium
- Title length issues
- Missing image alt text
- Missing JSON-LD schema
- Heading hierarchy issues
- Orphan pages (zero inlinks)

### Low
- Missing OG tags
- Long URLs
- Minor meta issues

## Notes

- Use Australian English (EN-AU)
- Be specific: "Fix missing H1 on /services" not "Add headings to pages"
- Focus on technical correctness, not keyword density or vanity scores
- For WordPress sites, cross-reference JezPress data if available
