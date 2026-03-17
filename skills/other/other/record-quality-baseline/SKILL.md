---
name: record-quality-baseline
description: Record quality metrics baseline before refactoring or major changes, capturing audit scores, test coverage, and complexity for comparison
---

# Record Quality Baseline

## Purpose

Capture current code quality metrics before making changes to enable before/after comparison and ensure refactoring improves (or maintains) quality standards.

## When to Use

- Refactor agent Step 1 (Pre-Refactor Validation)
- Before any code restructuring or simplification
- Before technical debt reduction
- When establishing quality improvement targets
- Before major feature implementation

## Instructions

### Step 1: Run Baseline Tests

```bash
echo "→ Recording quality baseline..."
echo ""

# Run tests with coverage
echo "Running tests..."
if npm run test -- --coverage --silent 2>&1 | tee .claude/baseline/test-output.txt; then
  TEST_STATUS="passing"
  TEST_EXIT_CODE=0
else
  TEST_STATUS="failing"
  TEST_EXIT_CODE=$?
fi

# Extract test metrics
TOTAL_TESTS=$(grep -oP '\d+ tests?' .claude/baseline/test-output.txt | head -1 | grep -oP '\d+' || echo "0")
PASSED_TESTS=$(grep -oP '\d+ passed' .claude/baseline/test-output.txt | grep -oP '\d+' || echo "0")
FAILED_TESTS=$(grep -oP '\d+ failed' .claude/baseline/test-output.txt | grep -oP '\d+' || echo "0")
```

### Step 2: Extract Coverage Metrics

```bash
# Parse coverage from output or coverage file
if [ -f coverage/coverage-summary.json ]; then
  COVERAGE=$(jq -r '.total.lines.pct' coverage/coverage-summary.json)
  STMT_COVERAGE=$(jq -r '.total.statements.pct' coverage/coverage-summary.json)
  BRANCH_COVERAGE=$(jq -r '.total.branches.pct' coverage/coverage-summary.json)
  FUNCTION_COVERAGE=$(jq -r '.total.functions.pct' coverage/coverage-summary.json)
else
  # Fallback: parse from text output
  COVERAGE=$(grep -oP 'All files.*?\|\s+(\d+\.\d+)' .claude/baseline/test-output.txt | grep -oP '\d+\.\d+' || echo "0")
  STMT_COVERAGE=$COVERAGE
  BRANCH_COVERAGE=$COVERAGE
  FUNCTION_COVERAGE=$COVERAGE
fi

echo "✅ Test baseline recorded"
echo "   Tests: $PASSED_TESTS/$TOTAL_TESTS passing"
echo "   Coverage: ${COVERAGE}%"
```

### Step 3: Run Code Quality Audit

```bash
# Run audit if available
if npm run audit:code --silent 2>&1 | tee .claude/baseline/audit-output.txt; then
  AUDIT_STATUS="success"
else
  AUDIT_STATUS="not_available"
fi

# Parse audit score (if available)
if [ "$AUDIT_STATUS" = "success" ]; then
  AUDIT_SCORE=$(grep -oP 'Score:\s+(\d+\.\d+)' .claude/baseline/audit-output.txt | grep -oP '\d+\.\d+' || echo "0")
  echo "✅ Audit baseline recorded"
  echo "   Score: ${AUDIT_SCORE}/10"
else
  AUDIT_SCORE="N/A"
  echo "ℹ️ Code audit not available"
fi
```

### Step 4: Check TypeScript Errors

```bash
# Run TypeScript check
if command -v tsc &>/dev/null; then
  if tsc --noEmit 2>&1 | tee .claude/baseline/tsc-output.txt; then
    TS_ERRORS=0
    TS_STATUS="passing"
  else
    TS_ERRORS=$(grep -c 'error TS' .claude/baseline/tsc-output.txt || echo "0")
    TS_STATUS="failing"
  fi

  echo "✅ TypeScript baseline recorded"
  echo "   Errors: $TS_ERRORS"
else
  TS_ERRORS="N/A"
  TS_STATUS="not_available"
  echo "ℹ️ TypeScript not available"
fi
```

### Step 5: Analyze Code Complexity (Optional)

```bash
# If complexity analysis tool available
if command -v complexity &>/dev/null; then
  COMPLEXITY=$(complexity analyze src/ --json 2>/dev/null || echo "{}")
  echo "✅ Complexity baseline recorded"
else
  COMPLEXITY="N/A"
  echo "ℹ️ Complexity analysis not available"
fi
```

### Step 6: Save Baseline to File

```bash
mkdir -p .claude/baseline

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

cat > .claude/baseline/quality-baseline.json << EOF
{
  "timestamp": "$TIMESTAMP",
  "tests": {
    "status": "$TEST_STATUS",
    "total": $TOTAL_TESTS,
    "passed": $PASSED_TESTS,
    "failed": $FAILED_TESTS,
    "exitCode": $TEST_EXIT_CODE
  },
  "coverage": {
    "overall": $COVERAGE,
    "statements": $STMT_COVERAGE,
    "branches": $BRANCH_COVERAGE,
    "functions": $FUNCTION_COVERAGE
  },
  "audit": {
    "status": "$AUDIT_STATUS",
    "score": "$AUDIT_SCORE"
  },
  "typescript": {
    "status": "$TS_STATUS",
    "errors": $TS_ERRORS
  },
  "complexity": $COMPLEXITY,
  "git": {
    "branch": "$(git branch --show-current)",
    "commit": "$(git rev-parse --short HEAD)"
  }
}
EOF

echo ""
echo "✅ Quality baseline saved to .claude/baseline/quality-baseline.json"
```

### Step 7: Validate Baseline Requirements

```bash
# Check if baseline meets minimum requirements for refactoring
CAN_REFACTOR=true

if [ "$TEST_STATUS" != "passing" ]; then
  echo "❌ Cannot proceed - tests failing before refactoring"
  CAN_REFACTOR=false
fi

if [ "$TS_STATUS" = "failing" ]; then
  echo "⚠️ Warning: TypeScript errors exist before refactoring"
fi

if [ "$CAN_REFACTOR" = true ]; then
  echo "✅ Quality baseline acceptable - safe to proceed with refactoring"
else
  echo "❌ Quality baseline unacceptable - fix test failures first"
  exit 1
fi
```

## Output Format

### Successful Baseline

```json
{
  "status": "success",
  "baseline": {
    "timestamp": "2025-10-21T14:30:00Z",
    "tests": {
      "status": "passing",
      "total": 45,
      "passed": 45,
      "failed": 0
    },
    "coverage": {
      "overall": 87.5,
      "statements": 88.2,
      "branches": 84.1,
      "functions": 89.3
    },
    "audit": {
      "status": "success",
      "score": 7.5
    },
    "typescript": {
      "status": "passing",
      "errors": 0
    },
    "canProceed": true
  },
  "file": ".claude/baseline/quality-baseline.json"
}
```

### Baseline with Failing Tests

```json
{
  "status": "error",
  "baseline": {
    "tests": {
      "status": "failing",
      "total": 45,
      "passed": 42,
      "failed": 3
    }
  },
  "canProceed": false,
  "error": "Tests failing before refactoring - fix failures first"
}
```

## Integration with Refactor Agent

Used in refactor workflow Step 1:

```markdown
### Step 1: Pre-Refactor Validation

Use `record-quality-baseline` skill to capture current state:

Expected output:
- Tests: All passing ✅
- Coverage: 87.5%
- Audit: 7.5/10
- TypeScript: 0 errors

If baseline tests fail:
  ❌ BLOCK refactoring
  → Fix test failures first
  → Re-run baseline

If baseline acceptable:
  ✅ Proceed to Step 2 (Target Analysis)
  → Save baseline for comparison after refactoring
```

## Comparison After Refactoring

After refactoring, compare to baseline:

```bash
# Load baseline
BASELINE_SCORE=$(jq -r '.audit.score' .claude/baseline/quality-baseline.json)
BASELINE_COVERAGE=$(jq -r '.coverage.overall' .claude/baseline/quality-baseline.json)

# Get current metrics
CURRENT_SCORE=8.5
CURRENT_COVERAGE=89.2

# Compare
SCORE_DELTA=$(echo "$CURRENT_SCORE - $BASELINE_SCORE" | bc)
COVERAGE_DELTA=$(echo "$CURRENT_COVERAGE - $BASELINE_COVERAGE" | bc)

echo "Quality Improvement:"
echo "  Audit score: $BASELINE_SCORE → $CURRENT_SCORE (${SCORE_DELTA:+}$SCORE_DELTA)"
echo "  Coverage: $BASELINE_COVERAGE% → $CURRENT_COVERAGE% (${COVERAGE_DELTA:+}$COVERAGE_DELTA%)"
```

## Related Skills

- `quality-gate` - Comprehensive quality validation
- `validate-typescript` - TypeScript-specific validation
- `validate-coverage-threshold` - Coverage threshold checking

## Baseline Storage

- **Location**: `.claude/baseline/quality-baseline.json`
- **Git**: Should be in `.gitignore` (temporary)
- **Lifetime**: Valid for single refactoring session
- **Cleanup**: Delete after refactoring complete

## Best Practices

1. **Always record before refactoring** - Essential for comparison
2. **Block if tests failing** - Never refactor broken code
3. **Save all outputs** - Useful for debugging
4. **Validate JSON** - Ensure baseline file is valid
5. **Compare after changes** - Verify improvement
6. **Clean up baseline files** - Don't commit to repo

## Error Handling

### Test Command Not Found

```bash
if ! npm run test --dry-run &>/dev/null; then
  echo "❌ Error: No test script configured"
  echo "Add test script to package.json"
  exit 1
fi
```

### Coverage Data Missing

```bash
if [ ! -f coverage/coverage-summary.json ]; then
  echo "⚠️ Warning: Coverage data not found"
  echo "Ensure tests run with --coverage flag"
  COVERAGE="0"
fi
```

## Notes

- Baseline is essential for safe refactoring
- Tests must pass before refactoring begins
- Audit score should improve or stay same after refactoring
- Coverage should not decrease after refactoring
- TypeScript errors should not increase
