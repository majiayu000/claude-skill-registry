---
name: influencer-discovery
version: 2026-02-24
description: Find and rank influencers by niche, engagement, and authenticity using Xpoz. Searches Twitter, Instagram, and Reddit for active voices in any topic. Use when asked to "find influencers", "discover thought leaders", "who's talking about X", "influencer research", or "find KOLs".
---

# Influencer Discovery

## Overview

Find, evaluate, and rank influencers for any niche across Twitter/X and Instagram. Identifies who is actively creating content about a topic, ranks them by engagement and relevance, and provides authenticity scoring.

## When to Use

Activate when the user asks:
- "Find influencers in [NICHE] on Twitter"
- "Who are the top voices talking about [TOPIC]?"
- "Discover thought leaders in [INDUSTRY]"
- "Find micro-influencers for [PRODUCT CATEGORY]"
- "KOL research for [TOPIC]"
- "Who should we partner with for [CAMPAIGN]?"

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
- **Niche/topic** to search
- **Platform** (default: Twitter; add Instagram if relevant)
- **Influencer tier** preference (if specified):
  - Mega: 1M+ followers
  - Macro: 100K–1M
  - Micro: 10K–100K
  - Nano: 1K–10K
- **Time period** (default: last 30 days)

Build search queries targeting content creators, not just mentions:
- Topic keywords: `"AI agents" OR "autonomous AI" OR "agentic AI"`
- Include specific subtopics for better targeting

### Step 2: Find Active Users by Topic

#### Via MCP

```
Call getTwitterUsersByKeywords:
  query: "<expanded query>"
  fields: ["id", "username", "name", "description", "followersCount", "followingCount", "tweetCount", "relevantTweetsCount", "relevantTweetsLikesSum", "relevantTweetsImpressionsSum", "isInauthentic", "isInauthenticProbScore", "verified"]
  startDate: "<30 days ago, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
```

**CRITICAL:** Call `checkOperationStatus` with the returned `operationId` and poll until "completed".

The response includes powerful aggregation fields:
- `relevantTweetsCount` — how many times they posted about the topic
- `relevantTweetsLikesSum` — total likes on their topic-relevant posts
- `relevantTweetsImpressionsSum` — total impressions on relevant posts

**For deeper analysis on top candidates:**
```
Call getTwitterPostsByAuthor:
  identifier: "<username>"
  identifierType: "username"
  fields: ["id", "text", "likeCount", "retweetCount", "impressionCount", "createdAtDate"]
  startDate: "<30 days ago>"
```

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

# Find users who posted about the topic
users = client.twitter.get_users_by_keywords(
    '"AI agents" OR "autonomous AI" OR "agentic AI"',
    start_date="2026-01-24",
    end_date="2026-02-23",
    fields=[
        "id", "username", "name", "description",
        "followers_count", "following_count", "tweet_count",
        "relevant_tweets_count", "relevant_tweets_likes_sum",
        "relevant_tweets_impressions_sum",
        "is_inauthentic", "is_inauthentic_prob_score", "verified"
    ]
)

# Collect all pages
all_users = users.data
while users.has_next_page():
    users = users.next_page()
    all_users.extend(users.data)

# Deep-dive on top candidates
for user in top_candidates[:10]:
    posts = client.twitter.get_posts_by_author(
        user.username,
        start_date="2026-01-24",
        fields=["id", "text", "like_count", "retweet_count", "impression_count", "created_at_date"]
    )
    # Analyze their content quality, consistency, tone

client.close()
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const users = await client.twitter.getUsersByKeywords(
  '"AI agents" OR "autonomous AI" OR "agentic AI"',
  {
    startDate: "2026-01-24",
    endDate: "2026-02-23",
    fields: [
      "id", "username", "name", "description",
      "followersCount", "followingCount", "tweetCount",
      "relevantTweetsCount", "relevantTweetsLikesSum",
      "relevantTweetsImpressionsSum",
      "isInauthentic", "isInauthenticProbScore", "verified",
    ],
  }
);

await client.close();
```

### Step 3: Score and Rank

For each user, calculate an **Influencer Score (0–100)**:

| Factor | Weight | Calculation |
|--------|--------|-------------|
| Relevance | 30% | `min(relevantTweetsCount × 6, 30)` — more topic posts = more relevant |
| Engagement | 30% | `min((relevantTweetsLikesSum / relevantTweetsCount) / 50, 30)` — avg engagement per post |
| Reach | 20% | `min(log10(followersCount) × 5, 20)` — logarithmic follower scale |
| Authenticity | 10% | `(1 - isInauthenticProbScore) × 10` — Xpoz bot detection |
| Consistency | 10% | `min(relevantTweetsCount / days × 10, 10)` — posting frequency |

### Step 4: Classify Influencers

**By Tier:**
| Tier | Followers | Typical Value |
|------|-----------|---------------|
| Mega | 1M+ | Broad awareness, expensive |
| Macro | 100K–1M | Strong reach, established |
| Micro | 10K–100K | High engagement, niche authority |
| Nano | 1K–10K | Very targeted, authentic, affordable |

**By Voice Type** (analyze their bio + recent posts):
| Type | Description |
|------|-------------|
| Analyst | Data-driven, market commentary |
| Builder | Creates products/tools in the space |
| Educator | Tutorials, explainers, threads |
| News | Breaks/shares news and updates |
| Commentator | Opinions, hot takes, discussions |
| Community | Moderates/leads community spaces |

### Step 5: Generate Report

```
## Influencer Discovery: [TOPIC]
**Period:** [date range] | **Users analyzed:** [count] | **Platform:** Twitter

### Top Influencers

| Rank | User | Followers | Posts | Avg Likes | Score | Tier | Type |
|------|------|-----------|-------|-----------|-------|------|------|
| 1 | @user | 45K | 12 | 890 | 87 | Micro | Builder |
| 2 | ... | ... | ... | ... | ... | ... | ... |

### Tier Distribution
- Mega (1M+): X users
- Macro (100K–1M): X users
- Micro (10K–100K): X users
- Nano (1K–10K): X users

### Detailed Profiles (Top 10)

#### 1. @username — "Display Name"
- **Bio:** [description]
- **Followers:** X | **Topic Posts:** X | **Avg Engagement:** X
- **Voice Type:** Builder
- **Authenticity:** ✅ Verified authentic (score: 0.95)
- **Sample Posts:**
  - "[tweet text]" (❤️ X, 🔁 X)
  - "[tweet text]" (❤️ X, 🔁 X)
- **Why They Matter:** [1-2 sentences on their influence in this niche]

### Recommendations
[Which influencers are best for different goals: awareness vs credibility vs engagement]
```

## Example Prompts

- "Find the top 20 AI agent influencers on Twitter"
- "Who are the micro-influencers talking about sustainable fashion on Instagram?"
- "Discover crypto KOLs with high engagement rates"
- "Find developer advocates who post about MCP servers"

## Notes

- Xpoz's `relevantTweetsCount` and `relevantTweetsLikesSum` fields let you find influencers by **what they create**, not just follower count
- Authenticity scoring (`isInauthenticProbScore`) helps filter out bots and fake accounts
- Free tier: 100K results/month at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=influencer-discovery)
