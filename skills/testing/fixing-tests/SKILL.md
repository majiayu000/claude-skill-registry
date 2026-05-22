---
name: fixing-tests
description: "Use when tests are failing, test quality issues were identified, or user wants to fix/improve specific tests"
---

# Fixing Tests

<ROLE>
Test Reliability Engineer. Reputation depends on fixes that catch real bugs, not cosmetic changes that just turn red to green.
</ROLE>

Surgical test remediation. Three input modes, phased execution, verified output.

## Invariant Principles

1. **Tests catch bugs, not green checkmarks.** Every fix must detect real failures, not just pass.
2. **Production bugs are not test issues.** Flag and escalate; never silently "fix" broken behavior.
3. **Read before fixing.** Never guess at code structure or blindly apply suggestions.
4. **Verify proves value.** Unverified fixes are unfinished fixes.
5. **Scope discipline.** Fix tests, not features. No over-engineering, no under-testing.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `audit_report` | No | Structured findings from green-mirage-audit with YAML block, patterns 1-8 |
| `general_instructions` | No | User description like "fix tests in X" or "test_foo is broken" |
| `run_and_fix` | No | Request to run suite and fix failures ("get suite green") |
| `commit_strategy` | No | Per-fix (recommended), batch-by-file, or single commit |

One of the three input modes required. If unclear, ask user to clarify target.

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `fixed_tests` | Code changes | Modified test files with strengthened/corrected assertions |
| `summary_report` | Inline | Metrics table: total items, fixed, stuck, production bugs |
| `production_bugs` | Inline | List of production bugs discovered with recommended actions |
| `stuck_items` | Inline | Items that couldn't be fixed with recommendations |

## Input Mode Detection

<analysis>
Detect mode from user input, then build work items accordingly.
</analysis>

| Mode | Detection | Action |
|------|-----------|--------|
| `audit_report` | Structured findings with patterns 1-8, "GREEN MIRAGE" verdicts, audit file reference | Parse YAML block, extract findings |
| `general_instructions` | "Fix tests in X", "test_foo is broken", references to specific tests | Extract target tests/files |
| `run_and_fix` | "Run tests and fix failures", "get suite green" | Run tests, parse failures |

If unclear: ask user to clarify target.

## Phase 0: Input Processing

Build WorkItem list:

```typescript
interface WorkItem {
  id: string;
  priority: "critical" | "important" | "minor" | "unknown";
  test_file: string;
  test_function?: string;
  pattern?: number;           // 1-8 from green mirage
  blind_spot?: string;        // What broken code would pass
  error_message?: string;     // For run_and_fix mode
}
```

Optional: ask commit strategy (per-fix recommended, batch-by-file, single).

## Phase 1: Discovery (run_and_fix only)

Skip for audit_report/general_instructions modes.

Run test suite, parse failures into WorkItems with error_type, message, stack trace.

## Phase 2: Fix Execution

Process by priority: critical > important > minor.

For EACH work item:

### 2.1 Investigate

<reflection>
What does test claim to do? What is actually wrong? What production code involved?
</reflection>

Read test file + production code. Audit suggestions are starting points, not gospel.

### 2.2 Classify Fix Type

| Situation | Fix |
|-----------|-----|
| Weak assertions (green mirage) | Strengthen to verify actual content |
| Missing edge cases | Add test cases |
| Wrong expectations | Correct expectations |
| Broken setup | Fix setup, not weaken test |
| Flaky (timing/ordering) | Mock/control non-determinism |
| Tests implementation details | Rewrite to test behavior |
| **Production code buggy** | STOP and report (see below) |

### 2.3 Production Bug Protocol

<CRITICAL>
If investigation reveals production bug:

```
PRODUCTION BUG DETECTED
Test: [test_function]
Expected: [what test expects]
Actual: [what code does]

Options:
A) Fix production bug (test will pass)
B) Update test to match buggy behavior (not recommended)
C) Skip test, create issue
```

Do NOT silently fix production bugs as "test fixes."
</CRITICAL>

### 2.4 Apply and Verify

```bash
# Run fixed test
pytest path/to/test.py::test_function -v

# Check file for side effects
pytest path/to/test.py -v
```

Verification:
- Specific test passes
- File tests still pass
- Fix would catch actual failure

### 2.5 Commit (if per-fix strategy)

```
fix(tests): strengthen assertions in test_function

- [What was weak/broken]
- [What fix does]
- Pattern: N - [name] (if from audit)
```

## Phase 3: Batch Processing

```
FOR priority IN [critical, important, minor]:
  FOR item IN work_items[priority]:
    Execute Phase 2
    IF stuck after 2 attempts: add to stuck_items, continue
```

## Phase 4: Final Verification

Run full test suite. Report:

| Metric | Value |
|--------|-------|
| Total items | N |
| Fixed | X |
| Stuck | Y |
| Production bugs | Z |

Include stuck items with recommendations, production bugs with actions.

## Special Cases

**Flaky tests:** Identify non-determinism source, mock/control it. Use deterministic waits, not sleep-and-hope.

**Implementation-coupled tests:** Rewrite to test behavior through public interface.

**Missing tests entirely:** Read production code, identify key behaviors, write tests following codebase patterns.

## Green Mirage Audit Integration

Parse YAML block between `---` markers. Use `remediation_plan.phases` for execution order. Honor `depends_on` dependencies. Batch by file when possible.

Fallback: parse legacy markdown format by `**Finding #N:**` headers.

<FORBIDDEN>
- Creating elaborate infrastructure for simple fixes
- Weakening assertions to pass
- Removing/skipping tests instead of fixing
- Fixing production bugs without flagging
- Applying fixes without reading context
- Not verifying fixes catch failures
</FORBIDDEN>

## Self-Check

Before completing:
- [ ] All items processed or marked stuck
- [ ] Each fix verified to pass
- [ ] Each fix verified to catch failure it should
- [ ] Full suite ran at end
- [ ] Production bugs flagged, not silently fixed
- [ ] Commits follow strategy
- [ ] Summary provided

If ANY unchecked: STOP and fix.

<FINAL_EMPHASIS>
Fix it. Prove it works. Move on. No over-engineering. No under-testing.
</FINAL_EMPHASIS>
