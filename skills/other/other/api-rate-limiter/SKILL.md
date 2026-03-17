---
name: api-rate-limiter
description: Manage API rate limits across all data sources (Alpha Vantage, Finnhub, Polygon, NewsAPI). Use when implementing data fetching, optimizing API calls, or debugging rate limit issues. Trigger on API quota, rate limiting, or data ingestion discussions.
metadata: {"clawdbot":{"emoji":"🚦","project":"investment-analysis-platform"}}
---

# API Rate Limiter Skill

Efficiently manage API rate limits across all data providers to maximize data quality while staying within free tier limits.

## Rate Limit Reference

| Provider | Rate Limit | Daily Limit | Strategy |
|----------|------------|-------------|----------|
| Alpha Vantage | 5/min | 25/day | High-value stocks only |
| Finnhub | 60/min | Unlimited | Bulk quotes, news |
| Polygon | 5/min | Unlimited | Supplementary data |
| NewsAPI | - | 100/day | Sector news batch |

## Implementation Patterns

### Token Bucket Rate Limiter

```python
import asyncio
from datetime import datetime, timedelta
from collections import deque

class RateLimiter:
    def __init__(self, calls_per_minute: int, calls_per_day: int = None):
        self.calls_per_minute = calls_per_minute
        self.calls_per_day = calls_per_day
        self.minute_calls = deque()
        self.daily_calls = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> bool:
        async with self._lock:
            now = datetime.utcnow()

            # Clean old minute calls
            while self.minute_calls and self.minute_calls[0] < now - timedelta(minutes=1):
                self.minute_calls.popleft()

            # Clean old daily calls
            while self.daily_calls and self.daily_calls[0] < now - timedelta(days=1):
                self.daily_calls.popleft()

            # Check limits
            if len(self.minute_calls) >= self.calls_per_minute:
                wait_time = (self.minute_calls[0] + timedelta(minutes=1) - now).total_seconds()
                await asyncio.sleep(wait_time)

            if self.calls_per_day and len(self.daily_calls) >= self.calls_per_day:
                return False  # Daily limit exceeded

            # Record call
            self.minute_calls.append(now)
            self.daily_calls.append(now)
            return True

# Pre-configured limiters for each API
RATE_LIMITERS = {
    "alpha_vantage": RateLimiter(calls_per_minute=5, calls_per_day=25),
    "finnhub": RateLimiter(calls_per_minute=60),
    "polygon": RateLimiter(calls_per_minute=5),
    "news_api": RateLimiter(calls_per_minute=10, calls_per_day=100),
}
```

### Request Batching

```python
async def batch_finnhub_quotes(tickers: list[str]) -> dict:
    """
    Batch fetch quotes using Finnhub's 60/min limit efficiently.
    For 6000 stocks: ~100 minutes with optimal batching.
    """
    limiter = RATE_LIMITERS["finnhub"]
    results = {}

    for ticker in tickers:
        if await limiter.acquire():
            try:
                data = await finnhub_client.quote(ticker)
                results[ticker] = data
            except Exception as e:
                logger.warning(f"Failed to fetch {ticker}: {e}")
        else:
            logger.warning("Rate limit reached, pausing...")
            await asyncio.sleep(60)

    return results
```

### Priority Queue Strategy

```python
from enum import IntEnum
from heapq import heappush, heappop

class Priority(IntEnum):
    CRITICAL = 1   # Top holdings, active alerts
    HIGH = 2       # Watchlist, sector leaders
    MEDIUM = 3     # S&P 500 components
    LOW = 4        # Other stocks
    BACKGROUND = 5 # Rarely traded, low volume

class PriorityAPIQueue:
    def __init__(self):
        self.queue = []
        self.processed = set()

    def add(self, ticker: str, priority: Priority):
        if ticker not in self.processed:
            heappush(self.queue, (priority, ticker))

    def get_batch(self, size: int) -> list[str]:
        batch = []
        while self.queue and len(batch) < size:
            _, ticker = heappop(self.queue)
            if ticker not in self.processed:
                batch.append(ticker)
                self.processed.add(ticker)
        return batch

# Usage: Prioritize Alpha Vantage's 25 daily calls
priority_queue = PriorityAPIQueue()
priority_queue.add("AAPL", Priority.CRITICAL)
priority_queue.add("GOOGL", Priority.CRITICAL)
# ... add all stocks with priorities

alpha_vantage_batch = priority_queue.get_batch(25)
```

## Optimal API Usage Strategy

### Daily Pipeline Schedule

```
6:00 AM ET - Market Data Pipeline Start
├── Finnhub Bulk Quotes (6000 stocks @ 60/min = ~100 min)
├── Alpha Vantage Detailed (25 priority stocks)
├── Polygon Supplementary (5/min for top 100)
└── NewsAPI Batch (100 articles for sentiment)

Pipeline completes by ~8:30 AM ET
```

### API Selection Matrix

| Data Need | Primary API | Fallback | Cache TTL |
|-----------|-------------|----------|-----------|
| Current price | Finnhub | Polygon | 1 min |
| Historical OHLCV | Polygon | Alpha Vantage | 24 hours |
| Company info | Finnhub | Alpha Vantage | 7 days |
| News/sentiment | NewsAPI | Finnhub | 4 hours |
| Fundamentals | Alpha Vantage | SEC EDGAR | 24 hours |

## Monitoring Commands

```bash
# Check current rate limit status
python -c "
from backend.services.rate_limiter import get_rate_limit_status

status = get_rate_limit_status()
for api, info in status.items():
    print(f'{api}:')
    print(f'  Minute: {info[\"minute_used\"]}/{info[\"minute_limit\"]}')
    if info.get('daily_limit'):
        print(f'  Daily: {info[\"daily_used\"]}/{info[\"daily_limit\"]}')
"

# View API call history
python -c "
from backend.services.api_tracker import get_call_history
import json

history = get_call_history(hours=24)
print(json.dumps(history, indent=2))
"
```

## Error Handling

```python
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

class APIError(Exception):
    pass

class RateLimitExceeded(APIError):
    pass

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=lambda e: isinstance(e, aiohttp.ClientError)
)
async def safe_api_call(api_name: str, func, *args, **kwargs):
    """Wrapper for safe API calls with rate limiting and retry."""
    limiter = RATE_LIMITERS.get(api_name)

    if limiter:
        if not await limiter.acquire():
            raise RateLimitExceeded(f"{api_name} daily limit exceeded")

    try:
        return await func(*args, **kwargs)
    except aiohttp.ClientResponseError as e:
        if e.status == 429:  # Rate limited by API
            logger.warning(f"{api_name} rate limited, backing off...")
            await asyncio.sleep(60)
            raise
        raise
```

## Quick Reference

| Situation | Action |
|-----------|--------|
| Alpha Vantage limit hit | Wait until next day, use Finnhub |
| Finnhub 429 error | Wait 60 seconds, reduce concurrency |
| Polygon limit hit | Reduce to 1 call per 15 seconds |
| NewsAPI exhausted | Use cached news, wait for reset |
| All APIs down | Serve from cache, alert admin |
