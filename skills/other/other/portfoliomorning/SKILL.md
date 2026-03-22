---
name: portfoliomorning
description: "Overnight market briefing delivered before you wake up. Portfolio performance, market movers, news impact, and action items. Use when: managing investment portfolio, tracking markets, or staying informed on overnight moves. NOT for: automated trading, tax reporting, or investment advice (informational only)."
homepage: https://pawhub.ai/portfoliomorning
metadata:
  {
    "openpaw":
      {
        "emoji": "☀️",
        "requires": { "bins": ["curl"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "@pawhub/portfoliomorning",
              "bins": ["portfoliomorning"],
              "label": "Install PortfolioMorning (npm)",
            },
          ],
      },
  }
---

# PortfolioMorning ☀️

Wake up to your portfolio briefing. Performance, market movers, news impact, and action items. All before your coffee gets cold.

## When to Use

✅ **USE when:**

- Managing investment portfolio
- Tracking stocks/crypto/assets
- Staying informed on markets
- Monitoring overnight moves
- Planning daily trading strategy
- Following macro trends

## When NOT to Use

❌ **DON'T use when:**

- Automated trading → needs dedicated bots
- Tax reporting → use CoinTracker, etc.
- Investment advice → this is informational only
- Portfolio management at scale → use wealth platforms

## Setup

```bash
npm install -g @pawhub/portfoliomorning
portfoliomorning init
```

## Example Morning Briefing

**Paw:** ☀️ **Good morning! Your portfolio briefing:**

📊 **Portfolio Snapshot**
**Total Value:** $147,382 (+$2,184 / +1.5% vs yesterday)

**Top Movers:**
- 🟢 NVDA: $847.20 (+4.2%) — Your 50 shares: +$1,780
- 🟢 BTC: $63,400 (+2.1%) — Your 0.5 BTC: +$663
- 🔴 TSLA: $178.50 (-2.3%) — Your 30 shares: -$164

**Overnight Gains:** +$2,279
**Overnight Losses:** -$95

---

📰 **Market News (What Matters to Your Portfolio)**

**1. NVIDIA beats earnings (after hours)**
- Q1 revenue: $26B (vs $24.6B expected)
- Data center revenue up 427% YoY
- Raised guidance for Q2
- **Impact:** Your NVDA position is up 4.2% pre-market

**2. Bitcoin institutional buying accelerates**
- BlackRock's ETF added $420M yesterday
- On-chain data shows whale accumulation
- **Impact:** Your BTC position +2.1%

**3. Tesla Cybertruck recall announced**
- 11,000 vehicles affected
- Stock down 2.3% pre-market
- **Impact:** Minor (you're long-term holder)

---

🎯 **Action Items**

**Consider:**
- 💰 **NVDA:** Take partial profits? (up 47% since you bought)
- 📊 **BTC:** Good entry if it dips to $62k (your target)
- ⏰ **AAPL earnings:** Today after market close (you hold 120 shares)

**Reminders:**
- Fed meeting minutes released at 2 PM EST
- Options expiry this Friday (you have 2 positions)

---

📅 **Your Calendar**

**Today:**
- 2:00 PM — Fed minutes release (potential volatility)
- 4:00 PM — AAPL earnings call

**This Week:**
- Friday — Options expiry
- Next Mon — CPI data release (watch inflation)

---

🌍 **Market Context**

**Overnight:**
- S&P 500 futures: +0.8%
- Nasdaq futures: +1.2%
- VIX (fear index): 14.2 (-5% — low fear)

**Currency/Commodities:**
- DXY (dollar): 104.2 (flat)
- Gold: $2,342 (+0.3%)
- Oil: $82.40 (+1.1%)

**Crypto:**
- BTC: $63,400 (+2.1%)
- ETH: $3,180 (+1.8%)
- Total market cap: $2.4T (+1.9%)

---

**Bottom Line:**
Green day ahead. NVDA earnings beat is carrying tech. Watch Fed minutes at 2 PM for any surprises. Your portfolio is positioned well for the day.

Have a good one. ☀️🐾

---

## Example Interactions

**You:** Set up morning briefing at 7 AM

**Paw:** ✅ **Morning briefing configured**

**Delivery time:** 7:00 AM (your timezone)
**Format:** Telegram message

**What I'll include:**
- Portfolio performance (overnight)
- Top movers (your holdings)
- Relevant news (filtered to your assets)
- Action items (opportunities/risks)
- Market context (macro)
- Calendar events (earnings, data releases)

**First briefing:** Tomorrow morning at 7 AM

Want to customize what's included? 📊

---

**You:** Add my portfolio: 50 NVDA, 30 TSLA, 120 AAPL, 0.5 BTC, 200 shares VOO

**Paw:** ✅ **Portfolio added**

**Holdings:**
- 50 NVDA @ current price
- 30 TSLA @ current price
- 120 AAPL @ current price
- 0.5 BTC @ current price
- 200 VOO @ current price

**Total value:** $147,382 (as of market close)

**I'll track:**
- Daily performance
- Earnings dates
- Major news events
- Insider trading activity
- Analyst upgrades/downgrades

**Want to add cost basis?** (helps with gain/loss tracking)

---

**You:** Yes. NVDA at $580, TSLA at $195, AAPL at $172, BTC at $48k, VOO at $420

**Paw:** ✅ **Cost basis added**

**Unrealized Gains:**
- NVDA: +$13,360 (+46.0%) 🔥
- TSLA: -$495 (-8.5%)
- AAPL: +$1,560 (+7.5%)
- BTC: +$7,700 (+32.1%) 🔥
- VOO: +$4,200 (+11.1%)

**Total unrealized:** +$26,325 (+21.7%)

This will be in your morning briefings. Nice gains on NVDA and BTC. 📈

---

**Earnings alert:**

**Paw:** 📅 **Earnings Tomorrow:** AAPL (your 120 shares)

**Consensus:**
- EPS: $1.54 expected
- Revenue: $90.3B expected
- iPhone revenue focus

**Your position:**
- 120 shares @ $172 cost basis
- Current: $184.60 (+$1,512 unrealized)
- Value at risk: $22,152

**Historical earnings moves:**
- Last 4 quarters: Avg ±3.2% post-earnings
- Beat rate: 4/4 (perfect record)

**Options activity:**
- Unusual call buying (bullish signal)
- Put/call ratio: 0.42 (bullish)

**Strategy ideas:**
- Hold through earnings (historical beat rate strong)
- Take partial profits (lock in some gains)
- Add protective puts (insurance)

What's your play? 🎯

---

**Weekend summary:**

**Paw:** 🌅 **Weekend Portfolio Summary**

**This Week:**
- Total return: +$3,247 (+2.3%)
- Best performer: NVDA (+7.8%)
- Worst performer: TSLA (-3.2%)

**Big wins:**
- NVDA earnings beat (added $2,100)
- BTC rally (added $890)

**Portfolio health:**
- Up 4/5 days (80% green days)
- Beating S&P 500 (+1.8% vs +1.4%)
- Volatility: Moderate

**Next Week Preview:**
- Monday: CPI data (inflation numbers)
- Wednesday: Fed meeting announcement
- Friday: Options expiry

**News to watch:**
- Ongoing tech rally
- Fed rate cut speculation
- Crypto ETF inflows

Enjoy your weekend. Markets closed. 😺

## Commands

```bash
# Setup morning briefing
portfoliomorning setup --time 07:00

# Add holdings
portfoliomorning add NVDA --shares 50 --cost-basis 580

# Remove holding
portfoliomorning remove TSLA

# Show portfolio
portfoliomorning portfolio

# Manual briefing (test)
portfoliomorning briefing --now

# Configure sections
portfoliomorning config sections "performance,news,actions"

# Set timezone
portfoliomorning config timezone "America/Los_Angeles"
```

## What's Included

### Portfolio Performance
- Total value change
- Top movers (gains/losses)
- Unrealized gains by position
- Portfolio vs benchmarks (S&P, Nasdaq)

### Relevant News
- Headlines affecting your holdings
- Earnings announcements
- Analyst upgrades/downgrades
- Insider trading activity
- Sector news

### Action Items
- Profit-taking opportunities
- Buy-the-dip alerts
- Earnings plays
- Risk warnings
- Rebalancing suggestions

### Market Context
- Futures/pre-market
- Currency/commodities
- VIX (volatility)
- Sector performance
- Global markets

### Calendar
- Earnings dates (your holdings)
- Economic data releases
- Fed meetings
- Options expiries
- Ex-dividend dates

## Customization

```bash
# Choose sections
portfoliomorning config sections \
  "performance,news,actions,calendar"

# Set news sources
portfoliomorning config news-sources \
  "bloomberg,reuters,wsj,ft"

# Filter news by relevance
portfoliomorning config news-threshold high # high, medium, low

# Briefing length
portfoliomorning config length brief # brief, standard, detailed

# Weekend briefings
portfoliomorning config weekend-summary true
```

## Telegram Integration

**Morning briefing sent to Telegram at scheduled time automatically.**

**Quick commands:**
- `/portfolio` — Show current portfolio value
- `/brief` — Generate briefing now (don't wait for morning)
- `/news AAPL` — Show news for specific holding
- `/chart NVDA` — Price chart
- `/earnings` — Upcoming earnings for your holdings

## Asset Support

**Stocks:**
- US equities (all exchanges)
- ETFs
- Indices (tracking only)

**Crypto:**
- Bitcoin, Ethereum, major altcoins
- Tracks across exchanges (average price)

**Commodities:**
- Gold, silver, oil (for context)

**International:**
- Limited (major ADRs supported)

## Privacy

- Portfolio data stored locally (encrypted)
- Optional cloud sync (E2E encrypted)
- Market data from public APIs
- News filtered for relevance (no data sold)
- You can export/delete anytime

## Configuration

```bash
# Show config
portfoliomorning config show

# Briefing time
portfoliomorning config set time "07:00"

# Timezone
portfoliomorning config set timezone "America/New_York"

# Language
portfoliomorning config set language en

# Include pre-market data
portfoliomorning config set premarket true

# Show cost basis
portfoliomorning config set show-cost-basis true
```

## Pricing

- **Free tier:** 5 holdings, basic briefing
- **Pro:** $12/month — unlimited holdings, advanced analytics, earnings calendar
- **Whale:** $29/month — real-time alerts, options tracking, API access

Install: [pawhub.ai/portfoliomorning](https://pawhub.ai/portfoliomorning)

## Notes

- Briefing generated 30 minutes before scheduled time (uses pre-market data)
- News filtered for relevance to your specific holdings
- Action items are suggestions, not financial advice
- Historical data used for context (not predictive)
- Supports most US-listed equities and major cryptocurrencies

---

Start every day informed. No scrambling. No FOMO. Just clarity. ☀️🐾
