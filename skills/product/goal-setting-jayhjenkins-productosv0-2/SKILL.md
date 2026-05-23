---
name: goal-setting
description: Use when establishing targets for defined metrics - validates metric is movable by team, assesses movement needed for company goals, evaluates aggressive vs conservative targets with trade-off analysis
---

# Goal Setting Workflow

## Purpose

Establish ambitious but realistic targets for defined metrics by understanding company-level impact needed, validating team's ability to move the metric, and evaluating trade-offs between aggressive and conservative goals.

## When to Use This Workflow

Use this workflow when:
- After defining success metrics, need to set OKRs or targets
- Planning roadmap and need to estimate impact of initiatives
- Leadership asks "what's the goal for this metric this quarter?"
- Evaluating whether proposed project is worth the investment
- Setting team or product area goals
- Translating company-level goals to product-level targets

## Skills Sequence

This workflow orchestrates 3 core skills:

```
1. North Star Alignment
   ↓ (How much movement matters to company goals?)
2. Proxy Metric Selection
   ↓ (Validate metric is movable by this team)
3. Trade-off Evaluation
   ↓ (Cost of aggressive vs conservative targets)
   
OUTPUT: Target value or % improvement, timeframe, confidence level,
        dependencies and assumptions
```

## Required Inputs

Gather this information before starting:

### Metric Information
- **The metric and its current baseline**
  - Metric name and formula
  - Current value
  - Example: "Weekly Active Users = 100,000"

- **Historical trends**
  - How has metric moved historically?
  - Seasonality patterns?
  - Growth rate trajectory?
  - Example: "Growing 3% month-over-month for past year"

### Context
- **Planned initiatives**
  - What are you building to move this metric?
  - Estimated impact of each initiative
  - Timeline for delivery

- **Comparison benchmarks (if available)**
  - Competitor metrics
  - Industry standards
  - Similar products' performance

### Company Goals
- **Company-level targets**
  - What are company OKRs?
  - How does this metric contribute?
  - What movement is needed for company goals?

- **Resource constraints**
  - Team size and capacity
  - Budget limitations
  - Technical constraints

## Workflow Steps

### Step 1: Assess Company-Level Impact Needed (15 minutes)

**Use the `north-star-alignment` skill**

Understand how much metric movement matters to company goals:

**Activities:**

1. **Identify North Star connection**
   - How does your metric connect to company North Star?
   - What's the multiplier or contribution factor?
   - Example: "10% increase in WAU → 2% increase in company MAU"

2. **Calculate company goal contribution**
   - If company wants X% growth in North Star
   - How much must your metric grow?
   - Example: "Company wants 10% MAU growth; our product = 20% of MAU; need 10% WAU growth minimum"

3. **Evaluate strategic importance**
   - Is this metric critical path to company goals?
   - Or nice-to-have but not essential?
   - Priority: Critical / Important / Opportunistic

**Output:**

```markdown
## Company-Level Impact Assessment

**North Star Connection:**
- Company North Star: [Metric name]
- Your metric's contribution: [How it ladders up]
- Multiplier/factor: [Quantify relationship]

**Company Goal Translation:**
- Company target: [X% growth in North Star]
- Required from your product: [Y% growth in your metric]
- Rationale: [Calculation or logic]

**Strategic Priority:**
- [Critical / Important / Opportunistic]
- Why: [Explanation]

**Minimum viable target:**
- To meet company needs: [Minimum % or absolute value]
```

### Step 2: Validate Metric Movability (20 minutes)

**Use the `proxy-metric-selection` skill**

Confirm the team can actually influence this metric:

**Activities:**

1. **Identify levers team controls**
   - What features/changes can team implement?
   - What's outside team's control?
   - What dependencies exist?

2. **Estimate initiative impacts**
   - For each planned initiative, estimate impact
   - Use historical data, A/B tests, competitor analysis
   - Range estimates (low/medium/high confidence)

3. **Sum potential impact**
   - Add up all initiatives
   - Account for overlap/cannibalization
   - Reality-check against historical growth rates

4. **Assess confidence**
   - High confidence: Proven tactics, similar to past successes
   - Medium confidence: Reasonable hypotheses, some validation
   - Low confidence: Exploratory, unproven approaches

**Output:**

```markdown
## Movability Assessment

**Team Control:**
- Direct levers: [What team can change]
- Indirect influence: [What team can affect partially]
- Outside control: [What team cannot affect]

**Planned Initiatives:**

| Initiative | Est. Impact (Low) | Est. Impact (High) | Confidence | Timeline |
|------------|-------------------|---------------------|------------|----------|
| [Feature A] | +2% | +5% | Medium | Q1 |
| [Feature B] | +1% | +3% | High | Q1 |
| [Feature C] | +3% | +8% | Low | Q2 |

**Total Potential Impact:**
- Conservative (low estimates): [Sum]
- Aggressive (high estimates): [Sum]
- Reality-checked: [Adjusted for overlap, feasibility]

**Confidence Level:**
- [High / Medium / Low]
- Based on: [Historical performance, validation, team track record]

**Dependencies:**
- [Other teams, external factors, resources needed]
```

### Step 3: Evaluate Target Trade-offs (20 minutes)

**Use the `tradeoff-evaluation` skill**

Assess costs and benefits of aggressive vs. conservative targets:

**Framework: Three target levels**

#### Level 1: Conservative Target
- **Definition:** Achievable with high confidence
- **Characteristics:**
  - Based on proven tactics
  - Requires minimal risk-taking
  - Accounts for setbacks
- **Pro:** Likely to hit target, builds credibility
- **Con:** May leave growth on table, less inspiring

#### Level 2: Ambitious Target
- **Definition:** Stretch goal requiring execution excellence
- **Characteristics:**
  - Requires most initiatives to succeed
  - Some unknowns but reasonable
  - Pushes team but achievable
- **Pro:** Motivating, meaningful if hit
- **Con:** 50-70% confidence, some risk

#### Level 3: Moonshot Target
- **Definition:** Requires everything to go right + surprises
- **Characteristics:**
  - All initiatives succeed maximally
  - Plus unexpected wins
  - Low probability but transformative
- **Pro:** Inspires big thinking
- **Con:** High failure risk, may demotivate if unrealistic

**Evaluate each level:**

**Questions:**
1. **Resource cost:** What resources required for each level?
2. **Opportunity cost:** What are we NOT doing to hit this?
3. **Risk:** What breaks if we miss?
4. **Motivation:** Does target inspire or overwhelm team?
5. **Stakeholder expectation:** What's leadership expecting?

**Output:**

```markdown
## Target Trade-off Analysis

**Conservative Target:** [Value or % improvement]
- Confidence: 90%+
- Based on: [Proven tactics, historical trends]
- Pros: [List]
- Cons: [List]
- Resource needs: [Description]

**Ambitious Target:** [Value or % improvement]
- Confidence: 60-70%
- Based on: [All planned initiatives + reasonable execution]
- Pros: [List]
- Cons: [List]
- Resource needs: [Description]
- Risk if missed: [Impact]

**Moonshot Target:** [Value or % improvement]
- Confidence: 20-30%
- Based on: [Everything + unexpected wins]
- Pros: [List]
- Cons: [List]
- Resource needs: [Description]
- Risk if missed: [Impact]

**Recommendation:** [Which level to commit to]
- Rationale: [Why this level makes sense]
- Publicly commit to: [May be different from internal stretch]
- Internal stretch: [What team pushes for privately]
```

### Step 4: Set Final Goal (10 minutes)

Synthesize analyses into clear goal statement:

**Components of good goal:**
1. **Metric:** Precise definition
2. **Target:** Specific value or % improvement
3. **Timeframe:** Clear deadline
4. **Confidence:** Commitment vs. aspirational
5. **Dependencies:** What must be true
6. **Milestones:** Intermediate checkpoints

**Goal template:**

```markdown
## Final Goal Statement

**Primary Goal:**
Increase [Metric name] from [Current baseline] to [Target value] by [Date]

**This represents:** [X% improvement]

**Commitment level:** [Committed / Aspirational / Stretch]

**Confidence:** [%]

**Why this target:**
1. [Company contribution reason]
2. [Team capability reason]
3. [Strategic timing reason]

**Key Initiatives:**
1. [Initiative name]: [Expected contribution]
2. [Initiative name]: [Expected contribution]
3. [Initiative name]: [Expected contribution]

**Dependencies:**
- [External dependency 1]
- [External dependency 2]
- [Resource dependency]

**Milestones:**
- Month 1: [Intermediate target]
- Month 2: [Intermediate target]
- Month 3: [Intermediate target]

**Success criteria:**
- Hit target: [What constitutes success]
- Partial success: [What's acceptable]
- Failure: [What triggers re-evaluation]

**Review cadence:**
- [Weekly / Bi-weekly / Monthly] check-ins
- [What triggers goal revision]
```

## Goal-Setting Frameworks

### Framework 1: OKR Structure

**Objective:** Qualitative, inspiring
**Key Results:** Quantitative, measurable

**Example:**
- **Objective:** Make our product indispensable for power users
- **Key Result 1:** Increase WAU from 100K to 120K (20% growth)
- **Key Result 2:** Increase daily actives from 40K to 50K (25% growth)
- **Key Result 3:** Improve week-2 retention from 60% to 70%

**Scoring:** 0-1 scale
- 0.7-1.0 = Success (ambitious targets)
- 0.4-0.6 = Partial progress
- <0.4 = Missed

### Framework 2: Committed vs. Aspirational

**Committed goals:**
- 90%+ confidence
- Resources committed
- What you'll be evaluated on
- Example: "Grow WAU 10%"

**Aspirational goals:**
- 50-60% confidence
- Stretch targets
- Not penalized for missing
- Example: "Grow WAU 25%"

### Framework 3: Input vs. Output Goals

**Output goals (results):**
- "Increase WAU 20%"
- What you want to achieve
- Ties to company goals

**Input goals (activities):**
- "Launch 3 major features"
- What you'll do
- Ties to team capacity

**Best practice:** Set both
- Primary: Output goal
- Supporting: Input goals that should deliver output

### Framework 4: Leading Indicator Targets

**Why:** Leading indicators move before lagging outcomes

**Example:**
- Lagging: Retention rate (know months later)
- Leading: Activation rate (know immediately)

**Set targets for:**
- Leading indicators (drive focus)
- Lagging indicators (confirm success)

## Common Pitfalls

| Pitfall | How to Avoid |
|---------|--------------|
| Sandbagging (too easy) | Push to ambitious level, not conservative |
| Moonshot without plan | Ensure initiatives exist to support target |
| No company alignment | Start with North Star connection |
| Ignoring historical trends | Reality-check against past performance |
| No intermediate milestones | Break into monthly/quarterly checkpoints |
| Not considering seasonality | Adjust for known seasonal effects |
| Resource mismatch | Validate team capacity to execute |

## Success Criteria

Goal setting succeeds when:
- Target value/% clearly stated
- Timeframe specific
- Company-level impact articulated
- Team's ability to move metric validated
- Initiatives mapped to target with estimated impacts
- Trade-offs between aggressive/conservative evaluated
- Confidence level honest
- Dependencies and assumptions documented
- Intermediate milestones defined
- Review cadence established
- Stakeholders aligned on goal

## Real-World Example: Uber Driver Quality Program

### Context
- Metric: Hours driven in 4.8+ rating bucket
- Current: 4.8M hours / 60% of total
- Timeline: Next quarter (Q1)

### Step 1: Company Impact (15 min)

```
Company Goal: Grow Monthly Active Drivers 15% in 2025
Our Contribution: Driver quality → retention → supply growth

Math:
- If quality drivers stay 20% longer
- And recruit 10% more drivers via referrals (quality attracts quality)
- Contributes ~5 percentage points to 15% MAD goal

Strategic Priority: Critical (supply is bottleneck for growth)

Minimum viable: 65% of hours in 4.8+ bucket (5 percentage point improvement)
```

### Step 2: Movability Assessment (20 min)

```
Team Control:
- Direct: Quality dashboard, driver tips, rating transparency
- Indirect: Driver training, incentives (ops team)
- Outside: Rider behavior, market conditions

Planned Initiatives:

| Initiative | Low Impact | High Impact | Confidence | Timeline |
|------------|------------|-------------|------------|----------|
| Enhanced dashboard | +1% | +2% | High | Month 1 |
| Quality tips program | +2% | +4% | Medium | Month 1-2 |
| Referral program | +1% | +3% | Medium | Month 2-3 |
| Driver coaching | +1% | +2% | High | Ongoing |

Total Potential:
- Conservative: +5 percentage points (65% total)
- Aggressive: +11 percentage points (71% total)
- Reality-checked: +7 percentage points (67% total)
  (Accounting for overlap, execution risk)

Confidence: Medium-High (70%)
- Based on: Similar programs in other markets worked
- Risk: Driver adoption lower than expected

Dependencies:
- Ops team for coaching rollout
- Data team for dashboard enhancements
```

### Step 3: Trade-off Analysis (20 min)

```
Conservative Target: 65% (5 points)
- Confidence: 90%
- Based on: Enhanced dashboard + quality tips (proven tactics)
- Pro: Highly achievable, builds credibility
- Con: Doesn't capitalize on full potential, uninspiring
- Resource: 2 engineers, 1 designer, 1 PM

Ambitious Target: 67% (7 points)
- Confidence: 70%
- Based on: All initiatives, reasonable execution
- Pro: Meaningful improvement, motivating team
- Con: Requires referral program success (moderate risk)
- Resource: +1 growth engineer for referrals

Moonshot Target: 70% (10 points)
- Confidence: 30%
- Based on: Everything working + viral referral growth
- Pro: Transformative if achieved
- Con: Very low probability, may demotivate if unrealistic
- Resource: Full team focus, opportunity cost high

Recommendation: Ambitious (67%)
- Company needs meaningful contribution (5% minimum)
- Team has clear plan for 7% (all initiatives)
- 70% confidence acceptable for OKR
- Publicly commit to 67%, internal stretch to 69%
```

### Step 4: Final Goal (10 min)

```
PRIMARY GOAL:
Increase hours driven in 4.8+ rating bucket from 60% to 67% by end of Q1 2025

This represents: 7 percentage point improvement

Commitment level: Aspirational OKR (targeting 0.7-1.0 score)

Confidence: 70%

Why this target:
1. Company contribution: Supports 15% MAD growth goal (critical path)
2. Team capability: Have clear initiatives totaling 7-11% potential
3. Strategic timing: Quality program momentum from Q4, capitalize now

Key Initiatives:
1. Enhanced dashboard (Month 1): +1-2 points
2. Quality tips program (Month 1-2): +2-4 points
3. Referral program (Month 2-3): +1-3 points
4. Driver coaching (Ongoing): +1-2 points

Dependencies:
- Ops team partnership for coaching
- Data team dashboard platform (committed)
- Referral incentive budget approved

Milestones:
- Month 1: 62% (dashboard launch, tips program start)
- Month 2: 64% (tips program maturing, referrals launching)
- Month 3: 67% (all initiatives running, compounding effects)

Success criteria:
- Hit 67%: Full success
- 64-66%: Partial success (0.5-0.7 OKR score)
- <64%: Miss (requires post-mortem)

Review cadence:
- Weekly: Quality distribution trends
- Bi-weekly: Initiative progress review
- Month-end: Milestone assessment
- Trigger for revision: <1 point improvement per month
```

**Time to complete: 65 minutes**

## Goal Calibration Examples

### Example 1: Too Conservative
**Problem:**
- Current: 100K WAU, growing 3% monthly
- Target: 103K in 3 months (3% growth)
- Historical trend: Would hit this doing nothing

**Fix:**
- Ambitious target: 115K (15% growth = 5% monthly)
- Requires initiatives beyond business-as-usual
- Stretches team but achievable

### Example 2: Too Aggressive
**Problem:**
- Current: 100K WAU, growing 3% monthly
- Target: 200K in 3 months (100% growth)
- No clear path to doubling in 3 months

**Fix:**
- Reality-check: What's maximum with all initiatives?
- Maybe 125K (25% growth) if everything works
- Set 120K committed, 130K stretch

### Example 3: Well-Calibrated
**Problem:**
- Current: 100K WAU, growing 3% monthly
- Business-as-usual trajectory: 109K in 3 months
- Target: 120K (10% growth above baseline)

**Good because:**
- Requires planned initiatives to succeed
- Achievable with good execution
- Meaningful above baseline
- Team bought in

## Related Skills

This workflow orchestrates these skills:
- **north-star-alignment** (Step 1)
- **proxy-metric-selection** (Step 2)
- **tradeoff-evaluation** (Step 3)

## Related Workflows

- **metrics-definition**: Defines metrics before setting goals
- **dashboard-design**: Uses goals to set alert thresholds

## Time Estimate

**Total: 65-75 minutes**
- Step 1 (Company impact): 15 min
- Step 2 (Movability): 20 min
- Step 3 (Trade-offs): 20 min
- Step 4 (Final goal): 10 min

