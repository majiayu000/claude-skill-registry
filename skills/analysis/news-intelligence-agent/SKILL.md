---
name: news-intelligence-agent
description: Batch news analyzer for /news page. Processes multiple news articles simultaneously, extracting sentiment, keywords, themes, and ticker mentions. Generates aggregated market intelligence including trending topics and ticker buzz scores.
license: Proprietary
compatibility: Requires news_articles table, NLP sentiment analysis, keyword extraction, theme clustering
metadata:
  author: ai-trading-system
  version: "1.0"
  category: analysis
  agent_role: news_intel
---

# News Intelligence Agent - 뉴스 인텔리전스

## Role
`/news` 페이지에서 **배치**로 여러 뉴스를 동시 분석하여 시장 전체 흐름을 파악합니다.

## Core Capabilities

### 1. Batch News Processing

```python
async def analyze_batch(
    news_articles: List[NewsArticle],
    batch_size: int = 50
) -> Dict:
    """Process multiple articles in parallel"""
    
    results = []
    
    # Process in batches to avoid API rate limits
    for i in range(0, len(news_articles), batch_size):
        batch = news_articles[i:i+batch_size]
        
        # Parallel processing
        batch_results = await asyncio.gather(*[
            analyze_single_article(article)
            for article in batch
        ])
        
        results.extend(batch_results)
    
    return aggregate_batch_results(results)
```

### 2. Sentiment Analysis

#### Sentiment Scoring
```python
def calculate_sentiment(text: str) -> float:
    """Calculate sentiment score -1 to +1"""
    
    # Positive keywords
    positive = ["surge", "beat", "record", "growth", "bullish", "upgrade"]
    
    # Negative keywords
    negative = ["plunge", "miss", "loss", "decline", "bearish", "downgrade"]
    
    # Count occurrences
    pos_count = sum(text.lower().count(word) for word in positive)
    neg_count = sum(text.lower().count(word) for word in negative)
    
    # Normalize
    total = pos_count + neg_count
    if total == 0:
        return 0.0
    
    sentiment = (pos_count - neg_count) /total
    
    # Clamp to [-1, 1]
    return max(-1.0, min(1.0, sentiment))
```

#### Sentiment Categories
```python
SENTIMENT_LEVELS = {
    "VERY_POSITIVE": (0.6, 1.0),
    "POSITIVE": (0.3, 0.6),
    "NEUTRAL": (-0.3, 0.3),
    "NEGATIVE": (-0.6, -0.3),
    "VERY_NEGATIVE": (-1.0, -0.6)
}
```

### 3. Keyword Extraction

```python
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(texts: List[str], top_n: int = 10) -> List[str]:
    """Extract important keywords using TF-IDF"""
    
    vectorizer = TfidfVectorizer(
        max_features=top_n,
        stop_words='english',
        ngram_range=(1, 2)  # Unigrams and bigrams
    )
    
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    feature_names = vectorizer.get_feature_names_out()
    
    # Get top keywords
    scores = tfidf_matrix.sum(axis=0).A1
    top_indices = scores.argsort()[-top_n:][::-1]
    
    keywords = [feature_names[i] for i in top_indices]
    
    return keywords
```

### 4. Theme Detection

```python
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def detect_themes(articles: List[str], n_themes: int = 5) -> List[Dict]:
    """Cluster articles into themes"""
    
    # Vectorize
    vectorizer = TfidfVectorizer(max_features=100, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(articles)
    
    # Cluster
    kmeans = KMeans(n_clusters=n_themes, random_state=42)
    kmeans.fit(tfidf_matrix)
    
    # Extract theme keywords
    themes = []
    feature_names = vectorizer.get_feature_names_out()
    
    for i, cluster_center in enumerate(kmeans.cluster_centers_):
        top_indices = cluster_center.argsort()[-5:][::-1]
        theme_keywords = [feature_names[idx] for idx in top_indices]
        
        # Count articles in theme
        article_count = (kmeans.labels_ == i).sum()
        
        themes.append({
            "theme_id": i,
            "keywords": theme_keywords,
            "article_count": article_count,
            "theme_name": generate_theme_name(theme_keywords)
        })
    
    return sorted(themes, key=lambda x: x['article_count'], reverse=True)
```

### 5. Ticker Buzz Score

```python
def calculate_ticker_buzz(
    ticker: str,
    news_articles: List[NewsArticle],
    timeframe_hours: int = 24
) -> Dict:
    """Calculate how much a ticker is being discussed"""
    
    # Filter articles mentioning ticker
    ticker_articles = [
        a for a in news_articles
        if ticker in (a.ticker or '') or ticker in (a.content or '').upper()
    ]
    
    # Recency weight (more recent = higher weight)
    now = datetime.now()
    weighted_mentions = 0
    
    for article in ticker_articles:
        hours_ago = (now - article.created_at).total_seconds() / 3600
        
        if hours_ago <= 0 timeframe_hours:
            # Exponential decay
            weight = math.exp(-hours_ago / (timeframe_hours / 2))
            weighted_mentions += weight
    
    # Normalize to 0-100 scale
    buzz_score = min(100, weighted_mentions * 10)
    
    # Sentiment breakdown
    sentiments = [a.sentiment_score for a in ticker_articles if a.sentiment_score]
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    
    return {
        "ticker": ticker,
        "buzz_score": buzz_score,
        "mention_count": len(ticker_articles),
        "avg_sentiment": avg_sentiment,
        "timeframe_hours": timeframe_hours,
        "trending": "UP" if buzz_score > 50 else "NORMAL"
    }
```

## Decision Framework

```
Step 1: Fetch News Articles
  articles = db.query(NewsArticle).filter(
    NewsArticle.created_at >= datetime.now() - timedelta(hours=24)
  ).all()

Step 2: Batch Sentiment Analysis
  FOR each article in articles:
    sentiment = calculate_sentiment(article.content)
    article.sentiment_score = sentiment
    article.sentiment_label = categorize_sentiment(sentiment)

Step 3: Extract Keywords
  all_text = [a.content for a in articles]
  keywords = extract_keywords(all_text, top_n=20)

Step 4: Detect Themes
  themes = detect_themes([a.headline + ' ' + a.content for a in articles])

Step 5: Calculate Ticker Buzz
  unique_tickers = set(a.ticker for a in articles if a.ticker)
  
  buzz_scores = {}
  FOR ticker in unique_tickers:
    buzz_scores[ticker] = calculate_ticker_buzz(ticker, articles)

Step 6: Aggregate Results
  return {
    "total_articles": len(articles),
    "sentiment_distribution": count_by_sentiment(articles),
    "top_keywords": keywords,
    "trending_themes": themes,
    "ticker_buzz": buzz_scores,
    "timestamp": datetime.now()
  }
```

## Output Format

```json
{
  "analysis_timestamp": "2025-12-21T13:00:00Z",
  "timeframe": "last_24_hours",
  "total_articles_analyzed": 237,
  
  "sentiment_distribution": {
    "VERY_POSITIVE": 45,
    "POSITIVE": 89,
    "NEUTRAL": 67,
    "NEGATIVE": 28,
    "VERY_NEGATIVE": 8
  },
  
  "market_sentiment_summary": {
    "overall_score": 0.32,
    "overall_label": "POSITIVE",
    "confidence": 0.85,
    "interpretation": "시장 전반적으로 긍정적 뉴스 우세"
  },
  
  "top_keywords": [
    {
      "keyword": "ai growth",
      "frequency": 67,
      "importance_score": 0.92
    },
    {
      "keyword": "earnings beat",
      "frequency": 54,
      "importance_score": 0.88
    },
    {
      "keyword": "fed rate",
      "frequency": 48,
      "importance_score": 0.85
    },
    {
      "keyword": "semiconductor",
      "frequency": 42,
      "importance_score": 0.80
    },
    {
      "keyword": "tech rally",
      "frequency": 38,
      "importance_score": 0.75
    }
  ],
  
  "trending_themes": [
    {
      "theme_id": 0,
      "theme_name": "AI 붐",
      "keywords": ["ai", "chip", "nvidia", "demand", "growth"],
      "article_count": 78,
      "avg_sentiment": 0.68,
      "interpretation": "AI 관련 긍정적 뉴스 주도"
    },
    {
      "theme_id": 1,
      "theme_name": "Fed 금리 논의",
      "keywords": ["fed", "rate", "inflation", "policy", "powell"],
      "article_count": 56,
      "avg_sentiment": 0.12,
      "interpretation": "금리 관련 중립적 논의"
    },
    {
      "theme_id": 2,
      "theme_name": "실적 시즌",
      "keywords": ["earnings", "beat", "guidance", "revenue", "profit"],
      "article_count": 43,
      "avg_sentiment": 0.45,
      "interpretation": "실적 호조 뉴스 다수"
    }
  ],
  
  "ticker_buzz_rankings": [
    {
      "rank": 1,
      "ticker": "NVDA",
      "buzz_score": 92,
      "mention_count": 45,
      "avg_sentiment": 0.75,
      "trending": "UP",
      "summary": "AI 수요 급증 관련 압도적 언급"
    },
    {
      "rank": 2,
      "ticker": "AAPL",
      "buzz_score": 78,
      "mention_count": 38,
      "avg_sentiment": 0.58,
      "trending": "UP",
      "summary": "iPhone 판매 호조 뉴스"
    },
    {
      "rank": 3,
      "ticker": "TSLA",
      "buzz_score": 65,
      "mention_count": 32,
      "avg_sentiment": -0.25,
      "trending": "UP",
      "summary": "가격 인하 관련 우려 섞인 논의"
    }
  ],
  
  "sector_sentiment": {
    "Technology": {
      "article_count": 128,
      "avg_sentiment": 0.52,
      "label": "POSITIVE",
      "top_tickers": ["NVDA", "AAPL", "MSFT"]
    },
    "Finance": {
      "article_count": 45,
      "avg_sentiment": 0.18,
      "label": "NEUTRAL",
      "top_tickers": ["JPM", "BAC", "GS"]
    },
    "Healthcare": {
      "article_count": 34,
      "avg_sentiment": 0.35,
      "label": "POSITIVE",
      "top_tickers": ["JNJ", "PFE", "MRNA"]
    }
  },
  
  "alerts": [
    {
      "type": "HIGH_BUZZ",
      "ticker": "NVDA",
      "message": "NVDA buzz score 92 (매우 높음)",
      "severity": "INFO"
    },
    {
      "type": "SENTIMENT_SPIKE",
      "theme": "AI 붐",
      "message": "AI 관련 뉴스 sentiment +0.68 (매우 긍정)",
      "severity": "INFO"
    }
  ]
}
```

## Examples

**Example 1**: Tech Rally Day
```
Input: 237 articles (last 24h)

Output:
- Overall Sentiment: +0.45 (POSITIVE)
- Top Theme: "AI Growth" (78 articles)
- Top Buzz: NVDA (92), AAPL (78), MSFT (65)
- Keywords: "ai growth", "earnings beat", "chip demand"
```

**Example 2**: Market Correction Day
```
Input: 189 articles

Output:
- Overall Sentiment: -0.38 (NEGATIVE)
- Top Theme: "Fed Rate Hike Fears" (92 articles)
- Top Buzz: SPY (88), VIX (76), TLT (54)
- Keywords: "rate hike", "inflation", "recession fears"
```

## Guidelines

### Do's ✅
- **배치 처리**: 효율성 극대화
- **Ticker Buzz 추적**: 시장  주목도 파악
- **Theme Detection**: 숨겨진 패턴 발견
- **Sector Breakdown**: 섹터별 sentiment

### Don'ts ❌
- 단일 기사만 분석 금지 (Quick/Deep Reasoning 역할)
- Theme 너무 세분화 금지 (5개 이내)
- Buzz score 과신 금지 (quality over quantity)
- Historical context 무시 금지

## Integration

### Batch Processing Endpoint

```python
@router.post("/api/news/batch-analyze")
async def batch_analyze_news(
    timeframe_hours: int = 24,
    db: Session = Depends(get_db)
):
    """Batch analyze recent news"""
    
    # Fetch articles
    cutoff = datetime.now() - timedelta(hours=timeframe_hours)
    articles = db.query(NewsArticle).filter(
        NewsArticle.created_at >= cutoff
    ).all()
    
    # Run News Intelligence Agent
    agent = NewsIntelligenceAgent()
    
    result = await agent.execute({
        'articles': articles,
        'timeframe_hours': timeframe_hours
    })
    
    return result
```

### Real-Time Updates (WebSocket)

```python
from fastapi import WebSocket

@router.websocket("/ws/news-intel")
async def news_intel_websocket(websocket: WebSocket):
    """Stream news intelligence updates"""
    
    await websocket.accept()
    
    while True:
        # Run analysis every 5 minutes
        result = await batch_analyze_news(timeframe_hours=1)
        
        await websocket.send_json(result)
        
        await asyncio.sleep(300)  # 5 minutes
```

## Performance Metrics

- **Batch Processing Speed**: 목표 < 10초 for 100 articles
- **Sentiment Accuracy**: > 80%
- **Theme Detection Quality**: > 75% (사람 판단과 일치)
- **Ticker Buzz Precision**: > 85%

## Comparison

| Agent | Scope | Speed | Use Case |
|-------|-------|-------|----------|
| News Intelligence | 배치 (100+ articles) | 10초 | 시장 전체 흐름 |
| Quick Analyzer | 단일 ticker | 5초 | 개별 종목 확인 |
| Deep Reasoning | 단일 news | 30초 | 중요한 뉴스 심층 분석 |

## Version History

- **v1.0** (2025-12-21): Initial release with batch processing and theme detection
