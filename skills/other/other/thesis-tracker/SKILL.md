---
name: thesis-tracker
description: Track and update investment theses for portfolio positions and watchlist. Maintains scorecard of pillars, catalysts, and conviction level. Triggers on "update thesis", "thesis check", "is my thesis intact", "add data point", "review positions".
---

# Thesis Tracker

Maintain investment theses with structured tracking of pillars, evidence, and catalysts.

## Step 1: Load or Create Thesis

**New thesis — collect:**
- Ticker + market (BYMA/US/crypto)
- Direction: Long or Short
- Core thesis: 1-2 sentences (e.g., "Long GGAL — margin expansion from rate normalization + deposit growth as inflation drops")
- 3-5 key pillars (supporting arguments)
- 3-5 key risks (what invalidates the thesis)
- Catalysts with dates (earnings, regulatory, macro events)
- Target price + time horizon
- Stop-loss trigger (price or fundamental)
- Position size (% of portfolio)

**Existing thesis:** load from project files or ask user for current state.

## Step 2: Pillar Scorecard

Maintain running scorecard:

| Pillar | Original Expectation | Current Status | Evidence | Trend |
|--------|---------------------|----------------|----------|-------|
| Revenue growth >15% | On track | Q3 was 18% YoY | 10-Q filed 11/8 | Stable |
| Margin expansion | Behind | EBITDA margin flat | Earnings call | Concerning |
| Catalyst pending | Watching | Reg decision delayed | Press release | Watch |

**Trend values:** Confirming / Stable / Concerning / Broken

## Step 3: Update Log

For each new data point:
- **Date**: when it happened
- **Event**: what changed (earnings, macro, competitor, regulatory)
- **Impact**: which pillar affected, how (strengthens/weakens/neutral)
- **Action**: hold / add / trim / exit
- **Conviction**: High / Medium / Low (updated)

## Step 4: Catalyst Calendar

| Date | Event | Ticker | Expected Impact | Status |
|------|-------|--------|-----------------|--------|
| | | | | Pending/Done/Missed |

## Step 5: AR-Specific Tracking (if applicable)

For CEDEARs:
- Track underlying ADR price + CEDEAR price + CCL implicit
- Calculate premium/discount vs theoretical parity
- Flag when premium >5% or discount >3%

For bonds (soberanos/corporativos):
- Track TIR, duration, paridad
- Spread vs benchmark (US Treasury or similar)
- Next coupon date and amortization schedule

For CCL/MEP:
- Track spread (CCL - MEP) / MEP
- Settlement dates (T+1 vs T+2)
- Parking requirement compliance

## Step 6: Thesis Health Summary

Output format:

```
═══ THESIS: [TICKER] — [LONG/SHORT] ═══
Core: [thesis statement]
Conviction: [High/Medium/Low] (was: [previous])
Pillars: [N/M on track]  Risks: [N/M active]
Next catalyst: [event] on [date]
Last updated: [date]

⚠️ ALERTS:
- [pillar X] showing weakness: [evidence]
- [catalyst Y] missed deadline
```

## Important Notes

- Track disconfirming evidence as rigorously as confirming
- If >50% of pillars are Concerning or Broken → force re-evaluation
- Quarterly review mandatory even if nothing dramatic happened
- For portfolio-wide review: show all theses sorted by conviction, flag any with deteriorating trend
- A thesis without a falsification condition is not a thesis — reject it
