---
name: prd-v09-alternatives-pages
description: >
  Generate "X vs Y" and "Alternative to X" SEO/CRO pages targeting competitive search intent
  during PRD v0.9 Go-to-Market. Triggers on requests to build comparison pages, target
  competitive search traffic, or when user asks "build alternatives pages", "X vs Y page",
  "competitor comparison page", "we're better than X page", "capture branded search",
  "competitive SEO". Outputs SCR-ALT-* page specs and GTM-* channel entries.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Alternatives Pages (Competitive Comparison SEO/CRO)

Position in workflow: v0.9 AEO Audit → **v0.9 Alternatives Pages** → v0.9 Launch Metrics

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | 2 pages for the single most-searched competitor (X-vs-us + alternative-to-X) |
| **standard** | 5–10 pages covering top 3–5 competitors with both variant types; CRO copy + comparison table |
| **deep** | Full competitor portfolio (10+ competitors); plus multi-way comparison ("X vs Y vs Z"); page-level A/B test plan; SEO targeting per page |

## What This Does

Produces a portfolio of high-intent comparison pages — `/x-vs-us` and `/alternative-to-x` — that capture buyers actively searching for competitor names + comparison/alternative keywords. These are the highest-converting acquisition surface for B2B SaaS and many consumer products: the buyer has already passed awareness and is in active evaluation.

The pages must be **fair, credible, and conversion-oriented** — acknowledging where the competitor wins, claiming where you win, with social proof and a clear "when to pick each" guide. Aggressive trashing fails: buyers fact-check, and one false claim loses the page.

## How It Works

1. **Source the competitor list** — From the AEO Audit's comparison gaps and v0.2 CFD- competitive landscape. Rank by search volume (use Ahrefs/Semrush/free volume estimators) × buyer-intent strength.
2. **For each competitor, design two pages**:
   - **`/<competitor>-vs-<us>`** — Symmetric comparison. Buyer is comparing both.
   - **`/alternative-to-<competitor>`** — Asymmetric. Buyer is leaving competitor or shopping replacements.
3. **Apply the page template** (see Output Template) — Honest comparison table on 5–8 dimensions, "When to pick each" guidance, your unique attributes (from Dunford positioning), social proof, CTA.
4. **Anchor in positioning rules** — Each page must respect the BR-POS-* constraints. If positioning says "not for enterprise procurement," the page does not court enterprise buyers.
5. **Plan attribution** — Each page gets its own UTM source and a conversion event. Track per-page activation rate to identify dead pages.

## Example

Competitor: **Mixpanel** (mid-search-volume, B2B SaaS analytics).

**Page 1: `/mixpanel-vs-us`**

Symmetric comparison table:

| Dimension | Mixpanel | Us |
|-----------|----------|-----|
| Setup time | 1–2 weeks (data engineering required) | 15 minutes (autoinstrument) |
| Analytics depth | Industry-leading (cohorts, retention, funnels) | Solid (cohorts, funnels — no formula language) |
| Pricing | Custom enterprise; usage-based | Flat tier; predictable |
| Best-fit team | 50+ person product orgs | 1–20 person teams |

"**Pick Mixpanel if**: you have a data team and need advanced funnel/cohort analysis."
"**Pick us if**: you're a small team that needs analytics today, not after a 2-week setup."

CTA: "Start free trial — full setup in under an hour"

**Page 2: `/alternative-to-mixpanel`**

Asymmetric, replacement-oriented. Headline: "Looking for a faster Mixpanel alternative?" Same table, plus migration guide ("export your Mixpanel events; we'll set up identical funnels in 1 hour"), plus customer story ("[Customer X] moved off Mixpanel in 2 days — here's how").

## What You Get Back

- **SCR-ALT-\* page specs** — One per page. Includes URL slug, headline, comparison table content, "when to pick each" copy, social proof references, CTA. Hands off to design/dev for build.
- **GTM-\* with Type=Channel** for each page — The page treated as a channel (Owned layer), with attribution plan
- **Page priority queue** — Build order ranked by competitor search volume × conversion potential

## When to Use It

| Trigger | Mode |
|---------|------|
| AEO Audit identified comparison gaps | standard |
| Competitor raised prices / had a public incident (capture displaced buyers) | quick (single page, fast) |
| Quarterly competitive SEO refresh | standard |
| Launch wave needs additional Owned-channel surfaces | standard |
| Enterprise / paid-tier buyer education | deep |

Do **not** use for products in tightly regulated categories where comparison claims have legal exposure (e.g., medical devices, financial advice) without legal review.

## Consumes

- **CFD-\* competitive alternatives** (from v0.2 + v0.3 Moat) — Anchor for honest comparison; CFD- entries should include competitor strengths, not just weaknesses
- **GTM-AEO-\* gaps** (from v0.9 AEO Audit) — Comparison gaps become page priorities
- **GTM-\* positioning** + **BR-POS-\*** (from v0.9 Positioning) — Defines "when to pick us" claims; pages must honor BR-POS- constraints
- **CFD-\* customer stories** (from v0.1–v0.4 + post-launch) — Social proof and migration stories
- **FEA-\* feature list** — Anchor for "what we have" claims (no vaporware)

## Produces

- **SCR-ALT-\* page specs** (subcategorized SCR- entries for alternatives pages, lives in `SoT/SoT.USER_JOURNEYS.md` alongside other SCR- entries)
- **GTM-\* with Type=Channel** for each page (the page-as-channel with attribution plan)
- **CFD-\* gaps surfaced** — If a competitor strength is unaddressed, log CFD- research-gap

## Output Template

```
SCR-ALT-XXX: Comparison page — [Competitor] vs. Us
Type: ScreenAlternatives
Variant: [vs | alternative-to]
URL slug: /<competitor>-vs-<us> (or /alternative-to-<competitor>)
Owner: [Person / role]
Status: [Draft | Review | Live]

Headline: "[Headline]"
Subhead: "[Subhead]"

Comparison table (5–8 dimensions, honest):
  | Dimension | Competitor | Us |
  | ... | ... | ... |

"Pick competitor if": [Honest acknowledgment]
"Pick us if": [Anchored in BR-POS-* and positioning value claims]

Social proof:
  - CFD-XXX (testimonial or migration story)
  - [Customer logo references]

CTA: [Specific action; matches Offer Construction CTA where possible]

Linked IDs: CFD-XXX (competitor), GTM-YYY (positioning), FEA-ZZZ (feature claims), BR-POS-AAA (constraints)
Linked Channel: GTM-ALT-XXX
```

```
GTM-ALT-XXX: Channel — Alternatives page <slug>
Type: Channel
Layer: Owned
Status: Live

Channel: SEO/CRO page at <URL>
Attribution: utm_source=alt-page&utm_medium=organic&utm_campaign=<slug>
KPI target: KPI-AAA (alt-page → trial signup conversion rate)

Linked IDs: SCR-ALT-XXX (page), GTM-YYY (positioning), KPI-AAA
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Trash the competitor** | Page reads like a hit piece | Acknowledge where they win; credibility > short-term clicks |
| **Same page, find/replace competitor name** | 8 pages with identical structure | Each page tunes for the *specific* alternative's buyer profile |
| **Stale comparison data** | Comparison table is 18 months old | Quarterly refresh; date the page; cite version |
| **Vaporware feature claims** | Claiming features that don't ship | Every "we have" claim must trace to FEA- |
| **Ignoring BR-POS-*** | Page courts buyers positioning says aren't best-fit | Add "this might not be for you if..." section |
| **No "when to pick each"** | Pure us-favored framing | Buyers know it's biased; the "when to pick each" earns trust |
| **No social proof** | Empty assertion of superiority | Cite CFD- customer stories or migration data |

## Quality Gates

Before pages go live:

- [ ] Each page traces to one CFD- competitor entry
- [ ] Each page traces to GTM- positioning + at least one BR-POS- constraint
- [ ] "Pick competitor if" section exists on every page (the credibility test)
- [ ] All feature claims trace to shipping FEA-
- [ ] Attribution plan (UTM + KPI- target) per page
- [ ] Date on page; refresh schedule documented
- [ ] (deep mode) A/B test plan documented

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Launch Channels (ORB)** | Pages = Owned channels; added to mix matrix | `/x-vs-us` → GTM- Owned entry |
| **Launch Metrics** | Per-page conversion rates roll up to KPI-acquisition | KPI-ALT-conversion-rate |
| **Feedback Loop Setup** | Page bounce/scroll signals feed CFD- | Bounce on a specific section → CFD-gap |
| **AEO Audit (re-run)** | Pages should resolve comparison gaps; re-test after 4–6 weeks | Gap closure verification |
| **v1.0 Continuous Discovery** | Page winners suggest positioning sharpenings | High-converting page → positioning hypothesis |

## Detailed References

- jonathimer's `alternatives-pages` skill (devmarketing-skills)
- Corey Haines's `competitors` and `competitor-profiling` skills (marketingskills)
- (No bundled `references/` — competitor data lives in CFD-, not here)
