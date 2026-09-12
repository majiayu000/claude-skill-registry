---
name: competitor-alternatives
description: "Creates high-converting 'X vs Y' and 'X alternatives' SEO pages that capture comparison search traffic. Researches competitors, writes honest comparison content, and adds schema markup (FAQPage, ItemList). Use when someone needs alternatives pages, comparison content, or says 'alternatives page', 'vs page', 'comparison', 'competitor alternatives', 'X vs Y page', or wants to capture competitor brand search traffic with SEO content. Also trigger when someone wants to rank for competitor brand names, capture competitor search traffic, create a compare page, or build a competitive content hub. Even if they just say 'how do we compete with X' or 'we need to show up when people search for [competitor]', this skill applies. Owns the individual alternatives / vs / comparison page. For a batch roadmap of many pages with a phase tracker, see /seo-machine. For programmatic SEO and templated content at scale, see /seo-content."
category: seo
tier: nice-to-have
reads:
  - brand/competitors.md
  - brand/positioning.md
  - brand/voice-profile.md
  - brand/audience.md
  - brand/landscape.md
writes:
  - campaigns/comparisons/vs/{competitor}-vs-{product}.md
  - campaigns/comparisons/alternatives/{competitor}-alternatives.md
triggers:
  - alternatives page
  - vs page
  - comparison page
  - competitor alternatives
  - X vs Y
  - compete with
  - competitor search traffic
  - brand comparison
  - capture traffic
allowed-tools: []
---

# Competitor Alternatives Pages

## Purpose

People searching "[Competitor] alternatives" or "[Product] vs [Competitor]" have high purchase intent. They already know the category — they're choosing. This skill captures that traffic with structured comparison content that ranks and converts.

## On Activation

1. Read `brand/` directory: load `competitors.md`, `positioning.md`, `voice-profile.md`, `audience.md` if present.
2. Show what loaded:

## Backend Selection

Prefer OpenSEO `find_serp_competitors` / `get_serp_results` and `openseo-competitor-analysis` findings when configured; otherwise Exa SERP scrape with overlap `unknown`. Full contract: `skills/openseo/references/backend-contract.md`.

```
Brand context loaded:
├── Competitors    ✓/✗  ({N} competitors profiled)
├── Positioning    ✓/✗  ("{primary angle}")
├── Voice Profile  ✓/✗
└── Audience       ✓/✗
```
3. If `competitors.md` is missing: suggest running `/competitive-intel` first, or ask user to provide competitor names, pricing, and key differentiators.
4. If `positioning.md` is missing: ask for the product's primary value prop and target audience.
5. Ask which competitors to create pages for (or "all" from competitors.md).
6. Read `brand/landscape.md` if it exists — check the Claims Blacklist before making ecosystem or competitive claims. If stale (>14 days) or missing, warn that market claims may be outdated.

## Reads

- `brand/competitors.md` — Known competitors, their positioning, pricing, weaknesses
- `brand/positioning.md` — Your product's unique value props, differentiators, target audience
- `brand/voice-profile.md` — Tone for comparison copy
- `brand/audience.md` — Who is choosing between you and competitors

## Depends On

- `competitive-intel` — Should have competitor research completed first (not hard-blocked — can proceed with user-provided data)

## Workflow

### Step 1: Identify Comparison Queries

Pull from `competitors.md` and generate the full keyword set:

- `[competitor] alternatives` (highest volume)
- `[competitor] vs [your product]` (branded)
- `[your product] vs [competitor]` (branded reverse)
- `best [category] tools` (category)
- `[competitor] review` (review intent)
- `[competitor] pricing` (price-sensitive)

Prioritize by: search volume estimate > purchase intent > your win rate against that competitor.

### If Web Search Is Unavailable

Use data from brand/competitors.md if it exists. Ask the user directly for: competitor pricing, key strengths/weaknesses, and notable reviews or complaints they've seen. Note limitation: 'Competitor data is based on provided context, not live research. Verify current pricing and features before publishing.'

### Step 2: Research Each Competitor

For each competitor page, gather:

- **Core product** — What they actually do (one sentence)
- **Pricing** — Free tier, paid plans, enterprise
- **Strengths** — 3-5 genuine strengths (be honest, builds credibility)
- **Weaknesses** — 3-5 real weaknesses (factual, not snarky)
- **Best for** — Their ideal customer profile
- **Not ideal for** — Where they fall short (your opportunity)
- **Key reviews** — G2, Capterra, Reddit sentiment summary

### Step 3: Write the Comparison Page

Structure for each page:

```markdown
---
title: "[Competitor] vs [Your Product]: Honest Comparison [Year]"
description: "Comparing [Competitor] and [Your Product] on features, pricing, and ease of use. See which is right for your needs."
slug: /compare/[competitor]-vs-[your-product]
schema: ComparisonPage
---

## TL;DR

[2-3 sentence verdict. Be specific about WHO should pick which tool.]

## Quick Comparison

| Feature | [Your Product] | [Competitor] |
|---------|---------------|--------------|
| [Feature 1] | [Status/Detail] | [Status/Detail] |
| [Feature 2] | [Status/Detail] | [Status/Detail] |
| Pricing starts at | $X/mo | $Y/mo |
| Free tier | Yes/No | Yes/No |
| Best for | [Audience] | [Audience] |

## [Your Product] Overview
[2-3 paragraphs. Lead with your strongest differentiator against THIS specific competitor.]

## [Competitor] Overview
[2-3 paragraphs. Fair and accurate. Acknowledge their strengths.]

## Feature-by-Feature Breakdown

### [Category 1]
[Detailed comparison with specifics, not vague claims]

### [Category 2]
[Same pattern]

## Pricing Comparison
[Side-by-side pricing breakdown. Include hidden costs, overage fees, feature gates.]

## Verdict: Which Should You Choose?

**Choose [Your Product] if:**
- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]

**Choose [Competitor] if:** (**REQUIRED — 3 honest tradeoffs minimum**)
- [Specific use case where they genuinely win — cite the feature, not a vague claim]
- [Another honest scenario — name the situation concretely]
- [A third where they're objectively better — pricing tier, integration, niche capability]

> **Honesty section is non-negotiable.** Three concrete, verifiable scenarios where the competitor wins. This is the section that earns the reader's trust — and the section AI Overviews and ChatGPT cite when picking which comparison page to surface. Pages without it underperform measurably on both ranking AND conversion. "We're better at everything" reads as marketing copy; "they're better at X, Y, Z but we're better at A, B, C" reads as a real comparison.

## Ready to try [Your Product]?
[CTA — free trial, demo, or signup. Match to the comparison context.]
```

### Step 4: Write the Alternatives Roundup

For the "[Your Product] alternatives" defensive page and "[Competitor] alternatives" offensive pages:

```markdown
---
title: "Best [Competitor] Alternatives [Year]"
description: "Looking for [Competitor] alternatives? Compare the top X options including pricing, features, and who each is best for."
slug: /compare/[competitor]-alternatives
schema: ItemList
---

## Why People Switch from [Competitor]

[3-5 common reasons based on review mining — pricing, missing features, UX friction]

## Best [Competitor] Alternatives

### 1. [Your Product] — Best for [specific use case]
**Pricing:** ...
**Key difference:** ...
**Best for:** ...

### 2. [Alternative 2] — Best for [different use case]
[Same structure]

### 3-5. [More alternatives]
[Same structure, be genuinely helpful]

## Comparison Table
[Full matrix of all alternatives]

## How to Choose
[Decision framework based on use case, team size, budget]
```

### Step 5: Schema Markup

Add JSON-LD schema to each page:

- **VS pages** — Use `FAQPage` schema with common comparison questions
- **Alternatives pages** — Use `ItemList` schema for the roundup
- Both — Include `Article` schema with author, date, modified date

## Verdict Frameworks

Use these to write honest, credible verdicts:

**The Acknowledger:** "While [Competitor] excels at [X], [Your Product] is purpose-built for [Y] — which matters more if you're [target use case]."

**The Segmenter:** "[Competitor] is the right choice for [persona A]. But if you're [persona B], [Your Product] will save you [specific outcome]."

**The Switcher:** "If you're already using [Competitor] and frustrated by [common complaint], [Your Product] solves that with [specific feature]."

## Brand Integration

- **positioning.md** → Every comparison verdict ties back to the positioning angle. Don't just compare features — compare through the lens of your unique value proposition.
- **competitors.md** → Use teardown data for accurate, specific claims. Vague comparisons destroy credibility. Cite specific features, pricing, and limitations.

## CTA Templates

**For clear wins:** "Start your free trial — most teams switch from [Competitor] in under an hour."

**For close comparisons:** "Not sure yet? Try both free tiers and compare with your actual workflow."

**For price-sensitive:** "Get [Competitor]-level features at [fraction] of the cost. See pricing."

## Output

Each comparison generates:
- One markdown file per competitor (VS page)
- One alternatives roundup page per competitor
- One defensive "alternatives to [your product]" page
- SEO metadata and schema markup included in frontmatter
- Internal linking suggestions between comparison pages

## File Output Format

### Directory Structure

```
./campaigns/comparisons/
├── vs/
│   ├── {competitor-slug}-vs-{your-product-slug}.md
│   └── ...
├── alternatives/
│   ├── {competitor-slug}-alternatives.md
│   └── {your-product-slug}-alternatives.md  (defensive)
└── index.md                                  (comparison hub page)
```

### Frontmatter (VS Pages)

```yaml
---
title: "{Competitor} vs {Your Product}: Honest Comparison {Year}"
meta_description: "{150-160 chars}"
slug: /compare/{competitor}-vs-{your-product}
page_type: comparison
competitor: "{Competitor Name}"
date_created: "{YYYY-MM-DD}"
last_updated: "{YYYY-MM-DD}"
status: "draft"
schema_faq: |
  {FAQPage JSON-LD}
schema_article: |
  {Article JSON-LD}
---
```

### Frontmatter (Alternatives Pages)

```yaml
---
title: "Best {Competitor} Alternatives {Year}"
meta_description: "{150-160 chars}"
slug: /compare/{competitor}-alternatives
page_type: alternatives
competitor: "{Competitor Name}"
alternatives_count: {number}
date_created: "{YYYY-MM-DD}"
last_updated: "{YYYY-MM-DD}"
status: "draft"
schema_itemlist: |
  {ItemList JSON-LD}
schema_article: |
  {Article JSON-LD}
---
```

---

## Quality Checks

- [ ] Every competitor strength acknowledged (credibility)
- [ ] **Honesty section present with ≥3 concrete tradeoffs where the competitor wins** (non-negotiable — pages without this underperform)
- [ ] Feature claims are specific, not vague ("AI-powered" means nothing)
- [ ] Pricing is current and includes all tiers
- [ ] Verdict is genuinely helpful, not just "pick us"
- [ ] Schema markup validates
- [ ] CTAs match the comparison context
- [ ] No competitor trademark violations in meta titles
- [ ] Files saved to correct paths with complete frontmatter

---

## Anti-Patterns

- **Snark destroys credibility.** Backhanded compliments ("Competitor is fine if you don't need real features") make you look petty, not confident. Genuine respect for competitors makes your wins land harder — the reader trusts you more when you're fair.
- **Unverifiable claims undermine everything.** "Our platform is 10x faster" without benchmarks reads as marketing fluff. Readers researching alternatives are already skeptical — every claim needs evidence (benchmark, case study, specific feature comparison).
- **Acknowledging competitor strengths builds trust.** Readers know competitors aren't terrible — they're actively considering them. Trying to make competitors look bad makes your content look biased. Honest acknowledgment is what makes your differentiators credible.
- **Stale pricing erodes trust instantly.** If a reader checks and your pricing is wrong, they'll question everything else on the page. When you can't verify current pricing, say "as of {date}" and note it may have changed — this is more trustworthy than confident-but-wrong numbers.
- **Thin comparison pages are doorway pages.** A feature table with checkmarks and no analysis doesn't help anyone choose. Each page needs genuine insight about *when* to choose each option — that's what earns the ranking and the conversion.
- **Skipping the honesty section breaks the trust contract.** Pages that claim "we win on every dimension" read as marketing copy. Readers researching alternatives are already skeptical of vendor-published comparisons — three honest tradeoffs where the competitor wins is the credibility move that lets your differentiators land. AI Overviews and ChatGPT cite honest pages over self-serving ones because they're more useful to the searcher. The honesty section isn't a generosity; it's a positioning lever.

---

## Error States

- **No competitors.md:** Ask user for competitor names and key info. Suggest running `/competitive-intel` first for thorough research. Can proceed with user-provided data.
- **No positioning.md:** Ask user for their product's value prop, target audience, and key differentiators. Comparison quality will be lower without clear positioning.
- **No web search available:** Use data from brand/competitors.md. Ask user directly for current pricing and recent product changes. Note: "Competitor data based on provided context — verify current pricing and features before publishing."
- **Incomplete competitor data:** Generate pages for competitors with sufficient data, skip others. Note which competitors need more research.
- **Can't save files:** Display content for manual copy. Suggest checking write permissions.

---

## Chain Offers

After saving, suggest:

- `/competitive-intel` — deepen research on specific competitors
- `/seo-content` — create supporting content (e.g., "[category] buyer's guide")
- `/page-cro` — optimize comparison pages for conversion
- `/content-atomizer` — distribute comparison insights across social channels
- "Update" — refresh pricing and features periodically
