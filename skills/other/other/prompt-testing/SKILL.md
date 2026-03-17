---
name: prompt-testing
description: A/B testing and performance metrics for prompts
allowed-tools: Read, Write, Bash
---

# Prompt Testing

Skill for testing, comparing, and measuring prompt performance.

## Documentation

- [metrics.md](docs/metrics.md) - Performance metrics definition
- [methodology.md](docs/methodology.md) - A/B testing protocol

## Testing Workflow

```text
1. DEFINE
   └── Test objective
   └── Metrics to measure
   └── Success criteria

2. PREPARE
   └── Variants A and B
   └── Test dataset
   └── Baseline (if existing)

3. EXECUTE
   └── Run on dataset
   └── Collect results
   └── Document observations

4. ANALYZE
   └── Calculate metrics
   └── Compare variants
   └── Identify patterns

5. DECIDE
   └── Recommendation
   └── Statistical confidence
   └── Next iterations
```

## Performance Metrics

### Quality

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Accuracy** | Correct responses | Correct / Total |
| **Compliance** | Format adherence | Compliant / Total |
| **Consistency** | Response stability | 1 - Variance |
| **Relevance** | Meeting the need | Average score (1-5) |

### Efficiency

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Tokens Input** | Prompt size | Token count |
| **Tokens Output** | Response size | Token count |
| **Latency** | Response time | ms |
| **Cost** | Price per request | Tokens × Price |

### Robustness

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **Edge Cases** | Edge case handling | Passed / Total |
| **Jailbreak Resist** | Bypass resistance | Blocked / Attempts |
| **Error Recovery** | Error recovery | Recovered / Errors |

## Test Format

### Test Dataset

```json
{
  "name": "Test Dataset v1",
  "description": "Dataset for testing prompt XYZ",
  "cases": [
    {
      "id": "case_001",
      "type": "standard",
      "input": "Test input",
      "expected": "Expected output",
      "tags": ["basic", "format"]
    },
    {
      "id": "case_002",
      "type": "edge_case",
      "input": "Edge input",
      "expected": "Expected behavior",
      "tags": ["edge", "error"]
    }
  ]
}
```

### Test Report

```markdown
# A/B Test Report: {{TEST_NAME}}

## Configuration

| Parameter | Value |
|-----------|-------|
| Date | {{DATE}} |
| Dataset | {{DATASET}} |
| Cases tested | {{N_CASES}} |
| Model | {{MODEL}} |

## Tested Variants

### Variant A (Baseline)
[Description or link to prompt A]

### Variant B (Challenger)
[Description or link to prompt B]

## Results

### Overall Scores

| Metric | A | B | Delta | Winner |
|--------|---|---|-------|--------|
| Accuracy | X% | Y% | +/-Z% | A/B |
| Compliance | X% | Y% | +/-Z% | A/B |
| Tokens | X | Y | +/-Z | A/B |
| Latency | Xms | Yms | +/-Zms | A/B |

### Detail by Case Type

| Type | A | B | Notes |
|------|---|---|-------|
| Standard | X% | Y% | |
| Edge cases | X% | Y% | |
| Error cases | X% | Y% | |

### Problematic Cases

| Case ID | Expected | A | B | Analysis |
|---------|----------|---|---|----------|
| case_XXX | ... | ❌ | ✅ | [Explanation] |

## Analysis

### B's Strengths
- [Improvement 1]
- [Improvement 2]

### B's Weaknesses
- [Regression 1]

### Observations
[Qualitative insights]

## Recommendation

**Verdict**: ✅ Adopt B / ⚠️ Iterate / ❌ Keep A

**Confidence**: High / Medium / Low

**Justification**:
[Explanation of recommendation]

## Next Steps
1. [Action 1]
2. [Action 2]
```

## Commands

```bash
# Create a test
/prompt test create --name "Test v1" --dataset tests.json

# Run an A/B test
/prompt test run --a prompt_a.md --b prompt_b.md --dataset tests.json

# View results
/prompt test results --id test_001

# Compare two tests
/prompt test compare --tests test_001,test_002
```

## Decision Criteria

### When to adopt variant B?

```text
IF:
  - Accuracy B >= Accuracy A
  AND (Tokens B <= Tokens A * 1.1 OR accuracy improvement > 5%)
  AND no regression on edge cases
THEN:
  → Adopt B

ELSE IF:
  - Accuracy improvement > 10%
  AND token regression < 20%
THEN:
  → Consider B (acceptable trade-off)

ELSE:
  → Keep A or iterate
```

## Best Practices

1. **Minimum 20 test cases** for significance
2. **Include edge cases** (15-20% of dataset)
3. **Test multiple runs** for consistency
4. **Document hypotheses** before testing
5. **Version the prompts** being tested
