---
name: deep-reasoning-agent  
description: Three-stage Chain of Thought (CoT) analyzer for /deep-reasoning page. Performs comprehensive analysis in 3 stages Direct Impact → Secondary Effects → Final Conclusion for complex news articles. Optimized for depth over speed.
license: Proprietary
compatibility: Requires news_articles table, comprehensive market data, AI reasoning capabilities, related tickers database
metadata:
  author: ai-trading-system
  version: "1.0"
  category: analysis
  agent_role: deep_reasoner
---

# Deep Reasoning Agent - 3단계 심층 분석

## Role
`/deep-reasoning` 페이지에서 뉴스 기사를 **3단계 Chain of Thought (CoT)**로 심층 분석합니다. 속도보다 깊이를 우선시합니다.

## Core Capabilities

### 1. Three-Stage Chain of Thought

#### Stage 1: Direct Impact (직접 영향)
```
Goal: 뉴스가 해당 기업에 미치는 즉각적이고 직접적인 영향 분석

Questions:
- 이 뉴스는 무엇을 말하는가?
- 회사의 어떤 부분에 영향을 주는가?
- 재무적 영향은 얼마나 되는가?
- 시간 프레임은? (즉시 vs 장기)

Output:
- 직접 영향 요약
- Impact Score (0-1)
- Timeframe (immediate, short-term, long-term)
```

**Example**:
```
News: "FDA approves XYZ cancer drug"

Stage 1 Analysis:
- 직접 영향: 신약 판매 승인 → 매출 증가
- 예상 매출: 연간 $5B (analyst estimates)
- 영향 크기: VERY_HIGH (0.9)
- Timeframe: Short-term (6-12 months to ramp up)
```

#### Stage 2: Secondary Effects (2차 파급 효과)
```
Goal: 공급망, 경쟁사, 관련 산업에 미치는 간접 영향 분석

Questions:
- 경쟁사는 어떤 영향을 받는가?
- 공급망(upstream/downstream)은?
- 규제 환경 변화?
- 시장 점유율 변화?

Output:
- 영향 받는 티커 리스트
- 각 티커별 영향 방향 (positive/negative)
- 산업 전체 영향
```

**Example**:
```
News: "Tesla announces 20% price cut"

Stage 2 Analysis:
- 경쟁사 영향:
  * GM, F: NEGATIVE (가격 경쟁 압박)
  * RIVN, LCID: VERY_NEGATIVE (소규모 업체, 가격 대응 어려움)
- 공급망:
  * Battery suppliers (PANW, LG에너지솔루션): NEGATIVE (주문량 감소 우려)
  * Charging network (CHPT): NEUTRAL (볼륨 증가 가능)
- 산업 영향: 전기차 가격 하락 압박 → 보급 가속화
```

#### Stage 3: Final Conclusion (최종 결론)
```
Goal: Stage 1 + Stage 2 종합하여 투자 결정 및 전략 수립

Questions:
- 종합 판단: BUY/SELL/HOLD?
- 시간대별 전략?
- 주요 리스크는?
- 대안 시나리오는?

Output:
- Action (BUY/SELL/HOLD)
- Confidence (0-1)
- Short-term vs Long-term 전략
- Risk Factors
- Alternative Scenarios
```

**Example**:
```
Conclusion:
- Action: BUY (the drug company)
- Confidence: 0.85
- Short-term (1-3 months): STRONG BUY (FDA 승인 모멘텀)
- Long-term (6-12 months): BUY (매출 본격화)
- Risks:
  * 보험 coverage 불확실성
  * 경쟁 약물 개발 가능성
- Alternative Scenario:
  * IF insurance rejects coverage → 주가 -15%
  * IF competitor announces similar drug → 주가 -10%
```

### 2. Related Tickers Analysis

```python
def find_related_tickers(news_article: NewsArticle) -> List[Dict]:
    """Find all tickers affected by the news"""
    
    related = []
    
    # Primary ticker (mentioned in news)
    primary = news_article.ticker
    
    # Competitors (same sector)
    competitors = get_competitors(primary)
    
    # Supply chain
    suppliers = get_suppliers(primary)
    customers = get_customers(primary)
    
    # Industry ETFs
    etfs = get_related_etfs(primary)
    
    return {
        "primary": primary,
        "competitors": competitors,
        "suppliers": suppliers,
        "customers": customers,
        "etfs": etfs
    }
```

### 3. Impact Quantification

```python
def quantify_impact(
    news_type: str,
    magnitude: str,
    company_size: str
) -> Dict:
    """Estimate price impact"""
    
    # Base impact by news type
    BASE_IMPACT = {
        "fda_approval": 0.15,      # +15% average
        "earnings_beat": 0.05,     # +5%
        "merger": 0.20,            # +20%
        "lawsuit": -0.10,          # -10%
        "ceo_departure": -0.08     # -8%
    }
    
    # Magnitude multiplier
    MAGNITUDE = {
        "small": 0.5,
        "medium": 1.0,
        "large": 1.5
    }
    
    # Company size adjustment
    SIZE_ADJ = {
        "large_cap": 0.7,    # Less volatile
        "mid_cap": 1.0,
        "small_cap": 1.3     # More volatile
    }
    
    base = BASE_IMPACT.get(news_type, 0.05)
    mag = MAGNITUDE.get(magnitude, 1.0)
    size = SIZE_ADJ.get(company_size, 1.0)
    
    estimated_impact = base * mag * size
    
    return {
        "estimated_price_change_pct": estimated_impact,
        "confidence": 0.6,  # Historical accuracy
        "timeframe": "1-3 months"
    }
```

## Decision Framework

```
Step 1: Receive News Article
  - news_id: 123
  - ticker: MRNA
  - headline: "FDA Approves Cancer Vaccine"
  - content: [full article]

Step 2: Stage 1 Analysis (Direct Impact)
  prompt_stage1 = f"""
  Analyze the DIRECT impact of this news on {ticker}:
  
  News: {headline}
  {content}
  
  Answer:
  1. What happened?
  2. How does it affect the company's revenue?
  3. What is the financial impact?
  4. When will impact be felt?
  """
  
  stage1_result = call_ai(prompt_stage1)

Step 3: Stage 2 Analysis (Secondary Effects)
  # Find related tickers
  related = find_related_tickers(ticker)
  
  prompt_stage2 = f"""
  Stage 1 conclusion: {stage1_result}
  
  Now analyze SECONDARY effects:
  
  Competitors: {related['competitors']}
  Suppliers: {related['suppliers']}
  
  Answer:
  1. How do competitors react?
  2. Supply chain impact?
  3. Industry-wide changes?
  """
  
  stage2_result = call_ai(prompt_stage2)

Step 4: Stage 3 Conclusion
  prompt_stage3 = f"""
  Stage 1: {stage1_result}
  Stage 2: {stage2_result}
  
  Provide FINAL trading decision:
  
  1. BUY/SELL/HOLD?
  2. Short-term vs Long-term strategy?
  3. Key risks?
  4. Alternative scenarios?
  """
  
  stage3_result = call_ai(prompt_stage3)

Step 5: Generate Trading Signal
  IF stage3_result.action == "BUY":
    create_trading_signal(
      ticker=ticker,
      action="BUY",
      source="deep_reasoning",
      confidence=stage3_result.confidence,
      metadata={
        "news_id": news_id,
        "stage1": stage1_result,
        "stage2": stage2_result,
        "stage3": stage3_result
      }
    )
```

## Output Format

```json
{
  "news_id": 123,
  "ticker": "MRNA",
  "headline": "FDA Approves Moderna Cancer Vaccine",
  "analysis_timestamp": "2025-12-21T13:00:00Z",
  "analysis_duration_sec": 28,
  
  "stage1_direct_impact": {
    "summary": "FDA 승인으로 Moderna의 암 백신이 시장 진입. 연간 매출 $5B 추정 (분석가 컨센서스). 회사 총 매출의 ~40% 증가 예상.",
    "impact_score": 0.9,
    "impact_level": "VERY_HIGH",
    "timeframe": "short_term",
    "financial_estimates": {
      "annual_revenue_potential": 5000000000,
      "margin_estimate": 0.65,
      "market_exclusivity_years": 7
    },
    "reasoning": "신약 승인은 즉각적인 매출 기회 창출. Moderna는 mRNA 플랫폼의 입증된 리더로 빠른 상용화 가능."
  },
  
  "stage2_secondary_effects": {
    "summary": "경쟁 제약사(PFE, MRCK)는 암 백신 경쟁 심화. mRNA 공급망(LNP suppliers) 수혜. 헬스케어 섹터 전체 긍정적.",
    "affected_tickers": [
      {
        "ticker": "PFE",
        "relationship": "competitor",
        "impact": "NEGATIVE",
        "impact_score": -0.3,
        "reasoning": "시장 점유율 위협, 경쟁 심화"
      },
      {
        "ticker": "MRCK",
        "relationship": "competitor",
        "impact": "NEGATIVE",
        "impact_score": -0.2,
        "reasoning": "암 치료 시장 경쟁 증가"
      },
      {
        "ticker": "NVAX",
        "relationship": "competitor",
        "impact": "NEUTRAL",
        "impact_score": 0.1,
        "reasoning": "다른 질병 포커스, 직접 경쟁 적음"
      },
      {
        "ticker": "XLV",
        "relationship": "sector_etf",
        "impact": "POSITIVE",
        "impact_score": 0.2,
        "reasoning": "헬스케어 혁신 긍정적 신호"
      }
    ],
    "industry_impact": "mRNA 기술 입지 강화, 암 치료 패러다임 전환 기대감",
    "supply_chain_effects": "LNP(Lipid Nanoparticle) 수요 증가, CDMO 수혜"
  },
  
  "stage3_conclusion": {
    "action": "BUY",
    "confidence": 0.85,
    "reasoning": "Stage 1 매우 긍정적 직접 영향 + Stage 2 경쟁사 약세는 MRNA의 경쟁 우위 강화. 단기 모멘텀 + 장기 펀더멘털 모두 양호.",
    
    "time_horizon_strategy": {
      "short_term_1_3_months": {
        "action": "STRONG_BUY",
        "confidence": 0.90,
        "rationale": "FDA 승인 모멘텀, 미디어 주목, 기관 매수 예상",
        "target_price": 185.00,
        "expected_return": 0.18
      },
      "medium_term_3_6_months": {
        "action": "BUY",
        "confidence": 0.80,
        "rationale": "상용화 진행, 초기 매출 데이터 공개",
        "target_price": 200.00,
        "expected_return": 0.28
      },
      "long_term_6_12_months": {
        "action": "HOLD_OR_BUY",
        "confidence": 0.70,
        "rationale": "매출 본격화, 하지만 경쟁 약물 출현 가능성",
        "target_price": 210.00,
        "expected_return": 0.34
      }
    },
    
    "risk_factors": [
      {
        "risk": "보험 coverage 불확실성",
        "probability": 0.30,
        "impact": "HIGH",
        "mitigation": "FDA 승인 후 보험사 협상 주시"
      },
      {
        "risk": "경쟁 약물 파이프라인",
        "probability": 0.40,
        "impact": "MEDIUM",
        "mitigation": "PFE, MRCK 임상 데이터 모니터링"
      },
      {
        "risk": "부작용 보고",
        "probability": 0.15,
        "impact": "VERY_HIGH",
        "mitigation": "초기 phase 4 데이터 주시"
      }
    ],
    
    "alternative_scenarios": [
      {
        "scenario": "보험 coverage 거부",
        "probability": 0.20,
        "price_impact": -0.15,
        "action_change": "HOLD → SELL"
      },
      {
        "scenario": "경쟁사 유사 약물 승인 (6개월 내)",
        "probability": 0.25,
        "price_impact": -0.10,
        "action_change": "BUY → HOLD"
      },
      {
        "scenario": "초기 매출 기대치 초과",
        "probability": 0.35,
        "price_impact": +0.20,
        "action_change": "BUY → STRONG_BUY"
      }
    ],
    
    "key_catalysts": [
      "보험 coverage 발표 (positive)",
      "임상 추가 데이터 (efficacy 확인)",
      "국제 승인 (EU, Japan)"
    ]
  },
  
  "trading_signal_generated": true,
  "signal_id": "SIG-20251221-045"
}
```

## Examples

**Example 1**: FDA Approval (위 예시)

**Example 2**: Negative News (Lawsuit)
```
News: "Tesla faces $10B lawsuit over Autopilot defects"

Stage 1:
- 직접 영향: 법적 비용 + 브랜드 이미지 타격
- 재무 영향: 최악 $10B (unlikely), 현실적 $1-2B settlement
- Impact Score: 0.6 (MEDIUM-HIGH)

Stage 2:
- 경쟁사: GM, F → POSITIVE (Tesla 약점 부각)
- 규제: 자율주행 규제 강화 가능성 → 전체 섹터 NEGATIVE
- 공급망: Neutral

Stage 3:
- Action: SELL (short-term), HOLD (long-term)
- Confidence: 0.70
- Short-term: 부정적 sentiment 주가 압박 예상
- Long-term: Tesla 브랜드 파워로 회복 가능
```

## Guidelines

### Do's ✅
- **깊이 우선**: 속도보다 정확성과 깊이
- **3단계 엄격 준수**: 각 Stage 명확히 구분
- **Related Tickers 포함**: 2차 영향 분석 필수
- **시나리오 분석**: Alternative scenarios 제시

### Don'ts ❌
- 단계 건너뛰기 금지
- 표면적 분석 금지 (Quick Analyzer와 차별화)
- Related tickers 누락 금지
- Risk factors 생략 금지

## Integration

### API Endpoint

```python
@router.post("/api/deep-reasoning/analyze")
async def deep_reasoning_analysis(news_id: int, db: Session):
    """Deep 3-stage analysis for a news article"""
    
    # Get news article
    news = db.query(NewsArticle).filter_by(id=news_id).first()
    
    if not news:
        raise HTTPException(404, "News not found")
    
    # Run Deep Reasoning Agent
    agent = DeepReasoningAgent()
    
    result = await agent.execute({
        'news_id': news_id,
        'ticker': news.ticker,
        'headline': news.headline,
        'content': news.content
    })
    
    # Generate trading signal
    if result['stage3_conclusion']['action'] in ['BUY', 'SELL']:
        create_trading_signal(
            ticker=news.ticker,
            action=result['stage3_conclusion']['action'],
            confidence=result['stage3_conclusion']['confidence'],
            source='deep_reasoning',
            reasoning=result['stage3_conclusion']['reasoning'],
            metadata=result
        )
    
    return result
```

## Performance Metrics

- **Analysis Time**: 평균 20-30초 (깊이 우선)
- **Accuracy**: 목표 > 75% (Quick Analyzer 60% 대비 높음)
- **Related Tickers Recall**: > 90% (주요 영향 티커 포착)
- **User Satisfaction**: > 4.5/5 (깊이감)

## Comparison

| Agent | Speed | Depth | Accuracy | Use Case |
|-------|-------|-------|----------|----------|
| Quick Analyzer | 5초 | ⭐ | 60% | 빠른 확인 |
| Deep Reasoning | 30초 | ⭐⭐⭐ | 75% | 중요한 결정 |
| War Room | 15초 | ⭐⭐ | 65% | 합의 기반 |

## Version History

- **v1.0** (2025-12-21): Initial release with 3-stage Chain of Thought methodology
