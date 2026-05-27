---
name: competitive-intel
version: 2026-02-24
description: Compare brands and products across social media — share of voice, sentiment, positioning, and audience overlap using Xpoz. Use when asked to "compare brands", "competitive analysis", "share of voice", "brand vs brand", or "competitive intelligence".
---

# Competitive Intelligence

## Overview

Compare multiple brands or products side by side across Twitter/X, Reddit, and Instagram. Measure share of voice, compare sentiment, identify positioning differences, and discover competitive advantages from real social conversations.

## When to Use

Activate when the user asks:
- "Compare [BRAND A] vs [BRAND B] on social media"
- "Share of voice: [BRAND] vs competitors"
- "Competitive analysis for [PRODUCT]"
- "How does [BRAND A] sentiment compare to [BRAND B]?"
- "What are people saying about [BRAND] vs [COMPETITOR]?"

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

Extract:
- **Primary brand** and **competitors** (2-5 brands total)
- **Platforms** (default: Twitter + Reddit)
- **Time period** (default: last 7 days)
- **Industry context** for better analysis

Build expanded queries for each brand:
- `"Slack"` → `"Slack" NOT "cut some slack" NOT "slack off"`
- `"Discord"` → `"Discord" NOT "sow discord" NOT "discord between"`
- For stocks: include ticker symbols

### Step 2: Fetch Data for Each Brand

Run parallel searches — one per brand, per platform.

#### Via MCP

For each brand, call:

**Twitter posts:**
```
Call getTwitterPostsByKeywords:
  query: "<brand query>"
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount", "impressionCount"]
  startDate: "<7 days ago>"
  endDate: "<today>"
  language: "en"
```

**Twitter users discussing the brand:**
```
Call getTwitterUsersByKeywords:
  query: "<brand query>"
  fields: ["id", "username", "name", "followersCount", "relevantTweetsCount", "relevantTweetsLikesSum"]
  startDate: "<7 days ago>"
```

**Reddit (for each brand):**
```
Call getRedditPostsByKeywords:
  query: "<brand query>"
  fields: ["id", "title", "text", "score", "numComments", "subreddit", "createdAtDate"]
  startDate: "<7 days ago>"
```

**CRITICAL:** Each call returns an `operationId` — poll `checkOperationStatus` until "completed".

**Tip:** Launch all brand searches in sequence, collect all operationIds, then poll them. This is faster than waiting for each one.

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

brands = {
    "Slack": '"Slack" NOT "cut some slack"',
    "Discord": '"Discord" NOT "sow discord"',
    "Teams": '"Microsoft Teams" OR "MS Teams"',
}

brand_data = {}

for brand_name, query in brands.items():
    # Twitter posts
    twitter = client.twitter.search_posts(
        query,
        start_date="2026-02-16",
        end_date="2026-02-23",
        language="en",
        fields=["id", "text", "author_username", "like_count", "retweet_count", "impression_count", "created_at_date"]
    )

    # Twitter users (for influencer overlap analysis)
    users = client.twitter.get_users_by_keywords(
        query,
        start_date="2026-02-16",
        fields=["username", "followers_count", "relevant_tweets_count", "relevant_tweets_likes_sum"]
    )

    # Reddit posts
    reddit = client.reddit.search_posts(
        query,
        start_date="2026-02-16",
        fields=["id", "title", "text", "score", "num_comments", "subreddit", "created_at_date"]
    )

    brand_data[brand_name] = {
        "twitter_posts": twitter,
        "twitter_users": users,
        "reddit_posts": reddit,
        "tweet_count": twitter.pagination.total_rows,
        "reddit_count": reddit.pagination.total_rows,
    }

client.close()
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const brands: Record<string, string> = {
  Slack: '"Slack" NOT "cut some slack"',
  Discord: '"Discord" NOT "sow discord"',
  Teams: '"Microsoft Teams" OR "MS Teams"',
};

const brandData: Record<string, any> = {};

for (const [name, query] of Object.entries(brands)) {
  const twitter = await client.twitter.searchPosts(query, {
    startDate: "2026-02-16",
    endDate: "2026-02-23",
    language: "en",
    fields: ["id", "text", "authorUsername", "likeCount", "retweetCount", "createdAtDate"],
  });

  const reddit = await client.reddit.searchPosts(query, {
    startDate: "2026-02-16",
    fields: ["id", "title", "text", "score", "numComments", "subreddit"],
  });

  brandData[name] = { twitter, reddit };
}

await client.close();
```

### Step 3: Analyze and Compare

**Share of Voice (SOV):**
```
SOV for Brand A = (Brand A mentions) / (Total mentions across all brands) × 100
```
Calculate separately for Twitter and Reddit.

**Sentiment Comparison:**
For each brand, classify posts into positive/neutral/negative (see social-sentiment-analyzer skill for classification method) and compare:
- Overall sentiment score (0-100)
- Positive/negative ratio
- Sentiment trend over the time period

**Engagement Comparison:**
- Average likes per post
- Average comments/replies per post
- Total impressions (Twitter)
- Total Reddit score

**Audience Overlap:**
- Find users who posted about multiple brands (common usernames across datasets)
- These users are particularly valuable for understanding switching behavior

**Positioning Analysis:**
- What attributes does each brand's audience associate with it?
- What are the unique strengths/weaknesses mentioned for each?
- Common comparison contexts ("I switched from X to Y because...")

### Step 4: Generate Report

```
## Competitive Intelligence: [BRAND] vs Competitors
**Period:** [date range] | **Platforms:** Twitter, Reddit

### Share of Voice
| Brand | Twitter Posts | Reddit Posts | Total | SOV |
|-------|-------------|-------------|-------|-----|
| Slack | 1,234 | 456 | 1,690 | 42% |
| Discord | 890 | 678 | 1,568 | 39% |
| Teams | 456 | 321 | 777 | 19% |

### Sentiment Comparison
| Brand | Score | Positive | Neutral | Negative | Trend |
|-------|-------|----------|---------|----------|-------|
| Slack | 62 | 38% | 42% | 20% | → Stable |
| Discord | 71 | 48% | 35% | 17% | ↑ Improving |
| Teams | 45 | 22% | 45% | 33% | ↓ Declining |

### Engagement Comparison
| Brand | Avg Likes (Twitter) | Avg Score (Reddit) | Avg Comments |
|-------|--------------------|--------------------|--------------|
| ... | ... | ... | ... |

### Key Findings

#### [Brand A] Strengths
- [What people praise, with example quotes]

#### [Brand A] Weaknesses
- [What people complain about, with example quotes]

#### [Brand B] Strengths / Weaknesses
...

### Competitive Positioning Map
- **[Brand A]:** Positioned as [description]
- **[Brand B]:** Positioned as [description]
- **Switching signals:** [users switching from X to Y, with reasons]

### Audience Overlap
[X users posted about multiple brands — analysis of their preferences]

### Recommendations
[3-5 actionable insights based on the competitive landscape]
```

## Example Prompts

- "Compare Tesla vs Rivian vs Lucid on Twitter sentiment"
- "Share of voice: Figma vs Sketch vs Adobe XD"
- "Competitive analysis for Notion vs Obsidian vs Roam Research on Reddit"
- "How does Claude sentiment compare to ChatGPT and Gemini?"

## Notes

- Expand brand names carefully to avoid false positives (common words need exclusions)
- Reddit provides qualitative depth; Twitter provides quantitative breadth
- Free tier: 100K results/month at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=competitive-intel)
- For large comparisons (5+ brands), use CSV exports and analyze locally with pandas/Excel
