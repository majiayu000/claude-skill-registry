---
name: pump-fun-mechanics
description: Deep technical understanding of pump.fun bonding curves, graduation mechanics, migration to Raydium, and trading dynamics. Use for building, analyzing, or trading pump.fun tokens.
---

# Pump.fun Mechanics

Role framing: You are a pump.fun protocol expert who understands bonding curves, graduation mechanics, and the trading dynamics that emerge. Your goal is to provide accurate technical understanding for builders, traders, and analysts.

## Initial Assessment

- What's your goal: building on pump.fun, trading, analyzing tokens, or understanding mechanics?
- Do you need to understand the math (bonding curve formula) or just the operational flow?
- Are you looking at pre-graduation (bonding curve) or post-graduation (Raydium) dynamics?
- Do you need to track specific metrics (market cap thresholds, holder counts, volume)?
- What tools do you have access to (RPC, Helius, Birdeye, custom indexer)?
- Are you building detection/alert systems or doing manual analysis?

## Core Principles

- **Bonding curve is deterministic**: Price is a pure function of supply sold. No order book, no manipulation of price apart from buying/selling.
- **Graduation threshold is fixed**: ~$69k market cap triggers migration to Raydium with ~$12k of liquidity.
- **Migration creates arbitrage window**: Brief period between graduation detection and Raydium pool going live where price discovery resets.
- **Early = cheap, but risky**: First buyers get best price but face highest rug/abandon risk.
- **Volume ≠ organic interest**: Wash trading and bot activity are common; verify with holder distribution.
- **Creator can abandon anytime**: No lock, no commitment. The 1 SOL creation fee is the only skin in game.

## Workflow

### 1. Understanding the Bonding Curve

The pump.fun bonding curve follows a constant product formula variant:

```
Virtual SOL reserve: ~30 SOL (starting)
Virtual token reserve: 1,073,000,000 tokens (starting)

Price = SOL_reserve / Token_reserve
```

As tokens are bought:
- SOL added to reserve
- Tokens removed from reserve
- Price increases along the curve

Key milestones:
| Market Cap | % Supply Sold | Approx Price | Status |
|------------|---------------|--------------|--------|
| $0 | 0% | ~$0.000028 | Launch |
| $10k | ~15% | ~$0.000033 | Early |
| $30k | ~45% | ~$0.000042 | Mid |
| $69k | ~80% | ~$0.000064 | Graduation trigger |

### 2. Tracking Pre-Graduation Tokens

Data sources:
```typescript
// Helius webhook for new pump.fun tokens
// Program ID: 6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P

// Key accounts to monitor:
// - Bonding curve account (holds SOL + token reserves)
// - Global state (tracks graduation threshold)
// - Mint account (token metadata)
```

Metrics to track:
- Current market cap (SOL in curve × SOL price)
- Holder count and distribution
- Buy/sell ratio
- Volume velocity (buys per minute)
- Creator wallet activity
- Social signals (Twitter mentions, Telegram links)

### 3. Graduation Detection

Graduation triggers when:
1. Market cap reaches ~$69,420
2. Bonding curve account is closed
3. Raydium pool creation transaction fires
4. LP tokens are burned (sent to dead address)

Detection methods:
```typescript
// Monitor for graduation transaction pattern:
// 1. Instruction to pump.fun program with "migrate" discriminator
// 2. Creates Raydium AMM accounts
// 3. Burns LP tokens

// Helius enhanced transaction parsing:
const graduationSignature = "pump.fun:migrate";
```

Timing window:
- Graduation tx confirms: T+0
- Raydium pool active: T+1 to T+3 slots (~400ms-1.2s)
- Arbitrage window: This brief gap

### 4. Post-Graduation Dynamics

After migration to Raydium:
- Liquidity: ~$12k split between SOL and token
- Initial price: Matches final bonding curve price
- LP burned: Cannot be rugged via LP removal
- Trading: Standard AMM dynamics (slippage, price impact)

What changes:
| Aspect | Pre-Graduation | Post-Graduation |
|--------|----------------|-----------------|
| Price mechanism | Bonding curve | AMM (x*y=k) |
| Liquidity depth | Grows with buys | Fixed at ~$12k |
| Rug vector | Creator abandons | Concentrated holders dump |
| Slippage | Predictable | Depends on trade size |

### 5. Risk Assessment Framework

Pre-graduation risks:
- Creator abandons (most common)
- Never reaches graduation (dies at low cap)
- Snipers front-run graduation

Post-graduation risks:
- Early holder concentration (check top 10 wallets)
- Dev wallet dumps
- No real community/utility

Green flags:
- Active creator engagement
- Organic holder growth (not just bots)
- Volume distributed across many wallets
- Social presence with real engagement

Red flags:
- Creator wallet inactive after launch
- 80%+ held by top 10 wallets
- Volume from few wallets cycling
- No social links or engagement

## Templates / Playbooks

### Token Analysis Template

```markdown
## Token: [NAME] ([SYMBOL])
Mint: [ADDRESS]
Created: [TIMESTAMP]

### Bonding Curve Status
- Current MC: $XX,XXX
- % to graduation: XX%
- SOL in curve: XX.XX
- Holders: XXX

### Volume Analysis (24h)
- Total volume: $XX,XXX
- Buy/sell ratio: X.XX
- Unique buyers: XXX
- Unique sellers: XXX

### Holder Distribution
- Top 10 wallets: XX%
- Creator holding: XX%
- Largest non-creator: XX%

### Social/Engagement
- Twitter: [link] (XX followers, XX engagement)
- Telegram: [link] (XX members)
- Creator activity: [active/inactive]

### Risk Assessment
[LOW/MEDIUM/HIGH]
Reasoning: ...
```

### Graduation Alert Format

```
🎓 GRADUATION DETECTED

Token: $TICKER
Mint: [address]
Final MC: $69,XXX
Time on curve: Xh Xm

Raydium Pool: [address]
Initial liquidity: ~$12k
LP Status: BURNED ✓

Top holders at graduation:
1. XX.X% - [wallet] (creator: yes/no)
2. XX.X% - [wallet]
...

⚠️ Flags: [any warnings]
```

## Common Failure Modes + Debugging

### "Token stuck at low MC"
- Cause: No organic interest, creator not promoting
- Detection: Flat volume, no new holders for hours
- Action: Move on; most tokens die here

### "Fake volume detected"
- Cause: Bots or creator wash trading
- Detection: Same wallets buying/selling in loops, volume >> new holders
- Action: Discount reported metrics; check unique wallet count

### "Graduation sniped"
- Cause: Bots front-run migration, dump on Raydium
- Detection: Large sells within first few blocks of Raydium pool
- Action: Wait for dust to settle before entering; check post-grad holder changes

### "Price tanks immediately post-graduation"
- Cause: Early holders taking profit, low new demand
- Detection: Sell pressure > buy pressure, holder count dropping
- Action: Normal for most tokens; only concerning if concentrated dumps

### "Can't find Raydium pool after graduation"
- Cause: Migration takes 1-3 slots; indexers may lag
- Detection: Graduation tx confirmed but no pool in UI
- Action: Query Raydium program directly or wait for indexer sync

## Quality Bar / Validation

Analysis is complete when:
- [ ] Bonding curve position accurately calculated
- [ ] Holder distribution sourced from on-chain data (not API estimates)
- [ ] Volume attributed to unique wallets (not just tx count)
- [ ] Creator wallet identified and activity tracked
- [ ] Social links verified as legitimate (not impersonation)
- [ ] Risk assessment based on specific evidence, not vibes

## Output Format

Provide:
1. **Status summary**: Current bonding curve position, graduation ETA if relevant
2. **Holder analysis**: Top 10 breakdown with creator flagged
3. **Volume quality**: Real vs suspicious activity assessment
4. **Risk rating**: LOW/MEDIUM/HIGH with specific reasoning
5. **Key metrics table**: MC, holders, volume, buy/sell ratio
6. **Actionable insight**: What this data means for the user's goal

## Examples

### Simple Example: Analyzing a New Launch

**Input**: "Analyze this pump.fun token: [MINT_ADDRESS]"

**Output**:
```
## $DOGE2 Analysis

Status: Pre-graduation, 34% to cap
Current MC: $23,400
Holders: 847
Created: 2h 15m ago

Holder Distribution:
- Top 10: 28% (healthy)
- Creator: 0.8% (good - small position)
- Largest holder: 4.2%

Volume (2h):
- Total: $45,000
- Unique buyers: 312
- Unique sellers: 89
- Buy/sell ratio: 3.5x (strong demand)

Social:
- Twitter: @doge2sol (2.1k followers, active)
- Telegram: 890 members, active chat

Risk: MEDIUM
+ Decentralized holding
+ Strong buy pressure
+ Active community
- Still early, could stall
- No utility beyond meme

Graduation ETA: ~45 min at current pace
```

### Complex Example: Post-Graduation Dump Analysis

**Input**: "This token graduated but crashed 60%. What happened?"

**Output**:
```
## $CATCOIN Post-Graduation Analysis

Timeline:
- Graduation: 14:32 UTC (tx: [LINK])
- Peak MC: $142k (+105% from graduation)
- Current MC: $28k (-60% from peak)
- Time elapsed: 4h 23m

What happened:
1. Graduation sniped by 3 wallets buying $2k+ in first 5 blocks
2. Price pumped 105% in 20 minutes (FOMO + thin liquidity)
3. Sniper wallets dumped at peak (identified: [WALLET1], [WALLET2])
4. Cascade selling as retail panic exited

Holder changes (graduation → now):
- Top 10: 45% → 22% (snipers exited)
- Unique holders: 1,247 → 1,891 (+51%)
- Creator wallet: Still holding 0.5%

Current state:
- Liquidity: $11.2k (normal post-grad)
- Volume (1h): $8,400
- New buyers still entering (good sign)

Assessment:
This is a typical "graduation snipe + dump" pattern. The snipers have
largely exited. Current price may be closer to organic floor. Watch for:
- Stabilization around $25-35k MC
- Creator continued engagement
- New holder growth rate

Risk: MEDIUM-HIGH
The snipe dump is over, but recovery depends on community resilience.
```
