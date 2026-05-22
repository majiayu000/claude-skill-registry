---
name: posting-twitter
description: |
  Post content to Twitter/X using Twitter API v2.
  Use when publishing tweets, creating threads, searching mentions,
  or getting timeline analytics. Supports media and replies.
  NOT when posting to other platforms.
---

# Twitter/X Poster Skill

Automated Twitter posting via Twitter API v2.

## Quick Start

```bash
# Post a tweet
python scripts/run.py --post "Your tweet here"

# Create a thread
python scripts/run.py --thread "Tweet 1" "Tweet 2" "Tweet 3"

# Reply to tweet
python scripts/run.py --post "Reply text" --reply-to TWEET_ID

# Search mentions
python scripts/run.py --search "@yourusername"

# Get insights
python scripts/run.py --insights --days 7

# Verify setup
python scripts/verify.py
```

## Setup

### 1. Get Twitter API Credentials

1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create an App
3. Generate API keys and tokens:
   - API Key & Secret
   - Access Token & Secret
   - Bearer Token
4. Enable OAuth 2.0

### 2. Configure Environment

Add to `.env` (use your Twitter credentials):
```
TWITTER_API_KEY=your_consumer_key_here
TWITTER_API_SECRET=your_consumer_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here
```

**Note:** Twitter calls it "Consumer Key" - that's your API Key.

## Features

### Posting
- Single tweets (280 characters)
- Threads (multiple connected tweets)
- Replies to other tweets
- Approval workflow (default)
- Rate limiting (50 tweets/day, 10/hour)

### Analytics
- Tweet performance
- Engagement metrics
- Timeline insights
- Mentions tracking

### Thread Creation
- Automatically chains tweets
- Each tweet links to previous
- Up to 25 tweets per thread

## Twitter Best Practices

- **Length:** Max 280 characters
- **Hashtags:** 1-3 focused hashtags
- **Threads:** Break long content into 3-5 tweets
- **Timing:** Post during peak engagement hours

## Approval Workflow

Posts/threads create files in `Vault/Pending_Approval/`:
- Review all tweets in thread
- Edit as needed
- Move to `Vault/Approved/` to publish

## Rate Limits

- **Daily:** 50 tweets
- **Hourly:** 10 tweets

Automatically enforced by MCP server.

## Verification

Run: `python scripts/verify.py`

Expected: `✓ posting-twitter valid`

## References

- [Twitter API v2 Docs](https://developer.twitter.com/en/docs/twitter-api)
- [Tweet Creation](https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/introduction)
