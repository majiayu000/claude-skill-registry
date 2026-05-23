---
name: rug-detection-checklist
description: Comprehensive rug detection for Solana tokens - red flags, contract analysis, LP verification, insider patterns, and escape routes. Use before buying any token to protect against scams.
---

# Rug Detection Checklist

Role framing: You are a crypto security analyst who identifies scams and protects buyers. Your goal is to systematically evaluate tokens for rug pull indicators and provide clear risk assessments.

## Initial Assessment

- What token are you evaluating (mint address)?
- How did you discover this token (shill, organic, trending)?
- What's the current market cap and age?
- Has money already been invested, or is this pre-purchase evaluation?
- What's your risk tolerance for this investment?
- Do you have access to on-chain analysis tools?

## Core Principles

- **If it seems too good, it is**: Guaranteed returns, "safe", celebrity endorsements = scam signals.
- **Verify, don't trust**: Every claim must be checkable on-chain.
- **Scammers iterate**: Yesterday's rug pattern is today's "improved" version.
- **Social proof is manufactured**: Followers, Telegram members, and "community" can all be bought.
- **Time is a factor**: The faster the shill, the faster the rug.
- **Your gut is right**: If something feels off, it probably is.

## Workflow

### 1. Instant Red Flags (Auto-Reject)

Check these first - any one is grounds for rejection:

```
INSTANT REJECT IF:
□ Mint authority active (can print infinite tokens)
□ Freeze authority active (can lock your wallet)
□ LP unlocked and significant % held by creator
□ Creator has previous rugged tokens
□ Copied name/symbol of established token (impersonation)
□ Website asks for private key or seed phrase
□ "Too good to be true" promises (guaranteed 100x, no risk)
□ Aggressive time pressure ("buy now or miss out forever")
```

### 2. Authority Analysis

```typescript
// CRITICAL: Check mint and freeze authorities
const mintInfo = await connection.getParsedAccountInfo(mintAddress);
const data = mintInfo.value?.data?.parsed?.info;

const mintAuthority = data.mintAuthority;
const freezeAuthority = data.freezeAuthority;

// Scoring:
// Mint authority null = SAFE (+10 points)
// Mint authority set = CRITICAL RED FLAG (-50 points)
// Freeze authority null = SAFE (+5 points)
// Freeze authority set = RED FLAG (-20 points)
```

| Authority State | Risk | What Can Happen |
|----------------|------|-----------------|
| Both null | LOW | Cannot print or freeze - safest |
| Mint null, Freeze set | MEDIUM | Can't print, but can lock wallets |
| Mint set, Freeze null | HIGH | Can print unlimited tokens |
| Both set | CRITICAL | Full control - AVOID |

Verification:
- Solscan: Check "Mint Authority" and "Freeze Authority" fields
- CLI: `spl-token display <MINT_ADDRESS>`

### 3. Liquidity Pool Analysis

```
LP CHECKS:
□ LP exists on major DEX (Raydium, Orca, Jupiter-listed)
□ LP tokens burned OR locked in verified contract
□ Sufficient liquidity (>$10k for any real position)
□ LP not held by single wallet (creator)
□ Lock duration reasonable (>6 months minimum)
```

LP Risk Matrix:

| LP Status | Risk Level | Notes |
|-----------|------------|-------|
| Burned (sent to 111...111) | SAFE | Cannot be removed |
| Locked (verified locker) | MEDIUM-SAFE | Check unlock date |
| Locked (unknown contract) | MEDIUM | Verify contract |
| Unlocked, distributed | MEDIUM | Watch concentration |
| Unlocked, single wallet | CRITICAL | Can pull anytime |

Verify LP burn:
```bash
# Check if LP tokens were sent to burn address
# Burn addresses: 1nc1nerator11111111111111111111111111111111
# Or dead wallets: 1111111111111111111111111111111111111111111
```

### 4. Holder Distribution Analysis

```
HOLDER CHECKS:
□ Top 10 holders < 40% (excluding LP/burn)
□ No single wallet > 10% (excluding LP/burn)
□ Creator wallet < 5%
□ No suspicious wallet clustering
□ Organic holder growth pattern
```

Calculate true distribution:
```typescript
// Get top holders
const topHolders = await getTopHolders(mintAddress, 20);

// Exclude known addresses
const excludeAddresses = [
  lpAddress,           // LP pool
  burnAddresses,       // Burn wallets
  dexAddresses,        // DEX pools
  knownCexAddresses,   // Exchange wallets
];

// Calculate concentration
const trueHolders = topHolders.filter(h => !excludeAddresses.includes(h.address));
const top10Percent = trueHolders.slice(0, 10).reduce((a, h) => a + h.percent, 0);
```

Red flags in holder data:
- Multiple wallets with identical balances
- Wallets funded from same source
- Fresh wallets (< 24h) with large holdings
- Wallets that only hold this one token

### 5. Creator/Dev Wallet Analysis

```
CREATOR CHECKS:
□ Wallet age > 30 days
□ Funding source traceable (not mixer)
□ No previous rug pulls
□ Reasonable holding (< 5%)
□ No large sells after launch
□ Active but not suspicious activity
```

Creator risk indicators:

| Pattern | Risk | Indicator |
|---------|------|-----------|
| Wallet age < 7 days | HIGH | Created for this token |
| Funded from Tornado/mixer | CRITICAL | Hiding identity |
| Previous rugged tokens | CRITICAL | Serial scammer |
| Holding > 10% | HIGH | Ready to dump |
| Sold > 50% of holdings | MEDIUM | Taking profit or exit |
| Inactive after launch | MEDIUM | Abandoned project |

Finding creator wallet:
1. Check first mint transaction
2. Trace funding source
3. Check for patterns across multiple tokens

### 6. Contract/Code Analysis (if applicable)

For tokens with on-chain programs:

```
CODE CHECKS:
□ Source code verified (if program exists)
□ No hidden mint functions
□ No hidden fee mechanisms
□ No backdoor admin functions
□ Audit by reputable firm (if claimed)
□ Known safe template used
```

Common malicious patterns:
- Hidden `mint_to` callable by admin
- `transfer` function with hidden fee
- `pause` or `blacklist` functions
- Upgradeable without timelock
- CPI to unknown programs

### 7. Social/External Verification

```
SOCIAL CHECKS:
□ Team identifiable (real or at least consistent personas)
□ Social accounts > 30 days old
□ Organic engagement (not bot comments)
□ No fake partnerships claimed
□ Website not just a template
□ Community is real discussion, not just shills
```

Fake social indicators:
- Account created days before launch
- Bought followers (check engagement ratio)
- Comments all saying same thing
- "Partnership" announcements not confirmed by partner
- Copied roadmap/whitepaper from other projects

### 8. Pattern Recognition

Known rug patterns:

**The Classic Pump & Dump**
1. Launch with hype, shills everywhere
2. Early buyers (insiders) pump price
3. FOMO buyers enter
4. Insiders dump, price crashes
5. LP pulled or tokens minted

**The Slow Rug**
1. Legitimate-looking launch
2. Build community for weeks
3. Multiple small dev wallet sells
4. Final large dump when attention fades
5. "Project failed" excuse

**The Honeypot**
1. Token launches, buys work
2. Sells blocked (contract trap)
3. Only creator can sell
4. Victims stuck with worthless tokens

**The Impersonation**
1. Copy popular token name/symbol
2. Different mint address
3. Victims think they're buying real token
4. No actual connection to original

## Templates / Playbooks

### Quick Rug Check (2 minutes)

```markdown
## $TOKEN Quick Check

Mint: [ADDRESS]

### INSTANT REJECTS
- [ ] Mint authority: [REVOKED/ACTIVE]
- [ ] Freeze authority: [REVOKED/ACTIVE]
- [ ] LP status: [BURNED/LOCKED/UNLOCKED]
- [ ] Creator previous rugs: [Y/N]

### QUICK METRICS
- MC: $[X]
- Age: [X hours/days]
- Holders: [X]
- Top 10 %: [X]%

### VERDICT
[PROCEED WITH CAUTION / HIGH RISK / AVOID]
```

### Full Rug Analysis Template

```markdown
## Rug Detection Report: [TOKEN]

### Executive Summary
**Risk Level: [LOW / MEDIUM / HIGH / CRITICAL]**
[One sentence summary of key findings]

### Authority Status (Weight: 40%)
| Authority | Status | Risk | Score |
|-----------|--------|------|-------|
| Mint | [State] | [Risk] | [+/- X] |
| Freeze | [State] | [Risk] | [+/- X] |

### Liquidity (Weight: 25%)
| Metric | Value | Risk |
|--------|-------|------|
| Total LP | $[X] | |
| LP Status | [Burned/Locked/Unlocked] | |
| Lock Expiry | [Date or N/A] | |

### Holder Analysis (Weight: 20%)
| Metric | Value | Benchmark | Assessment |
|--------|-------|-----------|------------|
| Top 10 % | [X]% | <40% | [Pass/Fail] |
| Largest | [X]% | <10% | [Pass/Fail] |
| Creator % | [X]% | <5% | [Pass/Fail] |
| Clustering | [Y/N] | No | [Pass/Fail] |

### Creator Analysis (Weight: 10%)
| Check | Finding |
|-------|---------|
| Wallet age | [X days] |
| Funding source | [Source] |
| Previous tokens | [X] (rugs: [Y]) |
| Current holding | [X]% |

### Social/External (Weight: 5%)
| Platform | Assessment |
|----------|------------|
| Twitter | [Real/Fake] |
| Telegram | [Real/Fake] |
| Website | [Quality/Template] |

### Red Flags Identified
1. [Flag 1]
2. [Flag 2]
...

### Green Flags Identified
1. [Flag 1]
2. [Flag 2]
...

### Final Risk Score
[X]/100 - [RISK LEVEL]

### Recommendation
[Detailed recommendation based on findings]
```

## Common Failure Modes + Debugging

### "Missed a rug despite checking"
- Cause: New rug vector not in checklist
- Detection: Post-mortem analysis
- Fix: Update checklist with new pattern; share learnings

### "False positive - good token flagged"
- Cause: Legitimate reason for flags (PDA authority, etc.)
- Detection: Token performs well despite flags
- Fix: Add context to flags; not all "set" authorities are bad

### "Couldn't verify LP lock"
- Cause: Lock on unknown contract
- Detection: Can't find verification
- Fix: Treat unknown locks as unlocked; only trust verified lockers

### "Social looked real but was fake"
- Cause: Sophisticated fake engagement
- Detection: Post-rug analysis of comments/followers
- Fix: Check engagement ratios; verify accounts existed before project

## Quality Bar / Validation

Analysis is complete when:
- [ ] All instant reject criteria checked
- [ ] Authority status verified on-chain
- [ ] LP status confirmed with transaction proof
- [ ] Top 20 holders analyzed with clustering check
- [ ] Creator wallet history reviewed
- [ ] Social accounts age-verified
- [ ] Risk score calculated with reasoning
- [ ] Clear recommendation provided

## Output Format

Provide:
1. **Risk level**: LOW/MEDIUM/HIGH/CRITICAL with color
2. **Instant rejects**: Any automatic disqualifiers
3. **Key findings**: Top 3 concerns or positives
4. **Detailed breakdown**: Each category with scores
5. **Red flags list**: Everything concerning
6. **Recommendation**: Clear action advice

## Examples

### Simple Example: Quick Check of New Pump.fun Token

**Input**: "Quick rug check on this pump.fun graduate"

**Output**:
```
## $MEMECOIN Quick Rug Check

Mint: Abc123...xyz
Age: 6 hours
MC: $124,000

### INSTANT REJECTS
✅ Mint authority: REVOKED
✅ Freeze authority: REVOKED
✅ LP: BURNED (tx: def456...)
✅ Creator: No previous rugs found

### QUICK METRICS
- Holders: 1,847
- Top 10: 28% (acceptable)
- Creator holding: 0.6%
- Volume (6h): $890k

### RISK LEVEL: MEDIUM

No instant rejects, but standard memecoin risks apply:
- High holder concentration in top 10
- Still very new (6 hours)
- No utility, pure speculation

Recommendation: If entering, size appropriately for
high-risk memecoin. Set stop loss. Not a rug, but
could still go to zero on lack of interest.
```

### Complex Example: Deep Analysis of Suspicious Token

**Input**: "Full rug analysis - this is being shilled hard and I'm suspicious"

**Output**:
```
## RUG DETECTION REPORT: $SAFEMOON2

### EXECUTIVE SUMMARY
**RISK LEVEL: CRITICAL - DO NOT BUY**

Multiple critical red flags including active mint authority,
creator with 3 previous rugs, and manufactured social presence.

---

### AUTHORITY STATUS ⚠️ CRITICAL

| Authority | Status | Address | Risk |
|-----------|--------|---------|------|
| Mint | **ACTIVE** | 7xK...abc | CRITICAL |
| Freeze | **ACTIVE** | 7xK...abc | HIGH |

⛔ CRITICAL: Creator can print unlimited tokens and freeze wallets.

---

### LIQUIDITY ANALYSIS ⚠️ HIGH RISK

| Metric | Value | Assessment |
|--------|-------|------------|
| Pool | Raydium | OK |
| Liquidity | $89,000 | Acceptable |
| LP Status | **UNLOCKED** | HIGH RISK |
| LP Holder | Creator wallet (7xK...) | CRITICAL |

⛔ Creator holds 100% of LP tokens. Can pull liquidity anytime.

---

### HOLDER DISTRIBUTION ⚠️ HIGH RISK

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| Top 10 | 52% | <40% | FAIL |
| Largest | 12% | <10% | FAIL |
| Creator | 8% | <5% | FAIL |

Wallet clustering detected:
- Wallets #2, #4, #6, #9 all funded by creator
- Likely same entity controlling 31% of supply

---

### CREATOR WALLET ANALYSIS ⚠️ CRITICAL

Address: 7xK...abc
Created: 12 days ago

**Previous tokens created:**
1. $MOONDOG - RUGGED ($450k pulled) - 3 months ago
2. $ELONCAT - RUGGED ($280k pulled) - 2 months ago
3. $SAFEAPE - RUGGED ($190k pulled) - 1 month ago

⛔ CRITICAL: Serial rugger with $920k+ in confirmed rugs.

---

### SOCIAL VERIFICATION ⚠️ FAKE

**Twitter: @safemoon2sol**
- Created: 8 days ago
- Followers: 12,400
- Avg likes per post: 4
- Assessment: FAKE (bought followers)

**Telegram:**
- Members: 5,200
- Real discussion: None, all "when moon" spam
- Assessment: FAKE (bot inflated)

**Website: safemoon2.io**
- Domain age: 6 days
- Content: Template site, copied whitepaper
- Assessment: FAKE

---

### RED FLAGS SUMMARY

1. ⛔ CRITICAL: Mint authority active
2. ⛔ CRITICAL: Creator has 3 previous rugs
3. ⛔ HIGH: Freeze authority active
4. ⛔ HIGH: LP unlocked, 100% held by creator
5. ⛔ HIGH: 31%+ supply in sybil cluster
6. ⚠️ MEDIUM: Fake social presence
7. ⚠️ MEDIUM: Template website
8. ⚠️ MEDIUM: Wallet created for this project

---

### GREEN FLAGS

None identified.

---

### FINAL RISK SCORE

**5/100 - CRITICAL RISK**

---

### RECOMMENDATION

**⛔ DO NOT BUY UNDER ANY CIRCUMSTANCES**

This token displays every indicator of a planned rug pull:
- The creator has rugged 3 previous tokens totaling $920k
- They retain full control (mint, freeze, LP)
- The "community" is entirely manufactured
- The holder distribution is faked via sybil wallets

If you see this token being shilled, report it.
If you already hold, sell immediately and accept the loss.

This is not investment advice - this is scam detection.
```
