---
name: calculate-priority-score
description: Calculate priority score for bugs, issues, or tasks based on severity, impact, and likelihood. Use for bug prioritization, task ordering, or risk assessment.
---

# Calculate Priority Score

Calculate numeric priority score and category for issues based on multiple factors.

## When to Use

- Bug prioritization
- Security vulnerability risk assessment
- Task ordering
- Resource allocation decisions

## Instructions

### Step 1: Receive Issue Attributes

Accept issue attributes as input.

**Expected Input**:

```json
{
  "severity": "critical|high|medium|low",
  "impact": "breaking|major|minor|none",
  "likelihood": "certain|likely|possible|unlikely"
}
```

### Step 2: Load Scoring Matrix

Use scoring matrix to assign points.

**Severity Scores**:

- critical: 10
- high: 7
- medium: 5
- low: 2

**Impact Scores**:

- breaking: 10
- major: 7
- minor: 3
- none: 0

**Likelihood Scores**:

- certain: 10
- likely: 7
- possible: 5
- unlikely: 2

### Step 3: Calculate Total Score

Sum all factor scores.

**Formula**: `score = severity + impact + likelihood`

**Range**: 0-30

### Step 4: Determine Priority Category

Map score to priority category.

**Priority Categories**:

- **P0 (Critical)**: 25-30
  - Label: "Critical - Immediate Action Required"
  - Action: Drop everything, fix now

- **P1 (High)**: 19-24
  - Label: "High - Fix This Sprint"
  - Action: Prioritize in current sprint

- **P2 (Medium)**: 12-18
  - Label: "Medium - Schedule for Next Sprint"
  - Action: Include in backlog, address soon

- **P3 (Low)**: 5-11
  - Label: "Low - Schedule When Convenient"
  - Action: Nice to have, low priority

- **P4 (Minimal)**: 0-4
  - Label: "Minimal - Consider Closing"
  - Action: May not be worth fixing

### Step 5: Return Scored Result

Return complete priority assessment.

**Expected Output**:

```json
{
  "score": 27,
  "category": "P0",
  "label": "Critical - Immediate Action Required",
  "factors": {
    "severity": 10,
    "impact": 10,
    "likelihood": 7
  },
  "recommendation": "Drop everything, fix now"
}
```

## Error Handling

- **Invalid Severity**: Return error listing valid values
- **Invalid Impact**: Return error listing valid values
- **Invalid Likelihood**: Return error listing valid values
- **Missing Factor**: Return error requesting all factors

## Examples

### Example 1: Critical Bug

**Input**:

```json
{
  "severity": "critical",
  "impact": "breaking",
  "likelihood": "certain"
}
```

**Output**:

```json
{
  "score": 30,
  "category": "P0",
  "label": "Critical - Immediate Action Required",
  "factors": {
    "severity": 10,
    "impact": 10,
    "likelihood": 10
  },
  "recommendation": "Drop everything, fix now"
}
```

### Example 2: Medium Priority Issue

**Input**:

```json
{
  "severity": "medium",
  "impact": "minor",
  "likelihood": "likely"
}
```

**Output**:

```json
{
  "score": 15,
  "category": "P2",
  "label": "Medium - Schedule for Next Sprint",
  "factors": {
    "severity": 5,
    "impact": 3,
    "likelihood": 7
  },
  "recommendation": "Include in backlog, address soon"
}
```

### Example 3: Low Priority Enhancement

**Input**:

```json
{
  "severity": "low",
  "impact": "minor",
  "likelihood": "unlikely"
}
```

**Output**:

```json
{
  "score": 7,
  "category": "P3",
  "label": "Low - Schedule When Convenient",
  "factors": {
    "severity": 2,
    "impact": 3,
    "likelihood": 2
  },
  "recommendation": "Nice to have, low priority"
}
```

### Example 4: High-Impact but Unlikely

**Input**:

```json
{
  "severity": "high",
  "impact": "breaking",
  "likelihood": "unlikely"
}
```

**Output**:

```json
{
  "score": 19,
  "category": "P1",
  "label": "High - Fix This Sprint",
  "factors": {
    "severity": 7,
    "impact": 10,
    "likelihood": 2
  },
  "recommendation": "Prioritize in current sprint"
}
```

## Validation

- [ ] Calculates score correctly
- [ ] Maps to correct priority category
- [ ] Handles all valid factor values
- [ ] Returns clear recommendations
- [ ] Validates input factors

## Supporting Files

- `scoring-matrix.json`: Factor scoring rules (see Supporting Files section)
