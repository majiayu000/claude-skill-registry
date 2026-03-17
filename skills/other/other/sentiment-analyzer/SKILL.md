---
name: sentiment-analyzer
description: Analyze text sentiment (positive/negative/neutral) with confidence scores, emotion detection, and visualization. Supports single text, CSV batch, and trend analysis.
---

# Sentiment Analyzer

Analyze the sentiment of text content with detailed scoring, emotion detection, and visualization capabilities. Process single texts, CSV files, or track sentiment trends over time.

## Quick Start

```python
from scripts.sentiment_analyzer import SentimentAnalyzer

# Analyze single text
analyzer = SentimentAnalyzer()
result = analyzer.analyze("I love this product! It's amazing.")
print(f"Sentiment: {result['sentiment']} ({result['score']:.2f})")

# Batch analyze CSV
results = analyzer.analyze_csv("reviews.csv", text_column="review")
analyzer.plot_distribution("sentiment_dist.png")
```

## Features

- **Sentiment Classification**: Positive, negative, neutral with confidence
- **Polarity Scoring**: -1.0 (negative) to +1.0 (positive)
- **Subjectivity Detection**: Objective vs subjective content
- **Emotion Detection**: Joy, anger, sadness, fear, surprise
- **Batch Processing**: Analyze CSV files with any text column
- **Trend Analysis**: Track sentiment over time
- **Visualizations**: Distribution plots, trend charts, word clouds

## API Reference

### Initialization

```python
analyzer = SentimentAnalyzer()
```

### Single Text Analysis

```python
result = analyzer.analyze("This is great!")
# Returns:
# {
#     'text': 'This is great!',
#     'sentiment': 'positive',  # positive, negative, neutral
#     'score': 0.85,            # -1.0 to 1.0
#     'confidence': 0.92,       # 0.0 to 1.0
#     'subjectivity': 0.75,     # 0.0 (objective) to 1.0 (subjective)
#     'emotions': {'joy': 0.8, 'anger': 0.0, ...}
# }
```

### Batch Analysis

```python
# From list
texts = ["Great product!", "Terrible service.", "It's okay."]
results = analyzer.analyze_batch(texts)

# From CSV
results = analyzer.analyze_csv(
    "reviews.csv",
    text_column="review_text",
    output="results.csv"
)
```

### Trend Analysis

```python
# Analyze sentiment over time
results = analyzer.analyze_csv(
    "posts.csv",
    text_column="content",
    date_column="posted_at"
)
analyzer.plot_trend("sentiment_trend.png")
```

### Visualizations

```python
# Sentiment distribution
analyzer.plot_distribution("distribution.png")

# Sentiment over time
analyzer.plot_trend("trend.png")

# Word cloud by sentiment
analyzer.plot_wordcloud("positive", "positive_words.png")
```

## CLI Usage

```bash
# Analyze single text
python sentiment_analyzer.py --text "I love this product!"

# Analyze file
python sentiment_analyzer.py --input reviews.csv --column review --output results.csv

# With visualization
python sentiment_analyzer.py --input reviews.csv --column text --plot distribution.png

# Trend analysis
python sentiment_analyzer.py --input posts.csv --column content --date posted_at --trend trend.png
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--text` | Single text to analyze | - |
| `--input` | Input CSV file | - |
| `--column` | Text column name | `text` |
| `--date` | Date column for trends | - |
| `--output` | Output CSV file | - |
| `--plot` | Save distribution plot | - |
| `--trend` | Save trend plot | - |
| `--format` | Output format (json, csv) | `json` |

## Examples

### Product Review Analysis

```python
analyzer = SentimentAnalyzer()
results = analyzer.analyze_csv("amazon_reviews.csv", text_column="review")

# Summary statistics
positive = sum(1 for r in results if r['sentiment'] == 'positive')
negative = sum(1 for r in results if r['sentiment'] == 'negative')
print(f"Positive: {positive}, Negative: {negative}")

# Average sentiment score
avg_score = sum(r['score'] for r in results) / len(results)
print(f"Average sentiment: {avg_score:.2f}")
```

### Social Media Monitoring

```python
analyzer = SentimentAnalyzer()

# Analyze tweets with timestamps
results = analyzer.analyze_csv(
    "tweets.csv",
    text_column="tweet_text",
    date_column="created_at"
)

# Plot sentiment trend
analyzer.plot_trend("twitter_sentiment.png", title="Brand Sentiment Over Time")
```

### Customer Feedback Categorization

```python
analyzer = SentimentAnalyzer()

feedback = [
    "Your support team was incredibly helpful!",
    "The product broke after one day.",
    "Shipping was on time.",
    "I'm extremely disappointed with the quality.",
    "It works as expected, nothing special."
]

for text in feedback:
    result = analyzer.analyze(text)
    print(f"{result['sentiment'].upper():8} ({result['score']:+.2f}): {text[:50]}")
```

## Output Format

### JSON Output

```json
{
  "text": "I love this product!",
  "sentiment": "positive",
  "score": 0.85,
  "confidence": 0.92,
  "subjectivity": 0.75,
  "emotions": {
    "joy": 0.82,
    "anger": 0.02,
    "sadness": 0.01,
    "fear": 0.03,
    "surprise": 0.12
  }
}
```

### CSV Output

| text | sentiment | score | confidence | subjectivity |
|------|-----------|-------|------------|--------------|
| Great product! | positive | 0.85 | 0.91 | 0.80 |
| Terrible... | negative | -0.72 | 0.88 | 0.65 |

## Dependencies

```
textblob>=0.17.0
pandas>=2.0.0
matplotlib>=3.7.0
```

## Limitations

- English language optimized (other languages may have reduced accuracy)
- Sarcasm and irony may not be detected accurately
- Context-dependent sentiment may be missed
- Short texts (<5 words) have lower confidence
