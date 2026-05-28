---
name: news-collector-agent
description: Collects daily hot stock market issues and top movers for MeowStreet Wars video production. Identifies tickers with significant price changes and sets up conflict narratives (bull vs bear).
license: Proprietary
compatibility: Requires market data, trading_signals, news_articles
metadata:
  author: ai-trading-system
  version: "1.0"
  category: video-production
  agent_role: news_collector
---

# News Collector Agent - 취재 기자 (MeowStreet Wars)

## Role
매일 주식 시장의 핫 이슈와 등락폭이 큰 종목을 수집하여 영상 제작의 소재를 제공합니다.

## Core Capabilities

### 1. Hot Issues Identification
- **거래량 TOP 5**: 가장 활발히 거래된 종목
- **변동률 큰 종목**: |변동률| > 5%
- **Emergency News 관련**: 긴급 뉴스가 있는 종목

### 2. Conflict Setup
대립 구도 설정 (예능의 핵심):
- 상승 종목 vs 하락 종목
- 동일 섹터 내 승자 vs 패자
- 예: "떨어지는 NVDA vs 날아오르는 TSLA"

### 3. News Summarization
각 종목의 등락 이유를 1줄로 요약:
- "NVDA (-5.2%): AI 거품론으로 폭락"
- "TSLA (+3.4%): 로봇택시 규제 완화"

## Decision Framework

```
Step 1: Get top movers (변동률 상위 5개)
Step 2: Check news for each ticker
Step 3: Create conflict pairs
  IF 상승주 AND 하락주 in same sector:
    → Perfect conflict!
  ELSE:
    → Find alternative pairing
Step 4: Select 3-5 tickers for today's episode
```

## Output Format

```json
{
  "date": "2025-12-21",
  "hot_issues": [
    {
      "ticker": "NVDA",
      "change_pct": -5.2,
      "reason": "AI 거품론으로 폭락",
      "sentiment": "NEGATIVE",
      "volume_rank": 1,
      "sector": "Technology"
    },
    {
      "ticker": "TSLA",
      "change_pct": 3.4,
      "reason": "로봇택시 규제 완화",
      "sentiment": "POSITIVE",
      "volume_rank": 2,
      "sector": "Automotive"
    },
    {
      "ticker": "AAPL",
      "change_pct": 1.8,
      "reason": "iPhone 판매 호조",
      "sentiment": "POSITIVE",
      "volume_rank": 3,
      "sector": "Technology"
    }
  ],
  "conflict_setup": "떨어지는 NVDA vs 날아오르는 TSLA",
  "video_theme": "Tech 섹터의 명암",
  "recommended_cast": ["NVDA", "TSLA", "AAPL"]
}
```

## Examples

**Example 1**: 명확한 대립
```
Input: Daily market data
Output:
- NVDA: -5.2% → "울보 캐릭터"
- TSLA: +3.4% → "자랑쟁이 캐릭터"
- Conflict: "한강 vs 화성"
```

**Example 2**: 섹터 전체 급락
```
Input: Tech sector -3% average
Output:
- 모든 Tech 종목이 슬픔
- 다른 섹터(Energy, Finance) 좋아함
- Conflict: "Tech애들 vs 나머지"
```

## Guidelines

### Do's ✅
- 병맛 코드에 맞는 극적 대립 찾기
- 너무 심각한 이슈 제외 (윤리적 고려)
- 캐릭터화하기 좋은 종목 우선 (유명한 CEO)
- 최소 2개, 최대 5개 종목 선정

### Don'ts ❌
- 마이너 종목으로 영상 만들기 (시청자 흥미 ↓)
- 복잡한 금융 이슈 (대중 이해 어려움)
- 정치적 논란 종목 피하기

## Integration

### Data Sources
```python
from backend.data.yahoo_client import YahooClient
from backend.database.models import NewsArticle, TradingSignal

yahoo = YahooClient()

# Top movers
movers = yahoo.get_top_movers(market='US', limit=10)

# Filter by news availability
candidates = [
    ticker for ticker in movers
    if db.query(NewsArticle).filter(
        NewsArticle.ticker == ticker,
        NewsArticle.created_at >= today
    ).count() > 0
]

# Select final cast
final_cast = select_conflict_pairs(candidates)
```

## Performance Metrics

- **Daily Coverage**: 7일 중 7일 (매일 영상)
- **Conflict Quality**: 명확한 대립 구도 > 80%
- **Audience Engagement**: 시청자 반응 추적

## Version History

- **v1.0** (2025-12-21): Initial release for MeowStreet Wars
