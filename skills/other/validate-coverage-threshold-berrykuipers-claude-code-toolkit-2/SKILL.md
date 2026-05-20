---
name: validate-coverage-threshold
description: Validate test coverage meets minimum thresholds for overall, statement, branch, and function coverage
---

# Validate Coverage Threshold

## Purpose

Parse test coverage reports and validate that coverage meets minimum thresholds, blocking commits or PRs if coverage is insufficient.

## When to Use

- Quality gate validation
- After running tests with coverage
- Pre-commit checks
- Conductor Phase 3 (Quality Assurance)
- As part of `quality-gate` skill

## Default Thresholds

```json
{
  "overall": 80,
  "statements": 80,
  "branches": 75,
  "functions": 80
}
```

## Instructions

### Step 1: Check Coverage Data Exists

```bash
# Check for coverage file
if [ -f coverage/coverage-summary.json ]; then
  COVERAGE_SOURCE="json"
elif [ -f .claude/baseline/test-output.txt ]; then
  COVERAGE_SOURCE="text"
else
  echo "❌ Error: No coverage data found"
  echo "Run: npm run test -- --coverage"
  exit 1
fi

echo "Coverage source: $COVERAGE_SOURCE"
```

### Step 2: Extract Coverage Metrics

```bash
if [ "$COVERAGE_SOURCE" = "json" ]; then
  # Parse from JSON (preferred)
  OVERALL_COV=$(jq -r '.total.lines.pct' coverage/coverage-summary.json)
  STMT_COV=$(jq -r '.total.statements.pct' coverage/coverage-summary.json)
  BRANCH_COV=$(jq -r '.total.branches.pct' coverage/coverage-summary.json)
  FUNC_COV=$(jq -r '.total.functions.pct' coverage/coverage-summary.json)

else
  # Parse from text output (fallback)
  OVERALL_COV=$(grep -oP 'All files.*?\|\s+(\d+\.\d+)' .claude/baseline/test-output.txt | grep -oP '\d+\.\d+' | head -1 || echo "0")
  STMT_COV=$OVERALL_COV
  BRANCH_COV=$OVERALL_COV
  FUNC_COV=$OVERALL_COV
fi

echo "Coverage metrics:"
echo "  Overall: ${OVERALL_COV}%"
echo "  Statements: ${STMT_COV}%"
echo "  Branches: ${BRANCH_COV}%"
echo "  Functions: ${FUNC_COV}%"
```

### Step 3: Load Thresholds

```bash
# Use provided thresholds or defaults
MIN_OVERALL=${1:-80}
MIN_STMT=${2:-80}
MIN_BRANCH=${3:-75}
MIN_FUNC=${4:-80}

echo ""
echo "Minimum thresholds:"
echo "  Overall: ${MIN_OVERALL}%"
echo "  Statements: ${MIN_STMT}%"
echo "  Branches: ${MIN_BRANCH}%"
echo "  Functions: ${MIN_FUNC}%"
```

### Step 4: Validate Against Thresholds

```bash
echo ""
echo "→ Validating coverage thresholds..."

THRESHOLD_PASSED=true
FAILURES=()

# Check overall
if [ "$(echo "$OVERALL_COV < $MIN_OVERALL" | bc -l)" -eq 1 ]; then
  echo "❌ Overall coverage below threshold: ${OVERALL_COV}% < ${MIN_OVERALL}%"
  THRESHOLD_PASSED=false
  FAILURES+=("overall:${OVERALL_COV}%<${MIN_OVERALL}%")
else
  echo "✅ Overall coverage: ${OVERALL_COV}% ≥ ${MIN_OVERALL}%"
fi

# Check statements
if [ "$(echo "$STMT_COV < $MIN_STMT" | bc -l)" -eq 1 ]; then
  echo "❌ Statement coverage below threshold: ${STMT_COV}% < ${MIN_STMT}%"
  THRESHOLD_PASSED=false
  FAILURES+=("statements:${STMT_COV}%<${MIN_STMT}%")
else
  echo "✅ Statement coverage: ${STMT_COV}% ≥ ${MIN_STMT}%"
fi

# Check branches
if [ "$(echo "$BRANCH_COV < $MIN_BRANCH" | bc -l)" -eq 1 ]; then
  echo "❌ Branch coverage below threshold: ${BRANCH_COV}% < ${MIN_BRANCH}%"
  THRESHOLD_PASSED=false
  FAILURES+=("branches:${BRANCH_COV}%<${MIN_BRANCH}%")
else
  echo "✅ Branch coverage: ${BRANCH_COV}% ≥ ${MIN_BRANCH}%"
fi

# Check functions
if [ "$(echo "$FUNC_COV < $MIN_FUNC" | bc -l)" -eq 1 ]; then
  echo "❌ Function coverage below threshold: ${FUNC_COV}% < ${MIN_FUNC}%"
  THRESHOLD_PASSED=false
  FAILURES+=("functions:${FUNC_COV}%<${MIN_FUNC}%")
else
  echo "✅ Function coverage: ${FUNC_COV}% ≥ ${MIN_FUNC}%"
fi
```

### Step 5: Identify Uncovered Files

```bash
if [ "$COVERAGE_SOURCE" = "json" ]; then
  # Find files with low coverage
  UNCOVERED_FILES=$(jq -r '
    to_entries |
    map(select(.key != "total" and .value.lines.pct < 80)) |
    map({file: .key, coverage: .value.lines.pct}) |
    sort_by(.coverage) |
    .[]' coverage/coverage-summary.json | \
    jq -s -c '.')
else
  UNCOVERED_FILES="[]"
fi
```

### Step 6: Return Result

```json
{
  "status": "$([ "$THRESHOLD_PASSED" = true ] && echo 'success' || echo 'warning')",
  "coverage": {
    "overall": $OVERALL_COV,
    "statements": $STMT_COV,
    "branches": $BRANCH_COV,
    "functions": $FUNC_COV
  },
  "thresholds": {
    "overall": $MIN_OVERALL,
    "statements": $MIN_STMT,
    "branches": $MIN_BRANCH,
    "functions": $MIN_FUNC
  },
  "passed": $THRESHOLD_PASSED,
  "failures": $(printf '%s\n' "${FAILURES[@]}" | jq -R -s -c 'split("\n") | map(select(length > 0))'),
  "uncoveredFiles": $UNCOVERED_FILES
}
```

## Output Format

### All Thresholds Met

```json
{
  "status": "success",
  "coverage": {
    "overall": 87.5,
    "statements": 88.2,
    "branches": 84.1,
    "functions": 89.3
  },
  "thresholds": {
    "overall": 80,
    "statements": 80,
    "branches": 75,
    "functions": 80
  },
  "passed": true,
  "failures": []
}
```

### Below Threshold

```json
{
  "status": "warning",
  "coverage": {
    "overall": 75.3,
    "statements": 76.1,
    "branches": 72.8,
    "functions": 78.2
  },
  "thresholds": {
    "overall": 80,
    "statements": 80,
    "branches": 75,
    "functions": 80
  },
  "passed": false,
  "failures": [
    "overall:75.3%<80%",
    "statements:76.1%<80%",
    "branches:72.8%<75%",
    "functions:78.2%<80%"
  ],
  "uncoveredFiles": [
    {"file": "src/utils/helpers.ts", "coverage": 45.2},
    {"file": "src/services/api.ts", "coverage": 62.8}
  ]
}
```

## Integration with Quality Gate

Used in `quality-gate` skill:

```markdown
### Step 4: Check Test Coverage

Use `validate-coverage-threshold` skill:
- Input: thresholds (or use defaults)
- Expected: All thresholds met

If coverage below threshold:
  ⚠️ WARNING (not blocking for MVP)
  → Log coverage gap
  → Create GitHub issue for improvement
  → Continue with quality gate

If coverage acceptable:
  ✅ Coverage validation passed
```

## Configurable Thresholds

### Via Skill Parameters

```bash
# Custom thresholds
validate-coverage-threshold 85 85 80 90

# Parameters: overall, statements, branches, functions
```

### Via Config File

```json
// .claude/quality-gate-config.json
{
  "minimumCoverage": 80,
  "coverageThresholds": {
    "overall": 85,
    "statements": 85,
    "branches": 80,
    "functions": 90
  },
  "blockOnCoverage": false
}
```

## Related Skills

- `quality-gate` - Uses this for coverage validation
- `record-quality-baseline` - Records coverage baseline
- `run-comprehensive-tests` - Generates coverage data

## Error Handling

### No Coverage Data

```json
{
  "status": "error",
  "error": "Coverage data not found",
  "suggestion": "Run tests with coverage: npm run test -- --coverage"
}
```

### Invalid Coverage Format

```json
{
  "status": "error",
  "error": "Cannot parse coverage data",
  "suggestion": "Verify coverage output format"
}
```

## Best Practices

1. **Run tests with coverage first** - Ensure data exists
2. **Set realistic thresholds** - Based on project maturity
3. **Track coverage trends** - Monitor over time
4. **Don't block on coverage** - Use as warning, not blocker (initially)
5. **Identify gaps** - Focus on uncovered critical paths

## Notes

- Coverage below threshold is WARNING not ERROR (configurable)
- Helps track code coverage quality
- Uncovered files help prioritize test additions
- Can be made blocking in CI/CD pipeline
