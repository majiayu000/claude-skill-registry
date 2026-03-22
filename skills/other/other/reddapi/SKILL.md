---
name: reddapi
description: Use this skill to access Reddit's full data archive via reddapi.dev API. Features semantic search, subreddit discovery, and real-time trend analysis. Perfect for market research, competitive analysis, and niche opportunity discovery.
license: MIT
keywords:
  - reddit
  - api
  - search
  - market-research
  - niche-discovery
  - social-media
---

# reddapi.dev Skill

## Overview

Access **Reddit's complete data archive** through reddapi.dev's powerful API. This skill provides semantic search, subreddit discovery, and trend analysis capabilities.

## Key Features

### 🔍 Semantic Search
Natural language search across millions of Reddit posts and comments.

```bash
# Search for user pain points
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "best productivity tools for remote teams", "limit": 100}'

# Find complaints and frustrations
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "frustrations with current TOOL_NAME", "limit": 100}'
```

### 📊 Trends API
Discover trending topics with engagement metrics.

```bash
# Get trending topics
curl "https://reddapi.dev/api/v1/trends" \
  -H "Authorization: Bearer $REDDAPI_API_KEY"
```

Response includes:
- `post_count`: Number of posts
- `total_upvotes`: Engagement score
- `avg_sentiment`: Sentiment analysis (-1 to 1)
- `trending_keywords`: Top keywords
- `growth_rate`: Trend momentum

### 📝 Subreddit Discovery

```bash
# List popular subreddits
curl "https://reddapi.dev/api/subreddits?limit=100" \
  -H "Authorization: Bearer $REDDAPI_API_KEY"

# Get specific subreddit info
curl "https://reddapi.dev/api/subreddits/programming" \
  -H "Authorization: Bearer $REDDAPI_API_KEY"
```

## Use Cases

### Market Research
```bash
# Analyze competitor discussions
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "COMPETITOR problems complaints", "limit": 200}'
```

### Niche Discovery
```bash
# Find underserved user needs
curl -X POST "https://reddapi.dev/api/v1/search/semantic" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" \
  -d '{"query": "I wish there was an app that", "limit": 100}'
```

### Trend Analysis
```bash
# Monitor topic growth
curl "https://reddapi.dev/api/v1/trends" \
  -H "Authorization: Bearer $REDDAPI_API_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for trend in data.get('data', {}).get('trends', []):
    print(f\"{trend['topic']}: {trend['growth_rate']}% growth\")
"
```

## Response Format

### Search Results
```json
{
  "success": true,
  "results": [
    {
      "id": "post123",
      "title": "User post title",
      "selftext": "Post content...",
      "subreddit": "r/somesub",
      "score": 1234,
      "num_comments": 89,
      "created_utc": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 15000
}
```

### Trends Response
```json
{
  "success": true,
  "data": {
    "trends": [
      {
        "topic": "AI regulation",
        "post_count": 1247,
        "total_upvotes": 45632,
        "avg_sentiment": 0.42,
        "growth_rate": 245.3
      }
    ]
  }
}
```

## Environment Variables

```bash
export REDDAPI_API_KEY="your_api_key"
```

Get your API key at: https://reddapi.dev

## Related Skills

- **niche-hunter**: Automated opportunity discovery
- **market-analysis**: Comprehensive research workflows
