---
name: test-analysis
description: Analyze creative test results using heatmaps and data visualization to identify statistical winners and recommend next steps (scale, iterate, or kill). Use when reviewing test performance, making optimization decisions, or planning next test phases.
---

# Test Analysis

Analyze test results and recommend actions.

## Process

### Step 1: Input Performance Data

Gather metrics:
- CPL (Cost Per Lead)
- CPA (Cost Per Acquisition)
- CTR (Click-Through Rate)
- CVR (Conversion Rate)
- Spend per creative
- Initiate checkouts (leading indicator)
- Time period data

### Step 2: Create Heatmap Visualization

**For 2x2 or 2x2x3 Tests:**

```
         | Ad Text 1 | Ad Text 2 |
---------|-----------|-----------|
Headline1|   CPA $X  |   CPA $X  |
Headline2|   CPA $X  |   CPA $X  |
```

**Color Coding:**
- Green: Below target CPA
- Yellow: At target CPA
- Red: Above target CPA

**For Avatar/Image Tests:**

```
         | Image 1 | Image 2 | Image 3 | ...
---------|---------|---------|---------|----
Avatar 1 |  $CPA   |  $CPA   |  $CPA   |
Avatar 2 |  $CPA   |  $CPA   |  $CPA   |
...
```

### Step 3: Identify Statistical Winners

**Winner Criteria (Jason K):**
- Doesn't lose more than 1x in 3 days
- Doesn't lose more than 2x in 7 days
- Consistent performance over time

**Statistical Confidence:**
- Minimum spend: 1.5-2x target CPA
- Minimum conversions: 10+ for confidence
- Look at trends, not single days

**Leading Indicators:**
- Initiate checkout CPA = ~1/3 of purchase CPA
- High CTR + low CVR = lander issue
- Low CTR + any CVR = creative issue

### Step 4: Categorize Results

**SCALE** - Move to scaling CBO
- Consistent winner over 3+ days
- Below target CPA
- Good volume potential

**ITERATE** - Create variations
- Shows promise but inconsistent
- Close to target CPA
- Clear element working (hook, angle, etc.)

**KILL** - Stop spending
- Consistently above target
- No signs of improvement
- Clear loser after sufficient spend

**TEST MORE** - Needs more data
- Insufficient spend for decision
- Mixed signals
- New variable to isolate

### Step 5: Output Analysis Report

```
## TEST ANALYSIS: [Test Name]
Period: [Date range]
Total Spend: $[Amount]
Target CPA: $[Amount]

---

### HEATMAP: [Test Type]

[Visual heatmap grid]

---

### PERFORMANCE SUMMARY

| Creative | Spend | Leads | CPA | CTR | CVR | Status |
|----------|-------|-------|-----|-----|-----|--------|
| Ad 1     | $X    | X     | $X  | X%  | X%  | SCALE  |
| Ad 2     | $X    | X     | $X  | X%  | X%  | ITERATE|
| Ad 3     | $X    | X     | $X  | X%  | X%  | KILL   |

---

### WINNERS (Move to Scale CBO)

**Ad 1: [Name/Description]**
- CPA: $X (X% below target)
- Key elements: [What's working]
- Volume potential: [Assessment]

---

### ITERATE (Create Variations)

**Ad 2: [Name/Description]**
- CPA: $X (X% above target)
- Promising elements: [What's working]
- Issues: [What to fix]
- Next test: [Specific variation to try]

---

### KILL (Stop Immediately)

**Ad 3: [Name/Description]**
- CPA: $X (X% above target)
- Why it failed: [Analysis]
- Learnings: [What to avoid]

---

### PATTERN ANALYSIS

**What's Working:**
- [Pattern 1]
- [Pattern 2]

**What's Not Working:**
- [Pattern 1]
- [Pattern 2]

**Hypothesis for Next Test:**
- [Based on data, test this next]

---

### RECOMMENDATIONS

**Immediate Actions:**
1. Scale [Ad X] to CBO
2. Kill [Ad Y, Z]
3. Create iterations of [Ad A]

**Next Test Phase:**
- Test type: [Description]
- Variables: [What to test]
- Budget: $[Amount]
- Timeline: [Duration]

**Funnel Optimization:**
- [If lander issues identified]
- [If offer issues identified]
```

## Analysis Framework

**Metric Priorities:**
1. CPA/CPL (primary)
2. CVR (funnel health)
3. CTR (creative appeal)
4. Initiate checkout (leading indicator)

**Time Analysis:**
- Day-over-day trends
- Day-of-week patterns
- Hour-of-day patterns (for day-parting)

**Diagnostic Questions:**
- High CTR, low CVR → Lander problem
- Low CTR → Creative problem
- Good metrics, no scale → Audience saturation
- Inconsistent → Need more data or bid caps

Source: Jason K (heatmap method), Meta-CastovsJasonK
