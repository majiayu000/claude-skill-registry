---
name: test
description: Run unit and UI tests for GridRacer
model: haiku
allowed-tools:
  - Bash
  - Read
---

# Run GridRacer Tests

Execute unit tests and optionally UI tests.

## Steps

1. Auto-detect simulator:
   ```bash
   SIMULATOR=$(xcrun simctl list devices available | grep -E "iPhone (16|15|14)" | grep -v unavailable | head -1 | sed -E 's/.*iPhone ([0-9]+).*/iPhone \1/')
   ```

2. Run unit tests:
   ```bash
   xcodebuild test -scheme GridRacer -destination "platform=iOS Simulator,name=$SIMULATOR" -only-testing:GridRacerTests 2>&1 > /tmp/test_output.log
   ```

3. Parse and report results:

   Count results:
   ```bash
   PASSED=$(grep -c "passed on" /tmp/test_output.log || echo "0")
   FAILED=$(grep -c "failed on" /tmp/test_output.log || echo "0")
   TOTAL=$((PASSED + FAILED))
   ```

   **If all passed:**
   ```
   Test Results:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Passed: <PASSED> tests
   ❌ Failed: 0 tests

   Test Suites:
     ✅ GridPointTests (4/4)
     ✅ GridVectorTests (5/5)
     ✅ MovementCalculatorTests (5/5)
     ✅ BresenhamPathTests (7/7)
     ✅ TrackTests (6/6)
     ✅ PlayerTests (6/6)
     ✅ GameStateTests (6/6)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Status: READY TO COMMIT ✓
   ```

   **If failures:**
   ```
   Test Results:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ Passed: <PASSED> tests
   ❌ Failed: <FAILED> tests

   Failed Tests:
   ```

   Then show failed test names:
   ```bash
   grep "failed on" /tmp/test_output.log | sed -E "s/.*Test case '([^']+)'.*/  - \1/" | head -10
   ```

   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   Status: FIX TESTS BEFORE COMMITTING ❌
   ```

4. Optionally run UI tests if requested:
   ```bash
   xcodebuild test -scheme GridRacer -destination "platform=iOS Simulator,name=$SIMULATOR" -only-testing:GridRacerUITests 2>&1 | grep -E "(Test Case|passed|failed|error:|SUCCEEDED|FAILED)" | tail -30
   ```

## Output Format

The skill should always produce formatted, easy-to-read output with:
- Clear pass/fail counts
- Test suite breakdown (when possible)
- Specific failed test names
- Clear status indicator for commit readiness
