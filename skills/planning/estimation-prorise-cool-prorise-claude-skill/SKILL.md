---
name: estimation
description: Estimation techniques including analogous, parametric, three-point, and expert judgment methods. Provides effort, cost, duration, and complexity estimates for projects, features, and tasks.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Estimation

## When to Use This Skill

Use this skill when:

- **Estimation tasks** - Working on estimation techniques including analogous, parametric, three-point, and expert judgment methods. provides effort, cost, duration, and complexity estimates for projects, features, and tasks
- **Planning or design** - Need guidance on Estimation approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Systematically estimate effort, cost, duration, and complexity using proven estimation techniques. Supports analogous, parametric, three-point (PERT), and expert judgment methods for projects, features, and tasks.

## What is Estimation?

**Estimation** is the process of forecasting the resources, time, and cost required to complete work. Good estimation balances:

- **Accuracy**: How close to actual results
- **Precision**: Consistency of estimates
- **Speed**: Time to produce estimates
- **Communication**: Shared understanding of uncertainty

### Estimation vs Commitment

| Concept | Definition | Use |
|---------|------------|-----|
| **Estimate** | Best guess given current knowledge | Planning, forecasting |
| **Commitment** | Promise to deliver by date/cost | Contracts, deadlines |
| **Target** | Desired outcome to aim for | Goals, objectives |

**Key principle:** Estimates are ranges with uncertainty, not single-point guarantees.

## Estimation Techniques

### Analogous Estimation (Top-Down)

Estimate based on similar past work:

| Step | Action |
|------|--------|
| 1 | Identify similar completed project/feature |
| 2 | Retrieve actual effort/cost/duration |
| 3 | Adjust for differences (complexity, team, technology) |
| 4 | Apply adjustment factor |

**Formula:**

```text
New Estimate = Historical Actual × Adjustment Factor

Example:
Similar project took 200 hours
New project is ~20% more complex
Estimate = 200 × 1.20 = 240 hours
```

**When to Use:** Early phases, limited detail, experienced teams with historical data

**Accuracy:** +/- 25-50% (improves with good historical data)

### Parametric Estimation

Estimate using statistical relationships:

| Element | Description |
|---------|-------------|
| **Unit of Work** | Measurable element (screen, API, table) |
| **Productivity Rate** | Effort per unit from historical data |
| **Quantity** | Number of units to produce |

**Formula:**

```text
Estimate = Quantity × Productivity Rate

Example:
10 API endpoints × 16 hours/endpoint = 160 hours
```

**Common Productivity Metrics:**

| Work Type | Metric | Typical Range |
|-----------|--------|---------------|
| UI screens | Hours/screen | 8-40 hours |
| API endpoints | Hours/endpoint | 4-24 hours |
| Database tables | Hours/table | 4-16 hours |
| Test cases | Hours/test | 0.5-4 hours |
| Documentation pages | Hours/page | 2-8 hours |

**When to Use:** Repeatable work, good historical data, similar technology

**Accuracy:** +/- 15-25% (with calibrated rates)

### Three-Point Estimation (PERT)

Estimate using optimistic, most likely, and pessimistic values:

| Value | Symbol | Definition |
|-------|--------|------------|
| **Optimistic** | O | Best case, everything goes right |
| **Most Likely** | M | Most probable outcome |
| **Pessimistic** | P | Worst case, problems occur |

**PERT Formula (Weighted Average):**

```text
Expected = (O + 4M + P) / 6
Standard Deviation = (P - O) / 6

Example:
O = 5 days, M = 8 days, P = 17 days
Expected = (5 + 4×8 + 17) / 6 = 9 days
Std Dev = (17 - 5) / 6 = 2 days
```

**Confidence Intervals:**

| Confidence | Calculation | Example (E=9, SD=2) |
|------------|-------------|---------------------|
| 68% | E ± 1 SD | 7-11 days |
| 95% | E ± 2 SD | 5-13 days |
| 99.7% | E ± 3 SD | 3-15 days |

**When to Use:** Uncertain work, new technology, need to communicate risk

**Accuracy:** Provides explicit uncertainty range

### Expert Judgment

Estimate using collective expert knowledge:

**Wideband Delphi Process:**

| Round | Activity |
|-------|----------|
| 1 | Experts estimate independently |
| 2 | Collect and share anonymous estimates |
| 3 | Discuss high/low outliers, share rationale |
| 4 | Re-estimate independently |
| 5 | Repeat until convergence (or average) |

**Planning Poker (Agile):**

| Step | Action |
|------|--------|
| 1 | Present item to estimate |
| 2 | Discuss briefly (2-5 minutes) |
| 3 | Each team member selects card privately |
| 4 | Reveal simultaneously |
| 5 | Discuss outliers |
| 6 | Re-vote until consensus |

**Common Scales:**

| Scale Type | Values |
|------------|--------|
| Fibonacci | 1, 2, 3, 5, 8, 13, 21, 34, 55, 89 |
| Modified Fibonacci | 0, 0.5, 1, 2, 3, 5, 8, 13, 20, 40, 100 |
| T-shirt | XS, S, M, L, XL, XXL |
| Powers of 2 | 1, 2, 4, 8, 16, 32, 64 |

**When to Use:** Complex work, multiple perspectives needed, team alignment

### Function Point Analysis

Estimate based on functional size (for larger systems):

| Component | Description | Weight Range |
|-----------|-------------|--------------|
| External Inputs | Data entering system | 3-6 |
| External Outputs | Data leaving system | 4-7 |
| External Inquiries | Read-only queries | 3-6 |
| Internal Files | Logical data stores | 7-15 |
| External Interfaces | Shared data | 5-10 |

**Process:**

1. Count each component type
2. Classify complexity (low/medium/high)
3. Apply weights
4. Calculate unadjusted function points
5. Apply technical complexity factor

**When to Use:** Large projects, formal contracts, industry benchmarking

## Relative Estimation

### Story Points

Relative complexity/effort measure:

| Points | Relative Size | Example |
|--------|---------------|---------|
| 1 | Trivial | Fix typo, config change |
| 2 | Simple | Simple bug fix, minor feature |
| 3 | Moderate | Standard feature, moderate complexity |
| 5 | Complex | Multi-component feature |
| 8 | Very complex | Integration work, significant unknowns |
| 13 | Epic-sized | Consider breaking down |
| 21+ | Too large | Must decompose |

**Baseline:** Pick a well-understood story as reference (e.g., "this is a 3")

**Velocity:** Story points completed per iteration (used for forecasting)

### T-Shirt Sizing

Quick relative sizing for roadmap planning:

| Size | Effort Range | Duration Range |
|------|--------------|----------------|
| XS | 1-4 hours | < 1 day |
| S | 0.5-2 days | 1-2 days |
| M | 2-5 days | 3-5 days |
| L | 1-2 weeks | 1-2 weeks |
| XL | 2-4 weeks | 2-4 weeks |
| XXL | 1-3 months | Too big, decompose |

## Workflow

### Phase 1: Prepare

#### Step 1: Clarify Scope

```markdown
## Estimation Request

**Item:** [What's being estimated]
**Requester:** [Who needs the estimate]
**Purpose:** [Planning/budgeting/commitment]
**Deadline:** [When estimate is needed]
**Precision:** [ROM/Budget/Definitive]

### Scope Definition

- **In Scope:** [What's included]
- **Out of Scope:** [What's excluded]
- **Assumptions:** [Key assumptions]
- **Constraints:** [Known constraints]
```

#### Step 2: Select Estimation Technique

| Situation | Recommended Technique |
|-----------|----------------------|
| Early project phase | Analogous + T-shirt sizing |
| Detailed requirements | Parametric + Three-point |
| Agile backlog | Story points + Planning poker |
| New technology/domain | Expert judgment + Three-point |
| Contract/budget | Function points + Parametric |

### Phase 2: Estimate

#### Step 1: Decompose Work

Break down into estimable units (half-day to 2-week chunks)

#### Step 2: Apply Technique

Use selected technique(s) from above

#### Step 3: Add Contingency

```markdown
## Contingency Calculation

| Risk Level | Contingency | When to Use |
|------------|-------------|-------------|
| Low | 10-15% | Well-understood, experienced team |
| Medium | 20-30% | Some unknowns, new team members |
| High | 40-50% | Significant unknowns, new technology |
| Very High | 75-100% | Research, innovation, first-of-kind |
```

#### Step 4: Validate

- Sanity check against similar work
- Review with team
- Check for missing items
- Verify assumptions

### Phase 3: Communicate

#### Step 1: Express as Range

```markdown
## Estimate Summary

**Effort:** 160-200 hours (confidence: 80%)
**Duration:** 4-5 weeks (with 2 developers)
**Cost:** $24,000-$30,000

**Key Risks:**
- API integration complexity unknown
- Dependency on third-party availability
```

#### Step 2: Document Assumptions

```markdown
## Estimation Assumptions

1. Requirements are stable and complete
2. Team has 80% availability (20% overhead)
3. No major technology changes
4. Dependencies delivered on time
5. [Additional assumptions...]

**If assumptions change, estimate should be revisited.**
```

## Output Formats

### Narrative Summary

```markdown
## Estimation Summary

**Item:** [Feature/Project name]
**Date:** [ISO date]
**Estimator:** estimation-analyst
**Technique:** [Technique used]

### Estimate

| Dimension | Low | Expected | High | Confidence |
|-----------|-----|----------|------|------------|
| Effort | 120h | 160h | 220h | 80% |
| Duration | 4w | 5w | 7w | 80% |
| Cost | $18K | $24K | $33K | 80% |

### Basis of Estimate

- **Historical Reference:** [Similar past work]
- **Productivity Rate:** [If parametric]
- **Expert Input:** [Who contributed]

### Assumptions

1. [Assumption 1]
2. [Assumption 2]

### Risks Affecting Estimate

| Risk | Impact on Estimate |
|------|-------------------|
| [Risk 1] | +20% if occurs |
| [Risk 2] | +15% if occurs |

### Recommendations

1. [Next steps for refining estimate]
2. [When to re-estimate]
```

### Structured Data (YAML)

```yaml
estimation:
  version: "1.0"
  date: "2025-01-15"
  item: "User Dashboard Feature"
  estimator: "estimation-analyst"
  technique: "three_point"

  scope:
    description: "Interactive user dashboard with analytics"
    in_scope:
      - "Dashboard UI components"
      - "Data visualization"
      - "User preferences"
    out_of_scope:
      - "Backend analytics engine"
      - "Real-time updates"
    assumptions:
      - "API endpoints available"
      - "Design mockups complete"

  estimates:
    effort:
      optimistic: 120
      most_likely: 160
      pessimistic: 240
      expected: 166
      unit: "hours"
      std_deviation: 20
    duration:
      optimistic: 3
      most_likely: 4
      pessimistic: 6
      expected: 4.2
      unit: "weeks"
    cost:
      expected: 24000
      range_low: 18000
      range_high: 36000
      currency: "USD"

  confidence: 0.80
  contingency: 0.20

  breakdown:
    - component: "UI Components"
      effort: 60
      technique: "parametric"
      rate: "15h/component"
      quantity: 4
    - component: "Data Integration"
      effort: 40
      technique: "analogous"
      reference: "PROJ-123"
    - component: "Testing"
      effort: 40
      technique: "percentage"
      percentage: 0.25

  risks:
    - risk: "API complexity higher than expected"
      probability: 0.3
      impact_hours: 30
    - risk: "Design changes during development"
      probability: 0.2
      impact_hours: 20

  historical_comparison:
    similar_item: "Admin Dashboard"
    actual_effort: 180
    adjustment_factor: 0.9
```

### Breakdown Table

```markdown
## Effort Breakdown

| Component | Technique | Estimate | Contingency | Total |
|-----------|-----------|----------|-------------|-------|
| UI Components | Parametric | 60h | 12h | 72h |
| Data Integration | Analogous | 40h | 10h | 50h |
| Testing | % of Dev | 40h | 8h | 48h |
| Documentation | Parametric | 16h | 4h | 20h |
| **Subtotal** | | **156h** | **34h** | **190h** |
| Management Overhead | 10% | | | 19h |
| **Total** | | | | **209h** |
```

## Estimation Accuracy

### Cone of Uncertainty

Estimate accuracy improves as project progresses:

| Phase | Accuracy Range |
|-------|----------------|
| Initial concept | 0.25x - 4x |
| Approved project | 0.5x - 2x |
| Requirements complete | 0.67x - 1.5x |
| Detailed design | 0.8x - 1.25x |
| Code complete | 0.9x - 1.1x |

**Implication:** Early estimates need wider ranges; refine as knowledge grows.

### Estimation Levels

| Level | Accuracy | When Used |
|-------|----------|-----------|
| **ROM** (Rough Order of Magnitude) | -25% to +75% | Initial budgeting |
| **Budget** | -10% to +25% | Project approval |
| **Definitive** | -5% to +10% | Execution baseline |

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Single-point estimates | Always provide ranges |
| Optimism bias | Use historical data, add contingency |
| Anchoring | Estimate before seeing others' estimates |
| Planning fallacy | Include realistic overhead and risks |
| Scope creep | Document assumptions, re-estimate on changes |
| Precision theater | Match precision to actual knowledge |

## Integration

### Upstream

- **Requirements** - What to estimate
- **risk-analysis** - Risks affecting estimates
- **stakeholder-analysis** - Who needs estimates, precision required

### Downstream

- **Project planning** - Resource allocation, scheduling
- **Budgeting** - Cost forecasting
- **prioritization** - Cost input for value/effort analysis

## Related Skills

- `risk-analysis` - Risks affecting estimates
- `prioritization` - Using estimates for prioritization
- `decision-analysis` - Trade-off decisions
- `value-stream-mapping` - Estimating process improvement effort

## Version History

- **v1.0.0** (2025-12-26): Initial release
