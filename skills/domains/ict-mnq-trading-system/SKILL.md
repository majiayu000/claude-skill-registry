---
name: ict-mnq-trading
description: ICT-based MNQ futures trading analysis system for MFFU prop firm evaluation. Use when user provides market data (PDH, PDL, FVG levels, liquidity sweeps) and asks for trade analysis, entry/exit points, or bias confirmation. Also handles advanced concepts: breaker blocks, rejection blocks, SMT divergence, Power of 3, Judas Swing, OTE, NWOG, NDOG. Triggers on keywords like "trade setup", "NQ analysis", "entry", "SL", "TP", "bias", "liquidity sweep", "FVG", "order block", "ICT", "MMXM", "MMBM", "MMSM", "market maker model", "smart money reversal", "SMR", "breaker", "rejection block", "SMT", "Power of 3", "Judas swing", "OTE", "opening gap", "NWOG", "NDOG".
---

# ICT MNQ Trading System for MFFU Evaluation

## Account Parameters (FIXED)

| Parameter | Value |
|-----------|-------|
| Account Size | $50,000 |
| Daily Loss Limit | $2,500 |
| Contracts | 5 MNQ |
| Point Value | $2/point per contract ($10 total) |
| Max SL per trade | 25 points ($250) |
| Target per trade | 30-50 points ($300-$500) |
| Max trades per day | 3-4 (to preserve daily limit) |
| Profit target for eval | $3,000 |

## Risk Rules (NEVER VIOLATE)

1. **Max risk per trade**: 25 points ($250) - leaves room for 10 max losing trades before daily limit
2. **If down $1,500 in a day**: STOP TRADING - reassess next session
3. **No revenge trading**: Wait minimum 30 minutes after a loss
4. **No trading during high-impact news**: Within 15 min before/after

## Analysis Workflow

When user provides setup data, follow this exact sequence:

### Step 0: Enhanced Context Check

**Check for Market Context (NEW):**
Read `market-context-analysis.md` for:
1. SMT Divergence between NQ and ES
2. Power of 3 phase identification
3. Judas Swing detection

**Check for MMXM Structure:**
Read `mmxm-models.md` for Market Maker Model framework.

**Check for Advanced Entry Zones (NEW):**
Read `advanced-entry-refinement.md` for:
1. OTE confluence opportunities
2. NWOG/NDOG gap alignment
Read `breaker-rejection-blocks.md` for:
1. Failed OB (Breaker) setups
2. Wick rejection opportunities

### Step 1: Determine HTF Bias
Read `references/bias-determination.md` for detailed rules.

Quick check:
- Daily/4H structure: Higher highs/lows = BULLISH, Lower highs/lows = BEARISH
- Previous day candle: Bullish close above 50% = BULLISH bias
- Week structure: Where is price relative to PWH/PWL?

### Step 2: Identify Session Context
Read `references/session-times.md` for kill zone windows.

- **London**: 02:00-05:00 ET (manipulation phase)
- **NY AM Kill Zone**: 09:30-11:00 ET (PRIMARY - highest probability)
- **NY Lunch**: 11:00-13:00 ET (AVOID - choppy)
- **NY PM Kill Zone**: 14:00-15:00 ET (secondary setups)

### Step 3: Check for Valid Setup
Read `references/ict-setups.md` for detailed setup criteria.
Read `references/mmxm-models.md` for MMXM framework.

Valid setups (in order of priority):
1. **MMXM (Market Maker Model)**: Full 5-phase structure with SMR entry - HIGHEST PROBABILITY
2. **Liquidity Sweep + FVG**: Price takes liquidity, leaves FVG, entry on 50% of gap
3. **Order Block + MSS**: Market structure shift into valid OB
4. **Silver Bullet**: 10:00-11:00 or 14:00-15:00 FVG entries
5. **OTE**: 62-79% fib retracement in discount/premium

### Step 4: Calculate Entry, SL, TP

For MMXM MMBM (Long) setups:
- Confirm: Original Consolidation → Engineering (lower highs) → SMR zone reached
- Entry: 50% of FVG formed AFTER MSS/CHoCH
- SL: Below swept liquidity / SMR low (max 25 points)
- TP1: Old highs from Engineering Liquidity phase
- TP2: Original Consolidation high or HTF DOL

For MMXM MMSM (Short) setups:
- Confirm: Original Consolidation → Engineering (higher lows) → SMR zone reached
- Entry: 50% of FVG formed AFTER MSS/CHoCH
- SL: Above swept liquidity / SMR high (max 25 points)
- TP1: Old lows from Engineering Liquidity phase
- TP2: Original Consolidation low or HTF DOL

For standard LONG setups:
- Entry: 50% of bullish FVG or top of bullish OB
- SL: Below FVG/OB low OR below liquidity sweep low (max 25 points)
- TP1: Nearest sell-side liquidity (equal highs, PDH, session high)
- TP2: HTF draw on liquidity

For standard SHORT setups:
- Entry: 50% of bearish FVG or bottom of bearish OB  
- SL: Above FVG/OB high OR above liquidity sweep high (max 25 points)
- TP1: Nearest buy-side liquidity (equal lows, PDL, session low)
- TP2: HTF draw on liquidity

### Step 5: Provide Verdict

Always respond in this exact format:

```
═══════════════════════════════════════════
TRADE ANALYSIS
═══════════════════════════════════════════
VERDICT:     [LONG / SHORT / NO TRADE]
CONFIDENCE:  [HIGH / MEDIUM / LOW]
═══════════════════════════════════════════
BIAS:        [Bullish / Bearish / Neutral]
BIAS REASON: [1-2 sentences]
═══════════════════════════════════════════
SETUP TYPE:  [MMXM MMBM / MMXM MMSM / Liquidity Sweep + FVG / OB + MSS / Silver Bullet / OTE / None]
═══════════════════════════════════════════
ENTRY:       [price]
SL:          [price] ([X] points / $[X] risk)
TP1:         [price] ([X] points / $[X] profit) - [target description]
TP2:         [price] ([X] points / $[X] profit) - [target description]
═══════════════════════════════════════════
R:R RATIO:   [X:1]
═══════════════════════════════════════════
REASONING:
[2-3 bullet points explaining the ICT logic]
═══════════════════════════════════════════
WARNINGS:
[Any concerns, news events, or reasons for caution]
═══════════════════════════════════════════
```

## NO TRADE Conditions

Issue "NO TRADE" verdict when:
- No clear HTF bias (consolidation)
- No valid ICT setup present
- R:R less than 1.5:1
- SL would exceed 25 points
- Within NY Lunch (11:00-13:00 ET)
- High-impact news within 15 minutes
- Already at 3+ trades for the day
- Down $1,500+ for the day

## Input Template

User should provide data in this format:

```
SESSION: [London / NY AM / NY PM]
TIME: [current time ET]
CURRENT PRICE: [price]
HTF BIAS: [Bullish / Bearish / Neutral] + reason
PDH: [price]
PDL: [price]
PWH: [price]
PWL: [price]
ASIA HIGH: [price]
ASIA LOW: [price]
LIQUIDITY TAKEN: [describe any sweeps]
FVG LEVELS: [list with prices]
OB LEVELS: [list with prices]
NEWS TODAY: [any high impact events + times]
DAILY P&L: [$X]
TRADES TODAY: [X]
SETUP DESCRIPTION: [what you see]

MMXM CONTEXT (optional but increases accuracy):
ORIGINAL CONSOLIDATION: [price range if visible]
ENGINEERING PHASE: [describe - lower highs for MMBM / higher lows for MMSM]
CURRENT MMXM PHASE: [1-Consolidation / 2-Engineering / 3-SMR / 4-Accumulation / 5-Completion]
SMT DIVERGENCE: [Yes/No - comparing NQ to ES or YM]
MSS/CHoCH CONFIRMED: [Yes/No + price level]
```
