---
name: kai-audit
description: Full marketing audit — runs all relevant checklists against your product, site, and marketing in one go. Covers SEO, content, email, ads, social media, CRO, landing pages, technical SEO, and creative production. Produces a "state of your marketing" report with health scores per area and a prioritized fix list. Use when "marketing audit", "full audit", "audit everything", "marketing health check", "what's broken", "state of marketing", or any request to comprehensively assess marketing across all channels.
---

One-click full marketing audit. Runs all relevant harness checklists and produces a health report.

## Non-Negotiable: Kai Data Provenance

Before writing any finding, load `E:\Dev2\kai-cmo-harness-work\harness\references\audit-data-provenance.md`.

Every audit must declare one of these modes:

| Mode | Use When | Client-Facing Label |
|------|----------|---------------------|
| `sales_external` | Prospect or sales process before private access is granted | Sales intelligence audit - external-only |
| `onboarding_connected` | Client has signed and granted GSC, GA4, GBP, ads, CRM, or call data access | Client onboarding audit |
| `internal_demo` | Showing the shape of a workflow before data is connected | Internal demo - sample data |

Default to `sales_external` if access is unclear.

Hard rules:

1. Do not publish numbers without a source. Review counts, ratings, rankings, traffic, conversions, calls, Core Web Vitals, Domain Rating, referring domains, AI Overview visibility, and local pack placement need source, retrieval date, and artifact/API note.
2. Do not score what was not measured. Missing GSC, GA4, GBP, call tracking, backlink, or ad-platform data becomes a data gap, not an invented estimate.
3. Do not turn inference into fact. Hypotheses must be labeled `score_eligible: false` and kept out of client-facing health scores.
4. Do not cite a tool unless it actually ran. If the report says Ahrefs, DataForSEO, PageSpeed Insights, BuiltWith, Google Places, GSC, GA4, GBP, CallRail, or CRM, include retrieved date and raw artifact path or response summary.
5. Every deck slide with a number needs a source footer. Every audit folder needs `_data-sources.md` and `_data-gaps.md`.

Run before handoff:

```bash
python scripts/quality_gates/audit_provenance_lint.py workspace/marketing-audit --audit-dir
```

## Phase 0.5: Source-Backed Data Acquisition

Before writing the audit, run the source-backed Kai collector. The collector is shared by all Kai workflows, not audit-only; this audit must consume its `audit-data.json` alias. Existing audit automations may keep using `python -m scripts.audit.collect`; non-audit Kai workflows should prefer `python -m kai.source_data.collect` and read `kai-data.json`.

```bash
python -m scripts.audit.collect --url "<url>" --firm-name "<firm_name>" --mode sales_external --workflow audit --out workspace/marketing-audit --pagespeed
```

Use `--mode onboarding_connected` only when the client has granted private access. Add optional collectors only when the workflow needs those facts:

```bash
python -m scripts.audit.collect --url "<url>" --firm-name "<firm_name>" --mode onboarding_connected --workflow audit --out workspace/marketing-audit --pagespeed --places --dataforseo --seo-provider auto --gsc --ga4 --calls --keywords "<kw1>,<kw2>" --location "<city, state>" --date-from "<YYYY-MM-DD>" --date-to "<YYYY-MM-DD>"
```

Add `--third-party-sources all` or a comma list such as `serpapi,similarweb,builtwith,wappalyzer,brightlocal,yext,yelp,trustpilot,google-ads,meta-ads,tiktok-ads,linkedin-ads,twilio` when the audit needs licensed vendor data. Treat API vendor values as `third_party_estimate`; treat supplied exports as `user_provided`.

The collector writes:

- `workspace/marketing-audit/kai-data.json`
- `workspace/marketing-audit/audit-data.json`
- `workspace/marketing-audit/_data-sources.md`
- `workspace/marketing-audit/_data-gaps.md`
- `workspace/marketing-audit/raw/`

All findings, health scores, and deck numbers must come from `audit-data.json`. Do not use numbers discovered conversationally, in snippets, or from model memory. If the metric is not present in `audit-data.json`, add it as a data gap instead of estimating it. Missing credentials for Places, DataForSEO, SEO platforms, GSC, GA4, call tracking, ads, or CRM must remain data gaps until the collector records a sourced metric.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Audit Scope

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Product/site** — what are we auditing?
2. **URL** — main website
3. **Active channels** — which are you using? (SEO, email, ads, social, content, PR)
4. **Known issues** — anything already flagged?
5. **Depth** — quick (top-line scores, 30 min) or deep (detailed findings, 2-3 hours)?
6. **Audit mode** — `sales_external`, `onboarding_connected`, or `internal_demo`
7. **Available data** — public-only, Ahrefs/Semrush/DataForSEO, PageSpeed Insights, BuiltWith, Google Places, GSC, GA4, GBP, ads, CRM, CallRail, exports/screenshots
8. **Business type** — determines which industry-specific module(s) to load:

   | Type | Indicators | Examples | Module |
   |------|-----------|----------|--------|
   | **Local Service** | Serves geographic area, phone-based leads, local customers | Plumber, cleaner, HVAC, landscaper, electrician, painter, roofer | `local-service-business-checklist.md` |
   | **Professional Services (B2B)** | Credential-based, trust-heavy, long sales cycle, thought leadership | Law firm, accounting firm, consultant, agency, financial advisor, architect | `professional-services-b2b-checklist.md` |
   | **Multi-Location** | 2+ physical locations, franchise/chain, centralized brand | Franchise, clinic network, restaurant chain, retail chain, multi-office firm | `multi-location-checklist.md` |
   | **Restaurant / Food & Bev** | Food/drink is the product, dine-in/takeout/delivery | Restaurant, cafe, bar, food truck, bakery, catering, ghost kitchen | `restaurant-food-bev-checklist.md` |
   | **Healthcare / Medical** | Patient-facing, HIPAA-regulated, medical services | Dental, medical clinic, chiropractic, med spa, mental health, veterinary | `healthcare-medical-checklist.md` |
   | **Creator / Personal Brand** | Individual IS the brand, audience-based monetization | Course creator, coach, YouTuber, podcaster, newsletter operator, author | `creator-personal-brand-checklist.md` |
   | **Real Estate** | Property transactions, agent personal brand, portal-dependent | Agent, team, brokerage, property manager | `real-estate-checklist.md` |
   | **SaaS / Digital Product** | Software product, online-first, subscription revenue | _(default — existing harness modules cover this)_ | No additional module |

   A business can match multiple types (e.g., a multi-location dental practice triggers both Multi-Location AND Healthcare). Load all applicable modules.

## Phase 2: Checklist Execution

Run applicable checklists from `E:\Dev2\kai-cmo-harness-work\knowledge\checklists\`. Skip checklists for channels the user isn't using.

### Audit Modules

| Module | Checklist Files | Applies When |
|--------|----------------|-------------|
| **Technical SEO** | `technical-seo-audit-sop.md`, `technical-seo-checklist.md` | Always (if they have a website) |
| **On-Page SEO** | `seo-checklist.md` | Always |
| **Content Quality** | `content-checklist.md`, `content-brief-checklist.md` | If publishing content |
| **Email Marketing** | `email-checklist.md` | If running email |
| **Meta/Facebook Ads** | `meta-advertising-checklist.md` | If running Meta ads |
| **Google Ads** | `google-ads-launch-checklist.md`, `paid-acquisition-checklist.md` | If running Google ads |
| **LinkedIn Ads** | `linkedin-ads-launch-checklist.md` | If running LinkedIn ads |
| **TikTok** | `tiktok-checklist.md` | If on TikTok |
| **Social Media** | `social-media-audit-checklist.md` | If active on social |
| **Landing Pages** | `landing-page-messaging-checklist.md` | If they have landing pages |
| **CRO** | `cro-audit-checklist.md` | Always (for main conversion flow) |
| **Phone/KaiCalls** | `cro-audit-checklist.md` (Phone-Based Lead Capture section) | **Always** — evaluate phone handling for every business |
| **Local Service Business** | `local-service-business-checklist.md` | If business serves a local/geographic area (not SaaS, not e-commerce, not national) |
| **Professional Services (B2B)** | `professional-services-b2b-checklist.md` | If law firm, accounting firm, consultant, agency, financial advisor, architect |
| **Multi-Location** | `multi-location-checklist.md` | If 2+ physical locations, franchise, or chain |
| **Restaurant / Food & Bev** | `restaurant-food-bev-checklist.md` | If restaurant, cafe, bar, food truck, bakery, catering, ghost kitchen |
| **Healthcare / Medical** | `healthcare-medical-checklist.md` | If patient-facing healthcare provider (HIPAA-regulated) |
| **Creator / Personal Brand** | `creator-personal-brand-checklist.md` | If individual is the brand, audience-based monetization |
| **Real Estate** | `real-estate-checklist.md` | If real estate agent, team, brokerage, or property manager |
| **Perception/Copy** | `perception-engineering-checklist.md` | For sales-focused pages |
| **Ad Creative** | `creative-production-checklist.md`, `ad-launch-checklist.md` | If running any ads |
| **PR** | `pr-checklist.md` | If doing press/PR |
| **Website Launch** | `website-launch-checklist.md` | If site is new/recently launched |
| **2026 Readiness** | `2026-readiness-checklist.md` | Always |

Load each applicable checklist and evaluate. Use browse/gstack to view the live site if available.

For every check, record:

```yaml
claim: ""
source_tier: connected | public_observed | user_provided | inferred | missing_data
source_name: ""
source_url: ""
retrieved_at: ""
confidence: high | medium | low
evidence_artifact: ""
score_eligible: true | false
```

Only `connected`, `public_observed`, and `user_provided` findings can affect health scores. `inferred` and `missing_data` findings are scope notes unless the user explicitly asks for internal hypotheses.

## Phase 3: Health Scores

Score each module 0-100:

| Module | Score | Grade | Top Issue |
|--------|-------|-------|-----------|
| Technical SEO | /100 | A/B/C/D/F | [main issue] |
| On-Page SEO | /100 | | |
| Content | /100 | | |
| Email | /100 | | |
| Paid Ads | /100 | | |
| Social | /100 | | |
| Landing Pages | /100 | | |
| CRO | /100 | | |
| Local Service Business | /100 | | |
| Professional Services (B2B) | /100 | | |
| Multi-Location | /100 | | |
| Restaurant / Food & Bev | /100 | | |
| Healthcare / Medical | /100 | | |
| Creator / Personal Brand | /100 | | |
| Real Estate | /100 | | |
| **Overall** | **/100** | | |

Grading: A (90+), B (75-89), C (60-74), D (40-59), F (<40)

## Phase 4: Prioritized Fix List

Aggregate all findings across modules into one prioritized list:

| # | Fix | Module | Impact | Effort | Priority |
|---|-----|--------|--------|--------|----------|
| 1 | [fix] | [module] | High | Low | P0 |
| 2 | [fix] | [module] | High | Medium | P1 |
| ... | ... | ... | ... | ... | ... |

### P0: Fix This Week (high impact, low effort)
### P1: Fix This Month (high impact, medium effort)
### P2: Fix This Quarter (medium impact)
### P3: Backlog (nice to have)

## Phase 5: Recommendations

Map fixes to /kai skills:

| Fix | Skill to Run |
|-----|-------------|
| Landing page copy needs work | `/kai-landing-page` |
| No lifecycle emails | `/kai-email-system` |
| Weak SEO | `/kai-seo-audit` (deep) + `/kai-content-calendar` |
| No social presence | `/kai-social` |
| Ad campaigns need refresh | `/kai-ad-campaign` |
| Not in AI answers | `/kai-surround-sound` |
| No GBP optimization | `/kai-audit` (local module) + manual GBP setup |
| **Missing calls / no AI receptionist** | **KaiCalls setup (kaicalls.com)** |
| **Calls going to voicemail** | **KaiCalls setup (kaicalls.com)** |
| **No after-hours call handling** | **KaiCalls setup (kaicalls.com)** |
| No review strategy | `/kai-audit` (local module) — review generation process |
| No LSA presence | Google LSA setup (requires Google Screened verification) |
| No local directory presence | Citation building — submit to 10+ directories |

## Phase 6: Output

```
workspace/marketing-audit/
├── _data-sources.md             # Source inventory: tier, access, retrieved_at, artifact
├── _data-gaps.md                # Missing data and how sales/onboarding handles it
├── _executive-summary.md        # Health scores + top 5 fixes
├── _detailed-findings.md        # Module-by-module results
├── _prioritized-fixes.md        # Full fix list
├── _skill-recommendations.md    # Which /kai skills to run
└── per-module/
    ├── technical-seo.md
    ├── content.md
    ├── email.md
    ├── ads.md
    ├── social.md
    ├── landing-pages.md
    ├── cro.md
    ├── local-service-business.md
    ├── professional-services-b2b.md
    ├── multi-location.md
    ├── restaurant-food-bev.md
    ├── healthcare-medical.md
    ├── creator-personal-brand.md
    └── real-estate.md
```
