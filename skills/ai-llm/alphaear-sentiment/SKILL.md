---
name: alphaear-sentiment
description: Analyze text sentiment using FinBERT or LLM. Use when the user needs to determine the sentiment (positive/negative/neutral) and score of financial texts.
---

# AlphaEar Sentiment Skill

## Overview

This skill provides sentiment analysis capabilities tailored for financial texts, supporting both FinBERT (local model) and LLM-based analysis modes.

## Capabilities

### 1. Analyze Sentiment

Use `scripts/sentiment_tools.py` to analyze short texts like news titles or summaries.

**Key Methods:**

-   `analyze_sentiment(text)`: Get sentiment score and label.
    -   **Returns**: `{'score': float, 'label': str, 'reason': str}`.
    -   **Score Range**: -1.0 (Negative) to 1.0 (Positive).
-   `batch_update_news_sentiment(source, limit)`: Batch process unanalyzed news in the database.

**Example Usage (Python):**

```python
from scripts.database_manager import DatabaseManager
from scripts.sentiment_tools import SentimentTools

db = DatabaseManager()
# mode="auto" selects FinBERT if available, else LLM (mock/api)
sentiment_tools = SentimentTools(db, mode="auto")

# Analyze single text
result = sentiment_tools.analyze_sentiment("Company X reports record-breaking profits for Q4.")
print(result)
# Output: {'score': 0.95, 'label': 'positive', 'reason': '...'}
```

## Dependencies

-   `torch` (for FinBERT)
-   `transformers` (for FinBERT)
-   `sqlite3` (built-in)

Ensure `DatabaseManager` is initialized correctly.
