---
name: twitter
description: "Twitter/X integration with three modes: official API v2 search/research via x-search (pay-per-use, $0.005/read), session-based posting/reading via bird CLI (free, browser cookies), and bookmark archival via Smaug. This skill should be used when searching tweets, researching topics on X, posting, monitoring accounts, or archiving bookmarks."
---

# Twitter/X — Dual-Mode Integration

Three tools for different operations. Choose by task:

| Mode | Tool | Auth | Cost | Use For |
|------|------|------|------|---------|
| **Official API** | `x-search` | Bearer token | $0.005/read, $0.01/user | Search, research, profiles, threads, monitoring |
| **Official API** | `x-search post/reply` | OAuth 1.0a | $0.01/post | Posting, replying via official API |
| **Session** | `bird` | Browser cookies | Free | Posting, replying, bookmarks, mentions, media |
| **Archival** | `smaug` | Via bird | Free | Bookmark/likes processing, AI-powered filing |

> **Alternative**: `opencli twitter` provides 25 free session-based commands (post, reply, search, bookmarks, follow, block, etc.) via Chrome session reuse. Prefer opencli for routine Twitter operations. Use x-search for deep research with cost tracking. bird CLI remains available as fallback.

## Setup

### x-search (Official API v2)

Requires an X API Bearer token from [console.x.com](https://console.x.com). Pay-per-use — no monthly commitment.

```bash
# Store token (pick one)
echo 'X_BEARER_TOKEN=your_token_here' >> ~/.claude/skills/twitter/.env
# OR
export X_BEARER_TOKEN=your_token_here
# OR
mkdir -p ~/.config/env && echo 'X_BEARER_TOKEN=your_token_here' >> ~/.config/env/global.env
```

#### OAuth 1.0a (for posting)

Posting requires OAuth 1.0a credentials in addition to the Bearer token.

1. Go to [console.x.com](https://console.x.com) → your project → Keys and tokens
2. Under "Consumer Keys", copy **API Key** and **API Key Secret**
3. Under "Authentication Tokens", generate **Access Token** and **Access Token Secret** (with **Read and Write** permissions)
4. Add all four to `~/.claude/skills/twitter/.env`:

```bash
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### bird CLI

```bash
brew install steipete/tap/bird   # or: npm install -g @steipete/bird
bird whoami                       # verify auth (uses browser cookies)
```

### Smaug (archival)

```bash
cd ~/tools/smaug && npx smaug setup
```

---

## x-search — Official API Research

Run via: `bun run ~/.claude/skills/twitter/x-search/x-search.ts <command>`

### Quick Search (cost-conscious default)

```bash
bun run ~/.claude/skills/twitter/x-search/x-search.ts search "AI agents" --quick
# 1 page, max 10 results, auto noise filter, 1hr cache, cost summary
# Est. cost: ~$0.50
```

### Full Search

```bash
bun run ~/.claude/skills/twitter/x-search/x-search.ts search "Claude Code" --pages 3 --sort likes --since 1d
bun run ~/.claude/skills/twitter/x-search/x-search.ts search "BG3 mods" --from LarianStudios --quality
bun run ~/.claude/skills/twitter/x-search/x-search.ts search "Minoan archaeology" --markdown --save
```

### Search Options

| Flag | Default | Description |
|------|---------|-------------|
| `--quick` | off | 1 page, max 10, noise filter, 1hr cache |
| `--sort` | likes | `likes\|impressions\|retweets\|recent` |
| `--since` | 7d | `1h\|3h\|12h\|1d\|7d` or ISO timestamp |
| `--pages` | 1 | 1-5 pages (100 tweets/page) |
| `--limit` | 15 | Max results displayed |
| `--from` | — | Shorthand for `from:username` |
| `--quality` | off | Filter tweets with < 10 likes |
| `--min-likes` | 0 | Minimum like threshold |
| `--no-replies` | off | Exclude replies |
| `--save` | off | Save markdown to `~/tools/smaug/knowledge/research/` |
| `--json` | off | Raw JSON output |
| `--markdown` | off | Markdown research document |

### Profiles, Threads, Single Tweets

```bash
bun run ~/.claude/skills/twitter/x-search/x-search.ts profile AnthropicAI --count 10
bun run ~/.claude/skills/twitter/x-search/x-search.ts thread 1234567890 --pages 3
bun run ~/.claude/skills/twitter/x-search/x-search.ts tweet 1234567890
```

### Feed -- Daily Reading from Followed Accounts

Pull the latest tweets from named account groups, filtered by time window. Uses batched OR-query search (cheap, ~$0.005/tweet).

```bash
# Read today's tweets from a feed group
bun run ~/.claude/skills/twitter/x-search/x-search.ts feed geopolitics --since 1d

# Last week from all groups
bun run ~/.claude/skills/twitter/x-search/x-search.ts feed all-feeds --since 7d

# Custom accounts (comma-separated)
bun run ~/.claude/skills/twitter/x-search/x-search.ts feed imetatronink,Megatron_ron --since 1d

# Free via bird CLI (no API cost)
bun run ~/.claude/skills/twitter/x-search/x-search.ts feed geopolitics --since 1d --bird

# Save as markdown research doc
bun run ~/.claude/skills/twitter/x-search/x-search.ts feed all-feeds --since 7d --markdown --save
```

Feed options: `--since 1d|7d|1h|3h|12h`, `--limit N` (tweets per account, default 4), `--bird` (free), `--markdown`, `--save`, `--json`, `--no-cache`.

### Feed Groups -- Named Account Collections

```bash
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup                              # list all
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup show geopolitics              # show group
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup create tech "Tech follows"
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup add tech kaboreas "K8s/infra"
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup remove tech kaboreas
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup delete tech
bun run ~/.claude/skills/twitter/x-search/x-search.ts feedgroup alias daily geopolitics,palestine
```

Pre-configured groups: `geopolitics` (18 accounts), `palestine` (3 accounts), alias `all-feeds` (all 21). Stored at `~/.claude/skills/twitter/x-search/data/feedgroups.json`.

### Watchlist

Monitor accounts with batch checking (uses profile API, more expensive).

```bash
bun run ~/.claude/skills/twitter/x-search/x-search.ts watchlist                    # show list
bun run ~/.claude/skills/twitter/x-search/x-search.ts watchlist add kikismith "Ancient art"
bun run ~/.claude/skills/twitter/x-search/x-search.ts watchlist remove kikismith
bun run ~/.claude/skills/twitter/x-search/x-search.ts watchlist check              # check all accounts
```

Watchlist stored at `~/.claude/skills/twitter/x-search/data/watchlist.json`.

### Posting and Replying (OAuth 1.0a)

Post tweets and replies via the official API. Requires OAuth 1.0a credentials (see setup above).

```bash
# Post a tweet
bun run ~/.claude/skills/twitter/x-search/x-search.ts post "Hello from x-search!"

# Reply to a tweet
bun run ~/.claude/skills/twitter/x-search/x-search.ts reply 1234567890 "Great thread!"
```

- 280-character limit enforced
- Cost: $0.01 per post
- Returns the posted tweet URL
- Errors: descriptive messages for missing credentials, permission issues, rate limits

### Cache

15-minute TTL (1hr in quick mode). File-based, auto-managed.

```bash
bun run ~/.claude/skills/twitter/x-search/x-search.ts cache clear
```

### Cost Reference

| Resource | Cost |
|----------|------|
| Post read | $0.005 |
| User lookup | $0.010 |
| Post create | $0.010 |
| Quick search (~100 tweets) | ~$0.50 |
| 3-page deep search (~300 tweets) | ~$1.50 |
| Profile check | ~$0.51 |
| Cached repeat | FREE |

X API deduplicates reads within 24h. Cache prevents redundant queries within 15min.

---

## bird CLI — Session-Based Operations

Uses undocumented Twitter GraphQL APIs via browser cookies. Free but may break when Twitter rotates internals.

### Posting

```bash
bird tweet "Hello world"
bird reply 123456789 "Great thread!"
bird tweet "With image" --media photo.png --alt "Description"
```

### Reading

```bash
bird read 123456789
bird thread https://x.com/user/status/123456789
bird replies 123456789 --json
```

### Search (free, via GraphQL)

```bash
bird search "query" -n 10
bird search "from:anthropic" -n 20 --json
```

### Monitoring

```bash
bird mentions -n 10
bird bookmarks -n 20
bird likes -n 20
bird following -n 50
bird followers -n 50
```

### Maintenance

```bash
bird whoami          # verify auth
bird check           # credential sources
bird query-ids --fresh  # refresh when Twitter rotates IDs
```

---

## Smaug — Bookmark Archival

Archives bookmarks/likes to organized markdown with AI categorization.

```bash
cd ~/tools/smaug
npx smaug run                    # fetch + process with Claude
npx smaug fetch 20               # fetch only
npx smaug fetch --source likes   # likes instead of bookmarks
npx smaug run -t                 # track token costs
npx smaug status                 # check state
```

Output: `bookmarks.md`, `knowledge/tools/`, `knowledge/articles/`

---

## Research Methodology

For deep X research, follow this agentic loop:

1. **Decompose** — Break topic into 2-3 search queries targeting different angles
2. **Search** — Run each query with `--quick` first to assess signal quality
3. **Refine** — Narrow queries based on initial results (add `--from`, `--quality`, `--since`)
4. **Thread** — Follow high-value conversation threads for deeper context
5. **Deep-Dive** — Re-run best queries with `--pages 3 --markdown --save`
6. **Synthesize** — Compile findings from saved markdown into analysis

Default to `--quick` for exploratory queries. Use full mode only for confirmed-valuable searches.

---

## Troubleshooting

### x-search: "X_BEARER_TOKEN not found"

Set token via env, `~/.config/env/global.env`, or `~/.claude/skills/twitter/.env`. Get one at [console.x.com](https://console.x.com).

### bird: 403 Errors

Browser cookies expired. Log into Twitter in browser, then `bird check`.

### bird: Query ID Errors

Twitter rotated internals. Run `bird query-ids --fresh`.

### Rate Limiting (429)

Wait for reset. x-search shows reset time. bird: wait a few minutes.

---

## When to Use Which

| Task | Tool | Why |
|------|------|-----|
| Search tweets by topic | x-search | Official API, cost-tracked, cached |
| Research a topic deeply | x-search | Multi-page, markdown output, save |
| Monitor specific accounts | x-search watchlist | Batch check with cost tracking |
| Post a tweet or reply | x-search post/reply | Official API, reliable, $0.01/post |
| Post with media | bird | Free, media upload support |
| Read a specific tweet/thread | bird (free) or x-search (tracked) | bird for quick reads, x-search for research |
| Check mentions | bird | Free, real-time |
| Archive bookmarks | smaug | AI categorization, markdown output |
| Fetch bookmarks/likes | bird + smaug | Session-based access |
