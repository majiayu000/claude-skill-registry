---
name: xpoz-social-tracking
version: 2026-06-10
description: Set up and manage social media tracking across Twitter, Instagram, Reddit, and TikTok using Xpoz. Add, remove, and view tracked keywords, users, subreddits, and hashtags. Use when asked to "track mentions", "monitor brand", "set up tracking", "add tracked item", "what am I tracking", "stop tracking", "remove tracked", or "social monitoring".
allowed-tools: Bash(xpoz-cli *)
---

# Social Media Tracking

## Overview

Tracking is a best practice for getting more complete data from Xpoz. When you track a keyword, user, subreddit, or hashtag, Xpoz continuously collects data for those items in the background. This means:

- **More complete data:** Tracked items accumulate data over time, giving you a fuller picture than one-off queries.
- **Better coverage:** Continuous collection captures posts and activity that a single point-in-time query might miss.

You can track four types of items across platforms:
- **Keywords** — Track any phrase or topic (e.g., "AI agents", "your brand name"). Xpoz continuously collects posts matching these keywords across the platforms you specify.
- **Users** — Track specific accounts (e.g., a competitor, influencer, or your own brand handle). Xpoz collects their posts and activity.
- **Subreddits** (Reddit only) — Track entire subreddit communities to monitor discussions.
- **Hashtags** (TikTok only) — Track TikTok hashtags to follow trends and campaigns.

## When to Use
- "Track mentions of [BRAND] across social media"
- "Set up monitoring for [KEYWORD] on Twitter and Reddit"
- "What keywords am I currently tracking?"
- "Add @competitor to my tracked users on Instagram"
- "Monitor #AIagents on TikTok"
- "Stop tracking [OLD KEYWORD]"
- "How many tracked items can I add?"

## Step 1: Check Current Tracking

First, see what's already being tracked.

### Via MCP
```
Call getTrackedItems
```

### Via Python SDK
```python
from xpoz import XpozClient

client = XpozClient()
items = client.tracking.get_tracked_items()
for item in items:
    print(f"[{item.platform}] {item.type}: {item.phrase}")
client.close()
```

### Via TypeScript SDK
```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();
const items = await client.tracking.getTrackedItems();
items.forEach(item => console.log(`[${item.platform}] ${item.type}: ${item.phrase}`));
await client.close();
```

### Via CLI
```bash
xpoz-cli tracking get_tracked_items
```

Present results as a table:
| Platform | Type | Phrase |
|----------|------|--------|
| twitter | keyword | AI agents |
| instagram | user | competitor_brand |
| reddit | subreddit | machinelearning |

## Step 2: Add Tracked Items

### Supported Types per Platform

| Platform | keyword | user | subreddit | hashtag |
|----------|---------|------|-----------|---------|
| Twitter | Yes | Yes | — | — |
| Instagram | Yes | Yes | — | — |
| Reddit | Yes | Yes | Yes | — |
| TikTok | Yes | Yes | — | Yes |

### Via MCP
```
Call addTrackedItems with items:
  [
    { "phrase": "AI agents", "type": "keyword", "platform": "twitter" },
    { "phrase": "AI agents", "type": "keyword", "platform": "reddit" },
    { "phrase": "competitor_user", "type": "user", "platform": "instagram" },
    { "phrase": "machinelearning", "type": "subreddit", "platform": "reddit" },
    { "phrase": "aitools", "type": "hashtag", "platform": "tiktok" }
  ]
```

### Via Python SDK
```python
client.tracking.add_tracked_items([
    {"phrase": "AI agents", "type": "keyword", "platform": "twitter"},
    {"phrase": "AI agents", "type": "keyword", "platform": "reddit"},
    {"phrase": "competitor_user", "type": "user", "platform": "instagram"},
    {"phrase": "machinelearning", "type": "subreddit", "platform": "reddit"},
    {"phrase": "aitools", "type": "hashtag", "platform": "tiktok"},
])
```

### Via TypeScript SDK
```typescript
await client.tracking.addTrackedItems([
  { phrase: "AI agents", type: "keyword", platform: "twitter" },
  { phrase: "AI agents", type: "keyword", platform: "reddit" },
  { phrase: "competitor_user", type: "user", platform: "instagram" },
  { phrase: "machinelearning", type: "subreddit", platform: "reddit" },
  { phrase: "aitools", type: "hashtag", platform: "tiktok" },
]);
```

### Via CLI
```bash
xpoz-cli tracking add_tracked_items \
  --items '[{"phrase": "AI agents", "type": "keyword", "platform": "twitter"}, {"phrase": "AI agents", "type": "keyword", "platform": "reddit"}, {"phrase": "competitor_user", "type": "user", "platform": "instagram"}]'
```

**Important:** Call `getAccountDetails` to check available tracked item slots before adding.

## Step 3: Remove Tracked Items

### Via MCP
```
Call removeTrackedItems with items:
  [{ "phrase": "old keyword", "type": "keyword", "platform": "twitter" }]
```

### Via Python SDK
```python
client.tracking.remove_tracked_items([
    {"phrase": "old keyword", "type": "keyword", "platform": "twitter"},
])
```

### Via TypeScript SDK
```typescript
await client.tracking.removeTrackedItems([
  { phrase: "old keyword", type: "keyword", platform: "twitter" },
]);
```

### Via CLI
```bash
xpoz-cli tracking remove_tracked_items \
  --items '[{"phrase": "old keyword", "type": "keyword", "platform": "twitter"}]'
```

**Tip:** Call `getTrackedItems` first to see exact phrases and platforms before removing.

## Tracking Item Format

| Field | Type | Description | Valid Values |
|-------|------|-------------|-------------|
| phrase | string | The keyword, username, subreddit name, or hashtag to track | Any string |
| type | string | What kind of item | "keyword", "user", "subreddit" (Reddit only), "hashtag" (TikTok only) |
| platform | string | Which platform | "twitter", "instagram", "reddit", "tiktok" |

## Common Workflows

### Track a Brand Across All Platforms
```
items: [
  { phrase: "YourBrand", type: "keyword", platform: "twitter" },
  { phrase: "YourBrand", type: "keyword", platform: "instagram" },
  { phrase: "YourBrand", type: "keyword", platform: "reddit" },
  { phrase: "YourBrand", type: "keyword", platform: "tiktok" },
  { phrase: "yourbrand", type: "user", platform: "twitter" },
  { phrase: "yourbrand", type: "user", platform: "instagram" }
]
```

### Track Keywords for Market Research
```
items: [
  { phrase: "AI agents", type: "keyword", platform: "twitter" },
  { phrase: "AI agents", type: "keyword", platform: "reddit" },
  { phrase: "AI agents", type: "keyword", platform: "tiktok" },
  { phrase: "LLM tools", type: "keyword", platform: "twitter" },
  { phrase: "LLM tools", type: "keyword", platform: "reddit" }
]
```

### Monitor a Competitor
```
items: [
  { phrase: "competitor_handle", type: "user", platform: "twitter" },
  { phrase: "competitor_handle", type: "user", platform: "instagram" },
  { phrase: "CompetitorName", type: "keyword", platform: "reddit" }
]
```

### Track a Hashtag Campaign on TikTok
```
items: [
  { phrase: "yourcampaign", type: "hashtag", platform: "tiktok" },
  { phrase: "campaignvariant", type: "hashtag", platform: "tiktok" },
  { phrase: "your campaign", type: "keyword", platform: "twitter" }
]
```

### Set Up Subreddit Monitoring
```
items: [
  { phrase: "machinelearning", type: "subreddit", platform: "reddit" },
  { phrase: "artificial", type: "subreddit", platform: "reddit" },
  { phrase: "LocalLLaMA", type: "subreddit", platform: "reddit" }
]
```

## Notes

- **Tracking vs one-shot queries:** Tracking sets up continuous data collection for more comprehensive results. One-shot queries (like `getTwitterPostsByKeywords`) search existing cached data and may miss recent activity. Track items you care about for ongoing, complete data; use one-shot queries for ad-hoc research.
- **Data completeness:** Tracked items are crawled regularly, giving you more comprehensive data than untracked queries. This is especially impactful for fast-moving topics or competitive monitoring.
- **Data availability:** Tracked data accumulates over time. New tracked items won't have historical data — they start collecting from when you add them.

## See Also

- [xpoz-best-practices](../xpoz-best-practices/SKILL.md) — query syntax, pagination, field selection, full auth docs
- [social-sentiment-analyzer](../social-sentiment-analyzer/SKILL.md) — analyze sentiment of tracked topics
- [competitive-intel](../competitive-intel/SKILL.md) — compare brands you're tracking
- [xpoz-getting-started](../xpoz-getting-started/SKILL.md) — first-time setup and onboarding

## Example Prompts

- "Track mentions of 'Claude Code' on Twitter and Reddit"
- "What am I currently tracking?"
- "Add @openai to my tracked users on Twitter"
- "Set up monitoring for our brand across all platforms"
- "Monitor #sustainability on TikTok"
- "Stop tracking 'old product name' on all platforms"
- "How many tracked items do I have left?"
- "Track the r/LocalLLaMA subreddit"
