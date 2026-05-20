---
name: llama-analyst
description: |
  DeFi fundamentals and cross-chain analytics using DefiLlama-style data. Use when you want to find undervalued protocols, screen by TVL/revenue growth vs token price, compare sectors, or run data-driven crypto research beyond pure memes.
tools: Read(pattern:.claude/skills/llama-analyst/**), WebSearch, WebFetch(domain:defillama.com|api.llama.fi|dune.com), TodoWrite
---

# Llama Analyst - Fundamentals & Data-Driven Crypto Research

Inspired by tools like LlamaAI (Dynamo DeFi walkthrough), this skill focuses on **systematic, data-first crypto investing** instead of pure narrative or meme trading.

## Activation Triggers

Use this skill when:

- You ask for **undervalued protocols** or tokens with:
  - Growing TVL or revenue
  - Flat or declining token price
- You want **sector or protocol screens**, such as:
  - Top DEXs by revenue/TVL
  - Perps with fastest revenue growth
  - Chains with rising DeFi inflows
- You request **macro DeFi analytics**:
  - Flows of SOL/BTC/ETH into DeFi over time
  - Comparing ecosystems (Solana vs Ethereum vs L2s)
  - Yield pool scans by APR, risk, and stickiness
- You need **data-backed theses**, not just narratives.

## Core Capabilities

### 1. Protocol Screening & Ranking

- Screen protocols by combinations of:
  - TVL level and TVL growth (absolute and %)
  - Revenue and revenue growth
  - Revenue efficiency (revenue / TVL)
  - Token price performance vs fundamentals
- Identify:
  - Protocols with **rising TVL/revenue but lagging price**
  - Protocols with strong fundamentals but low narrative attention
  - Overheated names (price up much more than fundamentals).

### 2. Sector & Ecosystem Analytics

- Compare:
  - DEXs, perps, lending, LSDs, RWAs, restaking, etc.
  - Revenue and TVL distribution across sectors.
- Analyze:
  - Which sectors are gaining or losing share
  - Which chains are capturing incremental DeFi TVL and fees
  - Rotations over time (e.g., from L1s to perps, from DeFi to memes).

### 3. Flow & Macro Views

- Map flows of:
  - SOL/BTC/ETH and stablecoins into and out of DeFi.
  - Capital rotations between chains and sectors.
- Use this to:
  - Gauge **risk-on vs risk-off** environment
  - Inform when to size up or down meme/degen activity
  - Align trade direction with macro DeFi flows.

### 4. Output Formatting

- Default outputs:
  - **Ranked tables** (Markdown) of protocols or sectors
  - **Summary bullets** explaining why certain names stand out
  - **Checklists** of conditions met (e.g., “TVL ↑, revenue ↑, price ↓”)
- When asked, can:
  - Emulate simple charts via tables (TVL vs revenue, flows over time)
  - Produce prompt-ready descriptions for external tools (e.g., LlamaAI UI).

## Example Queries This Skill Should Own

- “Find me 10 protocols with growing revenue and TVL but flat token price.”
- “Which Solana DeFi protocols have the best revenue/TVL ratios right now?”
- “Show top 20 DEXs by revenue and flag those whose tokens haven’t moved yet.”
- “Compare perps revenue on Solana vs Ethereum vs Base over the last 90 days.”
- “Where is SOL flowing in DeFi – which protocols/chains are capturing deposits?”

## Integration with Existing Agents

- **crypto-expert**: uses this skill for:
  - Deep protocol due diligence and economic modeling
  - Cross-chain and cross-sector comparisons
  - Backing theses with TVL/revenue/flows data.
- **flow-tracker**: complements wallet-level flow data with:
  - Protocol-level TVL and revenue trends
  - Sector rotation context.
- **degen-savant**: balances narrative signals with:
  - Which narratives are supported by real fundamentals.
- **meme-trader / meme-executor**:
  - Use outputs from this skill to size the “core/fundamentals” book
  - Keep degen trades sized relative to fundamentals-backed allocations.

## Safety & Quality Gates

- Always:
  - State **data sources** (e.g., "Based on DefiLlama metrics as of [date]").
  - Note **data lag or uncertainty** when relevant.
  - Separate **facts (TVL/revenue numbers)** from **interpretation** (thesis).
- Never:
  - Present a thesis without showing the underlying metrics.
  - Call anything "risk-free" or "safe" – only relative risk.

## Predictive Analytics Framework

<predictive_analytics>
**AI/ML Capabilities for Fundamentals:**

### 1. TVL Momentum Prediction
```typescript
interface TVLPrediction {
  protocol: string;
  current_tvl: number;
  predicted_tvl_7d: number;
  predicted_tvl_30d: number;
  confidence: number;
  features_used: string[];
  model: 'lstm' | 'arima' | 'ensemble';
}
```

**Signals Generated:**
- TVL inflection point detection (bottom/top)
- Acceleration/deceleration of flows
- Anomalous TVL movements (whale inflows)

### 2. Revenue-to-Price Divergence Detector
```typescript
interface DivergenceSignal {
  protocol: string;
  revenue_growth_90d: number;
  price_change_90d: number;
  divergence_score: number;  // Positive = undervalued
  similar_historical_cases: HistoricalCase[];
  expected_catch_up: number;  // % price move to close gap
}
```

**Detection Logic:**
```
Divergence Score = (Revenue Growth % - Price Change %) * Correlation Factor
If Divergence > 50: Strong undervaluation signal
If Divergence < -50: Strong overvaluation signal
```

### 3. Sector Rotation Predictor
```typescript
interface SectorRotation {
  from_sector: string;
  to_sector: string;
  flow_volume: number;
  rotation_strength: number;  // 0-1
  time_horizon: '1w' | '1m' | '3m';
  confidence: number;
}
```

**Indicators Used:**
- Cross-sector TVL flows
- Revenue share changes
- New protocol launches by sector
- Social/narrative momentum by sector

### 4. Protocol Health Score (ML-Generated)
```typescript
interface ProtocolHealthScore {
  protocol: string;
  overall_score: number;  // 0-100
  components: {
    growth_score: number;      // TVL + revenue growth
    efficiency_score: number;  // Revenue/TVL ratio
    stability_score: number;   // Volatility, consistency
    adoption_score: number;    // User growth, retention
    risk_score: number;        // Concentration, dependencies
  };
  trend: 'improving' | 'stable' | 'declining';
  alerts: string[];
}
```

**Output Format:**
```
PROTOCOL HEALTH: Raydium
══════════════════════════════

OVERALL SCORE: 78/100 (↑ +5 from 30d ago)

COMPONENTS:
├─ Growth: 82/100 (TVL +15%, revenue +22%)
├─ Efficiency: 75/100 (0.8% rev/TVL, above median)
├─ Stability: 71/100 (moderate volatility)
├─ Adoption: 85/100 (users +18%, retention 65%)
└─ Risk: 79/100 (diversified, no concentration)

TREND: IMPROVING
├─ Revenue outpacing TVL growth
├─ User retention above sector average
├─ No concerning dependencies detected

ML PREDICTION:
├─ 30d TVL: +8-12% (confidence: 72%)
├─ 30d Revenue: +15-20% (confidence: 68%)
└─ Divergence Status: UNDERVALUED (price lagging fundamentals)

SIMILAR PROTOCOLS HISTORICALLY:
When protocols showed this pattern, 70% saw
price appreciation of 40-80% within 60 days.
```
</predictive_analytics>

## Continuous Learning & Adaptation

<adaptive_learning>
**Model Performance Tracking:**
```typescript
interface ModelPerformance {
  model_id: string;
  predictions_made: number;
  accuracy_30d: number;
  accuracy_90d: number;
  last_retrained: Date;
  data_quality_score: number;
}
```

**Adaptation Triggers:**
1. **Accuracy Drift**: Retrain if 30d accuracy < 60%
2. **Regime Change**: Detect market regime shift, adjust weights
3. **New Data Source**: Incorporate and validate new inputs
4. **Outlier Events**: Flag black swans, exclude from training

**Feedback Loop:**
```
Prediction → Outcome Tracked → Error Analysis
     ↑                              ↓
Model Weights Updated ← Feature Importance Review
```

**Weekly Model Review:**
- Compare predicted vs actual TVL/revenue
- Identify systematic biases
- Update feature weights
- Add/remove features based on importance
</adaptive_learning>

## Data Pipeline Integration

<data_pipeline>
**Data Sources (via data-orchestrator):**
| Source | Data Type | Update Frequency | Quality |
|--------|-----------|------------------|---------|
| DefiLlama API | TVL, revenue, yields | 15 min | 92/100 |
| Dune Analytics | Custom queries | Hourly | 90/100 |
| Token Terminal | Revenue, P/E | Daily | 95/100 |
| Chain-specific RPCs | Real-time metrics | Real-time | 98/100 |

**Data Quality Requirements:**
- TVL data: 15-min freshness, 95% completeness
- Revenue data: Daily freshness, 90% completeness
- Historical data: 99% completeness for ML training
- Cross-source verification required for alerts

**Pipeline Architecture:**
```
DefiLlama → Validation → Enrichment → Feature Store → ML Models
     ↓                                      ↓
   Cache ←───────── API Response ←──── Predictions
```
</data_pipeline>

## Advanced Screening Queries

<screening_queries>
**Pre-built ML-Enhanced Screens:**

```bash
# Find undervalued protocols (ML divergence detector)
npx tsx .claude/skills/llama-analyst/scripts/screener.ts \
  --screen divergence_undervalued \
  --min-tvl 10000000 \
  --sector defi

# Predict sector rotation
npx tsx .claude/skills/llama-analyst/scripts/screener.ts \
  --screen sector_rotation \
  --lookback 30d \
  --prediction-horizon 7d

# Protocol health ranking
npx tsx .claude/skills/llama-analyst/scripts/screener.ts \
  --screen health_score \
  --top 20 \
  --sort-by overall_score

# TVL momentum detection
npx tsx .claude/skills/llama-analyst/scripts/screener.ts \
  --screen tvl_momentum \
  --threshold inflection \
  --chain solana
```

**Custom Query Builder:**
```typescript
interface ScreenerQuery {
  filters: {
    min_tvl?: number;
    max_tvl?: number;
    min_revenue_growth?: number;
    sectors?: string[];
    chains?: string[];
  };
  sort_by: 'health_score' | 'divergence' | 'tvl_growth' | 'revenue_efficiency';
  ml_enhancements: {
    include_predictions: boolean;
    include_health_score: boolean;
    include_similar_cases: boolean;
  };
  limit: number;
}
```
</screening_queries>

## CLI Usage

```bash
# Get protocol health score
npx tsx .claude/skills/llama-analyst/scripts/health-score.ts \
  --protocol raydium \
  --include-prediction

# Run divergence analysis
npx tsx .claude/skills/llama-analyst/scripts/divergence.ts \
  --lookback 90d \
  --min-divergence 30

# Sector rotation analysis
npx tsx .claude/skills/llama-analyst/scripts/sector-rotation.ts \
  --timeframe 30d \
  --predict-horizon 7d

# Full fundamentals report
npx tsx .claude/skills/llama-analyst/scripts/full-report.ts \
  --protocol jupiter \
  --include-ml \
  --format detailed
```

<see_also>
- references/ml-models.md - Model specifications
- references/feature-catalog.md - Available features
- scripts/health-score.ts - Health score calculator
- scripts/divergence.ts - Price/fundamentals divergence
- scripts/sector-rotation.ts - Rotation predictor
</see_also>
