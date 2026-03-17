---
name: data-training-manager
description: Manage AI training data, monitor content freshness, detect repetition, and update training samples for continuous learning. Use when managing training data, checking content quality, updating AI models, or preventing repetitive content.
allowed-tools: Read, Write, Bash(python:*)
model: claude-sonnet-4-20250514
---

# Data Training Manager

Continuous learning system for managing AI training data, monitoring content freshness, and preventing repetitive outputs.

## Overview

Maintain high-quality AI outputs through:
- **Training Data Management** - Add, update, remove training samples
- **Freshness Monitoring** - Detect stale and repetitive content
- **Quality Scoring** - Track performance of training samples
- **Continuous Learning** - Automatically update based on engagement
- **Trend Analysis** - Identify patterns in successful content

## Quick Start

### 1. Check Training Data Freshness

```python
from src.freshness_monitor import FreshnessMonitor

monitor = FreshnessMonitor()

# Check if generated content is fresh
score = monitor.check_freshness(
    generated_text="gm to data contributors who deserve equity...",
    threshold=0.7  # 70% uniqueness required
)

if score < 0.7:
    print("⚠️ Content too similar to existing samples")
else:
    print("✅ Content is fresh!")
```

### 2. Add New Training Sample

```python
from src.continuous_learning import ContinuousLearningSystem

learning = ContinuousLearningSystem()

# Add high-performing tweet
learning.add_sample(
    text="gm to everyone building on @base 💙",
    type="gm",
    engagement={"likes": 150, "retweets": 20},
    features={"has_emoji": True, "mentions": ["@base"]}
)
```

### 3. Manage Training Data

```bash
# Check freshness of all samples
python scripts/manage_training.py check

# View statistics
python scripts/manage_training.py stats

# Add new sample
python scripts/manage_training.py add \
  --text "your tweet text" \
  --type gm \
  --engagement '{"likes":100}'
```

## Training Data Structure

### Sample Format

Each training sample contains:

```json
{
  "id": "sample_001",
  "text": "The actual content...",
  "type": "gm|insight|casual|reply",
  "topic": "data_ownership|x402|base|milady|...",
  "style": "short|medium|long",
  "created_at": "2026-01-07T10:00:00Z",
  "engagement": {
    "likes": 150,
    "retweets": 30,
    "replies": 10,
    "impressions": 5000
  },
  "features": {
    "has_emoji": true,
    "emoji_list": ["🎀", "🧹"],
    "has_ascii_art": false,
    "has_thread": false,
    "has_mentions": true,
    "mention_list": ["@codatta_io"],
    "has_hashtags": false,
    "tone": "critical|supportive|casual|...",
    "word_count": 25,
    "char_count": 120
  },
  "freshness_score": 0.85,
  "quality_score": 0.92,
  "last_used": "2026-01-05T14:30:00Z",
  "use_count": 3,
  "performance_trend": "improving|stable|declining"
}
```

### Training Files

| File | Purpose | Sample Count |
|------|---------|--------------|
| `gm_posts.json` | GM post variations | 50+ |
| `codatta_insights.json` | Industry insights | 60+ |
| `casual_posts.json` | Personal/casual content | 30+ |
| `interactions.json` | Reply examples | 40+ |
| `archived_samples.json` | Low-performing samples | Unlimited |

## Freshness Monitoring

### How It Works

Freshness score (0.0-1.0) measures uniqueness:

```python
def calculate_freshness(new_text, existing_samples):
    """
    Returns:
      1.0 = Completely unique
      0.8 = Similar but fresh
      0.5 = Moderately repetitive
      0.0 = Identical to existing
    """

    scores = []

    for sample in existing_samples:
        # 1. Jaccard similarity (word overlap)
        jaccard = jaccard_similarity(new_text, sample['text'])

        # 2. Phrase similarity (3-gram overlap)
        phrase = phrase_similarity(new_text, sample['text'])

        # 3. Semantic similarity (embedding distance)
        semantic = semantic_similarity(new_text, sample['text'])

        # Combined score (weighted)
        combined = (jaccard * 0.3 + phrase * 0.4 + semantic * 0.3)
        scores.append(combined)

    # Return inverse of max similarity
    return 1.0 - max(scores)
```

### Usage

```python
monitor = FreshnessMonitor()

# Check single text
score = monitor.check_freshness(
    "gm to data contributors 🎀",
    data_type="gm",
    threshold=0.7
)

# Batch check
texts = [
    "gm everyone",
    "good morning frens",
    "gm to builders on base"
]

results = monitor.batch_check(texts, threshold=0.7)
# Returns: [{"text": "...", "score": 0.85, "is_fresh": True}, ...]
```

### Freshness Thresholds

```python
FRESHNESS_THRESHOLDS = {
    "gm": 0.65,          # GM posts can be more repetitive
    "insight": 0.80,     # Insights must be unique
    "casual": 0.70,      # Casual moderate uniqueness
    "reply": 0.75        # Replies should be fresh
}
```

## Continuous Learning System

### Auto-Update from Performance

```python
learning = ContinuousLearningSystem()

# Add successful tweet to training data
learning.learn_from_performance(
    tweet_id="1234567890",
    text="gm to data contributors who deserve equity 🎀",
    engagement={"likes": 200, "retweets": 40}
)

# System automatically:
# 1. Checks freshness
# 2. Evaluates quality
# 3. Adds to appropriate training file
# 4. Archives low-performers if needed
```

### Performance Tracking

```python
# Track sample performance over time
stats = learning.get_sample_stats("sample_001")

# Returns:
{
  "use_count": 5,
  "avg_engagement": {"likes": 120, "retweets": 25},
  "freshness_decay": 0.15,  # How much freshness dropped
  "trend": "stable",
  "recommendation": "keep|archive|update"
}
```

### Auto-Archiving

```python
# Archive low-performing samples
archived = learning.auto_archive(
    min_quality_score=0.6,
    min_freshness=0.5,
    max_age_days=90
)

print(f"Archived {len(archived)} samples")
```

## Quality Scoring

### Quality Metrics

```python
def calculate_quality_score(sample):
    """
    Returns 0.0-1.0 quality score based on:
    - Engagement performance (40%)
    - Freshness (30%)
    - Feature diversity (20%)
    - Recency (10%)
    """

    # Engagement score (normalized)
    engagement_score = normalize_engagement(sample['engagement'])

    # Freshness score
    freshness_score = sample['freshness_score']

    # Feature diversity (more features = higher score)
    features = sample['features']
    diversity_score = calculate_diversity(features)

    # Recency score (newer = higher)
    recency_score = calculate_recency(sample['created_at'])

    # Weighted combination
    quality = (
        engagement_score * 0.4 +
        freshness_score * 0.3 +
        diversity_score * 0.2 +
        recency_score * 0.1
    )

    return quality
```

### Usage

```python
# Calculate quality for all samples
quality_report = learning.analyze_quality(
    data_type="gm",
    min_samples=10
)

# Returns:
{
  "avg_quality": 0.75,
  "high_quality": 15,  # score > 0.8
  "medium_quality": 20,  # 0.6-0.8
  "low_quality": 5,  # < 0.6
  "recommendations": [
    "Archive 5 low-quality samples",
    "Add more diversity to casual posts"
  ]
}
```

## Management Scripts

### Check Freshness

```bash
python scripts/manage_training.py check

# Output:
# Checking gm_posts.json...
# ✅ 45/50 samples are fresh (90%)
# ⚠️ 5 samples below threshold
#
# Checking codatta_insights.json...
# ✅ 58/60 samples are fresh (97%)
# ⚠️ 2 samples below threshold
#
# Overall freshness: 93%
```

### View Statistics

```bash
python scripts/manage_training.py stats

# Output:
# Training Data Statistics
# ========================
#
# Total samples: 180
# - GM posts: 50
# - Insights: 60
# - Casual: 30
# - Interactions: 40
#
# Quality Distribution:
# - High (>0.8): 120 (67%)
# - Medium (0.6-0.8): 50 (28%)
# - Low (<0.6): 10 (5%)
#
# Freshness:
# - Avg score: 0.82
# - Min threshold: 0.70
# - Samples below: 8 (4%)
```

### Add New Sample

```bash
# Interactive mode
python scripts/manage_training.py add

# Prompts for:
# - Text content
# - Type (gm/insight/casual/reply)
# - Topic
# - Engagement metrics
# - Features

# Non-interactive mode
python scripts/manage_training.py add \
  --text "gm to builders on base 💙" \
  --type gm \
  --topic base \
  --engagement '{"likes":150,"retweets":30}' \
  --features '{"has_emoji":true,"mentions":["@base"]}'
```

### Import Batch

```bash
# Import from CSV
python scripts/manage_training.py import \
  --file successful_tweets.csv \
  --type gm \
  --min-likes 100

# Import from JSON
python scripts/manage_training.py import \
  --file tweets_export.json \
  --auto-categorize  # Auto-detect type/topic
```

### Archive Old Samples

```bash
# Archive samples older than 90 days with low engagement
python scripts/manage_training.py archive \
  --max-age 90 \
  --min-quality 0.6 \
  --dry-run  # Preview before archiving

# Actually archive
python scripts/manage_training.py archive \
  --max-age 90 \
  --min-quality 0.6
```

### View History

```bash
# Show addition/removal history
python scripts/manage_training.py history \
  --days 30

# Output:
# Training Data History (Last 30 days)
# =====================================
#
# 2026-01-07: Added 3 samples (gm)
# 2026-01-06: Archived 2 samples (low quality)
# 2026-01-05: Added 5 samples (insights)
# 2026-01-04: Updated 1 sample (engagement)
# ...
```

## Trend Analysis

### Identify Successful Patterns

```python
from src.trend_analyzer import TrendAnalyzer

analyzer = TrendAnalyzer()

# Find common features in high-performing samples
trends = analyzer.analyze_trends(
    min_engagement={"likes": 100},
    days=30
)

# Returns:
{
  "top_features": [
    {"feature": "has_emoji", "success_rate": 0.85},
    {"feature": "mentions_base", "success_rate": 0.78},
    {"feature": "short_format", "success_rate": 0.72}
  ],
  "top_topics": [
    {"topic": "data_ownership", "avg_likes": 150},
    {"topic": "base_ecosystem", "avg_likes": 130}
  ],
  "optimal_length": {
    "word_count": "20-30",
    "char_count": "120-150"
  },
  "emoji_usage": {
    "optimal_count": "2-3",
    "top_emojis": ["🎀", "🧹", "💙"]
  }
}
```

### Suggest Improvements

```python
# Get suggestions for improving training data
suggestions = analyzer.suggest_improvements()

# Returns:
[
  "Add more samples about x402 token (only 5 currently)",
  "Increase casual content (15% vs target 20%)",
  "Archive 3 GM samples with freshness < 0.5",
  "Add more emoji diversity (currently 70% use 🎀)"
]
```

## Advanced Features

### A/B Testing

```python
# Test two versions of content
results = learning.ab_test(
    version_a="gm to data contributors 🎀",
    version_b="good morning to data labelers 🧹",
    duration_days=7
)

# Returns:
{
  "winner": "version_a",
  "version_a_engagement": {"likes": 120, "retweets": 25},
  "version_b_engagement": {"likes": 90, "retweets": 18},
  "confidence": 0.85
}
```

### Template Generation

```python
# Generate templates from high-performing samples
templates = learning.generate_templates(
    min_quality=0.8,
    max_templates=10
)

# Returns:
[
  {
    "template": "gm to {target_group} who deserve {value}",
    "variables": ["target_group", "value"],
    "examples": [
      "gm to data contributors who deserve equity",
      "gm to builders who deserve recognition"
    ]
  }
]
```

### Diversity Analysis

```python
# Check content diversity
diversity = learning.analyze_diversity()

# Returns:
{
  "topic_distribution": {
    "data_ownership": 0.35,
    "base_ecosystem": 0.25,
    "x402": 0.20,
    "casual": 0.15,
    "milady": 0.05
  },
  "style_distribution": {
    "short": 0.40,
    "medium": 0.45,
    "long": 0.15
  },
  "tone_distribution": {
    "critical": 0.30,
    "supportive": 0.40,
    "casual": 0.30
  },
  "diversity_score": 0.78,
  "recommendations": [
    "Increase Milady content (target 15%)",
    "Add more long-form content"
  ]
}
```

## Integration with Content Generation

### Use Training Data in Generation

```python
from skills.twitter_content_ai.src.content_generator import ContentGenerator
from src.continuous_learning import ContinuousLearningSystem

generator = ContentGenerator()
learning = ContinuousLearningSystem()

# Generate using high-quality samples
tweet = generator.generate_from_samples(
    sample_type="gm",
    min_quality=0.8,
    ensure_freshness=0.75
)

# Learn from generated content
if tweet_posted:
    learning.learn_from_performance(
        tweet_id=tweet_id,
        text=tweet,
        engagement=get_engagement(tweet_id)
    )
```

## Best Practices

1. **Regular Freshness Checks** - Run weekly to maintain quality
2. **Archive Strategically** - Don't delete, archive for future reference
3. **Track Performance** - Link training samples to actual tweets
4. **Diverse Samples** - Ensure variety in topics, styles, tones
5. **Update Frequently** - Add 3-5 new samples per week
6. **Quality Over Quantity** - 50 great samples > 200 mediocre ones
7. **Monitor Trends** - Analyze what's working and adjust
8. **Test Changes** - Use A/B testing before large updates

## Monitoring Dashboard

```python
# Generate visual dashboard
dashboard = learning.generate_dashboard()

# Includes:
# - Freshness trend over time
# - Quality distribution
# - Topic balance
# - Performance metrics
# - Recommendations

dashboard.save("training_dashboard.html")
```

## Configuration

### Freshness Settings

```python
# config/learning_config.yaml
freshness:
  thresholds:
    gm: 0.65
    insight: 0.80
    casual: 0.70
    reply: 0.75
  check_interval_days: 7
  min_samples: 30

quality:
  min_score: 0.60
  archive_threshold: 0.50
  weights:
    engagement: 0.40
    freshness: 0.30
    diversity: 0.20
    recency: 0.10

automation:
  auto_add_successful: true
  auto_archive_old: true
  min_auto_add_likes: 100
  max_sample_age_days: 180
```

## Troubleshooting

**Too many low-freshness warnings:**
```python
# Lower thresholds temporarily
monitor.set_threshold("gm", 0.60)
```

**Quality scores too low:**
```bash
# Add more high-quality samples
python scripts/manage_training.py import \
  --file best_tweets.json \
  --min-likes 150
```

**Not enough diversity:**
```python
# Get diversity report
report = learning.diversity_report()
# Follow recommendations to add underrepresented topics
```

## Related Documentation

- [FRESHNESS_SYSTEM.md](FRESHNESS_SYSTEM.md) - Detailed freshness algorithm
- [LEARNING_GUIDE.md](LEARNING_GUIDE.md) - Continuous learning guide
- [Training Data Examples](../twitter-content-ai/training_data/)

## Related Skills

- [twitter-content-ai](../twitter-content-ai/SKILL.md) - Uses training data for generation
- [social-monitoring](../social-monitoring/SKILL.md) - Identifies high-performing content

---

**Goal**: Maintain 85%+ freshness score across all training data with continuous improvement.
