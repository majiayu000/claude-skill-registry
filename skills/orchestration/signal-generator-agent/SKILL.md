---
name: signal-generator-agent
description: Final trading signal generator. Consolidates outputs from all analysis sources (War Room, Manual Analysis, Deep Reasoning, CEO Analysis, News) into unified TradingSignal database entries with proper attribution.
license: Proprietary
compatibility: Requires trading_signals table, all analysis agents
metadata:
  author: ai-trading-system
  version: "1.0"
  category: system
  agent_role: signal_generator
---

# Signal Generator Agent - 최종 시그널 생성기

## Role
모든 분석 소스(War Room, Analysis, Deep Reasoning, CEO Analysis, News)의 결과물을 통합하여 최종 `TradingSignal`을 생성하고 `trading_signals` 테이블에 저장합니다.

## Core Capabilities

### 1. Multi-Source Integration

#### Signal Sources
- **war_room**: AI Debate 결과
- **manual_analysis**: `/analysis` 페이지 빠른 분석
- **deep_reasoning**: `/deep-reasoning` 3단계 분석
- **ceo_analysis**: CEO 발언 Tone Shift
- **news_analysis**: 뉴스 감성 분석
- **emergency_news**: Grounding API 긴급 뉴스

### 2. Signal Unification

모든 소스의 Output을 표준 `TradingSignal` 포맷으로 변환:

```python
class TradingSignal:
    ticker: str
    action: str  # BUY, SELL, HOLD
    confidence: float  # 0.0 - 1.0
    reasoning: str
    source: str  # 출처 추적
    target_price: Optional[float]
    stop_loss: Optional[float]
    expected_return: Optional[float]
    risk_reward_ratio: Optional[float]
    metadata: Dict  # Source-specific data
```

### 3. Duplicate Detection

```
IF 동일 ticker + 동일 날짜 + 유사한 action:
  → Check if duplicate
  → IF confidence higher:
      → Update existing signal
  → ELSE:
      → Keep existing signal
```

### 4. Signal Priority

```
Emergency News > War Room > Deep Reasoning > CEO Analysis > Manual Analysis > News Analysis

IF conflict:
  → Higher priority source wins
  → Log conflict for review
```

## Decision Framework

```
Step 1: Receive analysis result from any source
  - War Room result
  - Analysis page result
  - Deep Reasoning result
  - CEO Analysis result
  - News Intelligence result
  - Emergency News alert

Step 2: Validate input
  - Required fields present
  - Action in [BUY, SELL, HOLD]
  - Confidence in [0, 1]

Step 3: Check for duplicates
  - Same ticker?
  - Same day?
  - Similar action?

Step 4: Resolve conflicts
  IF duplicate found:
    Apply priority rule or confidence rule

Step 5: Generate unified TradingSignal
  - Map source-specific fields to standard format
  - Add source attribution
  - Add timestamp

Step 6: Save to trading_signals table
  INSERT INTO trading_signals (...)

Step 7: Notify subscribers
  - WebSocket to /trading page
  - Optional Telegram notification
```

## Output Format

```json
{
  "signal_id": "SIG-20251221-001",
  "ticker": "AAPL",
  "action": "BUY",
  "confidence": 0.85,
  "reasoning": "War Room 합의 (5/6 BUY), 펀더멘털 양호, 기술적 골든크로스",
  "source": "war_room",
  "target_price": 205.00,
  "stop_loss": 195.00,
  "expected_return": 0.05,
  "risk_reward_ratio": 2.0,
  "metadata": {
    "war_room_consensus": 0.83,
    "agent_votes": {
      "trader": "BUY",
      "risk": "HOLD",
      "analyst": "BUY",
      "macro": "BUY",
      "institutional": "BUY",
      "news": "BUY",
      "pm": "BUY"
    },
    "constitutional_validation": {
      "is_constitutional": true,
      "violated_articles": []
    }
  },
  "created_at": "2025-12-21T13:00:00Z",
  "status": "ACTIVE"
}
```

## Examples

**Example 1**: War Room Signal
```
Input (from War Room):
{
  "ticker": "NVDA",
  "final_decision": "BUY",
  "final_confidence": 0.90,
  "consensus_level": 0.83,
  "agent_votes_summary": {...}
}

Output (TradingSignal):
{
  "ticker": "NVDA",
  "action": "BUY",
  "confidence": 0.90,
  "source": "war_room",
  "reasoning": "강력한 합의 (5/6 BUY), 헌법 준수",
  "metadata": {
    "consensus": 0.83,
    "votes": {...}
  }
}
```

**Example 2**: Deep Reasoning Signal
```
Input (from Deep Reasoning):
{
  "news_id": 123,
  "ticker": "TSLA",
  "stage3_conclusion": {
    "action": "BUY",
    "confidence": 0.85,
    "short_term": "BUY (1-3 months)",
    "long_term": "STRONG BUY (6-12 months)"
  }
}

Output (TradingSignal):
{
  "ticker": "TSLA",
  "action": "BUY",
  "confidence": 0.85,
  "source": "deep_reasoning",
  "reasoning": "3단계 CoT 분석 결과: 직접 수혜 + 시장 독과점 강화",
  "metadata": {
    "news_id": 123,
    "analysis_depth": "3_stage_cot",
    "timeframe": "short_to_long"
  }
}
```

**Example 3**: Emergency News Signal
```
Input (from Emergency News):
{
  "ticker": "MRNA",
  "urgency": "CRITICAL",
  "headline": "FDA Approves Cancer Vaccine",
  "impact_assessment": {
    "expected_price_impact": "+15-20%",
    "immediate_action": "BUY"
  }
}

Output (TradingSignal):
{
  "ticker": "MRNA",
  "action": "BUY",
  "confidence": 0.95,
  "source": "emergency_news",
  "reasoning": "긴급: FDA 신약 승인, 즉각적 시장 반응 예상 +15-20%",
  "metadata": {
    "urgency": "CRITICAL",
    "news_source": "Reuters",
    "detection_latency_seconds": 120
  }
}
```

**Example 4**: Duplicate Conflict Resolution
```
Existing Signal (09:00):
- Source: manual_analysis
- Action: BUY
- Confidence: 0.70

New Signal (10:00):
- Source: war_room
- Action: BUY
- Confidence: 0.85

Resolution:
→ Update existing signal with War Room data (higher priority)
→ Log: "Updated SIG-001 from manual_analysis to war_room"
```

## Guidelines

### Do's ✅
- **항상 source 기록**: 추적 가능성 중요
- **중복 방지**: 같은 ticker 하루에 여러 번 체크
- **Metadata 보존**: 원본 분석 데이터 유지
- **WebSocket 알림**: `/trading` 페이지 실시간 업데이트

### Don'ts ❌
- Source 정보 누락 금지
- 충돌 시 임의 선택 금지 (우선순위 규칙 따름)
- 과거 signal 무단 수정 금지
- 검증 없는 signal 생성 금지

## Database Integration

### trading_signals Table Schema

```sql
CREATE TABLE trading_signals (
    id SERIAL PRIMARY KEY,
    signal_id VARCHAR(50) UNIQUE NOT NULL,
    ticker VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL,
    confidence FLOAT NOT NULL,
    reasoning TEXT NOT NULL,
    source VARCHAR(50) NOT NULL,  -- NEW COLUMN
    
    target_price FLOAT,
    stop_loss FLOAT,
    expected_return FLOAT,
    risk_reward_ratio FLOAT,
    
    metadata JSONB,
    
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_ticker (ticker),
    INDEX idx_source (source),
    INDEX idx_created_at (created_at)
);
```

### Insert Example

```python
from backend.database.models import TradingSignal
from sqlalchemy.orm import Session

def create_trading_signal(
    session: Session,
    ticker: str,
    action: str,
    confidence: float,
    reasoning: str,
    source: str,
    metadata: dict
) -> TradingSignal:
    
    # Generate signal_id
    signal_id = f"SIG-{datetime.now().strftime('%Y%m%d')}-{get_next_seq()}"
    
    # Create signal
    signal = TradingSignal(
        signal_id=signal_id,
        ticker=ticker,
        action=action,
        confidence=confidence,
        reasoning=reasoning,
        source=source,
        metadata=metadata,
        status='ACTIVE'
    )
    
    session.add(signal)
    session.commit()
    
    return signal
```

## WebSocket Integration

```python
from fastapi import WebSocket

active_connections: List[WebSocket] = []

async def broadcast_new_signal(signal: TradingSignal):
    """Send new signal to all connected /trading page clients"""
    message = {
        "type": "new_signal",
        "data": {
            "signal_id": signal.signal_id,
            "ticker": signal.ticker,
            "action": signal.action,
            "confidence": signal.confidence,
            "source": signal.source,
            "timestamp": signal.created_at.isoformat()
        }
    }
    
    for connection in active_connections:
        await connection.send_json(message)
```

## Source-Specific Mapping

### War Room → TradingSignal
```python
def map_war_room_to_signal(war_room_result: Dict) -> Dict:
    return {
        "ticker": war_room_result["ticker"],
        "action": war_room_result["final_decision"],
        "confidence": war_room_result["final_confidence"],
        "reasoning": f"War Room 합의 ({war_room_result['consensus_level']:.0%})",
        "source": "war_room",
        "target_price": war_room_result.get("proposal", {}).get("target_price"),
        "stop_loss": war_room_result.get("proposal", {}).get("stop_loss"),
        "metadata": {
            "consensus": war_room_result["consensus_level"],
            "votes": war_room_result["agent_votes_summary"],
            "constitutional": war_room_result["constitutional_validation"]
        }
    }
```

### Deep Reasoning → TradingSignal
```python
def map_deep_reasoning_to_signal(deep_result: Dict) -> Dict:
    stage3 = deep_result["analysis"]["stage3_conclusion"]
    
    return {
        "ticker": deep_result["ticker"],
        "action": stage3["action"],
        "confidence": stage3["confidence"],
        "reasoning": stage3["reasoning"],
        "source": "deep_reasoning",
        "metadata": {
            "news_id": deep_result["news_id"],
            "stage1": deep_result["analysis"]["stage1_direct_impact"],
            "stage2": deep_result["analysis"]["stage2_secondary_effects"]
        }
    }
```

## Performance Metrics

- **Signal Generation Speed**: 목표 < 1초
- **Duplicate Detection Accuracy**: > 99%
- **Conflict Resolution Correctness**: > 95%
- **WebSocket Latency**: < 100ms

## Collaboration Example

```
Scenario: 동일 ticker AAPL에 대해 여러 소스에서 신호 발생

09:00 - Manual Analysis: BUY (confidence 0.70)
  → Create SIG-20251221-001

10:00 - War Room: BUY (confidence 0.85)
  → Update SIG-20251221-001 (higher priority)

11:00 - Deep Reasoning: HOLD (confidence 0.60)
  → Conflict! War Room > Deep Reasoning
  → Keep BUY, log conflict

12:00 - Emergency News: STRONG BUY (confidence 0.95)
  → Update SIG-20251221-001 (highest priority)

Final Signal:
- Action: BUY
- Confidence: 0.95
- Source: emergency_news
- History: [manual_analysis, war_room, emergency_news]
```

## Version History

- **v1.0** (2025-12-21): Initial release with multi-source integration
