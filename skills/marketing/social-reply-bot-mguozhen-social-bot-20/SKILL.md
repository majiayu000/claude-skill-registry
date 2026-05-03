---
name: social-reply-bot
description: "Reddit & X/Twitter auto-reply bot for ecommerce/SaaS growth. Finds relevant posts about AI customer service, Amazon FBA, Shopify — posts genuine AI-generated replies mentioning your product. Includes Reddit account warmup (karma building) and lead tracking. Triggers: social reply bot, reddit auto reply, twitter auto reply, x auto reply, social media bot, amazon seller engagement, ecommerce social engagement, reddit warmup, karma building, warmup reddit, social leads, potential customers"
allowed-tools: Bash
metadata:
  openclaw:
    homepage: https://github.com/mguozhen/social-bot
---

# Social Reply Bot

Automatically finds and replies to relevant Reddit and X/Twitter posts about ecommerce, Amazon FBA, and AI customer service. Also builds Reddit account karma and tracks potential customer leads.

## Commands

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

## Setup

```bash
curl -fsSL https://raw.githubusercontent.com/mguozhen/social-bot/main/install.sh | bash
```

## Requirements

- `browse` CLI: `npm install -g @browserbasehq/browse-cli`
- Log in to Reddit and X in the browse-controlled Chrome window
- `ANTHROPIC_API_KEY` in `.env`

## Features

### Daily Reply Bot
- Searches subreddits and X for posts matching your product keywords
- Claude generates genuine, on-topic replies (not spam)
- Browser automation — no Reddit/X API key needed
- SQLite deduplication — never replies to the same post twice

### Reddit Warmup (karma building)
- Visits low-moderation subreddits (r/karma, r/CasualConversation, r/self)
- Claude Haiku generates authentic short comments (no product mentions)
- Natural delays between posts (90–180s)
- Builds Comment Karma to unlock restricted subreddits

### Lead Tracking
- Every replied post analyzed by Claude for customer potential
- Scored 1–10 with urgency level
- Extracts business type and pain points
- View with: `social reply bot leads`

## Configuration

Edit `~/social-bot/config.json` to set your subreddits, X search queries, product descriptions, and daily targets.
