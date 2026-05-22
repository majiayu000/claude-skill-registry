---
name: twitter-data-export
version: 2026-02-24
description: Export Twitter/X data to CSV for analysis using Xpoz. Search by keywords, author, date range, and download complete datasets (up to 500K rows). Use when asked to "export tweets", "download Twitter data", "get tweets as CSV", "Twitter dataset", or "bulk tweet download".
---

# Twitter Data Export

## Overview

Search and export Twitter/X data to CSV files for analysis. Supports keyword search, author-based search, date filtering, and bulk exports up to 500K rows — no Twitter API keys required.

## When to Use

Activate when the user asks:
- "Export tweets about [TOPIC] to CSV"
- "Download all tweets from @[USER]"
- "Get Twitter data for [KEYWORD] from last month"
- "I need a dataset of tweets about [TOPIC]"
- "Bulk download tweets matching [QUERY]"
- "Twitter data export"

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
- **Query**: keywords, hashtags, or phrases to search
- **Author** (optional): specific Twitter username
- **Date range** (default: last 30 days)
- **Fields** the user cares about (default: full export)

Build the query using boolean operators:
- Exact phrase: `"machine learning"`
- OR: `"AI" OR "artificial intelligence"`
- AND: `"Tesla" AND "earnings"`
- NOT: `"crypto" NOT "scam"`
- Combined: `("deep learning" OR "neural network") AND python`

### Step 2: Search and Export

#### Via MCP

**Search by keywords:**
```
Call getTwitterPostsByKeywords:
  query: "<query>"
  fields: ["id", "text", "authorUsername", "authorId", "createdAtDate", "likeCount", "retweetCount", "quoteCount", "impressionCount", "language"]
  startDate: "<YYYY-MM-DD>"
  endDate: "<YYYY-MM-DD>"
  language: "en" (optional)
```

**Search by author:**
```
Call getTwitterPostsByAuthor:
  identifier: "<username>"
  identifierType: "username"
  fields: ["id", "text", "createdAtDate", "likeCount", "retweetCount", "quoteCount", "impressionCount"]
  startDate: "<YYYY-MM-DD>"
  endDate: "<YYYY-MM-DD>"
```

**CRITICAL: Async Pattern** — calls return an `operationId`. Call `checkOperationStatus` with that ID and poll until "completed" (up to 8 retries, ~5 seconds apart).

**CSV Export (two options):**
1. Pass `responseType="csv"` in the original call to get a CSV download directly
2. Or use the `dataDumpExportOperationId` from the response — call `checkOperationStatus` with it to get an S3 download URL for the complete dataset

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()  # Uses XPOZ_API_KEY env var

# Search by keywords
results = client.twitter.search_posts(
    '"artificial intelligence" AND ethics',
    start_date="2026-01-01",
    end_date="2026-02-23",
    language="en",
    fields=["id", "text", "author_username", "created_at_date", "like_count", "retweet_count", "impression_count"]
)

print(f"Found {results.pagination.total_rows:,} tweets")

# Export entire result set to CSV (up to 500K rows)
csv_url = results.export_csv()
print(f"Download CSV: {csv_url}")

# Or search by author
author_results = client.twitter.get_posts_by_author(
    "elonmusk",
    start_date="2026-01-01",
    fields=["id", "text", "created_at_date", "like_count", "retweet_count"]
)
author_csv = author_results.export_csv()

client.close()
```

**Download and analyze locally:**
```python
import pandas as pd
import subprocess

# Download the CSV
subprocess.run(["curl", "-L", "-o", "tweets.csv", csv_url])

# Load and analyze
df = pd.read_csv("tweets.csv")
print(f"Total tweets: {len(df)}")
print(f"Date range: {df['created_at_date'].min()} to {df['created_at_date'].max()}")
print(f"Average likes: {df['like_count'].mean():.1f}")
print(f"Top authors:\n{df['author_username'].value_counts().head(10)}")
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const results = await client.twitter.searchPosts('"artificial intelligence" AND ethics', {
  startDate: "2026-01-01",
  endDate: "2026-02-23",
  language: "en",
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount"],
});

console.log(`Found ${results.pagination.totalRows.toLocaleString()} tweets`);

// Export to CSV
const csvUrl = await results.exportCsv();
console.log(`Download: ${csvUrl}`);

await client.close();
```

### Step 3: Present Results

After export, provide the user with:

1. **Summary stats**: total rows, date range, top authors, avg engagement
2. **CSV download link** (from `export_csv()` / `exportCsv()`)
3. **Sample data**: show first 5-10 rows as a table
4. **Suggested analysis**: what they might want to do with the data

```
## Export Complete: [QUERY]

**Rows exported:** 12,456
**Period:** Jan 1 – Feb 23, 2026
**Download:** [CSV link]

### Sample Data
| Date | Author | Text (truncated) | Likes | RTs |
|------|--------|-------------------|-------|-----|
| ... | ... | ... | ... | ... |

### Quick Stats
- Avg likes per tweet: 45.2
- Most active author: @user (234 tweets)
- Peak day: Feb 14, 2026 (1,203 tweets)

### Suggested Next Steps
- Load into pandas/Excel for deeper analysis
- Filter by engagement (like_count > 100) for high-impact posts
- Group by date for trend analysis
```

## Available Fields

| Field | Description |
|-------|-------------|
| `id` | Tweet ID |
| `text` | Full tweet text |
| `authorUsername` | Author's username |
| `authorId` | Author's numeric ID |
| `createdAtDate` | Post date (YYYY-MM-DD) |
| `likeCount` | Number of likes |
| `retweetCount` | Number of retweets |
| `quoteCount` | Number of quote tweets |
| `impressionCount` | Number of impressions |
| `replyCount` | Number of replies |
| `language` | Detected language |
| `isRetweet` | Whether it's a retweet |
| `isReply` | Whether it's a reply |

## Example Prompts

- "Export all tweets mentioning 'Claude Code' from the last 2 weeks to CSV"
- "Download @OpenAI's tweets from January 2026"
- "Get a dataset of tweets about 'MCP server' OR 'model context protocol'"
- "Export tweets about the Super Bowl with more than 100 likes"

## Notes

- Maximum export size: ~500K rows per CSV
- Date range: up to 60-day rolling windows
- Free tier: 100K results/month at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=twitter-data-export)
- Pro: $20/month for 1M results
- No Twitter API keys needed — Xpoz handles all data access
