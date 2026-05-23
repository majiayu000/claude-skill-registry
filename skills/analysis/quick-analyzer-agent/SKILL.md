---
name: quick-analyzer-agent
description: Fast ticker analysis for /analysis page. Provides quick BUY/SELL/HOLD recommendations based on technical indicators, recent news, and basic fundamentals within seconds. Optimized for speed over depth.
license: Proprietary
compatibility: Requires market data (OHLCV), news_articles table, basic financial data
metadata:
  author: ai-trading-system
  version: "1.0"
  category: analysis
  agent_role: quick_analyst
---

# Quick Analyzer Agent - 빠른 티커 분석

## Role
`/analysis` 페이지에서 사용자가 티커를 입력하면 **5초 이내**에 BUY/SELL/HOLD 추천을 제공합니다. 속도를 위해 핵심 지표만 분석합니다.

## Core Capabilities

### 1. Fast Technical Analysis

#### Price Action
- **Moving Averages**: MA20, MA50 교차 확인
- **Trend**: 상승/하락/횡보 판단
- **Support/Resistance**: 주요 가격대

#### Momentum Indicators
- **RSI (14일)**: 과매수(>70), 과매도(<30) 
- **MACD**: 골든크로스/데드크로스
- **Volume**: 거래량 증가/감소 패턴

### 2. Recent News Scan (Last 7 Days)

```python
# News sentiment aggregation
news_articles = get_recent_news(ticker, days=7)

avg_sentiment = sum(a.sentiment_score for a in news_articles) / len(news_articles)

positive_ratio = len([a for a in news_articles if a.sentiment_score > 0.3]) / len(news_articles)
```

#### News Signals
- **Very Positive** (avg > 0.6): 강한 호재
- **Positive** (avg > 0.3): 긍정적
- **Neutral** (avg -0.3 to 0.3): 중립
- **Negative** (avg < -0.3): 부정적
- **Very Negative** (avg < -0.6): 강한 악재

### 3. Basic Fundamental Check

#### Valuation
- **P/E Ratio**: 현재 vs 업종 평균
- **P/B Ratio**: 자산 가치 대비
- **Quick Check**: 과대/적정/저평가

#### Recent Earnings
- **Beat/Miss**: 최근 분기 실적
- **Surprise %**: 컨센서스 대비

## Decision Framework

```
Step 1: Technical Analysis
  score_technical = 0
  
  IF MA20 > MA50:
    score_technical += 2
  
  IF RSI in [30, 70]:
    score_technical += 1
  ELIF RSI < 30:
    score_technical += 3  # Oversold
  ELIF RSI > 70:
    score_technical -= 3  # Overbought
  
  IF Volume > avg_volume * 1.5:
    score_technical += 1

Step 2: News Analysis
  score_news = 0
  
  IF avg_sentiment > 0.6:
    score_news += 3
  ELIF avg_sentiment > 0.3:
    score_news += 2
  ELIF avg_sentiment < -0.3:
    score_news -= 2
  ELIF avg_sentiment < -0.6:
    score_news -= 3

Step 3: Fundamental Check
  score_fundamental = 0
  
  IF P/E < industry_avg * 0.8:
    score_fundamental += 2  # Undervalued
  ELIF P/E > industry_avg * 1.2:
    score_fundamental -= 2  # Overvalued
  
  IF recent_earnings == 'BEAT':
    score_fundamental += 2

Step 4: Final Decision
  total_score = score_technical + score_news + score_fundamental
  
  IF total_score >= 5:
    action = "BUY"
    confidence = min(0.9, 0.6 + total_score * 0.05)
  
  ELIF total_score <= -5:
    action = "SELL"
    confidence = min(0.9, 0.6 + abs(total_score) * 0.05)
  
  ELSE:
    action = "HOLD"
    confidence = 0.5 + abs(total_score) * 0.03
```

## Output Format

```json
{
  "ticker": "AAPL",
  "action": "BUY",
  "confidence": 0.75,
  "reasoning": "기술적 골든크로스 (MA20 > MA50), 최근 뉴스 긍정적 (sentiment +0.6), 업종 대비 저평가 (P/E 25 vs 28)",
  "analysis_time_ms": 3200,
  "price_info": {
    "current": 197.50,
    "change_1d_pct": 0.024,
    "change_1w_pct": 0.058,
    "ma20": 195.00,
    "ma50": 192.00,
    "ma200": 185.00,
    "support_level": 190.00,
    "resistance_level": 205.00
  },
  "technical_indicators": {
    "rsi_14": 58,
    "rsi_signal": "NEUTRAL",
    "macd_signal": "BULLISH",
    "volume_change_pct": 0.35,
    "trend": "UPTREND"
  },
  "technical_summary": "BULLISH",
  "technical_score": 6,
  "news_analysis": {
    "total_articles_7d": 9,
    "avg_sentiment": 0.62,
    "positive_count": 7,
    "negative_count": 2,
    "sentiment_label": "VERY_POSITIVE",
    "top_headlines": [
      "Apple reports record iPhone sales",
      "New AI features boost user engagement"
    ]
  },
  "news_summary": "7 positive, 2 negative (last 7d)",
  "news_score": 3,
  "fundamental_analysis": {
    "pe_ratio": 25.3,
    "industry_avg_pe": 28.0,
    "pe_relative": 0.904,
    "valuation": "UNDERVALUED",
    "pb_ratio": 42.5,
    "recent_earnings": "BEAT",
    "earnings_surprise_pct": 0.125
  },
  "fundamental_summary": "P/E 25 (industry avg 28) - undervalued, recent earnings beat 12.5%",
  "fundamental_score": 4,
  "total_score": 13,
  "risk_factors": [
    "Potential profit-taking at resistance $205",
    "Tech sector rotation risk"
  ],
  "next_review_date": "2025-12-28"
}
```

## Examples

**Example 1**: Strong BUY Signal
```
Input:
- Ticker: NVDA
- Price: $520
- MA20: $510, MA50: $490 (골든크로스)
- RSI: 55
- News: 8 positive, 1 negative (avg +0.7)
- P/E: 45 (industry 52) - 저평가
- Recent Earnings: Beat 15%

Calculation:
- Technical Score: +6 (MA골든+2, RSI중립+1, Volume+1, Trend+2)
- News Score: +3 (매우 긍정)
- Fundamental Score: +4 (저평가+2, Beat+2)
- Total: 13

Output:
- Action: BUY
- Confidence: 0.85
- Reasoning: "강한 기술적 신호 + 긍정적 뉴스 + 저평가"
```

**Example 2**: SELL Signal
```
Input:
- Ticker: XYZ
- MA20 < MA50 (데드크로스)
- RSI: 78 (과매수)
- News: 2 positive, 7 negative (avg -0.5)
- P/E: 85 (industry 40) - 고평가

Calculation:
- Technical Score: -4 (데드크로스-2, 과매수-3, 정상볼륨+1)
- News Score: -2 (부정)
- Fundamental Score: -2 (고평가)
- Total: -8

Output:
- Action: SELL
- Confidence: 0.80
- Reasoning: "기술적 약세 + 부정 뉴스 + 고평가"
```

**Example 3**: HOLD Signal
```
Input:
- Ticker: MSFT
- MA20 ≈ MA50 (횡보)
- RSI: 52
- News: 4 positive, 3 negative (avg +0.1)
- P/E: 30 (industry 30) - 적정

Calculation:
- Technical Score: +1
- News Score: 0
- Fundamental Score: 0
- Total: 1

Output:
- Action: HOLD
- Confidence: 0.55
- Reasoning: "명확한 방향성 부재, 관망 추천"
```

## Guidelines

### Do's ✅
- **Speed First**: 5초 이내 응답 (복잡한 분석 지양)
- **핵심 지표만**: RSI, MA, P/E, News Sentiment
- **명확한 신호**: 강한 BUY/SELL만, 애매하면 HOLD
- **Risk Factors 포함**: 주요 리스크 1-2개 언급

### Don'ts ❌
- 과도한 분석 금지 (Deep Reasoning Agent 역할 아님)
- 복잡한 모델 사용 금지 (속도 저하)
- 모호한 표현 금지 ("maybe", "possibly")
- 100% 확신 금지 (confidence 최대 0.90)

## Integration

### API Endpoint

```python
from fastapi import APIRouter, HTTPException
from backend.ai.skills.base_agent import AnalysisSkillAgent

router = APIRouter()

@router.get("/api/analysis/quick/{ticker}")
async def quick_analyze_ticker(ticker: str):
    """Quick analysis for a ticker"""
    
    try:
        agent = QuickAnalyzerAgent()
        
        result = await agent.execute({
            'ticker': ticker,
            'task_description': f'Provide quick analysis for {ticker}'
        })
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Data Sources

```python
from backend.data.yahoo_client import YahooClient
from backend.database.models import NewsArticle
from sqlalchemy.orm import Session

async def gather_quick_data(ticker: str, db: Session) -> Dict:
    """Gather data for quick analysis"""
    
    yahoo = YahooClient()
    
    # Price data
    price_data = yahoo.get_current_price(ticker)
    
    # Technical indicators
    tech_data = yahoo.get_technical_indicators(ticker)
    
    # News (last 7 days)
    news = db.query(NewsArticle).filter(
        NewsArticle.ticker == ticker,
        NewsArticle.created_at >= datetime.now() - timedelta(days=7)
    ).all()
    
    # Basic fundamentals
    fundamentals = yahoo.get_key_stats(ticker)
    
    return {
        'price': price_data,
        'technical': tech_data,
        'news': news,
        'fundamentals': fundamentals
    }
```

## Performance Metrics

- **Response Time**: 목표 < 5초 (평균 3초)
- **Accuracy**: > 60% (빠른 분석이므로 Deep Reasoning보다 낮음)
- **User Satisfaction**: > 4/5 (속도 중요)
- **Cache Hit Rate**: > 70% (동일 ticker 5분 내 재조회 시)

## Caching Strategy

```python
from functools import lru_cache
from time import time

# 5분 TTL cache
@lru_cache(maxsize=100)
def cached_quick_analysis(ticker: str, timestamp: int) -> Dict:
    """Cache analysis for 5 minutes"""
    # timestamp rounded to 5 minutes
    return perform_quick_analysis(ticker)

# Usage
current_5min_slot = int(time() // 300)
result = cached_quick_analysis(ticker, current_5min_slot)
```

## Comparison with Other Agents

| Agent | Speed | Depth | Use Case |
|-------|-------|-------|----------|
| Quick Analyzer | ⭐⭐⭐ 5s | ⭐ Basic | 빠른 확인 |
| Deep Reasoning | ⭐ 30s | ⭐⭐⭐ Deep | 중요한 결정 |
| War Room | ⭐⭐ 15s | ⭐⭐ Medium | 합의 기반 |

## Version History

- **v1.0** (2025-12-21): Initial release with 5-second target response time
