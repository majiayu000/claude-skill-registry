---
name: kai-seo-audit
description: One-click technical SEO audit of a website. Runs the full technical SEO audit SOP — crawlability, indexation, Core Web Vitals, schema markup, internal linking, mobile UX, and content quality. Outputs a prioritized fix list. Use when "SEO audit", "technical SEO", "site audit", "crawl issues", "indexation problems", "why aren't we ranking", "SEO health check", or any request to diagnose SEO issues on a website.
---

Run a technical SEO audit using the harness SOPs and checklists. Produces a prioritized fix list.

## Non-Negotiable: Kai Data Provenance

Before writing any finding, load `E:\Dev2\kai-cmo-harness-work\harness\references\audit-data-provenance.md`.

Declare the audit mode:

- `sales_external` for public-only or prospect audits.
- `onboarding_connected` when GSC, GA4, GBP, crawl exports, or SEO platform data are connected.
- `internal_demo` when values are placeholders.

Do not publish rankings, traffic, clicks, CTR, Core Web Vitals, PageSpeed, indexed-page counts, backlinks, Domain Rating, AI Overview visibility, schema validity, or local pack placement without source, retrieval date, and artifact/API note. Missing private data becomes a `Data needed` item, not an estimate.

Run before handoff:

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/seo-audit --audit-dir
```

## Phase 0.5: Source-Backed Data Acquisition

Before writing the SEO audit, run the source-backed Kai collector. The collector is shared by all Kai workflows, not audit-only; this SEO audit must consume its `audit-data.json` alias. Existing audit automations may keep using `python -m scripts.audit.collect`; non-audit SEO workflows should prefer `python -m kai.source_data.collect` and read `kai-data.json`.

```bash
python -m scripts.audit.collect --url "<url>" --mode sales_external --workflow seo-audit --out workspace/seo-audit --pagespeed --dataforseo --seo-provider auto --keywords "<kw1>,<kw2>" --location "<city, state>"
```

Use `--mode onboarding_connected` only when GSC/GA4/GBP or SEO platform exports are connected:

```bash
python -m scripts.audit.collect --url "<url>" --mode onboarding_connected --workflow seo-audit --out workspace/seo-audit --pagespeed --places --dataforseo --seo-provider auto --gsc --ga4 --keywords "<kw1>,<kw2>" --location "<city, state>" --date-from "<YYYY-MM-DD>" --date-to "<YYYY-MM-DD>"
```

Add `--third-party-sources serpapi,brightlocal,similarweb,builtwith,wappalyzer,bing-webmaster` when the SEO audit needs licensed vendor or non-Google search data. Treat API vendor values as `third_party_estimate`; treat supplied exports as `user_provided`.

The audit must read SEO metrics from `workspace/seo-audit/audit-data.json`; non-audit SEO workflows can read the identical `workspace/seo-audit/kai-data.json`. If a ranking, traffic, backlink, review, PageSpeed, Core Web Vitals, schema, GSC, GA4, or local pack metric is missing there, write it as a data gap rather than estimating it.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Site Input

Read from `MARKETING.md`. Only ask about things not covered there:

1. **URL** — what site are we auditing?
2. **Scope** — full site or specific sections?
3. **Known issues** — anything already flagged?
4. **Access** — do we have Search Console / analytics access?
5. **Priority** — what matters most? (rankings, traffic, indexation, speed)
6. **Audit mode** — `sales_external`, `onboarding_connected`, or `internal_demo`
7. **Data sources available** — public crawl, PageSpeed Insights, DataForSEO, Ahrefs/Semrush/Moz, GSC, GA4, GBP, Screaming Frog/Sitebulb export

## Phase 2: Audit Execution

Load these before starting:
- `E:\Dev2\kai-cmo-harness-work\knowledge\checklists\technical-seo-audit-sop.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\checklists\technical-seo-checklist.md`
- `E:\Dev2\kai-cmo-harness-work\knowledge\checklists\seo-checklist.md`

### Audit Layers (run in order)

**Layer 1: Crawlability & Indexation**
- robots.txt — blocking important pages?
- XML sitemap — exists, submitted, up to date?
- Canonical tags — correct, consistent?
- Noindex/nofollow — any unintended blocks?
- HTTP status codes — 404s, redirect chains, 5xx errors?
- Pagination — rel=next/prev or infinite scroll handling?

**Layer 2: Technical Performance**
- Core Web Vitals (LCP, INP, CLS)
- Mobile-friendliness
- Page speed (server response time, render-blocking resources)
- HTTPS — mixed content, certificate issues?
- Structured data / schema markup — present, valid?

**Layer 3: On-Page SEO**
- Title tags — unique, keyword-included, under 60 chars?
- Meta descriptions — unique, compelling, under 155 chars?
- H1 tags — one per page, keyword-relevant?
- Image alt text — descriptive, keyword-relevant?
- Internal linking — orphan pages, shallow link depth?
- URL structure — clean, descriptive, flat hierarchy?

**Layer 4: Content Quality**
- Thin content pages (under 300 words)
- Duplicate content (internal and external)
- Keyword cannibalization (multiple pages targeting same keyword)
- Content freshness — last updated dates
- E-E-A-T signals — author bios, citations, credentials

**Layer 5: Off-Page Signals**
- Backlink profile overview (if data available)
- Brand mentions without links
- Local SEO (if applicable) — GBP, NAP consistency

Use the browse/gstack skill to actually crawl pages if available. Otherwise, work from what the user provides or can check.

Every check must carry source metadata:

```yaml
source_tier: connected | public_observed | user_provided | inferred | missing_data
source_name: ""
source_url: ""
retrieved_at: ""
evidence_artifact: ""
confidence: high | medium | low
score_eligible: true | false
```

Do not include `inferred` or `missing_data` items in the health score.

## Phase 3: Prioritized Fix List

Score each finding:

| Priority | Impact | Effort | Examples |
|----------|--------|--------|----------|
| **P0** | High impact, easy fix | < 1 hour | Missing title tags, broken canonical, noindex on important pages |
| **P1** | High impact, moderate effort | 1 day | CWV failures, redirect chains, thin content |
| **P2** | Medium impact | 1 week | Schema markup, internal linking optimization |
| **P3** | Low impact / nice-to-have | Ongoing | Alt text gaps, URL cleanup |

## Recurring SEO Ops Monitor

For retained or repeated SEO work, add `seo-ops-monitor.md` beside the audit report. Keep it source-backed and operational:

- Cadence: weekly for crawl/indexation/CWV/schema regressions; monthly for content decay, query movement, and internal-link opportunities.
- Inputs: collector output, GSC/GA4 exports when connected, PageSpeed artifacts, crawl exports, sitemap and robots snapshots, rank or local data vendor exports when licensed.
- Alert rules: new noindex, robots block, sitemap drop, 4xx/5xx spike, redirect chain, canonical conflict, CWV regression, schema error, title/H1 removal, orphaned priority page, organic landing-page drop.
- Queue format: issue, source, retrieved_at, affected URL, severity, owner, proposed fix, approval needed, status, next check date.
- Never report movement, traffic, rankings, or visibility without provenance. Missing connected data becomes a monitor gap.

## Phase 4: Output

```markdown
# SEO Audit Report: [site.com]

Audit Mode: [sales_external/onboarding_connected/internal_demo]

## Health Score: [X]/100

## Critical Issues (P0)
| Issue | Pages Affected | Fix |
|-------|---------------|-----|
| ... | ... | ... |

## High Priority (P1)
| Issue | Pages Affected | Fix |
|-------|---------------|-----|

## Medium Priority (P2)
...

## Low Priority (P3)
...

## Technical Checklist Results
- [ ] robots.txt: [PASS/FAIL — detail]
- [ ] XML sitemap: [PASS/FAIL]
- [ ] Canonical tags: [PASS/FAIL]
- [ ] Core Web Vitals: [PASS/FAIL — LCP: Xs, INP: Xms, CLS: X]
- [ ] Mobile: [PASS/FAIL]
- [ ] HTTPS: [PASS/FAIL]
- [ ] Schema: [PASS/FAIL]
- [ ] Title tags: [PASS/FAIL]
- [ ] Internal linking: [PASS/FAIL]
...

## Recommendations
[Top 5 actions ordered by impact-to-effort ratio]

## Data Sources
[Source inventory with retrieved_at and artifacts]

## Data Gaps
[Missing access or exports that limit confidence]
```

Save to `workspace/seo-audit/[domain].md`.
