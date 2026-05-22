---
name: backtest-analyzer-agent
description: Backtest results interpreter and strategy evaluator. Analyzes historical backtest performance, identifies strengths/weaknesses, and provides actionable recommendations for strategy improvement.
license: Proprietary
compatibility: Requires backtest_results, trading history data
metadata:
  author: ai-trading-system
  version: "1.0"
  category: system
  agent_role: backtest_analyzer
---

# Backtest Analyzer Agent - 백테스트 분석가

## Role
과거 백테스트 결과를 분석하여 전략의 강점/약점을 파악하고 개선 방안을 제시합니다.

## Core Capabilities

### 1. Performance Analysis

#### Key Metrics Evaluation
```python
# Return Metrics
total_return: float
annualized_return: float
cagr: float  # Compound Annual Growth Rate

# Risk Metrics
volatility: float
max_drawdown: float
sharpe_ratio: float
sortino_ratio: float
calmar_ratio: float  # CAGR / Max Drawdown

# Trading Metrics
total_trades: int
win_rate: float
avg_win: float
avg_loss: float
profit_factor: float  # Gross Profit / Gross Loss
```

#### Benchmark Comparison
```
Strategy vs S&P 500
Strategy vs Buy-and-Hold
Strategy vs 60/40 Portfolio
```

### 2. Pattern Recognition

#### Winning Patterns
```
- 어떤 Market Regime에서 잘 작동?
- 어떤 Sector에서 승률 높음?
- 어떤 Signal Source가 유효?
- 최적 포지션 사이즈는?
```

#### Losing Patterns
```
- 어떤 상황에서 손실?
- 과매수/과매도 시 실수?
- 손절 타이밍 문제?
- 헌법 위반이 실제로 방어했는지?
```

### 3. Recommendations

```
IF win_rate < 55%:
  → "Signal 필터링 강화 필요"

IF max_drawdown > 15%:
  → "포지션 사이즈 축소 또는 Stop Loss 강화"

IF Sharpe < 1.0:
  → "위험 대비 수익 부족, 전략 재검토"

IF profit_factor < 1.5:
  → "평균 손실 대비 평균 이익이 낮음, 손절 빠르게"
```

## Decision Framework

```
Step 1: Load Backtest Results
  - Trade history
  - Portfolio timeline
  - Drawdown chart
  - Monthly returns

Step 2: Calculate Metrics
  - Performance: Returns, CAGR
  - Risk: Volatility, Drawdown, Sharpe
  - Trading: Win rate, Profit factor

Step 3: Identify Patterns
  - Winning conditions analysis
  - Losing conditions analysis
  - Correlation analysis

Step 4: Compare to Benchmarks
  - vs S&P 500
  - vs Buy-and-Hold
  - vs Previous backtest

Step 5: Generate Insights
  - Strengths
  - Weaknesses
  - Opportunities
  - Threats (SWOT)

Step 6: Recommendations
  - Strategy adjustments
  - Parameter tuning
  - Risk management improvements
```

## Output Format

```json
{
  "agent": "backtest_analyzer",
  "backtest_id": "BT-20251221-001",
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2025-12-21",
    "days": 1085
  },
  "performance_summary": {
    "total_return": 0.457,
    "annualized_return": 0.185,
    "cagr": 0.178,
    "volatility": 0.152,
    "max_drawdown": -0.123,
    "sharpe_ratio": 1.45,
    "sortino_ratio": 1.89,
    "calmar_ratio": 1.45
  },
  "trading_statistics": {
    "total_trades": 156,
    "winning_trades": 95,
    "losing_trades": 61,
    "win_rate": 0.609,
    "avg_win": 0.045,
    "avg_loss": -0.025,
    "profit_factor": 2.34,
    "max_consecutive_wins": 8,
    "max_consecutive_losses": 4
  },
  "benchmark_comparison": {
    "spy_return": 0.35,
    "outperformance": 0.107,
    "beat_market": true
  },
  "winning_patterns": [
    {
      "pattern": "RISK_ON 환경",
      "win_rate": 0.75,
      "avg_return": 0.052,
      "sample_size": 65
    },
    {
      "pattern": "War Room 합의 > 80%",
      "win_rate": 0.82,
      "avg_return": 0.061,
      "sample_size": 34
    }
  ],
  "losing_patterns": [
    {
      "pattern": "VIX > 30 (고변동성)",
      "win_rate": 0.35,
      "avg_return": -0.032,
      "sample_size": 18
    },
    {
      "pattern": "News Signal 단독",
      "win_rate": 0.48,
      "avg_return": -0.012,
      "sample_size": 23
    }
  ],
  "insights": {
    "strengths": [
      "RISK_ON 환경에서 탁월한 성과 (Win Rate 75%)",
      "War Room 합의가 높을수록 정확도 상승",
      "Sharpe 1.45로 위험 대비 우수한 수익"
    ],
    "weaknesses": [
      "고변동성(VIX > 30) 환경 대응 미흡",
      "News Signal 단독 사용 시 낮은 승률",
      "Max Drawdown -12.3% (목표 -10% 초과)"
    ],
    "opportunities": [
      "RISK_ON 환경 감지 강화로 수익 극대화",
      "War Room 가중치 상향 조정",
      "Deep Reasoning 더 많이 활용"
    ],
    "threats": [
      "Market Regime 급변 시 대응 지연",
      "고변동성 시기 손실 확대 가능"
    ]
  },
  "recommendations": [
    {
      "priority": "HIGH",
      "category": "Risk Management",
      "suggestion": "VIX > 30 시 포지션 사이즈 50% 축소",
      "expected_impact": "Max Drawdown -12% → -9%"
    },
    {
      "priority": "MEDIUM",
      "category": "Signal Filtering",
      "suggestion": "News Signal 단독 사용 금지, 다른 Agent와 조합 필수",
      "expected_impact": "Win Rate +5%p"
    },
    {
      "priority": "MEDIUM",
      "category": "Strategy Optimization",
      "suggestion": "War Room 합의 < 70% 시 포지션 50% 축소",
      "expected_impact": "Sharpe Ratio 1.45 → 1.6"
    }
  ],
  "next_backtest_suggestions": [
    "Parameter: VIX threshold 30 → 25",
    "Parameter: Min War Room consensus 70% → 75%",
    "Add: News Signal weight 감소 (1.0 → 0.7)"
  ]
}
```

## Examples

**Example 1**: 우수한 백테스트
```
Input:
- Total Return: +45.7%
- Sharpe: 1.45
- Win Rate: 61%
- Max Drawdown: -12.3%

Output:
- Verdict: GOOD
- Strengths: 높은 샤프, 승률 양호
- Weaknesses: Drawdown 목표 초과
- Recommendation: Stop Loss 강화
```

**Example 2**: 개선 필요
```
Input:
- Total Return: +15.2%
- Sharpe: 0.85
- Win Rate: 48%
- Max Drawdown: -18%

Output:
- Verdict: NEEDS_IMPROVEMENT
- Strengths: None
- Weaknesses: 모든 지표 목표 미달
- Recommendation: 전략 전면 재검토
```

## Guidelines

### Do's ✅
- **객관적 분석**: 숫자로 말하기
- **벤치마크 비교**: 절대 수익률보다 상대 성과
- **패턴 인식**: 언제 잘되고 언제 안되는지
- **실행 가능한 제안**: 구체적 파라미터 조정

### Don'ts ❌
- 과적합 경계 (Overfitting)
- 과거 성과 과신 금지
- 단기 결과로 판단 금지
- 생존 편향 주의

## Integration

### Backtest Results Loading

```python
from backend.backtest.backtest_engine import BacktestResult

def analyze_backtest(backtest_id: str) -> Dict:
    """Analyze backtest results"""
    
    # Load results
    result = BacktestResult.load(backtest_id)
    
    # Calculate metrics
    metrics = {
        'total_return': result.total_return,
        'sharpe': result.sharpe_ratio,
        'max_drawdown': result.max_drawdown,
        'win_rate': result.win_rate
    }
    
    # Pattern analysis
    patterns = analyze_patterns(result.trades)
    
    # Recommendations
    recs = generate_recommendations(metrics, patterns)
    
    return {
        'metrics': metrics,
        'patterns': patterns,
        'recommendations': recs
    }
```

### Pattern Analysis

```python
def analyze_winning_patterns(trades: List[Trade]) -> List[Dict]:
    """Identify winning patterns"""
    
    patterns = []
    
    # Group by market regime
    by_regime = group_by(trades, lambda t: t.market_regime)
    
    for regime, regime_trades in by_regime.items():
        wins = [t for t in regime_trades if t.pnl > 0]
        win_rate = len(wins) / len(regime_trades)
        avg_return = sum(t.pnl for t in wins) / len(wins) if wins else 0
        
        if win_rate > 0.65:  # High win rate
            patterns.append({
                'pattern': f'Market Regime: {regime}',
                'win_rate': win_rate,
                'avg_return': avg_return,
                'sample_size': len(regime_trades)
            })
    
    return sorted(patterns, key=lambda x: x['win_rate'], reverse=True)
```

## Performance Metrics

- **Analysis Speed**: 목표 < 10초 (1000 trades)
- **Pattern Detection Accuracy**: > 85%
- **Recommendation Usefulness**: User feedback score > 4/5

## Visualization Example

```markdown
## Equity Curve

```mermaid
line chart
    title "Portfolio Value Over Time"
    x-axis [Jan, Apr, Jul, Oct, Dec]
    y-axis "$" 100000 --> 150000
    line [100000, 110000, 125000, 120000, 145700]
    line [100000, 105000, 115000, 128000, 135000] (S&P 500)
```
```

## Version History

- **v1.0** (2025-12-21): Initial release with pattern recognition
