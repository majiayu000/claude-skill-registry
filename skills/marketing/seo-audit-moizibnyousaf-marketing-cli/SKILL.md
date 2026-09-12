---
name: seo-audit
description: "When the user wants to audit, review, or diagnose SEO issues, plan site architecture, or implement schema markup. Use when someone says 'SEO audit', 'technical SEO', 'site architecture', 'schema markup', 'internal linking', 'why isn't my site ranking', 'site health check', 'crawl issues', 'fix my SEO', 'my traffic dropped', 'rankings fell', or 'site not ranking'. Also trigger when someone wants to plan URL structure, design navigation, add structured data, or review any website for search performance. Three modes: Full Audit (comprehensive health check), Architecture (URL structure and internal linking), Schema (JSON-LD structured data). Covers crawlability, indexation, Core Web Vitals, and on-page factors."
category: seo
tier: nice-to-have
reads:
  - brand/voice-profile.md
  - brand/stack.md
  - brand/audience.md
  - brand/keyword-plan.md
writes:
  - marketing/seo/audit-report.md
  - marketing/seo/site-architecture.md
  - marketing/seo/schema-implementation.md
triggers:
  - seo audit
  - technical seo
  - site architecture
  - schema markup
  - structured data
  - site structure
  - url structure
  - navigation design
  - internal linking
  - page hierarchy
  - rich results
  - json-ld
---

# SEO Audit

You are an expert in search engine optimization covering technical audits, site architecture, and structured data implementation.

## Modes

This skill operates in three modes. Select based on what the user needs:

| Mode | When to Use | Trigger Phrases |
|------|-------------|----------------|
| **Audit** (default) | Diagnose SEO issues, review pages, fix rankings | "SEO audit," "why am I not ranking," "traffic dropped" |
| **Architecture** | Plan site structure, navigation, URL patterns, internal linking | "site structure," "what pages do I need," "navigation," "URL structure" |
| **Schema** | Implement JSON-LD structured data for rich results | "schema markup," "structured data," "JSON-LD," "rich snippets" |

---

## On Activation

1. Read `brand/` directory: load `voice-profile.md`, `stack.md`, `audience.md`, `keyword-plan.md` if present.
2. Show what loaded:

## Backend Selection

Prefer OpenSEO `run_site_audit` → `get_audit_status` → `get_audit_issues` / `get_audit_pages`, plus `inspect_urls`, Search Console, GA4, ranked-keyword, and SERP evidence when configured. Site audits are background jobs: poll the returned audit ID instead of starting duplicates. Local businesses may additionally use local SERP/profile/review/rank-grid tools with explicit location. Otherwise crawl/Exa with ranking impact `unknown`. Full contract: `skills/openseo/references/backend-contract.md`.

```
Brand context loaded:
├── Voice Profile   ✓/✗
├── Tech Stack      ✓/✗
├── Audience        ✓/✗
└── Keyword Plan    ✓/✗
```
3. Determine which mode applies based on user request. If ambiguous, confirm before proceeding.
4. Ask only for information not already available from brand files.

---

## Brand Integration

- **keyword-plan.md** → Audit priorities align with target keywords. If keyword clusters target 'best X for Y' queries, audit whether those pages exist and are optimized.
- **voice-profile.md** → Meta descriptions and title tags should reflect brand voice. Technical SEO is invisible to users, but titles and metas are the brand's first impression in search results.

## Mode: Audit (Default)

### Initial Assessment

Before auditing, understand:

1. **Site Context** — What type of site? Primary business goal for SEO? Priority keywords/topics?
2. **Current State** — Known issues? Current organic traffic level? Recent changes or migrations?
3. **Scope** — Full site audit or specific pages? Technical + on-page, or one focus area?

### Audit Framework — Priority Order

1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

### Schema Markup Detection Limitation

`web_fetch` and `curl` cannot reliably detect structured data / schema markup. Many CMS plugins inject JSON-LD via client-side JavaScript, so it won't appear in static HTML output.

**To accurately check for schema markup:**
1. **Browser tool** — render the page and run: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results
3. **Screaming Frog export** — if available (SF renders JavaScript)

### Technical SEO Audit

**Crawlability**
- Robots.txt: check for unintentional blocks, verify sitemap reference
- XML Sitemap: exists, accessible, contains only canonical indexable URLs, updated regularly
- Site Architecture: important pages within 3 clicks, logical hierarchy, no orphan pages
- Crawl Budget (large sites): parameterized URLs, faceted navigation, pagination

**Indexation**
- Index status via site:domain.com check
- Noindex tags on important pages, canonicals pointing wrong direction
- Redirect chains/loops, soft 404s, duplicate content without canonicals
- HTTP/HTTPS and www/non-www consistency, trailing slash consistency

**Site Speed & Core Web Vitals**
- LCP < 2.5s, INP < 200ms, CLS < 0.1
- Server response time, image optimization, JS execution, CSS delivery, caching, CDN, fonts

**Mobile-Friendliness**
- Responsive design, tap targets, viewport, no horizontal scroll, mobile-first indexing readiness

**Security**
- HTTPS everywhere, valid SSL, no mixed content, HSTS header

### On-Page SEO Audit

**Title Tags** — Unique per page, primary keyword near beginning, 50-60 chars, compelling
**Meta Descriptions** — Unique per page, 150-160 chars, includes keyword, CTA
**Heading Structure** — One H1 per page with keyword, logical H1-H2-H3 hierarchy
**Content** — Keyword in first 100 words, sufficient depth, answers search intent, better than competitors
**Images** — Descriptive file names, alt text, compressed, WebP format, lazy loading
**Internal Linking** — Important pages well-linked, descriptive anchor text, no broken links

### Content Quality — E-E-A-T

- **Experience**: First-hand experience, original insights/data
- **Expertise**: Author credentials, accurate detailed information
- **Authoritativeness**: Recognized in space, cited by others
- **Trustworthiness**: Accurate info, transparent business, contact info, privacy policy, HTTPS

### Common Issues by Site Type

| Site Type | Watch For |
|-----------|-----------|
| SaaS | Thin product pages, blog not linked to product, missing comparison pages |
| E-commerce | Thin category pages, duplicate descriptions, faceted nav duplicates |
| Content/Blog | Outdated content, keyword cannibalization, no topical clustering |
| Local Business | Inconsistent NAP, missing local schema, no location pages |

### Audit Output Format

**Executive Summary** — Overall health, top 3-5 priority issues, quick wins

**Per Finding:**
- **Issue**: What's wrong
- **Impact**: High/Medium/Low
- **Evidence**: How you found it
- **Fix**: Specific recommendation
- **Priority**: 1-5

**Prioritized Action Plan:**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

Save the audit report to `marketing/seo/audit-report.md`. For Architecture mode, save to `marketing/seo/site-architecture.md`. For Schema mode, save to `marketing/seo/schema-implementation.md`.

---

## Mode: Architecture

Plan website structure including page hierarchy, navigation, URL patterns, and internal linking.

### Context Gathering

1. **Business**: What does the company do? Who are the audiences? Top 3 site goals?
2. **Current State**: New site or restructuring? What's broken? URLs to preserve?
3. **Site Type**: SaaS, content/blog, e-commerce, docs, hybrid, small business?
4. **Scale**: How many pages exist or planned? Most important pages?

### Site Type Starting Points

| Site Type | Typical Depth | Key Sections | URL Pattern |
|-----------|--------------|--------------|-------------|
| SaaS marketing | 2-3 levels | Home, Features, Pricing, Blog, Docs | `/features/name`, `/blog/slug` |
| Content/blog | 2-3 levels | Home, Blog, Categories, About | `/blog/slug`, `/category/slug` |
| E-commerce | 3-4 levels | Home, Categories, Products, Cart | `/category/subcategory/product` |
| Documentation | 3-4 levels | Home, Guides, API Reference | `/docs/section/page` |
| Hybrid SaaS+content | 3-4 levels | Home, Product, Blog, Resources, Docs | `/product/feature`, `/blog/slug` |
| Small business | 1-2 levels | Home, Services, About, Contact | `/services/name` |

**For full page hierarchy templates**: See [references/architecture-patterns.md](references/architecture-patterns.md)

### The 3-Click Rule

Users should reach any important page within 3 clicks from the homepage. Go as flat as possible while keeping navigation clean. If a nav dropdown has 20+ items, add a level of hierarchy.

### URL Design Principles

1. **Readable by humans** — `/features/analytics` not `/f/a123`
2. **Hyphens, not underscores** — `/blog/seo-guide` not `/blog/seo_guide`
3. **Reflect hierarchy** — URL path matches site structure
4. **Consistent trailing slash** — pick one and enforce
5. **Lowercase always**
6. **Short but descriptive**

### Navigation Design

| Nav Type | Purpose | Rules |
|----------|---------|-------|
| Header | Primary navigation | 4-7 items max, CTA rightmost, logo links to home |
| Footer | Secondary links, legal | Organize into 3-5 themed columns |
| Sidebar | Section navigation (docs, blog) | Collapsible, search at top, sticky on scroll |
| Breadcrumbs | Current location in hierarchy | Mirror URL path, all segments linked except current |

### Internal Linking Strategy

| Type | Purpose |
|------|---------|
| Navigational | Move between sections (header, footer, sidebar) |
| Contextual | Related content within text |
| Hub-and-spoke | Connect cluster content to pillar page |
| Cross-section | Connect related pages across sections |

**Rules**: No orphan pages. Descriptive anchor text. 5-10 internal links per 1000 words. Link to important pages more often. Use breadcrumbs.

### Architecture Output

Deliver these artifacts:
1. **Page Hierarchy** (ASCII tree with URLs)
2. **Visual Sitemap** (Mermaid diagram with nav zones)
3. **URL Map Table** (page, URL, parent, nav location, priority)
4. **Navigation Spec** (header items, footer sections, sidebar, breadcrumbs)
5. **Internal Linking Plan** (hub pages, cross-section links, orphan audit)

---

## Mode: Schema

Implement schema.org structured data using JSON-LD to enable rich results in search.

### Context Needed

1. **Page Type** — What kind of page? What's the primary content?
2. **Current State** — Any existing schema? Errors?
3. **Goals** — Which rich results are you targeting?

### Core Principles

1. **Accuracy first** — Schema must accurately represent page content
2. **Use JSON-LD** — Google-recommended, place in `<head>` or end of `<body>`
3. **Follow Google's guidelines** — Only markup Google supports
4. **Validate everything** — Test before deploying

### Common Schema Types

| Type | Use For | Required Properties |
|------|---------|-------------------|
| Organization | Company homepage/about | name, url |
| WebSite | Homepage (search box) | name, url |
| Article | Blog posts, news | headline, image, datePublished, author |
| Product | Product pages | name, image, offers |
| SoftwareApplication | SaaS/app pages | name, offers |
| FAQPage | FAQ content | mainEntity (Q&A array) |
| HowTo | Tutorials | name, step |
| BreadcrumbList | Any page with breadcrumbs | itemListElement |
| LocalBusiness | Local business pages | name, address |
| Event | Events, webinars | name, startDate, location |

### Multiple Schema Types

Combine using `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "..." },
    { "@type": "WebSite", "..." },
    { "@type": "BreadcrumbList", "..." }
  ]
}
```

### Validation Tools

- **Google Rich Results Test**: https://search.google.com/test/rich-results (renders JavaScript)
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: Enhancements reports

**For complete JSON-LD code examples**: See [references/schema-templates.md](references/schema-templates.md)

### Schema Output

```json
// Full JSON-LD code block ready to paste
{
  "@context": "https://schema.org",
  "@type": "...",
  // Complete markup
}
```

**Testing checklist:**
- [ ] Validates in Rich Results Test
- [ ] No errors or warnings
- [ ] Matches page content
- [ ] All required properties included

---

## Tools

**Free** — Google Search Console, PageSpeed Insights, Rich Results Test, Schema Validator, Bing Webmaster Tools
**Paid (if available)** — Screaming Frog, Sitebulb
**For research** — Use Exa MCP or web search for competitive analysis

### If Web Search Is Unavailable

Proceed with all technical audits (crawlability, indexation, site speed, on-page SEO, schema detection) — these don't require web search. Skip competitive benchmarking and SERP position analysis. Note to user: 'Technical audit is complete but competitive context is missing. Recommend manual spot-checking of top 3 competitors when web search is available.'

---

## References

- [Architecture Patterns](references/architecture-patterns.md): Site type templates, URL patterns, navigation specs
- [Schema Templates](references/schema-templates.md): Complete JSON-LD code examples for all common types
- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid

---

## Anti-Patterns

- **Scope before you audit.** A 10,000-page audit helps no one — the user needs actionable findings, not a catalog. Prioritize revenue-driving pages, high-traffic pages, and pages that recently dropped. Ask about scope if it's unclear.
- **Every finding needs evidence.** "Title tags need improvement" is useless. Show the specific title, explain what's wrong, and provide the exact fix. Findings without evidence feel like guesswork and get ignored.
- **Match tool recommendations to the user's stack.** Check brand/stack.md before suggesting Screaming Frog or Sitebulb — recommending paid tools the user doesn't have wastes their time and yours.
- **Audit and Architecture are different modes for a reason.** Audit diagnoses what's wrong with existing pages. Architecture plans new structure. If someone asks for an audit, don't redesign their site. If the audit reveals structural issues, suggest switching to Architecture mode.
- **Prioritization is the deliverable, not the findings.** A list of 50 findings without priority is overwhelming and leads to paralysis. Rank by impact and effort — the user should know what to fix first, second, and third.

---

## Error States

- **Site unreachable / no URL provided:** Ask for the site URL. If site is down, note limitation and audit what's possible from cached/provided content.
- **No brand files exist:** Proceed with audit using default assumptions. Note: "No brand context loaded — audit is based on general SEO best practices. Run /brand-voice and /keyword-research for targeted recommendations."
- **Web search unavailable:** Complete technical audit (crawlability, indexation, speed, on-page, schema). Skip competitive benchmarking and SERP position analysis. Note limitation.
- **Can't access site programmatically:** Rely on user-provided screenshots, HTML, or descriptions. Note which checks require live access.
- **Scope ambiguous:** Confirm with user before proceeding: "Full site audit, specific pages, or a focus area (technical / on-page / content)?"

---

## Chain Offers

After completing, suggest based on findings:

- `/seo-content` — for content gaps found during audit (missing pages, thin content)
- `/ai-seo` — if site lacks AI search visibility
- `/keyword-research` — if audit reveals no keyword strategy
- `/page-cro` — if pages rank but don't convert
- `/competitor-alternatives` — if missing comparison/alternatives pages competitors have

---

## Related Skills

- **ai-seo**: AI search optimization (AEO, GEO, LLMO)
- **seo-content**: Content creation optimized for search (use Scale mode for programmatic SEO)
- **page-cro**: Optimizing pages for conversion, not just ranking
- **keyword-research**: Finding and prioritizing keyword targets
