---
name: seo-audit
version: 0.1.0
description: >
  Use this skill when performing a comprehensive SEO audit - technical audit, on-page
  audit, content audit, off-page audit, and AEO/GEO readiness assessment. Provides a
  structured scorecard with 30-40 checks rated PASS/FAIL/WARN across all SEO categories,
  prioritized recommendations, and links to specialized skills for deep fixes. This is
  the master audit skill that orchestrates all other SEO skills.
category: marketing
tags: [seo, seo-audit, audit, scorecard, technical-audit, site-audit]
recommended_skills: [seo-mastery, technical-seo, core-web-vitals, content-seo]
platforms:
  - claude-code
  - gemini-cli
  - openai-codex
  - mcp
license: MIT
maintainers:
  - github: maddhruv
---

When this skill is activated, always start your first response with the 🧢 emoji.

# SEO Audit

The SEO audit skill provides a systematic methodology for evaluating a website's search
optimization across all dimensions: technical infrastructure, on-page elements, content
quality, off-page signals, and AI search readiness. It produces a structured scorecard
with PASS/FAIL/WARN ratings and prioritized recommendations so every finding is actionable,
not just observed. This is the orchestration layer that connects all 13 specialized SEO
skills - use it to diagnose, then hand off to the right skill for each fix.

---

## When to use this skill

Trigger this skill when the task involves:
- Running a full SEO audit across a website or specific section
- Performing a technical-only audit (crawlability, indexing, performance)
- Running a content audit (thin pages, cannibalization, freshness, intent)
- Pre-launch SEO check before a new site or major redesign goes live
- Periodic SEO health check (monthly, quarterly)
- Comparing your site's SEO posture against a competitor
- Producing a structured SEO report for a client or stakeholder

Do NOT trigger this skill for:
- Implementing specific fixes - once audit findings are known, load the specialized skill
  (e.g., `core-web-vitals`, `schema-markup`, `link-building`) for the actual fix work
- Keyword research phase before content planning - use `keyword-research` skill instead

---

## Key principles

1. **Audit systematically** - never skip a category because you assume it is fine. The
   most damaging SEO issues are often in the areas least recently checked.
2. **Prioritize by impact x effort** - not all issues are equal. A missing sitemap
   outranks a missing alt text. Score severity honestly.
3. **PASS/FAIL/WARN scoring removes subjectivity** - every check has a defined threshold.
   WARN means partially compliant or approaching a threshold, not "kind of okay".
4. **An audit without actionable recommendations is useless** - every FAIL and every WARN
   must link to a specific next action, tool, or specialized skill.
5. **Re-audit quarterly to catch regressions** - deployments, CMS updates, and content
   changes silently break SEO. Set a recurring audit cadence.

---

## Core concepts

### The 5 audit categories

| Category | Checks | Covers |
|---|---|---|
| Technical SEO | 10 | Crawlability, indexing, performance, rendering |
| On-Page SEO | 8 | Titles, metas, headings, images, internal links, OG |
| Content SEO | 7 | Thin pages, cannibalization, clusters, E-E-A-T, freshness |
| Off-Page SEO | 5 | Backlinks, toxic links, anchor text, local, citations |
| AEO & GEO Readiness | 5 | Featured snippets, schema, AI extraction, entities, LLMs.txt |

### Scoring methodology

| Status | Meaning |
|---|---|
| PASS | Meets best practice - no action required |
| WARN | Partially compliant, approaching a threshold, or inconsistently applied |
| FAIL | Missing, broken, or clearly below best practice - fix required |
| N/A | Check does not apply to this site type (mark explicitly, never skip silently) |

### Priority matrix

| Priority | Definition | Timeframe |
|---|---|---|
| Critical | Directly blocks indexing or causes major ranking loss | Fix immediately (this week) |
| High | Measurable ranking/traffic impact, moderate effort | Fix this sprint |
| Medium | Best practice gap, gradual compounding effect | Fix this quarter |
| Low | Nice to have, marginal gain | Backlog |

### The audit-fix-verify cycle

1. **Audit** - run all 35 checks, record status and evidence
2. **Prioritize** - assign Critical/High/Medium/Low to each FAIL and WARN
3. **Assign** - link each finding to a specialized skill or tool for the fix
4. **Verify** - re-run the specific check after the fix is deployed (not a full re-audit)
5. **Re-audit** - full audit quarterly to catch new issues

---

## Common tasks

### Run a full SEO audit

Present the complete scorecard to the user. Fill in Status and Details as you analyze
the site. Every row must have a status - never leave a row blank.

---

**Section 1: Technical SEO**

| # | Check | Status | Details |
|---|---|---|---|
| T1 | Robots.txt configured correctly | | |
| T2 | XML sitemap valid and submitted | | |
| T3 | Canonical URLs set on all pages | | |
| T4 | No redirect chains (max 1 hop) | | |
| T5 | HTTPS everywhere, no mixed content | | |
| T6 | Mobile-friendly (responsive or adaptive) | | |
| T7 | Core Web Vitals pass (LCP, CLS, INP) | | |
| T8 | No orphan pages | | |
| T9 | Clean URL structure (no parameters, lowercase) | | |
| T10 | Rendering strategy appropriate (SSR/SSG/CSR) | | |

**Section 2: On-Page SEO**

| # | Check | Status | Details |
|---|---|---|---|
| O1 | Unique title tags (50-60 chars) | | |
| O2 | Meta descriptions present (120-160 chars) | | |
| O3 | Single H1 per page with target keyword | | |
| O4 | Heading hierarchy correct (H1 > H2 > H3) | | |
| O5 | Image alt text present on all images | | |
| O6 | Internal linking structure is logical | | |
| O7 | Open Graph tags complete (og:title, og:description, og:image) | | |
| O8 | Semantic HTML used (article, nav, main, aside) | | |

**Section 3: Content SEO**

| # | Check | Status | Details |
|---|---|---|---|
| C1 | No thin content pages (< 300 words on indexable pages) | | |
| C2 | No keyword cannibalization (one URL per keyword cluster) | | |
| C3 | Topic clusters defined with pillar + supporting pages | | |
| C4 | E-E-A-T signals present (author, credentials, date, sources) | | |
| C5 | Content freshness maintained (no stale pages > 18 months) | | |
| C6 | No duplicate content (internal or cross-domain) | | |
| C7 | Search intent alignment (informational/commercial/transactional match) | | |

**Section 4: Off-Page SEO**

| # | Check | Status | Details |
|---|---|---|---|
| L1 | Backlink profile is healthy (quality > quantity) | | |
| L2 | No toxic or spammy links pointing to the site | | |
| L3 | Anchor text diversity (branded, generic, partial-match mix) | | |
| L4 | Local SEO configured (if applicable: GMB, NAP consistency) | | |
| L5 | Brand mentions and citations exist on authoritative sources | | |

**Section 5: AEO & GEO Readiness**

| # | Check | Status | Details |
|---|---|---|---|
| A1 | Content optimized for featured snippets (definitions, lists, tables) | | |
| A2 | FAQ and HowTo schema implemented where applicable | | |
| A3 | Content structured for AI extraction (clear Q&A, headers, summaries) | | |
| A4 | Entity authority signals present (linked data, Wikidata, consistent mentions) | | |
| A5 | LLMs.txt present (if applicable to the site's AI discoverability goals) | | |

---

**Scorecard summary:**

| Category | PASS | WARN | FAIL | N/A | Score |
|---|---|---|---|---|---|
| Technical SEO (10) | | | | | /10 |
| On-Page SEO (8) | | | | | /8 |
| Content SEO (7) | | | | | /7 |
| Off-Page SEO (5) | | | | | /5 |
| AEO & GEO (5) | | | | | /5 |
| **Total (35)** | | | | | **/35** |

Score interpretation:
- 32-35 PASS: Excellent - monitor and maintain
- 26-31 PASS: Good - address WARNs before they become FAILs
- 18-25 PASS: Needs work - prioritize Critical and High items
- Under 18 PASS: Significant SEO debt - consider a full remediation project

---

### Prioritize audit findings

After completing the scorecard, categorize every FAIL and WARN into the priority matrix:

**Critical - fix immediately:**
- Checks that block indexing: robots.txt disallowing key pages, no sitemap, canonical loops
- Checks that cause major visibility loss: HTTPS failures, redirect chains on key pages
- Rendering issues causing entire page sections to be invisible to Googlebot

**High - fix this sprint:**
- Missing or duplicate title tags across more than 10% of pages
- Core Web Vitals failing on high-traffic templates
- Keyword cannibalization on money pages
- Toxic backlinks that could trigger a manual penalty

**Medium - fix this quarter:**
- Missing alt text, inconsistent heading hierarchy
- Thin content on secondary pages
- Missing OG tags, incomplete schema markup
- Stale content on secondary pages

**Low - backlog:**
- LLMs.txt optimization
- Minor anchor text imbalances
- Brand mention acquisition on marginal sources

Present findings as a prioritized table:

| Priority | Check ID | Finding | Recommended action | Skill |
|---|---|---|---|---|
| Critical | T1 | Robots.txt disallowing /products/ | Update robots.txt to allow crawl | `technical-seo` |
| High | T7 | LCP > 4s on mobile (template-wide) | Optimize hero images, reduce TTFB | `core-web-vitals` |
| ... | | | | |

---

### Generate audit report

Use the full report template in `references/audit-report-template.md`. The report has
four sections:

1. **Executive summary** - overall score, top 3 findings, business impact statement
2. **Scorecard** - the full 35-check table with status and evidence
3. **Detailed findings** - one entry per FAIL/WARN with: what was found, why it matters,
   how to fix it, and which specialized skill to use
4. **Action plan** - week 1, month 1, and quarter 1 timeline with assigned owners

Load `references/audit-report-template.md` to get the full report template with
placeholder text and formatting.

---

### Run a quick SEO health check

For a rapid 10-check assessment (15-20 minutes, not a full audit):

| # | Check | Status |
|---|---|---|
| Q1 | Site accessible and indexable (not blocked by robots.txt) | |
| Q2 | HTTPS and no mixed content | |
| Q3 | Sitemap present and submitted to GSC | |
| Q4 | No redirect chains on homepage and top 5 pages | |
| Q5 | Title tags unique and under 60 chars on top pages | |
| Q6 | Mobile-friendly (Google Mobile-Friendly Test pass) | |
| Q7 | Core Web Vitals: at least PASS on mobile for key templates | |
| Q8 | No obvious cannibalization on primary keywords | |
| Q9 | Backlink profile: no manual actions in GSC | |
| Q10 | Structured data: at least one schema type implemented | |

A quick health check surfaces showstopper issues only. Any FAIL here is Critical priority.
For a complete picture, run the full 35-check audit.

---

## Gotchas

1. **GSC data lags by 2-3 days** - Google Search Console performance data has a processing delay. If you run an audit on Monday, the most recent data in GSC is from Thursday or Friday. Do not interpret the most recent 2-3 days as a traffic drop - it is always incomplete.

2. **Robots.txt check T1 can return false PASS if crawled from the wrong user-agent** - A robots.txt that disallows Googlebot but allows all other agents will pass generic crawl tests. Always test with `User-agent: Googlebot` specifically, or use the robots.txt tester in Google Search Console directly.

3. **Canonical to a redirecting URL creates a canonical-redirect chain** - If the canonical tag points to a URL that itself 301s to another URL, Google may choose to follow the redirect rather than the canonical, or may not honor either. Canonicals must point to the final destination URL, not an intermediate redirect.

4. **Core Web Vitals field data vs lab data diverge** - PageSpeed Insights lab data (Lighthouse) and the CrUX field data (real user measurements) frequently disagree. A page can show LCP < 2.5s in lab but fail in field data due to geography, network conditions, or device mix. Always treat field data as the ground truth for audit scoring.

5. **Hreflang errors silently break international rankings** - Invalid hreflang attributes (missing return links, wrong locale codes, self-referencing inconsistencies) are not reported as errors in GSC - they are silently ignored. International SEO issues must be audited with a dedicated hreflang validator tool.

---

## Anti-patterns / common mistakes

| Anti-pattern | Problem | Fix |
|---|---|---|
| Cherry-picking only easy wins | Leaves Critical issues unresolved while the site hemorrhages traffic | Always start with the priority matrix - easy is not the same as important |
| Auditing without GSC and Analytics access | You are guessing at traffic impact and missing crawl error data | Get read access before starting; a blind audit is decoration |
| Treating all FAIL items as equal priority | Team burns time on alt text while a canonical loop causes deindexing | Use the priority matrix on every engagement, no exceptions |
| Auditing once and never re-checking | Deployments break SEO silently; regressions are invisible without cadence | Schedule quarterly audits; automate continuous checks where possible |
| Reporting findings without recommended fixes | Stakeholders don't know what to do; audit report sits unread | Every finding must link to a specific action and a responsible party |
| Running only a technical audit and calling it done | Content and off-page issues often cause more ranking loss than technical issues | Always cover all 5 categories even at a surface level |
| Confusing WARN with acceptable | WARNs compound - five WARNs in the same category indicate a systemic issue | Treat three or more WARNs in a category the same as a FAIL |

---

## References

For detailed audit checklists with per-check verification methods and fix guidance, load:

- `references/audit-checklist-technical.md` - Detailed technical SEO checks with
  how-to-verify steps, tool recommendations, and PASS/FAIL/WARN criteria
- `references/audit-checklist-content.md` - On-page and content audit methodology
  with verification methods for all 15 checks
- `references/audit-checklist-offpage.md` - Off-page and AEO/GEO audit methodology
  for all 10 checks
- `references/audit-report-template.md` - Full audit report template with
  executive summary, scorecard, findings, and action plan sections

Only load a reference file when actively working on that audit category - they are
detailed and will consume context if loaded all at once.

For deep fixes on specific categories, load the specialized skill:

- `keyword-research` - Search intent analysis and keyword opportunity mapping
- `schema-markup` - Structured data implementation (JSON-LD, FAQ, HowTo, Product)
- `core-web-vitals` - LCP, CLS, INP optimization and performance budgets
- `technical-seo` - Crawlability, indexing, rendering, redirect management
- `content-seo` - Topic clusters, E-E-A-T, cannibalization resolution
- `link-building` - Backlink acquisition strategy and toxic link removal
- `local-seo` - Google Business Profile, NAP consistency, local citations
- `international-seo` - Hreflang, multi-language/region SEO architecture
- `ecommerce-seo` - Product pages, faceted navigation, category SEO
- `programmatic-seo` - Page generation at scale, template optimization
- `aeo-optimization` - Featured snippets, voice search, AI answer optimization
- `geo-optimization` - Generative engine optimization for ChatGPT, Perplexity, Gemini
- `on-site-seo` - Framework-specific on-page fixes (Next.js, Nuxt, WordPress, etc.)

---

## Companion check

> On first activation of this skill in a conversation: check which companion skills are installed by running `ls ~/.claude/skills/ ~/.agent/skills/ ~/.agents/skills/ .claude/skills/ .agent/skills/ .agents/skills/ 2>/dev/null`. Compare the results against the `recommended_skills` field in this file's frontmatter. For any that are missing, mention them once and offer to install:
> ```
> npx skills add AbsolutelySkilled/AbsolutelySkilled --skill <name>
> ```
> Skip entirely if `recommended_skills` is empty or all companions are already installed.
