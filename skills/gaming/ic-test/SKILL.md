---
name: ic-test
description: Test IC10 code for correctness and logic bugs. Use when user wants to verify IC10 code works through test cases or simulation analysis.
---

# IC10 Code Testing

Test IC10 code to verify it works correctly through analysis and test case design.

## Workflow

### 1. Analysis Phase
Use Task tool to spawn:
- `code-tester` - Perform static analysis and design test cases

### 2. Test Case Phase (If Needed)

If tester requires specific test scenarios, request them from user:
- What devices should be connected?
- What input states to test?
- What outputs are expected?

### 3. Verification Phase

Based on test results:
- **All tests pass** - Code is verified working
- **Some tests fail** - Recommend fixes via ic-debug
- **Simulation needed** - Note limitations and recommend in-game testing

## Testing Capabilities

### Static Analysis
- Logic flow verification
- Edge case identification
- State machine validation
- Resource deadlock detection

### Test Case Design
- Normal operation scenarios
- Boundary conditions
- Error recovery paths
- Device connectivity scenarios

### Pattern Verification
- State machine structure
- PID controller terms
- Batch operation correctness
- Indirect addressing usage

## Limitations

**Important**: Full IC10 simulation is not available. Testing is limited to:

1. **Static Analysis** - Code inspection without execution
2. **Manual Tracing** - Step-by-step logic simulation
3. **Pattern Comparison** - Against known working code
4. **Test Case Design** - Create procedures for manual testing

For actual execution, code must be tested in-game.

## Instructions

When the user asks to test IC10 code:

1. **Launch code-tester** with the code
   - Include any specific test requirements
   - Note if this is generated code or user-written

2. **Review test report**
   - Check which tests passed/failed
   - Review edge cases identified
   - Note any logic errors found

3. **Present results clearly**
   - Overall verdict (PASS/FAIL/NEEDS_TESTING)
   - Specific issues with line numbers
   - Recommendations for fixes or in-game testing

4. **Offer next steps**
   - If issues found: "Want me to fix these bugs?"
   - If tests pass: "Ready for in-game testing"
   - If uncertain: "Recommend testing with specific scenario"

## Example Triggers

- "Test this code"
- "Verify this IC10 script"
- "Does this code work?"
- "Check for logic errors"
- "Create test cases for..."
- "Will this script handle..."

## Output Format

After testing completes, respond with:

```
## Test Results: [Script Name]

### Static Analysis
✅ Logic flow correct
✅ All states reachable
⚠️  Missing error handling for edge case

### Test Cases

| Scenario | Expected | Result | Status |
|----------|-----------|--------|--------|
| Normal operation | Device activates | PASS |
| No ore available | Device off | PASS |
| Kill switch active | Stop all | PASS |

### Issues Found

1. **Logic Error** (Line 45)
   - Problem: Comparison inverted
   - Impact: Device activates when shouldn't
   - Fix: Change `slt` to `sgt`

### Overall Verdict
**Status**: ⚠️ NEEDS_FIXES

**Recommendation**: Fix logic error in line 45, then re-test
```

## Notes

- Testing is static - in-game verification still required
- Complex state machines may need manual test case review
- Multi-chip coordination requires testing all chips together
- Batch operations need hash verification in-game
