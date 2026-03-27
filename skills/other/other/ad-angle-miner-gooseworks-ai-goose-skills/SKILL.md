---
name: ad-angle-miner
description: >
  Mine the highest-converting ad angles from customer reviews, Reddit complaints,
  support tickets, and competitor ads. Extracts actual pain language, competitor
  weaknesses, and outcome phrases that real buyers use. Outputs a ranked angle bank
  with proof quotes and recommended ad formats per angle.
tags: [ads]
---

# Ad Angle Miner

Dig through customer voice data — reviews, Reddit, support tickets, competitor ads — to extract the specific language, pain points, and outcome desires that make ads convert. The output is an angle bank your team can pull from for any campaign.

**Core principle:** The best ad angles aren't invented in a brainstorm. They're extracted from what real people are already saying. This skill finds those angles and ranks them by strength of evidence.

## When to Use

- "What angles should we run in our ads?"
- "Find pain points we can use in ad copy"
- "What are people complaining about with [competitors]?"
- "Mine reviews for ad messaging"
- "I need fresh ad angles — not the same tired stuff"

## Phase 0: Intake

1. **Your product** — Name + what it does in one sentence
2. **Competitors** — 2-5 competitor names (for review mining)
3. **ICP** — Who are you targeting? (role, company stage, pain)
4. **Data sources to mine** (pick all that apply):
   - G2/Capterra/Trustpilot reviews (yours + competitors)
   - Reddit threads in relevant subreddits
   - Twitter/X complaints or praise
   - Support tickets or NPS comments (paste or file)
   - Competitor ads (Meta + Google)
5. **Any angles you've already tested?** — So we can skip those

## Phase 1: Source Collection

### 1A: Review Mining

Run `review-scraper` for your product and each competitor:

```bash
python3 skills/review-scraper/scripts/scrape_reviews.py \
  --product "<product_name>" \
  --platforms g2,capterra \
  --output json
```

Focus on:
- **1-2 star reviews of competitors** — Pain they're failing to solve
- **4-5 star reviews of you** — Outcomes that delight buyers
- **4-5 star reviews of competitors** — Strengths you need to counter or match
- **Review language patterns** — Exact phrases buyers use

### 1B: Reddit/Community Mining

Run `reddit-scraper` for relevant subreddits:

```bash
python3 skills/reddit-scraper/scripts/scrape_reddit.py \
  --query "<product category> OR <competitor> OR <pain keyword>" \
  --subreddits "<relevant_subreddits>" \
  --sort relevance \
  --time month \
  --limit 50
```

Extract:
- Questions people ask before buying
- Complaints about current solutions
- "I wish [product] would..." statements
- Comparison threads (vs discussions)

### 1C: Twitter/X Mining

Run `twitter-scraper`:

```bash
python3 skills/twitter-scraper/scripts/scrape_twitter.py \
  --query "<competitor> (frustrating OR broken OR hate OR love OR switched)" \
  --max-results 50
```

### 1D: Competitor Ad Mining (Optional)

Run `ad-creative-intelligence` to see what angles competitors are currently using. This reveals:
- Angles they've validated (long-running ads = working)
- Angles they're testing (new ads)
- Angles nobody is running (white space)

### 1E: Internal Data (Optional)

If the user provides support tickets, NPS comments, or sales call transcripts — ingest and tag with the same framework below.

## Phase 2: Angle Extraction

Process all collected data through this extraction framework:

### Angle Categories

| Category | What to Look For | Ad Power |
|----------|-----------------|----------|
| **Pain angles** | Specific frustrations with status quo or competitors | High — pain motivates action |
| **Outcome angles** | Desired results buyers describe in their own words | High — positive aspiration |
| **Identity angles** | How buyers describe themselves or want to be seen | Medium — emotional resonance |
| **Fear angles** | Risks of NOT switching or acting | Medium — loss aversion |
| **Competitive displacement** | Specific reasons people switched from a competitor | Very high — direct comparison |
| **Social proof angles** | Outcomes or metrics buyers cite in reviews | High — credibility |
| **Contrast angles** | Before/after or old way/new way framings | High — clear value prop |

### For Each Angle, Extract:

1. **The angle** — One-sentence framing
2. **Proof quotes** — 2-5 verbatim quotes from sources
3. **Source count** — How many independent sources mention this?
4. **Competitor weakness?** — Does this exploit a specific competitor's gap?
5. **Emotional register** — Frustration / Aspiration / Fear / Relief / Pride
6. **Recommended format** — Search ad / Meta static / Meta video / LinkedIn / Twitter

## Phase 3: Scoring & Ranking

Score each angle on:

| Factor | Weight | Description |
|--------|--------|-------------|
| **Evidence strength** | 30% | Number of independent sources mentioning it |
| **Emotional intensity** | 25% | How strongly people feel about this (language intensity) |
| **Competitive differentiation** | 20% | Does this set you apart, or could any competitor claim it? |
| **ICP relevance** | 15% | How closely does this match the target buyer's world? |
| **Freshness** | 10% | Is this angle already overused in competitor ads? |

**Total score out of 100. Rank all angles.**

## Phase 4: Output Format

```markdown
# Ad Angle Bank — [Product Name] — [DATE]

Sources mined: [list]
Total angles extracted: [N]
Top-tier angles (score 70+): [N]

---

## Tier 1: Highest-Conviction Angles (Score 70+)

### Angle 1: [One-sentence angle]
- **Category:** [Pain / Outcome / Identity / Fear / Displacement / Proof / Contrast]
- **Score:** [X/100]
- **Emotional register:** [Frustration / Aspiration / etc.]
- **Proof quotes:**
  > "[Verbatim quote 1]" — [Source: G2 review / Reddit / etc.]
  > "[Verbatim quote 2]" — [Source]
  > "[Verbatim quote 3]" — [Source]
- **Source count:** [N] independent mentions
- **Competitor weakness exploited:** [Competitor name + specific gap, or "N/A"]
- **Recommended formats:** [Search ad headline / Meta static / Video hook / etc.]
- **Sample headline:** "[Draft headline using this angle]"
- **Sample body copy:** "[Draft 1-2 sentence body]"

### Angle 2: ...

---

## Tier 2: Worth Testing (Score 50-69)

[Same format, briefer]

---

## Tier 3: Emerging / Low-Evidence (Score < 50)

[Brief list — angles with potential but insufficient evidence]

---

## Competitive Angle Map

| Angle | Your Product | [Comp A] | [Comp B] | [Comp C] |
|-------|-------------|----------|----------|----------|
| [Angle 1] | Can claim ✓ | Weak here ✗ | Also claims | Not relevant |
| [Angle 2] | Strong ✓ | Strong | Weak ✗ | Not relevant |
...

---

## Recommended Test Plan

### Week 1-2: Test Tier 1 Angles
- [Angle] → [Format] → [Platform]
- [Angle] → [Format] → [Platform]

### Week 3-4: Test Tier 2 Angles
- [Angle] → [Format] → [Platform]
```

Save to `clients/<client-name>/ads/angle-bank-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| Review scraper (per product) | ~$0.10-0.30 (Apify) |
| Reddit scraper | ~$0.05-0.10 (Apify) |
| Twitter scraper | ~$0.10-0.20 (Apify) |
| Ad scraper (optional) | ~$0.40-1.00 (Apify) |
| Analysis | Free (LLM reasoning) |
| **Total** | **~$0.25-1.60** |

## Tools Required

- **Apify API token** — `APIFY_API_TOKEN` env var
- **Upstream skills:** `review-scraper`, `reddit-scraper`, `twitter-scraper`
- **Optional:** `ad-creative-intelligence` (for competitor ad angles)

## Trigger Phrases

- "Mine ad angles from reviews"
- "What angles should we run?"
- "Find pain language for our ads"
- "Build an ad angle bank for [client]"
- "What are people complaining about with [competitor]?"
