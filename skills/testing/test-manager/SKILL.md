---
name: Test Manager
description: Run visual tests, compare golden files, and report bugs for Stapledons Voyage. Use when user asks to run tests, check golden files, or report visual regressions.
---

# Test Manager

Manage visual regression testing for Stapledon's Voyage. Run test scenarios, compare against golden files, and generate bug reports.

## Quick Start

**Most common usage:**
```bash
# Run all test scenarios in test mode (no UI)
.claude/skills/test-manager/scripts/run_tests.sh

# Compare current output to golden files
.claude/skills/test-manager/scripts/compare_golden.sh

# Generate bug report for a visual regression
.claude/skills/test-manager/scripts/report_bug.sh <scenario-name> "<description>"
```

## When to Use This Skill

Invoke this skill when:
- User asks to "run tests" or "check tests"
- User mentions "golden files" or "visual regression"
- User wants to compare current rendering against baseline
- User reports a visual bug that needs investigation
- After making changes to rendering code

## Available Scripts

### `scripts/run_tests.sh [scenario-name]`
Run test scenarios and capture screenshots with UI stripped (test mode).

**Usage:**
```bash
# Run all scenarios
.claude/skills/test-manager/scripts/run_tests.sh

# Run specific scenario
.claude/skills/test-manager/scripts/run_tests.sh camera-pan
```

**Output:**
- Screenshots saved to `out/test/<scenario-name>/`
- Summary of pass/fail status

### `scripts/compare_golden.sh [scenario-name]`
Compare current test output against golden files.

**Usage:**
```bash
# Compare all scenarios
.claude/skills/test-manager/scripts/compare_golden.sh

# Compare specific scenario
.claude/skills/test-manager/scripts/compare_golden.sh camera-pan
```

**Output:**
- Lists matching and differing files
- Generates diff images for mismatches (if ImageMagick available)
- Exit code 0 if all match, 1 if differences found

### `scripts/update_golden.sh [scenario-name]`
Update golden files from current test output.

**Usage:**
```bash
# Update all golden files
.claude/skills/test-manager/scripts/update_golden.sh

# Update specific scenario
.claude/skills/test-manager/scripts/update_golden.sh camera-pan
```

### `scripts/report_bug.sh <scenario> <description>`
Generate a bug report design doc for visual regression.

**Usage:**
```bash
.claude/skills/test-manager/scripts/report_bug.sh camera-zoom "Zoom out produces artifacts at edge"
```

## Workflow

### 1. Run Tests

Run all scenarios in test mode to generate current screenshots:
```bash
.claude/skills/test-manager/scripts/run_tests.sh
```

### 2. Compare Against Golden Files

Check if current output matches the baseline:
```bash
.claude/skills/test-manager/scripts/compare_golden.sh
```

### 3. Handle Results

**If tests pass:** No action needed.

**If tests fail:**
- Review the diff images in `out/test/<scenario>/diff/`
- If change is intentional: `scripts/update_golden.sh`
- If change is a bug: `scripts/report_bug.sh <scenario> "<description>"`

### 4. Investigate Bugs

When a visual regression is found:
1. Run the specific scenario: `make scenario-<name>`
2. Review screenshots
3. Create bug report with design doc
4. Fix the issue
5. Re-run tests to verify

## Test Scenarios

Current test scenarios in `scenarios/`:

| Scenario | Purpose |
|----------|---------|
| `camera-pan` | Test WASD camera movement |
| `camera-zoom` | Test Q/E zoom controls |
| `npc-movement` | Capture NPC movement over time |

Add `"test_mode": true` to JSON for golden file testing.

## Golden Files

Golden files are stored in `golden/<scenario-name>/` and should be committed to git.

**Structure:**
```
golden/
├── camera-pan/
│   ├── initial.png
│   ├── after-down.png
│   └── after-right.png
├── camera-zoom/
│   └── ...
└── npc-movement/
    └── ...
```

## Output Organization

Test output follows the project's [out/ directory structure](../../../out/README.md):

| Directory | Purpose |
|-----------|---------|
| `out/test/<scenario>/` | Current test output (screenshots) |
| `out/test/<scenario>/diff/` | Diff images when tests fail |
| `out/scenarios/` | Temporary scenario runner output |
| `golden/<scenario>/` | Baseline golden files (committed to git) |

**Important:**
- Test output in `out/test/` is gitignored and ephemeral
- Golden files in `golden/` are committed and versioned
- Never put test output in `out/` root - always use `out/test/<scenario>/`

## Notes

- Always run tests with `--test-mode` to strip UI elements
- Golden files should be updated intentionally, not automatically
- Use deterministic seeds for reproducible tests
- Screenshots are at 1280x960 internal resolution

## IMPORTANT: Screenshot Method

**NEVER use macOS `screencapture`** - it captures the desktop at native resolution (5K+), producing huge files.

**ALWAYS use in-game screenshot flags:**
```bash
go run ./cmd/game --screenshot 30 --output out/test.png
```

Or use the helper script:
```bash
.claude/skills/sprint-executor/scripts/take_screenshot.sh -f 30 -o out/test.png
```
