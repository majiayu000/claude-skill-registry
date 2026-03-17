---
name: social-monitoring
description: Monitor Twitter accounts (151 tracked), detect mentions, analyze engagement, and identify interaction opportunities. Use when tracking Twitter activity, monitoring mentions, analyzing social metrics, or managing social media presence.
allowed-tools: Read, Write, Bash(python:*)
model: claude-sonnet-4-20250514
---

# Social Monitoring

Comprehensive Twitter monitoring system tracking 151 accounts across 6 ecosystems with intelligent interaction prioritization.

## Overview

Monitor and analyze Twitter activity to:
- **Track 151 key accounts** across Codatta, Base, x402, AI/Data, Crypto, and Milady ecosystems
- **Detect mentions** in real-time
- **Identify interaction opportunities** with priority scoring
- **Analyze engagement metrics** (likes, retweets, replies)
- **Automate monitoring** with scheduled checks

## Quick Start

### 1. Configure Twitter API

```bash
# Set Twitter API credentials
export TWITTER_API_KEY="your_api_key"
export TWITTER_API_SECRET="your_api_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_SECRET="your_access_secret"
```

### 2. Run Monitor

```python
from src.twitter_monitor import TwitterMonitor

monitor = TwitterMonitor()

# Check for new mentions
mentions = monitor.check_mentions()

# Monitor specific account
activity = monitor.monitor_account("@codatta_io")

# Get interaction opportunities
opportunities = monitor.find_opportunities()
```

## Account Matrix

### 151 Tracked Accounts (6 Categories)

| Category | Count | Priority | Auto-Interact |
|----------|-------|----------|---------------|
| **Must Interact** | 4 | 100 | Always |
| **Base Ecosystem** | 25 | 85-90 | High |
| **x402/8004 Community** | 30 | 80-85 | High |
| **AI/Data Industry** | 20 | 70-80 | Medium |
| **Crypto KOLs** | 30 | 60-75 | Medium |
| **Milady Community** | 42 | 50-70 | Low-Medium |

### Must Interact (Priority 100)

**Always respond within 1 hour:**

```json
{
  "must_interact": [
    {"handle": "@codatta_io", "priority": 100, "role": "company"},
    {"handle": "@drtwo101", "priority": 100, "role": "founder"},
    {"handle": "@qiw", "priority": 100, "role": "founder"},
    {"handle": "@ddcrying", "priority": 100, "role": "team"}
  ]
}
```

### Base Ecosystem (Priority 85-90)

**Respond to 70-80% of relevant posts:**

- @base - Base official account (90)
- @jesseb_base - Jesse (Base founder) (90)
- @buildonbase - Base developer account (85)
- @0xwitchy - Witchy.eth (85)
- @zksync - zkSync (85)
- Plus 20 more Base builders...

### x402/8004 Community (Priority 80-85)

**Respond to 60-70% of relevant posts:**

- Community members holding x402 token
- Active in x402 ecosystem discussions
- Codatta early adopters

### AI/Data Industry (Priority 70-80)

**Monitor for opportunities to discuss data ownership:**

- @sama - Sam Altman (80)
- @ylecun - Yann LeCun (80)
- @karpathy - Andrej Karpathy (75)
- @AnthropicAI - Anthropic (75)
- AI researchers and companies

### Crypto KOLs (Priority 60-75)

**Engage on relevant topics:**

- Major crypto influencers
- DeFi builders
- Web3 thought leaders

### Milady Community (Priority 50-70)

**Selective engagement:**

- Fellow Milady holders
- Milady culture creators
- Remilio/Charlotte community

## Monitoring Features

### 1. Mention Detection

```python
monitor = TwitterMonitor()

# Check for new mentions
mentions = monitor.check_mentions(
    since_id="last_checked_id"  # Only new mentions
)

# Returns:
[
  {
    "id": "1234567890",
    "author": "@someone",
    "text": "@jessie what do you think about...",
    "created_at": "2026-01-07T10:30:00Z",
    "metrics": {"likes": 10, "retweets": 2}
  }
]
```

### 2. Account Monitoring

```python
# Monitor specific account's recent activity
activity = monitor.monitor_account(
    handle="@codatta_io",
    hours=24  # Last 24 hours
)

# Returns recent tweets, engagement metrics
```

### 3. Keyword Tracking

```python
# Track specific keywords
tweets = monitor.track_keywords(
    keywords=["data ownership", "AI ethics", "x402"],
    hours=24
)
```

### 4. Interaction Opportunities

```python
# Find tweets worth interacting with
opportunities = monitor.find_opportunities(
    min_priority=70,  # Only high priority
    max_results=20
)

# Returns ranked list of tweets to potentially reply to
```

## Interaction Rules

### Priority Scoring Algorithm

```python
def calculate_priority(tweet):
    """Calculate interaction priority (0-100)"""

    score = 0

    # 1. Account priority (0-100)
    score += account_priority[tweet.author]

    # 2. Mention bonus (+50)
    if "@jessie" in tweet.text:
        score += 50

    # 3. Topic relevance (0-20)
    if has_codatta_keywords(tweet.text):
        score += 20
    elif has_base_keywords(tweet.text):
        score += 15
    elif has_data_keywords(tweet.text):
        score += 10

    # 4. Engagement bonus (0-15)
    if tweet.likes > 500:
        score += 15
    elif tweet.likes > 100:
        score += 10
    elif tweet.likes > 50:
        score += 5

    # 5. Recency bonus (0-10)
    if hours_ago(tweet) < 1:
        score += 10
    elif hours_ago(tweet) < 6:
        score += 5

    return min(score, 100)
```

### Interaction Decision Tree

```
Is it from Must Interact account? → YES (100%) → Reply
                                  ↓
Is it an @mention? → YES (100%) → Reply
                   ↓
Priority score > 80? → YES (70-80%) → Reply
                     ↓
Priority score 60-80? → YES (40-60%) → Maybe reply
                       ↓
Priority score < 60? → NO (10-20%) → Monitor only
```

## Usage Examples

### Example 1: Daily Monitoring Routine

```python
from src.twitter_monitor import TwitterMonitor

monitor = TwitterMonitor()

# Morning routine
def morning_check():
    print("Checking mentions...")
    mentions = monitor.check_mentions()

    print("Checking must-interact accounts...")
    for account in ["@codatta_io", "@drtwo101", "@qiw"]:
        activity = monitor.monitor_account(account, hours=24)
        print(f"{account}: {len(activity)} new tweets")

    print("Finding opportunities...")
    opportunities = monitor.find_opportunities(min_priority=70)
    print(f"Found {len(opportunities)} high-priority opportunities")

    return {
        "mentions": mentions,
        "opportunities": opportunities
    }

results = morning_check()
```

### Example 2: Real-Time Mention Response

```python
# Set up real-time monitoring
def monitor_mentions_realtime():
    """Check for mentions every 5 minutes"""

    while True:
        mentions = monitor.check_mentions()

        for mention in mentions:
            print(f"New mention from {mention['author']}")

            # Generate reply (using twitter-content-ai skill)
            from skills.twitter_content_ai.src.content_generator import ContentGenerator

            generator = ContentGenerator()
            reply = generator.generate_reply(
                original_tweet=mention['text'],
                author=mention['author']
            )

            print(f"Suggested reply: {reply}")

        time.sleep(300)  # 5 minutes
```

### Example 3: Ecosystem Tracking

```python
# Track Base ecosystem activity
def track_base_ecosystem():
    """Monitor all Base ecosystem accounts"""

    base_accounts = monitor.get_accounts_by_category("base_ecosystem")

    activity_report = {}

    for account in base_accounts:
        tweets = monitor.monitor_account(account['handle'], hours=24)

        # Filter for high engagement
        high_engagement = [
            t for t in tweets
            if t['metrics']['likes'] > 100
        ]

        activity_report[account['handle']] = {
            "total_tweets": len(tweets),
            "high_engagement": len(high_engagement),
            "top_tweet": max(tweets, key=lambda t: t['metrics']['likes'])
        }

    return activity_report
```

## Analytics Features

### Engagement Metrics

```python
# Get engagement metrics for tracked accounts
metrics = monitor.get_engagement_metrics(
    accounts=["@codatta_io", "@base"],
    days=7
)

# Returns:
{
  "@codatta_io": {
    "avg_likes": 50,
    "avg_retweets": 10,
    "total_tweets": 15,
    "growth": "+5%"
  },
  "@base": {
    "avg_likes": 500,
    "avg_retweets": 100,
    "total_tweets": 20,
    "growth": "+10%"
  }
}
```

### Trending Topics

```python
# Find trending topics in tracked accounts
trending = monitor.find_trending_topics(
    category="base_ecosystem",
    hours=24
)

# Returns:
{
  "topics": [
    {"topic": "onchain summer", "mentions": 15},
    {"topic": "base builders", "mentions": 12}
  ]
}
```

### Interaction History

```python
# Track your interaction history
history = monitor.get_interaction_history(days=7)

# Returns:
{
  "total_interactions": 45,
  "by_category": {
    "must_interact": 10,
    "base_ecosystem": 15,
    "x402_community": 10,
    "ai_data": 5,
    "crypto_kols": 3,
    "milady": 2
  },
  "avg_response_time": "2.5 hours"
}
```

## Configuration

### Account Configuration File

Located in: `config/accounts.json`

```json
{
  "must_interact": [
    {
      "handle": "@codatta_io",
      "priority": 100,
      "role": "company",
      "auto_interact": true,
      "notification": "instant"
    }
  ],
  "base_ecosystem": [
    {
      "handle": "@base",
      "priority": 90,
      "role": "platform",
      "auto_interact": false,
      "keywords": ["onchain", "base", "builders"]
    }
  ]
}
```

### Monitoring Settings

```python
# config/monitoring_config.yaml
monitoring:
  check_interval: 300  # 5 minutes
  mention_priority: 100
  min_interaction_priority: 70
  max_daily_interactions: 30

rate_limits:
  tweets_per_hour: 50
  api_calls_per_hour: 500

notifications:
  email: true
  webhook: true
  lark: true
```

## Automation

### Scheduled Monitoring

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

# Check mentions every 5 minutes
scheduler.add_job(
    func=monitor.check_mentions,
    trigger="interval",
    minutes=5
)

# Generate daily report every morning at 9am
scheduler.add_job(
    func=monitor.generate_daily_report,
    trigger="cron",
    hour=9,
    minute=0
)

scheduler.start()
```

### Alert System

```python
# Set up alerts for high-priority events
monitor.set_alert(
    event="mention_from_must_interact",
    action="send_notification",
    channels=["lark", "email"]
)

monitor.set_alert(
    event="viral_tweet_about_codatta",
    condition=lambda t: t['likes'] > 1000,
    action="send_notification"
)
```

## Twitter Client Integration

### Basic Twitter Operations

```python
from src.twitter_client import TwitterClient

client = TwitterClient()

# Get user info
user = client.get_user("@codatta_io")

# Get recent tweets
tweets = client.get_user_tweets(
    user_id=user['id'],
    max_results=10
)

# Search tweets
results = client.search_tweets(
    query="data ownership",
    max_results=20
)

# Post tweet
client.post_tweet("gm from monitoring system 🎀")

# Reply to tweet
client.reply_to_tweet(
    tweet_id="1234567890",
    text="Great point about data ownership!"
)
```

### Rate Limit Handling

```python
# Auto-handles rate limits
try:
    tweets = client.get_user_tweets(user_id, max_results=100)
except RateLimitError as e:
    print(f"Rate limited. Reset at: {e.reset_time}")
    # Automatically waits and retries
```

## Dashboard (Optional)

```python
# Generate monitoring dashboard
dashboard = monitor.generate_dashboard()

# Returns HTML dashboard with:
# - Recent mentions
# - High-priority opportunities
# - Engagement metrics
# - Trending topics
# - Interaction history

dashboard.save("monitor_dashboard.html")
```

## Best Practices

1. **Check mentions frequently** - Every 5-15 minutes for must-interact accounts
2. **Prioritize quality over quantity** - Better to have 10 meaningful interactions than 50 generic ones
3. **Track engagement patterns** - Learn when your audience is most active
4. **Update account lists regularly** - Add new important accounts, remove inactive ones
5. **Monitor competitor activity** - Learn from successful accounts in your space
6. **Set reasonable limits** - Don't over-interact (max 30-40 per day)
7. **Use analytics** - Review weekly metrics to improve strategy

## Troubleshooting

**Rate limits exceeded:**
```python
# Use rate limit buffer
monitor = TwitterMonitor(rate_limit_buffer=0.8)  # Use only 80% of limit
```

**Missing mentions:**
```python
# Increase check frequency
monitor.set_check_interval(minutes=3)
```

**Too many notifications:**
```python
# Increase priority threshold
monitor.set_min_notify_priority(90)  # Only notify for 90+ priority
```

## Related Documentation

- [ACCOUNT_MATRIX.md](ACCOUNT_MATRIX.md) - Complete list of 151 accounts
- [INTERACTION_RULES.md](INTERACTION_RULES.md) - Detailed interaction rules
- [Twitter API Docs](https://developer.twitter.com/en/docs)

## Related Skills

- [twitter-content-ai](../twitter-content-ai/SKILL.md) - Generate replies
- [lark-bot-integration](../lark-bot-integration/SKILL.md) - Send alerts to Lark

---

**Cost**: Twitter API v2 is free for basic tier (500k tweets/month)
