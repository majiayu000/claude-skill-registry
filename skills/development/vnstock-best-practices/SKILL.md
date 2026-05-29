---
name: vnstock-quote-best-practices
description: Best practices for using vnstock3 Quote class with VCI source. Use when fetching Vietnamese stock price data, implementing batch processing, caching, error handling, or data validation for vnstock Quote operations. Triggers on queries about vnstock performance optimization, resilient data fetching, or Quote API patterns.
---

# VNStock Quote Best Practices

## Quick Reference

```python
from vnstock import Quote

# Basic usage - VCI source only
quote = Quote(symbol='VCI', source='VCI')
df = quote.history(start='2024-01-01', end='2024-12-31', interval='1D')
```

**Parameters:**
- `symbol`: Stock ticker (e.g., 'VCI', 'ACB', 'FPT')
- `source`: Must be `'VCI'` for this skill
- `interval`: `'1D'` (daily), `'1W'` (weekly), `'1M'` (monthly)

**Output columns:** `time`, `open`, `high`, `low`, `close`, `volume`

## Patterns

### Batch Processing

Reuse Quote instance, change symbol:

```python
from vnstock import Quote

symbols = ['VCI', 'ACB', 'FPT']
quote = Quote(source='VCI', symbol='VCI')
results = {}

for symbol in symbols:
    quote.symbol = symbol
    results[symbol] = quote.history(start='2024-01-01', end='2024-12-31', interval='1D')
```

### Caching

See `references/caching.md` for file-based cache implementation with TTL.

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    retry=retry_if_exception_type((requests.RequestException, TimeoutError)),
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def fetch_with_retry(quote, start, end):
    return quote.history(start=start, end=end)
```

### Source Fallback

```python
def get_price_with_fallback(symbol, start, end):
    sources = ['VCI', 'TCBS']  # VCI primary, TCBS backup
    for source in sources:
        try:
            quote = Quote(source=source, symbol=symbol)
            return quote.history(start=start, end=end)
        except Exception:
            continue
    raise Exception("All sources failed")
```

### Data Validation

```python
def validate_ohlc(df):
    issues = []
    required = ['time', 'open', 'high', 'low', 'close', 'volume']
    missing = [c for c in required if c not in df.columns]
    if missing:
        issues.append(f"Missing: {missing}")
    if df.isnull().any().any():
        issues.append(f"Nulls: {df.isnull().sum().sum()}")
    if (df['high'] < df['low']).any():
        issues.append("Invalid OHLC: high < low")
    return issues
```

### Outlier Detection

```python
import numpy as np

def detect_outliers(df, column='close', threshold=3):
    z = np.abs((df[column] - df[column].mean()) / df[column].std())
    return df[z > threshold]
```

## Error Handling

See `references/error-handling.md` for:
- Circuit breaker pattern
- Connection pooling
- Comprehensive logging setup

## Key Rules

1. **Always use `source='VCI'`** - This skill targets VCI source only
2. **Reuse Quote instances** - Don't create new instances per symbol in loops
3. **Validate data after fetch** - Check for nulls, OHLC logic, gaps
4. **Implement retries** - Network requests can fail temporarily
5. **Cache when appropriate** - Reduce API calls for historical data
