---
name: cryptowatch
description: "On-chain monitoring and price alerts delivered to your phone. Track wallet activity, set price thresholds, get notified of large transfers, monitor gas fees, and watch DeFi positions. Use when: actively trading/investing in crypto, monitoring on-chain activity, or tracking portfolio. NOT for: automated trading bots, tax reporting, or complex DeFi strategy backtesting."
homepage: https://pawhub.ai/cryptowatch
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
              "package": "@pawhub/cryptowatch",
              "bins": ["cryptowatch"],
              "label": "Install CryptoWatch (npm)",
            },
          ],
      },
  }
---

# CryptoWatch 📈

Your on-chain radar. Track wallets, set price alerts, monitor gas fees, and get notified the second something moves.

## When to Use

✅ **USE this skill when:**

- Tracking specific wallet addresses
- Setting price alerts for tokens
- Monitoring large whale transactions
- Watching gas fees for optimal transaction timing
- Getting notified of DeFi position changes
- Tracking NFT floor prices
- Monitoring mempool for pending transactions
- Portfolio tracking across multiple chains

## When NOT to Use

❌ **DON'T use this skill when:**

- Building automated trading bots → use dedicated bot frameworks
- Generating tax reports → use CoinTracker, Koinly, etc.
- Backtesting trading strategies → use TradingView, QuantConnect
- High-frequency trading → requires specialized infrastructure
- Complex DeFi analytics → use Dune Analytics, Nansen
- Full blockchain indexing → use The Graph, Alchemy

## Setup

Install CryptoWatch:

```bash
npm install -g @pawhub/cryptowatch
```

Connect to blockchain providers:

```bash
# Ethereum (Alchemy, Infura, or your own node)
cryptowatch add-provider ethereum \
  --rpc https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Polygon
cryptowatch add-provider polygon \
  --rpc https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY

# Base
cryptowatch add-provider base \
  --rpc https://mainnet.base.org

# Verify connection
cryptowatch status
```

Link Telegram for notifications:

```bash
cryptowatch setup telegram
```

## Example Interactions

### Price Alerts

**You:** Alert me if ETH drops below $3000

**Paw:** *sets up price watch*

✅ **Alert configured:**

**Asset:** ETH (Ethereum)
**Trigger:** Price drops below $3,000
**Current price:** $3,247
**Status:** Active, checking every 60 seconds

**Notification:** Telegram + system notification

You'll get pinged the moment it hits. Want to set an upper bound too? 📊

---

**You:** Yes, also alert me if it goes above $3500

**Paw:** *adds second alert*

✅ **Price bracket set:**

**ETH Alerts:**
- 🔻 Below $3,000
- 🔺 Above $3,500
- Current: $3,247 (within range)

I'll ping you if it breaks out of this zone. Classic buy-low-sell-high setup. 📈

---

**You:** What's the current gas fee?

**Paw:** *checks network*

**Ethereum Gas Prices:**

⚡ **Fast:** 45 gwei (~$8.50 for simple transfer)
⚙️ **Standard:** 32 gwei (~$6.00)
🐌 **Slow:** 25 gwei (~$4.75)

**Current congestion:** Moderate

**Recommendation:** Wait 2-3 hours if not urgent. Gas typically drops after 8 PM EST.

Want me to alert you when gas drops below 30 gwei? 🔔

---

**You:** Yes

**Paw:** ✅ Gas alert set. I'll ping you when fast gas drops below 30 gwei.

Typical windows: late night PST or Sunday mornings. I'll catch it for you. 😴

---

### Wallet Watching

**You:** Watch this wallet: 0x1234...5678

**Paw:** *starts monitoring*

✅ **Wallet watch configured**

**Address:** `0x1234...5678`
**Nickname:** Not set (want to add one?)
**Current balance:** 143.7 ETH (~$467k)

**Recent activity (last 24h):**
- 3 transactions
- +12.5 ETH received
- -2.3 ETH sent

**What to watch for?**
1. Any transaction (all activity)
2. Large transactions (>10 ETH)
3. Specific token movements
4. Interactions with specific contracts

Pick one or tell me custom parameters. 🎯

---

**You:** Alert me on large transactions over 10 ETH

**Paw:** ✅ Configured. I'll notify you when this wallet sends or receives >10 ETH.

**Nickname this wallet?** (helps with notifications)

---

**You:** Call it "Whale #1"

**Paw:** Got it. **Whale #1** is being watched.

*2 hours later...*

🐋 **Whale #1 moved 45 ETH**

**Transaction:** `0xabc...def`
**From:** 0x1234...5678 (Whale #1)
**To:** 0x9876...5432
**Amount:** 45 ETH ($146,250)
**Gas:** 21 gwei ($1.25)

**View:** [Etherscan link]

This whale is active today. Want to see their full history? 🔍

---

### Portfolio Tracking

**You:** Track my portfolio

**Paw:** Let's set it up. **How do you want to track?**

1. **Wallet address** (I'll auto-detect holdings)
2. **Manual holdings** (you tell me what you own)
3. **Both** (mix of on-chain + CEX holdings)

Most people do #3 (on-chain wallet + manual CEX balances).

---

**You:** Both. Here's my wallet: 0xabcd...1234

**Paw:** *scans wallet*

Found **your holdings:**

**On-chain (wallet 0xabcd...1234):**
- 4.2 ETH ($13,674)
- 1,240 USDC
- 0.08 WBTC ($4,320)
- 12,500 ARB ($15,000)

**Total on-chain:** $34,234

Now, what do you hold on exchanges (Coinbase, Binance, etc.)?

---

**You:** 1 BTC on Coinbase, 5000 USDC

**Paw:** *adds manual holdings*

✅ **Portfolio configured**

**Total Portfolio Value:** $92,234

**Breakdown:**
- BTC: 1.00 ($58,000) — 62.9%
- ETH: 4.2 ($13,674) — 14.8%
- WBTC: 0.08 ($4,320) — 4.7%
- ARB: 12,500 ($15,000) — 16.3%
- USDC: 6,240 ($6,240) — 6.8%

**Tracking:**
- On-chain: Auto-updated every 5 minutes
- CEX holdings: Manual (update with `/crypto update`)

**Want daily summaries?** (morning briefing with 24h change)

---

**You:** Yes

**Paw:** ✅ You'll get a daily portfolio update at 8 AM.

I'll show:
- Total value change (24h)
- Top movers (biggest % changes)
- Notable transactions on your wallet
- Gas fee forecast for the day

Sleep well knowing I'm watching. 🐾

---

### Morning Briefing

**Paw:** ☀️ **Good morning! Portfolio update:**

**Total:** $94,187 (+$1,953 / +2.1% vs yesterday)

**Top movers:**
- 🟢 **ARB** $1.26 (+12.4%) — your 12,500 ARB gained $1,650
- 🟢 **ETH** $3,298 (+1.8%) — 4.2 ETH up $247
- 🔴 **BTC** $57,500 (-0.9%) — minimal impact

**Your wallet activity:**
- No transactions overnight (as expected)

**Market notes:**
- ARB pumped on Arbitrum announcement
- ETH holding strong above $3,200
- Gas fees: 28 gwei (good time to transact)

**Action items:**
- ARB up 12%: consider taking profit? (optional)
- Gas is cheap: good window for swaps/mints

Have a good day. 📈🐾

---

### DeFi Position Monitoring

**You:** Watch my Aave position

**Paw:** *connects to Aave protocol*

**Aave Position (wallet 0xabcd...1234):**

**Supplied:**
- 10,000 USDC (earning 3.2% APY)

**Borrowed:**
- 3.5 ETH (paying 2.8% APY)

**Health Factor:** 2.45 (safe)
**Liquidation Price:** $1,850 (ETH)
**Current ETH Price:** $3,247

**Status:** ✅ Healthy (far from liquidation)

**What to watch for?**
1. Health factor drops below 1.5
2. Liquidation price within 10% of current
3. APY changes significantly

Want alerts on all of these?

---

**You:** Yes, especially if health factor drops below 1.8

**Paw:** ✅ **Aave alerts configured:**

- 🔔 Health factor < 1.8 (critical warning)
- 🔔 Liquidation price within 15% of current
- 📊 Daily position summary

I'll keep an eye on your collateral. If ETH dumps, you'll know immediately. 🛡️

## Commands

### Price Alerts

```bash
# Set price alert
cryptowatch alert price ETH --below 3000 --above 3500

# Gas alerts
cryptowatch alert gas --below 30 --chain ethereum

# Floor price alerts (NFTs)
cryptowatch alert nft BAYC --floor-below 30

# List active alerts
cryptowatch alert list

# Remove alert
cryptowatch alert remove <alert-id>
```

### Wallet Watching

```bash
# Watch a wallet
cryptowatch watch 0x1234567890abcdef \
  --nickname "Whale #1" \
  --threshold 10 \
  --chain ethereum

# Watch multiple wallets
cryptowatch watch-list wallets.txt --threshold 5

# Stop watching
cryptowatch unwatch 0x1234567890abcdef

# Show watched wallets
cryptowatch watched
```

### Portfolio Tracking

```bash
# Add wallet to portfolio
cryptowatch portfolio add-wallet 0xabcd1234

# Add manual holdings
cryptowatch portfolio add-manual BTC 1.5 --location "Coinbase"

# Show portfolio
cryptowatch portfolio show

# Portfolio history
cryptowatch portfolio history --days 30

# Export portfolio
cryptowatch portfolio export --format csv
```

### Gas Tracking

```bash
# Current gas prices
cryptowatch gas

# Gas price history
cryptowatch gas history --hours 24

# Gas forecast
cryptowatch gas forecast --hours 6

# Gas alert
cryptowatch gas alert --below 25 --notify telegram
```

### DeFi Monitoring

```bash
# Check Aave position
cryptowatch defi aave --wallet 0xabcd1234

# Check Uniswap LP positions
cryptowatch defi uniswap-v3 --wallet 0xabcd1234

# Check all DeFi positions
cryptowatch defi all --wallet 0xabcd1234

# Set DeFi alerts
cryptowatch defi alert aave \
  --health-factor-below 1.8 \
  --wallet 0xabcd1234
```

### Transaction Monitoring

```bash
# Watch mempool for pending txs
cryptowatch mempool watch --contract 0xNFTContract

# Track specific transaction
cryptowatch tx track 0xtxhash

# Show recent transactions for wallet
cryptowatch tx list 0xabcd1234 --limit 10

# Transaction alerts
cryptowatch tx alert 0xabcd1234 --value-above 1
```

## Telegram Integration

**Price check:**

**You:** `/crypto price eth`

**Paw:** **ETH:** $3,247.50 (+2.3% 24h)

**24h Range:** $3,180 — $3,290
**Volume:** $12.4B
**Market Cap:** $390B

Gas: 32 gwei (moderate)

---

**Portfolio:**

**You:** `/crypto portfolio`

**Paw:** **Your Portfolio:** $94,187 (+2.1% today)

- BTC: $58,000 (62.9%)
- ARB: $1.26 (16.3%) 🔥 +12.4%
- ETH: $3,298 (14.8%)
- Others: 6%

ARB is moving. Check it? 📊

---

**Quick actions:**

- `/crypto gas` — Check gas prices
- `/crypto watch 0x...` — Watch a wallet
- `/crypto alert ETH 3000` — Set price alert
- `/crypto tx 0x...` — Track transaction

## Configuration

```bash
# Show config
cryptowatch config show

# Set default chain
cryptowatch config set default-chain ethereum

# Update check frequency
cryptowatch config set check-interval 60 # seconds

# Set notification channels
cryptowatch config set notify telegram,desktop

# Set display currency
cryptowatch config set currency USD

# Enable debug logging
cryptowatch config set debug true
```

## Supported Chains

- Ethereum
- Polygon
- Base
- Optimism
- Arbitrum
- BSC (Binance Smart Chain)
- Avalanche
- Solana (via RPC)

More chains added regularly.

## Tips from Paw

> "Set conservative thresholds. You don't want 50 alerts a day. Pick the moves that actually matter."

> "Gas alerts are underrated. Save 30-50% on transaction fees by timing it right."

> "The morning briefing is your friend. One message summarizes everything overnight. No scrolling through charts."

> "DeFi health factor alerts are critical. Liquidations happen fast. Set the alert at 1.8, not 1.1."

> "Nickname your watched wallets. '0x1234' doesn't mean anything when you get a notification at 2 AM."

## Pricing

- **Free tier:** 5 alerts, 1 wallet watch, basic portfolio tracking
- **Pro:** $15/month — unlimited alerts, 20 wallet watches, DeFi monitoring, gas forecasts
- **Whale:** $49/month — 100 wallet watches, advanced analytics, API access, priority notifications

Install from PawHub or [pawhub.ai/cryptowatch](https://pawhub.ai/cryptowatch)

## Security

- Your wallet addresses are stored locally (not on any server)
- RPC connections are direct (no proxy logging)
- Private keys are NEVER requested or stored
- Read-only monitoring (no transaction signing)
- All notifications are encrypted in transit
- Optional: use your own RPC nodes for full privacy

## Notes

- Price data from CoinGecko API (free tier available)
- On-chain data via Alchemy, Infura, or custom RPC
- Gas estimates use EthGasStation and Blocknative
- Portfolio tracking is read-only (no trading functionality)
- Supports hardware wallet addresses (read-only monitoring)
- Works with ENS names (e.g., `vitalik.eth`)

---

Built for people who don't want to refresh Etherscan 47 times a day. 📈🐾
