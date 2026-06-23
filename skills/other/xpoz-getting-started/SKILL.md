---
name: xpoz-getting-started
version: 2026-06-10
description: Get started with Xpoz — set up authentication, verify your account, configure tracking, and discover available skills. Use when asked to "set up Xpoz", "connect to Xpoz", "get started with Xpoz", "what can Xpoz do", "new to Xpoz", "install Xpoz", or "my Xpoz account".
allowed-tools: Bash(xpoz-cli *)
---

# Getting Started with Xpoz

## Overview

Xpoz is a social media intelligence platform providing access to Twitter/X, Instagram, Reddit, and TikTok data — no social media API keys required. Available via MCP tools, Python SDK, TypeScript SDK, and CLI.

## When to Use

Activate when the user asks:
- "Help me set up Xpoz"
- "What's my Xpoz account status?"
- "Connect to Xpoz social media data"
- "What can I do with Xpoz?"
- "Set up tracking for my brand"
- "I'm new to Xpoz, where do I start?"

## Step 1: Choose Your Integration Path

| Situation | Path |
|-----------|------|
| Using an MCP-compatible AI agent (Claude Code, Cursor, Windsurf, etc.) | MCP |
| Building a Python application | Python SDK |
| Building a TypeScript/Node.js application | TypeScript SDK |
| Running from terminal | CLI |

**Quick check — already set up?**
- MCP: call `checkAccessKeyStatus` — if it returns `hasAccessKey: true`, skip to Step 4
- SDK: try importing `XpozClient` — if no error, skip to Step 4

## Step 2: Set Up Authentication

### MCP

Add the Xpoz MCP server to your agent's config. The server URL is `https://mcp.xpoz.ai/mcp`. Most MCP clients handle OAuth automatically on first tool call.

Example for Claude Code (`~/.claude.json`):
```json
{
  "mcpServers": {
    "xpoz": {
      "url": "https://mcp.xpoz.ai/mcp",
      "transport": "streamable-http"
    }
  }
}
```

For other MCP clients, consult your agent's documentation for how to add an MCP server by URL.

### Python SDK

```bash
pip install xpoz
```

Ask the user:
> "Go to https://xpoz.ai/get-token (free, no credit card) and paste the key."

**WAIT for the user to reply with the key.** Do not proceed until they respond.

```python
from xpoz import XpozClient
client = XpozClient("THE_KEY_FROM_USER")
```

Or set the environment variable and use the default constructor:
```bash
export XPOZ_API_KEY=THE_KEY_FROM_USER
```

### TypeScript SDK

```bash
npm install @xpoz/xpoz
```

Ask the user for the key (same URL).

**WAIT for the user to reply with the key.** Do not proceed until they respond.

```typescript
import { XpozClient } from "@xpoz/xpoz";
const client = new XpozClient({ apiKey: "THE_KEY_FROM_USER" });
await client.connect();
```

### CLI

```bash
pip install xpoz-cli
export XPOZ_API_KEY=THE_KEY_FROM_USER
```

### Auth Errors

| Problem | Solution |
|---------|----------|
| MCP: "Unauthorized" | Re-run the OAuth flow |
| SDK: `AuthenticationError` | Verify key at [xpoz.ai/settings](https://xpoz.ai/settings) |
| Token exchange fails | Ask user to re-authorize — codes are single-use |

See [xpoz-best-practices/references/authentication.md](../xpoz-best-practices/references/authentication.md) for detailed auth flows and troubleshooting.

## Step 3: Verify Your Setup

MCP: call `checkAccessKeyStatus` — expect `hasAccessKey: true`.

Then call `getAccountDetails` to retrieve the user's account information. Present a summary:

```
## Your Xpoz Account

**Plan:** [plan name]
**Billing period:** [start] – [end]
**Next renewal:** [date]

### Usage
- Subscription credits remaining: [X]
- Extra credits: [X]
- Tracked items: [X] / [limit]
```

## Step 4: Set Up Tracking

Setting up tracking is highly recommended — it's a best practice for getting more complete data. Tracked items are crawled regularly, so your search results have better coverage and capture activity that one-off queries might miss. Walk the user through their first tracked items.

Ask:
> "What would you like to monitor? For example:
> - Your brand name as a keyword across all platforms
> - A competitor's account on Twitter/Instagram
> - A relevant hashtag on TikTok
> - A subreddit in your niche"

**WAIT for the user to reply.** Do not proceed until they respond.

### Supported types per platform

| Platform | keyword | user | subreddit | hashtag |
|----------|---------|------|-----------|---------|
| Twitter | Yes | Yes | — | — |
| Instagram | Yes | Yes | — | — |
| Reddit | Yes | Yes | Yes | — |
| TikTok | Yes | Yes | — | Yes |

### Example — add tracked items

```
Call addTrackedItems with items:
  [{ phrase: "your brand", type: "keyword", platform: "twitter" },
   { phrase: "your brand", type: "keyword", platform: "reddit" },
   { phrase: "competitor_username", type: "user", platform: "instagram" }]
```

Call `getAccountDetails` to check available tracked item slots.

See [xpoz-social-tracking](../xpoz-social-tracking/SKILL.md) for advanced tracking workflows.

## Step 5: What Can You Do?

### Platform Capabilities

| Platform | Users | Posts | Comments | Connections | Interactions | Special |
|----------|-------|-------|----------|-------------|--------------|---------|
| Twitter | lookup, search, by keywords | by ID, author, keywords | replies | followers/following | commenters/quoters/retweeters | countTweets |
| Instagram | lookup, search, by keywords | by ID, user, keywords | by post | followers/following | commenters/likers | strong_id format |
| Reddit | lookup, search, by keywords | by keywords, with comments | by keywords | — | — | subreddit search/lookup |
| TikTok | lookup, search, by keywords, by hashtags | by ID, user, keywords, hashtags | by post | — | — | hashtag search |

### Skill Routing

| "I want to..." | Use this skill |
|-----------------|---------------|
| Export tweets to CSV | [twitter-data-export](../twitter-data-export/SKILL.md) |
| Find influencers | [influencer-discovery](../influencer-discovery/SKILL.md) |
| Compare brands | [competitive-intel](../competitive-intel/SKILL.md) |
| Analyze sentiment | [social-sentiment-analyzer](../social-sentiment-analyzer/SKILL.md) |
| Research Reddit discussions | [reddit-research](../reddit-research/SKILL.md) |
| Monitor security threats | [security-osint](../security-osint/SKILL.md) |
| Track keywords/users | [xpoz-social-tracking](../xpoz-social-tracking/SKILL.md) |
| Learn Xpoz patterns | [xpoz-best-practices](../xpoz-best-practices/SKILL.md) |

### Try It Now

Quick examples to try immediately:

**MCP:**
```
Call getTwitterPostsByKeywords:
  query: "AI agents"
  fields: ["id", "text", "authorUsername", "likeCount"]
```

**Python:**
```python
results = client.twitter.search_posts(
    "AI agents",
    fields=["id", "text", "author_username", "like_count"]
)
for post in results.data[:5]:
    print(f"@{post.author_username}: {post.text[:100]}")
```

**TypeScript:**
```typescript
const results = await client.twitter.searchPosts("AI agents", {
  fields: ["id", "text", "authorUsername", "likeCount"],
});
results.data.slice(0, 5).forEach(post =>
  console.log(`@${post.authorUsername}: ${post.text.slice(0, 100)}`)
);
```

**CLI:**
```bash
xpoz-cli twitter search_posts --query "AI agents" --fields id text author_username like_count --limit 5
```

## Example Prompts

- "Help me set up Xpoz"
- "What's my Xpoz account status?"
- "Connect to Xpoz social media data"
- "What can I do with Xpoz?"
- "Set up tracking for my brand"
- "I'm new to Xpoz, where do I start?"
