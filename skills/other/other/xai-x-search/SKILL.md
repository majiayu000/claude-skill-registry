---
name: xai-x-search
description: Search Twitter/X in real-time using Grok API. Use when searching X posts, tracking trends, monitoring accounts, or analyzing social discussions.
version: 1.0.0
---

# xAI X (Twitter) Search

Real-time Twitter/X search using Grok's native X integration - a capability unique to xAI.

## Quick Start

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# Simple X search
response = client.chat.completions.create(
    model="grok-4-1-fast",
    messages=[{
        "role": "user",
        "content": "Search X for what people are saying about Tesla stock today"
    }]
)
print(response.choices[0].message.content)
```

## Search Capabilities

### 1. Topic Search
```python
def search_x_topic(topic: str) -> str:
    """Search X for posts about a topic."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"Search X for recent posts about {topic}. Summarize the main discussions and sentiment."
        }]
    )
    return response.choices[0].message.content
```

### 2. Ticker/Stock Search
```python
def search_stock_mentions(ticker: str) -> str:
    """Search X for stock ticker mentions."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Search X for mentions of ${ticker} stock.
            Find:
            - Recent discussions
            - Sentiment (bullish/bearish)
            - Key influencer opinions
            - Breaking news mentions
            Return structured analysis."""
        }]
    )
    return response.choices[0].message.content
```

### 3. Account Monitoring
```python
def monitor_account(handle: str) -> str:
    """Get recent posts from a specific X account."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"Search X for the most recent posts from @{handle}. Summarize their latest activity."
        }]
    )
    return response.choices[0].message.content
```

### 4. Trending Topics
```python
def get_trending() -> str:
    """Get current trending topics on X."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": "What are the current trending topics on X? List the top 10 with brief descriptions."
        }]
    )
    return response.choices[0].message.content
```

## Agent Tools API (Advanced)

For more control, use the Agent Tools API:

```python
# Using Responses API with x_search tool
response = client.chat.completions.create(
    model="grok-4-1-fast",
    messages=[{
        "role": "user",
        "content": "Search X for posts about Bitcoin from the last 24 hours"
    }],
    tools=[{
        "type": "x_search",
        "x_search": {
            "enabled": True,
            "date_range": {
                "start": "2025-12-04",
                "end": "2025-12-05"
            }
        }
    }]
)
```

### Filter by Handles
```python
# Search only specific accounts
response = client.chat.completions.create(
    model="grok-4-1-fast",
    messages=[{
        "role": "user",
        "content": "What are these financial analysts saying about the market?"
    }],
    tools=[{
        "type": "x_search",
        "x_search": {
            "enabled": True,
            "allowed_x_handles": [
                "jimcramer",
                "elonmusk",
                "chaikinadx",
                "unusual_whales"
            ]
        }
    }]
)
```

## Common Use Cases

### Financial News Monitoring
```python
def monitor_financial_news() -> dict:
    """Monitor financial news on X."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": """Search X for breaking financial news in the last hour.
            Focus on:
            - Market-moving news
            - Earnings announcements
            - Fed/economic news
            - Major analyst calls

            Return as JSON:
            {
                "breaking_news": [...],
                "market_sentiment": "bullish/bearish/neutral",
                "key_events": [...]
            }"""
        }]
    )
    return response.choices[0].message.content
```

### Earnings Reaction Tracking
```python
def track_earnings_reaction(ticker: str) -> str:
    """Track X reaction to earnings announcement."""
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Search X for reaction to ${ticker} earnings.
            Analyze:
            - Overall sentiment
            - Key concerns raised
            - Positive highlights mentioned
            - Notable influencer reactions
            - Volume of discussion"""
        }]
    )
    return response.choices[0].message.content
```

### Competitor Analysis
```python
def compare_sentiment(tickers: list) -> str:
    """Compare X sentiment across multiple stocks."""
    ticker_str = ", ".join([f"${t}" for t in tickers])
    response = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{
            "role": "user",
            "content": f"""Compare X sentiment for: {ticker_str}
            For each, provide:
            - Current sentiment score (-1 to +1)
            - Key themes being discussed
            - Notable mentions
            Return as structured comparison."""
        }]
    )
    return response.choices[0].message.content
```

## Search Parameters

| Parameter | Description | Max |
|-----------|-------------|-----|
| `allowed_x_handles` | Only search these accounts | 10 |
| `excluded_x_handles` | Exclude these accounts | 10 |
| `date_range.start` | Start date (ISO8601) | - |
| `date_range.end` | End date (ISO8601) | - |
| `include_media` | Analyze images/videos | - |

## Rate Limits & Costs

| Metric | Value |
|--------|-------|
| Cost per search | $0.005 ($5/1,000) |
| Max handles filter | 10 |
| Date range | Any |

## Best Practices

### 1. Be Specific
```python
# Bad - too vague
"Search X for stocks"

# Good - specific query
"Search X for posts about $AAPL stock price movement today from verified financial accounts"
```

### 2. Request Structured Output
```python
# Request JSON for easier parsing
content = """Search X for $NVDA sentiment. Return JSON:
{
    "sentiment": "bullish/bearish/neutral",
    "score": -1 to 1,
    "key_posts": [...],
    "influencer_opinions": [...]
}"""
```

### 3. Use Handle Filters for Quality
```python
# Filter to trusted sources
financial_handles = [
    "DeItaone",  # Breaking news
    "unusual_whales",  # Options flow
    "Fxhedgers",  # Market news
    "zaborsky"  # Analysis
]
```

### 4. Combine with Other Data
```python
# Combine X sentiment with price data
x_sentiment = search_stock_mentions("AAPL")
price_data = finnhub_client.get_quote("AAPL")
# Analyze together
```

## Limitations

1. **Sarcasm detection** - May misinterpret sarcastic posts
2. **Bot content** - Cannot always filter bot posts
3. **Historical depth** - Best for recent data
4. **Rate limits** - $5/1,000 searches

## Error Handling

```python
def safe_x_search(query: str) -> dict:
    """X search with error handling."""
    try:
        response = client.chat.completions.create(
            model="grok-4-1-fast",
            messages=[{"role": "user", "content": query}],
            timeout=30
        )
        return {
            "success": True,
            "data": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

## Related Skills
- `xai-sentiment` - Sentiment analysis
- `xai-stock-sentiment` - Stock-specific sentiment
- `xai-agent-tools` - Advanced tool usage

## References
- [xAI Live Search](https://docs.x.ai/docs/guides/live-search)
- [Agent Tools API](https://x.ai/news/grok-4-1-fast/)
