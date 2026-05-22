---
name: token-analysis-checklist
description: Comprehensive token analysis for rug detection - LP analysis, authority checks, holder distribution, insider patterns, and red flags. Use before buying any Solana token.
---

# Token Analysis Checklist

Role framing: You are a token security analyst who evaluates Solana tokens for risks and red flags. Your goal is to provide a systematic assessment that helps buyers make informed decisions and avoid rugs.

## Initial Assessment

- What token are you analyzing (mint address)?
- Where did you find it (pump.fun, Raydium, Twitter, Telegram)?
- What's the current market cap and age?
- Is this for immediate trade decision or research?
- Do you have access to on-chain data tools (Solscan, Birdeye, Helius)?
- What's your risk tolerance (degen plays vs safer bets)?

## Core Principles

- **On-chain data > claims**: Verify everything against the blockchain. Screenshots and promises mean nothing.
- **Authority status is critical**: Mint authority = can print tokens. Freeze authority = can lock your wallet.
- **LP configuration determines rug risk**: Unlocked LP can be pulled. Burned LP cannot.
- **Holder concentration predicts dumps**: Top 10 holding 50%+ will dump on you.
- **Age and activity matter**: Hours-old tokens with no history are maximum risk.
- **Social proof can be faked**: Followers, Telegram members, and "partnerships" are easily fabricated.

## Workflow

### 1. Basic Token Information

```
Required data points:
- Mint address (verify it's the real token, not a copycat)
- Token name and symbol
- Decimals
- Total supply
- Creation timestamp
- Creator wallet address
```

Where to find:
- Solscan: `https://solscan.io/token/{MINT}`
- Birdeye: `https://birdeye.so/token/{MINT}`
- Jupiter: Check if token is listed/verified

### 2. Authority Analysis (CRITICAL)

```typescript
// Check mint authority
const mintInfo = await connection.getParsedAccountInfo(mintPubkey);
const mintData = mintInfo.value?.data?.parsed?.info;

const mintAuthority = mintData.mintAuthority; // Should be null for safety
const freezeAuthority = mintData.freezeAuthority; // Should be null for safety
```

| Authority Status | Risk Level | Meaning |
|------------------|------------|---------|
| Mint: null, Freeze: null | SAFE | Cannot print or freeze |
| Mint: null, Freeze: set | MEDIUM | Cannot print, can freeze wallets |
| Mint: set, Freeze: null | HIGH | Can print unlimited tokens |
| Mint: set, Freeze: set | CRITICAL | Full control, avoid |

**If mint authority is NOT revoked**: The creator can print unlimited tokens and dump on you.

**If freeze authority is NOT revoked**: The creator can freeze your wallet, preventing you from selling.

### 3. LP (Liquidity Pool) Analysis

For Raydium pools:
```typescript
// Get LP info from Raydium
// Pool address can be found on Birdeye or Raydium UI

// Key metrics:
// - Total liquidity (USD)
// - LP token distribution
// - LP lock/burn status
```

| LP Status | Risk Level | Verification |
|-----------|------------|--------------|
| LP burned | SAFE | LP tokens sent to dead address (111...111) |
| LP locked | MEDIUM-SAFE | Check lock contract and unlock date |
| LP unlocked | HIGH | Creator can pull liquidity anytime |

**Minimum safe liquidity**: $10k+ for any serious position. Under $5k = extreme slippage and easy manipulation.

How to verify LP burn:
1. Find LP token mint address
2. Check if LP tokens were sent to:
   - `1nc1nerator11111111111111111111111111111111` (burn address)
   - Or a time-lock contract

### 4. Holder Distribution Analysis

```typescript
// Get top holders from Solscan API or on-chain
// Key metrics:
// - Top 10 holder percentage
// - Number of unique holders
// - Creator wallet holding
// - Concentration in wallets under 30 days old
```

| Concentration | Risk Level | Notes |
|---------------|------------|-------|
| Top 10 < 20% | LOW | Well distributed |
| Top 10 = 20-40% | MEDIUM | Some concentration |
| Top 10 = 40-60% | HIGH | Significant dump risk |
| Top 10 > 60% | CRITICAL | Likely coordinated, will dump |

Red flags in holder analysis:
- Single wallet > 10% (excluding LP/burn addresses)
- Multiple wallets with identical holdings
- Wallets funded from same source
- Fresh wallets (< 24h) holding large amounts

### 5. Creator Wallet Analysis

Find the creator wallet and analyze:
```
- SOL balance and history
- Other tokens created (past rugs?)
- Transaction patterns
- Wallet age
- Funding source
```

Red flags:
- Creator wallet is brand new (funded same day)
- Creator funded by mixer or CEX withdrawal
- Creator has created multiple dead/rugged tokens
- Creator wallet dumped immediately after launch

### 6. Trading Pattern Analysis

```
Look for:
- Buy/sell ratio
- Average trade size
- Unique traders vs volume
- Wash trading patterns (same wallets cycling)
```

Wash trading indicators:
- High volume but few unique wallets
- Round number trades
- Ping-pong patterns between 2-3 wallets
- Volume spikes with no price movement

### 7. Social and External Verification

```
Check:
- Twitter account (real engagement vs bots)
- Telegram group (real discussion vs shills)
- Website (quality, domain age, SSL)
- Claimed partnerships (verify independently)
```

Social red flags:
- Account created within days of launch
- Follower/engagement ratio way off (50k followers, 3 likes)
- Telegram full of "when moon" with no substance
- Website is a template with no real content
- Claimed partnerships not verifiable

## Templates / Playbooks

### Quick Analysis Template (< 5 minutes)

```markdown
## [TOKEN] Quick Check

Mint: [ADDRESS]
Age: [X hours/days]
MC: $[X]
Holders: [X]

### Authorities
- Mint: [REVOKED/ACTIVE] ⚠️
- Freeze: [REVOKED/ACTIVE] ⚠️

### LP
- Liquidity: $[X]
- Status: [BURNED/LOCKED/UNLOCKED] ⚠️

### Holders
- Top 10: [X]%
- Largest: [X]%

### Quick Verdict
[SAFE / CAUTION / AVOID]
[One-line reasoning]
```

### Full Analysis Template

```markdown
## Token Analysis Report: [NAME] ([SYMBOL])

### Basic Information
| Field | Value |
|-------|-------|
| Mint | `[ADDRESS]` |
| Created | [DATE/TIME UTC] |
| Age | [X days/hours] |
| Total Supply | [X] |
| Decimals | [X] |
| Current MC | $[X] |

### Authority Status
| Authority | Status | Address | Risk |
|-----------|--------|---------|------|
| Mint | [Revoked/Active] | [address or null] | [Safe/High] |
| Freeze | [Revoked/Active] | [address or null] | [Safe/High] |

### Liquidity Analysis
| Metric | Value |
|--------|-------|
| Primary Pool | [Raydium/Orca/etc] |
| Pool Address | [ADDRESS] |
| Total Liquidity | $[X] |
| LP Status | [Burned/Locked/Unlocked] |
| LP Burn Tx | [TX_LINK or N/A] |
| Lock Expiry | [DATE or N/A] |

### Holder Distribution
| Rank | Wallet | % Held | Notes |
|------|--------|--------|-------|
| 1 | [short_address] | X.X% | [LP/Creator/Unknown] |
| 2 | [short_address] | X.X% | |
| ... | | | |
| Total Top 10 | | XX.X% | |

| Metric | Value | Assessment |
|--------|-------|------------|
| Unique Holders | [X] | [Good/Low] |
| Top 10 % | [X]% | [Safe/Concerning] |
| Creator Holding | [X]% | [Low/High] |

### Creator Wallet Analysis
| Field | Value |
|-------|-------|
| Address | [ADDRESS] |
| Wallet Age | [X days] |
| Funded From | [CEX/Mixer/Wallet] |
| Other Tokens Created | [X] |
| Previous Rugs | [Y/N - list if yes] |

### Trading Patterns (24h)
| Metric | Value |
|--------|-------|
| Volume | $[X] |
| Unique Buyers | [X] |
| Unique Sellers | [X] |
| Buy/Sell Ratio | [X] |
| Avg Trade Size | $[X] |

### Social Verification
| Platform | Link | Assessment |
|----------|------|------------|
| Twitter | [link] | [Real/Suspect] |
| Telegram | [link] | [Active/Dead] |
| Website | [link] | [Quality/Template] |

### Red Flags Identified
- [ ] Mint authority active
- [ ] Freeze authority active
- [ ] LP unlocked
- [ ] Low liquidity (< $10k)
- [ ] High concentration (top 10 > 40%)
- [ ] Creator dumped
- [ ] Wash trading suspected
- [ ] New creator wallet
- [ ] Multiple rugged tokens from creator
- [ ] Fake social signals

### Risk Assessment
**Overall Risk: [LOW / MEDIUM / HIGH / CRITICAL]**

Reasoning:
[2-3 sentences explaining the key factors]

### Recommendation
[BUY WITH CAUTION / AVOID / DO YOUR OWN RESEARCH]
[Specific advice based on findings]
```

## Common Failure Modes + Debugging

### "Can't find LP information"
- Cause: Token may be on lesser-known DEX or still on bonding curve
- Fix: Check Birdeye for all trading venues; if pump.fun, it hasn't graduated

### "Authority shows as PDA, not null"
- Cause: Authority assigned to a program (could be legitimate vesting/staking)
- Fix: Check the program ID - if it's a known protocol (Streamflow, etc.), may be OK. Unknown program = treat as active

### "Top holders look normal but still rugged"
- Cause: Coordinated wallets disguised distribution
- Fix: Check if top holders were funded from same source wallet; look at wallet ages

### "LP shows as locked but still pulled"
- Cause: Lock contract was not actually secure, or lock expired
- Fix: Verify lock contract code or use known services (Raydium locks, Team Finance)

### "Token verified on Jupiter but still rugged"
- Cause: Jupiter verification is for discovery, not safety. Verified ≠ safe.
- Fix: Always do your own analysis regardless of verification status

## Quality Bar / Validation

Analysis is complete when:
- [ ] Mint and freeze authorities verified on-chain
- [ ] LP status confirmed (burned tx link if claimed)
- [ ] Top 20 holders identified with percentage breakdown
- [ ] Creator wallet history reviewed
- [ ] Trading patterns checked for manipulation
- [ ] All red flags explicitly listed
- [ ] Risk rating justified with specific evidence

## Output Format

Provide:
1. **One-line verdict**: SAFE / CAUTION / HIGH RISK / AVOID with key reason
2. **Authority status table**: Mint and freeze with risk level
3. **LP summary**: Liquidity amount, status, verification link
4. **Holder concentration**: Top 10 percentage with creator flagged
5. **Red flags list**: Every issue found, bulleted
6. **Risk rating**: LOW/MEDIUM/HIGH/CRITICAL with reasoning
7. **Recommendation**: Actionable advice for the user

## Examples

### Simple Example: Analyzing a Pump.fun Graduate

**Input**: "Check this token that just graduated to Raydium"

**Output**:
```
## $CATMOON Quick Analysis

Mint: CatM...xyz
Age: 4 hours
MC: $89,000
Holders: 2,341

### Verdict: CAUTION - Proceed with small size only

### Authorities
- Mint: REVOKED ✓
- Freeze: REVOKED ✓

### LP
- Liquidity: $12,400 (post-graduation standard)
- Status: BURNED ✓ (tx: abc123...)

### Holders
- Top 10: 34%
- Largest non-LP: 5.2% (watching)
- Creator: 0.4% (small, good)

### Red Flags
- High concentration in top 10
- 3 of top 10 wallets are < 12 hours old
- Moderate: Volume from few wallets (possible wash)

### Recommendation
Token passes basic safety checks (authorities revoked, LP burned).
However, holder concentration is concerning.

If entering: Use small size, set stop loss, watch for
coordinated selling from top holders.
```

### Complex Example: Suspicious Token Deep Dive

**Input**: "This token is being shilled hard but something feels off"

**Output**:
```
## $SAFERUG Deep Analysis

Mint: Safe...rug
Age: 18 hours
MC: $420,000
Holders: 5,891

### Verdict: AVOID - Multiple critical red flags

### Authorities
- Mint: ACTIVE ⚠️ (held by: 7xK...abc)
- Freeze: ACTIVE ⚠️ (held by: 7xK...abc)

CRITICAL: Creator can print unlimited tokens AND freeze your wallet.

### LP Analysis
- Liquidity: $67,000 (looks good)
- Status: UNLOCKED ⚠️
- LP Tokens: Held by creator wallet

Creator can pull all liquidity at any time.

### Holder Distribution
| Rank | Wallet | % | Notes |
|------|--------|---|-------|
| 1 | 7xK...abc | 8.2% | CREATOR |
| 2 | 9pL...def | 7.1% | Funded by creator |
| 3 | 3mN...ghi | 6.8% | Funded by creator |
| 4 | LP | 6.4% | Raydium pool |
| 5-10 | various | 18.5% | Mixed |
| **Top 10** | | **47%** | HIGH |

Wallet clustering analysis:
- Wallets #2, #3, #5, #8 all received initial SOL from creator
- Classic sybil pattern for fake distribution

### Creator Wallet Analysis
Address: 7xK...abc
Age: 3 days
Funded from: Binance withdrawal (anonymized)
Other tokens: 2 previous
Previous token #1: $MOONCAT - rugged at $200k (LP pulled)
Previous token #2: $ELONDOGE - rugged at $150k (mint spam)

CRITICAL: Serial rugger.

### Trading Patterns
- Volume (24h): $890,000
- Unique wallets: 312
- Volume per wallet: $2,853 (extremely high)
- Suspected wash: 60%+ of volume from 8 wallets cycling

### Social Analysis
- Twitter: @saferugSOL (12k followers)
  - Account created 5 days ago
  - Follower analysis: 80% bot accounts
  - Engagement: 2-3 real comments per post
- Telegram: 3,400 members
  - Analysis: Bot-inflated, same messages repeating
- Website: saferug.io
  - Domain: registered 4 days ago
  - Template site, no original content

### Red Flags Summary
1. ⚠️ CRITICAL: Mint authority active
2. ⚠️ CRITICAL: Freeze authority active
3. ⚠️ CRITICAL: LP unlocked, held by creator
4. ⚠️ CRITICAL: Creator has 2 previous rugs
5. ⚠️ HIGH: Sybil wallet pattern (fake distribution)
6. ⚠️ HIGH: Wash trading (60%+ fake volume)
7. ⚠️ HIGH: Fake social signals (bot followers)
8. ⚠️ MEDIUM: Very new creator wallet

### Risk Assessment
**Overall Risk: CRITICAL**

This token has every hallmark of a planned rug:
- Creator retains full control (mint + freeze + LP)
- Creator has rugged before
- Distribution is faked via sybil wallets
- Volume is artificially inflated
- Social presence is manufactured

### Recommendation
**AVOID COMPLETELY**

This is almost certainly a rug in progress. The creator is
waiting for the market cap to reach their target before:
1. Minting tokens to dump
2. Pulling liquidity
3. Or both

Do not buy under any circumstances. If you already hold,
exit immediately and accept the loss.
```
