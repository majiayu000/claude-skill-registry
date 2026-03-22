---
name: trendhunter
description: "Monitors the web for topics you care about and surfaces signals before they peak. Tracks Twitter, Reddit, Hacker News, Product Hunt, and custom sources. Use when: staying ahead of industry trends, monitoring competitors, or catching viral content early. NOT for: social media analytics dashboards, sentiment analysis at scale, or building trend prediction models."
homepage: https://pawhub.ai/trendhunter
metadata:
  {
    "openpaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["curl", "jq"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/trendhunter",
              "bins": ["trendhunter"],
              "label": "Install TrendHunter (npm)",
            },
          ],
      },
  }
---

# TrendHunter 🔍

Catch trends before they blow up. Monitor keywords across Twitter, Reddit, HN, Product Hunt, and custom sources. Get pinged when something's heating up.

## When to Use

✅ **USE this skill when:**

- Monitoring industry keywords (e.g., "AI agents," "web3")
- Tracking competitor mentions
- Catching viral content early
- Staying on top of tech/product launches
- Finding breaking news in your niche
- Discovering emerging technologies
- Monitoring brand mentions
- Spotting opportunities before they peak

## When NOT to Use

❌ **DON'T use this skill when:**

- Building full social media analytics dashboards → use Sprout Social, Hootsuite
- Large-scale sentiment analysis → use Brandwatch, Meltwater
- Training trend prediction ML models → use historical datasets
- Real-time stock trading signals → use specialized fintech tools
- Competitive intelligence at enterprise scale → use Crayon, Klue
- Academic research on social trends → use proper research tools

## Setup

Install TrendHunter:

```bash
npm install -g @pawhub/trendhunter
```

Configure sources:

```bash
# Twitter/X (via API or scraping)
trendhunter add-source twitter --api-key YOUR_KEY

# Reddit
trendhunter add-source reddit

# Hacker News
trendhunter add-source hackernews

# Product Hunt
trendhunter add-source producthunt --api-key YOUR_KEY

# Custom RSS feeds
trendhunter add-source rss --url https://example.com/feed

# Verify sources
trendhunter sources list
```

## Example Interactions

### Setting Up Watches

**You:** Watch for mentions of "AI agents"

**Paw:** *configures trend watch*

✅ **Tracking:** "AI agents"

**Sources:**
- Twitter/X (tracking keyword + hashtags)
- Hacker News (stories + comments)
- Reddit (r/artificial, r/MachineLearning, r/technology)
- Product Hunt (product descriptions + comments)

**Baseline activity (last 7 days):** 342 mentions/day

**Alert triggers:**
- 🔥 Spike: >2x baseline (>680 mentions/day)
- 📈 Trending: sustained 50% increase over 48 hours
- 🌟 Viral post: single post with >1000 engagements

**Notification:** Telegram (instant)

I'll ping you when something moves. 🎯

---

**You:** Also watch "GPT-5" and "Claude 4"

**Paw:** *adds more watches*

✅ **Now tracking 3 keywords:**

1. **AI agents** (342/day baseline)
2. **GPT-5** (89/day baseline)
3. **Claude 4** (127/day baseline)

All sources active. I'll surface signals when things heat up.

**Pro tip:** These are adjacent topics. Want me to group them into a "AI Models" bundle? (easier notifications)

---

**You:** Yes

**Paw:** ✅ **Bundle created:** "AI Models"

- AI agents
- GPT-5
- Claude 4

Single notification stream for all related activity. Less noise, better signal. 📊

---

### Catching a Trend

**Paw:** 🔥 **Trend Alert: "AI agents" is spiking**

**Activity:** 1,240 mentions (last 24h)
**Baseline:** 342 mentions/day
**Change:** +263% 📈

**Top sources:**
1. **Twitter:** 847 tweets (+312%)
2. **Hacker News:** 3 front-page stories
3. **Reddit:** 156 posts (r/artificial is buzzing)

**Viral posts:**
- Twitter: "@founder: We're open-sourcing our AI agent framework" (8.2k likes, 2.1k retweets)
- HN: "Show HN: Built an AI agent that actually works" (742 points, 289 comments)

**Sentiment:** 78% positive, 15% neutral, 7% critical

**Trend velocity:** Rising fast (peaked 2 hours ago, still elevated)

**Your move:**
- Read top posts? (`/trend read`)
- Save for later? (`/trend save`)
- Set follow-up alert? (`/trend follow`)

What do you want to do? 🔍

---

**You:** Read top posts

**Paw:** **Top 3 Posts:**

**1. Twitter — @founder (8.2k likes)**
> "After 6 months of building, we're open-sourcing our AI agent framework. Works with Claude, GPT-4, and local models. MIT licensed.
>
> Features:
> - Tool calling
> - Memory persistence
> - Multi-agent coordination
>
> Star it: [GitHub link]"

**Engagement:** 8,241 likes, 2,103 retweets, 412 replies
**Vibe:** Very positive, lots of "this is what we needed" energy

---

**2. Hacker News — "Show HN: Built an AI agent that actually works"**
> Solo founder spent 6 months building a production-ready AI agent framework. Open source, well-documented, works with multiple LLM providers.

**Discussion highlights:**
- "Finally, something that doesn't hallucinate tool calls"
- "The memory system is clever"
- "This vs LangChain?"

**Score:** 742 points (trending #3 on front page)
**Comments:** 289 (mostly positive, some technical deep-dives)

---

**3. Reddit — r/artificial**
> "New open-source AI agent framework drops. Actually production-ready."

**Thread:** 156 upvotes, 47 comments
**Top comment:** "Used it this morning. It's legit. Memory actually works."

---

**Summary:**
This is a legit launch, not just noise. Framework looks solid, community reception is strong. Might be worth checking out.

Want me to track this specific project going forward? 🎯

---

**You:** Yes, track it

**Paw:** ✅ **Tracking:** "@founder's agent framework"

I'll monitor:
- GitHub stars/activity
- Social media mentions
- HN/Reddit follow-up discussions
- Related blog posts/tutorials

You'll get updates when there's movement. 📚

---

### Competitive Monitoring

**You:** Watch my competitor "CompetitorCo"

**Paw:** *sets up competitor watch*

**Tracking:** CompetitorCo

**Monitoring:**
- Brand mentions (Twitter, Reddit, HN)
- Product launches (Product Hunt, Twitter)
- Hiring activity (LinkedIn, job boards)
- Content releases (blog, Medium)
- Press coverage (TechCrunch, The Verge, etc.)

**Baseline (last 30 days):**
- 47 mentions/day
- Last launch: 23 days ago ("Feature X")
- Recent press: TechCrunch (2 weeks ago)

**Alert me when:**
- New product launch detected
- Significant press coverage (Tier 1 outlets)
- Mention spike (>2x normal)
- Major hiring push

Sound good? 🔍

---

**You:** Yes

**Paw:** ✅ Competitor watch active. I'll keep you posted on their moves. 🕵️

*3 days later...*

🚨 **Competitor Alert: CompetitorCo**

**Activity:** New product launch detected

**Source:** Product Hunt (posted 2 hours ago)
**Product:** "FeatureY — The thing you've been asking for"
**Votes:** 287 (trending #2)
**Comments:** 43

**Description snippet:**
> "FeatureY solves [problem] with [approach]. Built for [target audience]."

**Early reception:** Positive (89% upvote rate)
**Founder comment:** Active in replies, engaging with users

**Your move:**
- Check it out? [Product Hunt link]
- Track mentions? (watch "FeatureY" keyword)
- Analyze approach? (I can pull full details)

Want the full breakdown? 📊

---

### Morning Digest

**Paw:** ☀️ **TrendHunter Daily Digest**

**Watches:** 8 active

**Activity (last 24h):**

**🔥 Trending:**
1. **"AI agents"** — 890 mentions (+160%)
   - Twitter: New framework launch (still buzzing)
   - HN: 2 front-page stories

2. **"CompetitorCo"** — 312 mentions (+564%)
   - Product Hunt: FeatureY launch (trending #2)
   - Twitter: Founder thread gaining traction

**📊 Normal Activity:**
- "GPT-5" — 94 mentions (steady)
- "Claude 4" — 118 mentions (slight uptick)

**💤 Quiet:**
- Other watches below baseline (no signals)

**Top Stories (curated):**
1. [Twitter] AI agent framework goes viral (8k+ likes)
2. [HN] "Show HN: Production-ready agent" (742 pts)
3. [PH] CompetitorCo launches FeatureY (#2 trending)

**Action items:**
- Consider checking out the AI agent framework
- Monitor CompetitorCo's FeatureY reception

Have a good day. 🔍🐾

## Commands

### Watch Management

```bash
# Add watch
trendhunter watch "AI agents" \
  --sources twitter,reddit,hn \
  --alert spike,trending

# Add with custom threshold
trendhunter watch "startup funding" \
  --threshold 2.5x \
  --min-baseline 50

# Create bundle
trendhunter bundle create "AI Models" \
  --keywords "GPT-5,Claude 4,Gemini 2"

# List active watches
trendhunter watch list

# Remove watch
trendhunter watch remove "AI agents"

# Pause watch temporarily
trendhunter watch pause "AI agents"
```

### Competitor Monitoring

```bash
# Track competitor
trendhunter competitor add "CompetitorCo" \
  --monitor launches,press,mentions

# Add multiple competitors
trendhunter competitor add-bulk competitors.txt

# Show competitor activity
trendhunter competitor report "CompetitorCo"

# Compare competitors
trendhunter competitor compare "CompA" "CompB"
```

### Trend Analysis

```bash
# Current trending topics
trendhunter trending --source twitter --last 24h

# Keyword velocity
trendhunter velocity "AI agents" --chart

# Sentiment analysis
trendhunter sentiment "AI agents" --sources all

# Topic clusters
trendhunter clusters --keywords "AI,ML,agents"

# Export trend data
trendhunter export "AI agents" --format csv --days 30
```

### Alerts & Notifications

```bash
# Configure alert thresholds
trendhunter alert config "AI agents" \
  --spike 2x \
  --trending 1.5x \
  --viral 1000

# Notification channels
trendhunter notify set telegram,email

# Alert schedule (quiet hours)
trendhunter notify quiet 22:00-08:00

# Test notification
trendhunter notify test
```

### Reports

```bash
# Daily digest
trendhunter report daily

# Weekly roundup
trendhunter report weekly

# Custom report
trendhunter report custom \
  --watches "AI agents,GPT-5" \
  --days 7 \
  --format markdown
```

## Source Configuration

```bash
# Add Twitter/X
trendhunter source add twitter --api-key YOUR_KEY --api-secret YOUR_SECRET

# Add Reddit (no auth needed)
trendhunter source add reddit

# Add Hacker News (no auth needed)
trendhunter source add hackernews

# Add Product Hunt
trendhunter source add producthunt --api-key YOUR_KEY

# Add custom RSS
trendhunter source add rss --url https://blog.example.com/feed --name "Example Blog"

# Test source
trendhunter source test twitter

# Remove source
trendhunter source remove twitter
```

## Telegram Integration

**Quick checks:**

**You:** `/trend check "AI agents"`

**Paw:** **"AI agents"** activity (last 24h):

📊 847 mentions (+148% vs baseline)
🔥 Status: Trending
📈 Velocity: Rising

Top post: "@founder: open-sourcing framework" (8.2k likes)

---

**Daily digest:**

**You:** `/trend digest`

**Paw:** *sends formatted digest*

**TrendHunter Digest:**
- 🔥 2 trending
- 📊 4 normal
- 💤 2 quiet

React for details or `/trend report` for full breakdown.

---

**Quick actions:**
- `/trend add "keyword"` — Add watch
- `/trend top` — Show top trending
- `/trend competitor CompanyName` — Competitor report

## Configuration

```bash
# Show config
trendhunter config show

# Default sources
trendhunter config set default-sources "twitter,reddit,hn"

# Check frequency
trendhunter config set check-interval 30 # minutes

# Alert threshold
trendhunter config set default-threshold 2.0 # 2x baseline

# Sentiment analysis
trendhunter config set sentiment-enabled true

# Language
trendhunter config set language en

# Time zone
trendhunter config set timezone "America/Los_Angeles"
```

## Tips from Paw

> "Start with 3-5 keywords max. More than that and you'll drown in notifications. Quality over quantity."

> "Competitor monitoring is where this shines. You'll know about their launches before their own customers do."

> "The daily digest is non-negotiable. Set it for 8 AM. You'll catch trends while drinking coffee."

> "Use bundles for related terms. 'AI agents,' 'GPT-5,' 'Claude 4' should be one bundle, not three separate watches."

> "Baselines take 7 days to stabilize. Don't panic if early alerts seem noisy. It learns your patterns."

## Pricing

- **Free tier:** 3 watches, 2 sources, daily digest
- **Pro:** $12/month — 20 watches, all sources, hourly checks, sentiment analysis
- **Team:** $39/month — unlimited watches, competitor monitoring, API access, shared dashboards

Install from PawHub or [pawhub.ai/trendhunter](https://pawhub.ai/trendhunter)

## Privacy

- No social media credentials stored (read-only API access)
- Keyword watches stored locally on your gateway
- Social data is ephemeral (not permanently stored)
- Export your data anytime
- Can run fully offline with RSS-only sources

## Notes

- Twitter/X requires API access (paid tiers recommended for high volume)
- Reddit and Hacker News work without authentication
- Product Hunt requires free API key
- Baseline calculation: 7-day rolling average
- Alerts use statistical thresholds (configurable)
- Supports regex for advanced keyword matching

---

Built for people who want to catch waves before they crest. 🔍🐾
