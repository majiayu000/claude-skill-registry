<p align="center">
  <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" width="80" alt="Social Bot">
</p>

<h1 align="center">Social Reply Bot</h1>

<p align="center">
  <strong>AI-powered Reddit & X auto-reply bot that finds your customers and joins the conversation.</strong>
</p>

<p align="center">
  <a href="#quick-start"><img src="https://img.shields.io/badge/setup-5min-brightgreen?style=flat-square" alt="5min Setup"></a>
  <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-blue?style=flat-square" alt="Agent Skills"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/platforms-Reddit%20%2B%20X-FF4500?style=flat-square" alt="Reddit + X">
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#screenshots">Screenshots</a> &bull;
  <a href="#configuration">Configuration</a> &bull;
  <a href="#architecture">Architecture</a>
</p>

---

## What is this?

**Social Reply Bot** searches Reddit and X/Twitter for posts relevant to your product, then uses Claude AI to generate genuine, helpful replies that naturally mention your brand. No API keys for Reddit or X required — it uses browser automation to act like a real user.

**Not spam.** The AI evaluates every post for relevance first. If a post isn't a good fit, it skips it. When it does reply, it sounds like an experienced practitioner sharing real insight — because that's what the prompt engineers it to be.

Currently configured for two products:
- **[Solvea](https://solvea.cx)** — AI customer service agent for Amazon/Shopify sellers
- **[VOC.ai](https://voc.ai)** — Amazon review intelligence and sentiment analysis

But it's fully configurable for any product/niche via `config.json`.

## Features

| Feature | Description |
|---------|-------------|
| **Dual Platform** | Reddit (subreddit search) + X/Twitter (keyword search) |
| **AI-Generated Replies** | Claude crafts genuine, on-topic responses — not templates |
| **Smart Filtering** | Two-layer filter: keyword match first, then AI relevance check |
| **Browser Automation** | No platform API keys needed — uses real browser sessions |
| **Reddit Warmup** | Karma-building mode for new accounts (safe subreddits, no product mentions) |
| **Lead Tracking** | Every replied post scored 1-10 for customer potential |
| **Web Dashboard** | Real-time Flask dashboard showing daily progress |
| **Deduplication** | SQLite-backed — never replies to the same post twice |
| **Rate Limiting** | Configurable delays (Reddit: 10min, X: 5min between replies) |
| **Daily Scheduling** | macOS LaunchAgent runs at 10:05 AM automatically |

## How It Works

```
Keyword Search (Reddit subreddits + X queries)
       ↓
Two-Layer Relevance Filter
  ├─ Layer 1: Keyword match (zero API cost)
  └─ Layer 2: Claude AI judges if post is worth replying to
       ↓
Claude generates reply as "experienced seller sharing real insight"
       ↓
Browser automation posts the reply
       ↓
SQLite logs it → Dashboard displays it → Lead scored
```

**The core principle:** Every reply must provide genuine value. The AI is prompted as a "seller with 5 years of experience" who naturally mentions tools they use — not as a marketer pushing a product. Posts that don't fit get skipped, not force-fitted.

## Screenshots

### Dashboard — Real-time Daily Progress

<p align="center">
  <img src="docs/screenshot_dashboard.png" width="700" alt="Dashboard showing daily reply targets and progress">
</p>

The web dashboard tracks daily X posts, Reddit comments, product mentions, and historical totals.

### X/Twitter — Targeted Competitive Replies

<p align="center">
  <img src="docs/screenshot_x_reply.png" width="700" alt="AI-generated reply on X to a competitor's post">
</p>

The bot found a competitor's tweet about customer support automation and replied with a genuine insight that naturally positioned Solvea as an alternative. No "Great product!" fluff — real technical substance.

### Reddit — High-Quality Community Comments

<p align="center">
  <img src="docs/screenshot_reddit_reply.png" width="700" alt="AI-generated Reddit comment about WooCommerce chatbot issues">
</p>

On r/ecommerce, a user discussed WooCommerce chatbot inventory sync issues. The bot shared specific technical experience (event-triggered vs. scheduled sync), earning genuine upvotes and discussion.

## Quick Start

### Option 1: One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/mguozhen/social-bot/main/install.sh | bash
```

This will:
1. Clone the repo to `~/social-bot`
2. Install Python dependencies (`anthropic`, `flask`)
3. Check for `browse` CLI
4. Guide you through `.env` setup
5. Initialize SQLite database
6. Register macOS LaunchAgent (daily 10:05 AM)

### Option 2: Manual Setup

```bash
git clone https://github.com/mguozhen/social-bot.git ~/social-bot
cd ~/social-bot
pip3 install -r requirements.txt
cp .env.template .env
# Edit .env with your ANTHROPIC_API_KEY
```

### Prerequisites

| Requirement | How to Get It |
|------------|---------------|
| Python 3.9+ | Pre-installed on macOS |
| `browse` CLI | `npm install -g @anthropic-ai/browse-cli` |
| Anthropic API Key | [console.anthropic.com](https://console.anthropic.com) |
| Reddit account | Log in once in the browse-controlled Chrome |
| X/Twitter account | Log in once in the browse-controlled Chrome |

> **No Reddit API key or Twitter API key required.** The bot uses browser sessions, not platform APIs.

## Commands

### As Claude Code Skill

Once installed as a skill, just tell Claude:

```
social reply bot                  # run both platforms
social reply bot x only           # X/Twitter only
social reply bot reddit only      # Reddit only
social reply bot warmup           # build Reddit karma (8 comments)
social reply bot warmup 15        # warmup with custom target
social reply bot leads            # show potential customers found
social reply bot stats            # today's stats
social reply bot dashboard        # open web dashboard
```

### As Standalone Script

```bash
python3 run_daily.py              # run both platforms
python3 run_daily.py --x-only     # X only
python3 run_daily.py --reddit-only # Reddit only
python3 warmup_reddit.py          # karma building mode
```

## Configuration

Edit `config.json` to customize for your product:

```json
{
  "x": {
    "username": "@YourAccount",
    "daily_target": 20,
    "min_delay_seconds": 300,
    "search_queries": [
      "your product keyword 1",
      "your product keyword 2"
    ]
  },
  "reddit": {
    "username": "your_reddit_user",
    "daily_target": 10,
    "min_delay_seconds": 600,
    "subreddits": ["YourTargetSubreddit", "AnotherOne"]
  },
  "products": {
    "YourProduct": {
      "description": "What your product does (AI uses this to craft mentions)",
      "trigger_keywords": ["keyword1", "keyword2"]
    }
  },
  "reply_style": {
    "tone": "knowledgeable practitioner sharing experience",
    "max_length_x": 260,
    "max_length_reddit": 400,
    "rules": [
      "Lead with genuine insight about the post",
      "Mention product as 'what we use/built' — not as an ad",
      "Skip if not relevant — never force a mention"
    ]
  }
}
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Claude API key for reply generation |
| `BROWSERBASE_API_KEY` | No | Optional: persistent browser sessions across reboots |
| `BROWSERBASE_PROJECT_ID` | No | Optional: pairs with Browserbase key |

## Architecture

```
social-bot/
├── bot/
│   ├── ai_engine.py        # Claude AI: relevance filter + reply generation
│   ├── browser.py           # Browser automation via browse CLI
│   ├── db.py                # SQLite: dedup, history, lead scoring
│   ├── reddit_bot.py        # Reddit: search subreddits, post comments
│   └── x_bot.py             # X/Twitter: search queries, post replies
├── dashboard/
│   ├── app.py               # Flask web dashboard
│   └── templates/           # Dashboard HTML
├── docs/
│   ├── screenshot_dashboard.png
│   ├── screenshot_reddit_reply.png
│   └── screenshot_x_reply.png
├── launchd/                 # macOS LaunchAgent plist
├── config.json              # Platform targets, keywords, products
├── run_daily.py             # Main entry point (scheduled daily)
├── warmup_reddit.py         # Reddit karma builder
├── install.sh               # One-line installer
├── setup.sh                 # Manual setup helper
├── SKILL.md                 # Claude Code / Agent Skills definition
└── .env.template            # Credential template
```

### Two-Layer Filtering

```python
# Layer 1: Fast keyword match (zero API cost)
def detect_product(text: str) -> Optional[str]:
    # Returns matching product name or None

# Layer 2: Claude AI relevance check
# If Layer 1 matches, Claude decides:
#   - Is this post genuinely relevant?
#   - Can we add real value with a reply?
#   - SKIP if forcing a mention would feel unnatural
```

### Rate Limiting & Safety

| Platform | Delay Between Replies | Daily Cap | Deduplication |
|----------|----------------------|-----------|---------------|
| Reddit | 10 minutes | 10 posts | SQLite (URL-based) |
| X/Twitter | 5 minutes | 20 posts | SQLite (URL-based) |

## Reddit Warmup

New Reddit accounts need karma before posting in restricted subreddits. The warmup mode:

- Visits safe, low-moderation subreddits (r/karma, r/CasualConversation, r/self)
- Claude Haiku generates authentic short comments (no product mentions)
- 90-180 second natural delays between posts
- Default: 8 comments per session, configurable

```bash
python3 warmup_reddit.py          # default 8 comments
python3 warmup_reddit.py --target 15  # custom target
```

## Expected Results

With default settings (X: 20/day, Reddit: 10/day):

| Metric | Monthly |
|--------|---------|
| Posts covered | 600+ targeted posts |
| Users reached | 600+ people actively discussing your niche |
| Click-through | ~10-15% visit your profile/link |
| Cost | ~$0.30/day (Claude API at ~$0.01/reply) |

This isn't viral growth — it's **consistent, targeted brand presence** in conversations where your product is genuinely relevant.

## Known Limitations

| Issue | Cause | Workaround |
|-------|-------|------------|
| Reddit comments auto-removed | Account karma < 10 or age < 10 days | Run `warmup` mode for 1-2 weeks first |
| Some X replies fail | Page structure changes or rate limits | Auto-retry with backoff, skips on persistent failure |
| Low match rate on some days | Today's posts don't match your keywords | Add more subreddits and search queries |

## FAQ

<details>
<summary><strong>Is this against Reddit/X terms of service?</strong></summary>

This tool uses browser automation (not API abuse) and generates unique, contextually relevant responses (not spam). However, automated posting always carries platform risk. Use responsibly, keep daily volumes reasonable, and ensure your replies genuinely add value to conversations.
</details>

<details>
<summary><strong>How do I add my own product?</strong></summary>

Edit the `products` section in `config.json`. Add your product name, description (used by Claude to craft natural mentions), and trigger keywords. Then update `search_queries` and `subreddits` to target where your audience hangs out.
</details>

<details>
<summary><strong>Can I use this without Claude Code?</strong></summary>

Yes. `run_daily.py` is a standalone script. You just need Python 3.9+, the `browse` CLI, and an Anthropic API key. The Claude Code skill integration is optional.
</details>

<details>
<summary><strong>How much does it cost to run?</strong></summary>

About $0.01 per reply (Claude API). At 30 replies/day, that's roughly $9/month. Browser automation is free — no Reddit or X API fees.
</details>

## Contributing

PRs welcome. Please test your changes with both platforms before submitting.

## License

[MIT](LICENSE)

---

<p align="center">
  Built with <a href="https://claude.ai">Claude AI</a> &bull; Browser automation via <a href="https://www.npmjs.com/package/@anthropic-ai/browse-cli">browse CLI</a>
</p>
