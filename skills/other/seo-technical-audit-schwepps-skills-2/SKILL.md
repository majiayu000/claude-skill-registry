---
name: seo-technical-audit
description: Professional technical SEO audit that analyzes crawlability, Core Web Vitals, site architecture, mobile readiness, security, structured data, and AI crawler configuration. Use when auditing websites for technical SEO issues, diagnosing indexation problems, or preparing comprehensive SEO reports.
license: MIT
metadata:
  author: Schwepps
  version: "1.0.0"
  category: marketing
  tags: seo, technical-seo, audit, core-web-vitals, crawlability
---

# Technical SEO Audit Framework

Professional methodology for comprehensive technical SEO analysis aligned with 2025 best practices.

## When to Use This Skill

- Full technical SEO audits
- Diagnosing crawling/indexation issues
- Core Web Vitals analysis
- Site architecture review
- Schema markup validation
- Mobile-first readiness assessment
- AI crawler configuration audit

## Audit Workflow

Execute in priority order—crawlability issues block all downstream optimizations.

### Phase 1: Crawlability & Indexation (CRITICAL)

```
1. robots.txt Analysis
   □ Accessible at /robots.txt
   □ No global Disallow: /
   □ CSS/JS not blocked
   □ Sitemap reference present

2. XML Sitemap Validation
   □ Only canonical, 200-status URLs
   □ No noindex pages included
   □ Submitted to GSC

3. Indexation Status (GSC)
   □ Check indexed vs excluded pages
   □ Identify "Crawled - not indexed"
   □ Find soft 404s
   □ Verify canonical consistency

4. Meta Robots
   □ Key pages: index,follow
   □ No accidental noindex
   □ Canonical self-references
```

### Phase 2: Core Web Vitals (2025 Standards)

**Passing Thresholds:**
| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | ≤2.5s | 2.5-4.0s | >4.0s |
| INP | ≤200ms | 200-500ms | >500ms |
| CLS | ≤0.10 | 0.10-0.25 | >0.25 |

**Data Sources (Priority Order):**
1. Google Search Console (field data)
2. CrUX Dashboard (field data)
3. PageSpeed Insights (lab + field)

**Common Fixes:**
- LCP: Optimize images, preload critical resources, reduce server response time
- INP: Break up long tasks, optimize JavaScript, use web workers
- CLS: Set dimensions on images/embeds, avoid inserting content above existing

### Phase 3: Site Architecture

```
Optimal Structure:
□ Max 3 clicks from homepage to any page
□ Flat hierarchy (avoid deep nesting)
□ Logical URL structure: /category/subcategory/page
□ Breadcrumb navigation implemented
□ Internal linking strategy documented

URL Best Practices:
□ Descriptive, keyword-relevant
□ Lowercase, hyphens (not underscores)
□ Under 60 characters
□ No parameters when possible
```

### Phase 4: Mobile-First Readiness

```
□ Mobile-friendly test passes
□ Responsive design (no horizontal scroll)
□ Touch targets ≥48px
□ Font size ≥16px base
□ No intrusive interstitials
□ Same content on mobile and desktop
```

### Phase 5: Security & HTTPS

```
□ HTTPS with valid certificate
□ HTTP → HTTPS redirects (301)
□ No mixed content warnings
□ HSTS header implemented
□ Security headers present (CSP, X-Frame-Options)
```

### Phase 6: Structured Data

**Priority Schema Types:**
1. Organization/LocalBusiness
2. BreadcrumbList
3. Article/BlogPosting (with author)
4. Product (for e-commerce)
5. FAQPage (for AI visibility)
6. HowTo (for tutorials)

**Validation:**
- Google Rich Results Test
- Schema.org validator
- Check for warnings, not just errors

### Phase 7: AI Crawler Configuration

**2025 robots.txt for AI Search:**
```
# Allow AI search crawlers
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# Optional: Block AI training (not search)
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /
```

## Output Format

Generate reports using this structure:

```markdown
# Technical SEO Audit Report

**Site:** [URL]
**Date:** [Date]
**Overall Score:** X/100

## Executive Summary
[2-3 sentence overview]

## Scores by Category

| Category | Score | Status |
|----------|-------|--------|
| Crawlability & Indexation | X/20 | [Good/Needs Work/Critical] |
| Core Web Vitals | X/20 | [Good/Needs Work/Critical] |
| Site Architecture | X/15 | [Good/Needs Work/Critical] |
| Mobile Readiness | X/15 | [Good/Needs Work/Critical] |
| Security & HTTPS | X/10 | [Good/Needs Work/Critical] |
| Structured Data | X/10 | [Good/Needs Work/Critical] |
| AI Crawler Readiness | X/10 | [Good/Needs Work/Critical] |

## Priority Issues (Fix First)
1. **[Issue]** - [Impact] - [Fix]
2. **[Issue]** - [Impact] - [Fix]
3. **[Issue]** - [Impact] - [Fix]

## Detailed Findings
[Category-by-category analysis]

## Action Plan

**Immediate (This Week):**
- [ ] Critical fix 1
- [ ] Critical fix 2

**Short-term (This Month):**
- [ ] High priority 1
- [ ] High priority 2

**Ongoing:**
- [ ] Monitoring task 1
- [ ] Regular audit 2
```

## Scoring Guide

- **90-100:** Excellent - Minor optimizations only
- **70-89:** Good - Some improvements needed
- **50-69:** Needs Work - Significant gaps
- **Below 50:** Critical - Major overhaul required

## Quick Audit (5-Point Check)

For rapid assessments:
1. **Indexation** - Are key pages indexed? (GSC)
2. **Speed** - Core Web Vitals passing? (LCP <2.5s)
3. **Mobile** - Mobile-friendly test pass?
4. **Security** - HTTPS with valid cert?
5. **Crawlability** - robots.txt not blocking content?

## Tools Reference

```bash
# Check robots.txt
curl -s https://example.com/robots.txt

# Check response headers
curl -I https://example.com

# Fetch and validate sitemap
curl -s https://example.com/sitemap.xml | head -50

# Check mobile-friendliness (requires API key)
# Use Google's Mobile-Friendly Test: https://search.google.com/test/mobile-friendly
```

## Additional Resources

For detailed checklists and schema patterns, ask for:
- "Show me the full crawlability checklist"
- "Give me JSON-LD schema examples"
- "List all Core Web Vitals optimization techniques"
