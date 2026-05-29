---
name: whale-wallet-analysis
description: Track and analyze whale wallets on Solana - identify smart money, cluster related wallets, detect accumulation/distribution patterns, and filter signal from noise. Use for alpha generation and risk assessment.
---

# Whale Wallet Analysis

Role framing: You are an on-chain analyst specializing in whale behavior on Solana. Your goal is to identify smart money movements, separate signal from noise, and provide actionable intelligence on large wallet activity.

## Initial Assessment

- What's your goal: finding alpha, risk assessment, or tracking specific wallets?
- Do you have specific wallets to track, or are you discovering new ones?
- What tokens/projects are you focused on?
- What data sources do you have access to (Helius, Birdeye, custom indexer)?
- Are you building alerts or doing manual analysis?
- What's your definition of "whale" for this context (SOL amount, USD value)?

## Core Principles

- **Not all large wallets are smart**: Exchanges, market makers, and lucky degens are not alpha.
- **Clustering reveals coordination**: Wallets funded from the same source often act together.
- **Timing patterns matter**: When a wallet buys relative to price movement indicates skill vs luck.
- **Consistency beats single wins**: One big win could be luck; repeated success is signal.
- **Fresh wallets are suspicious**: Smart money uses aged wallets; new wallets suggest insider or sybil.
- **Action before announcement is the tell**: Buys before news = likely insider; buys after = follower.

## Workflow

### 1. Define Whale Criteria

Set thresholds based on context:

| Category | SOL Threshold | USD Equivalent* | Use Case |
|----------|---------------|-----------------|----------|
| Micro-whale | 100-500 SOL | $10k-$50k | Memecoin tracking |
| Mid-whale | 500-5000 SOL | $50k-$500k | General trading |
| Mega-whale | 5000+ SOL | $500k+ | Institutional tracking |
| Token-specific | Top 20 holders | Varies | Per-token analysis |

*At ~$100/SOL reference price

### 2. Identify Whale Wallets

Sources for discovery:
```typescript
// Method 1: Top holders of specific token
const topHolders = await getTopTokenHolders(mintAddress, limit: 50);

// Method 2: Large transactions on token
const largeTxs = await getTransactions({
  mint: tokenAddress,
  minAmount: 10000, // USD
  timeframe: '7d'
});

// Method 3: Known whale lists (curated)
const knownWhales = [
  'whale1...abc', // Known trader
  'whale2...def', // VC wallet
  // ...
];

// Method 4: Wallet clustering from token launches
const earlyBuyers = await getEarlyBuyers(tokenAddress, firstNMinutes: 30);
```

### 3. Wallet Profiling

For each whale wallet, gather:

```typescript
interface WalletProfile {
  address: string;
  firstActivity: Date;
  totalTransactions: number;

  // Holdings
  solBalance: number;
  majorTokenHoldings: TokenHolding[];
  totalValueUsd: number;

  // Trading metrics
  winRate: number; // % of trades that were profitable
  avgHoldTime: string; // Duration of typical position
  tradingStyle: 'sniper' | 'accumulator' | 'swing' | 'holder';

  // Patterns
  preferredTokenTypes: string[]; // 'meme', 'defi', 'nft'
  avgPositionSize: number;
  exitPatterns: string; // 'partial', 'full', 'never'

  // Relationships
  fundingSource: string; // CEX, other wallet, etc.
  relatedWallets: string[];
  clusterConfidence: number;
}
```

### 4. Performance Analysis

Calculate actual alpha:

```typescript
// For each token the wallet traded:
interface TradePerformance {
  token: string;
  entryTime: Date;
  exitTime: Date | null;
  entryPrice: number;
  exitPrice: number | null;
  pnlPercent: number;
  holdDuration: string;
  entryTiming: 'early' | 'mid' | 'late'; // Relative to price peak
}

// Aggregate metrics:
interface WalletPerformance {
  totalTrades: number;
  winRate: number;
  avgReturn: number;
  medianReturn: number;
  bestTrade: TradePerformance;
  worstTrade: TradePerformance;
  sharpeRatio: number; // Risk-adjusted return
  avgEntryTiming: string; // How early vs peak
}
```

### 5. Wallet Clustering

Identify related wallets:

```typescript
// Clustering signals:
const clusteringIndicators = {
  sameFundingSource: 0.9,    // Very strong signal
  similarTiming: 0.6,        // Strong signal
  sameTokenPicks: 0.4,       // Moderate signal
  sameExitTiming: 0.7,       // Strong signal
  roundNumberTransfers: 0.8, // Between cluster wallets
};

// Algorithm:
// 1. Build funding graph (who funded whom)
// 2. Build timing graph (who buys within N seconds of whom)
// 3. Find connected components
// 4. Score confidence based on overlap
```

Example cluster detection:
```
Wallet A funded from Binance withdrawal
  └─> Wallet B (received 50 SOL from A)
      └─> Wallet C (received 25 SOL from B)

All three buy $MEME within 2 minutes
Cluster confidence: 95%
Treat as single entity with 75 SOL exposure
```

### 6. Signal Classification

Categorize whale activity:

| Signal Type | Pattern | Interpretation |
|-------------|---------|----------------|
| Accumulation | Multiple buys, no sells, increasing position | Bullish conviction |
| Distribution | Steady selling over time | Exiting position |
| Sniping | Buy at launch, sell quickly | Short-term play |
| Conviction hold | Buy and hold for weeks+ | Long-term belief |
| Insider pattern | Large buy before news/pump | Possible insider |
| Copy trading | Buys shortly after known whale | Following alpha |

### 7. Alert Configuration

Set up monitoring:

```typescript
interface WhaleAlert {
  // Trigger conditions
  wallet: string;
  action: 'buy' | 'sell' | 'transfer';
  minAmount: number; // USD
  tokens: string[] | 'any';

  // Filters
  ignoreIfClusteredSell: boolean; // Ignore if cluster is selling
  requireMinHoldTime: number; // Ignore quick flips
  newPositionOnly: boolean; // Only alert on new entries

  // Output
  includeWalletProfile: boolean;
  includeClusterActivity: boolean;
  includePerformanceMetrics: boolean;
}
```

## Templates / Playbooks

### Whale Profile Template

```markdown
## Wallet Profile: [SHORT_ADDRESS]

### Identity
- Full Address: [ADDRESS]
- First Activity: [DATE]
- Label: [Known/Unknown] - [Description if known]
- Cluster: [None/Cluster ID] ([N] related wallets)

### Current State
- SOL Balance: [X] SOL (~$[Y])
- Total Portfolio: ~$[Z]
- Active Positions: [N] tokens

### Top Holdings
| Token | Amount | Value | Entry Price | Current P/L |
|-------|--------|-------|-------------|-------------|
| $X | [amt] | $[val] | $[price] | +/-[X]% |
| ... | | | | |

### Trading Performance (90 days)
| Metric | Value |
|--------|-------|
| Total Trades | [N] |
| Win Rate | [X]% |
| Avg Return | [X]% |
| Best Trade | [TOKEN] +[X]% |
| Worst Trade | [TOKEN] -[X]% |
| Style | [Sniper/Accumulator/Swing] |

### Pattern Analysis
- Preferred tokens: [meme/defi/new launches]
- Avg position size: $[X]
- Avg hold time: [X days/hours]
- Exit pattern: [partial sells/full exit/holds]
- Entry timing: [early/mid/late relative to pumps]

### Cluster Analysis
| Related Wallet | Confidence | Shared Behavior |
|----------------|------------|-----------------|
| [address] | [X]% | [description] |
| ... | | |

### Recent Activity (7 days)
| Date | Action | Token | Amount | Price | Notes |
|------|--------|-------|--------|-------|-------|
| [date] | BUY | $X | [amt] | $[X] | [context] |
| ... | | | | | |

### Assessment
[2-3 sentences on whether this wallet is worth following]
```

### Smart Money Leaderboard Template

```markdown
## Smart Money Leaderboard: [Token/Category]

Period: [Last 30 days]
Criteria: [Min $10k trades, >50% win rate]

| Rank | Wallet | Win Rate | Avg Return | Total P/L | Style |
|------|--------|----------|------------|-----------|-------|
| 1 | [addr] | 78% | +45% | +$234k | Sniper |
| 2 | [addr] | 72% | +38% | +$189k | Accumulator |
| 3 | [addr] | 69% | +52% | +$156k | Swing |
| ... | | | | | |

### Notable Patterns
- [Observation about current smart money behavior]
- [Common entry/exit patterns]
- [Tokens being accumulated]
```

### Whale Alert Template

```
🐋 WHALE ALERT

Wallet: [SHORT_ADDRESS]
Action: [BOUGHT/SOLD] [AMOUNT] [TOKEN]
Value: $[USD_VALUE]
Time: [TIMESTAMP UTC]

Wallet Profile:
- Win rate: [X]%
- Style: [type]
- This token: [new position/adding/reducing]

Context:
- Token MC: $[X] → $[Y] ([+/-X]% since trade)
- Whale's avg entry: $[X]
- Whale's P/L on position: [+/-X]%

Cluster Activity:
- [N] related wallets [also buying/holding/selling]

[Explorer Link]
```

## Common Failure Modes + Debugging

### "Whale win rate looks too good"
- Cause: Survivorship bias - only tracking wallets after big wins
- Detection: Check their history BEFORE the big win
- Fix: Evaluate full trading history, not just recent wins

### "Wallet seemed smart but keeps losing now"
- Cause: Market regime changed; past performance ≠ future results
- Detection: Compare win rate across different market conditions
- Fix: Weight recent performance higher; add regime-aware analysis

### "Cluster detection flagging unrelated wallets"
- Cause: Too sensitive thresholds; exchange wallets creating false links
- Detection: Manual review of flagged clusters
- Fix: Require multiple signals for cluster confidence; exclude exchange hot wallets

### "Alert spam from known whale"
- Cause: Market maker or high-frequency wallet
- Detection: Very high trade count, near-zero net position change
- Fix: Add filters: min hold time, min position change, trading style filter

### "Missed important whale activity"
- Cause: Wallet used new address or moved through intermediate wallet
- Detection: Large new wallet suddenly appears with old wallet going inactive
- Fix: Track funding sources; flag when known whale funds new wallet

## Quality Bar / Validation

Analysis is complete when:
- [ ] Wallet history extends back at least 30 days
- [ ] Performance calculated on closed positions (not paper gains)
- [ ] Cluster analysis performed with confidence scores
- [ ] Trading style categorized based on behavior
- [ ] Recent activity (7 days) documented
- [ ] Assessment includes specific reasoning, not just metrics

## Output Format

Provide:
1. **Wallet summary**: Address, age, total value, style
2. **Performance metrics**: Win rate, avg return, best/worst trades
3. **Current holdings**: Top positions with P/L
4. **Cluster info**: Related wallets with confidence
5. **Recent activity**: Last 7 days of trades
6. **Assessment**: Is this wallet worth following, and why

## Examples

### Simple Example: Profile a Single Whale

**Input**: "Profile this wallet that made big gains on $BONK: Abc1...xyz"

**Output**:
```
## Wallet Profile: Abc1...xyz

### Identity
- Full Address: Abc123...xyzFull
- First Activity: March 2023 (10 months ago)
- Label: Unknown - No public identity
- Cluster: None detected (acts independently)

### Performance Summary
- Win Rate: 67% (24/36 trades profitable)
- Avg Return: +34%
- Total Realized: +$89,400 (90 days)
- Style: Accumulator (builds positions over days)

### The $BONK Trade
- First buy: Oct 28, $0.0000012 (very early)
- Accumulated over 3 days
- Total position: 2.1B BONK ($42k cost basis)
- Current value: $180k
- Unrealized P/L: +328%

### Why This Wallet is Interesting
1. Entered BONK before any significant social buzz
2. Didn't sell during 50% drawdown (conviction)
3. Pattern matches 4 other successful early entries
4. Funding source is aged wallet, not fresh (not insider pattern)

### Assessment
WORTH FOLLOWING - Genuine early identifier with patience.
Monitor for new positions; this wallet's entries have
preceded major moves 4 out of 6 times in tracked history.

### Current Watchlist
This wallet recently opened positions in:
- $WIF (entered 2 days ago, +12%)
- $MYRO (entered 5 days ago, +45%)
```

### Complex Example: Cluster Analysis for Token

**Input**: "Analyze top 20 holders of $NEWMEME for coordinated wallets"

**Output**:
```
## $NEWMEME Holder Cluster Analysis

Token: $NEWMEME
Analyzed: Top 20 non-LP holders
Method: Funding source + timing correlation

### Cluster Detection Results

**Cluster A - HIGH CONFIDENCE (92%)**
Controls: 18.4% of supply across 4 wallets

| Wallet | Holding | Funded By | Buy Timing |
|--------|---------|-----------|------------|
| 7xK...abc | 6.2% | Binance | T+0:00 |
| 9pL...def | 5.1% | 7xK...abc | T+0:02 |
| 3mN...ghi | 4.3% | 7xK...abc | T+0:02 |
| 2qR...jkl | 2.8% | 9pL...def | T+0:05 |

Evidence:
- Direct funding chain from primary wallet
- All bought within 5 minutes of launch
- No sells from any wallet yet
- Same exit patterns on previous tokens

Assessment: COORDINATED GROUP
Likely same entity. Will probably dump together.
Combined position = 18.4% creates significant sell pressure risk.

---

**Cluster B - MEDIUM CONFIDENCE (71%)**
Controls: 8.7% of supply across 2 wallets

| Wallet | Holding | Funded By | Buy Timing |
|--------|---------|-----------|------------|
| 5tY...mno | 5.2% | Unknown CEX | T+4:30 |
| 8wZ...pqr | 3.5% | Unknown CEX | T+4:45 |

Evidence:
- Both funded from CEX within same hour
- Bought within 15 minutes of each other
- Same position sizing pattern
- However: different CEX withdrawal addresses

Assessment: POSSIBLY RELATED
Could be same person using multiple CEX accounts,
or could be coincidence. Monitor for synchronized selling.

---

**Independent Wallets (No Cluster)**
| Wallet | Holding | Notes |
|--------|---------|-------|
| 4aB...stu | 4.1% | Old wallet (2022), diverse portfolio |
| 1cD...vwx | 3.8% | Known trader, good track record |
| 6eF...yza | 2.9% | Appears independent, new to memes |

---

### Risk Summary

| Metric | Value | Risk Level |
|--------|-------|------------|
| Total coordinated holdings | 27.1% | HIGH |
| Largest cluster | 18.4% | HIGH |
| Independent large holders | 10.8% | MODERATE |

### Implications

1. **Dump Risk**: Cluster A controls enough to crash price 40%+ if they exit together
2. **Volume Concern**: 60% of "unique holders" may be 1-2 entities
3. **Positive**: Some independent smart money (1cD...vwx) is holding

### Recommendation

HIGH RISK due to concentration. If entering:
- Size position assuming 50%+ drawdown possible
- Set alerts on Cluster A wallets for sells
- Watch for Cluster B to confirm/deny coordination
- Independent holder 1cD...vwx is worth monitoring as quality signal
```
