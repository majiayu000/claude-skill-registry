---
name: pm-competitive
description: Готовит многомерный разбор конкурентов — feature-матрица, SWOT с cross-strategy, 5 сил Портера, сравнение ценообразования, позиционирование, прогноз стратегических ходов и три уровня дифференциации (догнать / отстроиться / создать новое). Адаптируется под цель (продуктовый дизайн / fundraising / стратегия / годовой обзор). User-invoked only — do NOT auto-trigger. Triggers on /pm-competitive, "конкурентный анализ", "разбор конкурентов", "five forces", "SWOT", "competitive analysis", "competitor comparison", "feature matrix vs competitors".
---

# pm-competitive — Competitive analysis


Part of the Personal Corp framework — running a one-person business through AI agents.
Run a systematic multi-dimensional competitor study. Branches by analysis purpose. Includes information-credibility tagging, time-stamping of all findings, and explicit separation of fact vs inference.

## Inputs

| Field | Required | Notes |
|---|---|---|
| Competitor list | yes | 2-5 names; > 5 → batch into rounds |
| Our product | no | Used for differentiation positioning |
| Purpose | no | Product design / fundraising deck / strategic planning / annual review; default product design |
| Dimensions | no | Features / pricing / UX / tech / business model; default features + pricing |

## Step 1 — Set purpose and depth

| Purpose | Emphasis | Output focus | Length |
|---|---|---|---|
| **Product design** | Features + UX | Feature matrix + differentiation list | 2-3 pages |
| **Fundraising deck** | Market structure + moats | Landscape map + moat analysis | 1 page |
| **Strategic planning** | Full depth | SWOT + 5-Forces + pricing + roadmap | 5-8 pages |
| **Annual review** | Market share change + trends | YoY changes + trend judgment | 2-3 pages |

## Step 2 — Information collection

Use user-supplied materials first (URLs, screenshots, pricing pages). Tag everything with credibility and timestamp.

**Credibility tiers:**

| Tier | Sources | Tagging |
|---|---|---|
| **High** | Official site, pricing page, official announcements | Quote directly |
| **Medium** | Media coverage, user reviews, industry reports | Cite source |
| **Low** | Rumors, speculation, outdated info | Mark `[unverified]` |

**Information-collection checklist:**

| Dimension | What to collect | Typical sources |
|---|---|---|
| Fundamentals | Founded, funding rounds, team size, user base | Official site, business databases |
| Product | Core feature list, recent updates, roadmap | Official site, changelog, blog |
| Pricing | Tiers, price ranges, free-tier limits | Pricing page |
| Reputation | Praise, complaints, NPS | Review sites, app stores, social platforms |
| Strategy | Target market, acquisition channels, partnerships | Press, social media |

**Always tag freshness** — e.g. "based on Q1 2026 public information" — and prompt user to verify currency.

## Step 3 — Porter's Five Forces

Evaluate from industry-structure angle.

| Force | Dimension | Evaluation points |
|---|---|---|
| **Supplier power** | Upstream dependency | Concentration of key tech/talent/resources; switching cost |
| **Buyer power** | Downstream customer leverage | Customer concentration; switching cost; price sensitivity |
| **New-entrant threat** | Entry barriers | Tech / capital / brand / network effects / regulation |
| **Substitute threat** | Alternative solutions | What's the user's current alternative? Substitute's value-for-money? |
| **Industry rivalry** | Existing-player dynamics | Competitor count, concentration, differentiation, exit barriers |

Output: each force = strong / medium / weak + one-sentence rationale. Overall industry attractiveness = high / medium / low.

## Step 4 — Multi-dimensional comparison

**Feature comparison matrix (core deliverable):**

| Module | Sub-feature | Us | Comp A | Comp B | Comp C |
|---|---|---|---|---|---|
| {module 1} | {sub 1} | ✅ Mature | ✅ Mature | ⚠️ Basic | ❌ None |
| | {sub 2} | ⚠️ Basic | ✅ Mature | ✅ Mature | ⚠️ Basic |

Legend: ✅ Mature / ⚠️ Basic (exists but limited) / ❌ Missing / 🔜 Planned

**Positioning deep-dive:**

| Dimension | Method | Scoring |
|---|---|---|
| **Feature score** | 1-5 per module, weighted total | 5 = best-in-class, 3 = passing, 1 = barely present |
| **UX comparison** | Steps in core flow, learning curve, completion efficiency | Compare clicks + time-to-complete |
| **Tech architecture** | Patterns, stack, performance, openness | API openness, integration capability, extensibility |

**SWOT per competitor:**

| | Positive | Negative |
|---|---|---|
| **Internal** | Strengths (core advantages) | Weaknesses (clear gaps) |
| **External** | Opportunities (exploitable) | Threats (must watch) |

Each quadrant: 2-3 items, each with factual support. Banned: vague claims like "strong team" or "advanced tech".

**SWOT cross-strategies:**

| Strategy | Meaning | Direction |
|---|---|---|
| **SO** | Strengths × Opportunities | Use strengths to grab market window |
| **WO** | Weaknesses × Opportunities | Fill gaps to capture new opportunities |
| **ST** | Strengths × Threats | Use moats to defend against attacks |
| **WT** | Weaknesses × Threats | Most urgent defensive priorities |

**Pricing comparison (if pricing dimension included):**

| Item | Us | A | B | C |
|---|---|---|---|---|
| Free-tier scope | {} | {} | {} | {} |
| Entry-tier monthly | {} | {} | {} | {} |
| Enterprise monthly | {} | {} | {} | {} |
| Billing model | {per-seat / usage / feature-tier} | | | |
| Core differentiator | {pricing strategy reading} | | | |

**Pricing-strategy types:**
- **Penetration:** low price for share (look for generous free tier)
- **Skimming:** high price, premium positioning (look for many gated advanced features)
- **Freemium:** core free, advanced paid (look at the gap between free and paid)

## Step 5 — Positioning quadrant

Pick two most-discriminating dimensions (e.g. "feature depth vs ease of use", or "price vs feature breadth") and place all products into a 2×2:

| Quadrant | Trait | Products |
|---|---|---|
| High features + high price | Enterprise full-stack | {list} |
| High features + low price | Best value | {list} |
| Low features + high price | Niche specialist | {list} |
| Low features + low price | Entry-level | {list} |

## Step 6 — Strategic projection

Predict competitor's likely next moves based on recent signals.

**Method:**

1. **Signal collection:** product updates, funding moves, hiring focus, partnership announcements (last 3-6 months)
2. **Pattern recognition:** what does the cluster of signals imply?
   - Repeated feature launches in area X → betting on X
   - Heavy hiring in role Y → preparing new product line
   - Price cut / new free tier → market-share grab
3. **Projection output:**

| Competitor | Recent moves | Inferred intent | Impact on us | Confidence | Recommended response |
|---|---|---|---|---|---|
| {A} | {actions} | {hypothesis} | {assessment} | High/Medium/Low | {strategy} |

**Projection rules:**
- Distinguish "fact" from "inferred intent" — second always tagged with confidence
- One signal can have multiple readings — list 2-3 most likely
- Time windows: short-term (1-3 months), mid-term (3-12 months)

## Step 7 — Three-tier differentiation strategy

| Tier | Definition | Action |
|---|---|---|
| **Catch-up** | Competitors have it; we don't | List features to add + priority + estimated effort |
| **Differentiate** | We're unique or clearly ahead | List strengths to reinforce + marketing message ideas |
| **Innovate** | No competitor has done it; opportunity exists | List blue-ocean candidates + validation approach |

## Quality bar

1. Comparisons grounded in verifiable public info; cite source + date
2. Same dimension scored on the same scale across all products
3. Every SWOT item backed by a fact; no fluff
4. Differentiation suggestions concrete and prioritized
5. All data tagged with freshness ("as of Q1 2026")
6. Pricing data tagged with collection date
7. Strategic projections separate fact from inference
8. Five-Forces evaluation grounded in industry data

## Red lines

1. **No fabricated data** — unverified info → `[unverified]`
2. **No subjective trash-talk** — competitor evaluation must be objective; no pejoratives
3. **Always tag freshness** — every data point + collection date; nudge user to refresh
4. **Tag inference confidence** — every strategic projection labeled with confidence

## Market-structure judgment

| Structure | Trait | Strategy advice |
|---|---|---|
| **One-dominant** | One player > 50% share | Differentiate niches, avoid head-on |
| **Duopoly** | Top 2 = > 70% combined | Pick a side, or be the third option |
| **Fragmented** | Top 5 each < 20% | Speed-grab a niche #1 position |
| **Emerging** | No clear leader | Educate market first, build brand |

## Monitoring cadence

| Frequency | What to monitor | Trigger |
|---|---|---|
| **Weekly** | Product changelog, social signals | Major updates → tracker entry |
| **Monthly** | Pricing changes, new features, press | Update feature matrix |
| **Quarterly** | Full competitor report, strategy projection refresh | Quarterly competitor brief |
| **Event-driven** | Funding / M&A / major launches / exec changes | Immediate impact assessment |

## When input is incomplete

- **Only competitor names** → standard feature matrix + brief SWOT
- **No own product** → competitor-vs-competitor comparison only, no differentiation advice
- **> 5 competitors** → batch, or pick 3 for deep-dive + brief notes on others

## Related skills

- `/pm-prd` — differentiation gap → PRD
- `/pm-prioritize` — catch-up feature list → RICE-rank
- `/pm-feedback` — user mentions of competitors → enrich perception data
- `/pm-brainstorm` — diverge on differentiation ideas

