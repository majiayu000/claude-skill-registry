---
name: marketing-seo-complete
description: Complete SEO skill for technical audits (Core Web Vitals, site speed, crawlability/indexation, robots/sitemaps/canonicals, structured data, mobile, security, internal linking), SEO marketing strategy (keyword research, content planning, competitive analysis, E-E-A-T), operational workflows (cross-team collaboration, OKRs), link building, local SEO, international SEO (hreflang), and multi-platform SEO (Google, YouTube, Reddit, social). Updated for January 2026.
---

# SEO Technical and Marketing - Operational Skill

This skill contains **actionable, production-ready systems** for **traditional search engine optimization**:

- **Technical SEO auditing** (Core Web Vitals, crawlability, structured data, mobile optimization)
- **SEO marketing strategy** (keyword research, content planning, competitive analysis, brand building)
- **Operational workflows** (cross-team collaboration, stakeholder alignment, SEO OKRs)
- **Total Search Optimization** (Google, YouTube, Reddit, TikTok, forums, social SEO)

**Structure**: Technical fundamentals first -> Marketing strategy -> Operational execution -> Total Search Optimization.

**For AI search optimization** (ChatGPT, Perplexity, Gemini, AI Overviews, GEO): Use [marketing-ai-search-optimization](../marketing-ai-search-optimization/SKILL.md) instead.

---

## 2026 Operating Assumptions (Evergreen)

- Prioritize usefulness and intent satisfaction; technical SEO cannot compensate for weak content.
- E-E-A-T matters most when claims can impact money, health, safety, or major decisions; for all niches, show real experience and verifiable proof where possible.
- Mobile-first is the default: performance, UX, and rendering on mobile are the primary gate.
- Crawl/indexation wins come from discoverability (internal links, sitemaps) and removing low-value crawl traps.
- Core Web Vitals are a weak signal but a strong tiebreaker; fix regressions and obvious failures.
- Structured data is for eligibility and rich results, not a ranking boost; use it to improve extraction and display.
- SERPs are multi-surface (web, video, local, forums, social); measure channel-by-channel, not only rankings.

Primary sources live in `data/sources.json`. For time-sensitive changes (core updates, reporting changes), use official sources first (Google Search Central / Search Status Dashboard); if your environment supports web search, refresh against current updates before giving definitive advice.

### Key Thresholds (2026)

| Metric | Target | Impact |
|--------|--------|--------|
| LCP | < 2.5s | Mobile-first indexing threshold |
| INP | < 200ms | Replaced FID; user engagement signal |
| CLS | < 0.1 | Layout stability; ranking factor |
| TTFB | < 600ms | Crawl rate: slow servers often reduce pages crawled/day |
| Mobile score | > 90 | Required for competitive rankings |

---

## When NOT to Use

- **Pure AI platform optimization** (ChatGPT, Perplexity, Gemini visibility) -> Use [marketing-ai-search-optimization](../marketing-ai-search-optimization/SKILL.md)
- **Paid search campaigns** (Google Ads, Bing Ads) -> Use [marketing-paid-advertising](../marketing-paid-advertising/SKILL.md)
- **Social media strategy** (non-SEO focused) -> Use [marketing-social-media](../marketing-social-media/SKILL.md)
- **Content creation process** (writing, editing, publishing) -> Use [marketing-content-strategy](../marketing-content-strategy/SKILL.md)
- **Email marketing** -> Use [marketing-email-automation](../marketing-email-automation/SKILL.md)

---

## Quick Reference

| Task | Resource/Template | Location | When to Use |
|------|------------------|----------|-------------|
| **Auditing** | | | |
| Full Technical Audit | 10-Point Checklist | `assets/audits/full-technical-audit.md` | Comprehensive site-wide audit |
| Quick Audit | Abbreviated Checklist | `assets/audits/quick-audit-checklist.md` | Fast issue identification |
| Priority Matrix | Impact vs Effort | `assets/priority/impact-effort-matrix.md` | Prioritize audit findings |
| **Core Web Vitals** | | | |
| CWV Deep Dive | CWV Guide | `references/core-web-vitals-guide.md` | LCP, INP, CLS optimization |
| CWV Report | Report Template | `assets/cwv/core-web-vitals-report.md` | Document CWV findings |
| **Crawlability** | | | |
| Indexation Issues | Crawlability Guide | `references/crawlability-indexing.md` | Robots.txt, sitemaps, GSC issues |
| Indexation Acceleration | Fast Indexing Guide | `references/crawlability-indexing.md#indexation-acceleration` | New/large sites, internal linking, E-E-A-T |
| **Performance** | | | |
| Site Speed | Speed Guide | `references/site-speed-optimization.md` | TTFB, render-blocking, images |
| **Technical Setup** | | | |
| Mobile Optimization | Mobile Guide | `references/mobile-seo-guide.md` | Responsive, viewport, mobile-first |
| Structured Data | Schema Guide | `references/structured-data-guide.md` | JSON-LD, rich snippets |
| Schema Report | Validation Template | `assets/schema/schema-validation-report.md` | Document schema findings |
| Security/HTTPS | Security Guide | `references/security-https-guide.md` | HTTPS, HSTS, headers |
| **Architecture** | | | |
| Internal Linking | Link Strategy | `references/internal-linking-strategy.md` | Link equity, orphan pages |
| Duplicate Content | Canonical Guide | `references/duplicate-content-handling.md` | Canonicals, pagination |
| International SEO | Hreflang Guide | `references/internationalization-hreflang.md` | Multi-language/region sites |
| **Link Building** | | | |
| Link Acquisition | Link Building Guide | `references/link-building-strategy.md` | Backlinks, digital PR, HARO |
| **Local SEO** | | | |
| Google Business Profile | Local SEO Guide | `references/local-seo-guide.md` | GBP, citations, reviews, local pack |

---

## 10-Point Audit Framework

Every technical SEO audit follows this systematic checklist:

| # | Area | Key Metrics | Weight |
|---|------|-------------|--------|
| 1 | **Crawlability** | robots.txt status, sitemap coverage, crawl budget | High |
| 2 | **Core Web Vitals** | LCP <2.5s, INP <200ms, CLS <0.1 | High |
| 3 | **Site Speed** | TTFB <800ms, FCP <1.8s, Speed Index | High |
| 4 | **Mobile** | Mobile-friendly score, viewport, touch targets | High |
| 5 | **Security** | HTTPS, mixed content, HSTS, headers | Medium |
| 6 | **Structured Data** | Schema validity, rich snippet eligibility | Medium |
| 7 | **On-Page** | Meta tags, heading hierarchy, keyword signals | Medium |
| 8 | **Architecture** | Internal links, URL structure, canonicals | High |
| 9 | **Duplicate Content** | Canonical implementation, pagination | Medium |
| 10 | **Internationalization** | Hreflang (if applicable), geo-targeting | Low |

**Scoring**: Rate each area 0-10, calculate weighted average for overall Technical Health Score.

---

## Decision Trees

```text
### Audit Type Selection
Full site audit needed
  -> Use assets/audits/full-technical-audit.md
Quick issue check
  -> Use assets/audits/quick-audit-checklist.md
CWV-only deep dive
  -> Use assets/cwv/core-web-vitals-report.md
Schema validation only
  -> Use assets/schema/schema-validation-report.md

### Core Web Vitals Failing
LCP >2.5s
  -> Preload LCP element, optimize images, add CDN
  -> See references/core-web-vitals-guide.md
INP >200ms
  -> Reduce JavaScript, optimize event handlers
  -> See references/core-web-vitals-guide.md
CLS >0.1
  -> Add dimensions to images/ads, avoid layout shifts
  -> See references/core-web-vitals-guide.md

### Indexation Issues
Pages not indexed
  -> Check robots.txt blocking
  -> Verify sitemap inclusion
  -> Check canonical tags
  -> See references/crawlability-indexing.md
Crawl budget problems
  -> Remove low-value pages from crawl
  -> Fix redirect chains
  -> Optimize pagination
  -> See references/crawlability-indexing.md
New/large site needs fast indexation
  -> Internal linking (#1 accelerator)
  -> Manual GSC submission (10-20 priority pages)
  -> Real content updates (not fake lastmod)
  -> Brand mentions > backlinks (early stage)
  -> See references/crawlability-indexing.md#indexation-acceleration

### Mobile Issues
Mobile-unfriendly
  -> Check viewport meta tag
  -> Verify responsive CSS
  -> Test touch target sizes
  -> See references/mobile-seo-guide.md

### Link Building Issues
Need more backlinks
  -> Create linkable assets (research, tools)
  -> Set up HARO/Featured.com
  -> Broken link building outreach
  -> See references/link-building-strategy.md
Low domain authority
  -> Focus on DA 50+ targets
  -> Digital PR campaigns
  -> Competitor backlink analysis
  -> See references/link-building-strategy.md

### Local SEO Issues
Not showing in local pack
  -> Optimize Google Business Profile
  -> Build local citations (NAP consistency)
  -> Generate more reviews
  -> See references/local-seo-guide.md
GBP not verified
  -> Complete verification process
  -> Ensure NAP matches website
  -> See references/local-seo-guide.md

### Security Issues
Mixed content warnings
  -> Update all HTTP resources to HTTPS
  -> See references/security-https-guide.md
SSL/TLS issues
  -> Run SSL Labs test
  -> See references/security-https-guide.md
```

---

## GSC Issue Triage (Strict Output)

Use this format when diagnosing Google Search Console indexation and canonicalization statuses.

If missing context blocks a safe recommendation, ask only the minimum clarifying questions (example: "Should these URLs be indexed?").

For each issue:

- **Issue:**
- **Severity:** Critical / Moderate / Informational
- **What Google Is Detecting:**
- **Why This Happens:**
- **Is This Against Google Rules? (Yes/No + Explanation):**
- **Safe Fix (Step-by-Step):**
- **Expected SEO Benefit:**
- **What NOT to Do (Important):**

---

## Navigation

### Core Resources

- [references/core-web-vitals-guide.md](references/core-web-vitals-guide.md) - LCP, INP, CLS thresholds and optimization
- [references/crawlability-indexing.md](references/crawlability-indexing.md) - Robots.txt, sitemaps, GSC, indexation
- [references/site-speed-optimization.md](references/site-speed-optimization.md) - TTFB, render-blocking, image optimization
- [references/mobile-seo-guide.md](references/mobile-seo-guide.md) - Mobile-first indexing, responsive design
- [references/structured-data-guide.md](references/structured-data-guide.md) - Schema.org, JSON-LD, rich snippets
- [references/security-https-guide.md](references/security-https-guide.md) - HTTPS, HSTS, security headers
- [references/internal-linking-strategy.md](references/internal-linking-strategy.md) - Link architecture, orphan pages
- [references/duplicate-content-handling.md](references/duplicate-content-handling.md) - Canonicals, pagination, parameters
- [references/internationalization-hreflang.md](references/internationalization-hreflang.md) - Hreflang, geo-targeting

### Marketing & Operations

- [references/seo-marketing-strategy.md](references/seo-marketing-strategy.md) - Keyword research, content planning, competitive analysis, brand building
- [references/seo-operational-workflows.md](references/seo-operational-workflows.md) - Cross-team collaboration, OKRs, stakeholder communication
- [references/total-search-optimization.md](references/total-search-optimization.md) - YouTube, Reddit, TikTok, LinkedIn, AI platforms

### Link Building & Local SEO

- [references/link-building-strategy.md](references/link-building-strategy.md) - Backlink acquisition, digital PR, HARO, broken link building
- [references/local-seo-guide.md](references/local-seo-guide.md) - Google Business Profile, citations, reviews, local pack ranking

### Templates

#### Audits
- [assets/audits/full-technical-audit.md](assets/audits/full-technical-audit.md) - Complete 10-point audit checklist
- [assets/audits/quick-audit-checklist.md](assets/audits/quick-audit-checklist.md) - Fast abbreviated audit

#### Core Web Vitals
- [assets/cwv/core-web-vitals-report.md](assets/cwv/core-web-vitals-report.md) - CWV-specific audit report

#### Structured Data
- [assets/schema/schema-validation-report.md](assets/schema/schema-validation-report.md) - Schema audit report

#### Prioritization
- [assets/priority/impact-effort-matrix.md](assets/priority/impact-effort-matrix.md) - Issue prioritization matrix

---

## Trend Awareness Protocol

IMPORTANT: When users ask recommendation questions about SEO, refresh against current updates before giving definitive guidance. If your environment supports web search, use it. If not, rely on official sources in `data/sources.json` and ask the minimum clarifying question about timeframe/market (example: "Is this for the US market, and do you care about changes in the last 30/90 days?").

### Trigger Conditions

- "What's the best approach for [Core Web Vitals/site speed/crawlability]?"
- "What should I focus on for SEO in 2026?"
- "What's the latest Google algorithm update?"
- "Current best practices for [structured data/mobile SEO/indexation]?"
- "Is [SEO technique] still relevant in 2026?"
- "How has Google Search changed recently?"
- "What Core Web Vitals thresholds should I target?"

### Required Searches

1. Search: `site:developers.google.com search updates`
2. Search: `Google Search Status Dashboard`
3. Search: `Core Web Vitals thresholds INP`
4. Search: `Search Console new features`

### What to Report

After searching, provide:

- **Current landscape**: What SEO factors matter most NOW (not 6 months ago)
- **Emerging trends**: New ranking signals or Google features
- **Deprecated/declining**: Techniques that no longer work or hurt rankings
- **Recommendation**: Based on fresh data and recent algorithm updates

### Example Topics (verify with fresh search)

- Core Web Vitals updates (INP replacing FID, thresholds)
- Google algorithm updates (helpful content, spam updates)
- Structured data new types and requirements
- Mobile-first indexing changes
- AI Overviews impact on traditional search
- New Search Console features

---

## SEO Marketing Strategy (January 2026)

Keyword research, content planning, competitive analysis, and brand building.

**Key areas covered:**
- Keyword research framework (seed discovery, expansion, intent classification, prioritization)
- Content planning by intent (informational, commercial, transactional, navigational)
- Competitive analysis workflow (monthly audits, intelligence signals)
- Brand building tactics (brand and entity signals often correlate with durable performance; validate with current updates)
- E-E-A-T content strategy (Experience, Expertise, Authoritativeness, Trust)

**See full guide**: [references/seo-marketing-strategy.md](references/seo-marketing-strategy.md)

---

## SEO Operational Workflows (2026)

Cross-team collaboration, OKRs, and stakeholder communication.

**Key areas covered:**
- SEO as strategic quarterback (not isolated channel)
- Cross-team collaboration framework (Product, Engineering, Content, Paid, PR, Social)
- Pre-launch and post-deployment checklists
- SEO OKRs aligned to revenue (not vanity metrics)
- Stakeholder-specific reporting and communication

**See full guide**: [references/seo-operational-workflows.md](references/seo-operational-workflows.md)

---

## Total Search Optimization (2026)

Multi-platform visibility beyond Google.

**Platforms covered:**
- YouTube SEO (video optimization, ranking factors)
- Reddit SEO (forum results increasingly appear for "best", "vs", and review-intent queries)
- Social SEO (LinkedIn B2B, TikTok B2C, X/Twitter)
- AI platforms (ChatGPT, Perplexity, Gemini) - for deep coverage, use `marketing-ai-search-optimization`
- Unified content distribution strategy

**See full guide**: [references/total-search-optimization.md](references/total-search-optimization.md)

---

## Related Skills

**Marketing & SEO**

- [../marketing-ai-search-optimization/SKILL.md](../marketing-ai-search-optimization/SKILL.md) - Search visibility beyond classic SERPs (complements technical SEO)
- [../marketing-social-media/SKILL.md](../marketing-social-media/SKILL.md) - Social media marketing and content distribution

**Technical Implementation**

- [../software-frontend/SKILL.md](../software-frontend/SKILL.md) - Frontend performance optimization, SSR
- [../software-backend/SKILL.md](../software-backend/SKILL.md) - Server-side optimization, API performance
- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) - Security hardening, HTTPS implementation

**Quality & Performance**

- [../qa-observability/SKILL.md](../qa-observability/SKILL.md) - Performance monitoring, observability
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) - CDN setup, infrastructure optimization

---

## Key Differentiators

**Audit Output Format:**
- **Critical Issues** - Fix immediately (high impact)
- **Important Optimizations** - Fix soon (medium impact)
- **Recommended Enhancements** - Nice to have

**Each finding includes:**
- What's wrong and why it matters
- Step-by-step fix instructions
- Expected outcome
- Validation method

---

## External Resources

See [data/sources.json](data/sources.json) for primary sources across:

- Google Search Central, web.dev, and Chrome developer docs (CWV, Lighthouse, CrUX)
- Bing Webmaster Guidelines and diagnostic tooling
- Crawl/index/render fundamentals (robots, sitemaps, canonicals, JS SEO)
- Structured data eligibility and validation tooling
- SEO marketing strategy (Backlinko, Search Engine Journal, Sitebulb, Content Whale)
- Cross-team collaboration and operational workflows
- Total Search Optimization (YouTube, Reddit, TikTok, LinkedIn)
- Optional automation references (Search Console API, CrUX API, Lighthouse CI)

---

## Getting Started

**Quick audit (15 minutes):**
1. Run PageSpeed Insights on key pages
2. Check robots.txt and sitemap.xml accessibility
3. Validate structured data with Rich Results Test
4. Review GSC Coverage report for indexation issues
5. Use [assets/audits/quick-audit-checklist.md](assets/audits/quick-audit-checklist.md)

**Full audit (2-4 hours):**
1. Use [assets/audits/full-technical-audit.md](assets/audits/full-technical-audit.md)
2. Work through all 10 audit areas systematically
3. Score each area 0-10
4. Prioritize findings with [assets/priority/impact-effort-matrix.md](assets/priority/impact-effort-matrix.md)
5. Document fixes with validation steps

**Ongoing monitoring:**
1. Set up GSC alerts for indexation issues
2. Monitor Core Web Vitals in CrUX
3. Schedule quarterly audits
4. Track improvements against baseline

---

## SEO Testing & Monitoring

| Signal | Frequency | Alert Threshold |
|--------|-----------|-----------------|
| Indexation (GSC) | Daily | >5% drop |
| CWV scores (CrUX) | Daily | Any metric fails |
| Crawl errors | Daily | Any new 4xx/5xx |
| Schema validity | Weekly | Any errors |

**Do**: Lighthouse CI in pipeline, GSC API monitoring, CrUX field data, baseline before optimization

**Avoid**: Testing on fast dev machines only, ignoring field data, multiple simultaneous changes

---

## Success Criteria

> A successful technical SEO audit delivers a prioritized list of issues with clear fix instructions and validation methods that measurably improve search visibility and Core Web Vitals scores.

---

## SEO Business Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **SEO ROI** | (Organic Revenue - SEO Cost) / SEO Cost * 100 | >300% |
| **Organic CAC** | Total SEO Cost / Organic Conversions | B2B: <$100, B2C: <$30 |
| **Pipeline Influence** | Organic-Sourced Pipeline / Total Pipeline | >30% |

**See full guide**: [references/seo-business-metrics.md](references/seo-business-metrics.md) - Attribution models, OKRs, stakeholder reporting

---

## Tools & Collaboration

**Crawl tools**: Screaming Frog, Sitebulb, Semrush, Ahrefs, ContentKing, Lumar

**Cross-team**: Product (early planning, redirects), Engineering (Lighthouse CI, CWV), Design (images, CLS)

---

## Anti-Patterns

| Anti-Pattern (AVOID) | Better Practice (DO) |
|-----------------|-----------|
| Audit without action | Assign owners, set deadlines |
| Fix everything at once | Batch by priority, deploy incrementally |
| Ignore mobile | Test mobile-first (often the majority of traffic) |
| Trust lab data only | Use CrUX (field data) as truth |
| One-time audit | Continuous monitoring, quarterly deep audits |
| Chase vanity metrics (rankings) | Track revenue, conversions, pipeline |
| Optimize pages in isolation | Build topical authority clusters |
| Ignore AI Overviews | Optimize for citation in AI results |

---

## International Markets

This skill uses Google-centric defaults. For international SEO:

| Need | See Skill |
|------|-----------|
| Non-Google search (Baidu, Yandex, Naver) | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Hreflang and multi-region strategy | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| Regional SERP features | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |
| CJK/RTL language optimization | [marketing-geo-localization](../marketing-geo-localization/SKILL.md) |

If you're using a router-based setup, mention country/region/search engine explicitly so the router can bring in [marketing-geo-localization](../marketing-geo-localization/SKILL.md) when needed.

---

## SEO Mistakes (High Risk)

High risk (can cause ranking loss or manual actions): keyword stuffing, link spam/toxic backlink patterns, hidden text/cloaking, doorway pages, deceptive structured data, scaled low-value content

Common suppressors: weak E-E-A-T signals, poor internal linking, failing CWV, mobile-unfriendly UX, stale content, wrong canonicals

Technical crawl/index blockers: accidental noindex, redirect chains >2 hops, broken links, missing sitemap, blocking critical JS/CSS for rendering

Recovery: GSC Manual Actions -> Coverage report -> Traffic analysis -> Site audit -> Fix by severity -> Reconsideration (manual only) -> Expect weeks to months
