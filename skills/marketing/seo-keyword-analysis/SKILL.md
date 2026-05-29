---
name: seo-keyword-analysis
description: "Keyword analysis using GSC data. Use when: evaluating keywords, validating niches, finding quick wins. Triggers on: 'keyword analysis', 'SEO analysis', 'quick wins'."
allowed-tools:
  - webfetch
  - Read
  - mcp__gsc__list_sites
  - mcp__gsc__search_analytics
  - mcp__gsc__enhanced_search_analytics
  - mcp__gsc__detect_quick_wins
  - mcp__gsc__index_inspect
---

# SEO Keyword Analysis

Analyze keywords using Google Search Console data combined with proven SEO methodology.

## Analysis Modes

### Mode 1: New Keyword Research
For keywords you don't rank for yet. Analyze SERP and competition.

### Mode 2: Existing Performance Analysis
For keywords you already rank for. Pull real data from GSC.

### Mode 3: Quick Wins Detection
Find low-hanging fruit: high impressions, good position, but low CTR.

---

## Core Methodology

### The Match and Exceed Principle

**This is the most important concept.** Before pursuing any keyword:

1. **Search the keyword on Google**
2. **Analyze top 10 results**:
   - What content type ranks? (tools, blogs, landing pages)
   - What's the content quality?
   - What's the Domain Authority of competitors?
3. **Ask yourself**:
   - Can I create something BETTER than what's ranking?
   - Do I have the resources to match the content type?
   - Can I exceed their authority over time?

**Example**:
- "free headshot generator" → Top results are all tools → You MUST build a tool
- "dragon tattoo ideas" → Top results are low-quality Pinterest/Wikipedia → Easy to exceed

---

## Keyword Types Strategy

### Short-tail Keywords
- **Definition**: 1-2 words (e.g., "car insurance", "AI headshots")
- **Characteristics**: High volume, high competition
- **Strategy**: Target AFTER building authority, not initially
- **Risk**: Very hard to rank without established backlinks

### Long-tail Keywords
- **Definition**: 3+ words (e.g., "best AI headshot generator for LinkedIn")
- **Characteristics**: Lower volume, lower competition, higher conversion
- **Strategy**: Start here! KD typically < 20
- **Advantage**: Quantity compensates for lower volume

### LSI Keywords (Latent Semantic Indexing)
- **Definition**: Semantically related keywords
- **Example**: For "AI tattoo generator":
  - "tattoo ideas"
  - "dragon tattoo design"
  - "forearm tattoo inspiration"
- **Strategy**: Expand from seed keyword to build content cluster

---

## Key SEO Metrics

### 1. Keyword Difficulty (KD)
| KD | Assessment | Backlinks Needed | Action |
|----|------------|------------------|--------|
| 0-10 | Very Easy | 0-5 | 🟢 Pursue immediately |
| 11-20 | Easy | 5-10 | 🟢 Good target |
| 21-40 | Medium | 10-50 | 🟡 Need some authority |
| 41-60 | Hard | 50-100+ | 🔴 Only with strong domain |
| 60+ | Very Hard | 100+ | 🔴 Avoid unless massive site |

**Target: KD < 20 for new sites**

### 2. Domain Authority (DA) / Page Authority (PA)
- **DA**: Overall domain strength
- **PA**: Specific page strength
- **Strategy**: Look for keywords where low DA/PA sites rank → opportunity
- **Quality > Quantity**: One CNN backlink (DA 90) > 100 low-DA links

### 3. Search Volume
| Volume | Classification | Strategy |
|--------|---------------|----------|
| < 100 | Too low | Skip unless very high CPC |
| 100-500 | Long-tail | Good for new sites |
| 500-5000 | Sweet spot | Target these |
| 5000+ | High volume | Need authority first |

**Click distribution**: #1 gets ~30%, #2 gets ~15%, #3 gets ~10%

### 4. Cost Per Click (CPC)
- **High CPC = High commercial value**
- **Example**: If advertisers pay $5+ per click, the keyword is lucrative
- **Ideal combo**: High CPC + Low KD + Decent volume = Goldmine

### 5. Geographic Distribution
- **50%+ from US** = Better monetization potential
- Western countries (US, UK, Canada, Australia) pay more
- Consider this when validating niche viability

---

## Niche Validation Checklist

Before pursuing a keyword/niche, verify ALL of these:

```
□ KD < 20 (or reasonable for your authority level)
□ Search volume > 100/month (ideally 500+)
□ Clear user intent identified
□ Top SERP results are beatable (Match & Exceed)
□ Monetization path exists (CPC check, product fit)
□ 50%+ traffic from monetizable regions
□ You can create the required content type
□ Related keywords exist for expansion (LSI)
□ Not dominated by major brands (CNN, Wikipedia, Amazon)
□ Not a YMYL topic without E-E-A-T credentials
```

---

## Red Flags (Auto-Avoid)

| Red Flag | Example | Why |
|----------|---------|-----|
| No search volume | ComfyUI workflows | No demand |
| KD > 60 | Car insurance (KD 83) | Impossible competition |
| Brand dominated | Major media owns SERP | Can't compete |
| YMYL without credentials | Medical advice | E-E-A-T required |
| Top results too good | Comprehensive tools | Can't exceed |

---

## Green Light Indicators

| Indicator | Why Good |
|-----------|----------|
| KD < 20 + Volume 500+ | Low effort, decent traffic |
| "Generator" or "free" in keyword | Tool opportunity |
| Low-quality SERP (Pinterest, forums) | Easy to exceed |
| High CPC + Low KD | Profitable + achievable |
| Clear content cluster potential | Multiple pages possible |

---

## GSC Integration Workflow

### Step 1: List Available Sites
```
mcp__gsc__list_sites
```

### Step 2: Pull Keyword Performance
```
mcp__gsc__search_analytics
- siteUrl: "sc-domain:example.com"
- startDate: "YYYY-MM-DD" (30 days ago)
- endDate: "YYYY-MM-DD" (today)
- dimensions: "query,page"
```

### Step 3: Find Quick Wins
```
mcp__gsc__detect_quick_wins
- positionRangeMin: 4
- positionRangeMax: 20
- minImpressions: 100
- maxCtr: 3
```

---

## Output Formats

### New Keyword Analysis

```
## Keyword Analysis: [keyword]

### Quick Verdict
[🟢 Pursue / 🟡 Consider / 🔴 Avoid] - [reason]

### Keyword Type
[Short-tail / Long-tail] - [strategy implication]

### Metrics
| Metric | Value | Assessment |
|--------|-------|------------|
| KD | [X] | [🟢/🟡/🔴] |
| Volume | [X]/mo | [🟢/🟡/🔴] |
| CPC | $[X] | [value assessment] |

### User Intent
- **Type**: [Informational/Commercial/Transactional/Navigational]
- **Required Content**: [what type to create]

### Match & Exceed Analysis
- **Top 3 Competitors**: [list with DA]
- **Content Quality**: [weak/moderate/strong]
- **Can We Exceed?**: [Yes/No + reasoning]

### Monetization Path
[How to make money from this keyword]

### LSI Expansion Opportunities
- [related keyword 1]
- [related keyword 2]
- [related keyword 3]

### Next Steps
1. [action]
2. [action]
```

### Existing Keyword (GSC Data)

```
## Performance Analysis: [keyword]

### Current Metrics (Last 30 Days)
| Metric | Value | Status |
|--------|-------|--------|
| Position | [X] | [🟢/🟡/🔴] |
| Impressions | [X] | [🟢/🟡/🔴] |
| Clicks | [X] | - |
| CTR | [X%] | [🟢/🟡/🔴] |

### Quick Win Potential
- **Eligible?**: [Yes/No]
- **Estimated Gain**: [X additional clicks/month]

### Optimization Actions
1. [specific action]
2. [specific action]
```

### Quick Wins Report

```
## Quick Wins Report: [site]

### Summary
- **Opportunities Found**: [X]
- **Estimated Traffic Gain**: [X clicks/month]

### Top Opportunities
| Keyword | Position | Impressions | CTR | Action |
|---------|----------|-------------|-----|--------|
| [kw] | [pos] | [imp] | [ctr%] | [action] |

### Priority Actions
1. [highest impact]
2. [second priority]
```

---

## Reference Files

- [INTENT-GUIDE.md](INTENT-GUIDE.md) - Deep dive on intent classification
- [GSC-GUIDE.md](GSC-GUIDE.md) - GSC tool usage patterns
