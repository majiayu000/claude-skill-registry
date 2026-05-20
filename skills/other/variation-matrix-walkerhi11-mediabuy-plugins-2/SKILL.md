---
name: variation-matrix
description: Generate all possible ad variations from modular components (hooks, bodies, CTAs) with prioritized testing order. Use when planning creative tests, maximizing existing assets, or building a systematic variation testing schedule.
---

# Variation Matrix

Create all possible ad combinations from modular components.

## Process

### Step 1: Input Available Components

**Hooks (H)**
List all available hook clips/copy:
- H1: [Description]
- H2: [Description]
- H3: [Description]
...

**Bodies (B)**
List all available body sections:
- B1: Testimonial body
- B2: Explainer body
- B3: Social proof compilation
...

**CTAs (C)**
List all available call-to-action clips/copy:
- C1: Direct CTA
- C2: Scarcity CTA
- C3: Story-based CTA
...

### Step 2: Create Combination Matrix

**Total Variations = H x B x C**

Example: 5 hooks x 3 bodies x 2 CTAs = 30 variations

```
| Variation | Hook | Body | CTA |
|-----------|------|------|-----|
| V1        | H1   | B1   | C1  |
| V2        | H1   | B1   | C2  |
| V3        | H1   | B2   | C1  |
| V4        | H1   | B2   | C2  |
| V5        | H1   | B3   | C1  |
...
```

### Step 3: Prioritize by Predicted Performance

**Scoring Factors:**
- Hook strength (past performance or score)
- Body relevance to hook
- CTA match to body
- Overall flow/coherence

**Priority Tiers:**

**Tier 1 - Test First (High confidence)**
- Best hooks + proven bodies
- Logical flow combinations
- Based on winning patterns

**Tier 2 - Test Second (Medium confidence)**
- Good hooks + new bodies
- Testing new combinations
- Iterating on Tier 1 learnings

**Tier 3 - Test Later (Experimental)**
- Untested combinations
- Unusual pairings
- "What if" variations

### Step 4: Suggest Testing Order

**Phase 1: Prove the hooks**
Test all hooks with best body + best CTA
- V1, V5, V9, V13, V17 (one per hook)

**Phase 2: Find best body for winning hooks**
Take top 2-3 hooks, test all bodies
- Winning hooks x all bodies

**Phase 3: Optimize CTA**
Take top combinations, test all CTAs

**Phase 4: Full matrix test**
Roll out remaining combinations based on learnings

### Step 5: Output Numbered Variation List

```
## VARIATION MATRIX: [Offer/Campaign]

### COMPONENT INVENTORY

**HOOKS ([#] available)**
| ID | Description | Score | Source |
|----|-------------|-------|--------|
| H1 | [Description] | 9/10 | [Clip/Copy] |
| H2 | [Description] | 8/10 | [Clip/Copy] |
...

**BODIES ([#] available)**
| ID | Type | Description | Duration |
|----|------|-------------|----------|
| B1 | Testimonial | [Description] | 20s |
| B2 | Explainer | [Description] | 25s |
...

**CTAs ([#] available)**
| ID | Type | Description |
|----|------|-------------|
| C1 | Direct | "Click the link below" |
| C2 | Scarcity | "Sale ends Friday" |
...

---

### FULL MATRIX

Total Possible Variations: [#]

| # | Hook | Body | CTA | Priority | Est. Length |
|---|------|------|-----|----------|-------------|
| 1 | H1 | B1 | C1 | Tier 1 | 30s |
| 2 | H1 | B1 | C2 | Tier 2 | 30s |
| 3 | H1 | B2 | C1 | Tier 2 | 35s |
...

---

### TESTING PHASES

**PHASE 1: Hook Test (Week 1)**
Variations: V1, V6, V11, V16, V21
Budget: $[X]
Goal: Identify top 2-3 hooks

| Var | Components | Priority |
|-----|------------|----------|
| V1 | H1+B1+C1 | Test |
| V6 | H2+B1+C1 | Test |
...

**PHASE 2: Body Test (Week 2)**
Take winning hooks, test all bodies
Budget: $[X]
Goal: Find best body for each hook

**PHASE 3: CTA Optimization (Week 3)**
Take winning combinations, test CTAs
Budget: $[X]
Goal: Maximize conversion

**PHASE 4: Scale Winners (Week 4+)**
Full variations of proven combinations

---

### QUICK REFERENCE

**Top 10 Priority Variations:**
1. V[X]: H[X] + B[X] + C[X] - [Rationale]
2. V[X]: H[X] + B[X] + C[X] - [Rationale]
...

**Experimental Combinations:**
- V[X]: [Why worth testing despite lower confidence]

---

### PRODUCTION CHECKLIST

**To Create [#] Variations:**
- [ ] Hook clips ready: [#]
- [ ] Body sections ready: [#]
- [ ] CTA clips ready: [#]
- [ ] Editing timeline: [Date]
- [ ] Launch date: [Date]

**Naming Convention:**
[Offer]_[Hook#]_[Body#]_[CTA#]_v[version]
Example: Rise_H1_B2_C1_v1
```

## Variation Strategy (LeadsIcon)

**Modular Thinking:**
- Each component has a job
- Hook: Grab attention
- Body: Build belief
- CTA: Remove friction

**Testing Efficiency:**
- Don't test everything at once
- Isolate variables
- Build on winners
- Kill losers fast

**From Winners:**
- Create 10+ variations of each winner
- Test new hooks on winning bodies
- Test new bodies with winning hooks
- Compound improvements

Source: LeadsIcon, VISCAP
