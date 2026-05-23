---
name: social-sentiment-analyzer
version: 2026-02-24
description: Analyze brand or topic sentiment across Twitter, Reddit, and Instagram using Xpoz. Classifies posts as positive/neutral/negative, extracts recurring themes, and generates a sentiment report. Use when asked for "sentiment analysis", "what are people saying about X", "brand sentiment", or "social media opinion on X".
---

# Social Sentiment Analyzer

## Overview

Analyze public sentiment for any brand, product, or topic across Twitter/X, Reddit, and Instagram. Fetches real posts, classifies sentiment, extracts themes, and produces a structured report.

## When to Use

Activate when the user asks:
- "What's the sentiment around [TOPIC]?"
- "Analyze sentiment for [BRAND] on Twitter"
- "What are people saying about [PRODUCT] on social media?"
- "Is the reaction to [EVENT] positive or negative?"
- "Social media opinion on [TOPIC]"

## Setup & Authentication

Before fetching data, ensure Xpoz access is configured. Follow these checks in order.

### Check 1: Already authenticated?

**If you have MCP tools**, try calling any Xpoz tool (e.g., `checkAccessKeyStatus`). If it works → skip to Step 1.

**If you have the SDK**, try:
```python
from xpoz import XpozClient
client = XpozClient()  # reads XPOZ_API_KEY env var
```
If this succeeds without error → skip to Step 1.

If neither works, you need to authenticate. Choose the path that fits your environment:

---

### Path A: MCP via mcporter (OpenClaw agents)

If `mcporter` is available:

```bash
mcporter call xpoz.checkAccessKeyStatus
```

If `hasAccessKey: true` → ready. If not:

```bash
mcporter config add xpoz https://mcp.xpoz.ai/mcp --auth oauth
```

Then authenticate — generate the OAuth URL and send it to the user:

**Step 1: Generate authorization URL**
```python
import secrets, hashlib, base64, urllib.parse, json, urllib.request, os

verifier = secrets.token_urlsafe(64)
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
state = secrets.token_urlsafe(32)

# Dynamic client registration
reg_req = urllib.request.Request(
    'https://mcp.xpoz.ai/oauth/register',
    data=json.dumps({
        'client_name': 'Agent Skills',
        'redirect_uris': ['https://www.xpoz.ai/oauth/openclaw'],
        'grant_types': ['authorization_code'],
        'response_types': ['code'],
        'token_endpoint_auth_method': 'none',
    }).encode(),
    headers={'Content-Type': 'application/json'},
)
reg_resp = json.loads(urllib.request.urlopen(reg_req).read())

params = urllib.parse.urlencode({
    'response_type': 'code',
    'client_id': reg_resp['client_id'],
    'code_challenge': challenge,
    'code_challenge_method': 'S256',
    'redirect_uri': 'https://www.xpoz.ai/oauth/openclaw',
    'state': state,
    'scope': 'mcp:tools',
    'resource': 'https://mcp.xpoz.ai/',
})

auth_url = 'https://mcp.xpoz.ai/oauth/authorize?' + params

# Save state for token exchange
os.makedirs(os.path.expanduser('~/.cache/xpoz-oauth'), exist_ok=True)
with open(os.path.expanduser('~/.cache/xpoz-oauth/state.json'), 'w') as f:
    json.dump({'verifier': verifier, 'state': state, 'client_id': reg_resp['client_id'],
               'redirect_uri': 'https://www.xpoz.ai/oauth/openclaw'}, f)

print(auth_url)
```

**Step 2: Send the URL to the user**

Tell them:
> "I need to connect to Xpoz for social media data. Please open this link and sign in:
>
> [auth_url]
>
> After authorizing, you'll see a code. Paste it back to me here."

**Step 3: WAIT for the user to reply with the code.** Do not proceed until they respond.

**Step 4: Exchange the code for a token**

Once the user provides the code (either a raw code or a URL containing `?code=...`), extract the code and exchange it:

```python
import json, urllib.request, urllib.parse, subprocess, os

with open(os.path.expanduser('~/.cache/xpoz-oauth/state.json')) as f:
    oauth = json.load(f)

code = "THE_CODE_FROM_USER"  # Extract from user's reply

data = urllib.parse.urlencode({
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': oauth['redirect_uri'],
    'client_id': oauth['client_id'],
    'code_verifier': oauth['verifier'],
}).encode()

req = urllib.request.Request(
    'https://mcp.xpoz.ai/oauth/token',
    data=data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
)
resp = json.loads(urllib.request.urlopen(req).read())
token = resp['access_token']

# Configure mcporter with the token (token is never printed)
subprocess.run(['mcporter', 'config', 'remove', 'xpoz'], capture_output=True)
subprocess.run(['mcporter', 'config', 'add', 'xpoz', 'https://mcp.xpoz.ai/mcp',
                '--header', f'Authorization=Bearer {token}'], check=True)

# Clean up
os.remove(os.path.expanduser('~/.cache/xpoz-oauth/state.json'))
print("Xpoz configured successfully")
```

**Step 5: Verify** with `mcporter call xpoz.checkAccessKeyStatus` → should return `hasAccessKey: true`.

---

### Path B: MCP via Claude Code config

For Claude Code users without mcporter, add to `~/.claude.json`:
```json
{
  "mcpServers": {
    "xpoz": {
      "url": "https://mcp.xpoz.ai/mcp",
      "transport": "http-stream"
    }
  }
}
```
Claude Code handles OAuth automatically on first tool call — the user just needs to authorize in their browser when prompted.

---

### Path C: SDK (Python or TypeScript)

Ask the user:
> "I need a Xpoz API key to access social media data. Please go to https://xpoz.ai/get-token (it's free, no credit card needed) and paste the key back to me."

**WAIT for the user to reply with the key.** Then:

**Python:**
```bash
pip install xpoz
```
```python
from xpoz import XpozClient
client = XpozClient("THE_KEY_FROM_USER")
```

**TypeScript:**
```bash
npm install @xpoz/xpoz
```
```typescript
import { XpozClient } from "@xpoz/xpoz";
const client = new XpozClient({ apiKey: "THE_KEY_FROM_USER" });
await client.connect();
```

Or set the environment variable and use the default constructor:
```bash
export XPOZ_API_KEY=THE_KEY_FROM_USER
```

---

### Auth Errors
| Problem | Solution |
|---------|----------|
| MCP: "Unauthorized" | Re-run the OAuth flow above |
| SDK: `AuthenticationError` | Verify key at [xpoz.ai/settings](https://xpoz.ai/settings) |
| Token exchange fails | Ask user to re-authorize — codes are single-use |


## Step-by-Step Instructions

### Step 1: Parse the Request

Extract from the user's message:
- **Topic/brand** to analyze
- **Platforms** to search (default: Twitter + Reddit; add Instagram if relevant)
- **Time period** (default: last 7 days)
- **Language** filter (default: English)

Expand the query for better coverage:
- Publicly traded companies → include ticker symbol: `"Tesla" OR "$TSLA"`
- Products → include common abbreviations: `"ChatGPT" OR "GPT-4"`
- Events → include hashtags: `"CES 2026" OR "#CES2026"`

### Step 2: Fetch Posts

#### Via MCP (if xpoz MCP server is configured)

**Twitter:**
```
Call getTwitterPostsByKeywords:
  query: "<expanded query>"
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount", "impressionCount"]
  startDate: "<7 days ago, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
  language: "en"
```

**Reddit:**
```
Call getRedditPostsByKeywords:
  query: "<expanded query>"
  fields: ["id", "title", "text", "authorUsername", "createdAtDate", "score", "numComments", "subreddit"]
  startDate: "<7 days ago>"
  endDate: "<today>"
```

**Instagram (if requested):**
```
Call getInstagramPostsByKeywords:
  query: "<expanded query>"
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "commentCount"]
  startDate: "<7 days ago>"
  endDate: "<today>"
```

**CRITICAL: Async Pattern** — Each call returns an `operationId`. You MUST call `checkOperationStatus` with that ID and poll until status is "completed" (up to 8 retries, ~5 seconds apart).

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()  # Uses XPOZ_API_KEY env var

# Twitter
twitter_results = client.twitter.search_posts(
    '"Tesla" OR "$TSLA"',
    start_date="2026-02-16",
    end_date="2026-02-23",
    language="en",
    fields=["id", "text", "author_username", "created_at_date", "like_count", "retweet_count"]
)

# Reddit
reddit_results = client.reddit.search_posts(
    '"Tesla" OR "$TSLA"',
    start_date="2026-02-16",
    end_date="2026-02-23",
    fields=["id", "title", "text", "author_username", "created_at_date", "score", "num_comments", "subreddit"]
)

# Collect all posts
twitter_posts = twitter_results.data
reddit_posts = reddit_results.data

# Fetch additional pages if needed
while twitter_results.has_next_page():
    twitter_results = twitter_results.next_page()
    twitter_posts.extend(twitter_results.data)

client.close()
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const twitterResults = await client.twitter.searchPosts('"Tesla" OR "$TSLA"', {
  startDate: "2026-02-16",
  endDate: "2026-02-23",
  language: "en",
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount"],
});

const redditResults = await client.reddit.searchPosts('"Tesla" OR "$TSLA"', {
  startDate: "2026-02-16",
  endDate: "2026-02-23",
  fields: ["id", "title", "text", "authorUsername", "createdAtDate", "score", "numComments", "subreddit"],
});

await client.close();
```

### Step 3: Classify Sentiment

For each post, classify into one of 5 levels:

| Level | Indicators |
|-------|-----------|
| **Positive** | "love", "amazing", "bullish", "great", "best", 🚀🔥💪, strong praise |
| **Leaning Positive** | "looking good", "solid", "promising", measured optimism |
| **Neutral** | Questions, factual statements, news without opinion, balanced takes |
| **Leaning Negative** | "worried", "not sure", "concerned", "some issues", cautious criticism |
| **Negative** | "terrible", "worst", "avoid", "bearish", 📉💀, strong criticism |

**Tips:**
- Sarcasm detection: "Great, another outage" → Negative
- Retweets/quotes with no commentary → Neutral
- Engagement-weighted: high-engagement posts carry more signal

### Step 4: Extract Themes

Identify 5-8 recurring themes from the posts. For each theme:
- **Title**: 3-5 word label
- **Sentiment**: overall lean of posts in this theme
- **Key quotes**: 2-3 representative posts
- **Volume**: approximate % of total posts

### Step 5: Generate Report

Present results in this structure:

```
## Sentiment Report: [TOPIC]
**Period:** [start] to [end] | **Posts analyzed:** [count]

### Overall Sentiment
Score: [0-100, where 50=neutral, 100=max positive]
- Positive: X%
- Neutral: X%
- Negative: X%

### Platform Breakdown
| Platform | Posts | Sentiment Score | Top Theme |
|----------|-------|----------------|-----------|
| Twitter  | X     | X              | ...       |
| Reddit   | X     | X              | ...       |

### Key Themes
1. **[Theme Title]** (Positive/Neutral/Negative)
   [2-3 sentence explanation with example quotes]

2. **[Theme Title]** ...

### Notable Posts
[Top 5 highest-engagement posts with text, author, and metrics]

### Summary
[2-3 paragraph executive summary with actionable insights]
```

## Example Prompts

- "Analyze sentiment around NVIDIA this week on Twitter and Reddit"
- "What's the social media reaction to the new iPhone?"
- "How are people feeling about Cursor IDE on Reddit?"
- "Sentiment analysis for Bitcoin in the last 30 days"

## Notes

- Free tier: 100,000 results/month at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=social-sentiment-analyzer)
- For large datasets, use CSV export (`export_csv()` / `exportCsv()`) and analyze locally
- Reddit tends to have longer, more nuanced opinions; Twitter has higher volume but shorter takes
