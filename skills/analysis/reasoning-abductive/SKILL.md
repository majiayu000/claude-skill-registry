---
name: reasoning-abductive
description: Generate and evaluate explanatory hypotheses from incomplete observations. Use when diagnosing anomalies, explaining unexpected outcomes, or inferring causes from effects. Produces ranked hypotheses with evidence and confidence scores.
---

# Abductive Reasoning

Generate best explanations from observations. The logic of diagnosis and inference to cause.

## Type Signature

```
Abductive : Observation → Hypotheses[] → Evidence → BestExplanation

Where:
  Observation     : RawData × Surprise → AnomalyDescription
  Hypotheses      : AnomalyDescription → [PossibleCause]
  Evidence        : [PossibleCause] × AvailableData → [ScoredHypothesis]
  BestExplanation : [ScoredHypothesis] → (Cause × Confidence × NextSteps)
```

## When to Use

**Use abductive when:**
- Anomaly or surprise present (metric deviation, unexpected behavior)
- Need to explain an observation (why did X happen?)
- Incomplete data, must infer cause
- Diagnostic context (errors, issues, failures)
- Multiple possible explanations exist

**Don't use when:**
- Cause is already known (use causal execution instead)
- Need to compare decision alternatives
- Resolving stakeholder disagreements

## Four-Stage Process

### Stage 1: Observation

**Purpose:** Transform raw data into structured anomaly description.

**Input:**
```yaml
observation:
  raw_data: "Conversion dropped from 12% to 7% in Q4"
  context:
    timeframe: "Q4 2025"
    baseline: "12% historical average"
    current: "7% observed"
  surprise_level: 0.8  # How unexpected is this?
```

**Process:**
1. Quantify the deviation (% change, sigma from mean)
2. Identify temporal boundaries (when did it start?)
3. Scope the phenomenon (which segments affected?)
4. Rate surprise level (expected vs unexpected)

**Output:**
```yaml
anomaly:
  description: "42% drop in conversion rate (12% → 7%)"
  deviation: "-5 percentage points, -42% relative"
  temporal: "Started week 3 of Q4, persists through Q4"
  scope: "All segments equally affected"
  surprise: 0.8
  baseline_source: "12-month rolling average"
```

### Stage 2: Hypotheses Generation

**Purpose:** Generate diverse possible explanations without judgment.

**Rules:**
- Generate ≥5 hypotheses (more is better initially)
- Include obvious AND non-obvious causes
- Consider internal AND external factors
- Don't filter yet - cast wide net

**Hypothesis Categories:**

| Category | Examples |
|----------|----------|
| **Technical** | Site issues, bugs, performance |
| **Product** | Features, pricing, positioning |
| **Market** | Competition, trends, seasonality |
| **Operational** | Team changes, process issues |
| **External** | Economy, regulations, events |

**Output:**
```yaml
hypotheses:
  - id: H1
    cause: "Website performance degradation"
    category: technical
    mechanism: "Slow load times → abandonment"
    
  - id: H2
    cause: "Competitor launched aggressive pricing"
    category: market
    mechanism: "Price undercut → customer diversion"
    
  - id: H3
    cause: "Seasonal Q4 shopping behavior change"
    category: market
    mechanism: "Holiday spending patterns differ"
    
  - id: H4
    cause: "Product-market fit weakening"
    category: product
    mechanism: "Customer needs evolving away"
    
  - id: H5
    cause: "Sales qualification criteria changed"
    category: operational
    mechanism: "Different lead quality entering funnel"
    
  # ... continue until exhaustive
```

### Stage 3: Evidence Evaluation

**Purpose:** Score each hypothesis against available evidence.

**For each hypothesis, evaluate:**

| Criterion | Question | Score |
|-----------|----------|-------|
| **Explanatory power** | Does it fully explain the anomaly? | 0-1 |
| **Simplicity** | Fewest assumptions required? | 0-1 |
| **Coherence** | Consistent with other known facts? | 0-1 |
| **Testability** | Can we verify/falsify it? | 0-1 |
| **Prior probability** | How likely independent of this data? | 0-1 |

**Evidence Collection:**
```yaml
evidence:
  H1_technical:
    supporting:
      - "Page load time increased 2s in Q4" (confidence: 0.9)
      - "Mobile bounce rate up 15%" (confidence: 0.85)
    contradicting:
      - "Desktop conversion stable" (confidence: 0.8)
    net_score: 0.65
    
  H2_competitor:
    supporting:
      - "Competitor launched Oct 15" (confidence: 1.0)
      - "Google Trends shows competitor interest up" (confidence: 0.7)
    contradicting:
      - "Our traffic unchanged" (confidence: 0.9)
    net_score: 0.55
    
  # ... evaluate all hypotheses
```

**Scoring Formula:**
```
Score(H) = (Explanatory × 0.3) + (Simplicity × 0.2) + 
           (Coherence × 0.25) + (Testability × 0.1) + 
           (Prior × 0.15)
```

### Stage 4: Best Explanation

**Purpose:** Select most probable cause with confidence and next steps.

**Ranking:**
```yaml
ranked_hypotheses:
  - rank: 1
    hypothesis: H1
    cause: "Website performance degradation"
    score: 0.78
    confidence: 0.75
    
  - rank: 2
    hypothesis: H3
    cause: "Seasonal behavior change"
    score: 0.62
    confidence: 0.60
    
  - rank: 3
    hypothesis: H2
    cause: "Competitor pricing"
    score: 0.55
    confidence: 0.50
```

**Best Explanation Output:**
```yaml
conclusion:
  primary_cause: "Website performance degradation"
  confidence: 0.75
  mechanism: "2s increase in load time caused 42% more abandonment, 
              consistent with industry benchmarks (1s = ~7% conversion loss)"
  
  contributing_factors:
    - "Seasonal patterns may account for 10-15% of drop"
    
  ruled_out:
    - "Competitor pricing (traffic unchanged, not price-sensitive segment)"
    
  remaining_uncertainty:
    - "Whether mobile-specific or site-wide"
    - "Whether fix will fully restore conversion"
    
  next_steps:
    - "Verify: Run A/B test with performance fix (high priority)"
    - "Measure: Mobile vs desktop split post-fix"
    - "Monitor: Competitor activity (low priority)"
    
  suggested_next_mode: causal  # Ready to act on diagnosis
```

## Quality Gates

| Gate | Requirement | Failure Action |
|------|-------------|----------------|
| Hypothesis count | ≥5 hypotheses | Generate more before proceeding |
| Category diversity | ≥3 categories | Expand hypothesis search |
| Evidence present | ≥1 data point per top-3 | Gather more evidence |
| Confidence threshold | ≥0.6 for best | Flag as inconclusive |
| Testability | Best hypothesis testable | Propose test design |

## Common Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| **Anchoring** | First hypothesis gets all attention | Force diversity in Stage 2 |
| **Confirmation bias** | Only seek supporting evidence | Require contradicting evidence |
| **Complexity creep** | Elaborate explanations preferred | Weight simplicity appropriately |
| **Premature closure** | Stop at first plausible cause | Complete all 4 stages |

## Output Contract

```yaml
abductive_output:
  conclusion:
    primary_cause: string
    confidence: float  # 0.0-1.0
    mechanism: string  # How cause produces effect
    
  hypotheses:
    ranked: [ScoredHypothesis]  # All evaluated
    ruled_out: [string]         # Definitively excluded
    
  evidence:
    supporting: [EvidenceItem]
    contradicting: [EvidenceItem]
    gaps: [string]  # What evidence is missing?
    
  uncertainty:
    remaining_questions: [string]
    confidence_bounds: [float, float]  # Low, high
    
  next:
    immediate_actions: [string]
    tests_to_run: [string]
    suggested_mode: optional<ReasoningMode>
    
  trace:
    stages_completed: [1, 2, 3, 4]
    duration_ms: int
    hypotheses_generated: int
    evidence_points: int
```

## Example Execution

**Context:** "Enterprise conversion dropped 40% last quarter"

**Stage 1 - Observation:**
```
Anomaly: 40% drop (15% → 9%) in enterprise conversion
Temporal: Started week 5 of Q3, accelerated Q4
Scope: Enterprise only, SMB stable
Surprise: 0.85
```

**Stage 2 - Hypotheses:**
```
H1: Enterprise buyer behavior changed (economic uncertainty)
H2: Sales team restructuring disrupted relationships
H3: Competitor launched enterprise-specific offering
H4: Our enterprise pricing became uncompetitive
H5: Product gaps for enterprise use cases
H6: Longer sales cycles (not drop, just delay)
H7: Key account manager departures
```

**Stage 3 - Evidence:**
```
H1: Supporting (CFO involvement up 40%), Contradicting (overall enterprise IT spend flat)
H2: Supporting (3 senior reps left Q3), Contradicting (coverage maintained)
H6: Supporting (average cycle +45 days), Strong supporting
H7: Supporting (2 key AMs left), Moderate supporting
```

**Stage 4 - Conclusion:**
```
Primary: Sales cycle elongation (not true drop) + AM departures (relationship gaps)
Confidence: 0.72
Mechanism: Economic uncertainty extended CFO approval cycles by 45 days;
           AM departures created relationship gaps in 6 key accounts

Next: Wait 45 days to see if "delayed" deals close (causal monitoring)
      Immediately backfill AM roles (causal action)
```
