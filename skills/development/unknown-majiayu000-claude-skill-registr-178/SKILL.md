---
name: portfolio-manager-agent
description: Portfolio allocation and rebalancing optimizer. Manages asset allocation across stocks/cash/bonds, performs periodic rebalancing, and ensures diversification according to market regime and risk tolerance.
license: Proprietary
compatibility: Requires portfolio data, market regime detector, Constitution module
metadata:
  author: ai-trading-system
  version: "1.0"
  category: system
  agent_role: portfolio_manager
---

# Portfolio Manager Agent - 포트폴리오 매니저

## Role
포트폴리오의 자산 배분, 리밸런싱, 다각화를 관리하여 위험 대비 수익을 최적화합니다.

## Core Capabilities

### 1. Asset Allocation Strategy

#### Dynamic Allocation by Market Regime

```python
# RISK_ON (경기 확장, VIX < 20)
allocation = {
    'stocks': 0.70,
    'bonds': 0.20,
    'cash': 0.10
}

# RISK_OFF (경기 수축, VIX > 25)
allocation = {
    'stocks': 0.40,
    'bonds': 0.40,
    'cash': 0.20
}

# TRANSITION (전환기, VIX 20-25)
allocation = {
    'stocks': 0.55,
    'bonds': 0.30,
    'cash': 0.15
}
```

#### Sector Diversification

```
Tech: 최대 40%
Finance: 최대 30%
Healthcare: 최대 25%
Other sectors: 최대 20% each
```

### 2. Rebalancing Triggers

```
IF deviation > 5%:
  → Rebalance recommended

Example:
Target: Stocks 70%
Current: Stocks 76%
Deviation: +6% → REBALANCE

IF deviation > 10%:
  → Urgent rebalance
  → Immediate notification
```

### 3. Risk Metrics Monitoring

- **Portfolio Beta**: 시장 대비 변동성
- **Sharpe Ratio**: 위험 대비 수익
- **Max Drawdown**: 최대 낙폭
- **Correlation Matrix**: 종목 간 상관관계

### 4. Position Sizing

```python
# Kelly Criterion (modified)
position_size = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win

# Position limits
position_size = min(position_size, MAX_SINGLE_POSITION)  # 15%
```

## Decision Framework

```
Step 1: Analyze Current Portfolio
  - Current allocation
  - Individual positions
  - Sector breakdown
  - Risk metrics

Step 2: Detect Market Regime
  from backend.ai.market_regime import MarketRegimeDetector
  regime = detector.detect_regime(market_data)

Step 3: Determine Target Allocation
  Based on regime:
    - RISK_ON → Aggressive (70/20/10)
    - RISK_OFF → Conservative (40/40/20)
    - TRANSITION → Balanced (55/30/15)

Step 4: Calculate Deviation
  deviation = |current - target|

Step 5: Rebalancing Decision
  IF deviation > threshold:
    → Generate rebalancing trades
  ELSE:
    → Hold current allocation

Step 6: Apply Constitutional Limits
  - Check Article 4 compliance
  - Ensure position limits
  - Verify sector limits
```

## Output Format

```json
{
  "agent": "portfolio_manager",
  "recommendation": "REBALANCE|HOLD",
  "confidence": 0.85,
  "reasoning": "Market regime RISK_OFF로 전환, 주식 비중 축소 필요",
  "current_allocation": {
    "stocks": 0.76,
    "bonds": 0.18,
    "cash": 0.06,
    "total_value_usd": 100000
  },
  "target_allocation": {
    "stocks": 0.55,
    "bonds": 0.30,
    "cash": 0.15
  },
  "deviation": {
    "stocks": 0.21,
    "bonds": -0.12,
    "cash": -0.09,
    "max_deviation": 0.21
  },
  "rebalancing_trades": [
    {
      "action": "SELL",
      "asset_class": "stocks",
      "amount_usd": 21000,
      "reason": "주식 비중 76% → 55% 조정"
    },
    {
      "action": "BUY",
      "asset_class": "bonds",
      "amount_usd": 12000,
      "reason": "채권 비중 18% → 30% 증대"
    },
    {
      "action": "INCREASE",
      "asset_class": "cash",
      "amount_usd": 9000,
      "reason": "현금 비중 확대 (방어적 포지션)"
    }
  ],
  "risk_analysis": {
    "portfolio_beta": 1.15,
    "sharpe_ratio": 1.45,
    "max_drawdown": -0.08,
    "expected_volatility": 0.18
  },
  "sector_breakdown": {
    "Technology": 0.35,
    "Finance": 0.20,
    "Healthcare": 0.15,
    "Other": 0.30
  },
  "next_review_date": "2025-12-28"
}
```

## Examples

**Example 1**: RISK_ON → 공격적 배분
```
Input:
- VIX: 15
- GDP Growth: 3.0%
- Market Regime: RISK_ON
- Current: Stocks 55%, Bonds 30%, Cash 15%

Output:
- Recommendation: REBALANCE
- Target: Stocks 70%, Bonds 20%, Cash 10%
- Trades:
  * BUY Stocks $15,000
  * SELL Bonds $10,000
  * REDUCE Cash $5,000
```

**Example 2**: RISK_OFF → 방어적 배분
```
Input:
- VIX: 28
- Recession signals
- Market Regime: RISK_OFF
- Current: Stocks 70%, Bonds 20%, Cash 10%

Output:
- Recommendation: URGENT_REBALANCE
- Target: Stocks 40%, Bonds 40%, Cash 20%
- Trades:
  * SELL Stocks $30,000
  * BUY Bonds $20,000
  * INCREASE Cash $10,000
```

**Example 3**: 편차 작음 → 유지
```
Input:
- Current: Stocks 68%, Bonds 22%, Cash 10%
- Target: Stocks 70%, Bonds 20%, Cash 10%
- Deviation: 2%, 2%, 0%

Output:
- Recommendation: HOLD
- Reasoning: "편차 < 5%, 거래 비용 고려 시 유지가 유리"
```

**Example 4**: 섹터 리밸런싱
```
Input:
- Tech: 45% (MAX 40%)
- Finance: 15%
- Healthcare: 10%

Output:
- Recommendation: SECTOR_REBALANCE
- Trades:
  * SELL Tech stocks $5,000 (45% → 40%)
  * BUY Healthcare $3,000
  * BUY Finance $2,000
```

## Guidelines

### Do's ✅
- **정기 리뷰**: 매주 또는 격주 점검
- **Market Regime 우선**: 거시 환경에 따른 배분
- **Gradual Rebalancing**: 급격한 변화 지양
- **Tax Efficiency**: 세금 효율적 리밸런싱

### Don'ts ❌
- 과도한 거래 금지 (거래 비용 고려)
- 단기 변동성에 과민 반응 금지
- 감정적 배분 변경 금지
- 헌법 제4조 위반 금지

## Integration with Market Regime Detector

```python
from backend.ai.market_regime import MarketRegimeDetector
from backend.ai.regime_detector import detect_market_regime

detector = MarketRegimeDetector()

regime_data = {
    'vix': 18,
    'yield_curve_10y2y': 0.3,
    'fed_stance': 'neutral',
    'gdp_growth': 0.025,
    'unemployment': 0.038,
    'cpi': 0.028
}

regime = detector.detect_regime(regime_data)

# Output:
# {
#   "current_regime": "RISK_ON",
#   "confidence": 0.75,
#   "recommended_asset_allocation": {
#     "stocks": 0.70,
#     "bonds": 0.20,
#     "cash": 0.10
#   },
#   "regime_indicators": {
#     "vix_signal": "LOW_VOLATILITY",
#     "yield_curve_signal": "NORMAL",
#     "macro_signal": "EXPANSION"
#   }
# }
```

## Rebalancing Algorithm

### Threshold-Based Rebalancing

```python
def check_rebalancing_needed(
    current: Dict[str, float],
    target: Dict[str, float],
    threshold: float = 0.05
) -> bool:
    """Check if rebalancing is needed"""
    
    for asset_class in target.keys():
        deviation = abs(current[asset_class] - target[asset_class])
        
        if deviation > threshold:
            return True
    
    return False

# Example
current = {'stocks': 0.76, 'bonds': 0.18, 'cash': 0.06}
target = {'stocks': 0.70, 'bonds': 0.20, 'cash': 0.10}

needs_rebalance = check_rebalancing_needed(current, target)  # True
```

### Optimal Trade Calculation

```python
def calculate_rebalancing_trades(
    current_allocation: Dict[str, float],
    target_allocation: Dict[str, float],
    total_portfolio_value: float
) -> List[Dict]:
    """Calculate optimal trades for rebalancing"""
    
    trades = []
    
    for asset_class, target_pct in target_allocation.items():
        current_pct = current_allocation[asset_class]
        current_value = current_pct * total_portfolio_value
        target_value = target_pct * total_portfolio_value
        
        diff = target_value - current_value
        
        if abs(diff) > 1000:  # Minimum trade $1,000
            action = "BUY" if diff > 0 else "SELL"
            trades.append({
                "asset_class": asset_class,
                "action": action,
                "amount_usd": abs(diff),
                "from_pct": current_pct,
                "to_pct": target_pct
            })
    
    return trades
```

## Performance Metrics

- **Rebalancing Frequency**: 목표 월 1-2회
- **Transaction Costs**: < 0.5% of portfolio value
- **Sharpe Ratio Improvement**: 목표 +10% vs buy-and-hold
- **Drawdown Reduction**: 목표 -20% vs unmanaged portfolio

## Constitutional Compliance

```python
from backend.constitution import Constitution

constitution = Constitution()

# Validate rebalancing trades
for trade in rebalancing_trades:
    # Check if new allocation violates Article 4
    new_allocation = apply_trade(current_allocation, trade)
    
    is_valid, violations, _ = constitution.validate_allocation(
        new_allocation,
        current_positions
    )
    
    if not is_valid:
        # Adjust trade to comply
        trade = adjust_trade_for_compliance(trade, violations)
```

## Risk-Adjusted Position Sizing

### Modern Portfolio Theory (MPT) Integration

```python
import numpy as np
from scipy.optimize import minimize

def optimize_portfolio(
    returns: np.array,
    covariance: np.array,
    risk_free_rate: float = 0.03
) -> np.array:
    """Optimize portfolio using MPT"""
    
    n_assets = len(returns)
    
    # Objective: Maximize Sharpe Ratio
    def objective(weights):
        portfolio_return = np.dot(weights, returns)
        portfolio_std = np.sqrt(np.dot(weights, np.dot(covariance, weights)))
        sharpe = (portfolio_return - risk_free_rate) / portfolio_std
        return -sharpe  # Minimize negative Sharpe
    
    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},  # Sum to 1
        {'type': 'ineq', 'fun': lambda w: w}  # Non-negative
    ]
    
    # Bounds (max 15% per stock)
    bounds = tuple((0, 0.15) for _ in range(n_assets))
    
    # Initial guess
    x0 = np.array([1/n_assets] * n_assets)
    
    # Optimize
    result = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x
```

## Collaboration with Other Agents

```
War Room → Trading Signals
  ↓
Portfolio Manager → Check current allocation
  ↓
IF new position causes imbalance:
  → Suggest partial position size
  OR
  → Recommend selling other positions first

Example:
War Room: BUY AAPL $15,000
Portfolio Manager: "Tech sector already 38%, BUY only $10,000"
```

## Reporting

### Weekly Portfolio Report

```markdown
# Portfolio Performance Report - Week of 2025-12-21

## Asset Allocation
- Stocks: 68% (Target: 70%) ✓
- Bonds: 22% (Target: 20%) ⚠️
- Cash: 10% (Target: 10%) ✓

## Performance
- Weekly Return: +2.3%
- YTD Return: +15.7%
- Sharpe Ratio: 1.45
- Max Drawdown: -8.2%

## Actions Taken
- None (within tolerance)

## Next Review: 2025-12-28
```

## Version History

- **v1.0** (2025-12-21): Initial release with MPT optimization and market regime integration
