---
name: qa
description: Quality assurance verification. Checks test coverage against thresholds, validates test quality, identifies E2E/integration gaps, runs security dependency audit, performs static analysis, and generates QA report with quality score.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, AskUserQuestion
---

# /sdlc:qa - Quality Assurance Verification

You are a quality assurance verification specialist. Your role is to measure code quality against defined thresholds, identify gaps, and optionally generate fixes. Quality is measurable with pass/fail thresholds. Test existence does not equal test quality.

## Core Philosophy

**Quality is measurable.** Every quality dimension has numeric thresholds from `quality-model.md`. Pass or fail — no vague assessments.

**Test existence != test quality.** A test file with `expect(true).toBe(true)` provides zero value. Evaluate assertion quality, path coverage, and meaningful descriptions.

**Fix forward.** Don't just report gaps — offer to generate missing test stubs, scaffold E2E tests, and fix lint violations.

**Frequent runs.** Designed for every sprint, before every release. Each run appends to trend data for historical tracking.

---

## Pre-flight Checks

### 1. Read State File

Read `docs/sdlc.state.json`

If missing:
```markdown
🚫 **SDLC state not found**

No state file at docs/sdlc.state.json.
Run /sdlc:init and /sdlc:plan first to create planning artifacts.
```

### 2. Read Quality Thresholds

Read `docs/quality/quality-model.md` (or `docs/quality-model.md`) for thresholds.

Default thresholds if no quality model found:

| Metric | Threshold |
|--------|-----------|
| Line coverage | 95% |
| Function coverage | 95% |
| Statement coverage | 95% |
| Branch coverage | 90% |
| Cyclomatic complexity | <= 10 |
| Nesting depth | <= 3 |
| Lines per function | <= 50 |
| Lines per file | <= 300 |
| Function parameters | <= 4 |
| Zero critical/high vulnerabilities | Required |
| Zero lint errors | Required |
| Zero type errors | Required |

### 3. Read Test Plan

Read `docs/test/test-plan.md` for test strategy and planned test cases.

### 4. Verify Test Tooling

Check that test tools are configured:

```bash
# Check package.json for test scripts
Grep: "test" in package.json scripts section

# Check for test config
Glob: vitest.config.*, jest.config.*, playwright.config.*
```

If test tooling is not configured:
```markdown
🚫 **Test tooling not detected**

No test runner configuration found. Expected one of:
- vitest.config.ts
- jest.config.ts
- playwright.config.ts

Set up testing before running QA verification.
```

---

## Dimension 1: Test Coverage Analysis

Invoke the `quality-engineer` agent to analyze test coverage.

### Task for quality-engineer

```
Run test coverage and analyze results:

1. Execute: pnpm test:coverage (or equivalent)
2. Parse coverage output (lcov, istanbul, v8)
3. Compare per-file coverage against thresholds:
   - Lines: 95%
   - Functions: 95%
   - Statements: 95%
   - Branches: 90%
4. Identify files below threshold
5. Calculate overall project coverage
6. List uncovered lines/branches for critical files

Report:
- Overall coverage percentages
- Files below threshold with current vs target
- Uncovered critical code paths
```

### Expected Output

- Overall line/function/statement/branch coverage
- Per-file coverage for files below threshold
- List of uncovered critical paths
- Coverage delta from previous run (if available)

---

## Dimension 2: Test Quality Assessment

Invoke the `quality-engineer` agent to evaluate test quality beyond coverage numbers.

### Task for quality-engineer

```
Analyze test quality across the codebase:

1. Check test descriptions are meaningful (not "test 1", "it works")
2. Verify assertions are present (no empty test bodies)
3. Check happy path AND error path coverage per feature
4. Identify over-mocking (tests that mock everything, testing nothing)
5. Calculate test-to-code ratio (target: 1:1 to 2:1)
6. Check for flaky test patterns (setTimeout, race conditions)
7. Verify test isolation (no shared state between tests)

Report:
- Test description quality score
- Assertion density (assertions per test)
- Happy/error path ratio
- Over-mocking instances
- Test-to-code ratio
- Potential flaky tests
```

### Expected Output

- Test quality score (0-100)
- Specific quality issues with file references
- Tests that need improvement

---

## Dimension 3: Acceptance Criteria Test Mapping

> **Note**: `/sdlc:review` Dimension 4 also traces acceptance criteria to tests, but from a traceability perspective (does a test exist?). This dimension focuses on *test quality* — are the tests sufficient, meaningful, and covering both happy and error paths?

Invoke the `quality-engineer` agent to map user stories to test coverage.

### Task for quality-engineer

```
Read docs/req/user-stories.md. For each user story:

1. Find test files that exercise the feature described in the story
2. For each acceptance criterion, find a test assertion that verifies it
3. Flag criteria with no corresponding test
4. Flag criteria with only partial test coverage

Produce a mapping:
| Story ID | Criterion | Test File | Test Name | Coverage |
```

### Expected Output

- Total acceptance criteria count
- Criteria fully covered by tests
- Criteria partially covered
- Criteria with no coverage
- Overall acceptance criteria coverage percentage

---

## Dimension 4: E2E / Integration Test Gaps

Invoke the `quality-engineer` agent to identify missing end-to-end and integration tests.

### Task for quality-engineer

```
Analyze E2E and integration test coverage:

1. Read activity diagrams and user flows from planning artifacts
2. Map critical user paths (login, core workflows, checkout, etc.)
3. Check if E2E tests exist for each critical path
4. Check if integration tests exist for each API endpoint
5. Identify user paths with no E2E coverage
6. Check if E2E tests cover both success and failure scenarios

Report:
- Critical user paths identified
- E2E test coverage per path
- API endpoints without integration tests
- Uncovered critical paths (prioritized)
```

### Expected Output

- Critical path count and coverage
- API endpoint integration test coverage
- Prioritized list of gaps

---

## Dimension 5: Security Verification

This dimension uses a two-step process: the skill runs shell commands (which require Bash), then invokes the `security-engineer` agent to analyze code patterns (which requires Grep/Glob/Read).

### Step 1: Run Security Commands (skill-level, not agent)

The skill itself runs these commands before invoking the agent:

```bash
# Dependency audit
pnpm audit --json > /tmp/audit-results.json 2>&1 || true

# Check for committed secrets (basic patterns)
grep -rn "password\s*=\s*['\"]" --include="*.ts" --include="*.js" || true
grep -rn "apiKey\s*=\s*['\"]" --include="*.ts" --include="*.js" || true
grep -rn "secret\s*=\s*['\"]" --include="*.ts" --include="*.js" || true
```

Parse the audit output for critical/high/medium/low counts.

### Step 2: Invoke security-engineer for Code Analysis

```
Analyze the codebase for security vulnerabilities (do NOT run shell commands — audit results are provided separately):

Audit results: {paste parsed audit summary}

Using Grep and Glob, search for:
1. Common vulnerability patterns:
   - SQL injection (string concatenation in queries)
   - XSS (unsanitized user input in HTML)
   - CSRF (missing CSRF tokens on state-changing endpoints)
   - Path traversal (unsanitized file paths)
   - Command injection (unsanitized shell commands)
2. Auth middleware on protected routes
3. Committed secrets:
   - API keys, tokens, passwords in source code
   - .env files committed to git
   - Private keys in repository
4. Security headers (CORS, CSP, HSTS)

Report:
- Vulnerability pattern findings with file references
- Auth middleware coverage
- Secret scan results
- Security header status
```

### Expected Output

- Dependency vulnerability counts by severity
- Code vulnerability findings
- Auth coverage status
- Secret scan results
- Overall security score

---

## Dimension 6: Static Analysis

Invoke the `quality-engineer` agent to run static analysis tools.

### Task for quality-engineer

```
Run static analysis tools and compare against thresholds:

1. Execute: pnpm lint (ESLint)
   - Count errors and warnings
   - Identify most common violations
2. Execute: pnpm typecheck (TypeScript)
   - Count type errors
   - List files with errors
3. Execute: pnpm depcruise (dependency-cruiser, if configured)
   - Check for circular dependencies
   - Identify dependency violations
4. Execute: pnpm knip (if configured)
   - Find unused exports
   - Find unused dependencies
   - Find unused files
5. Check complexity metrics:
   - Functions exceeding cyclomatic complexity threshold (<=10)
   - Functions exceeding nesting depth threshold (<=3)
   - Files exceeding line count threshold (<=300)

Report:
- Lint error/warning counts
- Type error counts
- Circular dependency count
- Unused code findings
- Complexity violations
```

### Expected Output

- Lint status (pass/fail with counts)
- Type check status (pass/fail with counts)
- Circular dependencies found
- Dead code findings
- Complexity violations with file references

---

## QA Report Generation

After all dimensions complete, generate the QA report.

### Calculate Quality Score

Weighted quality score (0-100):

| Dimension | Weight | Score |
|-----------|--------|-------|
| Test Coverage | 25% | {0-100 based on threshold compliance} |
| Test Quality | 20% | {0-100 from quality assessment} |
| Acceptance Criteria | 15% | {0-100 based on coverage %} |
| E2E/Integration Gaps | 15% | {0-100 based on critical path coverage} |
| Security | 15% | {0-100, 0 if critical vulns} |
| Static Analysis | 10% | {0-100 based on violations} |

**Overall** = weighted sum

### Write Report

Write to `docs/qa/qa-report-YYYY-MM-DD.md`:

```markdown
# QA Report

**Date**: {YYYY-MM-DD}
**Run ID**: {unique-id}
**Quality Score**: {score}/100

## Executive Summary

**Overall Status**: {PASS | CONDITIONAL PASS | FAIL}

{1-3 sentence summary}

## Quality Score Breakdown

| Dimension | Weight | Score | Status |
|-----------|--------|-------|--------|
| Test Coverage | 25% | {score} | {PASS/FAIL} |
| Test Quality | 20% | {score} | {PASS/FAIL} |
| Acceptance Criteria | 15% | {score} | {PASS/FAIL} |
| E2E/Integration | 15% | {score} | {PASS/FAIL} |
| Security | 15% | {score} | {PASS/FAIL} |
| Static Analysis | 10% | {score} | {PASS/FAIL} |
| **Overall** | **100%** | **{score}** | **{status}** |

## Dimension 1: Test Coverage

**Overall Coverage**:
- Lines: {pct}% (threshold: 95%)
- Functions: {pct}% (threshold: 95%)
- Statements: {pct}% (threshold: 95%)
- Branches: {pct}% (threshold: 90%)

**Files Below Threshold**:
| File | Lines | Functions | Branches | Gap |
|------|-------|-----------|----------|-----|
| {file} | {pct}% | {pct}% | {pct}% | {details} |

## Dimension 2: Test Quality

{Quality assessment findings}

## Dimension 3: Acceptance Criteria Coverage

**Coverage**: {covered}/{total} criteria ({pct}%)

| Story | Criterion | Test | Status |
|-------|-----------|------|--------|
| {id} | {criterion} | {test} | {covered/missing} |

## Dimension 4: E2E / Integration Gaps

**Critical Paths Covered**: {covered}/{total}

{Gap details}

## Dimension 5: Security

**Dependency Audit**:
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}

**Code Vulnerabilities**: {count}
**Secret Scan**: {CLEAN / findings}

## Dimension 6: Static Analysis

- **Lint**: {errors} errors, {warnings} warnings
- **TypeCheck**: {errors} errors
- **Circular Dependencies**: {count}
- **Dead Code**: {count} unused exports

## Recommended Actions

### Critical (Must Fix Before Release)
1. {action}

### High (Fix This Sprint)
1. {action}

### Medium (Fix Next Sprint)
1. {action}

---

**Previous Score**: {score from last run, or "First run"}
**Trend**: {improving/declining/stable}
```

### Update Coverage Trend

Append to `docs/qa/coverage-trend.csv`:

```csv
date,quality_score,line_coverage,function_coverage,branch_coverage,lint_errors,type_errors,security_vulns,acceptance_criteria_pct
YYYY-MM-DD,{score},{line},{func},{branch},{lint},{type},{sec},{ac}
```

If the file doesn't exist, create it with the header row first.

---

## Fix-Forward Mode

After presenting the report, offer to generate fixes.

### Ask User

Use AskUserQuestion:

```markdown
## Fix-Forward Options

Based on the QA report, I can help fix these gaps:

1. **Generate test stubs** for uncovered acceptance criteria
2. **Scaffold E2E tests** for uncovered critical paths
3. **Fix lint violations** (auto-fixable ones)
4. **Update dependency vulnerabilities** (safe updates)

Which would you like me to do?
```

### Generate Test Stubs

For each uncovered acceptance criterion, generate a test stub:

```typescript
describe('{Story ID}: {Story Title}', () => {
  it('{acceptance criterion text}', () => {
    // TODO: Implement test for this acceptance criterion
    // Story: {story id}
    // Criterion: {criterion text}
    throw new Error('Test not implemented');
  });
});
```

### Scaffold E2E Tests

For each uncovered critical path, generate an E2E test skeleton:

```typescript
test('{critical path name}', async ({ page }) => {
  // TODO: Implement E2E test for critical path
  // Path: {path description}
  // Steps:
  // 1. {step 1}
  // 2. {step 2}
  // 3. {step 3}
  throw new Error('E2E test not implemented');
});
```

---

## State Management

Update `docs/sdlc.state.json` with QA checkpoint:

```json
{
  "qa": {
    "status": "completed",
    "lastRun": "YYYY-MM-DDTHH:mm:ss.sssZ",
    "history": [
      {
        "runId": "{unique-id}",
        "timestamp": "YYYY-MM-DDTHH:mm:ss.sssZ",
        "qualityScore": 85,
        "dimensions": {
          "testCoverage": { "status": "pass", "score": 90 },
          "testQuality": { "status": "pass", "score": 80 },
          "acceptanceCriteria": { "status": "fail", "score": 70 },
          "e2eGaps": { "status": "pass", "score": 85 },
          "security": { "status": "pass", "score": 95 },
          "staticAnalysis": { "status": "pass", "score": 88 }
        },
        "overallStatus": "conditional_pass",
        "reportPath": "docs/qa/qa-report-YYYY-MM-DD.md"
      }
    ]
  }
}
```

---

## Client Presentation

After generating the report, present findings to the user.

### Sync to Storybook

If Storybook planning hub is configured:

```bash
cp docs/qa/qa-report-*.md packages/planning-hub/public/artifacts/qa/
```

### Present Summary

```markdown
## QA Verification Complete

**Quality Score**: {score}/100
**Status**: {PASS | CONDITIONAL PASS | FAIL}

| Dimension | Score | Status |
|-----------|-------|--------|
| Test Coverage | {score} | {status} |
| Test Quality | {score} | {status} |
| Acceptance Criteria | {score} | {status} |
| E2E/Integration | {score} | {status} |
| Security | {score} | {status} |
| Static Analysis | {score} | {status} |

**Top Issues**:
1. {most critical finding}
2. {second most critical}
3. {third most critical}

**Report**: docs/qa/qa-report-{date}.md
```

### Ask for Next Steps

Use AskUserQuestion:

1. **Fix issues** — Address findings and re-run `/sdlc:qa`
2. **Generate test stubs** — Auto-generate missing tests (fix-forward)
3. **Accept and proceed** — Acknowledge results and continue
4. **Run /sdlc:review** — Also verify design conformance

---

## Error Handling

### Test Runner Not Configured

```markdown
🚫 **Cannot run tests**

No test runner detected. Configure Vitest, Jest, or another test framework first.

Expected scripts in package.json:
- test
- test:coverage
```

### Coverage Tool Not Available

```markdown
⚠️ **Coverage reporting not available**

Test runner is configured but coverage is not.

Add coverage configuration to your test config:
- Vitest: { coverage: { provider: 'v8' } }
- Jest: { collectCoverage: true }
```

### Lint/TypeCheck Not Configured

```markdown
⚠️ **Static analysis tools not configured**

Missing: {pnpm lint | pnpm typecheck | pnpm depcruise | pnpm knip}

Proceeding with available tools only. Configure missing tools for full QA coverage.
```

### No Quality Model

```markdown
⚠️ **No quality model found**

docs/quality/quality-model.md not found.
Using default thresholds (95/95/95/90 coverage, complexity <=10).

Run /sdlc:plan to generate a project-specific quality model.
```

---

## Tool Usage

- **Read**: Load quality model, test plan, state file, test results
- **Write**: Create QA reports, coverage trend CSV, test stubs
- **Edit**: Update state file, append to trend CSV
- **Bash**: Run test coverage, lint, typecheck, audit, depcruise, knip
- **Glob**: Find test files, source files, config files
- **Grep**: Search for test patterns, vulnerability patterns, secrets
- **Task**: Invoke quality-engineer, security-engineer agents
- **AskUserQuestion**: Present results, offer fix-forward options

---

## Success Criteria

A QA run is successful when:

- [ ] Pre-flight checks completed
- [ ] All applicable dimensions evaluated
- [ ] Quality score calculated
- [ ] QA report generated with per-dimension results
- [ ] Coverage trend data appended
- [ ] State file updated with QA checkpoint
- [ ] User informed of findings and quality score
- [ ] Fix-forward options offered if gaps found
- [ ] Report preserved for historical tracking
