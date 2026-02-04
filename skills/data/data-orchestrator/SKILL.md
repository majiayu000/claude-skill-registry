---
name: data-orchestrator
description: |
  Central data strategy coordinator for AI-driven crypto trading. Use when building data pipelines, validating data quality, coordinating multi-source data aggregation, or implementing ML-ready data infrastructure. Covers: data governance, quality validation, source management, real-time pipelines, backtesting infrastructure.
tools: Read(pattern:.claude/skills/data-orchestrator/**), WebSearch, WebFetch(domain:api.llama.fi|dexscreener.com|birdeye.so|coingecko.com|coinapi.io), mcp__perplexity-ask__search, mcp__perplexity-ask__reason, TodoWrite
---

# Data Orchestrator - AI Trading Data Strategy Layer

Central nervous system for all data operations across the meme-times ecosystem. Implements a robust, AI-ready data strategy that precedes and enables all trading decisions.

## Core Principle

> Data strategy comes BEFORE AI. Clean governance, validated sources, and secure infrastructure enable useful trading insights.

## Activation Triggers

<triggers>
- "Build a data pipeline for [use case]"
- "Validate data quality for [source]"
- "Set up backtesting infrastructure"
- "Aggregate data from multiple sources"
- "Data governance for [trading strategy]"
- "Real-time data feed for [token/market]"
- Keywords: data pipeline, data quality, validation, aggregation, backtesting, ML training, historical data, real-time feed, data governance
</triggers>

## Data Strategy Pillars

### 1. Diverse Data Sources

<data_sources>
**Price & Market Data:**
| Source | Data Type | Latency | Quality | Cost |
|--------|-----------|---------|---------|------|
| Dexscreener API | DEX prices, pools | Real-time | High | Free tier |
| Birdeye API | Solana tokens, analytics | Real-time | High | Paid |
| Jupiter Price API | Solana swap prices | Real-time | High | Free |
| CoinGecko | Cross-chain prices | 1-5 min | High | Free tier |
| CoinAPI | Historical + streaming | Configurable | Premium | Paid |

**On-Chain Data:**
| Source | Data Type | Latency | Quality | Cost |
|--------|-----------|---------|---------|------|
| Helius RPC | Solana transactions | Real-time | High | Freemium |
| Solscan API | Token info, holders | Near real-time | High | Free tier |
| Dune Analytics | SQL queries | Minutes-hours | High | Freemium |
| Flipside Crypto | Pre-built datasets | Hours | High | Free |

**Sentiment & Social:**
| Source | Data Type | Latency | Quality | Cost |
|--------|-----------|---------|---------|------|
| Twitter/X API | Social mentions | Real-time | Medium | Paid |
| LunarCrush | Social metrics | Near real-time | High | Paid |
| Telegram scraping | Community sentiment | Real-time | Low | DIY |
| Reddit API | Discussion sentiment | Minutes | Medium | Free |

**DeFi Protocol Data:**
| Source | Data Type | Latency | Quality | Cost |
|--------|-----------|---------|---------|------|
| DefiLlama API | TVL, revenue, yields | 15 min | High | Free |
| Token Terminal | Revenue, P/E ratios | Daily | High | Paid |
| DeFi Pulse | TVL rankings | Hourly | Medium | Free |
</data_sources>

### 2. Data Quality & Governance

<data_governance>
**Quality Dimensions:**
```typescript
interface DataQualityMetrics {
  accuracy: number;      // 0-100: correctness vs ground truth
  completeness: number;  // 0-100: missing values ratio
  timeliness: number;    // 0-100: freshness score
  consistency: number;   // 0-100: cross-source agreement
  validity: number;      // 0-100: schema conformance
}

interface QualityThresholds {
  trading_signals: { min: 90, critical: 'timeliness' };
  historical_analysis: { min: 85, critical: 'completeness' };
  sentiment_analysis: { min: 70, critical: 'consistency' };
  backtesting: { min: 95, critical: 'accuracy' };
}
```

**Validation Pipeline:**
```
Raw Data → Schema Validation → Anomaly Detection → Cross-Source Check → Quality Score → Accept/Reject
```

**Validation Rules:**
1. **Schema Validation**: All data must match expected types/formats
2. **Range Checks**: Prices, volumes, percentages within valid bounds
3. **Anomaly Detection**: Flag outliers > 3 standard deviations
4. **Cross-Source Verification**: Compare with 2+ sources for critical data
5. **Freshness Enforcement**: Reject stale data beyond threshold

**Automated Quality Monitoring:**
```bash
# Run continuous quality checks
npx tsx .claude/skills/data-orchestrator/scripts/quality-monitor.ts \
  --sources "dexscreener,birdeye,jupiter" \
  --interval 60 \
  --alert-threshold 80
```
</data_governance>

### 3. Real-Time Data Pipeline Architecture

<pipeline_architecture>
```
┌─────────────────────────────────────────────────────────────────┐
│                     DATA INGESTION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  WebSocket Feeds    │   REST Polling   │   RPC Subscriptions   │
│  (Dexscreener, WS) │   (Coingecko)    │   (Helius, Solana)    │
└──────────┬──────────┴────────┬─────────┴──────────┬────────────┘
           │                   │                    │
           ▼                   ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VALIDATION & ENRICHMENT                      │
├─────────────────────────────────────────────────────────────────┤
│  Schema Check  │  Anomaly Flag  │  Cross-Verify  │  Quality Score│
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE LAYER                         │
├─────────────────────────────────────────────────────────────────┤
│  Hot Store (Redis)   │  Warm Store (SQLite)  │  Cold (Parquet)  │
│  Real-time prices    │  Recent history (7d)  │  Historical data │
│  TTL: 5 minutes      │  Indexed, queryable   │  Compressed, ML  │
└──────────┬──────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CONSUMPTION LAYER                            │
├─────────────────────────────────────────────────────────────────┤
│  Trading Signals  │  ML Training  │  Backtesting  │  Dashboards │
│  (meme-trader)    │  (llama-analyst) │ (meme-executor) │ (Reports)│
└─────────────────────────────────────────────────────────────────┘
```

**Data Flow Configuration:**
```typescript
interface PipelineConfig {
  sources: DataSource[];
  validationRules: ValidationRule[];
  enrichmentSteps: EnrichmentFunction[];
  storageTargets: StorageTarget[];
  alertsEnabled: boolean;
  qualityThreshold: number;
}

const defaultPipeline: PipelineConfig = {
  sources: [
    { name: 'dexscreener', type: 'websocket', priority: 1 },
    { name: 'birdeye', type: 'rest', priority: 2 },
    { name: 'jupiter', type: 'rest', priority: 3 },
  ],
  validationRules: ['schema', 'range', 'anomaly', 'freshness'],
  enrichmentSteps: ['normalize', 'calculate_indicators', 'tag_quality'],
  storageTargets: ['redis:hot', 'sqlite:warm'],
  alertsEnabled: true,
  qualityThreshold: 85,
};
```
</pipeline_architecture>

### 4. ML/AI Integration Framework

<ml_integration>
**Data Preparation for ML:**
```typescript
interface MLReadyDataset {
  features: {
    price_data: TimeSeriesFeatures;
    volume_data: TimeSeriesFeatures;
    onchain_metrics: OnChainFeatures;
    sentiment_scores: SentimentFeatures;
    technical_indicators: TechnicalFeatures;
  };
  labels: {
    price_direction: 'up' | 'down' | 'sideways';
    price_magnitude: number;
    optimal_action: 'buy' | 'sell' | 'hold';
  };
  metadata: {
    timestamp: Date;
    token: string;
    quality_score: number;
    source_count: number;
  };
}

interface TimeSeriesFeatures {
  values: number[];
  timestamps: Date[];
  normalized: number[];  // Z-score normalized
  lagged: number[][];    // [lag_1, lag_5, lag_15, lag_60]
  rolling_stats: {
    mean_5: number[];
    std_5: number[];
    mean_15: number[];
    std_15: number[];
  };
}
```

**Supported ML Techniques:**
1. **Anomaly Detection**: Isolation forests for unusual price/volume patterns
2. **NLP/Sentiment**: BERT-based sentiment from social feeds
3. **Time Series**: LSTM/Transformer for price prediction
4. **Classification**: XGBoost for buy/sell signal classification
5. **Reinforcement Learning**: DQN for optimal trade execution

**Continuous Learning Pipeline:**
```
New Data → Feature Extraction → Model Inference → Signal Generation
                                      ↑
                                Performance Feedback
                                      ↓
                              Model Retraining (Weekly)
```
</ml_integration>

### 5. Backtesting Infrastructure

<backtesting>
**Historical Data Requirements:**
```typescript
interface BacktestDataset {
  token: string;
  timeframe: '1m' | '5m' | '15m' | '1h' | '4h' | '1d';
  start_date: Date;
  end_date: Date;
  data_points: {
    timestamp: Date;
    open: number;
    high: number;
    low: number;
    close: number;
    volume: number;
    liquidity: number;
    holders: number;
    sentiment_score?: number;
  }[];
  quality_metrics: DataQualityMetrics;
}
```

**Backtest Execution:**
```bash
# Run backtest with historical data
npx tsx .claude/skills/data-orchestrator/scripts/backtest-runner.ts \
  --strategy "momentum" \
  --token "BONK" \
  --start "2024-01-01" \
  --end "2024-12-01" \
  --initial-capital 1000 \
  --slippage 0.01
```

**Backtest Report Output:**
```
BACKTEST REPORT: Momentum Strategy on BONK
Period: 2024-01-01 to 2024-12-01

PERFORMANCE:
- Total Return: +234.5%
- Sharpe Ratio: 1.87
- Max Drawdown: -28.3%
- Win Rate: 62.4%
- Profit Factor: 2.15

TRADES:
- Total Trades: 156
- Avg Trade Duration: 4.2 hours
- Best Trade: +45.2%
- Worst Trade: -12.8%

DATA QUALITY:
- Coverage: 99.2%
- Missing Points: 847 / 105,120
- Quality Score: 94/100

CAVEATS:
- Historical results do not guarantee future performance
- Slippage model: 1% (actual may vary)
- Does not account for: MEV, extreme volatility periods
```
</backtesting>

### 6. Risk & Portfolio Data Layer

<risk_data>
**Portfolio Metrics:**
```typescript
interface PortfolioData {
  positions: {
    token: string;
    entry_price: number;
    current_price: number;
    size: number;
    unrealized_pnl: number;
    allocation_pct: number;
    risk_score: number;
  }[];
  aggregate: {
    total_value: number;
    total_pnl: number;
    daily_var: number;  // Value at Risk (95%)
    beta_to_sol: number;
    concentration_score: number;  // Herfindahl index
  };
  limits: {
    max_position_size: number;
    max_daily_loss: number;
    max_correlation: number;
    stop_loss_pct: number;
  };
}
```

**Risk Data Sources:**
- Position tracking from meme-executor
- Price volatility from historical data
- Correlation matrix from cross-asset analysis
- Liquidity depth from DEX APIs
</risk_data>

## Implementation Scripts

### Data Pipeline Manager
```bash
# Start the data pipeline
npx tsx .claude/skills/data-orchestrator/scripts/pipeline-manager.ts \
  --mode production \
  --sources all \
  --storage sqlite,redis

# Validate specific data source
npx tsx .claude/skills/data-orchestrator/scripts/validate-source.ts \
  --source dexscreener \
  --token "BONK" \
  --verbose

# Generate ML-ready dataset
npx tsx .claude/skills/data-orchestrator/scripts/ml-dataset-builder.ts \
  --token "BONK" \
  --features "price,volume,sentiment" \
  --lookback 30 \
  --output ./datasets/bonk_ml_ready.parquet
```

## Integration with Other Skills

<integrations>
**Data Orchestrator provides to:**
- **meme-trader**: Validated price/volume data, quality scores
- **llama-analyst**: DeFi protocol metrics, TVL/revenue time series
- **meme-executor**: Real-time execution prices, slippage estimates
- **flow-tracker**: On-chain flow data, whale movements
- **degen-savant**: Sentiment aggregates, social momentum

**Data Orchestrator receives from:**
- **All skills**: Data quality feedback, missing data requests
- **meme-executor**: Trade execution data for backtest validation
</integrations>

## Quality Gates

<validation_rules>
- All data must have quality score >= 80% for trading signals
- Price data staleness: max 30 seconds for live trading
- Historical data completeness: min 95% for backtesting
- Cross-source agreement: min 2 sources for critical decisions
- Schema validation: 100% compliance required
- Anomaly flagging: auto-reject data points > 5 sigma
</validation_rules>

## Error Handling

<error_recovery>
- **Source unavailable**: Failover to backup source within 5 seconds
- **Quality below threshold**: Alert + fallback to last good data
- **Schema mismatch**: Log error, use default values, alert
- **Rate limit hit**: Exponential backoff, rotate API keys
- **Network timeout**: Retry 3x with increasing delay
</error_recovery>

## Compliance & Security

<security>
- Encrypt API keys at rest and in transit
- Log all data access for audit trails
- Implement IP whitelisting for production
- GDPR-compliant: no PII in trading data
- Rate limit all external calls (prevent API bans)
- Regular security audits of data pipeline
</security>

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Data latency (real-time) | < 500ms | WebSocket to storage |
| Validation throughput | > 10K records/sec | Validation pipeline |
| Quality score accuracy | > 95% | vs manual audit |
| Backtest data coverage | > 99% | Historical completeness |
| ML feature freshness | < 5 min | Feature store update |

<see_also>
- references/data-sources.md - Complete API documentation
- references/quality-standards.md - Validation rule definitions
- references/ml-feature-catalog.md - Available ML features
- scripts/pipeline-manager.ts - Main orchestration script
- scripts/quality-monitor.ts - Continuous quality monitoring
- scripts/backtest-runner.ts - Historical backtesting
</see_also>
