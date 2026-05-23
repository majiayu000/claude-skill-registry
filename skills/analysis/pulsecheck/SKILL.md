---
name: pulsecheck
description: "Query your analytics in plain language via Telegram. Ask 'how many signups yesterday?' and get instant answers from Google Analytics, Plausible, Fathom, Mixpanel, or PostHog. Use when: checking metrics without opening dashboards, quick performance checks, or comparing time periods. NOT for: building custom dashboards, exporting raw data, or real-time streaming analytics."
homepage: https://pawhub.ai/pulsecheck
metadata:
  {
    "openpaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["curl", "jq"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/pulsecheck",
              "bins": ["pulsecheck"],
              "label": "Install PulseCheck (npm)",
            },
          ],
      },
  }
---

# PulseCheck 📊

Query your analytics dashboards using natural language. No more logging in, clicking through tabs, or squinting at charts at 2 AM.

## When to Use

✅ **USE this skill when:**

- "How many signups did we get yesterday?"
- "Show me bounce rate for the homepage"
- "Compare this week's revenue to last week"
- "What's our top traffic source today?"
- "Did the blog post launch move the needle?"
- Quick metric checks without context switching
- Checking numbers from your phone
- Sharing quick stats with the team

## When NOT to Use

❌ **DON'T use this skill when:**

- Building custom dashboards → use the analytics platform directly
- Exporting raw event data → use platform APIs or data warehouse
- Real-time streaming analytics → use dedicated monitoring tools
- Complex funnel analysis → use the full analytics interface
- Attribution modeling → requires specialized tools
- Creating visualizations → use Looker, Tableau, etc.

## Setup

Install the PulseCheck CLI:

```bash
npm install -g @pawhub/pulsecheck
```

Connect your analytics platform (choose one or more):

```bash
# Google Analytics
pulsecheck connect google-analytics --property-id UA-12345678-1

# Plausible
pulsecheck connect plausible --site-id example.com --api-key your-api-key

# Fathom
pulsecheck connect fathom --site-id ABC123 --api-key your-api-key

# Mixpanel
pulsecheck connect mixpanel --project-id 12345 --api-key your-api-key

# PostHog
pulsecheck connect posthog --project-id 1234 --api-key your-api-key

# Verify connection
pulsecheck status
```

Link to Telegram (optional but recommended):

```bash
pulsecheck setup telegram
```

## Example Interactions

### Quick Metrics

**You:** How many visitors yesterday?

**Paw:** *stretches and checks the numbers*

Yesterday: **2,847 visitors** (+12% vs previous day)
- Pageviews: 8,103
- Bounce rate: 42%
- Avg session: 3m 22s

Top pages:
1. /blog/launch-post — 1,204 views
2. /pricing — 892 views
3. / — 654 views

Looks like the launch post is doing well. Want the full breakdown? 📈

---

**You:** Show me signups this week

**Paw:** *taps keyboard with one paw*

This week (Mon–today): **137 signups**

Breakdown:
- Monday: 18
- Tuesday: 31 ⬆️
- Wednesday: 24
- Thursday: 42 🔥 (best day)
- Today so far: 22

Conversion rate: 4.8% (up from 4.1% last week)

That Thursday spike is interesting. Any campaigns running? 🤔

---

**You:** Compare revenue this month vs last month

**Paw:** *pulls up the numbers while yawning*

**This month (so far):** $24,380
**Last month (full):** $31,200

📉 Trending -22% (but we're only 18 days in)

Projected end-of-month: ~$40,500 (+30% vs last month)

Daily average:
- This month: $1,354/day
- Last month: $1,006/day

Looking good actually. Revenue per day is way up. 💰

---

**You:** What's our top traffic source?

**Paw:** *checks the logs*

Top traffic sources (last 7 days):

1. **Organic search** — 1,847 visits (43%)
   - Google: 1,623
   - Bing: 224

2. **Direct** — 982 visits (23%)

3. **Social** — 756 visits (18%)
   - Twitter: 512
   - LinkedIn: 244

4. **Referral** — 498 visits (12%)
   - news.ycombinator.com: 287 🔥
   - reddit.com: 156

5. **Email** — 201 visits (5%)

That HN spike is still paying dividends. Nice. 🎯

---

**You:** Did the blog post launch move the needle?

**Paw:** *digs into the data*

Blog post published: **Wednesday 3 PM**

Impact analysis:

**Traffic:**
- Wed (before): 1,204 visitors
- Wed (after): 3,102 visitors (+158%)
- Thursday: 4,287 visitors (sustained)
- Friday: 2,918 visitors (normalizing)

**Signups:**
- Wed: 24 → 42 after publish (+75%)
- Thursday: 38 (still elevated)

**Top referrers (post-launch):**
- twitter.com/yourhandle — 1,203 visits
- news.ycombinator.com — 847 visits
- Direct: 654 (probably newsletter)

Short answer: **Yes. Big yes.** 🚀

The spike is real and converting well. HN + Twitter combo is lethal.

## Commands

### Quick Queries

```bash
# Visitors yesterday
pulsecheck query "visitors yesterday"

# Signups this week
pulsecheck query "signups this week"

# Top pages today
pulsecheck query "top pages today"

# Bounce rate for homepage
pulsecheck query "bounce rate /homepage"

# Compare time periods
pulsecheck query "compare revenue this month vs last month"
```

### Scheduled Reports

```bash
# Daily summary at 8 AM
pulsecheck schedule daily "summary" --time "08:00" --telegram

# Weekly report every Monday
pulsecheck schedule weekly "full report" --day monday --time "09:00"

# List scheduled reports
pulsecheck schedule list

# Remove a scheduled report
pulsecheck schedule remove <report-id>
```

### Custom Metrics

```bash
# Define a custom metric
pulsecheck metric create "mrr" \
  --query "sum(subscriptions.amount) where status=active" \
  --format "currency"

# Query your custom metric
pulsecheck query "mrr this month"
```

## Telegram Integration

Once connected, you can ask Paw directly via Telegram:

**You:** `/pulse visitors today`

**Paw:** 1,847 visitors so far today (+22% vs yesterday same time). Traffic is looking healthy. 📊

---

**You:** `/pulse top sources this week`

**Paw:** *sends formatted table*

```
Source         Visits    %
─────────────────────────────
Organic        3,102    45%
Direct         1,847    27%
Social         1,203    18%
Referral         654    10%
```

Organic is crushing it this week. 🔍

## Natural Language Processing

PulseCheck understands flexible queries:

- "How many people visited yesterday?"
- "Show me yesterday's visitors"
- "Visitor count for yesterday"
- "What was traffic like yesterday?"

All work the same way. No rigid syntax required.

## Supported Platforms

| Platform | Metrics Available |
|----------|-------------------|
| **Google Analytics** | Visitors, pageviews, bounce rate, session duration, goals, events |
| **Plausible** | Visitors, pageviews, bounce rate, sources, countries, pages |
| **Fathom** | Pageviews, visitors, average time, top pages, referrers |
| **Mixpanel** | Events, funnels, retention, user properties, cohorts |
| **PostHog** | Events, sessions, user paths, feature flags, A/B tests |

## Configuration

```bash
# Show current config
pulsecheck config show

# Set default time zone
pulsecheck config set timezone "America/Los_Angeles"

# Set default date range
pulsecheck config set default-range "7d"

# Toggle Telegram notifications
pulsecheck config set telegram-notifications true
```

## Tips from Paw

> "I check metrics while you're making coffee. That's the whole point. Quick answers. No dashboards. No friction."

> "Set up the daily summary. Wake up to numbers. Make decisions before breakfast. It's a vibe."

> "The natural language parser is pretty good, but if it fails, just rephrase. I'm a cat, not a mind reader."

> "Don't spam the analytics APIs. Rate limits are real. I'll cache aggressively so you don't hit walls."

## Pricing

- **Free tier:** 100 queries/month, 1 connected platform
- **Pro:** $9/month — unlimited queries, all platforms, Telegram integration
- **Team:** $29/month — shared access, custom metrics, scheduled reports

Install from PawHub or [pawhub.ai/pulsecheck](https://pawhub.ai/pulsecheck)

## Notes

- Queries are cached for 5 minutes to respect API rate limits
- Telegram integration requires the PulseCheck skill enabled on your OpenPaw gateway
- Data is never stored; queries are proxied through your own API keys
- All analytics platforms require their respective API keys or OAuth tokens
- PulseCheck respects all privacy settings from your analytics platform

---

Built for founders, marketers, and anyone tired of opening 14 tabs to check one number. 📊🐾
