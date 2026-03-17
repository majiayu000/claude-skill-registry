---
name: priority-scoring
description: Use when ranking strategic options or roadmap items - applies weighted scoring formula (0.2×SignalStrength + 0.4×StrategicFit + 0.3×Impact - 0.1×Complexity) for consistent prioritization
---

# Priority Scoring

## Purpose

Apply consistent, objective scoring for roadmap sequencing and strategic comparisons:
- Standardized formula across all prioritization decisions
- Weighted scoring balancing signal strength, strategy, impact, and complexity
- Numerical rankings enabling roadmap sequencing
- Transparent methodology for stakeholder alignment

**Note:** PRDs use timeline-based prioritization rather than this scoring formula. This skill is primarily used for:
- Comparing strategic options
- Ranking backlog items for roadmap placement
- Strategy sessions evaluating trade-offs

## When to Use This Skill

Activate automatically when:
- `roadmap-updating` workflow sequences initiatives
- Strategy sessions evaluate option trade-offs
- User explicitly requests priority calculation
- Comparing competing features or initiatives

## Scoring Formula

**Standard formula:**
```
Priority Score = (0.2 × SignalStrength) + (0.4 × StrategicFit) + (0.3 × Impact) - (0.1 × Complexity)
```

**Component weights:**
- **SignalStrength (20%)**: Evidence from customers, partners, and internal teams
- **StrategicFit (40%)**: Alignment with current strategic priorities
- **Impact (30%)**: Expected influence on key business metrics
- **Complexity (10%, negative)**: Estimated difficulty and risk

**Score range:** 0.0 to 10.0 (higher = higher priority)

## Component Definitions

### 1. SignalStrength (0-10 scale)

**Definition**: Evidence quality and quantity supporting this item.

**Calculation:**
```
SignalStrength = (0.4 × CustomerScore) + (0.3 × RecencyScore) + (0.2 × DiversityScore) + (0.1 × FrequencyScore)
```

**CustomerScore (0-10):**
Based on unique customer/account mentions:
- 1 account: 3.0
- 2 accounts: 5.0
- 3 accounts: 7.0
- 4+ accounts: 9.0
- 6+ accounts: 10.0

**RecencyScore (0-10):**
Based on most recent mention:
- <7 days ago: 10.0
- 7-14 days ago: 8.0
- 14-30 days ago: 6.0
- 30-60 days ago: 4.0
- 60-90 days ago: 2.0
- >90 days ago: 1.0

**DiversityScore (0-10):**
Based on source type mix (customers, partners, internal functions):
- 1 source type: 4.0
- 2 source types: 7.0
- 3+ source types: 10.0

**FrequencyScore (0-10):**
Based on total mention count:
- 1-2 mentions: 3.0
- 3-5 mentions: 6.0
- 6-10 mentions: 8.0
- 11+ mentions: 10.0

### 2. StrategicFit (0-10 scale)

**Definition**: Alignment with current strategic priorities.

**Evaluation criteria:**

**High Strategic Fit (8-10):**
- Directly advances top-tier strategic goals
- Addresses core differentiators
- Supports primary growth vectors
- Enables strategic positioning

**Medium Strategic Fit (5-7):**
- Supports strategic goals indirectly
- Table-stakes feature (necessary but not differentiating)
- Addresses secondary growth vectors
- Competitive parity (match competitor features)

**Low Strategic Fit (1-4):**
- Tangential to current strategy
- One-off request not fitting larger themes
- Nice-to-have without strategic rationale
- Distracts from core priorities

**Scoring method:**
1. List current strategic priorities (from strategy memos, roadmap themes)
2. Assess item alignment with each priority
3. Score based on strength and breadth of alignment

### 3. Impact (0-10 scale)

**Definition**: Expected influence on key business metrics.

**Primary metrics:**
- Churn reduction
- Revenue growth / expansion
- Time-to-first-value (TTFV)
- User engagement / activation
- Customer satisfaction (NPS)

**Scoring tiers:**

**Transformative Impact (9-10):**
- 20%+ improvement in primary metric
- Addresses #1 churn reason or growth blocker
- Unlocks new market segment or revenue stream

**Significant Impact (7-8):**
- 10-20% improvement in primary metric
- Addresses top-3 churn reason or growth driver
- Measurable revenue or retention improvement

**Moderate Impact (5-6):**
- 5-10% improvement in primary metric
- Incremental improvement in satisfaction or engagement
- Small but measurable business impact

**Minor Impact (3-4):**
- <5% improvement
- Difficult to measure impact
- Improves experience but unclear business effect

**Minimal Impact (1-2):**
- No clear metric impact
- Pure convenience or polish
- Uncertain benefit

### 4. Complexity (0-10 scale, negative weight)

**Definition**: Estimated difficulty, time, and risk.

**Evaluation dimensions:**

**Technical Complexity:**
- Single system/surface: Low (2-3)
- Multiple systems: Medium (4-6)
- Cross-platform + integrations: High (7-8)
- Major architectural change: Very High (9-10)

**Time Estimate:**
- <1 week: Low (2)
- 1-2 weeks: Low-Medium (3-4)
- 2-4 weeks: Medium (5-6)
- 4-6 weeks: High (7-8)
- >6 weeks: Very High (9-10)

**Risk Level:**
- Well-understood, proven patterns: Low (2-3)
- Some unknowns, moderate dependencies: Medium (4-6)
- Many unknowns, high dependencies: High (7-8)
- Unproven approach, critical path: Very High (9-10)

**Complexity Score:**
```
Complexity = (0.4 × TechnicalComplexity) + (0.4 × TimeEstimate) + (0.2 × RiskLevel)
```

## Scoring Process

### 1. Load Item Data

**Required inputs:**
- Item title and description
- Signal data from meeting synthesis (if available):
  - Unique customer count
  - Mention count
  - Most recent mention date
  - Source diversity (customer/partner/internal)
- Strategic context (current priorities)
- Estimated time and complexity

### 2. Calculate Component Scores

Apply formulas for each component as defined above.

### 3. Apply Priority Formula

**Calculate:**
```
Priority Score = (0.2 × SignalStrength) + (0.4 × StrategicFit) + (0.3 × Impact) - (0.1 × Complexity)
```

**Round to one decimal place.**

### 4. Generate Scoring Report

**Output format:**
```markdown
# Priority Scoring Report

**Item**: {Title}

## Component Scores

**SignalStrength**: {score}/10
- Customer mentions: {N} accounts
- Most recent: {N} days ago
- Source diversity: {N} types
- Total mentions: {N}

**StrategicFit**: {score}/10
- Alignment assessment: {High/Medium/Low fit}

**Impact**: {score}/10
- Primary metric: {metric name}
- Expected improvement: {% or absolute}
- Impact tier: {Transformative/Significant/Moderate/Minor/Minimal}

**Complexity**: {score}/10 (negative weight)
- Technical complexity: {score}/10
- Time estimate: {weeks} weeks
- Risk level: {score}/10

## Final Priority Score

**{Final Score}/10**

**Interpretation**: {High/Medium/Low priority}
**Recommendation**: {Roadmap placement suggestion}
```

### 5. Rank Items

**When scoring multiple items:**
1. Calculate priority score for each
2. Sort by score (descending)
3. Group into priority tiers:
   - **High Priority** (8.0-10.0): Near-term roadmap
   - **Medium Priority** (5.0-7.9): Mid-term backlog
   - **Low Priority** (<5.0): Long-term or deferred

## Integration with Workflows

### Roadmap Updating Integration

**Invoked by:**
- `roadmap-updating` workflow

**Usage:**
- Re-score existing items when priorities shift
- Compare new items against existing roadmap
- Re-sequence based on updated scores

### Strategy Session Integration

**Invoked by:**
- `strategy-session` workflow (for option evaluation)

**Usage:**
- Score strategic alternatives
- Compare trade-offs numerically
- Support decision-making with objective criteria

## Success Criteria

Priority scoring complete when:
- All component scores calculated
- Formula applied correctly
- Final score rounded to one decimal
- Scoring report generated with rationale
- Item ranked relative to others (if batch scoring)

## Related Skills

- **meeting-synthesis**: Provides signal data for SignalStrength calculation
- **prd-validation**: Ensures PRDs meet quality standards
- **product-planning**: Uses priority context for roadmap sequencing

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "This feels higher priority" | Use formula, not gut feeling. |
| "Customer is important, boost score" | Formula already weighs customer signals. |
| "Complexity doesn't matter" | Complexity affects delivery, include it. |
| "Strategic fit is obvious" | Define and score against specific priorities. |
