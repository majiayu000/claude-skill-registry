---
name: testsprite-pre-pr
description: Comprehensive pre-PR testing using TestSprite MCP. Use before opening a pull request, after completing a task, or when full E2E validation is needed. Includes HITL checkpoints for user confirmation. Triggers on "pre-pr testing", "testsprite test", "before PR", "e2e validation", "run testsprite".
---

# TestSprite Pre-PR

## Purpose

Run comprehensive end-to-end testing using TestSprite MCP before opening a pull request. Ensures all changes work correctly in a realistic environment.

**Key Features:**
- Automatic test plan generation from PRD
- Human-in-the-loop (HITL) checkpoints
- Sandbox execution isolation
- Pre-commit validation gate

## When to Use

- Before opening a pull request
- After completing a development task
- When full E2E validation is needed
- Before merging to main branch
- After significant refactoring

**When NOT to use:**
- Quick unit testing (use Wallaby or npm test)
- Exploring new features (use Agent Browser CLI)
- Debugging (use Chrome DevTools MCP)

## Prerequisites

1. TestSprite MCP configured (see skill-test-setup)
2. Application running locally
3. PRD/PRP document available from TaskMaster
4. Git diff showing changes to test

## TestSprite MCP Tools

| Tool | Purpose |
|------|---------|
| `testsprite_bootstrap_tests` | Initialize testing environment |
| `testsprite_generate_tests` | Generate test cases |
| `testsprite_run_tests` | Execute tests |
| `testsprite_analyze_results` | Analyze test results |
| `testsprite_generate_report` | Generate test report |
| `testsprite_cleanup` | Clean up resources |
| `testsprite_ask` | Ask questions about results |

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    TESTSPRITE PRE-PR WORKFLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. ANALYZE CHANGES                                             │
│     └─> Read git diff                                           │
│     └─> Read PRD from TaskMaster                                │
│     └─> Identify test scope                                     │
│                                                                 │
│  2. BOOTSTRAP (automated)                                       │
│     └─> testsprite_bootstrap_tests()                            │
│     └─> Configure environment                                   │
│                                                                 │
│  3. HITL CHECKPOINT 1 ⏸️                                        │
│     └─> Review generated test plan                              │
│     └─> [USER] Approve/Modify                                   │
│                                                                 │
│  4. CONFIGURE SCOPE (HITL) ⏸️                                   │
│     └─> Choose: diff vs codebase                                │
│     └─> Choose: backend vs frontend vs both                     │
│     └─> [USER] Confirm selections                               │
│                                                                 │
│  5. GENERATE TESTS                                              │
│     └─> testsprite_generate_tests()                             │
│     └─> Create test cases                                       │
│                                                                 │
│  6. EXECUTE IN SANDBOX                                          │
│     └─> testsprite_run_tests()                                  │
│     └─> Isolated test execution                                 │
│                                                                 │
│  7. ANALYZE RESULTS                                             │
│     └─> testsprite_analyze_results()                            │
│     └─> Identify failures                                       │
│                                                                 │
│  8. HITL CHECKPOINT 2 ⏸️ (if failures)                          │
│     └─> Review failures with user                               │
│     └─> [USER] Decide: Fix / Skip / Override                    │
│                                                                 │
│  9. GENERATE REPORT                                             │
│     └─> testsprite_generate_report()                            │
│     └─> Human-readable summary                                  │
│                                                                 │
│  10. PRE-COMMIT DECISION                                        │
│      └─> All passed? ✅ OK for PR                               │
│      └─> Failures? 🔧 Fix and re-run                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Step-by-Step Execution

### Step 1: Analyze Changes

```bash
# Get git diff of current changes
git diff main...HEAD > /tmp/current-changes.diff

# Identify changed files
git diff --name-only main...HEAD
```

**Read PRD from TaskMaster:**
- Location: `.taskmaster/PRD.md` or similar
- Contains: Feature requirements, acceptance criteria

### Step 2: Bootstrap Test Environment

```json
{
  "tool": "testsprite_bootstrap_tests",
  "parameters": {
    "localPort": 5173,
    "type": "frontend",
    "projectPath": "/absolute/path/to/project",
    "testScope": "diff"
  }
}
```

**Parameters:**
- `localPort`: Where your app is running (default: 5173)
- `type`: "frontend" | "backend" | "fullstack"
- `projectPath`: Absolute path to project root
- `testScope`: "diff" (changed files) | "codebase" (full)

### Step 3: HITL Checkpoint - Review Test Plan

```markdown
⏸️ HUMAN CHECKPOINT REQUIRED

TestSprite has generated a test plan based on your PRD and changes.

Please review:
- Test coverage areas
- Test scenarios identified
- Edge cases included

[USER ACTION REQUIRED]
✅ Approve - Proceed with this plan
📝 Modify - Request changes to test plan
❌ Cancel - Abort testing
```

**Wait for user confirmation before proceeding.**

### Step 4: HITL Checkpoint - Configure Scope

```markdown
⏸️ CONFIGURATION REQUIRED

Select test scope:

**Test Mode:**
- [ ] diff - Test only changed files (faster)
- [ ] codebase - Test entire codebase (comprehensive)

**Test Target:**
- [ ] frontend - UI/UX tests only
- [ ] backend - API/Server tests only
- [ ] both - Full stack tests

**Additional Options:**
- [ ] Include regression tests
- [ ] Include performance tests
- [ ] Include accessibility tests

[USER ACTION REQUIRED]
Confirm selections to proceed
```

### Step 5: Generate Tests

```json
{
  "tool": "testsprite_generate_tests",
  "parameters": {
    "testScope": "diff",
    "testType": "e2e"
  }
}
```

**Test Types:**
- `unit` - Unit tests
- `integration` - Integration tests
- `e2e` - End-to-end tests

### Step 6: Execute Tests in Sandbox

```json
{
  "tool": "testsprite_run_tests",
  "parameters": {
    "testType": "e2e",
    "testScope": "diff"
  }
}
```

**Sandbox Features:**
- Isolated environment
- Clean browser state
- Reproducible conditions
- Parallel execution (if configured)

### Step 7: Analyze Results

```json
{
  "tool": "testsprite_analyze_results",
  "parameters": {
    "testType": "e2e"
  }
}
```

**Analysis Output:**
```
Test Results Summary:
- Total tests: 15
- Passed: 12
- Failed: 3
- Skipped: 0

Failed Tests:
1. TC003 - Login form validation
   Error: Timeout waiting for element #submit
   Screenshot: available

2. TC007 - Payment flow
   Error: API returned 500
   Stack trace: available

3. TC012 - Mobile responsive
   Error: Element overflow on 375px width
   Visual diff: available
```

### Step 8: HITL Checkpoint - Handle Failures

```markdown
⏸️ FAILURES DETECTED

3 tests failed. Review details above.

[USER ACTION REQUIRED]

Options:
🔧 Fix - I'll fix the issues and re-run
⏭️ Skip - Skip these tests (not blocking)
📝 Override - Mark as acceptable (document why)
🔄 Re-run - Try running again (flaky test?)

Note: All tests should pass before PR unless
there's a documented reason.
```

### Step 9: Generate Report

```json
{
  "tool": "testsprite_generate_report",
  "parameters": {
    "testType": "e2e"
  }
}
```

**Report Includes:**
- Executive summary
- Test coverage map
- Failure details with screenshots
- Performance metrics
- Recommendations

**Files Generated:**
```
testsprite_tests/
├── TestSprite_MCP_Test_Report.md      # Human-readable
├── TestSprite_MCP_Test_Report.html    # Formatted HTML
├── test_results.json                  # Machine-readable
└── screenshots/                       # Visual evidence
    ├── TC001_success.png
    ├── TC003_failure.png
    └── ...
```

### Step 10: Pre-Commit Decision

```markdown
╔════════════════════════════════════════════════════════════╗
║              PRE-COMMIT VALIDATION RESULT                  ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Status: ✅ ALL TESTS PASSED                               ║
║                                                            ║
║  Summary:                                                  ║
║  - 15/15 tests passed                                      ║
║  - 0 failures                                              ║
║  - Coverage: 87%                                           ║
║                                                            ║
║  ✅ You may proceed to open PR                             ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

Or:

```markdown
╔════════════════════════════════════════════════════════════╗
║              PRE-COMMIT VALIDATION RESULT                  ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Status: 🔧 FAILURES DETECTED                              ║
║                                                            ║
║  Summary:                                                  ║
║  - 12/15 tests passed                                      ║
║  - 3 failures (see report)                                 ║
║                                                            ║
║  ⚠️  Fix failures or document override before PR           ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

## Complete Example Session

```bash
# User: "Run pre-PR testing"

# 1. Analyze
> Reading git diff... 12 files changed
> Reading PRD from TaskMaster... Feature: User authentication

# 2. Bootstrap
> Initializing TestSprite environment...
> Port 5173 confirmed active
> Project type: frontend

# 3. HITL ⏸️
⏸️ Review test plan:
   - Login form validation (3 scenarios)
   - Registration flow (4 scenarios)
   - Password reset (2 scenarios)
   - Session management (3 scenarios)
   
   [User: ✅ Approve]

# 4. HITL ⏸️
⏸️ Configure scope:
   - Mode: diff (changed files only)
   - Target: both (frontend + backend)
   
   [User: ✅ Confirm]

# 5. Generate
> Generating 12 test cases...

# 6. Execute
> Running tests in sandbox...
> Progress: 12/12 completed

# 7. Analyze
> Results: 11 passed, 1 failed
> Failure: TC008 - Session timeout
> Error: Session not expiring after 30min

# 8. HITL ⏸️
⏸️ 1 test failed. Options:
   [User: 🔧 Fix]

# 9. Fix & Re-run
> Fixing session timeout...
> Re-running tests...
> Results: 12/12 passed ✅

# 10. Report
> Generated TestSprite_MCP_Test_Report.md

# 11. Result
╔═══════════════════════════════════════╗
║  ✅ ALL TESTS PASSED - OK FOR PR      ║
╚═══════════════════════════════════════╝
```

## Customization Options

### Add Custom Test Suites

```json
{
  "tool": "testsprite_generate_tests",
  "parameters": {
    "testScope": "diff",
    "testType": "e2e",
    "additionalSuites": ["accessibility", "performance", "security"]
  }
}
```

### Include External Tools

TestSprite can integrate additional tools in its workflow:
- Jest/Vitest for unit tests
- Playwright for browser automation
- Custom scripts

Configure in `testsprite_tests/config.json`

## Troubleshooting

### TestSprite Not Responding

```bash
# Check MCP server status
# Verify API key is set
# Restart MCP connection
```

### Sandbox Timeout

```markdown
Issue: Tests timeout in sandbox
Solution: 
- Increase timeout in config
- Check if app is responding
- Verify port is correct
```

### Flaky Tests

```markdown
Issue: Tests pass/fail inconsistently
Solution:
- Add retry logic
- Check for race conditions
- Stabilize test data
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| skill-test-setup | Initial tool configuration |
| skill-testing-philosophy | TDD principles |
| skill-testing-workflow | Tool selection guidance |

## Best Practices

1. **Always run before PR** - No exceptions
2. **Review test plan** - Don't auto-approve
3. **Fix real failures** - Don't override without reason
4. **Keep reports** - Attach to PR for reviewers
5. **Iterate quickly** - Fix and re-run, don't batch

## Version

v1.0.0 (2025-01-28) - TestSprite Pre-PR Testing