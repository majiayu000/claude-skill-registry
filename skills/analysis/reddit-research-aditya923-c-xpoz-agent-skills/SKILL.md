---
name: reddit-research
version: 2026-02-24
description: Search and analyze Reddit discussions for market research, product feedback, and community insights using Xpoz. Use when asked to "search Reddit", "what does Reddit think about X", "Reddit feedback on X", "subreddit analysis", or "Reddit market research".
---

# Reddit Research

## Overview

Search and analyze Reddit discussions across all subreddits. Extract community opinions, identify pain points, discover product feedback, and understand market sentiment — all without Reddit API keys.

## When to Use

Activate when the user asks:
- "What does Reddit think about [PRODUCT]?"
- "Search Reddit for [TOPIC]"
- "What are people saying about [BRAND] on Reddit?"
- "Reddit feedback on [TOOL/SERVICE]"
- "Find Reddit discussions about [TOPIC]"
- "Market research on Reddit for [INDUSTRY]"

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
- **Topic/product/brand** to research
- **Specific questions** the user wants answered
- **Time period** (default: last 30 days)
- **Subreddit filter** (if user specifies one)

Build the query:
- Product name + common alternatives: `"Cursor" OR "Cursor IDE" OR "cursor.sh"`
- Include comparison terms: `"Cursor vs" OR "Cursor alternative"`
- For feedback: `"Cursor" AND ("love" OR "hate" OR "switched" OR "review")`

### Step 2: Fetch Reddit Posts

#### Via MCP

```
Call getRedditPostsByKeywords:
  query: "<expanded query>"
  fields: ["id", "title", "text", "authorUsername", "createdAtDate", "score", "numComments", "subreddit", "url"]
  startDate: "<30 days ago, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
```

**CRITICAL:** Call `checkOperationStatus` with the returned `operationId` and poll until "completed" (up to 8 retries, ~5 seconds apart).

**For users who posted about the topic:**
```
Call getRedditUsersByKeywords:
  query: "<query>"
  fields: ["id", "username", "relevantPostsCount"]
  startDate: "<30 days ago>"
```

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

# Search Reddit posts
results = client.reddit.search_posts(
    '"Cursor" OR "Cursor IDE"',
    start_date="2026-01-24",
    end_date="2026-02-23",
    fields=["id", "title", "text", "author_username", "created_at_date", "score", "num_comments", "subreddit", "url"]
)

# Collect all pages
all_posts = results.data
while results.has_next_page():
    results = results.next_page()
    all_posts.extend(results.data)

print(f"Found {len(all_posts)} Reddit posts")

# Export to CSV for deeper analysis
csv_url = results.export_csv()

client.close()
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const results = await client.reddit.searchPosts('"Cursor" OR "Cursor IDE"', {
  startDate: "2026-01-24",
  endDate: "2026-02-23",
  fields: ["id", "title", "text", "authorUsername", "createdAtDate", "score", "numComments", "subreddit", "url"],
});

console.log(`Found ${results.pagination.totalRows} posts`);
const csvUrl = await results.exportCsv();

await client.close();
```

### Step 3: Analyze the Data

**Subreddit Distribution:**
- Group posts by subreddit
- Identify where the most discussion happens
- Note subreddit context (r/programming = developers, r/productivity = end users, etc.)

**Sentiment Analysis:**
- Reddit uses upvotes/downvotes as built-in sentiment (high score = community agrees)
- Posts with high `numComments` indicate controversial or engaging topics
- Score/comments ratio: high score + few comments = consensus; low score + many comments = debate

**Theme Extraction:**
Identify recurring themes:
- **Pain points**: complaints, frustrations, feature requests
- **Praise**: what users love, competitive advantages
- **Comparisons**: how the product compares to alternatives
- **Use cases**: how people actually use the product
- **Questions**: common confusion points or information gaps

**Tip:** Reddit posts often contain more nuanced, detailed opinions than Twitter. Prioritize posts with high `score` and `numComments` for quality insights.

### Step 4: Generate Report

```
## Reddit Research: [TOPIC]
**Period:** [date range] | **Posts analyzed:** [count]

### Overview
[2-3 sentence summary of what Reddit thinks]

### Subreddit Distribution
| Subreddit | Posts | Avg Score | Top Theme |
|-----------|-------|-----------|-----------|
| r/programming | X | X | Performance concerns |
| r/productivity | X | X | Workflow improvements |
| ... | ... | ... | ... |

### Key Themes

#### 1. 👍 What People Love
- [Theme with supporting quotes]
- [Theme with supporting quotes]

#### 2. 👎 Pain Points & Complaints
- [Theme with supporting quotes]
- [Theme with supporting quotes]

#### 3. 🔄 Comparisons & Alternatives
- [Product vs Competitor: community consensus]
- [Common alternatives mentioned]

#### 4. 💡 Feature Requests & Suggestions
- [Most requested features]
- [Creative use cases discovered]

### Top Posts (by engagement)
| Score | Comments | Subreddit | Title |
|-------|----------|-----------|-------|
| 1.2K | 234 | r/programming | "Title..." |
| ... | ... | ... | ... |

### Notable Quotes
> "Actual Reddit quote with context" — u/username in r/subreddit (⬆️ 456)

### Actionable Insights
[3-5 bullet points of what to do with this information]
```

## Example Prompts

- "What does Reddit think about Cursor IDE?"
- "Search Reddit for people complaining about Zapier pricing"
- "Reddit market research: what tools are indie hackers using for automation?"
- "Find Reddit posts comparing Claude vs GPT-4"
- "What's r/machinelearning saying about open-source LLMs?"

## Notes

- Reddit data includes post titles and body text — titles alone often reveal sentiment
- High `num_comments` posts are goldmines for qualitative research
- Free tier: 100K results/month at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=reddit-research)
- For CSV export, use `export_csv()` / `exportCsv()` to download complete datasets
