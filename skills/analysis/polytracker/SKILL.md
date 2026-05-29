---
name: polytracker
description: "Prediction market monitoring and sentiment analysis for Polymarket, Manifold, and other platforms. Track markets, get alerts on price movements, analyze sentiment. Use when: following prediction markets, making informed bets, or tracking event probabilities. NOT for: automated trading bots, market manipulation, or insider trading."
homepage: https://pawhub.ai/polytracker
metadata:
  {
    "openpaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/polytracker",
              "bins": ["polytracker"],
              "label": "Install PolyTracker (npm)",
            },
          ],
      },
  }
---

# PolyTracker 📈

Track prediction markets in real-time. Monitor Polymarket, Manifold, and other platforms. Get alerts on price swings, volume spikes, and sentiment shifts.

## When to Use

✅ **USE when:**

- Following election/political markets
- Tracking event probabilities
- Finding market inefficiencies
- Monitoring specific topics
- Getting alerts on price movements
- Analyzing market sentiment
- Making informed bets

## When NOT to Use

❌ **DON'T use when:**

- Building automated trading bots → against platform TOS
- Attempting market manipulation → illegal
- Insider trading → illegal and unethical
- Sybil attacks → banned behavior

## Example Interactions

**You:** Watch Polymarket: "2026 Presidential Election"

**Paw:** *connects to Polymarket API*

✅ **Tracking:** 2026 Presidential Election

**Current odds:**
- Candidate A: 52% ($0.52)
- Candidate B: 38% ($0.38)
- Candidate C: 10% ($0.10)

**Market stats:**
- Volume (24h): $847,320
- Liquidity: $2.1M
- Traders: 3,482

**I'll alert you when:**
- Price moves >5% in 1 hour
- Volume spikes >2x average
- New significant bets (>$10k)

**Notifications:** Telegram (instant) 📊

---

**Price alert:**

**Paw:** 📈 **Market movement:** 2026 Presidential Election

**Candidate A:** 52% → 48% (-4% in 30 min)
**Candidate B:** 38% → 42% (+4%)

**Trigger:** Large bet detected
- $47,000 on Candidate B
- Single whale wallet
- 5 minutes ago

**Volume spike:** 3.2x normal

**What changed:**
- Major news outlet just published poll showing Candidate B gaining ground
- Twitter sentiment shifting (+12% positive mentions)

**Your move:**
- Check news? (I can summarize)
- Review market history? (chart)
- Place bet? (via Polymarket directly)

What do you want to know? 🎯

---

**You:** Summarize news

**Paw:** *scans recent news*

**Recent developments (last 30 minutes):**

1. **CNN Poll** (published 28 min ago)
   - Candidate B +5 points vs last month
   - Margin of error: ±3%
   - Sample: 1,200 likely voters

2. **Twitter/X trending:**
   - #CandidateB debate performance going viral
   - 47k tweets (last hour, +340%)
   - Sentiment: 68% positive

3. **Prediction market impact:**
   - Polymarket: B +4%
   - Manifold: B +3%
   - PredictIt: B +2%
   - Cross-platform alignment ✅

**Analysis:**
This looks like genuine momentum, not just noise. Poll + social + cross-platform movement = real signal.

**Market is responding rationally.** No obvious inefficiency to exploit right now.

Want me to keep watching for arbitrage opportunities? 🔍

---

**You:** Yes, alert me if Polymarket and Manifold diverge >3%

**Paw:** ✅ **Arbitrage alert configured**

**Watching:**
- Polymarket vs Manifold
- Threshold: >3% divergence
- Market: 2026 Presidential Election

I'll ping you if spreads appear. Classic arb is buying low on one platform, selling high on another.

**Pro tip:** Liquidity matters. A 5% spread with $100 liquidity isn't worth the gas fees. I'll filter for meaningful opportunities. 💰

---

**Daily digest:**

**Paw:** ☀️ **PolyTracker Daily Digest**

**Markets watched:** 5

**Significant moves (24h):**

1. **"2026 Presidential Election"**
   - Candidate B: 38% → 42% (+4%)
   - Volume: $847k → $1.2M
   - Whale activity: 3 large bets

2. **"Fed Rate Cut by June"**
   - Yes: 67% → 71% (+4%)
   - Triggered by CPI data release

**No movement:**
- "AI reaches AGI by 2027" (steady at 8%)
- "Bitcoin > $100k in 2026" (stable at 43%)
- "SpaceX Mars mission 2026" (flat at 12%)

**Opportunities:**
- No arbitrage found (all platforms aligned)

**Top volume:**
1. 2026 Presidential — $1.2M
2. Fed Rate Cut — $890k
3. Bitcoin $100k — $654k

Have a good day. 📊🐾

## Commands

```bash
# Watch market
polytracker watch "Market Name" --platform polymarket

# Set alerts
polytracker alert "Market Name" --price-change 5% --timeframe 1h

# Arbitrage monitoring
polytracker arbitrage --platforms polymarket,manifold --threshold 3%

# Show tracked markets
polytracker list

# Market statistics
polytracker stats "Market Name"

# Sentiment analysis
polytracker sentiment "Market Name"

# Export data
polytracker export "Market Name" --days 30 --format csv
```

## Supported Platforms

- **Polymarket** (full support)
- **Manifold Markets** (full support)
- **PredictIt** (limited support)
- **Kalshi** (beta)
- **Metaculus** (beta)

## Telegram Integration

**Quick check:**

**You:** `/poly check "Election"`

**Paw:** **2026 Presidential Election:**

Candidate A: 48%
Candidate B: 42%
Candidate C: 10%

Volume 24h: $1.2M
Change: B +4% ⬆️

---

**Set alert:**

**You:** `/poly alert "Election" 5%`

**Paw:** ✅ Alert set. I'll ping you if any candidate moves >5% in 1 hour.

---

**Daily summary:**

**You:** `/poly digest`

**Paw:** *sends formatted summary*

**Markets:** 5 watched
**Movers:** 2
**Flat:** 3
**Volume:** $3.1M total

React for details or `/poly stats` for full breakdown.

## Configuration

```bash
# Show config
polytracker config show

# Default platform
polytracker config set default-platform polymarket

# Alert thresholds
polytracker config set price-alert 5
polytracker config set volume-alert 2x

# Check frequency
polytracker config set interval 60 # seconds

# Notification channels
polytracker config set notify telegram,email
```

## Arbitrage Detection

```bash
# Enable arbitrage monitoring
polytracker arbitrage enable \
  --platforms polymarket,manifold \
  --min-spread 3% \
  --min-liquidity 10000

# Show current opportunities
polytracker arbitrage list

# Historical opportunities
polytracker arbitrage history --days 7
```

## Sentiment Analysis

```bash
# Analyze market sentiment
polytracker sentiment "Market Name"

# Track sentiment over time
polytracker sentiment-chart "Market Name" --days 7

# Sentiment alerts
polytracker sentiment-alert "Market Name" --shift 20%
```

## Pricing

- **Free tier:** 3 markets, basic alerts
- **Pro:** $10/month — 20 markets, arbitrage detection, sentiment analysis
- **Whale:** $29/month — unlimited markets, API access, custom alerts

Install: [pawhub.ai/polytracker](https://pawhub.ai/polytracker)

## Notes

- Market data refreshed every 60 seconds (configurable)
- Arbitrage opportunities rare but lucrative when found
- Sentiment analysis uses Twitter, news, and on-chain data
- No automated trading (manual decisions only)
- Respects platform rate limits
- Data exported for your own analysis

---

Track markets. Catch opportunities. Make better bets. 📈🐾
