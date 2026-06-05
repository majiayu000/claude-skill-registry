---
name: kai-competitors
description: Competitive intelligence teardown — 5-layer analysis (signals, product, marketing, positioning, strategy) plus sales battlecard. Use when "competitor analysis", "competitive teardown", "who are our competitors", "battlecard", "competitive intel", "compare us to X", "what is X doing", or any request to research, analyze, or position against competitors.
---

Run a competitive intelligence teardown using the 5-layer CI framework. Produces analysis + sales battlecard.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Target Selection

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Your product** — what do you do?
2. **Competitors to analyze** — specific names, or "find them for me"?
3. **Depth** — quick (30 min, top 3) or deep (2-3 hours, full landscape)?
4. **Output need** — strategy doc, sales battlecard, or both?

Load: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\competitive-intelligence.md`

## Phase 2: 5-Layer Analysis

For each competitor, analyze:

### Layer 1: Signals (Observable Actions)
- Job postings (LinkedIn, careers page) — what roles are they hiring?
- Pricing changes — check their pricing page
- Recent feature launches — changelog, blog, Product Hunt
- Funding status — Crunchbase
- Executive changes — LinkedIn

### Layer 2: Product
- Core features vs yours (feature matrix)
- Pricing model and tiers
- Tech stack (if discoverable — BuiltWith, Wappalyzer)
- Integration ecosystem
- Free tier / trial model

### Layer 3: Marketing
- Traffic sources (estimate from content, ads, social presence)
- Content strategy (blog frequency, topics, SEO targets)
- Ad presence (Meta Ad Library, Google Ads Transparency)
- Social media activity and engagement
- Email strategy (subscribe and analyze)

### Layer 4: Positioning
- How they describe themselves (homepage headline, meta description)
- Who they say they're for (ICP from their copy)
- Messaging themes (what words/phrases they repeat)
- vs. your positioning — where do you overlap, where do you differ?

### Layer 5: Strategy
- Where are they investing? (infer from hiring, features, partnerships)
- What are they betting on long-term?
- Vulnerabilities — where are they weak or slow?
- Threats — where could they outflank you?

## Phase 3: Competitive Matrix

Generate a comparison table:

| Dimension | You | Competitor A | Competitor B | Competitor C |
|-----------|-----|-------------|-------------|-------------|
| Core offer | | | | |
| Price | | | | |
| Target ICP | | | | |
| Key differentiator | | | | |
| Biggest weakness | | | | |
| Growth trajectory | | | | |

## Phase 4: Sales Battlecard

Generate a 1-page battlecard per competitor:

```markdown
# Battlecard: [Your Product] vs [Competitor]

## Quick Win Positioning
[1-sentence positioning statement when this competitor comes up]

## When We Win
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

## When We Lose
- [Scenario 1 — and how to counter]
- [Scenario 2 — and how to counter]

## Their Pitch (What They'll Say)
- "[Claim 1]" → Our counter: [response]
- "[Claim 2]" → Our counter: [response]
- "[Claim 3]" → Our counter: [response]

## Killer Questions to Ask Prospects
- [Question that exposes competitor weakness 1]
- [Question that exposes competitor weakness 2]
- [Question that exposes competitor weakness 3]

## Landmines to Set
[Topics to raise early that shift evaluation criteria in your favor]
```

## Phase 5: Output

```
workspace/competitive-intel/
├── _landscape-overview.md       # Full 5-layer analysis
├── _competitive-matrix.md       # Comparison table
├── battlecards/
│   ├── vs-competitor-a.md
│   ├── vs-competitor-b.md
│   └── vs-competitor-c.md
└── _recommendations.md          # Strategic recommendations
```

## Quality Check

- Every claim about a competitor must cite a source or be labeled as inference
- Battlecard counters must be specific, not generic ("we're better" is not a counter)
- Killer questions must be genuinely useful in a sales conversation
- Matrix must be honest — mark where competitors genuinely win
