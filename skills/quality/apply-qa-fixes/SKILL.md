---
name: apply-qa-fixes
description: Systematically consume QA quality gate outputs and apply prioritized fixes for high-severity issues, NFR failures, and test coverage gaps. Use when quality review identifies issues requiring remediation.
acceptance:
  - fixes_applied: "All prioritized fixes from quality gate applied successfully"
  - tests_passing: "All tests pass after fixes applied"
  - validation_clean: "Lint and tests run cleanly with no errors"
  - task_updated: "Task file Implementation Record section updated with fix details"
inputs:
  task_id:
    type: string
    required: true
    description: "Task identifier (e.g., task-001)"
  quality_gate_path:
    type: string
    required: false
    description: "Path to quality gate YAML file (auto-detected if not provided)"
  fix_scope:
    type: enum
    values: ["all", "high_severity", "nfr_only", "coverage_only"]
    default: "all"
    description: "Scope of fixes to apply"
outputs:
  fixes_applied:
    type: array
    description: "List of fixes applied with issue IDs and descriptions"
  tests_added:
    type: number
    description: "Number of tests added to close coverage gaps"
  coverage_improvement:
    type: object
    description: "Coverage improvement metrics (before/after percentages)"
  validation_passed:
    type: boolean
    description: "Whether lint and tests pass after fixes"
  files_modified:
    type: array
    description: "List of files modified during fix application"
telemetry:
  emit: "skill.apply-qa-fixes.completed"
  track:
    - task_id
    - fixes_count
    - tests_added
    - coverage_before
    - coverage_after
    - duration_ms
    - validation_passed
---

# Apply QA Fixes

Systematically consume QA quality gate outputs and apply prioritized fixes for issues identified during quality review.

## Purpose

After Quinn's quality review creates a quality gate with CONCERNS or FAIL status, this skill enables James to systematically consume the findings and apply fixes in a deterministic, prioritized manner.

**Core Principles:**
- **Deterministic prioritization** - Always same priority order (high severity → NFR failures → coverage gaps)
- **Minimal changes** - Fix exactly what's in the gate, don't over-engineer
- **Validation loop** - Always run tests after fixes, iterate until clean
- **Observability** - Track all fixes applied, tests added, coverage improvement

**Integration:**
- **Input:** Quality gate YAML + assessment reports from Quinn
- **Processing:** Parse findings → Build fix plan → Apply fixes → Validate
- **Output:** Fixed code + updated task file + telemetry

## When to Use This Skill

**This skill should be used when:**
- Quality gate status is CONCERNS or FAIL
- Quinn has identified specific issues requiring fixes
- Task is in Review status with completed implementation

**This skill should NOT be used when:**
- Quality gate is PASS (no fixes needed)
- Quality gate is WAIVED (intentionally accepted)
- Task implementation is incomplete
- Issues require architectural changes (escalate to user)

## Prerequisites

- Task file exists at `.claude/tasks/{task-id}.md`
- Quality gate exists at `.claude/quality/gates/{task-id}-gate-{date}.yaml`
- Assessment reports exist in `.claude/quality/assessments/`
- bmad-commands skill available
- Tests can be executed

---

## Workflow

### Step 0: Load Configuration and Quality Gate

**Purpose:** Load project configuration, locate task file, find latest quality gate, verify readiness.

**Actions:**

1. **Load Configuration:**
   ```bash
   python .claude/skills/bmad-commands/scripts/read_file.py \
     --path .claude/config.yaml \
     --output json
   ```

   Parse configuration to extract:
   - Quality directory paths
   - Test framework
   - Coverage thresholds

2. **Load Task File:**
   ```bash
   python .claude/skills/bmad-commands/scripts/read_file.py \
     --path .claude/tasks/{task_id}.md \
     --output json
   ```

   Verify task is ready for fixes:
   - Status is "Review" or "InProgress"
   - Implementation Record section exists
   - Quality Review section exists (from Quinn)

3. **Locate Latest Quality Gate:**

   Search `.claude/quality/gates/` for latest gate file:
   - Pattern: `{task-id}-gate-{date}.yaml`
   - Select most recent by date
   - Verify gate status is CONCERNS or FAIL

4. **Load Quality Gate:**
   ```bash
   python .claude/skills/bmad-commands/scripts/read_file.py \
     --path .claude/quality/gates/{gate_file} \
     --output json
   ```

   Parse gate YAML structure:
   - `decision` - Gate status (PASS/CONCERNS/FAIL/WAIVED)
   - `overall_score` - Quality score (0-100)
   - `dimensions` - Quality dimension scores
   - `top_issues` - High/medium/low severity issues
   - `nfr_validation` - NFR assessment results
   - `trace` - Traceability gaps
   - `test_design` - Test coverage gaps
   - `action_items` - Recommended actions

**Halt if:**
- Configuration missing
- Task file not found
- Quality gate not found
- Gate status is PASS or WAIVED (no fixes needed)

**See:** `references/templates.md` for gate schema and configuration format

---

### Step 1: Parse QA Findings

**Purpose:** Extract all issues from quality gate and assessment reports.

**Actions:**

1. **Parse Top Issues from Gate:**

   From `gate.yaml`:
   ```yaml
   top_issues:
     - id: "SEC-001"
       category: "security"
       severity: "high"
       description: "Missing input validation on user endpoint"
       location: "src/api/user.ts:45"
       recommendation: "Add Joi validation schema"
   ```

   Categorize by severity:
   - **High severity** - Security vulnerabilities, data loss risks, critical bugs
   - **Medium severity** - Performance issues, reliability concerns, code quality
   - **Low severity** - Minor improvements, style issues, warnings

2. **Parse NFR Failures:**

   From `gate.nfr_validation`:
   ```yaml
   nfr_validation:
     security:
       status: "FAIL"
       score: 45
       concerns:
         - "Missing SQL parameterization (src/db/queries.ts:23)"
         - "No rate limiting on API endpoints"
   ```

   Extract:
   - **FAIL** statuses (must fix)
   - **CONCERNS** (should fix)
   - Specific locations and recommendations

3. **Parse Test Coverage Gaps:**

   From `gate.test_design.coverage_gaps`:
   ```yaml
   coverage_gaps:
     - ac_id: "AC2"
       description: "User authentication flow"
       missing_tests:
         - "Should reject invalid credentials"
         - "Should handle expired tokens"
   ```

4. **Parse Traceability Gaps:**

   From `gate.trace.ac_gaps`:
   ```yaml
   ac_gaps:
     - ac_id: "AC4"
       description: "Secure password storage"
       coverage: "partial"
       missing: ["bcrypt hashing not implemented"]
   ```

**Outputs:**
- `high_severity_issues[]` - List of high severity issues with locations
- `medium_severity_issues[]` - List of medium severity issues
- `low_severity_issues[]` - List of low severity issues
- `nfr_failures[]` - NFR FAIL statuses with fixes needed
- `nfr_concerns[]` - NFR CONCERNS with recommended fixes
- `coverage_gaps[]` - Test scenarios to add
- `trace_gaps[]` - Uncovered acceptance criteria

**See:** `references/templates.md` for full gate schema and parsing examples

---

### Step 2: Build Fix Plan (Priority Order)

**Purpose:** Create deterministic, prioritized fix plan ensuring critical issues addressed first.

**Priority Rules:**

1. **Priority 1: High Severity Issues** (security, data loss, critical bugs)
2. **Priority 2: NFR Failures** (status = FAIL)
3. **Priority 3: Test Coverage Gaps** (P0 scenarios from test-design)
4. **Priority 4: NFR Concerns** (status = CONCERNS)
5. **Priority 5: Traceability Gaps** (uncovered ACs)
6. **Priority 6: Medium Severity Issues**
7. **Priority 7: Low Severity Issues**

**Within Same Priority:**
- Security > Performance > Reliability > Maintainability
- Alphabetical by issue ID

**Actions:**

1. **Build Priority List:**

   ```typescript
   fix_plan = [
     // Priority 1: High severity
     { priority: 1, issue_id: "SEC-001", type: "security", ... },
     { priority: 1, issue_id: "SEC-002", type: "security", ... },

     // Priority 2: NFR failures
     { priority: 2, issue_id: "NFR-SEC-001", type: "nfr_fail", ... },

     // Priority 3: Coverage gaps
     { priority: 3, issue_id: "TEST-001", type: "coverage_gap", ac_id: "AC2", ... },

     // ... continue for all priorities
   ]
   ```

2. **Calculate Impact:**

   For each fix, estimate:
   - Files to modify
   - Diff lines expected
   - Tests to add
   - Total effort

3. **Check Guardrails:**

   Verify fix plan doesn't exceed James's guardrails:
   - Max 10 files per fix session
   - Max 800 diff lines
   - If exceeded, split into multiple fix sessions or escalate

4. **Present Fix Plan to User:**

   ```
   === Fix Plan ===

   Total Issues: 15

   Priority 1 (High Severity): 3 issues
   - SEC-001: Missing input validation (src/api/user.ts)
   - SEC-002: SQL injection risk (src/db/queries.ts)
   - PERF-001: N+1 query issue (src/services/data.ts)

   Priority 2 (NFR Failures): 2 issues
   - NFR-SEC-001: No rate limiting
   - NFR-REL-001: Missing error logging

   Priority 3 (Coverage Gaps): 5 tests to add
   - AC2: User authentication flow (2 tests)
   - AC4: Secure password storage (3 tests)

   Estimated Impact:
   - Files to modify: 8
   - Tests to add: 5
   - Expected diff: ~600 lines

   Proceed with fixes? (y/n)
   ```

**Outputs:**
- `fix_plan[]` - Ordered list of fixes to apply
- `estimated_impact{}` - Files, lines, tests
- `guardrail_check{}` - Pass/fail status

**See:** `references/priority-rules.md` for detailed priority logic and `references/examples.md` for fix plan examples

---

### Step 3: Apply Fixes

**Purpose:** Apply fixes from plan using bmad-commands primitives and Claude Code tools.

**Actions:**

For each fix in `fix_plan` (in priority order):

1. **Load Affected Files:**

   Use Claude Code Read tool to load files needing modification:
   ```
   Read: src/api/user.ts
   Read: tests/api/user.test.ts
   ```

2. **Apply Code Fix:**

   Use Claude Code Edit tool to apply fix:
   ```
   Edit: src/api/user.ts
   Old: const user = await db.query(`SELECT * FROM users WHERE id = ${userId}`)
   New: const user = await db.query('SELECT * FROM users WHERE id = ?', [userId])
   ```

   **Principles:**
   - Minimal changes (fix exactly what's specified)
   - Follow project patterns (maintain consistency)
   - Add comments where needed (explain security fixes)
   - No over-engineering (don't refactor unrelated code)

3. **Add Missing Tests:**

   Use Claude Code Write tool to add test files:
   ```
   Write: tests/api/user-auth.test.ts
   Content: [Test scenarios from coverage_gaps]
   ```

   Use Edit tool to add tests to existing files:
   ```
   Edit: tests/api/user.test.ts
   Add tests for:
   - Should reject invalid credentials
   - Should handle expired tokens
   ```

4. **Track Progress:**

   Update todo list as fixes applied:
   ```
   ✅ Fix 1/15: Added input validation (SEC-001)
   ✅ Fix 2/15: Added SQL parameterization (SEC-002)
   ⏳ Fix 3/15: Adding rate limiting middleware...
   ```

**Error Handling:**

If fix fails:
- Log error with details
- Skip to next fix
- Report all failures at end
- Allow user to review and retry

**Outputs:**
- `fixes_applied[]` - List of successfully applied fixes
- `fixes_failed[]` - List of failed fixes with errors
- `files_modified[]` - All files changed
- `tests_added` - Count of new tests

**See:** `references/examples.md` for fix application examples

---

### Step 4: Validate

**Purpose:** Run tests and lint to verify fixes don't introduce regressions.

**Actions:**

1. **Run Lint:**

   ```bash
   # Lint check (exact command depends on project)
   npm run lint
   # or
   eslint src/
   ```

   Capture output:
   - Errors count
   - Warnings count
   - Files with issues

2. **Run Tests:**

   ```bash
   python .claude/skills/bmad-commands/scripts/run_tests.py \
     --path . \
     --framework auto \
     --output json
   ```

   Parse results:
   ```json
   {
     "success": true,
     "outputs": {
       "passed": true,
       "total_tests": 45,
       "tests_passed": 45,
       "tests_failed": 0,
       "coverage_percent": 89
     }
   }
   ```

3. **Check Coverage Improvement:**

   Compare before/after coverage:
   - Before: 82% (from quality gate)
   - After: 89%
   - Improvement: +7%

4. **Iterate if Needed:**

   If tests fail:
   - Identify failing tests
   - Debug issues
   - Apply additional fixes
   - Re-run tests
   - Maximum 3 iterations before escalating

**Halt if:**
- Tests still failing after 3 iterations
- Lint errors can't be resolved
- Coverage decreased (regression)

**Outputs:**
- `lint_passed` - Boolean
- `tests_passed` - Boolean
- `coverage_before` - Number
- `coverage_after` - Number
- `coverage_improvement` - Number
- `validation_clean` - Boolean

**See:** `references/templates.md` for validation report format

---

### Step 5: Update Task File

**Purpose:** Update task Implementation Record with fix details.

**STRICT PERMISSIONS:**

**AUTHORIZED to update:**
- Implementation Record section (what fixed, why, how)
- File List (add/modified/deleted files)
- Status (only if re-review needed: InProgress → Review)

**NOT AUTHORIZED to update:**
- Objective
- Acceptance Criteria
- Context
- Tasks
- Quality Review section (that's Quinn's territory)

**Actions:**

1. **Load Current Task File:**

   ```bash
   python .claude/skills/bmad-commands/scripts/read_file.py \
     --path .claude/tasks/{task_id}.md \
     --output json
   ```

2. **Generate Fix Summary:**

   ```markdown
   ### QA Fixes Applied (2025-01-15)

   **Quality Gate:** .claude/quality/gates/{task-id}-gate-{date}.yaml
   **Status Before:** CONCERNS (72/100)
   **Status After:** Ready for re-review

   **Fixes Applied (15 total):**

   **Priority 1 (High Severity):**
   1. SEC-001: Added input validation (src/api/user.ts:45)
   2. SEC-002: Added SQL parameterization (src/db/queries.ts:23)
   3. PERF-001: Fixed N+1 query (src/services/data.ts:67)

   **Priority 2 (NFR Failures):**
   4. NFR-SEC-001: Added rate limiting middleware
   5. NFR-REL-001: Added error logging and monitoring

   **Priority 3 (Coverage Gaps):**
   6-10. Added 5 missing tests for AC2, AC4

   **Priority 4-7:**
   11-15. Addressed medium/low severity issues

   **Validation Results:**
   - ✅ Lint: 0 problems
   - ✅ Tests: 45/45 passed
   - ✅ Coverage: 82% → 89% (+7%)

   **Files Modified:**
   - src/api/user.ts
   - src/db/queries.ts
   - src/services/data.ts
   - src/middleware/rate-limit.ts (new)
   - tests/api/user.test.ts
   - tests/api/user-auth.test.ts (new)
   - tests/db/queries.test.ts

   **Next Steps:**
   - Ready for Quinn re-review: @quinn *review {task-id}
   ```

3. **Update Implementation Record:**

   Use Edit tool to append fix summary to Implementation Record section:
   ```
   Edit: .claude/tasks/{task-id}.md
   Section: Implementation Record
   Action: Append QA fix summary
   ```

4. **Update File List:**

   Add newly created/modified files to task file list.

5. **Update Status (if needed):**

   If fixes require re-review:
   - Status: Review (keep in review)
   - Or Status: InProgress → Review (if was moved out of review)

**Outputs:**
- `task_updated` - Boolean
- `fix_summary` - Markdown text

**See:** `references/templates.md` for task update template

---

### Step 6: Emit Telemetry

**Purpose:** Track metrics for observability and learning.

**Actions:**

Emit structured telemetry:

```json
{
  "event": "skill.apply-qa-fixes.completed",
  "timestamp": "2025-01-15T10:30:00Z",
  "data": {
    "task_id": "task-001",
    "quality_gate": ".claude/quality/gates/task-001-gate-2025-01-15.yaml",
    "fixes_count": 15,
    "fixes_applied": {
      "high_severity": 3,
      "nfr_failures": 2,
      "coverage_gaps": 5,
      "nfr_concerns": 2,
      "medium_severity": 2,
      "low_severity": 1
    },
    "tests_added": 5,
    "coverage_before": 82,
    "coverage_after": 89,
    "coverage_improvement": 7,
    "files_modified": 7,
    "validation_passed": true,
    "duration_ms": 180000,
    "iterations": 1,
    "fixes_failed": 0
  }
}
```

**Metrics to Track:**
- Fixes count by priority
- Tests added
- Coverage improvement
- Files modified
- Validation success
- Duration
- Iterations needed
- Failed fixes

**Use Cases:**
- Track most common QA issues
- Identify patterns in fixes
- Measure fix effectiveness
- Monitor coverage improvement trends
- Optimize fix prioritization

---

## Execution Complete

Skill complete when:

- ✅ Quality gate loaded and parsed
- ✅ Fix plan built with deterministic prioritization
- ✅ All prioritized fixes applied (or documented failures)
- ✅ Tests added for coverage gaps
- ✅ Validation clean (lint + tests pass)
- ✅ Task file updated with fix summary
- ✅ Telemetry emitted

## Integration with James

**James Routing:**

```yaml
# In james-developer-v2.md

command: "*apply-qa-fixes"

routing_logic:
  - condition: "high_severity_count > 5 OR nfr_failures > 2"
    guardrails:
      max_files: 10
      max_diff_lines: 800
      require_user_confirmation: true

  - condition: "high_severity_count > 0 OR nfr_failures > 0"
    guardrails:
      max_files: 7
      max_diff_lines: 600

  - condition: "default"
    guardrails:
      max_files: 5
      max_diff_lines: 400
```

**Usage:**

```bash
# After Quinn review creates gate with CONCERNS/FAIL
@james *apply-qa-fixes task-001

# James:
# ✅ Quality gate loaded: CONCERNS (3 high, 2 medium issues)
# ✅ Fix plan created (5 fixes prioritized)
# ⏳ Applying fixes...
# ✅ All fixes applied
# ✅ Validation passed
# ✅ Task updated
#
# Ready for re-review: @quinn *review task-001
```

## Best Practices

1. **Always validate after fixes** - Don't skip test runs
2. **Follow priority rules strictly** - Ensures consistency
3. **Minimal changes only** - Fix what's specified, no more
4. **Document all fixes** - Update Implementation Record
5. **Track failures** - Log any fixes that can't be applied
6. **Re-review after fixes** - Always have Quinn re-assess

## When to Escalate

**Escalate to user when:**
- Fixes exceed guardrails (>10 files, >800 lines)
- Fixes require architectural changes
- Tests fail after 3 iterations
- Security concerns arise during fixes
- Breaking API changes required
- Conflicting fixes (can't satisfy all issues)

## References

- `references/templates.md` - Gate schema, task update template, output formats
- `references/priority-rules.md` - Detailed priority logic and decision rules
- `references/examples.md` - Fix application examples and usage scenarios

---

*Part of BMAD Enhanced Development Suite - Integrates with Quinn (Quality) for complete feedback loop*
