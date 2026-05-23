---
name: risk-portfolio-manager
description: |
  AI-powered portfolio risk management and optimization. Use when sizing positions, managing portfolio allocation, calculating risk metrics (VaR, Sharpe), rebalancing, or implementing defensive strategies. Covers: position sizing, correlation analysis, drawdown management, dynamic rebalancing, kill switches.
tools: Read(pattern:.claude/skills/risk-portfolio-manager/**), WebSearch, WebFetch(domain:defillama.com|dexscreener.com|birdeye.so), mcp__perplexity-ask__search, mcp__perplexity-ask__reason, TodoWrite
---

# Risk Portfolio Manager - AI-Driven Risk Control

Systematic risk management layer that sits between signal generation and trade execution. Uses data-driven approaches to optimize position sizing, manage portfolio risk, and automate defensive actions.

## Core Principle

> Position sizing and risk management determine long-term survival. No single trade should threaten the portfolio.

## Activation Triggers

<triggers>
- "Size this position"
- "What's my portfolio risk?"
- "Rebalance my holdings"
- "Calculate VaR"
- "Should I take profit?"
- "Set up risk limits"
- "Portfolio correlation check"
- "Daily loss limit"
- Keywords: position size, risk management, portfolio, allocation, drawdown, VaR, Sharpe, rebalance, stop loss, take profit, correlation, diversification
</triggers>

## Core Capabilities

### 1. Position Sizing Engine

<position_sizing>
**Sizing Methods:**

```typescript
interface PositionSizeRequest {
  signal_strength: number;    // 0-1 from meme-trader
  token_risk_score: number;   // 1-10 from rug detection
  current_portfolio: Portfolio;
  market_regime: 'bull' | 'bear' | 'sideways' | 'volatile';
  risk_tolerance: 'conservative' | 'moderate' | 'degen';
}

interface PositionSizeResult {
  recommended_size_pct: number;  // % of portfolio
  recommended_size_usd: number;
  max_allowed_size: number;
  reasoning: string[];
  risk_warnings: string[];
}
```

**Kelly Criterion (Modified):**
```
Optimal Size = (Win Rate * Avg Win - (1 - Win Rate) * Avg Loss) / Avg Win
Adjusted Size = Kelly * Fractional Multiplier (0.25-0.5 for safety)
```

**Risk-Adjusted Sizing Matrix:**
| Risk Tolerance | Base Size | Max Single Position | Max Correlated Exposure |
|---------------|-----------|--------------------|-----------------------|
| Conservative | 0.5-1% | 2% | 5% |
| Moderate | 1-2% | 4% | 10% |
| Degen | 2-5% | 10% | 25% |

**Signal-Based Adjustments:**
```
Final Size = Base Size * Signal Strength * (1 - Token Risk / 20) * Market Multiplier

Where:
- Signal Strength: 0.5-1.5 (weak to strong)
- Token Risk: 1-10 (lower is safer)
- Market Multiplier: 0.5 (volatile) to 1.2 (trending)
```

**Output Format:**
```
POSITION SIZE RECOMMENDATION

Token: $MEME
Signal Strength: 8/10
Token Risk Score: 4/10
Market Regime: BULL

RECOMMENDED SIZE:
├─ Percentage: 2.3% of portfolio
├─ Amount: $460 (of $20,000 portfolio)
├─ Max Allowed: $800 (4% limit)
└─ Risk-Adjusted: WITHIN LIMITS

REASONING:
1. Strong signal (8/10) supports above-average sizing
2. Low-medium risk token (4/10) allows full allocation
3. Bull market regime permits aggressive sizing
4. No correlation with existing positions

WARNINGS:
- Consider scaling in (3 tranches) vs single entry
- Set stop-loss at -25% ($345 max loss)
```
</position_sizing>

### 2. Portfolio Risk Metrics

<risk_metrics>
**Real-Time Portfolio Dashboard:**
```
PORTFOLIO RISK DASHBOARD
═══════════════════════════════════════

POSITIONS (5 active):
Token      | Size    | PnL      | Risk  | Weight
$BONK      | $4,200  | +$840    | 5/10  | 21%
$MEME      | $3,100  | +$620    | 4/10  | 15.5%
$DOGE      | $2,800  | -$140    | 3/10  | 14%
$WIF       | $2,500  | +$1,250  | 6/10  | 12.5%
SOL        | $7,400  | +$2,220  | 2/10  | 37%
───────────────────────────────────────
TOTAL      | $20,000 | +$4,790  |       | 100%

RISK METRICS:
├─ Daily VaR (95%): -$1,240 (-6.2%)
├─ Max Drawdown (30d): -18.3%
├─ Current Drawdown: 0% (at ATH)
├─ Sharpe Ratio (30d): 2.14
├─ Sortino Ratio: 2.87
├─ Beta to SOL: 1.34

CORRELATION MATRIX:
        BONK   MEME   DOGE   WIF    SOL
BONK    1.00   0.82   0.71   0.78   0.65
MEME    0.82   1.00   0.68   0.85   0.61
DOGE    0.71   0.68   1.00   0.59   0.54
WIF     0.78   0.85   0.59   1.00   0.72
SOL     0.65   0.61   0.54   0.72   1.00

CONCENTRATION RISK:
├─ Top Position: 37% (SOL) - WITHIN LIMIT
├─ Top 3 Positions: 72.5% - HIGH
├─ Herfindahl Index: 0.23 - MODERATE
└─ Meme Exposure: 63% - HIGH

ALERTS:
⚠️ High correlation between MEME and WIF (0.85)
⚠️ Meme sector concentration above 50%
```

**Risk Calculations:**
```typescript
interface PortfolioRisk {
  // Value at Risk
  var_95: number;       // 95% confidence daily VaR
  var_99: number;       // 99% confidence daily VaR
  cvar_95: number;      // Conditional VaR (expected shortfall)

  // Performance Risk
  sharpe_ratio: number;
  sortino_ratio: number;
  max_drawdown: number;
  current_drawdown: number;

  // Correlation Risk
  avg_correlation: number;
  max_correlation: number;
  correlation_cluster: string[]; // Highly correlated groups

  // Concentration Risk
  herfindahl_index: number;
  top_position_pct: number;
  sector_concentrations: Record<string, number>;
}

function calculateVaR(
  positions: Position[],
  confidence: number = 0.95,
  horizon_days: number = 1
): number {
  // Historical VaR using past 30 days of returns
  const returns = getHistoricalReturns(positions, 30);
  const portfolio_returns = calculatePortfolioReturns(returns, positions);
  const sorted = portfolio_returns.sort((a, b) => a - b);
  const index = Math.floor((1 - confidence) * sorted.length);
  return sorted[index] * getPortfolioValue(positions) * Math.sqrt(horizon_days);
}
```
</risk_metrics>

### 3. Dynamic Rebalancing

<rebalancing>
**Rebalancing Triggers:**
- Drift > 5% from target allocation
- Single position > max limit
- Correlation spike > 0.9 between positions
- Sector concentration > threshold
- Weekly scheduled review

**Target Allocation Framework:**
```typescript
interface AllocationTarget {
  core_holdings: {
    SOL: { target: 30, min: 20, max: 50 };
    stablecoins: { target: 20, min: 10, max: 40 };
  };
  satellite_holdings: {
    memes: { target: 30, min: 0, max: 50 };
    defi: { target: 15, min: 0, max: 30 };
    other: { target: 5, min: 0, max: 15 };
  };
  rebalance_threshold: 5; // % drift to trigger
}
```

**Rebalancing Output:**
```
REBALANCING RECOMMENDATION

Current vs Target Allocation:
Category     | Current | Target | Drift  | Action
SOL          | 37%     | 30%    | +7%    | SELL $1,400
Memes        | 63%     | 50%    | +13%   | SELL $2,600
Stables      | 0%      | 20%    | -20%   | BUY $4,000

SUGGESTED TRADES:
1. SELL 15% of BONK position ($630) → USDC
2. SELL 20% of WIF position ($500) → USDC
3. SELL 10% of SOL position ($740) → USDC
4. Keep MEME and DOGE positions
5. Convert sales to USDC stablecoin buffer

POST-REBALANCE PROJECTION:
├─ SOL: 31% (target: 30%)
├─ Memes: 48% (target: 50%)
├─ Stables: 21% (target: 20%)
└─ VaR Reduction: -18% (improved risk profile)
```
</rebalancing>

### 4. Automated Defensive Actions

<defensive_actions>
**Kill Switch System:**
```typescript
interface KillSwitchConfig {
  daily_loss_limit: number;      // % of portfolio
  weekly_loss_limit: number;     // % of portfolio
  position_loss_limit: number;   // % per position
  drawdown_limit: number;        // % from peak
  correlation_spike_action: 'alert' | 'reduce' | 'exit';
  auto_execute: boolean;
}

const defaultKillSwitch: KillSwitchConfig = {
  daily_loss_limit: 10,      // Halt new trades at -10% day
  weekly_loss_limit: 20,     // Halt all activity at -20% week
  position_loss_limit: 30,   // Auto-close position at -30%
  drawdown_limit: 25,        // Emergency mode at -25% from peak
  correlation_spike_action: 'alert',
  auto_execute: false,       // Require confirmation in Phase 1
};
```

**Triggered Actions:**
| Trigger | Action | Severity |
|---------|--------|----------|
| Position -25% | Stop-loss warning | MEDIUM |
| Position -30% | Auto-close (if enabled) | HIGH |
| Daily -10% | Halt new trades | HIGH |
| Weekly -20% | Exit to stables | CRITICAL |
| Drawdown -25% | Emergency liquidation | CRITICAL |
| Correlation > 0.95 | Reduce one position | MEDIUM |

**Alert Output:**
```
🚨 RISK ALERT: DAILY LOSS LIMIT APPROACHING

Current Day PnL: -8.7% ($-1,740)
Daily Limit: -10% ($-2,000)
Buffer Remaining: $260

TRIGGERED ACTIONS:
1. ⏸️ New trade execution PAUSED
2. ⚠️ Review all open positions
3. 📊 Increased monitoring frequency

RECOMMENDED:
- Review worst performing position (WIF: -15%)
- Consider partial exit if trend continues
- DO NOT average down

Type RESUME to re-enable trading
Type EXIT_ALL to liquidate positions
```
</defensive_actions>

### 5. Scenario Analysis

<scenario_analysis>
**Stress Testing:**
```typescript
interface StressScenario {
  name: string;
  market_move: {
    sol: number;      // % change
    memes: number;    // % change vs SOL
    correlation_shift: number;
  };
  probability: number;
}

const stressScenarios: StressScenario[] = [
  {
    name: 'SOL -30% Flash Crash',
    market_move: { sol: -30, memes: -50, correlation_shift: 0.2 },
    probability: 0.05,
  },
  {
    name: 'Meme Rotation Out',
    market_move: { sol: 0, memes: -40, correlation_shift: -0.1 },
    probability: 0.10,
  },
  {
    name: 'Bull Run Continuation',
    market_move: { sol: 50, memes: 100, correlation_shift: 0 },
    probability: 0.15,
  },
  {
    name: 'Black Swan Event',
    market_move: { sol: -60, memes: -80, correlation_shift: 0.3 },
    probability: 0.01,
  },
];
```

**Stress Test Output:**
```
STRESS TEST RESULTS

Current Portfolio Value: $20,000

SCENARIO                    | Portfolio Impact | Probability
SOL -30% Flash Crash        | -$7,200 (-36%)   | 5%
Meme Rotation Out           | -$5,040 (-25%)   | 10%
Bull Run Continuation       | +$14,600 (+73%)  | 15%
Black Swan Event            | -$12,400 (-62%)  | 1%

EXPECTED PORTFOLIO VALUE:
├─ Base Case: $20,000
├─ Expected (prob-weighted): $22,340 (+11.7%)
├─ Worst Case (99%): -$12,400 (-62%)
└─ VaR (95%, 30d): -$4,800 (-24%)

RISK ASSESSMENT:
⚠️ High sensitivity to meme rotation (-25% scenario)
⚠️ Black swan exposure significant (-62%)
✓ Positive expected value in base scenarios
✓ Bull case upside substantial (+73%)

RECOMMENDATION:
Consider hedging meme exposure with SOL puts or reducing
meme allocation by 10-15% to improve risk profile.
```
</scenario_analysis>

## Integration Points

<integrations>
**Risk Manager receives from:**
- **meme-trader**: Signal strength, token risk scores
- **meme-executor**: Current positions, entry prices
- **flow-tracker**: Whale movements, liquidity data
- **data-orchestrator**: Validated price data, quality scores
- **llama-analyst**: Protocol fundamentals, TVL trends

**Risk Manager provides to:**
- **meme-executor**: Approved position sizes, stop-loss levels
- **meme-trader**: Position limits, available capital
- **All skills**: Portfolio state, risk alerts
</integrations>

## CLI Usage

```bash
# Calculate position size
npx tsx .claude/skills/risk-portfolio-manager/scripts/position-sizer.ts \
  --signal 8 \
  --risk-score 4 \
  --portfolio-file ./portfolio.json \
  --risk-mode moderate

# Get portfolio risk metrics
npx tsx .claude/skills/risk-portfolio-manager/scripts/risk-metrics.ts \
  --portfolio-file ./portfolio.json \
  --include-correlation \
  --var-confidence 95

# Rebalancing recommendation
npx tsx .claude/skills/risk-portfolio-manager/scripts/rebalancer.ts \
  --portfolio-file ./portfolio.json \
  --target-allocation ./targets.json \
  --threshold 5

# Run stress tests
npx tsx .claude/skills/risk-portfolio-manager/scripts/stress-test.ts \
  --portfolio-file ./portfolio.json \
  --scenarios default \
  --output-format detailed

# Check kill switch status
npx tsx .claude/skills/risk-portfolio-manager/scripts/kill-switch.ts \
  --portfolio-file ./portfolio.json \
  --check-status
```

## Quality Gates

<validation_rules>
- Position sizing requires quality score >= 85% on price data
- VaR calculations require 30+ days of clean historical data
- Correlation matrix requires synchronized price data
- All recommendations include confidence levels
- No position sizing without rug detection check
</validation_rules>

## Error Handling

<error_recovery>
- Missing price data: Use last known + stale warning
- Calculation error: Conservative fallback (minimum size)
- Kill switch conflict: Safety wins (halt > continue)
- Data quality insufficient: Reject sizing, request refresh
</error_recovery>

<see_also>
- references/risk-models.md - Mathematical formulas
- references/allocation-templates.md - Target portfolios
- scripts/position-sizer.ts - Sizing engine
- scripts/risk-metrics.ts - Risk calculations
- scripts/kill-switch.ts - Automated safety
</see_also>
