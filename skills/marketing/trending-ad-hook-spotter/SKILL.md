---
name: trending-ad-hook-spotter
description: >
  Monitor Twitter/X, Reddit, LinkedIn, and Hacker News for trending narratives,
  viral posts, and hot-button topics in your space. Maps trends to ad hook
  opportunities with timing urgency scores. Tells you what to run ads about
  right now while the topic is hot.
tags: [ads]
---

# Trending Ad Hook Spotter

Scan social platforms for what's trending in your space right now — viral posts, hot debates, breaking news, memes — and translate each trend into a concrete ad hook you can run while the topic is still hot.

**Core principle:** The highest-performing ads ride cultural and industry moments. This skill finds those moments before your competitors do and tells you exactly how to capitalize.

## When to Use

- "What's trending in our space that we could run ads about?"
- "Find viral hooks for our paid campaigns"
- "What topics are hot in [industry] right now?"
- "I want to ride a trend with a paid campaign"
- "What should we be running ads about this week?"

## Phase 0: Intake

1. **Your product** — Name + one-line description
2. **Industry/category** — What space are you in? (e.g., "AI sales tools", "developer infrastructure")
3. **ICP keywords** — 5-10 keywords that define your buyer's world
4. **Competitor names** — So we can spot when they become part of a trend
5. **Platforms to scan** (default: all):
   - Twitter/X
   - Reddit (specific subreddits if known)
   - LinkedIn
   - Hacker News
6. **Content velocity** — How fast can you create ads? (Same-day / 2-3 days / Weekly)

## Phase 1: Social Scanning

### 1A: Twitter/X Trend Scan

Run `twitter-scraper` with multiple queries:

```bash
# Industry trending topics
python3 skills/twitter-scraper/scripts/scrape_twitter.py \
  --query "<industry keyword> (viral OR trending OR hot take OR unpopular opinion OR thread)" \
  --max-results 50 \
  --sort top

# Competitor mentions (momentum signals)
python3 skills/twitter-scraper/scripts/scrape_twitter.py \
  --query "<competitor1> OR <competitor2> (raised OR launched OR shut down OR acquired OR outage)" \
  --max-results 30

# Pain/frustration spikes
python3 skills/twitter-scraper/scripts/scrape_twitter.py \
  --query "<category> (broken OR frustrating OR tired of OR switched from)" \
  --max-results 30
```

Score each tweet/thread by engagement velocity (likes + retweets relative to account size and age).

### 1B: Reddit Trend Scan

Run `reddit-scraper`:

```bash
python3 skills/reddit-scraper/scripts/scrape_reddit.py \
  --subreddits "<relevant_subreddits>" \
  --sort hot \
  --time week \
  --limit 30
```

Look for:
- Posts with unusually high upvote/comment ratios
- "What do you use for [X]?" threads (buying intent)
- Complaint threads about incumbents
- "I just switched from X to Y" posts

### 1C: LinkedIn Trend Scan

Run `linkedin-profile-post-scraper` for 5-10 KOLs in the space:

```bash
python3 skills/linkedin-profile-post-scraper/scripts/scrape_linkedin_posts.py \
  --urls "<kol_profile_urls>" \
  --max-posts 10
```

Identify high-engagement posts on topics relevant to your product category.

### 1D: Hacker News Scan

Run `hacker-news-scraper`:

```bash
python3 skills/hacker-news-scraper/scripts/scrape_hn.py \
  --query "<industry keyword>" \
  --type story \
  --sort points \
  --limit 20
```

## Phase 2: Trend Identification & Scoring

### Trend Detection Framework

Group collected signals into trends. A "trend" is:
- A topic appearing across 2+ platforms within the past 7 days
- A single post/thread with exceptional engagement (10x+ the norm)
- A breaking event (funding, acquisition, outage, launch) with cascading conversation

### Score Each Trend

| Factor | Weight | Description |
|--------|--------|-------------|
| **Recency** | 25% | How fresh? (< 24h = max, > 7 days = low) |
| **Velocity** | 25% | Is engagement accelerating or decelerating? |
| **Cross-platform** | 20% | Appearing on multiple platforms? |
| **ICP relevance** | 20% | Does your target buyer care about this? |
| **Product fit** | 10% | Can you credibly connect your product to this trend? |

**Total score out of 100. Urgency tiers:**
- **90-100:** Run today — this peaks within 24-48h
- **70-89:** Run this week — 3-5 day window
- **50-69:** Worth testing — stable trend, less time pressure
- **Below 50:** Monitor — not actionable yet

## Phase 3: Hook Translation

For each trend scoring 50+, generate:

### Ad Hook Formula

```
[Trend reference] + [Your unique angle] + [CTA tied to the moment]
```

### Per Trend, Produce:

1. **Trend summary** — What's happening in 2 sentences
2. **Why it's an ad opportunity** — Connection to your product/ICP
3. **3 hook variants:**
   - **Newsjack hook** — Reference the trend directly ("Everyone's talking about X. Here's what they're missing...")
   - **Contrarian hook** — Take the opposite stance ("Hot take: [trend] doesn't matter. Here's what does...")
   - **Practical hook** — Offer a solution related to the trend ("[Trend] means you need [your feature] now")
4. **Recommended format** — Static / video / carousel / search ad
5. **Recommended platform** — Where the trend is hottest
6. **Time window** — How long before this trend fades

## Phase 4: Output Format

```markdown
# Trending Ad Hooks — [DATE]

Industry: [category]
Platforms scanned: [list]
Trends identified: [N]
Actionable hooks (score 50+): [N]

---

## 🔴 Run Today (Score 90+)

### Trend: [Trend Title]
**What's happening:** [2-sentence summary]
**Engagement signal:** [X likes/comments across Y platforms in Z hours]
**Time window:** [Estimated hours/days before this fades]

**Hook 1 (Newsjack):** "[Ad headline]"
> [1-2 sentence body copy]
- Format: [Static/Video/Carousel]
- Platform: [Twitter/Meta/Google/LinkedIn]

**Hook 2 (Contrarian):** "[Ad headline]"
> [Body copy]

**Hook 3 (Practical):** "[Ad headline]"
> [Body copy]

---

## 🟡 Run This Week (Score 70-89)

[Same format]

---

## 🟢 Worth Testing (Score 50-69)

[Same format, briefer]

---

## Trend Velocity Dashboard

| Trend | Twitter | Reddit | LinkedIn | HN | Score | Window |
|-------|---------|--------|----------|----|----|--------|
| [Trend 1] | ▲▲▲ | ▲▲ | ▲ | — | 92 | 24h |
| [Trend 2] | ▲▲ | — | ▲▲▲ | ▲ | 78 | 5d |
| [Trend 3] | ▲ | ▲▲ | — | ▲▲ | 61 | 2w |

---

## Competitor Trend Involvement

| Trend | Competitor Riding It? | Their Angle | Your Counter-Angle |
|-------|----------------------|-------------|-------------------|
| [Trend] | [Y/N — who] | [Their take] | [Your differentiated take] |
```

Save to `clients/<client-name>/ads/trending-hooks-[YYYY-MM-DD].md`.

## Scheduling

Run weekly or on-demand when you need fresh hooks:

```bash
0 8 * * 1 python3 run_skill.py trending-ad-hook-spotter --client <client-name>
```

## Cost

| Component | Cost |
|-----------|------|
| Twitter scraper (3 queries) | ~$0.15-0.30 (Apify) |
| Reddit scraper | ~$0.05-0.10 (Apify) |
| LinkedIn scraper (5-10 KOLs) | ~$0.25-0.50 (Apify) |
| HN scraper | Free |
| Analysis & hook generation | Free (LLM reasoning) |
| **Total** | **~$0.45-0.90** |

## Tools Required

- **Apify API token** — `APIFY_API_TOKEN` env var
- **Upstream skills:** `twitter-scraper`, `reddit-scraper`, `linkedin-profile-post-scraper`, `hacker-news-scraper`

## Trigger Phrases

- "What's trending we could run ads about?"
- "Find viral hooks for our campaigns"
- "What's hot in [space] this week?"
- "Newsjacking opportunities for [client]"
- "Run the trending hook spotter"
