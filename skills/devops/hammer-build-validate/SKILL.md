---
name: hammer-build-validate
description: Runs complete build validation pipeline for SDL3 HammerEngine including Debug build, smoke test execution, core test suite, and summary report generation. Use when the user wants to quickly validate their changes, check if the codebase is in a good state, or run the standard daily validation workflow.
allowed-tools: [Bash, Read, Write]
---

# HammerEngine Build Validation Pipeline

This Skill automates the standard build validation workflow for SDL3 HammerEngine. It performs a complete validation cycle that developers typically run 5-10 times daily.

## Workflow Overview

The Skill executes these steps in sequence:
1. **Clean Debug Build** with warning detection
2. **Smoke Test** for crash detection
3. **Core Test Suite** for functional validation
4. **Summary Report** generation

## Detailed Execution Steps

### Step 1: Clean Debug Build

**Command:**
```bash
cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug && ninja -C build
```

**Validation:**
- Check if build succeeded (exit code 0)
- Filter and count compilation warnings:
  ```bash
  ninja -C build -v 2>&1 | grep -E "(warning|unused|error)" | head -n 100
  ```
- Categorize warnings by type (unused variables, type conversions, etc.)
- Flag if warning count exceeds threshold (>5 warnings = warning, >20 = concern)

**Error Handling:**
- If build fails, extract and display first 20 compilation errors
- Show file paths and line numbers for errors
- Recommend checking recent changes

### Step 2: Smoke Test (Crash Detection)

**Command:**
```bash
timeout 60s ./bin/debug/SDL3_Template > /tmp/app_log.txt 2>&1
```

**Working Directory:** `$PROJECT_ROOT/`

**Validation:**
- Check exit code:
  - 0 = clean exit
  - 124 = timeout (expected, app runs indefinitely)
  - Others = crash/error
- Scan `/tmp/app_log.txt` for:
  - Segmentation faults
  - Assertion failures
  - Exception messages
  - Memory errors (AddressSanitizer output if enabled)
  - SDL errors

**Success Criteria:**
- Exit code 124 (timeout) OR 0 (clean exit)
- No crash signatures in log
- No critical errors logged

**Error Handling:**
- If crashed, extract stack trace from log
- Show last 50 lines of output before crash
- Recommend running with AddressSanitizer for memory issues

### Step 3: Core Test Suite

**Command:**
```bash
./run_all_tests.sh --core-only --errors-only
```

**Working Directory:** `$PROJECT_ROOT/`

**What This Runs:**
- Thread System Tests
- Buffer Utilization Tests
- Thread-Safe AI Tests
- AI Optimization Tests
- Behavior Functionality Tests (8 behaviors)
- Save Manager Tests
- Event Manager Tests
- Collision System Tests
- Pathfinding Tests
- Integration Tests
- JSON Reader Tests
- Resource Tests
- World Manager Tests
- Particle Manager Tests

**Validation:**
- Parse output for test results
- Extract pass/fail counts
- Identify failed test names
- Check for unexpected errors or crashes

**Success Criteria:**
- All tests pass (typically 18+ test suites)
- No segfaults or crashes
- Execution completes in reasonable time (~2-5 minutes)

**Error Handling:**
- If tests fail, list failed test names
- Show brief error output for each failure
- Suggest running specific test script for details:
  ```bash
  ./tests/test_scripts/run_<system>_tests.sh --verbose
  ```

### Step 4: Generate Summary Report

**Report Format:**

```markdown
# Build Validation Report
**Date:** YYYY-MM-DD HH:MM:SS
**Branch:** <current-branch>
**Project:** SDL3 HammerEngine

## Results Summary

✓/✗ **Build:** <Status> (<warning-count> warnings)
✓/✗ **Smoke Test:** <Status> (<exit-reason>)
✓/✗ **Core Tests:** <passed>/<total> passed

**Total Execution Time:** <time>

## Details

### Build Warnings (<count>)
<list of warnings if any, max 10>

### Test Failures (<count>)
<list of failed tests with brief errors>

### Recommendations
<specific actions based on failures>

---
**Status:** ✓ PASSED / ✗ FAILED
```

**Save Location:** `/tmp/hammer_build_validation_report.md`

**Console Output:**
```
=== HammerEngine Build Validation ===

✓ Build: Success (3 warnings)
✓ Smoke Test: Clean (60s timeout)
✓ Core Tests: 18/18 passed

Total Time: 3m 42s

Status: ✓ PASSED

Report: /tmp/hammer_build_validation_report.md
```

## Exit Codes

- **0:** All validations passed
- **1:** Build failed
- **2:** Smoke test crashed
- **3:** Core tests failed
- **4:** Multiple failures

## Usage Examples

When the user says:
- "validate my changes"
- "check if everything builds"
- "run the daily validation"
- "make sure tests pass"
- "quick build check"

Activate this Skill automatically.

## Important Notes

1. **Always run from project root:** `$PROJECT_ROOT/`
2. **Timeout protection:** Smoke test has 60s timeout (app runs indefinitely)
3. **Core tests only:** Skips benchmarks (those take 5-20 minutes)
4. **Report persistence:** Report saved to `/tmp/` for user review
5. **Non-destructive:** Does not commit, push, or modify source files

## Performance Expectations

- **Build:** 30-90 seconds (depends on changes)
- **Smoke Test:** 60 seconds (timeout)
- **Core Tests:** 2-5 minutes
- **Total:** ~3-7 minutes

## Integration with Development Workflow

This Skill is designed to be run:
- **Before commits:** Ensure code is stable
- **After pulls:** Validate merge didn't break anything
- **During development:** Quick validation cycles
- **Before PRs:** Final check before creating pull request

## Troubleshooting

**Build fails with linker errors:**
- Try: `rm -rf build/ && cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug && ninja -C build`

**Smoke test always crashes:**
- Run with AddressSanitizer:
  ```bash
  cmake -B build/ -G Ninja -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_CXX_FLAGS="-D_GLIBCXX_DEBUG -fsanitize=address" \
    -DCMAKE_EXE_LINKER_FLAGS="-fsanitize=address" \
    -DUSE_MOLD_LINKER=OFF && ninja -C build
  ```

**Tests hang indefinitely:**
- Check for deadlocks in ThreadSystem
- Review recent threading changes
- Run specific test with timeout: `timeout 120s ./bin/debug/<test_name>`

**High warning count:**
- Review CLAUDE.md coding standards
- Run quality check Skill for detailed analysis
- Filter warnings: `ninja -C build -v 2>&1 | grep -E "warning" | sort | uniq`
