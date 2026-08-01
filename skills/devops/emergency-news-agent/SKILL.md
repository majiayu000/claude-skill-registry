---
name: emergency-news-agent
description: Real-time breaking news monitor using Grounding API. Continuously scans for market-moving events, classifies urgency (CRITICAL/HIGH/MEDIUM), and triggers immediate alerts to War Room and Notification Agent. Optimized for speed and recall.
license: Proprietary
compatibility: Requires Grounding API, NewsArticle database, notification system, War Room integration
metadata:
  author: ai-trading-system
  version: "1.0"
  category: analysis
  agent_role: emergency_monitor
---

# Emergency News Agent - 긴급 뉴스 모니터

## Role
**Grounding API**를 활용하여 시장 영향력이 큰 긴급 뉴스를 실시간 감지하고 즉각 알림합니다.

## Core Capabilities

### 1. Grounding API Integration

```python
from anthropic import Anthropic

anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

async def monitor_breaking_news(query: str) -> List[Dict]:
    """Monitor breaking news using Grounding API"""
    
    message = anthropic.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": query
        }],
        tools=[{
            "type": "web_search_20241022",
            "name": "web_search",
            "search_query": "breaking market news stock",
            "max_results": 10
        }]
    )
    
    # Parse results
    search_results = extract_search_results(message)
    
    return search_results
```

### 2. Urgency Classification

```python
def classify_urgency(news: Dict) -> str:
    """Classify news urgency based on content"""
    
    # CRITICAL keywords
    critical_keywords = [
        "halt", "suspended", "emergency",
        "bankruptcy", "sec investigation",
        "fda rejection", "recalls"
    ]
    
    # HIGH keywords
    high_keywords = [
        "acquisition", "merger",
        "earnings miss", "guidance cut",
        "ceo resignation", "lawsuit"
    ]
    
    # MEDIUM keywords
    medium_keywords = [
        "partnership", "new product",
        "analyst upgrade", "contract win"
    ]
    
    headline = news['headline'].lower()
    content = news.get('content', '').lower()
    text = headline + ' ' + content
    
    # Check CRITICAL
    if any(kw in text for kw in critical_keywords):
        return "CRITICAL"
    
    # Check HIGH
    if any(kw in text for kw in high_keywords):
        return "HIGH"
    
    # Check MEDIUM
    if any(kw in text for kw in medium_keywords):
        return "MEDIUM"
    
    return "LOW"
```

### 3. Ticker Extraction

```python
import re

def extract_tickers(text: str) -> List[str]:
    """Extract stock tickers from text"""
    
    # Common patterns
    patterns = [
        r'\b([A-Z]{1,5})\b',  # All caps 1-5 letters
        r'\$([A-Z]{1,5})\b',  # $AAPL format
        r'NYSE:\s*([A-Z]{1,5})',  # NYSE: AAPL
        r'NASDAQ:\s*([A-Z]{1,5})'  # NASDAQ: AAPL
    ]
    
    tickers = set()
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        tickers.update(matches)
    
    # Filter out common false positives
    false_positives = {'CEO', 'FDA', 'SEC', 'USA', 'IPO', 'ETF'}
    tickers = tickers - false_positives
    
    # Validate against known tickers
    valid_tickers = [t for t in tickers if is_valid_ticker(t)]
    
    return valid_tickers
```

### 4. Impact Assessment

```python
def assess_impact(
    urgency: str,
    ticker: str,
    news_type: str
) -> Dict:
    """Assess potential market impact"""
    
    # Base impact by urgency
    BASE_IMPACT = {
        "CRITICAL": 0.15,    # ±15%
        "HIGH": 0.08,        # ±8%
        "MEDIUM": 0.03,      # ±3%
        "LOW": 0.01          # ±1%
    }
    
    # News type multiplier
    TYPE_MULTIPLIER = {
        "fda_approval": 1.5,
        "fda_rejection": 1.8,
        "bankruptcy": 2.0,
        "merger": 1.3,
        "earnings": 1.0,
        "partnership": 0.8
    }
    
    base = BASE_IMPACT[urgency]
    multiplier = TYPE_MULTIPLIER.get(news_type, 1.0)
    
    estimated_impact = base * multiplier
    
    # Determine direction
    direction = infer_direction(news_type)
    
    return {
        "estimated_price_impact": estimated_impact,
        "direction": direction,  # POSITIVE/NEGATIVE
        "confidence": 0.6,
        "timeframe": "immediate" if urgency == "CRITICAL" else "short_term"
    }
```

### 5. Alert Triggering

```python
async def trigger_alert(news: Dict, urgency: str):
    """Trigger appropriate alerts based on urgency"""
    
    if urgency == "CRITICAL":
        # Immediate actions
        await send_telegram_alert(news, priority="URGENT")
        await notify_war_room(news)
        await broadcast_websocket(news)
        
        # Auto-trigger War Room debate
        if news.get('tickers'):
            for ticker in news['tickers']:
                await initiate_emergency_debate(ticker, news)
    
    elif urgency == "HIGH":
        await send_telegram_alert(news, priority="HIGH")
        await broadcast_websocket(news)
    
    elif urgency == "MEDIUM":
        await broadcast_websocket(news)
    
    # Always save to database
    save_emergency_news(news)
```

## Decision Framework

```
Step 1: Continuous Monitoring (Every 60 seconds)
  search_query = "breaking stock market news"
  
  results = grounding_api.search(
    query=search_query,
    recency="1_hour",
    max_results=10
  )

Step 2: Filter New Articles
  FOR each result in results:
    IF not exists_in_db(result.url):
      new_articles.append(result)

Step 3: Classify Urgency
  FOR article in new_articles:
    urgency = classify_urgency(article)
    
    IF urgency == "LOW":
      SKIP (not market-moving)

Step 4: Extract Tickers
  tickers = extract_tickers(article.content)
  
  IF len(tickers) == 0:
    tickers = ["SPY"]  # Market-wide news

Step 5: Assess Impact
  FOR ticker in tickers:
    impact = assess_impact(urgency, ticker, news_type)

Step 6: Create NewsArticle Entry
  article_entry = NewsArticle(
    ticker=ticker,
    headline=article.headline,
    content=article.content,
    source="emergency_news",
    urgency=urgency,
    sentiment_score=calculate_sentiment(article),
    created_at=datetime.now()
  )
  
  db.add(article_entry)

Step 7: Trigger Alerts
  await trigger_alert(article, urgency)

Step 8: IF CRITICAL:
  # Auto-initiate War Room debate
  await initiate_emergency_debate(ticker, article)
```

## Output Format

```json
{
  "alert_id": "EMERG-20251221-001",
  "timestamp": "2025-12-21T13:05:23Z",
  "urgency": "CRITICAL",
  "detection_latency_sec": 45,
  
  "news_details": {
    "headline": "FDA Rejects Moderna Cancer Vaccine - Major Setback",
    "summary": "FDA citing safety concerns in Phase 3 trial data. Moderna stock halted.",
    "source": "Reuters",
    "url": "https://reuters.com/article/...",
    "published_at": "2025-12-21T13:04:38Z"
  },
  
  "affected_tickers": [
    {
      "ticker": "MRNA",
      "relationship": "primary",
      "impact_assessment": {
        "estimated_price_impact": -0.27,
        "direction": "NEGATIVE",
        "confidence": 0.85,
        "timeframe": "immediate",
        "reasoning": "FDA 거부는 신약 파이프라인 붕괴, 역사적으로 -20~-30% 급락"
      }
    },
    {
      "ticker": "PFE",
      "relationship": "competitor",
      "impact_assessment": {
        "estimated_price_impact": 0.08,
        "direction": "POSITIVE",
        "confidence": 0.60,
        "timeframe": "short_term",
        "reasoning": "경쟁사 Moderna 약세는 PFE에 긍정적"
      }
    }
  ],
  
  "urgency_classification": {
    "level": "CRITICAL",
    "confidence": 0.95,
    "reasoning": "FDA rejection + trading halt = 시장 즉각 반응",
    "keywords_matched": ["fda rejection", "halted", "safety concerns"]
  },
  
  "actions_taken": [
    {
      "action": "telegram_alert_sent",
      "recipient": "COMMANDER",
      "timestamp": "2025-12-21T13:05:25Z",
      "priority": "URGENT"
    },
    {
      "action": "war_room_debate_initiated",
      "ticker": "MRNA",
      "timestamp": "2025-12-21T13:05:26Z"
    },
    {
      "action": "websocket_broadcast",
      "connections_notified": 5,
      "timestamp": "2025-12-21T13:05:24Z"
    },
    {
      "action": "database_entry_created",
      "news_id": 1024,
      "timestamp": "2025-12-21T13:05:23Z"
    }
  ],
  
  "recommended_actions": [
    "Review MRNA positions immediately",
    "Consider PFE as alternative",
    "Monitor for official company response"
  ]
}
```

## Examples

**Example 1**: CRITICAL - Trading Halt
```
Detected: "Tesla trading halted pending SEC investigation"

Actions:
1. TELEGRAM → Commander (URGENT)
2. War Room → Emergency debate on TSLA
3. WebSocket → All connected clients
4. Database → Save with urgency=CRITICAL

Expected Impact: -15% to -25%
```

**Example 2**: HIGH - Major Acquisition
```
Detected: "Microsoft to acquire OpenAI for $80B"

Actions:
1. TELEGRAM → Commander (HIGH priority)
2. WebSocket → Broadcast
3. Database → Save with urgency=HIGH

Expected Impact: MSFT +8%, GOOGL -3%
```

**Example 3**: MEDIUM - Partnership
```
Detected: "Apple partners with Samsung on chip development"

Actions:
1. WebSocket → Broadcast
2. Database → Save with urgency=MEDIUM

Expected Impact: AAPL +2%, Samsung +1%
```

## Guidelines

### Do's ✅
- **속도 최우선**: Detection latency < 2분
- **False Positive 허용**: 놓치는 것보다 나음 (Recall > Precision)
- **즉각 알림**: CRITICAL은 모든 채널 동시 알림
- **War Room 자동 촉발**: CRITICAL 뉴스는 자동 debate

### Don'ts ❌
- 과도한 필터링 금지 (중요 뉴스 놓칠 위험)
- Grounding API 남용 금지 (rate limit 준수)
- CRITICAL 남발 금지 (신뢰도 유지)
- Latency > 5분 금지 (긴급성 손실)

## Integration

### Continuous Monitoring Loop

```python
import asyncio

async def emergency_news_monitor():
    """Continuous monitoring loop"""
    
    logger.info("Emergency News Monitor started")
    
    while True:
        try:
            # Search for breaking news
            results = await monitor_breaking_news(
                query="breaking stock market news OR urgent company announcement"
            )
            
            # Process results
            for result in results:
                # Check if already processed
                if not is_duplicate(result):
                    await process_emergency_news(result)
            
            # Sleep for 60 seconds
            await asyncio.sleep(60)
        
        except Exception as e:
            logger.error(f"Emergency monitor error: {e}")
            await asyncio.sleep(10)  # Shorter retry on error
```

### Startup Integration

```python
# backend/main.py

from backend.ai.skills.analysis.emergency_news_agent import emergency_news_monitor

@app.on_event("startup")
async def startup_event():
    # Start emergency news monitor in background
    asyncio.create_task(emergency_news_monitor())
    logger.info("Emergency News Agent activated")
```

### War Room Auto-Trigger

```python
async def initiate_emergency_debate(ticker: str, news: Dict):
    """Auto-trigger War Room debate for critical news"""
    
    from backend.ai.debate.ai_debate_engine import AIDebateEngine
    
    debate_engine = AIDebateEngine()
    
    # Run emergency debate
    result = await debate_engine.run_debate(
        ticker=ticker,
        emergency_mode=True,
        context={
            "news_headline": news['headline'],
            "urgency": "CRITICAL",
            "detection_time": datetime.now()
        }
    )
    
    # Send result to Commander
    await send_telegram_message(
        f"🚨 Emergency Debate Result for {ticker}\n\n"
        f"Decision: {result['final_decision']}\n"
        f"Confidence: {result['final_confidence']:.0%}\n"
        f"News: {news['headline']}"
    )
```

## Performance Metrics

- **Detection Latency**: 목표 < 2분 (뉴스 발생 → 알림)
- **Recall**: > 95% (중요 뉴스 놓치지 않기)
- **Precision**: > 60% (False positive 허용)
- **Uptime**: > 99.9% (24/7 모니터링)

## Alert Examples

### Telegram Alert Format

```
🚨 CRITICAL ALERT 🚨

Ticker: MRNA
Impact: -27% (immediate)

FDA REJECTS CANCER VACCINE

Summary: FDA citing safety concerns. 
Trading halted.

Actions Taken:
✅ War Room debate initiated
✅ All systems notified

Recommendation: Review positions NOW

Time: 13:05:23 UTC
Latency: 45 seconds
```

## Version History

- **v1.0** (2025-12-21): Initial release with Grounding API and auto-alert system
