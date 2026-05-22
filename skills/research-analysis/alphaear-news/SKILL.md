---
name: alphaear-news
description: Fetch hot news, unified trends, and prediction market data. Use when the user needs real-time financial news, trend reports from multiple sources (Weibo, Zhihu, WallstreetCN, etc.), or Polymarket prediction data.
---

# AlphaEar News Skill

## Overview

This skill provides comprehensive capabilities to fetch real-time hot news, generate unified trend reports from multiple platforms, and retrieve prediction market data from Polymarket. It is designed for financial analysis and signal discovery.

## Capabilities

### 1. Fetch Hot News & Unified Trends

Use `scripts/news_tools.py` to interact with the NewsNow API.

**Key Methods:**

-   `fetch_hot_news(source_id, count)`: Get hot news list from a specific source.
    -   **Sources**: `cls` (Cailian Press), `wallstreetcn`, `weibo`, `zhihu`, `baidu`, `toutiao`, `douyin`, `thepaper`, `36kr`.
-   `get_unified_trends(sources)`: Get a unified report aggregating top news from specified sources.
-   `fetch_news_content(url)`: Extract main content from a URL using Jina Reader.

**Example Usage (Python):**

```python
from scripts.database_manager import DatabaseManager
from scripts.news_tools import NewsNowTools

db = DatabaseManager()
tools = NewsNowTools(db)

# 1. Fetch specific source
cls_news = tools.fetch_hot_news("cls", count=10)
print(cls_news)

# 2. Get unified report
report = tools.get_unified_trends(["cls", "wallstreetcn", "weibo"])
print(report)

# 3. Fetch content
content = tools.fetch_news_content("https://example.com/article")
```

### 2. Fetch Prediction Market Data

Use `scripts/news_tools.py` (specifically `PolymarketTools` class) to get data from Polymarket.

**Key Methods:**

-   `get_active_markets(limit)`: Get active prediction markets.
-   `get_market_summary(limit)`: Get a formatted summary report of prediction markets.

**Example Usage (Python):**

```python
from scripts.database_manager import DatabaseManager
from scripts.news_tools import PolymarketTools

db = DatabaseManager()
poly_tools = PolymarketTools(db)

# Get market summary
summary = poly_tools.get_market_summary(limit=10)
print(summary)
```

## Dependencies

-   `requests`
-   `loguru`
-   `pandas` (via DatabaseManager)
-   `sqlite3` (built-in)

Ensure these packages are installed in the environment. JINA_API_KEY environment variable is optional but recommended for better content extraction.
