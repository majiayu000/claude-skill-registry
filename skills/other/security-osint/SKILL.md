---
name: security-osint
version: 2026-02-24
description: Monitor social platforms for security threats, vulnerability discussions, and breach intelligence using Xpoz. Use when asked to "find CVE discussions", "security threat monitoring", "OSINT social media", "vulnerability intelligence", "breach mentions", or "threat intel from Twitter/Reddit".
---

# Security OSINT

## Overview

Monitor Twitter/X and Reddit for security-related discussions — CVE mentions, zero-day chatter, breach reports, exploit code sharing, and emerging threats. Provides early warning intelligence often 24-48 hours before formal advisories.

## When to Use

Activate when the user asks:
- "Find discussions about [CVE-XXXX-XXXXX] on Twitter"
- "What's the security community saying about [VULNERABILITY]?"
- "Monitor social media for [SOFTWARE] vulnerabilities"
- "OSINT research on [THREAT ACTOR/CAMPAIGN]"
- "Are there breach reports about [COMPANY] on social media?"
- "Threat intelligence from Twitter and Reddit"

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
- **Target**: CVE ID, software name, company, threat actor, or general topic
- **Scope**: specific vulnerability vs broad monitoring
- **Platforms** (default: Twitter + Reddit — where security researchers are most active)
- **Time period** (default: last 7 days; use 24-48h for breaking threats)

Build targeted queries:

**For a specific CVE:**
```
"CVE-2026-1234" OR "CVE202612345"
```

**For a software vulnerability:**
```
("[SOFTWARE]" AND ("vulnerability" OR "vuln" OR "exploit" OR "RCE" OR "zero-day" OR "0day" OR "CVE"))
```

**For breach monitoring:**
```
("[COMPANY]" AND ("breach" OR "hacked" OR "leak" OR "data leak" OR "compromised" OR "ransomware"))
```

**For threat actor tracking:**
```
("[THREAT ACTOR]" OR "[KNOWN ALIASES]") AND ("attack" OR "campaign" OR "APT" OR "malware")
```

### Step 2: Fetch Security Discussions

#### Via MCP

**Twitter (security researchers are very active here):**
```
Call getTwitterPostsByKeywords:
  query: "<security query>"
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount", "impressionCount"]
  startDate: "<7 days ago, YYYY-MM-DD>"
  endDate: "<today, YYYY-MM-DD>"
  language: "en"
```

**Find security researchers discussing the topic:**
```
Call getTwitterUsersByKeywords:
  query: "<security query>"
  fields: ["id", "username", "name", "description", "followersCount", "relevantTweetsCount", "relevantTweetsLikesSum", "verified"]
  startDate: "<7 days ago>"
```

**Reddit (r/netsec, r/cybersecurity, r/hacking, etc.):**
```
Call getRedditPostsByKeywords:
  query: "<security query>"
  fields: ["id", "title", "text", "authorUsername", "createdAtDate", "score", "numComments", "subreddit", "url"]
  startDate: "<7 days ago>"
```

**CRITICAL:** Poll `checkOperationStatus` with each `operationId` until "completed".

#### Via Python SDK

```python
from xpoz import XpozClient

client = XpozClient()

cve_id = "CVE-2026-1234"
query = f'"{cve_id}"'

# Twitter - security researcher chatter
twitter_posts = client.twitter.search_posts(
    query,
    start_date="2026-02-16",
    end_date="2026-02-23",
    fields=["id", "text", "author_username", "created_at_date", "like_count", "retweet_count", "impression_count"]
)

# Find researchers discussing it
researchers = client.twitter.get_users_by_keywords(
    query,
    start_date="2026-02-16",
    fields=["username", "name", "description", "followers_count", "relevant_tweets_count", "verified"]
)

# Reddit - deeper technical discussions
reddit_posts = client.reddit.search_posts(
    query,
    start_date="2026-02-16",
    fields=["id", "title", "text", "author_username", "created_at_date", "score", "num_comments", "subreddit", "url"]
)

print(f"Twitter: {twitter_posts.pagination.total_rows} posts")
print(f"Reddit: {reddit_posts.pagination.total_rows} posts")
print(f"Researchers: {researchers.pagination.total_rows} users")

# Export for analysis
twitter_csv = twitter_posts.export_csv()
reddit_csv = reddit_posts.export_csv()

client.close()
```

#### Via TypeScript SDK

```typescript
import { XpozClient } from "@xpoz/xpoz";

const client = new XpozClient();
await client.connect();

const cveId = "CVE-2026-1234";

const twitterPosts = await client.twitter.searchPosts(`"${cveId}"`, {
  startDate: "2026-02-16",
  endDate: "2026-02-23",
  fields: ["id", "text", "authorUsername", "createdAtDate", "likeCount", "retweetCount"],
});

const redditPosts = await client.reddit.searchPosts(`"${cveId}"`, {
  startDate: "2026-02-16",
  fields: ["id", "title", "text", "score", "numComments", "subreddit"],
});

await client.close();
```

### Step 3: Analyze Threat Intelligence

**Timeline Reconstruction:**
- Sort all posts chronologically
- Identify the first public mention (potential disclosure date)
- Track how discussion evolved (initial report → PoC → exploitation → patches)

**Severity Assessment (from social signals):**
| Signal | Indicates |
|--------|-----------|
| High engagement + rapid spread | Critical/actively exploited |
| Security researchers sharing PoC code | Weaponization in progress |
| Vendor accounts responding | Acknowledged, patch likely coming |
| Low volume, technical-only discussion | Early stage or low severity |
| Mentions of "in the wild" / "actively exploited" | Immediate action needed |

**Source Credibility:**
- Verified security researchers (check bio for "security", "pentest", "CISO", "CVE")
- High follower count in security niche
- Posted from known security company accounts
- Cross-referenced across multiple independent sources

**Key Information to Extract:**
- Affected software/versions
- Attack vector (remote/local, authentication required?)
- Exploit availability (PoC published?)
- Patch status (fixed? workaround available?)
- Active exploitation reports
- IoCs (indicators of compromise) shared

### Step 4: Generate Report

```
## Security Intelligence: [TARGET]
**Period:** [date range] | **Sources:** Twitter ([X] posts), Reddit ([X] posts)

### ⚠️ Threat Summary
**Severity:** Critical / High / Medium / Low
**Status:** [Active exploitation / PoC available / Discussion only / Patched]
**First seen:** [date of earliest social mention]

### Timeline
| Date | Source | Event |
|------|--------|-------|
| Feb 16 | Twitter @researcher | First public mention of vulnerability |
| Feb 17 | Reddit r/netsec | Technical analysis posted |
| Feb 18 | Twitter @vendor | Patch announced |

### Technical Details (from social sources)
- **Affected:** [software, versions]
- **Vector:** [remote/local, auth requirements]
- **Impact:** [RCE, data leak, DoS, etc.]
- **Exploit:** [PoC available? Where?]
- **Patch:** [Available? Version? Workaround?]

### Key Voices
| Researcher | Followers | Posts | Credibility |
|-----------|-----------|-------|-------------|
| @security_expert | 50K | 3 | High (CISO at [company]) |
| ... | ... | ... | ... |

### Notable Posts
> "Actual quote from security researcher" — @username (❤️ X, 🔁 X)

### Subreddit Activity
| Subreddit | Posts | Top Thread |
|-----------|-------|-----------|
| r/netsec | X | "Title..." (⬆️ X, 💬 X) |
| r/cybersecurity | X | "Title..." |

### Recommended Actions
1. [Immediate: patch/mitigate if affected]
2. [Monitor: watch for exploitation reports]
3. [Investigate: check logs for IoCs]
```

## Example Prompts

- "What's the security community saying about CVE-2026-1234?"
- "Monitor Twitter for Log4Shell discussions in the last 48 hours"
- "OSINT: find breach reports about [Company] on social media"
- "Are there any zero-day discussions about Chrome this week?"
- "Track discussions about the latest ransomware campaign on Twitter and Reddit"
- "Find security researchers talking about MCP server vulnerabilities"

## Notes

- Security discussions on Twitter often precede formal CVE publication by 24-48 hours
- Reddit r/netsec and r/cybersecurity provide technical depth; Twitter provides speed
- Use `relevantTweetsCount` from user search to find who's most actively discussing a threat
- Be careful with sensitive information — don't amplify exploit code or IoCs unnecessarily
- Free tier: 100K results/month at [xpoz.ai](https://xpoz.ai?utm_source=github&utm_medium=agent-skills&utm_campaign=security-osint)
