---
name: monetization-analyzer
description: Analyze game concepts for monetization potential, willingness-to-pay, viral mechanics, and revenue generation. Ranks concepts by total monetization score and identifies top revenue opportunities.
---

# Monetization Analyzer Skill

## Purpose

This skill evaluates game concepts to identify the most monetizable opportunities based on:
- **Willingness-to-Pay (WTP)** analysis from market data
- **Viral potential** and organic growth mechanics
- **Revenue model optimization** (premium, F2P, subscription, hybrid)
- **Market demand** and addressable market size
- **Competitive pricing** positioning
- **Lifetime Value (LTV)** projections

**Output**: Ranked list of top 3 most monetizable game concepts with detailed financial projections and go-to-market recommendations.

## When to Use This Skill

Use this skill when you have:
- ✅ Multiple game concepts to evaluate for investment prioritization
- ✅ Market analysis data showing pricing sentiment and willingness-to-pay signals
- ✅ Need to identify which concepts have highest revenue potential
- ✅ Want to optimize monetization models before development
- ✅ Require financial projections for pitch decks or funding proposals
- ✅ Need to validate business model assumptions with market data

## Prerequisites

### Required Input Files

1. **Market Analysis Report** (from `market-analyst` skill)
   - Location: `/docs/market-analysis-*.md`
   - Must include: Sentiment data on pricing, monetization pain points, willingness-to-pay signals
   - Example: `market-analysis-fps-games-2025-10-26.md`

2. **Game Concepts Document** (from brainstorming/design)
   - Location: `/docs/*-game-concepts-*.md` or `/docs/plans/*-design.md`
   - Must include: Price points, target personas, distribution channels, competitors
   - Example: `fps-game-concepts-market-driven-2025-10-26.md`

### Optional Input Files

3. **Competitor Financial Data** (if available)
   - Revenue reports, player counts, ARPU data
   - Enhances accuracy of projections

## Core Workflow

### Phase 1: Data Extraction and Normalization

**1. Load Market Analysis**

Extract willingness-to-pay signals:

```javascript
WTP_Signals = {
  price_sentiment: {
    "$0 (F2P)": {positive: X%, negative: Y%, mentions: N},
    "$10-20": {positive: X%, negative: Y%, mentions: N},
    "$20-30": {positive: X%, negative: Y%, mentions: N},
    "$60-70": {positive: X%, negative: Y%, mentions: N},
    "$70 + MTX": {positive: X%, negative: Y%, mentions: N}
  },
  monetization_pain_points: [
    {issue: "Premium + battle pass", severity: "CRITICAL", mentions: N},
    {issue: "Loot boxes", severity: "HIGH", mentions: N}
  ],
  value_propositions: [
    {model: "F2P cosmetic-only", sentiment: X%, examples: []},
    {model: "Budget indie ($15-25)", sentiment: X%, examples: []}
  ]
}
```

**2. Load Game Concepts**

Extract monetization-relevant data for each concept:

```javascript
GameConcept = {
  name: string,
  price_point: number | "F2P",
  monetization_model: string,
  target_audience: {
    primary_persona: {},
    market_size_estimate: number,
    spending_behavior: string
  },
  competitors: [{name, price, model, performance}],
  distribution_channels: [{platform, percentage, rationale}],
  lifecycle_commitment: string,
  development_cost_estimate: number
}
```

### Phase 2: Willingness-to-Pay Analysis

**3. Calculate WTP Score (0-100)**

```javascript
function calculateWTP(concept, marketData) {
  const score = {
    price_sentiment_alignment: 0,    // Does price match positive sentiment tier?
    value_perception: 0,              // Content/$ ratio vs. market expectations
    monetization_model_fit: 0,        // Model aligns with audience preferences?
    competitive_positioning: 0,       // Price competitive advantage?
    pain_point_avoidance: 0          // Avoids monetization red flags?
  };

  // Price Sentiment Alignment (0-30 points)
  const priceТier = getPriceTier(concept.price_point);
  const sentiment = marketData.price_sentiment[priceTier];
  score.price_sentiment_alignment = (sentiment.positive / 100) * 30;

  // Value Perception (0-25 points)
  const contentHours = estimateContentHours(concept);
  const pricePerHour = concept.price_point / contentHours;
  const marketAvgPricePerHour = calculateMarketAverage();

  if (pricePerHour < marketAvgPricePerHour * 0.8) {
    score.value_perception = 25; // Excellent value
  } else if (pricePerHour < marketAvgPricePerHour) {
    score.value_perception = 18; // Good value
  } else if (pricePerHour < marketAvgPricePerHour * 1.2) {
    score.value_perception = 10; // Fair value
  } else {
    score.value_perception = 0; // Poor value
  }

  // Monetization Model Fit (0-20 points)
  const modelSentiment = marketData.value_propositions.find(
    vp => vp.model === concept.monetization_model
  );
  score.monetization_model_fit = (modelSentiment.sentiment / 100) * 20;

  // Competitive Positioning (0-15 points)
  const competitorPrices = concept.competitors.map(c => c.price);
  const avgCompetitorPrice = average(competitorPrices);

  if (concept.price_point < avgCompetitorPrice * 0.7) {
    score.competitive_positioning = 15; // Undercut leaders
  } else if (concept.price_point < avgCompetitorPrice) {
    score.competitive_positioning = 10; // Competitive pricing
  } else {
    score.competitive_positioning = 5; // Premium positioning
  }

  // Pain Point Avoidance (0-10 points)
  const painPoints = marketData.monetization_pain_points;
  let violations = 0;

  painPoints.forEach(pp => {
    if (conceptViolatesPainPoint(concept, pp)) {
      violations += (pp.severity === "CRITICAL") ? 5 : 2;
    }
  });

  score.pain_point_avoidance = Math.max(0, 10 - violations);

  return {
    total: Object.values(score).reduce((a, b) => a + b, 0),
    breakdown: score,
    confidence: calculateConfidence(marketData.sample_size)
  };
}
```

**WTP Score Interpretation:**
- **90-100**: Exceptional WTP, price optimization perfect
- **75-89**: Strong WTP, minor adjustments possible
- **60-74**: Moderate WTP, consider price/model changes
- **Below 60**: Weak WTP, major repositioning needed

### Phase 3: Viral Potential Analysis

**4. Calculate Viral Score (0-100)**

```javascript
function calculateViralPotential(concept, marketData) {
  const score = {
    shareability: 0,           // Content naturally creates shareable moments?
    accessibility: 0,          // Low barrier to entry?
    network_effects: 0,        // Benefits from friend invites?
    streamer_appeal: 0,        // Twitch/YouTube friendly?
    novelty_factor: 0,         // Unique enough to generate buzz?
    social_features: 0         // Built for social play/sharing?
  };

  // Shareability (0-20 points)
  const shareableGenres = ["party game", "asymmetric", "sports hybrid", "roguelike"];
  if (shareableGenres.some(g => concept.genre.includes(g))) {
    score.shareability = 20;
  } else if (concept.genre.includes("competitive") || concept.genre.includes("co-op")) {
    score.shareability = 12;
  } else {
    score.shareability = 5; // Single-player, narrative
  }

  // Accessibility (0-20 points)
  if (concept.price_point === "F2P") {
    score.accessibility = 20; // Zero barrier
  } else if (concept.price_point <= 15) {
    score.accessibility = 15; // Impulse purchase
  } else if (concept.price_point <= 25) {
    score.accessibility = 10; // Reasonable
  } else {
    score.accessibility = 5; // Higher barrier
  }

  // Network Effects (0-20 points)
  if (concept.monetization_model.includes("F2P") || concept.monetization_model.includes("viral")) {
    score.network_effects = 20;
  } else if (concept.description.includes("co-op") || concept.description.includes("multiplayer")) {
    score.network_effects = 12;
  } else {
    score.network_effects = 0;
  }

  // Streamer Appeal (0-15 points)
  const streamerFriendly = [
    concept.genre.includes("asymmetric"),
    concept.genre.includes("roguelike"),
    concept.genre.includes("party"),
    concept.description.includes("viral moments"),
    concept.description.includes("spectator")
  ];
  score.streamer_appeal = streamerFriendly.filter(Boolean).length * 3;

  // Novelty Factor (0-15 points)
  const noveltyIndicators = marketData.novelty_successes || [];
  if (noveltyIndicators.some(n => concept.description.includes(n.innovation))) {
    score.novelty_factor = 15;
  } else if (concept.description.includes("unique") || concept.description.includes("first")) {
    score.novelty_factor = 10;
  } else {
    score.novelty_factor = 5;
  }

  // Social Features (0-10 points)
  const socialKeywords = ["co-op", "multiplayer", "friend", "clan", "team", "squad"];
  const socialCount = socialKeywords.filter(kw =>
    concept.description.toLowerCase().includes(kw)
  ).length;
  score.social_features = Math.min(10, socialCount * 2);

  return {
    total: Object.values(score).reduce((a, b) => a + b, 0),
    breakdown: score,
    viral_coefficient: estimateViralCoefficient(score.total)
  };
}

function estimateViralCoefficient(viralScore) {
  // Viral coefficient: How many new users does each user bring?
  // K > 1 = exponential growth, K < 1 = paid acquisition needed
  if (viralScore >= 85) return 1.5;      // Exceptional viral growth
  if (viralScore >= 70) return 1.2;      // Strong organic growth
  if (viralScore >= 55) return 0.8;      // Some viral mechanics
  if (viralScore >= 40) return 0.4;      // Minimal viral spread
  return 0.2;                             // Requires paid marketing
}
```

**Viral Score Interpretation:**
- **85-100**: Viral hit potential (K > 1.2), minimal marketing spend
- **70-84**: Strong organic growth (K ~1.0), word-of-mouth driven
- **55-69**: Moderate virality (K ~0.8), some paid marketing needed
- **40-54**: Low virality (K ~0.4), heavy marketing investment required
- **Below 40**: No viral mechanics (K ~0.2), paid acquisition only

### Phase 4: Revenue Projection Modeling

**5. Calculate Revenue Potential (Year 1-3 Projections)**

```javascript
function projectRevenue(concept, wtpScore, viralScore, marketData) {
  const model = concept.monetization_model;

  // Addressable Market Size
  const TAM = estimateTotalAddressableMarket(concept, marketData);
  const SAM = TAM * 0.15; // Serviceable addressable (15% of TAM realistic)
  const SOM = SAM * getMarketShareEstimate(viralScore, concept.competitors.length);

  // Player Acquisition Model
  const year1Players = calculateYear1Players(concept, viralScore, SOM);
  const year2Players = year1Players * getRetentionMultiplier(concept.lifecycle_commitment);
  const year3Players = year2Players * getGrowthMultiplier(viralScore);

  // Revenue Calculations
  if (model.includes("F2P")) {
    return projectF2PRevenue(year1Players, year2Players, year3Players, concept);
  } else if (model.includes("premium") || typeof concept.price_point === "number") {
    return projectPremiumRevenue(year1Players, year2Players, year3Players, concept);
  } else {
    return projectHybridRevenue(year1Players, year2Players, year3Players, concept);
  }
}

function projectF2PRevenue(y1Players, y2Players, y3Players, concept) {
  // F2P Model: Base * Conversion Rate * ARPPU
  const conversionRate = 0.03; // Industry avg: 3-5% pay
  const ARPPU = estimateARPPU(concept); // Average revenue per paying user

  const y1Revenue = y1Players * conversionRate * ARPPU;
  const y2Revenue = y2Players * (conversionRate * 1.1) * (ARPPU * 1.15); // Improve over time
  const y3Revenue = y3Players * (conversionRate * 1.15) * (ARPPU * 1.25);

  return {
    year1: {players: y1Players, revenue: y1Revenue, ARPU: y1Revenue / y1Players},
    year2: {players: y2Players, revenue: y2Revenue, ARPU: y2Revenue / y2Players},
    year3: {players: y3Players, revenue: y3Revenue, ARPU: y3Revenue / y3Players},
    total_3yr: y1Revenue + y2Revenue + y3Revenue,
    LTV: (y1Revenue + y2Revenue + y3Revenue) / y1Players
  };
}

function projectPremiumRevenue(y1Players, y2Players, y3Players, concept) {
  // Premium Model: Units Sold * Price + Optional DLC
  const basePrice = concept.price_point;
  const dlcAttachRate = 0.25; // 25% buy DLC
  const avgDLCSpend = basePrice * 0.6; // DLC ~60% of base price

  const y1Revenue = (y1Players * basePrice) + (y1Players * dlcAttachRate * avgDLCSpend * 0.5);
  const y2Revenue = (y2Players * 0.3 * basePrice) + (y2Players * 0.3 * dlcAttachRate * avgDLCSpend);
  const y3Revenue = (y3Players * 0.1 * basePrice) + (y3Players * 0.1 * dlcAttachRate * avgDLCSpend);

  return {
    year1: {players: y1Players, revenue: y1Revenue, ARPU: basePrice},
    year2: {players: y2Players * 0.3, revenue: y2Revenue, ARPU: basePrice},
    year3: {players: y3Players * 0.1, revenue: y3Revenue, ARPU: basePrice},
    total_3yr: y1Revenue + y2Revenue + y3Revenue,
    LTV: basePrice + (dlcAttachRate * avgDLCSpend)
  };
}

function estimateARPPU(concept) {
  // Average Revenue Per Paying User (F2P)
  if (concept.genre.includes("competitive")) return 45; // Esports skin buyers spend more
  if (concept.genre.includes("party")) return 20; // Casual spenders
  if (concept.genre.includes("co-op")) return 30; // Mid-tier
  return 25; // Default
}

function estimateTotalAddressableMarket(concept, marketData) {
  // Use market analysis data + platform data
  const steamActivePlayers = 120000000; // ~120M monthly active on Steam
  const genreMultiplier = getGenreMarketShare(concept.genre);
  return steamActivePlayers * genreMultiplier;
}

function getMarketShareEstimate(viralScore, competitorCount) {
  // Viral potential + competitive landscape determines realistic share
  let baseShare = 0.01; // 1% of SAM baseline

  if (viralScore >= 85) baseShare *= 3;      // Viral hit
  else if (viralScore >= 70) baseShare *= 2; // Strong growth
  else if (viralScore >= 55) baseShare *= 1.5;

  // Competitive penalty
  if (competitorCount > 5) baseShare *= 0.7;
  else if (competitorCount > 3) baseShare *= 0.85;

  return baseShare;
}
```

**6. Calculate Development ROI**

```javascript
function calculateROI(concept, revenueProjection) {
  const devCost = concept.development_cost_estimate || estimateDevCost(concept);
  const marketingCost = estimateMarketingCost(concept, revenueProjection.year1.players);
  const totalInvestment = devCost + marketingCost;

  const grossRevenue = revenueProjection.total_3yr;
  const platformFees = grossRevenue * 0.30; // Steam/console take 30%
  const netRevenue = grossRevenue - platformFees;
  const netProfit = netRevenue - totalInvestment;

  return {
    investment: totalInvestment,
    gross_revenue: grossRevenue,
    net_revenue: netRevenue,
    net_profit: netProfit,
    ROI_percentage: (netProfit / totalInvestment) * 100,
    payback_period_months: calculatePaybackPeriod(totalInvestment, revenueProjection),
    break_even_units: totalInvestment / (concept.price_point || 25)
  };
}

function estimateDevCost(concept) {
  // Based on scope, team size, timeline
  if (concept.description.includes("solo") || concept.description.includes("small team")) {
    return 150000; // $150K
  } else if (concept.description.includes("128-player") || concept.description.includes("large-scale")) {
    return 8000000; // $8M
  } else {
    return 1200000; // $1.2M (AA indie default)
  }
}

function estimateMarketingCost(concept, year1Players) {
  // Cost per acquisition based on viral coefficient
  const viralCoef = concept.viral_coefficient || 0.5;

  if (viralCoef >= 1.2) {
    // Viral growth, minimal paid marketing
    return year1Players * 0.50; // $0.50 CPA (mostly organic)
  } else if (viralCoef >= 0.8) {
    return year1Players * 2; // $2 CPA
  } else {
    return year1Players * 5; // $5 CPA (heavy paid)
  }
}
```

### Phase 5: Monetization Optimization Recommendations

**7. Analyze Monetization Model Fit**

```javascript
function analyzeMonetizationModel(concept, wtpScore, viralScore, marketData) {
  const currentModel = concept.monetization_model;
  const alternativeModels = [];

  // Test F2P vs. Premium
  if (currentModel.includes("premium") && viralScore >= 70) {
    alternativeModels.push({
      model: "F2P with cosmetic monetization",
      rationale: `High viral score (${viralScore}) suggests F2P could 5-10x player base`,
      projected_revenue_delta: "+40-80%",
      risk: "ARPPU uncertainty, requires cosmetic art pipeline"
    });
  }

  // Test pricing tiers
  if (typeof concept.price_point === "number") {
    const sentiment = marketData.price_sentiment;
    const currentTier = getPriceTier(concept.price_point);

    Object.keys(sentiment).forEach(tier => {
      if (tier !== currentTier && sentiment[tier].positive > sentiment[currentTier].positive + 10) {
        alternativeModels.push({
          model: `Price adjustment to ${tier}`,
          rationale: `${tier} has ${sentiment[tier].positive}% positive vs. current ${sentiment[currentTier].positive}%`,
          projected_revenue_delta: estimatePriceChangeDelta(concept, tier),
          risk: "Value perception vs. content ratio"
        });
      }
    });
  }

  // Test monetization add-ons
  if (!currentModel.includes("DLC") && concept.lifecycle_commitment.includes("2-3 year")) {
    alternativeModels.push({
      model: "Add expansion DLC model",
      rationale: "Long lifecycle supports premium content drops",
      projected_revenue_delta: "+15-25%",
      risk: "Community expectations for free updates"
    });
  }

  return {
    current_model: currentModel,
    current_model_score: scoreMonetizationModel(currentModel, wtpScore, viralScore),
    alternatives: alternativeModels.sort((a, b) =>
      parseFloat(b.projected_revenue_delta) - parseFloat(a.projected_revenue_delta)
    )
  };
}
```

### Phase 6: Composite Monetization Score & Ranking

**8. Calculate Total Monetization Score (0-100)**

```javascript
function calculateMonetizationScore(concept, wtpScore, viralScore, revenueProjection, roi) {
  const score = {
    willingness_to_pay: wtpScore.total * 0.25,          // 25% weight
    viral_potential: viralScore.total * 0.20,           // 20% weight
    revenue_potential: normalizeRevenue(revenueProjection.total_3yr) * 0.30, // 30% weight
    roi_efficiency: normalizeROI(roi.ROI_percentage) * 0.15,  // 15% weight
    time_to_profit: normalizePaybackPeriod(roi.payback_period_months) * 0.10 // 10% weight
  };

  return {
    total: Object.values(score).reduce((a, b) => a + b, 0),
    breakdown: score,
    tier: getMonetizationTier(Object.values(score).reduce((a, b) => a + b, 0))
  };
}

function normalizeRevenue(revenue) {
  // Normalize to 0-100 scale (assuming $50M = 100)
  return Math.min(100, (revenue / 50000000) * 100);
}

function normalizeROI(roiPercentage) {
  // Normalize to 0-100 scale (500% ROI = 100)
  return Math.min(100, (roiPercentage / 500) * 100);
}

function normalizePaybackPeriod(months) {
  // Shorter = better (6 months = 100, 36 months = 0)
  return Math.max(0, 100 - ((months - 6) / 30) * 100);
}

function getMonetizationTier(score) {
  if (score >= 90) return "S-TIER: Blockbuster potential";
  if (score >= 80) return "A-TIER: Strong monetization";
  if (score >= 70) return "B-TIER: Solid revenue opportunity";
  if (score >= 60) return "C-TIER: Moderate monetization";
  return "D-TIER: Weak monetization";
}
```

**9. Rank and Select Top 3**

```javascript
function rankConcepts(concepts, scores) {
  const ranked = concepts.map((concept, i) => ({
    concept: concept,
    scores: scores[i],
    monetization_score: scores[i].total,
    recommendation: generateRecommendation(concept, scores[i])
  })).sort((a, b) => b.monetization_score - a.monetization_score);

  return {
    top3: ranked.slice(0, 3),
    all_ranked: ranked,
    summary: generateRankingSummary(ranked)
  };
}

function generateRecommendation(concept, scores) {
  const strengths = [];
  const weaknesses = [];
  const actions = [];

  // Analyze strengths
  if (scores.breakdown.willingness_to_pay >= 20) strengths.push("Strong price/value fit");
  if (scores.breakdown.viral_potential >= 16) strengths.push("High organic growth potential");
  if (scores.breakdown.revenue_potential >= 24) strengths.push("Large revenue opportunity");

  // Analyze weaknesses
  if (scores.breakdown.willingness_to_pay < 15) weaknesses.push("Price optimization needed");
  if (scores.breakdown.viral_potential < 12) weaknesses.push("Lacks viral mechanics");
  if (scores.breakdown.roi_efficiency < 10) weaknesses.push("Long payback period");

  // Generate actions
  if (weaknesses.includes("Price optimization needed")) {
    actions.push("Test alternative price points ($X-Y range)");
  }
  if (weaknesses.includes("Lacks viral mechanics")) {
    actions.push("Add social features (friend invites, sharing, spectator mode)");
  }
  if (scores.breakdown.revenue_potential < 20) {
    actions.push("Expand addressable market (additional platforms, regions)");
  }

  return {strengths, weaknesses, priority_actions: actions};
}
```

## Output Format

### Monetization Analysis Report Structure

```markdown
# Monetization Analysis Report: [Game Category]

**Analysis Date**: [Date]
**Market Analysis Source**: [Filename]
**Game Concepts Analyzed**: [Number]
**Top 3 Selected By**: Total Monetization Score (WTP + Viral + Revenue + ROI + Time-to-Profit)

---

## Executive Summary

[2-3 paragraphs summarizing key findings, top picks, revenue potential]

---

## Top 3 Most Monetizable Games

### 🥇 #1: [Game Name] - Monetization Score: XX/100

**Monetization Tier**: [S/A/B/C/D-TIER]

#### Score Breakdown
| Component | Score | Weight | Contribution |
|-----------|-------|--------|--------------|
| Willingness-to-Pay | XX/100 | 25% | XX.X |
| Viral Potential | XX/100 | 20% | XX.X |
| Revenue Potential | XX/100 | 30% | XX.X |
| ROI Efficiency | XX/100 | 15% | XX.X |
| Time-to-Profit | XX/100 | 10% | XX.X |
| **TOTAL** | **XX/100** | **100%** | **XX.X** |

#### Willingness-to-Pay Analysis (XX/100)
- **Price Point**: $XX or F2P
- **Market Sentiment**: XX% positive for this price tier
- **Value Perception**: $X.XX per hour (market avg: $X.XX) - [Excellent/Good/Fair/Poor]
- **Monetization Model**: [Model name]
- **Model Sentiment**: XX% positive (proven by [examples])
- **Pain Points Avoided**: ✅ No premium+MTX ✅ No loot boxes ✅ [etc]
- **Competitive Pricing**: [XX% below/above] competitor average ($XX)

**Confidence**: [HIGH/MEDIUM/LOW] based on [sample size] data points

#### Viral Potential Analysis (XX/100)
- **Viral Coefficient**: X.X (players per player)
- **Growth Type**: [Exponential/Organic/Paid-driven]
- **Shareability**: XX/20 - [Why shareable]
- **Accessibility**: XX/20 - [Barrier to entry]
- **Network Effects**: XX/20 - [Friend invite mechanics]
- **Streamer Appeal**: XX/15 - [Twitch/YouTube potential]
- **Novelty Factor**: XX/15 - [Unique hook]
- **Social Features**: XX/10 - [Co-op/multiplayer/clans]

**Viral Mechanisms**:
- [Mechanism 1]: [How it drives viral spread]
- [Mechanism 2]: [How it drives viral spread]

#### Revenue Projections (3-Year)

**Player Acquisition**:
- Year 1: XXX,XXX players ([organic/paid mix])
- Year 2: XXX,XXX players ([retention rate]%)
- Year 3: XXX,XXX players ([growth trajectory])

**Revenue Model**: [Premium/F2P/Hybrid]
- Year 1: $X.XM revenue, $XX ARPU, XXX,XXX paying users
- Year 2: $X.XM revenue, $XX ARPU, XXX,XXX paying users
- Year 3: $X.XM revenue, $XX ARPU, XXX,XXX paying users
- **Total 3-Year**: $XX.XM gross revenue

**Lifetime Value (LTV)**: $XX per player

#### Financial Projections

**Investment Required**:
- Development: $X.XM ([team size, timeline])
- Marketing: $X.XM (CPA: $X.XX based on viral coef X.X)
- **Total Investment**: $X.XM

**Returns**:
- Gross Revenue (3yr): $XX.XM
- Platform Fees (30%): -$X.XM
- Net Revenue: $XX.XM
- Net Profit: $XX.XM
- **ROI**: XXX% over 3 years
- **Payback Period**: XX months
- **Break-Even Units**: XX,XXX copies/players

#### Monetization Model Analysis

**Current Model**: [Model description]
- **Model Score**: XX/100
- **Strengths**: [Why this model works]
- **Market Validation**: [Examples of successful similar models]

**Alternative Models Considered**:
1. **[Alternative Model]**
   - Projected Revenue Delta: +XX%
   - Rationale: [Why it could work better]
   - Risk: [Implementation challenges]

2. **[Alternative Model 2]**
   - Projected Revenue Delta: +XX%
   - Rationale: [Why it could work better]
   - Risk: [Implementation challenges]

**Recommendation**: [Stick with current / Switch to alternative X]

#### Market Demand Validation

**Addressable Market**:
- TAM (Total): XX million players ([genre] on [platforms])
- SAM (Serviceable): X.X million players (15% of TAM)
- SOM (Obtainable): XXX,XXX players (X.X% market share realistic)

**Demand Signals**:
- Market gap priority score: XX/100
- Explicit demand mentions: XXX+ in market analysis
- Competitor performance: [Leader doing $XXM ARR]
- Growth trajectory: [Growing/Stable/Declining] market

#### Strengths
1. ✅ [Strength 1 - from analysis]
2. ✅ [Strength 2 - from analysis]
3. ✅ [Strength 3 - from analysis]

#### Weaknesses
1. ⚠️ [Weakness 1 - from analysis]
2. ⚠️ [Weakness 2 - from analysis]

#### Priority Actions
1. 🎯 [Action 1 to improve monetization]
2. 🎯 [Action 2 to improve monetization]
3. 🎯 [Action 3 to improve monetization]

#### Go-to-Market Recommendation

**Launch Strategy**:
- **Platform Priority**: [Steam/Console/Multi] first
- **Pricing Strategy**: [Launch price, discount strategy]
- **Marketing Budget**: $X.XM ([CPA strategy])
- **Timeline**: [Optimal launch window based on competition]

**First 90 Days**:
- Week 1-2: [Activities]
- Month 1: [Milestones]
- Month 2-3: [Retention focus]

**Success Metrics**:
- Week 1: XXK units sold / downloads
- Month 1: XX% D30 retention
- Month 3: $XXK MRR / ARR run-rate
- Year 1: $X.XM revenue target

---

### 🥈 #2: [Game Name] - Monetization Score: XX/100

[Same detailed structure as #1]

---

### 🥉 #3: [Game Name] - Monetization Score: XX/100

[Same detailed structure as #1]

---

## Comparative Analysis: Top 3

### Quick Comparison Table

| Metric | #1: [Name] | #2: [Name] | #3: [Name] |
|--------|------------|------------|------------|
| **Monetization Score** | XX/100 | XX/100 | XX/100 |
| **WTP Score** | XX/100 | XX/100 | XX/100 |
| **Viral Score** | XX/100 | XX/100 | XX/100 |
| **3-Year Revenue** | $XXM | $XXM | $XXM |
| **ROI %** | XXX% | XXX% | XXX% |
| **Payback Period** | XX mo | XX mo | XX mo |
| **Investment Required** | $X.XM | $X.XM | $X.XM |
| **Year 1 Players** | XXXk | XXXk | XXXk |
| **Risk Level** | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |

### Portfolio Recommendation

**If investing in ONE game**: [#1/2/3] because [rationale]

**If investing in TWO games**: [#1 + #2/3] because [portfolio diversification rationale]

**If investing in ALL THREE**: [Portfolio strategy - risk balance, market coverage]

---

## All Concepts Ranked

| Rank | Game Name | Score | Tier | Revenue (3yr) | ROI | Why it ranked here |
|------|-----------|-------|------|---------------|-----|-------------------|
| 1 | [Name] | XX | S | $XXM | XXX% | [1-sentence reason] |
| 2 | [Name] | XX | A | $XXM | XXX% | [1-sentence reason] |
| 3 | [Name] | XX | A | $XXM | XXX% | [1-sentence reason] |
| 4 | [Name] | XX | B | $XXM | XXX% | [1-sentence reason] |
| 5 | [Name] | XX | B | $XXM | XXX% | [1-sentence reason] |
...

---

## Market Insights

### Willingness-to-Pay Patterns

**Price Tiers by Sentiment**:
1. ✅ **$15-25 (XX% positive)**: Sweet spot for indie/value games
2. ✅ **F2P (XX% positive)**: Works if cosmetic-only, fails if P2W
3. ⚠️ **$60-70 (XX% negative)**: Premium acceptable ONLY if no added MTX
4. ❌ **$70 + MTX (XX% negative)**: Market rejection, avoid entirely

**Monetization Models Ranked**:
1. F2P cosmetic-only (XX% positive) - Examples: CS2, [others]
2. Budget premium $15-25 (XX% positive) - Examples: Duckov, [others]
3. Premium $30-40 + expansions (XX% positive) - Examples: [Classic games]
4. Premium $60-70 clean (XX% positive / XX% negative) - Mixed
5. Premium + battle pass (XX% negative) - **AVOID**

### Viral Mechanisms That Work

**High Viral Coefficient (K > 1.0)**:
- F2P with friend invite rewards
- Asymmetric gameplay (streamers love)
- Party games with spectator mode
- Co-op with friend-only benefits

**Moderate Viral Coefficient (K ~0.8)**:
- Competitive with clan systems
- Roguelikes with meta-progression sharing
- Co-op PvE with progression

**Low Viral Coefficient (K < 0.5)**:
- Single-player narrative
- Premium with no social features
- Hardcore difficulty (small audience)

---

## Recommendations by Investment Scenario

### Scenario 1: Limited Budget ($500K-$1M)

**Best Pick**: [Game X]
- Why: Highest ROI (XXX%), fastest payback (XX months)
- Risk: [Low/Medium] - proven model
- Expected Return: $X.XM net profit

**Alternative**: [Game Y]
- Why: Lower risk, proven audience
- Expected Return: $X.XM net profit

### Scenario 2: Medium Budget ($2M-$5M)

**Best Pick**: [Game X]
- Why: Balance of revenue potential ($XXM) and viral growth
- Portfolio approach: [Game X] + [Game Y] for diversification

### Scenario 3: Large Budget ($10M+)

**Best Pick**: [Game X]
- Why: Blockbuster potential, large TAM
- Competitive moat: [Unique advantages]
- Market timing: [Why now is optimal]

---

## Risk Assessment

### Top 3 Monetization Risks

1. **[Risk 1]**: [Description]
   - Affects: [Which games]
   - Mitigation: [Strategy]
   - Probability: [Low/Med/High]

2. **[Risk 2]**: [Description]
   - Affects: [Which games]
   - Mitigation: [Strategy]
   - Probability: [Low/Med/High]

3. **[Risk 3]**: [Description]
   - Affects: [Which games]
   - Mitigation: [Strategy]
   - Probability: [Low/Med/High]

---

## Appendix: Methodology

### Data Sources
- Market Analysis: [Filename, data points, date]
- Game Concepts: [Filename, concepts count]
- Competitor Data: [Sources]

### Scoring Formulas
- WTP Score: [Components and weights]
- Viral Score: [Components and weights]
- Monetization Score: [Composite formula]

### Assumptions
- Platform fees: 30% (Steam/console standard)
- F2P conversion rate: 3-5%
- F2P ARPPU: $20-45 depending on genre
- Viral coefficient estimates based on genre/model
- TAM estimates based on [Steam/platform data]

### Confidence Levels
- HIGH: 100+ sentiment data points, direct competitor comp data
- MEDIUM: 50-99 data points, some comp data
- LOW: <50 data points, limited comp data

---

**Report Generated By**: Monetization Analyzer Skill v1.0
**Analysis Date**: [Date]
**Input Files**: [List]
**Concepts Evaluated**: [Number]
**Top 3 Selected**: [Names]
```

## Implementation Protocol

### Step 1: Create Analysis Plan

```javascript
TodoWrite([
  "Load market analysis report and extract WTP signals",
  "Load game concepts document and extract monetization data",
  "Calculate WTP score for each game concept",
  "Calculate viral potential score for each concept",
  "Project 3-year revenue for each concept",
  "Calculate ROI and financial metrics",
  "Compute total monetization score",
  "Rank all concepts by monetization score",
  "Select top 3 and generate detailed analysis",
  "Create optimization recommendations for top 3",
  "Generate comprehensive monetization report"
])
```

### Step 2: Data Loading (Parallel)

```javascript
[Single Message - Load All Inputs]:
  Read("/docs/market-analysis-[category]-[date].md")
  Read("/docs/[category]-game-concepts-[date].md")
  // Optional: Read competitor data if available
```

### Step 3: Scoring (Sequential for each concept)

For each game concept:
1. Calculate WTP score (0-100)
2. Calculate viral score (0-100)
3. Project revenue (3-year model)
4. Calculate ROI metrics
5. Compute composite monetization score

### Step 4: Ranking and Selection

1. Sort concepts by total monetization score (descending)
2. Select top 3
3. Generate detailed analysis for top 3
4. Create comparative analysis
5. Develop recommendations

### Step 5: Report Generation

Save comprehensive report to:
`/docs/monetization-analysis-[category]-top3-[date].md`

## Best Practices

### DO:
✅ Use actual market data for WTP signals (not assumptions)
✅ Consider viral coefficient in player acquisition costs
✅ Model both optimistic and conservative scenarios
✅ Validate assumptions against competitor performance
✅ Account for platform fees (30%) in revenue calculations
✅ Consider payback period for investment decisions
✅ Test alternative monetization models

### DON'T:
❌ Ignore market sentiment on pricing
❌ Assume high prices = high revenue (volume matters)
❌ Underestimate marketing costs for low-viral games
❌ Overestimate viral growth without evidence
❌ Mix incompatible monetization models (premium + aggressive MTX)
❌ Ignore competitive pricing dynamics
❌ Project beyond 3 years (too uncertain)

## Integration with Other Skills

This skill works with:
- **market-analyst**: Primary data source for WTP and demand
- **reddit-sentiment-analysis**: Raw sentiment on pricing/monetization
- **competitive-analysis**: Competitor revenue benchmarking
- **product-roadmap**: Feature prioritization by revenue impact

## Summary

The Monetization Analyzer Skill transforms market data and game concepts into financial intelligence by:

1. ✅ **Quantifying willingness-to-pay** from market sentiment
2. ✅ **Scoring viral potential** based on game mechanics
3. ✅ **Projecting 3-year revenue** with realistic models
4. ✅ **Calculating ROI** and payback periods
5. ✅ **Ranking concepts** by composite monetization score
6. ✅ **Selecting top 3** most monetizable opportunities
7. ✅ **Generating recommendations** for optimization

Output enables data-driven decisions for:
- Investment prioritization
- Pricing optimization
- Monetization model selection
- Go-to-market strategy
- Revenue forecasting
- Pitch deck financial projections
