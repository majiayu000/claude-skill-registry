---
name: campaign-structure
description: Design optimal Facebook/Meta campaign structure for testing including ABO vs CBO, ad set organization, targeting, and budget allocation. Use when setting up new campaigns, planning test structure, or optimizing account architecture.
---

# Campaign Structure Designer

Create optimal campaign architecture for testing and scaling.

## Process

### Step 1: Assess Offer and Budget

**Offer Type Assessment**
- VSL/long-form funnel → More controlled testing
- Lead gen/simple funnel → Can be more aggressive
- New offer → Need more testing budget
- Proven offer → Can scale faster

**Budget Allocation**
- Daily testing budget
- Target CPA/CPL
- Acceptable loss threshold
- Timeline to profitability

### Step 2: Choose Structure Type

**ABO Testing Structure (Recommended for Testing)**
Use when: Finding initial winners, testing new angles

```
Campaign: [Offer] Testing
├── Ad Set 1: [Concept A] - $X/day
│   ├── Ad 1: Hook variation 1
│   ├── Ad 2: Hook variation 2
│   └── Ad 3: Hook variation 3
├── Ad Set 2: [Concept B] - $X/day
│   ├── Ad 1...
...
```

**CBO Scaling Structure**
Use when: Scaling proven winners

```
Campaign: [Offer] Scale - $X/day CBO
├── Ad Set 1: Winners Only
│   ├── Winner Ad 1
│   ├── Winner Ad 2
│   └── Winner Ad 3
```

**2x2x3 Testing Method (Jason K)**
- 2 Headlines
- 2 Ad texts
- 3 Images/faces
= 12 ad variations testing copy combinations

**Double Six Shooter (Jason K)**
- 10-12 ad sets (different avatars)
- Same 10-12 images per ad set
- Large CBO with minimum spend per ad set
- Let Facebook find winning avatar + image combos

### Step 3: Set Targeting Parameters

**Testing Phase**
- 2% Lookalike audiences (Jason K recommends)
- Mobile newsfeed only
- WiFi only (for VSL)

**Scaling Phase**
- 10% Lookalike (Jason K)
- All placements
- Broader audiences

**Audience Sources**
- Purchase lookalikes
- Add to cart lookalikes
- Email list lookalikes
- Page engagers (for exclusions)

### Step 4: Define Budget Rules

**Testing Budget**
- Spend 1.5-2x target CPL before calling winner (Casto)
- Use initiate checkout as leading indicator (3x purchase data)
- Kill at threshold, don't hold hoping

**Winner Criteria (Jason K)**
- Doesn't lose more than once in 3 days
- Doesn't lose more than twice in 7 days
- Consistent performance, not just spikes

**Scaling Budget**
- 20% increases (safe)
- Can jump when hot, but risk breaking
- Spread across multiple ad accounts

### Step 5: Output Campaign Blueprint

```
## CAMPAIGN STRUCTURE: [Offer Name]

### PHASE 1: INITIAL TESTING

**Campaign: [Offer] - ABO Test**
- Objective: Conversions
- Budget: $[X]/day per ad set
- Duration: [X] days minimum

**Ad Set Structure:**
| Ad Set | Concept | Targeting | Budget |
|--------|---------|-----------|--------|
| 1 | [Concept A] | 2% LAL | $X |
| 2 | [Concept B] | 2% LAL | $X |
| 3 | [Concept C] | 2% LAL | $X |

**Per Ad Set:**
- 5-10 ads per concept
- Mix of hooks/variations
- Mobile newsfeed only

**Kill Criteria:**
- CPL > [X] after $[spend]
- CPA > [X] after [conversions]

**Winner Criteria:**
- CPL < [target]
- Consistent 3+ days
- Scalable volume

---

### PHASE 2: WINNER VALIDATION

**Campaign: [Offer] - CBO Scale**
- Budget: $[X]/day CBO
- Winners only (3-5 ads)
- Scale in place initially

**Expansion:**
- Replicate to Ad Account 2
- Replicate to Ad Account 3
- De-risk across accounts

---

### PHASE 3: FULL SCALE

**Structure:**
- Multiple CBOs across accounts
- $10K max per CBO (avoid instability)
- Weekend campaigns (separate)
- Day-parting: 4AM-1PM Eastern (VSL)

**Targeting Expansion:**
- Move to 10% LAL
- Test broad
- All placements

---

### CREATIVE TESTING CADENCE

**Weekly:**
- 50-100 new creative variations
- New hooks on proven angles
- New angles on proven offers

**Monthly:**
- New concept batches
- Founder content refresh
- Seasonal angles

### TRACKING SETUP
- UTM structure: [Define]
- Conversion events: [List]
- Attribution window: [Setting]
```

## Key Principles

**From Casto:**
- Broad targeting, let creative do targeting
- Use bid caps/cost caps when margins thin
- Spread across multiple ad accounts
- Build internal tools for launch automation

**From Jason K:**
- 2% LAL for testing, 10% for scaling
- Watch initiate checkouts (3x data)
- Day-part for VSL (turn off afternoon)
- Weekend campaigns with higher budgets
- Large CBO of winners is end goal

Source: Jason K, Casto (Meta-CastovsJasonK)
