---
name: campaign-diagnosis
description: Diagnose underperforming campaigns by analyzing metrics against benchmarks, checking creative fatigue, evaluating audience saturation, and assessing offer/lander issues. Use when campaigns stop working, CPA rises unexpectedly, or performance declines.
---

# Campaign Diagnosis

Identify and fix underperforming campaign issues.

## Process

### Step 1: Analyze Metrics vs Benchmarks

**Key Metrics to Check:**

| Metric | Current | Benchmark | Status |
|--------|---------|-----------|--------|
| CPA | $X | $X | +/-X% |
| CPL | $X | $X | +/-X% |
| CTR | X% | X% | +/-X% |
| CVR | X% | X% | +/-X% |
| CPM | $X | $X | +/-X% |
| CPC | $X | $X | +/-X% |

**Benchmark Sources:**
- Historical account averages
- Industry standards
- Previous winning campaigns
- Competitor estimates

### Step 2: Check Creative Fatigue Indicators

**Fatigue Signals:**
- Declining CTR over time
- Rising frequency on same audience
- Negative comment sentiment increasing
- Same creatives running 30+ days without refresh

**Fatigue Analysis:**
- Chart CTR over last 14/30 days
- Check frequency by ad
- Review comment quality
- Compare to fresh creative performance

### Step 3: Evaluate Audience Saturation

**Saturation Signals:**
- Declining reach at same budget
- Rising CPM without platform changes
- Decreasing results at same spend
- Audience size shrinking in reporting

**Saturation Checks:**
- Audience overlap between ad sets
- Total addressable audience vs. reach
- Frequency across all campaigns
- LAL exhaustion (2% vs 5% vs 10%)

### Step 4: Assess Offer/Lander Issues

**Lander Diagnostics:**
- Page load speed
- Mobile experience
- Form completion rates
- Exit points in funnel

**Offer Diagnostics:**
- Conversion rate changes
- Lead quality feedback from buyer
- Payout changes from network
- Competitive offer landscape

**Funnel Metrics:**
- Ad CTR → Lander CTR → Form submit → Conversion
- Identify biggest drop-off point

### Step 5: Output Prioritized Fix Recommendations

```
## CAMPAIGN DIAGNOSIS: [Campaign Name]

### CURRENT SITUATION
- Performance change: [Description]
- Timeline: [When it started]
- Magnitude: [How bad]
- Spend impact: $[Lost/At risk]

---

### DIAGNOSTIC SUMMARY

| Issue Area | Severity | Confidence |
|------------|----------|------------|
| Creative Fatigue | [H/M/L] | [H/M/L] |
| Audience Saturation | [H/M/L] | [H/M/L] |
| Lander Issues | [H/M/L] | [H/M/L] |
| Offer Issues | [H/M/L] | [H/M/L] |
| Platform Changes | [H/M/L] | [H/M/L] |
| Competition | [H/M/L] | [H/M/L] |

---

### ISSUE 1: [Primary Problem]

**Evidence:**
- [Data point 1]
- [Data point 2]
- [Data point 3]

**Root Cause:**
[Analysis of why this is happening]

**Recommended Fix:**
1. [Immediate action]
2. [Short-term fix]
3. [Long-term solution]

**Expected Impact:**
[What should improve and by how much]

---

### ISSUE 2: [Secondary Problem]
...

---

### FUNNEL ANALYSIS

```
Ad Impressions: [#]
    ↓ CTR: X% (Benchmark: X%)
Ad Clicks: [#]
    ↓ Lander CTR: X% (Benchmark: X%)
Lander Clicks: [#]
    ↓ Form Rate: X% (Benchmark: X%)
Form Submits: [#]
    ↓ Conversion: X% (Benchmark: X%)
Conversions: [#]

BOTTLENECK: [Biggest drop-off identified]
```

---

### PRIORITY ACTION LIST

**CRITICAL (Do Today):**
1. [Action] - Expected impact: [Result]
2. [Action] - Expected impact: [Result]

**HIGH (This Week):**
1. [Action] - Expected impact: [Result]
2. [Action] - Expected impact: [Result]

**MEDIUM (Next Week):**
1. [Action] - Expected impact: [Result]

---

### CREATIVE FATIGUE FIX

**If Fatigue Confirmed:**
1. Launch new creative batch immediately
2. Reduce budget on fatigued creatives
3. Iterate on winning angles with new hooks
4. Test new angles/concepts

**Creative Refresh Schedule:**
- Weekly: [X] new variations
- Bi-weekly: [X] new concepts

---

### AUDIENCE SATURATION FIX

**If Saturation Confirmed:**
1. Expand LAL (2% → 5% → 10%)
2. Test broad targeting
3. Open new geos
4. Find new audience sources
5. Reduce frequency caps

---

### LANDER/OFFER FIX

**If Lander Issue:**
1. Speed optimization
2. Mobile experience audit
3. Form simplification
4. A/B test headline
5. Add/improve social proof

**If Offer Issue:**
1. Negotiate better payout
2. Test alternative offers
3. Improve lead quality
4. Address buyer feedback

---

### MONITORING PLAN

**Daily Checks:**
- [ ] CPA vs target
- [ ] CTR trend
- [ ] Spend pacing

**Weekly Review:**
- [ ] Creative performance ranking
- [ ] Audience metrics
- [ ] Funnel conversion rates
- [ ] Competitor activity

**Escalation Triggers:**
- CPA >X% above target for 2 days
- CTR drops >X% week over week
- Volume drops >X% at same budget
```

## Diagnostic Framework

**CTR Issue → Creative Problem**
- Hooks not stopping scroll
- Images not compelling
- Ad fatigue

**High CTR + Low CVR → Lander Problem**
- Message mismatch
- Page issues
- Trust/proof missing

**Good Metrics + No Volume → Saturation**
- Audience tapped out
- Need expansion

**Sudden Drop → External Factor**
- Platform algorithm change
- Competitor activity
- Seasonal shift
- Offer/payout change

Source: Meta-CastovsJasonK, Jason K
