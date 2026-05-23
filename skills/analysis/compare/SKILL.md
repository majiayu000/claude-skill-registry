---
name: compare
description: Compare multiple alternatives using explicit criteria, weighted scoring, and tradeoff analysis. Use when choosing between options, evaluating alternatives, or making decisions.
argument-hint: "[options] [criteria] [weights]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Systematically evaluate multiple alternatives against defined criteria to produce a recommendation with transparent tradeoff analysis. Comparison enables informed decision-making through structured analysis.

**Success criteria:**
- All options evaluated against same criteria
- Criteria weighted by importance
- Clear recommendation with rationale
- Tradeoffs explicitly documented

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `options` | Yes | array[string\|object] | Alternatives to compare (2+ items) |
| `criteria` | Yes | array[string\|object] | Evaluation dimensions with optional weights |
| `context` | No | object | Constraints, priorities, or decision context |
| `must_have` | No | array[string] | Required criteria (eliminates options that fail) |

## Procedure

1) **Enumerate options**: List all alternatives under consideration
   - Verify each option is viable (not obviously invalid)
   - Ensure options are at same abstraction level
   - Flag if options are not mutually exclusive

2) **Define criteria**: Establish evaluation dimensions
   - Quantitative criteria: measurable (cost, time, size)
   - Qualitative criteria: assessed (quality, maintainability, risk)
   - Apply must_have filters to eliminate non-viable options

3) **Assign weights**: Determine relative importance of each criterion
   - Weights should sum to 1.0
   - If not provided, use equal weights
   - Document rationale for weight assignments

4) **Score each option**: Evaluate options against criteria
   - Quantitative: normalize to 0-1 scale
   - Qualitative: rate as 0.0 (poor) to 1.0 (excellent)
   - Document evidence for each score

5) **Calculate weighted scores**: Aggregate criteria scores
   - weighted_score = sum(criterion_score * criterion_weight)
   - Rank options by weighted score

6) **Analyze tradeoffs**: Document what each choice sacrifices
   - Identify criteria where top choice is not best
   - Quantify the gap between options on key criteria

7) **Formulate recommendation**: Propose choice with rationale
   - May recommend conditionally based on priorities
   - Flag if options are too close to distinguish

8) **Ground claims**: Attach evidence anchors to scores and analysis

## Output Contract

Return a structured object:

```yaml
options:
  - id: string  # Option identifier
    summary: string  # Brief description
criteria:
  - name: string  # Criterion name
    weight: number  # 0.0-1.0 importance weight
    type: quantitative | qualitative
comparison_matrix:
  - option_id: string
    scores:
      - criterion: string
        score: number  # 0.0-1.0 normalized score
        rationale: string  # Why this score
recommendation:
  choice: string  # Recommended option ID
  rationale: string  # Why this option
  confidence: number  # 0.0-1.0 in recommendation
tradeoffs:
  - option: string
    pros: array[string]
    cons: array[string]
confidence: number  # 0.0-1.0 overall comparison confidence
evidence_anchors: array[string]  # References to data sources
assumptions: array[string]  # Conditions affecting comparison
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `options` | array | List of alternatives with summaries |
| `criteria` | array | Evaluation dimensions with weights |
| `comparison_matrix` | array | Scores for each option on each criterion |
| `recommendation` | object | Proposed choice with confidence |
| `tradeoffs` | array | Pros/cons for each option |
| `confidence` | number | 0.0-1.0 overall analysis confidence |
| `evidence_anchors` | array[string] | References supporting scores |
| `assumptions` | array[string] | Conditions that could change outcome |

## Examples

### Example 1: Compare Database Options

**Input:**
```yaml
options:
  - id: "postgres"
    summary: "PostgreSQL relational database"
  - id: "mongodb"
    summary: "MongoDB document database"
  - id: "dynamodb"
    summary: "AWS DynamoDB managed service"
criteria:
  - name: "query_flexibility"
    weight: 0.3
  - name: "operational_overhead"
    weight: 0.25
  - name: "cost_at_scale"
    weight: 0.25
  - name: "team_familiarity"
    weight: 0.2
context:
  workload: "mixed read/write"
  scale: "10M records"
  team_size: 3
```

**Output:**
```yaml
options:
  - id: "postgres"
    summary: "PostgreSQL relational database with JSONB support"
  - id: "mongodb"
    summary: "MongoDB document database with flexible schema"
  - id: "dynamodb"
    summary: "AWS DynamoDB fully managed NoSQL"
criteria:
  - name: "query_flexibility"
    weight: 0.3
    type: qualitative
  - name: "operational_overhead"
    weight: 0.25
    type: qualitative
  - name: "cost_at_scale"
    weight: 0.25
    type: quantitative
  - name: "team_familiarity"
    weight: 0.2
    type: qualitative
comparison_matrix:
  - option_id: "postgres"
    scores:
      - criterion: "query_flexibility"
        score: 0.95
        rationale: "Full SQL + JSONB queries, complex joins supported"
      - criterion: "operational_overhead"
        score: 0.6
        rationale: "Requires backup, replication, tuning expertise"
      - criterion: "cost_at_scale"
        score: 0.7
        rationale: "~$500/mo for 10M records on RDS"
      - criterion: "team_familiarity"
        score: 0.9
        rationale: "All 3 engineers have 3+ years PostgreSQL experience"
  - option_id: "mongodb"
    scores:
      - criterion: "query_flexibility"
        score: 0.75
        rationale: "Good document queries, limited joins"
      - criterion: "operational_overhead"
        score: 0.7
        rationale: "Atlas reduces ops burden, but sharding is complex"
      - criterion: "cost_at_scale"
        score: 0.6
        rationale: "~$700/mo for 10M records on Atlas"
      - criterion: "team_familiarity"
        score: 0.4
        rationale: "1 engineer with production MongoDB experience"
  - option_id: "dynamodb"
    scores:
      - criterion: "query_flexibility"
        score: 0.4
        rationale: "Limited query patterns, requires careful data modeling"
      - criterion: "operational_overhead"
        score: 0.95
        rationale: "Fully managed, auto-scaling, zero maintenance"
      - criterion: "cost_at_scale"
        score: 0.75
        rationale: "~$400/mo with on-demand pricing"
      - criterion: "team_familiarity"
        score: 0.3
        rationale: "No team experience with DynamoDB"
recommendation:
  choice: "postgres"
  rationale: "Highest weighted score (0.79) driven by query flexibility and team familiarity. Operational overhead is manageable with RDS."
  confidence: 0.8
tradeoffs:
  - option: "postgres"
    pros:
      - "Most flexible query capabilities"
      - "Team already proficient"
      - "Strong ecosystem and tooling"
    cons:
      - "Highest operational overhead"
      - "Requires capacity planning"
  - option: "mongodb"
    pros:
      - "Flexible document model"
      - "Good middle ground on ops"
    cons:
      - "Team learning curve"
      - "Higher cost than alternatives"
  - option: "dynamodb"
    pros:
      - "Zero operational burden"
      - "Lowest cost at scale"
    cons:
      - "Significant team ramp-up needed"
      - "Query pattern limitations"
confidence: 0.85
evidence_anchors:
  - "aws:pricing-calculator:dynamodb"
  - "mongodb:atlas-pricing:m30"
  - "team_survey:db_experience:2024"
assumptions:
  - "Workload remains mixed read/write"
  - "No need for global distribution initially"
  - "Team composition stable for 6+ months"
```

**Evidence pattern:** Read pricing documentation, survey team skills, analyze workload patterns.

---

### Example 2: Compare Refactoring Approaches

**Input:**
```yaml
options:
  - "incremental refactoring"
  - "complete rewrite"
  - "strangler fig pattern"
criteria:
  - name: "risk"
    weight: 0.4
  - name: "time_to_value"
    weight: 0.35
  - name: "final_quality"
    weight: 0.25
must_have:
  - "maintains production uptime"
```

**Output:**
```yaml
options:
  - id: "incremental"
    summary: "Gradual refactoring while maintaining existing system"
  - id: "rewrite"
    summary: "Complete rebuild from scratch"
  - id: "strangler"
    summary: "Progressively replace components behind abstraction"
criteria:
  - name: "risk"
    weight: 0.4
    type: qualitative
  - name: "time_to_value"
    weight: 0.35
    type: qualitative
  - name: "final_quality"
    weight: 0.25
    type: qualitative
comparison_matrix:
  - option_id: "incremental"
    scores:
      - criterion: "risk"
        score: 0.85
        rationale: "Small changes, easy rollback"
      - criterion: "time_to_value"
        score: 0.7
        rationale: "Continuous improvement, but slow overall"
      - criterion: "final_quality"
        score: 0.6
        rationale: "May accumulate tech debt from compromises"
  - option_id: "rewrite"
    scores:
      - criterion: "risk"
        score: 0.3
        rationale: "Big bang cutover, high failure risk"
      - criterion: "time_to_value"
        score: 0.2
        rationale: "No value until complete"
      - criterion: "final_quality"
        score: 0.9
        rationale: "Clean slate, optimal design"
  - option_id: "strangler"
    scores:
      - criterion: "risk"
        score: 0.75
        rationale: "Component-level risk, rollback per component"
      - criterion: "time_to_value"
        score: 0.8
        rationale: "Each component delivers value"
      - criterion: "final_quality"
        score: 0.8
        rationale: "Good design with some integration overhead"
recommendation:
  choice: "strangler"
  rationale: "Best balance of risk and time-to-value (0.78 weighted score). Delivers incremental value while achieving good final quality."
  confidence: 0.75
tradeoffs:
  - option: "strangler"
    pros:
      - "Incremental value delivery"
      - "Manageable risk"
    cons:
      - "Abstraction layer overhead"
      - "Longer total timeline than rewrite"
confidence: 0.8
evidence_anchors:
  - "fowler:strangler-fig-pattern"
  - "internal:outage-report:2024-q3"
assumptions:
  - "Team can maintain abstraction discipline"
  - "System is decomposable into components"
```

## Verification

- [ ] All options evaluated against all criteria
- [ ] Criterion weights sum to 1.0
- [ ] All scores are in 0.0-1.0 range with rationale
- [ ] Recommendation aligns with highest weighted score
- [ ] Tradeoffs identify criteria where recommendation is not best
- [ ] must_have criteria properly filtered options

**Verification tools:** Manual review of scoring rationale, stakeholder validation

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Require at least 2 options for comparison
- Document evidence for all scores, not just final recommendation
- Flag when options are within margin of error (< 0.1 weighted score difference)
- Do not hide tradeoffs to favor a recommendation

## Composition Patterns

**Commonly follows:**
- `identify` - Compare identified alternatives
- `estimate` - Use estimates as comparison inputs
- `forecast` - Compare based on forecasted outcomes
- `discover` - Compare discovered options

**Commonly precedes:**
- `plan` - Comparison informs action planning
- `generate` - Generate solution based on chosen option
- `act` - Implement chosen option

**Anti-patterns:**
- Never compare without explicit criteria (biased comparison)
- Avoid comparison with single option (not a real comparison)
- Do not use compare for simple existence checking (use `detect`)

**Workflow references:**
- See `reference/composition_patterns.md#capability-gap-analysis` for compare-plans usage
- See `reference/composition_patterns.md#observe-model-act` for comparison in decision loops
