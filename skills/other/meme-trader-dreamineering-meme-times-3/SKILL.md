---
name: meme-trader
description: |
  Solana memecoin trading analysis and execution support. Use when analyzing tokens, detecting rugs, finding alpha, or planning trades on pump.fun, Raydium, Jupiter. Covers: token metrics, liquidity analysis, holder distribution, entry/exit signals, position sizing, degen strategies.
tools: Read(pattern:.claude/skills/meme-trader/**), WebSearch, WebFetch(domain:dexscreener.com|birdeye.so|solscan.io|pump.fun|jup.ag), mcp__perplexity-ask__search, TodoWrite
---

# Meme Trader - Solana Memecoin Trading System

Aggressive memecoin analysis, rug detection, and trade execution support for Solana ecosystem. Built for speed, alpha generation, and maximum degen potential.

## Activation Triggers

<triggers>
- "Analyze [token/CA]"
- "Is this a rug?"
- "Find me alpha"
- "Entry point for [token]"
- "Pump.fun launches"
- "Best memes to ape"
- "Liquidity check [token]"
- "Holder distribution [CA]"
- Keywords: memecoin, pump.fun, raydium, jupiter, dexscreener, birdeye, solana meme, ape, degen
</triggers>

## Core Capabilities

### 1. Token Analysis
- Contract verification (mint authority, freeze authority)
- Liquidity depth and lock status
- Holder distribution (whale concentration, dev wallets)
- Social sentiment scraping
- Volume/MCAP ratio analysis

### 2. Rug Detection
- Honeypot detection (sell tax, blacklist functions)
- Dev wallet tracking
- Liquidity pull risk assessment
- Contract red flags (hidden mints, proxy patterns)
- Team verification (KOL backing, doxxed devs)

### 3. Trade Signals
- Entry point identification (support levels, breakout detection)
- Exit signals (resistance, volume divergence)
- Position sizing based on risk tolerance
- Stop-loss recommendations
- Take-profit laddering strategies

### 4. Alpha Generation
- New launch monitoring (pump.fun, Raydium)
- Social trend detection (Twitter/X, Telegram)
- Whale wallet tracking
- Cross-reference with successful patterns

## Data Sources

<data_sources>
- **Dexscreener**: Price, volume, liquidity, charts
- **Birdeye**: Token analytics, holder data, trades
- **Solscan**: Contract verification, token info
- **Pump.fun**: New launches, bonding curves
- **Jupiter**: Swap routing, price impact
- **Helius/Shyft**: RPC, transaction parsing
</data_sources>

## Data Quality & Governance

<data_governance>
**Quality Requirements (via data-orchestrator):**
All trading signals require minimum data quality scores:

| Signal Type | Min Quality Score | Max Data Age |
|-------------|------------------|--------------|
| Entry Signal | 90/100 | 30 seconds |
| Exit Signal | 90/100 | 30 seconds |
| Rug Detection | 95/100 | 60 seconds |
| Position Sizing | 85/100 | 5 minutes |
| Alpha Scan | 80/100 | 15 minutes |

**Validation Pipeline:**
```
Raw Price Data → Schema Check → Cross-Source Verify → Anomaly Flag → Quality Score
                                    ↓
                        Min 2 sources agree (5% tolerance)
```

**Data Quality Indicators in Output:**
```
DATA QUALITY: 94/100 ✓
├─ Sources: 3/3 (dexscreener, birdeye, jupiter)
├─ Price Agreement: 99.2%
├─ Freshness: 12s ago
└─ Anomaly Check: PASS
```

**Rejection Criteria:**
- Quality score < 80%: REJECT signal, show warning
- Single source only: Add "LOW CONFIDENCE" flag
- Price divergence > 10%: REJECT, investigate
- Data age > 60s for live signals: STALE warning
</data_governance>

## ML-Enhanced Signal Generation

<ml_signals>
**AI/ML Signal Sources:**
1. **Anomaly Detection**: Flag unusual volume/price patterns
   - Isolation forest on 24h price/volume deviation
   - Alert when score > 0.8 (potential pump or dump)

2. **Sentiment Classification**: Social momentum scoring
   - NLP analysis of Twitter/Telegram mentions
   - Bullish/Bearish/Neutral with confidence score

3. **Pattern Recognition**: Historical pattern matching
   - Compare current setup to 1000+ historical pumps
   - Match score indicates similarity to successful entries

4. **Predictive Indicators**: ML-derived signals
   - 1h price direction probability (up/down/sideways)
   - Optimal entry window prediction
   - Volume momentum forecast

**Signal Confidence Framework:**
```typescript
interface MLSignal {
  type: 'anomaly' | 'sentiment' | 'pattern' | 'predictive';
  value: number;          // -1 to 1 (bearish to bullish)
  confidence: number;     // 0 to 1
  data_quality: number;   // 0 to 100
  features_used: string[];
  model_version: string;
  timestamp: Date;
}

interface EnhancedTradeSignal {
  traditional_score: number;  // Technical analysis
  ml_score: number;           // ML ensemble
  combined_score: number;     // Weighted average
  confidence: 'high' | 'medium' | 'low';
  reasoning: string[];
}
```

**ML Signal Output Format:**
```
ML SIGNALS: $MEME
├─ Anomaly Score: 0.72 (elevated activity detected)
├─ Sentiment: BULLISH (0.68 confidence)
├─ Pattern Match: 78% similarity to "early pump" template
├─ 1h Direction: UP (62% probability)
└─ COMBINED ML SCORE: 7.2/10

RECOMMENDATION: Traditional + ML signals ALIGNED
                Confidence: HIGH
```
</ml_signals>

## Adaptive Learning

<adaptive_learning>
**Continuous Improvement Loop:**
```
Signal Generated → Trade Outcome Tracked → Performance Feedback
        ↑                                          ↓
  Model Updated ← Weekly Retraining ← Outcome Analysis
```

**Signal Performance Tracking:**
- Track all generated signals with outcomes
- Calculate accuracy by signal type and market condition
- Adjust weighting based on recent performance
- Flag underperforming signal sources for review

**Adaptation Triggers:**
- Win rate drops below 55%: Review signal parameters
- New market regime detected: Retrain models
- Volatility spike: Tighten quality requirements
- High correlation breakdown: Recalibrate ensemble
</adaptive_learning>

## Implementation Workflow

### Step 1: Parse Query Intent
```typescript
interface MemeQuery {
  token_address?: string;
  token_name?: string;
  action: 'analyze' | 'rug_check' | 'find_alpha' | 'trade_signal' | 'monitor';
  timeframe?: '1m' | '5m' | '1h' | '4h' | '1d';
  risk_level?: 'conservative' | 'moderate' | 'degen';
}
```

### Step 2: Data Retrieval
Execute `scripts/fetch-meme-data.ts` with parsed parameters:
```bash
npx tsx .claude/skills/meme-trader/scripts/fetch-meme-data.ts \
  --token "PUMP123...abc" \
  --action analyze \
  --risk degen
```

### Step 3: Analysis Pipeline
1. **Contract Check** � Verify no malicious functions
2. **Liquidity Check** � Assess depth and lock status
3. **Holder Analysis** � Distribution and whale activity
4. **Social Scan** � Sentiment and narrative strength
5. **Signal Generation** � Entry/exit recommendations

### Step 4: Format Response
Use templates from `references/token-analysis-templates.md`

## Output Formats

### Quick Scan (Default)
```
TOKEN: $MEME (Contract: abc123...)
VERDICT: APE / WATCH / AVOID
RISK: 7/10

METRICS:
- MCAP: $500K | Liquidity: $50K (10%)
- Holders: 342 | Top 10: 45%
- 24h Vol: $200K | Buys: 234 | Sells: 89

RED FLAGS: None detected
GREEN FLAGS: LP locked 6mo, renounced mint

ENTRY: $0.00042 (current -5%)
TP1: $0.00065 (+55%)
TP2: $0.00098 (+133%)
SL: $0.00032 (-24%)
```

### Deep Analysis (--format deep)
Full contract audit, holder breakdown, social analysis, comparable tokens, historical pattern matching.

### Signal Only (--format signal)
```
$MEME: BUY @ 0.00042 | TP 0.00065/0.00098 | SL 0.00032 | Size: 2% port
```

## Risk Framework

### Degen Mode (Aggressive)
- Position size: Up to 5% portfolio per trade
- Stop-loss: 30-50% from entry
- Take-profit: 2-5x minimum target
- Acceptable rug risk: Up to 40%
- Entry timing: Early (< 50 holders)

### Moderate Mode
- Position size: 1-2% portfolio
- Stop-loss: 20-30%
- Take-profit: 50-100% gains
- Acceptable rug risk: < 20%
- Entry timing: After initial pump settles

### Conservative Mode
- Position size: 0.5-1% portfolio
- Stop-loss: 10-15%
- Take-profit: 20-50% gains
- Acceptable rug risk: < 10%
- Entry timing: Established tokens only

## Rug Detection Checklist

<rug_indicators>
**CRITICAL (Instant Avoid):**
- [ ] Mint authority NOT renounced
- [ ] Freeze authority enabled
- [ ] Hidden transfer fees > 5%
- [ ] Liquidity < $10K
- [ ] LP not locked
- [ ] Top holder > 20% (non-exchange)

**WARNING (Proceed with caution):**
- [ ] Dev wallet holds > 5%
- [ ] < 100 holders
- [ ] No social presence
- [ ] Copied contract (no modifications)
- [ ] Launch < 1 hour ago

**GREEN FLAGS:**
- [x] Mint renounced + freeze disabled
- [x] LP locked 3+ months
- [x] Top 10 holders < 30%
- [x] Active community (TG/Twitter)
- [x] KOL/influencer backing
- [x] Audited contract
</rug_indicators>

## Quality Gates

<validation_rules>
- Price data: Max 30 seconds old
- Holder data: Max 5 minutes old
- Contract verification: Always fresh
- Never recommend without liquidity check
- Always show risk score (1-10)
- Include stop-loss with every entry signal
</validation_rules>

## Error Handling

<error_recovery>
- API timeout: Retry with fallback source (Birdeye � Dexscreener � Jupiter)
- Invalid CA: Suggest similar tokens or request clarification
- No liquidity: Return "AVOID - No liquidity" immediately
- Rate limited: Queue and batch requests
</error_recovery>

## Performance Targets

- Token scan: < 3 seconds
- Full analysis: < 10 seconds
- Signal accuracy: > 60% profitable (degen mode)
- Rug detection: > 90% accuracy

## Security Considerations

<security>
- Never expose private keys or wallet seeds
- Sanitize all contract addresses
- Rate limit API calls (prevent ban)
- Warn on suspicious contract patterns
- No financial advice disclaimers (user assumes risk)
</security>

<see_also>
- references/meme-trading-strategies.md � Degen playbook
- references/token-analysis-templates.md � Analysis frameworks
- scripts/fetch-meme-data.ts � CLI implementation
</see_also>
