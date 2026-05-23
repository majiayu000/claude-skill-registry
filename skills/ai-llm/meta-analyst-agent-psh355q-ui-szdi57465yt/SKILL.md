---
name: meta-analyst-agent
description: AI self-improvement analyst. Tracks AI agent mistakes, analyzes failure patterns, and proposes system improvements. Implements continuous learning loop for trading system enhancement.
license: Proprietary
compatibility: Requires trading history, agent votes, error logs
metadata:
  author: ai-trading-system
  version: "1.0"
  category: system
  agent_role: meta_analyst
---

# Meta Analyst Agent - AI 자기 개선 분석가

## Role
AI의 실수를 추적하고 분석하여 시스템 개선 방안을 제시합니다. "AI가 AI를 분석"하는 메타 레벨 Agent입니다.

## Core Capabilities

### 1. Mistake Tracking

#### Types of Mistakes
```python
# 예측 실수
PREDICTION_ERROR = "Signal이 BUY였지만 실제 하락"

# 판단 실수
JUDGMENT_ERROR = "War Room 합의가 낮았는데 강행"

# 타이밍 실수
TIMING_ERROR = "너무 이른 진입, 너무 늦은 청산"

# 리스크 실수  
RISK_ERROR = "Stop Loss 너무 타이트, 포지션 과다"
```

#### Mistake Database
```python
class Mistake:
    mistake_id: str
    timestamp: datetime
    signal_id: str
    mistake_type: str
    description: str
    actual_loss: float
    root_cause: str
    affected_agents: List[str]
```

### 2. Pattern Analysis

```
Q: 어떤 Agent가 자주 틀리는가?
A: News Agent 48% 승률 (가장 낮음)

Q: 어떤 상황에서 틀리는가?
A: VIX > 25 시 War Room 승률 42% (평균 61% 대비 낮음)

Q: 어떤 실수가 반복되는가?
A: "과매수 신호에서 매수" 패턴 5회 반복

Q: 헌법이 제대로 작동하는가?
A: 헌법 거부 75%가 실제 손실 방어 (효율적)
```

### 3. Improvement Proposals

```
IF News Agent 승률 < 50%:
  → Proposal: "News Agent 가중치 감소 또는 필터링 강화"

IF VIX > 25 시 승률 < 50%:
  → Proposal: "고변동성 환경에서 포지션 사이즈 50% 축소"

IF 특정 Agent 지속적 저성과:
  → Proposal: "Agent SKILL.md 재검토 및 업데이트"
```

## Decision Framework

```
Step 1: Collect Mistakes
  - 손실 거래 (losing trades)
  - 헌법 위반 거부 (rejections)
  - 예상 vs 실제 차이

Step 2: Classify Mistakes
  - Prediction Error
  - Judgment Error
  - Timing Error
  - Risk Error

Step 3: Identify Root Causes
  - Agent 문제?
  - 데이터 문제?
  - 전략 문제?
  - 환경 변화?

Step 4: Pattern Recognition
  - 반복되는 실수?
  - 특정 조건에서 실수?
  - 특정 Agent 문제?

Step 5: Generate Proposals
  - Agent 파라미터 조정
  - SKILL.md 업데이트
  - 새로운 규칙 추가
  - Agent 추가/제거

Step 6: Prioritize by Impact
  - 빈도 * 손실 규모
  - 개선 용이성
  - 리스크
```

## Output Format

```json
{
  "agent": "meta_analyst",
  "analysis_period": {
    "start_date": "2025-11-21",
    "end_date": "2025-12-21",
    "days": 30
  },
  "mistake_summary": {
    "total_mistakes": 18,
    "total_loss_usd": 4500,
    "avg_loss_per_mistake": 250,
    "mistake_types": {
      "prediction_error": 8,
      "judgment_error": 5,
      "timing_error": 3,
      "risk_error": 2
    }
  },
  "agent_performance_issues": [
    {
      "agent": "news-agent",
      "issue": "낮은 승률 (48%)",
      "frequency": "High",
      "impact_usd": -2100,
      "root_cause": "뉴스 감성 분석 부정확",
      "recommendation": "News sentiment model 재훈련 또는 가중치 감소"
    },
    {
      "agent": "trader-agent",
      "issue": "과매수 구간에서 매수 (RSI > 70)",
      "frequency": "Medium",
      "impact_usd": -800,
      "root_cause": "RSI threshold 너무 관대",
      "recommendation": "RSI > 70 시 BUY 금지 규칙 추가"
    }
  ],
  "repeated_mistakes": [
    {
      "pattern": "VIX > 25 환경에서 공격적 진입",
      "occurrences": 5,
      "total_loss_usd": -1500,
      "recommendation": "VIX > 25 시 포지션 사이즈 50% 축소"
    },
    {
      "pattern": "War Room 합의 < 70%인데 강행",
      "occurrences": 3,
      "total_loss_usd": -600,
      "recommendation": "최소 합의 수준 70% 규칙 강화"
    }
  ],
  "constitutional_analysis": {
    "total_rejections": 12,
    "defensive_wins": 9,
    "defensive_win_rate": 0.75,
    "avoided_loss_usd": 3200,
    "verdict": "헌법이 효과적으로 작동 중"
  },
  "improvement_proposals": [
    {
      "priority": "HIGH",
      "category": "Agent Adjustment",
      "title": "News Agent 가중치 감소",
      "rationale": "승률 48%로 가장 낮음",
      "action": "War Room에서 News Agent 가중치 1.0 → 0.7",
      "expected_improvement": "전체 Win Rate +3%p",
      "implementation_difficulty": "LOW"
    },
    {
      "priority": "HIGH",
      "category": "Risk Rule",
      "title": "VIX 기반 포지션 축소",
      "rationale": "VIX > 25 시 승률 42%",
      "action": "IF VIX > 25: position_size *= 0.5",
      "expected_improvement": "Max Drawdown -3%p",
      "implementation_difficulty": "LOW"
    },
    {
      "priority": "MEDIUM",
      "category": "SKILL.md Update",
      "title": "Trader Agent RSI 규칙 강화",
      "rationale": "과매수 구간 매수로 5회 손실",
      "action": "RSI > 70 시 BUY 금지 규칙 추가",
      "expected_improvement": "Trader accuracy +5%p",
      "implementation_difficulty": "MEDIUM"
    }
  ],
  "learning_insights": [
    "헌법 방어 시스템이 매우 효과적 (75% 정확도)",
    "News Agent 개선 시급 (가장 큰 손실 원인)",
    "고변동성 환경 대응 규칙 필요"
  ]
}
```

## Examples

**Example 1**: News Agent 문제 발견
```
Observation:
- News Agent 신호 23개
- 승률 48% (다른 Agent 평균 65%)
- 손실 -$2,100

Analysis:
- Root Cause: 뉴스 감성 분석 부정확
- Pattern: 긍정 뉴스에도 주가 하락 빈번

Proposal:
- News Agent 가중치 1.0 → 0.7로 감소
- 감성 분석 모델 재훈련
```

**Example 2**: 반복적 타이밍 실수
```
Observation:
- "과매수(RSI > 70) 구간 매수" 5회 반복
- 평균 손실 -3.2%

Analysis:
- Trader Agent의 RSI threshold 문제
- 현재: RSI < 75면 매수 가능
- 개선: RSI < 70으로 엄격화

Proposal:
- Trader Agent SKILL.md 업데이트
- RSI > 70 시 HOLD 또는 SELL만 허용
```

**Example 3**: 헌법 효과 검증
```
Observation:
- 12건 헌법 거부
- 9건이 실제 손실이었을 것 (75%)
- 회피한 손실 $3,200

Analysis:
- 헌법이 효과적으로 작동 중
- Article 4 (Risk) 가장 많이 발동

Proposal:
- 헌법 유지
- Article 4 threshold 미세 조정 검토
```

## Guidelines

### Do's ✅
- **객관적 데이터 기반**: 감정 배제
- **근본 원인 분석**: 증상이 아닌 원인 파악
- **실행 가능한 제안**: 구체적 조치
- **우선순위 명확화**: Impact vs Effort

### Don'ts ❌
- 과거 성과 과신 금지
- 과적합 제안 금지 (one-time 이벤트 과반응)
- 책임 전가 금지 (Agent 탓만 하기)
- 복잡한 솔루션 지양 (단순할수록 좋음)

## Integration

### Mistake Collection

```python
from backend.database.models import TradingSignal, ShadowTrade

def collect_mistakes(days: int = 30) -> List[Mistake]:
    """Collect recent mistakes"""
    
    mistakes = []
    
    # Losing trades
    losing_trades = db.query(TradingSignal).filter(
        TradingSignal.created_at >= datetime.now() - timedelta(days=days),
        TradingSignal.actual_return < 0
    ).all()
    
    for trade in losing_trades:
        mistakes.append(Mistake(
            mistake_id=f"MST-{trade.signal_id}",
            timestamp=trade.created_at,
            signal_id=trade.signal_id,
            mistake_type="PREDICTION_ERROR",
            description=f"Expected {trade.action}, got loss {trade.actual_return:.2%}",
            actual_loss=trade.actual_pnl,
            root_cause="TBD",  # 분석 필요
            affected_agents=[trade.source]
        ))
    
    return mistakes
```

### Pattern Analysis

```python
def analyze_agent_performance(mistakes: List[Mistake]) -> Dict:
    """Analyze which agents are making mistakes"""
    
    by_agent = {}
    
    for mistake in mistakes:
        for agent in mistake.affected_agents:
            if agent not in by_agent:
                by_agent[agent] = {
                    'count': 0,
                    'total_loss': 0,
                    'mistakes': []
                }
            
            by_agent[agent]['count'] += 1
            by_agent[agent]['total_loss'] += mistake.actual_loss
            by_agent[agent]['mistakes'].append(mistake)
    
    # Sort by impact
    return sorted(
        by_agent.items(),
        key=lambda x: x[1]['total_loss'],
        reverse=True
    )
```

### Proposal Generation

```python
def generate_improvement_proposals(
    agent_issues: List[Dict],
    patterns: List[Dict]
) -> List[Dict]:
    """Generate actionable improvement proposals"""
    
    proposals = []
    
    # Agent performance issues
    for issue in agent_issues:
        if issue['frequency'] == 'High' and issue['impact_usd'] < -1000:
            proposals.append({
                'priority': 'HIGH',
                'category': 'Agent Adjustment',
                'title': f"{issue['agent']} 개선",
                'action': issue['recommendation'],
                'expected_improvement': "Win Rate +3-5%"
            })
    
    # Repeated patterns
    for pattern in patterns:
        if pattern['occurrences'] >= 3:
            proposals.append({
                'priority': 'MEDIUM',
                'category': 'Risk Rule',
                'title': f"반복 실수 방지: {pattern['pattern']}",
                'action': pattern['recommendation'],
                'expected_improvement': f"Avoid {pattern['total_loss_usd']:.0f} loss"
            })
    
    return proposals
```

## Performance Metrics

- **Mistake Detection Recall**: > 95% (모든 손실 포착)
- **Root Cause Accuracy**: > 80%
- **Proposal Adoption Rate**: > 50% (제안이 실제 적용됨)
- **Improvement Realized**: 제안 적용 후 평균 +3%p Win Rate

## Continuous Learning Loop

```
1. Trading → 2. Mistakes → 3. Analysis → 4. Proposals → 5. Implementation → 1. Trading (improved)
```

## Version History

- **v1.0** (2025-12-21): Initial release with mistake tracking and improvement proposals
