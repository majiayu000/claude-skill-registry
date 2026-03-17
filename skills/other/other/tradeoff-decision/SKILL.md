---
name: tradeoff-decision
description: Use when A/B tests show mixed results or features have conflicting metrics - evaluates net positive/negative through strategic alignment, explores mitigation strategies before binary rollback decisions
---

# Tradeoff Decision Workflow

## Purpose

Make informed ship/no-ship/iterate decisions when A/B test results are mixed (some metrics up, others down) or when a launched feature shows conflicting performance. Avoids binary thinking by exploring nuanced approaches that preserve gains while addressing losses.

## When to Use This Workflow

Use this workflow when:
- A/B test shows some metrics increasing, others decreasing
- Feature launched with mixed performance across different metrics
- Stakeholders disagree on whether to ship or rollback
- Redesign shifted user behavior in unexpected ways
- Need to choose between two good but mutually exclusive options
- Optimizing for one metric clearly harms another

## Skills Sequence

This workflow applies four skills systematically:

```
1. North Star Alignment
   ↓ (Determine which metric matters more strategically)
2. Trade-off Evaluation (Short vs. Long-term)
   ↓ (Assess temporal trade-offs)
3. Trade-off Evaluation (Mitigation)
   ↓ (Explore "best of both worlds" approaches)
4. Funnel-Based Metric Mapping
   ↓ (Identify where in user journey problem occurs)
   
OUTPUT: Assessment (net positive/negative/depends), 
        Recommended action (ship/rollback/iterate),
        Mitigation strategies, Risks
```

## Required Inputs

Gather this information before starting:

### Metric Changes
- **Metrics that increased**
  - Which metrics went up?
  - By how much (absolute and %)?
  - Statistical significance?

- **Metrics that decreased**
  - Which metrics went down?
  - By how much (absolute and %)?
  - Statistical significance?

### Context
- **Change description**
  - What was tested or launched?
  - What was the hypothesis?
  - How long has it been running?

- **Company strategic priorities**
  - What's most important to company now?
  - Growth, monetization, retention, competitive positioning?

- **User journey context**
  - Where in the funnel does change occur?
  - Which user behaviors shifted?

### Current State
- **Rollback feasibility**
  - Can we easily revert?
  - What's the cost of reverting?
  - How many users affected?

- **Iteration options**
  - Can we modify the change?
  - What variations could we test?
  - Timeline for iteration?

## Workflow Steps

### Step 1: Strategic Alignment Assessment (15 minutes)

**Use the `north-star-alignment` skill**

Determine which metric matters more to company strategy:

**Questions to answer:**

1. **Which metrics align with North Star?**
   - Do positive metrics connect to company-level goals?
   - Do negative metrics impact North Star metrics?

2. **Which metrics align with mission?**
   - Does change serve company mission?
   - Does it strengthen core value proposition?

3. **Which metrics drive long-term competitive advantage?**
   - Does change improve differentiation?
   - Does it strengthen market position?

4. **Which metrics feed important flywheels?**
   - Do positive metrics create virtuous cycles?
   - Do negative metrics break retention loops?

**Output:**

```markdown
## Strategic Alignment Assessment

**Metrics Aligned with Strategy:**
- [Metric that went up/down]: [Why strategically important]
- [Metric that went up/down]: [Why strategically important]

**Strategic Priority Ranking:**
1. [Most important metric]: [Rationale]
2. [Second priority]: [Rationale]
3. [Lower priority]: [Rationale]

**Mission Alignment:**
- Change serves mission: [Yes/No/Partially]
- Rationale: [Explanation]

**Competitive Positioning:**
- Strengthens positioning: [Yes/No/Mixed]
- Rationale: [Explanation]
```

### Step 2: Temporal Trade-off Analysis (15 minutes)

**Use the `tradeoff-evaluation` skill - Short vs. Long-term Framework**

Evaluate whether this is short-term gain/long-term loss or vice versa:

**Framework questions:**

1. **Short-term Impact (this quarter)**
   - Immediate revenue effect?
   - This quarter's growth?
   - Current user satisfaction?

2. **Long-term Impact (12+ months)**
   - User retention trajectory?
   - Flywheel effects?
   - Sustainable competitive advantage?
   - Brand and market position?

3. **Irreversibility Assessment**
   - Can we reverse course later if needed?
   - What becomes locked in?
   - What habits are we building?

**Apply Snapchat test:**
- Does this improve vanity metrics (time-on-site) while breaking engagement flywheel (messages/stories)?
- Are we optimizing for wrong thing?

**Output:**

```markdown
## Temporal Analysis

**Short-term (0-3 months):**
- Revenue impact: [Positive/Negative/Neutral - magnitude]
- Growth impact: [Positive/Negative/Neutral - magnitude]
- User satisfaction: [Positive/Negative/Neutral]

**Long-term (12+ months):**
- Retention impact: [Projected effect]
- Flywheel effects: [Strengthened/Weakened/Neutral]
- Competitive position: [Stronger/Weaker/Same]
- Strategic alignment: [High/Medium/Low]

**Trade-off Classification:**
- [Short-term gain, long-term loss] → Risky
- [Short-term loss, long-term gain] → Consider if affordable
- [Short-term gain, long-term gain] → Ship
- [Short-term loss, long-term loss] → Don't ship

**Recommendation based on temporal analysis:**
[Ship/Don't ship/Depends on mitigation]
```

### Step 3: Mitigation Strategy Exploration (20-30 minutes)

**Use the `tradeoff-evaluation` skill - Mitigation Framework**

Before deciding to rollback or ship as-is, explore "best of both worlds" options:

**Mitigation strategy categories:**

#### Strategy 1: Segmented Rollout

**When to use:** Impact varies by user segment

**Analysis:**
- Which segments show net positive?
- Which segments show net negative?
- Can we ship to positive segments only?

**Implementation:**
- Define segment criteria
- Rollout plan for positive segments
- Iteration plan for negative segments

#### Strategy 2: Feature Modification

**When to use:** Specific element causing harm

**Analysis:**
- Which specific change caused negative impact?
- Can we keep beneficial parts, modify harmful parts?
- What variations could preserve gains while fixing losses?

**Implementation:**
- Identify problematic component
- Design modified version
- A/B test: Original vs. Modified vs. Current

#### Strategy 3: Compensation Mechanisms

**When to use:** Trade-off is necessary but painful

**Analysis:**
- What complementary features could compensate?
- Can we create new paths to value?
- Can we boost other areas to offset loss?

**Implementation:**
- Identify compensation opportunities
- Parallel feature development
- Monitor net effect

#### Strategy 4: Gradual Rollout with Monitoring

**When to use:** Uncertain about long-term effects

**Analysis:**
- What could we learn from gradual rollout?
- What delayed effects might emerge?
- What monitoring would de-risk?

**Implementation:**
- 10% → 25% → 50% over weeks
- Maintain holdback group
- Set rollback trigger criteria

#### Strategy 5: Threshold-Based Approach

**When to use:** Acceptable within certain bounds

**Analysis:**
- What magnitude of negative impact is acceptable?
- What thresholds trigger concerns?
- Can we monitor and revert if crossed?

**Implementation:**
- Define acceptable thresholds
- Set up automated alerts
- Establish rollback criteria

**Output:**

```markdown
## Mitigation Strategies

### Evaluated Strategies:

**Strategy 1: [Name]**
- Approach: [Description]
- Preserves: [Positive metrics]
- Addresses: [Negative metrics]
- Feasibility: [Easy/Medium/Hard]
- Timeline: [How long to implement]
- Risks: [What could go wrong]

**Strategy 2: [Name]**
[Same structure]

**Strategy 3: [Name]**
[Same structure]

### Recommended Mitigation:
**[Strategy name]**
- Why: [Rationale]
- Implementation: [Specific steps]
- Success criteria: [How to know it worked]
- Fallback plan: [If mitigation fails]
```

### Step 4: Funnel Location Analysis (10 minutes)

**Use the `funnel-metric-mapping` skill**

Identify where in the user journey the trade-off occurs:

**Questions:**

1. **Which funnel stage is affected?**
   - Reach, Activation, Engagement, Retention?
   - Multiple stages?

2. **Is impact concentrated or distributed?**
   - Single point of friction?
   - Systemic shift across journey?

3. **Do metrics at different stages conflict?**
   - Earlier stage improved, later stage harmed?
   - Suggests optimization for wrong outcome

4. **What transitions are affected?**
   - Conversion rates between stages changed?
   - Drop-off points shifted?

**Output:**

```markdown
## Funnel Impact Analysis

**Affected stages:**
- [Stage name]: [Metric change description]
- [Stage name]: [Metric change description]

**Transition impacts:**
- [Stage A → Stage B]: [Conversion rate change]

**Concentration:**
- [Single point / Distributed across journey]

**Insights:**
- [What funnel analysis reveals about trade-off]
```

### Step 5: Make Recommendation (10 minutes)

Synthesize all analyses into clear recommendation:

**Decision options:**

1. **Ship Fully**
   - When: Net positive across segments, strategic alignment high
   - Action: Roll out to 100%
   - Monitoring: Track counter-metrics

2. **Ship to Segments**
   - When: Positive for some users, negative for others
   - Action: Roll out to net-positive segments
   - Plan: Iterate for problematic segments

3. **Iterate First**
   - When: Promising but needs modification
   - Action: Implement mitigation strategy
   - Timeline: Test modified version before full ship

4. **Gradual Rollout**
   - When: Uncertain about long-term effects
   - Action: Staged rollout with monitoring
   - Triggers: Rollback criteria defined

5. **Rollback**
   - When: Net negative, no clear mitigation, high risk
   - Action: Revert to previous state
   - Learning: Document why for future

**Recommendation document:**

```markdown
# Trade-off Decision: [Change Name]

## Executive Summary
[One paragraph: Metrics moved, strategic assessment, recommendation]

## Metric Changes
**Positive:**
- [Metric]: +X% ([why this matters])
- [Metric]: +X% ([why this matters])

**Negative:**
- [Metric]: -X% ([why this matters])
- [Metric]: -X% ([why this matters])

## Strategic Assessment (Step 1)
**Most important metric:** [Name]
**Rationale:** [Why strategically critical]
**Alignment:** [High/Medium/Low]

## Temporal Analysis (Step 2)
**Short-term:** [Net positive/negative]
**Long-term:** [Net positive/negative]
**Trade-off type:** [Classification]

## Mitigation Options (Step 3)
**Explored:**
1. [Strategy name]: [Feasibility]
2. [Strategy name]: [Feasibility]

**Recommended:** [Strategy name]

## Funnel Impact (Step 4)
**Affected stage:** [Stage name]
**Insight:** [What this reveals]

## Recommendation

**Decision:** [Ship Fully / Ship to Segments / Iterate First / Gradual / Rollback]

**Rationale:**
- [Point 1]
- [Point 2]
- [Point 3]

**Implementation:**
- Action: [Specific steps]
- Owner: [Name/team]
- Timeline: [When]
- Success criteria: [How to measure]

**Risks:**
- Risk 1: [Description + mitigation]
- Risk 2: [Description + mitigation]

**Monitoring Plan:**
- Metrics to track: [List]
- Review frequency: [Daily/Weekly]
- Rollback triggers: [Conditions that require revert]
- Responsible: [Name/team]

## Appendices
- A/B test results: [Detailed data]
- Segment analysis: [Breakdown]
- Stakeholder input: [Summary]
```

## Decision Matrix

Use this matrix for quick assessment:

| Strategic Alignment | Short-term | Long-term | Mitigation Feasible | Recommendation |
|---------------------|------------|-----------|---------------------|----------------|
| High | + | + | N/A | Ship Fully |
| High | + | - | Yes | Iterate First |
| High | + | - | No | Gradual with Monitoring |
| High | - | + | N/A | Ship if affordable |
| Low | + | - | Any | Rollback |
| Low | - | - | Any | Rollback |
| Mixed | Mixed | + | Yes | Iterate First |
| Mixed | Mixed | - | No | Rollback |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Binary thinking (ship or rollback only) | Explore mitigation strategies first |
| Not assessing strategic alignment | Start with North Star alignment |
| Ignoring long-term flywheel effects | Complete temporal analysis |
| Immediate rollback without diagnosis | Use metric-diagnosis first if root cause unclear |
| Treating all metrics as equal | Rank metrics by strategic importance |
| Not considering segmentation | Analyze by user segment |

## Success Criteria

Tradeoff decision succeeds when:
- Strategic alignment assessed (which metric matters more)
- Temporal trade-offs evaluated (short vs. long-term)
- 3-5 mitigation strategies explored
- Funnel impact analyzed
- Clear recommendation made with rationale
- Implementation plan defined
- Risks identified with mitigation plans
- Monitoring plan established
- Stakeholders aligned on decision

## Real-World Example: Snapchat Redesign

### Context
- Redesign launched: Separate social from media
- Time on site: ↑ 15%
- Messages sent: ↓ 12%
- Stories shared: ↓ 8%

### Step 1: Strategic Alignment (15 min)

**Questions:**
- Which metric aligns with Snapchat's strategic positioning?
- Camera/social app or content consumption app?

**Analysis:**
- **Content app positioning (time-on-site):**
  - Market saturated (TikTok, YouTube, Instagram)
  - Not core competency
  - Short-term thinking

- **Social/camera app positioning (messages/stories):**
  - Unique value proposition
  - Core competency
  - Sustainable competitive advantage

**Conclusion:** Messages and stories strategically more important than time-on-site

### Step 2: Temporal Analysis (15 min)

**Short-term (this quarter):**
- Revenue: Positive (more ads shown with higher time-on-site)
- Growth: Neutral
- User satisfaction: Mixed (some like creators, some miss social)

**Long-term (12 months):**
- Retention: Negative risk (broken social flywheel)
  - Fewer stories → Fewer notifications → Less app opening
  - Fewer messages → Less reciprocal engagement
- Flywheel: Weakened critical loop
- Competitive position: Confused (competing with TikTok in saturated market)

**Classification:** Short-term gain (time/ads), long-term loss (retention/flywheel)

**Assessment:** Net negative

### Step 3: Mitigation Strategies (25 min)

**Strategy 1: Immediate Rollback**
- Pros: Restores social flywheel quickly
- Cons: Loses time-on-site gains, admits failure
- Feasibility: Easy

**Strategy 2: Targeted Modifications**
- Approach: Keep creator content but re-integrate friend stories
- Implementation:
  - Show friend stories in creator tab
  - Add "message friend" prompts after content viewing
  - Balance algorithm between creator and friend content
- Preserves: Time-on-site gains
- Addresses: Social engagement losses
- Feasibility: Medium complexity, 4-6 weeks

**Strategy 3: Segmented Experience**
- Heavy social users: Friend-focused interface
- Content consumers: Creator-focused interface
- Feasibility: Complex, 8-12 weeks

**Recommended:** Strategy 2 (Targeted Modifications)
- Best balance of preserving gains and fixing losses
- Reasonable timeline
- Testable before full rollout

### Step 4: Funnel Analysis (10 min)

**Affected stages:**
- Engagement (Depth): Messages and stories down (core actions)
- Engagement (Breadth): Time on site up (passive consumption)

**Insight:**
- Optimizing breadth at expense of depth
- Depth drives retention flywheel, breadth doesn't
- Classic mistake: Vanity metric over strategic metric

### Step 5: Recommendation (10 min)

**Decision: Iterate First** (Don't immediately rollback, don't keep as-is)

**Rationale:**
1. Clear strategic importance of social metrics
2. Long-term retention risk outweighs short-term revenue gain
3. Feasible mitigation strategy exists
4. Can preserve some gains while fixing critical issue

**Implementation:**
- Action: Implement targeted modifications (Strategy 2)
- Owner: Product team + Design
- Timeline: 4-6 weeks for modified version
- Success criteria:
  - Messages sent: Recover to within 5% of baseline
  - Stories shared: Recover to within 5% of baseline
  - Time on site: Maintain at least 50% of gains

**Risks:**
- Risk: Modifications don't fix social engagement
  - Mitigation: Full rollback if metrics don't improve in 30 days
- Risk: Lose all time-on-site gains
  - Mitigation: Acceptable trade-off for strategic alignment

**Monitoring:**
- Daily: Messages, stories, time-on-site
- Weekly: Full funnel review
- Rollback trigger: If messages/stories drop further 5%

**Timeline: 90 minutes for full analysis**

## Related Skills

This workflow orchestrates these skills:
- **north-star-alignment** (Step 1)
- **tradeoff-evaluation** (Steps 2-3)
- **funnel-metric-mapping** (Step 4)

## Related Workflows

- **metric-diagnosis**: Use first if root cause of metric changes unclear
- **metrics-definition**: Defines counter-metrics to detect trade-offs early
- **dashboard-design**: Monitors trade-offs through balanced metric sets

## Time Estimate

**Total: 70-90 minutes**
- Step 1 (Strategic alignment): 15 min
- Step 2 (Temporal analysis): 15 min
- Step 3 (Mitigation): 20-30 min
- Step 4 (Funnel analysis): 10 min
- Step 5 (Recommendation): 10 min

