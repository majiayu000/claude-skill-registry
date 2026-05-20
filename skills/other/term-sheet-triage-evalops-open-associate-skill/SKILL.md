---
name: term-sheet-triage
description: "Analyze venture financing terms with waterfall modeling: economics, control, multi-investor stacks, and 'gotchas' with clear implications. Handles complex cap tables, participating preferred, and side letters."
license: Proprietary
compatibility: Requires reading term sheet text; waterfall calculations for complex scenarios; optional Salesforce logging.
metadata:
  author: evalops
  version: "0.3"
---
# Term sheet triage

## When to use
Use this skill when you need to:
- Review a term sheet quickly and identify what matters (< 30 minutes for simple, < 2 hours for complex)
- Model multi-investor liquidation waterfalls
- Explain term implications in plain language to partners or founders
- Compare competing term sheets
- Advise founders on incoming terms

## Inputs you should request (only if missing)
- The term sheet text (or key terms if redacted)
- **Full cap table** (all prior rounds, SAFEs, notes, option pool)
- Round size and price (or cap/discount if SAFE/note)
- **All prior liquidation preferences** (multiples, participation, seniority)
- Desired ownership / board goals (if investor-side)
- Founder goals / constraints (if advising founder)

## Outputs you must produce
1) **One-line summary** (economics in one sentence)
2) **Liquidation stack** (who gets paid first, in what order)
3) **Waterfall model** (who gets paid at $10m, $30m, $100m, $500m exits)
4) **One-page term summary** (economics + control + unusual terms)
5) **Red flags list** (ranked, max 5)
6) **Negotiation levers** (what to push, what to accept, difficulty rating)

Templates:
- assets/term-sheet-checklist.md
- assets/scenario-table.md
- assets/waterfall-model.md

## Procedure

### 1) One-line economics summary (do this first)
Write one sentence: "$Xm at $Ym pre ($Zm post), Z% ownership to new investors, with [standard/non-standard] prefs."

Examples:
- "$3m at $12m pre ($15m post), 20% to Series A, 1x non-participating"
- "$500k SAFE at $8m cap, ~5.9% assuming conversion at cap"
- "$10m at $40m pre, 20% to Series B, 1x participating with 3x cap"

### 2) Classify the instrument
- Priced equity round (Series Seed, A, B, etc.)
- SAFE (post-money or pre-money cap)
- Convertible note
- Other (revenue-based, etc.)

### 3) Build the liquidation stack (multi-investor)

**Seniority order (typical, but verify):**
1. Later rounds (Series B) - often pari passu or senior
2. Earlier preferred rounds (Series A, Seed)
3. Converted SAFEs/notes (often pari passu with the round they convert into)
4. Common stock (founders, employees)

**For each investor class, document:**
| Class | Investment | Liq pref multiple | Participation | Seniority | Cap on participation |
|---|---|---|---|---|---|
| Series B | $10m | 1x | Participating | Senior | 3x cap |
| Series A | $3m | 1x | Non-participating | Pari passu with Seed | N/A |
| Seed | $1.5m | 1x | Non-participating | Junior to B | N/A |
| SAFEs | $500k | 1x (converts to Seed) | Non-participating | Converts to Seed | N/A |
| Common | N/A | None | Pro rata | Last | N/A |

### 4) Build the waterfall model

**Step-by-step waterfall calculation:**

For each exit value ($10m, $30m, $100m, $500m):

**Step 1: Pay senior liquidation preferences**
- Series B gets min(remaining proceeds, $10m × 1x)
- If participating: Series B also participates in remaining after Step 2

**Step 2: Pay pari passu liquidation preferences**
- Series A and Seed share remaining proceeds pro rata up to their 1x preferences
- Series A: min(remaining × (3m/4.5m), $3m)
- Seed: min(remaining × (1.5m/4.5m), $1.5m)

**Step 3: Participation (if applicable)**
- Participating preferred gets their preference PLUS pro rata share of remainder
- Non-participating must choose: preference OR convert to common

**Step 4: Distribution to common**
- Whatever remains goes pro rata to common + converted preferred

**Waterfall table:**
| Exit value | Series B | Series A | Seed | Common | Founder % | Notes |
|---|---|---|---|---|---|---|
| $10m | $10m | $0 | $0 | $0 | 0% | B takes all |
| $30m | $14m | $4.8m | $2.4m | $8.8m | 22% | B participating to cap |
| $100m | $30m | $21m | $10.5m | $38.5m | 24% | B hits 3x cap |
| $500m | $30m | $141m | $70.5m | $258.5m | 32% | All convert, pro rata |

### 5) Extract economics that matter

**For priced rounds:**
| Term | Value | Standard? | Impact on founders |
|---|---|---|---|
| Pre-money valuation | | | |
| Post-money valuation | | | |
| New investor ownership | | | |
| Option pool (pre/post) | | >10% post is aggressive | |
| Liquidation preference | | 1x is standard | |
| Participation | | Non-participating is founder-friendly | |
| Participation cap | | 3x is reasonable if participating | |
| Anti-dilution | | Broad-based weighted avg is standard | |
| Pro-rata rights | | | |
| Pay-to-play | | None is standard | |

**For SAFEs/notes:**
| Term | Value | Standard? | Impact |
|---|---|---|---|
| Cap | | | |
| Discount | | 20% is standard | |
| MFN | | Yes is standard | |
| Interest rate (notes) | | 5-8% is standard | |
| Maturity (notes) | | 18-24 months is standard | |
| Conversion trigger | | Qualified financing is standard | |
| Pro-rata rights | | | |

### 6) Extract control terms
| Term | Provision | Standard? | What it blocks |
|---|---|---|---|
| Board composition | | 2 founders + 1 investor + 1 independent is common at A | |
| Board observer | | 1 observer is standard | |
| Protective provisions | | See standard list below | |
| Information rights | | Quarterly financials is standard | |
| Drag-along | | Majority preferred + majority common is standard | |
| Founder vesting | | 4-year with 1-year cliff is standard | |
| Voting agreement | | | |

**Standard protective provisions (investor consent required):**
- Change authorized shares
- Create senior or pari passu preferred
- Change charter or bylaws materially
- Sell or merge the company
- Change board size
- Declare dividends
- Wind down the company

**Non-standard protective provisions to flag:**
- Consent for hiring/firing executives
- Consent for budget approval
- Consent for contracts over $X
- Consent for debt over $X

### 7) Identify red flags (max 5, ranked)

| Red flag | Why it matters | Severity (1-5) | Negotiable? |
|---|---|---|---|
| Participating preferred without cap | Double-dips on exit, can take 40%+ of small exits | 5 | Yes - push for cap or non-participating |
| >1x liquidation preference | Blocks smaller exits, misaligns incentives | 5 | Yes - push for 1x |
| Full ratchet anti-dilution | Punitive in down round, can wipe out founders | 4 | Yes - push for broad-based weighted |
| Overly broad protective provisions | Investor can block normal operations | 4 | Yes - narrow scope |
| Redemption rights | Forces liquidity event, time bomb | 4 | Yes - remove or extend horizon |
| Founder vesting reset | Demotivates founders, often unreasonable | 3 | Yes - push for acceleration |
| Aggressive option pool | Dilutes founders pre-money | 3 | Yes - negotiate size |
| Side letters with extra rights | Creates conflicts between investors | 3 | Depends |

### 8) Side letter analysis (often where sharp edges hide)

**Common side letter provisions to review:**
| Provision | Standard? | Impact |
|---|---|---|
| Super pro-rata | Non-standard | Squeezes other investors in future rounds |
| Board seat guarantee | Depends on check size | May conflict with other investors |
| Information rights upgrade | Sometimes | Extra reporting burden |
| Most favored nation | Standard | If anyone gets better terms, they do too |
| Anti-dilution protection upgrade | Non-standard | Better protection than other investors |
| Co-sale rights | Standard | Can sell alongside founders |
| Veto on specific actions | Non-standard | Extra control |

**Side letter red flag:** If side letters give one investor materially better terms, other investors will likely demand the same (MFN cascade).

### 9) Multi-round complexity handling

**When comparing multiple term sheets:**
| Term | Offer A | Offer B | Offer C | Notes |
|---|---|---|---|---|
| Pre-money | $15m | $12m | $18m | |
| Check size | $3m | $4m | $3m | |
| Ownership | 16.7% | 25% | 14.3% | |
| Liq pref | 1x NP | 1x Part | 1x NP | B has participating |
| Board | 2/1/1 | 2/2/0 | 2/1/1 | B wants 2 seats |
| Pro-rata | Yes | Super | Yes | B wants super pro-rata |

**Effective valuation comparison (factor in option pool, prefs):**
- Offer A effective value: $Xm
- Offer B effective value: $Ym (lower due to participation)
- Offer C effective value: $Zm

### 10) Summary recommendation

**One paragraph:**
- Is this a fair deal?
- What are the 1-2 terms worth negotiating?
- What should be accepted as-is?
- Any deal-breakers?
- How does the waterfall look at realistic exit scenarios?

## Waterfall model template

```
Exit value: $___m

STEP 1: Senior preferences
- Series B: min($___m, $___ preference) = $___m
- Remaining: $___m

STEP 2: Pari passu preferences  
- Series A: min($___m × __%, $___ preference) = $___m
- Seed: min($___m × __%, $___ preference) = $___m
- Remaining: $___m

STEP 3: Participation
- Series B (participating): $___m × __% ownership = $___m (capped at $___m)
- Remaining: $___m

STEP 4: Conversion analysis
- Series A as-if-converted: $___m × __% = $___m
- Series A chooses: preference ($___m) vs converted ($___m) = $___m
[Repeat for each non-participating class]

STEP 5: Distribution
- Series A: $___m (___%)
- Seed: $___m (___%)
- Common: $___m (___%)
- Founder take-home: $___m (___%)
```

## Public references
- Brad Feld & Jason Mendelson's Venture Deals (liquidation preference mechanics)
- HSBC Innovation Banking waterfall guides
- Allied VC cap table modeling guides

## Salesforce logging (optional)
- Attach the term sheet as a File to the Opportunity
- Create a Note: "Term summary: [one-line] | Red flags: [list] | Rec: [accept/negotiate/walk]"
- Update Opportunity stage to "Term Sheet"
- Log waterfall model output in Notes

## Edge cases
- If terms are incomplete: list missing terms and explain what each missing term could change. Assume standard terms for modeling but flag assumptions.
- If there are side letters: treat them as first-class. Model their impact on the waterfall.
- If cap table is messy: clean it up first. SAFEs and notes must be modeled with conversion assumptions.
- If multiple SAFEs at different caps: model each conversion scenario separately.
- If there's a bridge round: model bridge terms and how they interact with the new round.
