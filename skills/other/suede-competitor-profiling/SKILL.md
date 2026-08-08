---
name: suede-competitor-profiling
description: "Suede-owned competitive-intelligence discipline for evidence-backed profiles of positioning, pricing, messaging, product, proof, and public-market signals. Use when researching named competitors from current public URLs or refreshing a structured landscape. NOT FOR: publishing comparison pages (use suede-competitors), internal sales battle cards (use suede-sales-enablement), or deciding pricing changes (use suede-pricing)."
metadata:
  version: 2.0.0
---

# Suede Competitor Profiling

Use this Suede competitive-intelligence playbook to turn current public evidence into structured profiles with fact, inference, and unknowns kept separate.

## Initial Assessment

**Check for product marketing context first:**
If `.agents/product-marketing.md` exists (or `.claude/product-marketing.md`, or the legacy `product-marketing-context.md` filename, in older setups), read it before asking questions. Use that context and only ask for information not already covered.

Before profiling, confirm:

1. **Competitor URLs** — the list of competitor website URLs to profile
2. **Your product** — what you do (if not in product marketing context)
3. **Depth level** — quick scan (key facts only) or deep profile (full research)
4. **Focus areas** — any specific dimensions to prioritize (e.g., pricing, positioning, SEO strength, content strategy)

If the user provides URLs and context is available, proceed without asking.

---

## Core Principles

### 1. Facts Over Opinions
Every claim in a profile should be traceable to a source — captured public-page
content, review data, or clearly labeled provider metrics. Label inferences
clearly.

### 2. Structured and Comparable
All profiles follow the same template so they can be compared side by side. Consistency matters more than completeness on any single profile.

### 3. Current Data
Profiles are snapshots. Always include the date generated. Flag anything that looks stale (e.g., "pricing page last updated 2023").

### 4. Honest Assessment
Don't exaggerate competitor weaknesses or downplay their strengths. Accurate profiles are useful profiles.

---

## Saving Raw Data

Before synthesizing the profile, persist all raw page captures, SEO inputs, and
review evidence to disk so they can be re-read, audited, or reused without
repeating provider requests or manual collection.

**Directory layout** (relative to project root):

```
competitor-profiles/
├── raw/
│   └── <competitor-slug>/
│       └── <YYYY-MM-DD>/
│           ├── scrapes/    # one .md file per captured page (homepage.md, pricing.md, ...)
│           ├── seo/        # one .json or .csv file per authorized metric source
│           └── reviews/    # one .md or .json file per review source (g2.md, capterra.md, ...)
├── <competitor-slug>.md    # final synthesized profile
└── _summary.md             # cross-competitor summary
```

Rules:

- `<competitor-slug>` is lowercase, hyphenated (e.g. `responsehub`, `safe-base`)
- `<YYYY-MM-DD>` is the date the data was pulled — supports re-running and diffing snapshots over time
- Save each browser, manual, or authorized-fetch page capture as raw markdown
  to `scrapes/<page-name>.md`
- Save each authorized SEO response or user-supplied export to
  `seo/<source-name>.<json|csv>`
- Save each review source to `reviews/<source>.md` (cleaned text) or `.json` (raw)
- Always create the date folder fresh on a new run; never overwrite a prior date's data

The synthesized profile (`<competitor-slug>.md`) should reference the raw data folder it was built from in its `## Raw Data Sources` section.

---

## Research Process

### Phase 1: Public-Site Evidence

For each competitor URL, capture key public pages to extract positioning,
features, pricing, and messaging.

**Availability gate:** Inspect the tools currently exposed in the session
before selecting an acquisition method. A named connector is usable only when
it is actually available, connected to the intended account when applicable,
authorized for this task, and its current schema has been read. Do not invent a
tool call from the examples below.

If no mapping or page-fetch tool is available, use a browser-neutral/manual
fallback: open the public site, follow its primary navigation, inspect its
public sitemap or search results when accessible, record the exact URLs and
access date, and capture only evidence visible to the user. Respect access
controls, site terms, robots directives where applicable, and rate limits.

#### Step 1: Map the site

If a current authorized connector exposes a site-map or crawl capability, use
its documented schema to discover the site structure. For example, some
Firecrawl connections expose a `firecrawl_map` operation, but that name is not
guaranteed. Otherwise build the URL list through the manual fallback.

```
available map capability or manual navigation → verified competitor URLs
```

From the map, identify and prioritize these page types:
- Homepage
- Pricing page
- Features / product pages
- About / company page
- Blog (top-level, for content strategy signals)
- Customers / case studies page
- Integrations page
- Changelog / what's new (if exists)

#### Step 2: Capture key pages

If a current authorized connector exposes single-page fetch or extraction, use
its documented schema on each identified URL. For example, some Firecrawl
connections expose `firecrawl_scrape`. Otherwise open each public page and
capture the relevant visible text manually.

```
available page-fetch capability or browser/manual capture → page evidence
```

Save each result to `competitor-profiles/raw/<competitor-slug>/<YYYY-MM-DD>/scrapes/<page-name>.md` before extracting fields.

Extract from each page:

| Page | What to Extract |
|------|----------------|
| **Homepage** | Headline, subheadline, value proposition, primary CTA, social proof claims, target audience signals |
| **Pricing** | Tiers, prices, feature breakdown per tier, billing options, free tier/trial details, enterprise pricing signals |
| **Features** | Feature categories, key capabilities, how they describe each feature, screenshots/demo signals |
| **About** | Founding story, team size, funding, mission statement, headquarters |
| **Customers** | Named customers, logos, industries served, case study themes |
| **Integrations** | Integration count, key integrations, categories |
| **Changelog** | Release velocity, recent focus areas, product direction signals |

#### Step 3: Capture competitor reviews (optional but high-value)

If a connected search/fetch tool is available and authorized, use its current
schema to find the sources below. Otherwise search or browse them manually.
Platform-specific or account-only content may be accessed only when that
platform is actually connected and the user has authorized it.
- G2 reviews page for the competitor
- Capterra reviews page
- Product Hunt launch page
- TrustRadius profile

Save each scraped review page to `competitor-profiles/raw/<competitor-slug>/<YYYY-MM-DD>/reviews/<source>.md`. Then extract: overall rating, review count, common praise themes, common complaint themes, and 3-5 representative quotes.

---

### Phase 2: Optional SEO and Market Data

First inspect current available tools and user-provided files. If an authorized
SEO-data connector is exposed, read its current schemas and gather the same
metrics for every competitor. Some DataForSEO connections use the capability
names below, but their presence and exact schemas are not guaranteed. If no
provider is available, analyze a current user-supplied export or mark these
fields `not collected`; never substitute guessed values.

Save each raw response or export to
`competitor-profiles/raw/<competitor-slug>/<YYYY-MM-DD>/seo/` before parsing.
Record provider, access date, market, device, database, and that traffic,
authority, and value metrics are provider estimates. See
[references/tool-reference.md](references/tool-reference.md) for conditional
capability mapping and manual fallbacks.

#### Domain Authority & Backlinks

When the connected provider exposes an equivalent of `backlinks_summary`,
collect:
- Domain rank / authority score
- Total backlinks
- Referring domains count
- Spam score

When it exposes an equivalent of `backlinks_referring_domains`, collect:
- Top referring domains (quality signals)
- Link acquisition patterns

#### Keyword & Traffic Intelligence

When it exposes ranked-keyword data, collect:
- Total organic keywords ranking
- Keywords in top 3, top 10, top 100
- Estimated organic traffic

When it exposes a domain organic overview, collect:
- Domain-level organic metrics
- Estimated traffic value
- Top keywords by traffic

When it exposes site-keyword discovery, collect:
- What keywords they target
- Content gaps vs. your site

#### Competitive Positioning Data

When it exposes organic-competitor overlap, collect:
- Their closest organic competitors (may reveal competitors you haven't considered)
- Market overlap data

When it exposes relevant-page estimates, collect:
- Their highest-traffic pages
- Content that drives the most organic value

---

### Phase 3: Synthesis

Combine scraped content with SEO data to build the profile. Cross-reference claims (e.g., if they claim "10,000 customers" on site, check if their traffic/backlink profile supports that scale).

---

## Output Format

### Profile Document Structure

Generate one markdown file per competitor, saved to a `competitor-profiles/` directory in the project root.

**Filename**: `competitor-profiles/[competitor-name].md`

**For the full profile and summary templates**: See [references/templates.md](references/templates.md)

Each profile follows this structure:

```markdown
# [Competitor Name] — Competitor Profile

**URL**: [website]
**Generated**: [date]
**Depth**: [quick scan / deep profile]

---

## At a Glance

| Metric | Value |
|--------|-------|
| Tagline | [from homepage] |
| Founded | [year] |
| Headquarters | [location] |
| Team size | [estimate] |
| Funding | [if known] |
| Provider domain metric | [value, provider, market, and access date; or not collected] |
| Est. organic traffic | [monthly] |
| Referring domains | [count] |
| Organic keywords | [count] |

---

## Positioning & Messaging

**Primary value proposition**: [headline + subheadline from homepage]

**Target audience**: [who they're speaking to, based on copy analysis]

**Positioning angle**: [how they position — e.g., "simplicity-first," "enterprise-grade," "all-in-one"]

**Key messaging themes**:
- [theme 1 — with source page]
- [theme 2]
- [theme 3]

---

## Product & Features

### Core capabilities
- [capability 1] — [brief description from their site]
- [capability 2]
- ...

### Notable differentiators
- [what they emphasize as unique]

### Integrations
- [count] integrations
- Key: [list top 5-10]

### Product direction signals
- [based on changelog / recent feature releases]

---

## Pricing

| Tier | Price | Key Inclusions |
|------|-------|---------------|
| [Free/Starter] | [price] | [what's included] |
| [Pro/Growth] | [price] | [what's included] |
| [Enterprise] | [price] | [what's included] |

**Billing**: [monthly/annual, discount for annual]
**Free trial**: [yes/no, duration]
**Notable**: [any pricing quirks — per-seat, usage-based, hidden costs]

---

## Customers & Social Proof

**Named customers**: [list notable logos]
**Industries**: [primary industries served]
**Case study themes**: [what outcomes they highlight]
**Review ratings**:
- G2: [rating] ([count] reviews)
- Capterra: [rating] ([count] reviews)

---

## SEO & Content Strategy

**Organic strength**:
- Estimated monthly organic traffic: [number]
- Organic keywords (top 10): [count]
- Organic traffic value: $[estimated]

**Top organic pages** (by estimated traffic):
1. [page URL] — [keyword] — [est. traffic]
2. [page URL] — [keyword] — [est. traffic]
3. [page URL] — [keyword] — [est. traffic]

**Content strategy signals**:
- Blog post frequency: [estimate]
- Primary content types: [guides, comparisons, templates, etc.]
- Content focus areas: [topics they invest in]

**Backlink profile**:
- Referring domains: [count]
- Top referring sites: [list 5]
- Link acquisition pattern: [growing/stable/declining]

---

## Strengths & Weaknesses

### Strengths
- [strength 1 — with evidence source]
- [strength 2]
- [strength 3]

### Weaknesses
- [weakness 1 — with evidence source]
- [weakness 2]
- [weakness 3]

---

## Competitive Implications for [Your Product]

**Where they're strong vs. us**: [areas where this competitor has an advantage]

**Where we're strong vs. them**: [areas where you have an advantage]

**Opportunities**: [gaps in their offering or positioning we can exploit]

**Threats**: [areas where they're improving or gaining ground]

---

## Raw Data Sources

- Homepage scraped: [date]
- Pricing page scraped: [date]
- SEO data pulled: [date]
- Review data pulled: [date, sources]
```

---

### Summary Document

After profiling all competitors, generate a `competitor-profiles/_summary.md` that includes:

1. **Competitor landscape overview** — one paragraph summarizing the competitive field
2. **Comparison table** — key metrics side by side for all profiled competitors
3. **Positioning map** — where each competitor sits (e.g., simple↔complex, cheap↔premium)
4. **Key takeaways** — 3-5 strategic observations from the research
5. **Gaps and opportunities** — where the market is underserved

---

## Quick Scan vs. Deep Profile

### Quick Scan (faster, lower cost)
- Public-site evidence: homepage + pricing page only
- SEO: one consistent provider overview and ranked-keyword summary when an
  authorized source or user export is available; otherwise `not collected`
- Skip: reviews, technology stack, backlink details
- Output: abbreviated profile (At a Glance + Positioning + Pricing + SEO summary)

### Deep Profile (comprehensive)
- Public-site evidence: all key pages + available review sources
- SEO: full backlink analysis + keyword intelligence + competitor discovery
- Include: technology stack, content strategy analysis, review mining
- Output: full profile template

Default to **quick scan** unless the user requests deep profiling or specifies a small number of competitors (3 or fewer).

---

## Handling Multiple Competitors

When profiling more than one competitor:

1. **Parallelize only when supported** — capture independent homepages or
   pricing pages concurrently only when the available tool supports it and its
   quota allows it; otherwise work sequentially
2. **Use consistent metrics** — use the same available provider, market,
   device, database, date window, and metric definitions for every competitor;
   otherwise mark the comparison unavailable
3. **Build the summary last** — after all individual profiles are complete
4. **Prioritize by relevance** — if the user has 10+ competitors, suggest profiling the top 5 first based on domain overlap or market similarity

---

## Updating Profiles

Profiles are snapshots. When updating:

- Check pricing pages first (most volatile)
- Refresh SEO metrics only through the same available provider and matching
  market/device/database parameters, or mark them unavailable
- Scan changelog for product changes
- Update the "Generated" date
- Note what changed since last profile in a `## Change Log` section at the bottom

---

## Task-Specific Questions

Only ask if not answered by context or input:

1. What competitor URLs should I profile?
2. Quick scan or deep profile?
3. Any specific dimensions to focus on (pricing, SEO, positioning)?
4. Should I compare findings against your product?

---

## Boundaries

- Do not present inference, stale pricing, traffic estimates, review summaries, or feature availability as verified current fact.
- Do not access private accounts, bypass controls, scrape prohibited sources, contact competitors, or publish a dossier without authorization.
- Do not label a competitor weak, deceptive, or noncompliant without a stated comparison criterion and evidence.
- Do not decide product, pricing, legal, or sales strategy; surface supported implications and unresolved questions.

## Routing

- Need a public comparison or alternative page -> use `suede-competitors`.
- Need a sales battle card -> use `suede-sales-enablement`.
- Need review and forum synthesis -> use `suede-customer-research`.
- Need pricing, ad, or content implications -> use `suede-pricing`, `suede-ads`, or `suede-content-strategy`.
- From those skills, route current-source competitor research back to `suede-competitor-profiling`.
