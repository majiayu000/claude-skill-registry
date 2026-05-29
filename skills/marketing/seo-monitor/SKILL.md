---
name: seo-monitor
description: "Batch monitor SEO health across all active client sites. Checks for regressions, starts fresh crawls for stale data, and generates a summary report. Trigger with 'seo monitor', 'check all seo', 'seo batch check', 'weekly seo', or 'monitor sites'."
compatibility: claude-code-only
---

# SEO Monitor

Batch check SEO health across all active Jezweb client sites. This is the weekly monitoring workflow — identifies sites with new issues, regressions, or stale crawl data.

## Required MCP Tools

- **Whispering Wombat**: `whispering_crawls`, `whispering_issues`
- **Brain**: `brain_sites` (to get active site list)
- **Google Chat** (optional): Post summary to SEO Ideas space

## Workflow

### Step 1: Get Active Sites

Use Brain to find sites that need SEO monitoring:

```
brain_sites find { status: "active", limit: 100 }
```

If Brain is not available, use `whispering_crawls list` and extract unique domains from recent crawls.

### Step 2: Check Each Site

For each site, check crawl freshness and health:

1. `whispering_crawls list` — find most recent crawl for this domain
2. Categorise:
   - **Fresh** (crawled < 7 days ago): check issues only
   - **Stale** (crawled > 7 days ago): start new crawl
   - **Never crawled**: start first crawl

For fresh sites:
- `whispering_issues summary { crawl_id }` — get issue counts
- If previous crawl exists: `whispering_crawls compare` — check for regressions

For stale sites:
- `whispering_crawls start { url, max_pages: 200 }` — lighter crawl for monitoring
- Note: don't wait for all crawls to complete — queue them and check later

### Step 3: Identify Concerns

Flag sites that need attention:

**Red flags** (report immediately):
- New 5xx errors since last crawl
- Significant increase in broken links (>5 new)
- Previously indexed pages now noindexed
- SEO score dropped by >10 points
- Site returning errors/timeouts

**Yellow flags** (note for review):
- New 4xx errors (>3)
- Missing sitemaps
- New duplicate content
- Score declined by 5-10 points

### Step 4: Generate Summary

Output a monitoring summary:

```markdown
# SEO Monitoring Report — {date}

## Sites Needing Attention
| Site | Issue | Severity | Change |
|------|-------|----------|--------|
| example.com | 5 new broken links | Red | +5 since last week |

## Crawl Status
- Fresh (< 7 days): {N} sites
- Stale (> 7 days): {N} sites — crawls started
- Never crawled: {N} sites — crawls started

## Overall Health
- Sites with critical issues: {N}
- Sites with warnings: {N}
- Healthy sites: {N}

## New Crawls Started
{List of domains where fresh crawls were initiated}
```

### Step 5: Communicate (Optional)

If Google Chat is available, post the summary to the SEO Ideas space.

Format for Google Chat (use their markdown):
```
*SEO Monitor — {date}*

*{N} sites need attention:*
• {domain} — {issue summary}
• {domain} — {issue summary}

_{N} fresh, {N} stale (crawls started), {N} healthy_
```

## Configuration

Default monitoring parameters:
- Max pages per monitoring crawl: 200 (lighter than full audit)
- Stale threshold: 7 days
- Max concurrent crawl starts: 5 (don't overwhelm WW)
- Rate limit per crawl: 2 req/s

## Notes

- Run this weekly (or trigger manually)
- Don't log individual issues to Brain during monitoring — only flag regressions
- If a site has critical regressions, suggest running `/seo-audit {domain}` for full analysis
- Keep the summary concise — it's a triage tool, not a full report
