---
name: ad-spend-allocator
description: >
  Analyze multi-channel ad performance data and recommend budget reallocation across
  Google, Meta, LinkedIn, and other paid channels. Identifies over-indexed and under-indexed
  channels based on CAC, conversion rates, and funnel stage coverage. Produces specific
  dollar-amount shift recommendations.
tags: [ads]
---

# Ad Spend Allocator

Take performance data from multiple ad channels and figure out where your next dollar should go. This skill compares channels on equal terms, identifies where you're over-spending vs under-spending relative to results, and produces a concrete budget reallocation plan.

**Core principle:** Most startups either spread budget too thin across channels (no channel gets enough to learn) or dump everything into one channel (missing cheaper opportunities elsewhere). This skill finds the right distribution.

## When to Use

- "How should I split my ad budget?"
- "Should I spend more on Google or Meta?"
- "Reallocate my ad spend across channels"
- "Where am I getting the best return?"
- "I have $X/month for ads — how should I distribute it?"

## Phase 0: Intake

1. **Total monthly ad budget** — Current or planned
2. **Channels currently running** — Google Ads, Meta Ads, LinkedIn Ads, Twitter/X Ads, TikTok Ads, other
3. **Performance data per channel** — For each active channel:
   - Monthly spend
   - Impressions
   - Clicks / CTR
   - Conversions (and conversion type: demo, trial, purchase)
   - CPA or CAC
   - Revenue attributed (if available)
   - ROAS (if available)
4. **Primary conversion goal** — Demos / Trials / Purchases / MQLs
5. **Funnel data** (if available):
   - Lead → MQL rate
   - MQL → SQL rate
   - SQL → Close rate
   - Average deal size
6. **Channels you're considering but haven't tried** — Want to test new channels?
7. **Constraints** — Minimum spend on any channel? Platform you must stay on?

## Phase 1: Channel Normalization

### Apples-to-Apples Comparison

Normalize all channels to the same metrics:

| Channel | Monthly Spend | Impressions | Clicks | CTR | CPC | Conversions | Conv Rate | CPA | ROAS | CAC* |
|---------|-------------|------------|--------|-----|-----|-------------|----------|-----|------|------|
| Google Search | $[X] | [N] | [N] | [X%] | $[X] | [N] | [X%] | $[X] | [X] | $[X] |
| Google Display | ... | | | | | | | | | |
| Meta (FB/IG) | ... | | | | | | | | | |
| LinkedIn | ... | | | | | | | | | |
| [Other] | ... | | | | | | | | | |
| **Total** | $[X] | | | | | [N] | | $[X] avg | [X] avg | $[X] avg |

*CAC = Full customer acquisition cost if funnel data provided (CPA × close-rate adjustment)

### Funnel-Adjusted CAC (If Funnel Data Available)

```
Channel CAC = CPA ÷ (MQL rate × SQL rate × Close rate)
```

This reveals which channels produce leads that actually close, not just convert.

## Phase 2: Channel Efficiency Analysis

### 2A: Efficiency Ranking

| Rank | Channel | CPA | Funnel-Adj CAC | Share of Spend | Share of Conversions | Efficiency Index |
|------|---------|-----|---------------|----------------|---------------------|-----------------|
| 1 | [Channel] | $[X] | $[X] | [X%] | [X%] | [Conv share ÷ Spend share] |

**Efficiency Index:**
- **> 1.0** = Under-invested (getting more than its share of conversions)
- **= 1.0** = Proportional (fair share)
- **< 1.0** = Over-invested (getting less than its share)

### 2B: Marginal Return Analysis

For each channel, estimate if additional spend would yield proportional returns:

| Channel | Current CPA | Impression Share / Saturation Signal | Marginal Return Estimate |
|---------|-------------|-------------------------------------|------------------------|
| Google Search | $[X] | [X%] impression share — room to grow | Likely positive |
| Meta | $[X] | Frequency [X] — audience may be saturated | Diminishing |
| LinkedIn | $[X] | Low volume — limited targeting pool | Ceiling soon |

### 2C: Funnel Stage Coverage

| Funnel Stage | Channels Covering It | Current Spend | Gap? |
|-------------|---------------------|--------------|------|
| **Awareness** (top) | [Meta Display, YouTube] | $[X] | [Yes/No] |
| **Consideration** (mid) | [Google Search, Meta retargeting] | $[X] | [Yes/No] |
| **Decision** (bottom) | [Google Brand, Google Search] | $[X] | [Yes/No] |
| **Retargeting** | [Meta, Google Display] | $[X] | [Yes/No] |

## Phase 3: Reallocation Recommendations

### 3A: Budget Shift Table

| Channel | Current Spend | Recommended Spend | Change | Reasoning |
|---------|-------------|------------------|--------|-----------|
| Google Search | $[X] | $[Y] | +$[Z] | [Lowest CPA, room to scale] |
| Meta | $[X] | $[Y] | -$[Z] | [Audience saturation, frequency too high] |
| LinkedIn | $[X] | $[Y] | $0 | [Maintain — niche but valuable] |
| [New channel] | $0 | $[Y] | +$[Y] | [Test budget — competitors succeeding here] |
| **Total** | $[X] | $[X] | $0 | Budget-neutral reallocation |

### 3B: Scenario Modeling

**Scenario 1: Conservative shift (+/- 20%)**
- Expected conversions: [N] (currently [N]) = [X%] improvement
- Expected blended CPA: $[X] (currently $[X])
- Risk: Low

**Scenario 2: Aggressive shift (+/- 40%)**
- Expected conversions: [N] = [X%] improvement
- Expected blended CPA: $[X]
- Risk: Medium — less data on scaled channels

**Scenario 3: Budget increase to $[Y]/mo**
- Recommended allocation: [table]
- Expected conversions: [N]
- New channels to test: [list]

## Phase 4: Output Format

```markdown
# Ad Spend Allocation — [Product/Client] — [DATE]

Total monthly budget: $[X]
Active channels: [list]
Period analyzed: [date range]

---

## Current State

| Channel | Spend | % of Budget | Conversions | CPA | Efficiency |
|---------|-------|------------|-------------|-----|-----------|
| [Channel] | $[X] | [X%] | [N] | $[X] | [Over/Under/Fair] |

**Blended CPA:** $[X]
**Total conversions:** [N]

---

## Recommended Reallocation

| Channel | Current | Recommended | Change | Why |
|---------|---------|------------|--------|-----|
| [Channel] | $[X] | $[Y] | [+/-$Z] | [1-line reason] |

**Projected impact:**
- Conversions: [N] → [N] (+[X%])
- Blended CPA: $[X] → $[Y] (-[X%])

---

## Funnel Stage Coverage

[Coverage map with gaps identified]

---

## New Channel Recommendations

### [Channel Name]
- **Why test:** [Reasoning]
- **Recommended test budget:** $[X]/mo for [X weeks]
- **Success criteria:** CPA < $[X]
- **Competitors using it:** [Yes/No — who]

---

## Implementation Plan

### Week 1: Quick Shifts
- [ ] Reduce [Channel] from $[X] to $[Y]
- [ ] Increase [Channel] from $[X] to $[Y]
- [ ] Set up [New Channel] test campaign

### Week 2-4: Monitor
- [ ] Track CPA shifts on scaled channels
- [ ] Watch for diminishing returns signals
- [ ] Evaluate new channel performance

### Month 2: Re-evaluate
- [ ] Run this analysis again with new data
- [ ] Adjust allocations based on actual results
```

Save to `clients/<client-name>/ads/spend-allocation-[YYYY-MM-DD].md`.

## Cost

| Component | Cost |
|-----------|------|
| Data analysis | Free (LLM reasoning) |
| Statistical modeling | Free |
| **Total** | **Free** |

## Tools Required

- No external tools needed — pure reasoning skill
- User provides multi-channel performance data

## Trigger Phrases

- "How should I allocate my ad budget?"
- "Should I spend more on Google or Meta?"
- "Reallocate my ad spend"
- "Where am I getting the best ROAS?"
- "Optimize my multi-channel ad budget"
