---
name: trace-requirements
description: Create comprehensive bidirectional requirements traceability matrix mapping acceptance criteria → implementation → tests with gap analysis, severity ratings, and coverage assessment. Maps each AC to implementation evidence (files, functions, code snippets) and test coverage (test files, scenarios, priorities). Use during quality review or for compliance audits to verify complete requirements coverage.
version: 2.0
category: Quality
acceptance:
  forward_traceability: "All acceptance criteria mapped to implementation evidence with file paths, line ranges, function names, and code snippets demonstrating implementation"
  backward_traceability: "All tests mapped to acceptance criteria they validate with test files, scenarios, types (unit/integration/E2E), and priorities (P0/P1/P2)"
  gaps_identified: "Coverage gaps identified and classified by type (implementation/test), severity (CRITICAL/HIGH/MEDIUM/LOW), and priority (P0/P1/P2) with required actions"
  traceability_report_generated: "Complete traceability report generated with matrix, detailed entries, gap analysis, recommendations, and quality gate impact assessment"
inputs:
  task_id:
    type: string
    required: true
    description: "Task identifier for traceability analysis (e.g., 'task-007')"
  task_file:
    type: string
    required: true
    description: "Path to task specification file"
  implementation_path:
    type: string
    required: false
    description: "Path to implementation code (defaults to project root)"
  test_path:
    type: string
    required: false
    description: "Path to test files (defaults to test directory)"
  risk_profile_file:
    type: string
    required: false
    description: "Path to risk profile file (for risk-informed gap severity)"
  test_design_file:
    type: string
    required: false
    description: "Path to test design file (for expected test scenarios)"
outputs:
  total_acceptance_criteria:
    type: number
    description: "Total number of acceptance criteria analyzed"
  implementation_coverage_percentage:
    type: number
    description: "Percentage of ACs with implementation evidence (0-100)"
  test_coverage_percentage:
    type: number
    description: "Percentage of ACs with test coverage (0-100)"
  traceability_score:
    type: number
    description: "Overall traceability score (0-100)"
  total_gaps:
    type: number
    description: "Total number of coverage gaps identified"
  critical_gaps_count:
    type: number
    description: "Number of critical severity gaps"
  high_gaps_count:
    type: number
    description: "Number of high severity gaps"
  traceability_report_path:
    type: string
    description: "Path to generated traceability report"
  quality_gate_impact:
    type: string
    description: "Predicted quality gate status (PASS/CONCERNS/FAIL)"
telemetry:
  emit: "skill.trace-requirements.completed"
  track:
    - task_id
    - total_acceptance_criteria
    - implemented_count
    - partial_implementation_count
    - not_implemented_count
    - implementation_coverage_percentage
    - tested_count
    - partial_test_count
    - not_tested_count
    - test_coverage_percentage
    - total_gaps
    - critical_gaps_count
    - high_gaps_count
    - medium_gaps_count
    - low_gaps_count
    - traceability_score
    - risk_profile_available
    - test_design_available
---

# Requirements Traceability Analysis

Perform **bidirectional requirements traceability analysis** ensuring every acceptance criterion is implemented and tested. Creates audit-ready traceability matrix showing complete chain: Requirements → Implementation → Tests.

## Purpose

Create comprehensive traceability documentation that demonstrates:
- **Forward traceability:** AC → Implementation (with file/line evidence)
- **Backward traceability:** Tests → AC (with test scenario mapping)
- **Gap identification:** Missing implementation or test coverage
- **Severity assessment:** CRITICAL/HIGH/MEDIUM/LOW based on risk and impact
- **Coverage metrics:** Implementation coverage, test coverage, traceability score
- **Quality gate impact:** Prediction of gate status (PASS/CONCERNS/FAIL)

**Key Capabilities:**
- Evidence-based verification with file paths, line ranges, code snippets
- Integration with risk-profile (risk-informed gap severity)
- Integration with test-design (test-to-requirement mapping)
- Audit-ready documentation for compliance
- Actionable recommendations with effort estimates

## When to Use This Skill

**Best Used:**
- During implementation review to verify all requirements addressed
- Before quality gate to ensure completeness
- During audit preparation to demonstrate traceability
- After test-design to map tests to requirements
- When coverage gaps need identification and prioritization

**Integration Points:**
- Reads task specification for acceptance criteria
- Reads risk profile for risk-informed gap severity (optional)
- Reads test design for test-to-requirement mapping (optional)
- Reads actual implementation files for evidence
- Reads test files for test coverage verification

**Triggers:**
- User asks to "trace requirements", "check coverage", "verify AC implementation"
- Before quality gate (proactively suggest)
- During code review (verify completeness)

## Traceability Concepts

**Forward Traceability (AC → Implementation):** Maps each AC to implementation evidence (file, function, code snippet) | Status: ✅ Implemented, ⚠️ Partial, ❌ Not Implemented, ❓ Unclear

**Backward Traceability (Tests → AC):** Maps each test to ACs it validates | Status: ✅ Tested, ⚠️ Partial, ❌ Not Tested, 🔄 Indirect

**Gap Severity:** CRITICAL (9): Security/data integrity/core functionality | HIGH (6-8): Important requirements/P0 tests | MEDIUM (3-5): Minor requirements/P1 tests | LOW (1-2): Nice-to-have/P2 tests

**See:** `references/templates.md` for complete examples and classification details

## SEQUENTIAL Skill Execution

**CRITICAL:** Do not proceed to next step until current step is complete

### Step 0: Load Configuration and Context

**Purpose:** Load project configuration, task specification, and related assessments

**Actions:**

1. **Load configuration from `.claude/config.yaml`:**
   - Extract quality settings (assessmentLocation)
   - Extract risk score threshold (for gap severity assessment)

2. **Get task file path from user:**
   - Example: `.claude/tasks/task-006-user-signup.md`
   - Verify file exists and is readable

3. **Read task specification:**
   - Extract task ID, title, type
   - Load objective and context
   - **Load Acceptance Criteria** (primary traceability source)
   - Load Implementation Record section (files created/modified)
   - Load Quality Review section (if exists)

4. **Load related assessments (optional but enhances analysis):**
   - Risk profile: `.claude/quality/assessments/{task-id}-risk-*.md` (for gap severity)
   - Test design: `.claude/quality/assessments/{task-id}-test-design-*.md` (for test mapping)

5. **Identify implementation files:**
   - From task spec "Implementation Record" section
   - Files created/modified during implementation
   - Line ranges for each change

6. **Prepare output:**
   - Output directory: `.claude/quality/assessments/`
   - Output file: `{task-id}-trace-{YYYYMMDD}.md`
   - Template: `.claude/templates/trace-requirements.md` (if exists)

**Output:** Configuration loaded, task spec loaded with AC count, related assessments checked (risk profile/test design), implementation files identified, output path set

**Halt If:** Config missing, task file not found, no ACs, cannot create output

**See:** `references/templates.md#step-0-configuration-loading-output` for complete format

---

### Step 1: Build Forward Traceability Matrix (AC → Implementation)

**Purpose:** Map each acceptance criterion to its implementation evidence

**Actions:**

1. **For each acceptance criterion:**
   - Extract AC from task specification
   - Example: "AC-1: User can sign up with email and password"

2. **Search implementation files for evidence:**
   - Read each file from Implementation Record
   - Search for relevant code implementing the AC
   - Record file paths, line ranges, function/class names
   - Extract code snippets as evidence (5-10 lines context)

3. **Classify implementation status:**
   - ✅ **Implemented:** Clear evidence found in code
   - ⚠️ **Partial:** Some evidence but incomplete (e.g., validation missing)
   - ❌ **Not Implemented:** No evidence found
   - ❓ **Unclear:** Code exists but unclear if it satisfies AC

4. **Record evidence:** File paths, line ranges, function names, code snippets (5-10 lines) for each AC

5. **Calculate implementation coverage:**
   ```
   Implementation Coverage = (Implemented + 0.5 × Partial) / Total AC × 100%
   ```

**Output:** Forward traceability complete, AC counts by status, implementation coverage %

**Halt If:** Cannot read implementation files, >50% ACs unclear

**See:** `references/templates.md#step-1-forward-traceability-output` for complete format and examples

---

### Step 2: Build Backward Traceability Matrix (Tests → AC)

**Purpose:** Map each test to the acceptance criteria it validates

**Actions:**

1. **Identify test files:**
   - From test-design assessment (if available)
   - From Implementation Record (test files created)
   - From convention: `**/*.test.ts`, `**/*.spec.ts`, `**/__tests__/*`

2. **For each test file, extract test cases:**
   - Read test file
   - Extract test names from `it()`, `test()`, `describe()` blocks
   - Extract test scenarios (Given-When-Then if present)

   Extract test names from `it()`, `test()`, `describe()` blocks

3. **Map tests to acceptance criteria:**
   - Analyze test name and assertions
   - Determine which AC(s) the test validates
   - A single test can validate multiple ACs
   - An AC typically has multiple tests (happy path, edge cases, errors)

   Map tests to ACs (analyze test name + assertions, single test can validate multiple ACs)

4. **Classify test coverage:**
   - ✅ **Tested:** AC has at least one test validating it
   - ⚠️ **Partial:** AC has tests but not all scenarios covered (e.g., only happy path)
   - ❌ **Not Tested:** AC has no tests
   - 🔄 **Indirect:** AC tested indirectly through E2E or other tests

5. **Calculate test coverage:**
   ```
   Test Coverage = (Tested + 0.5 × Partial) / Total AC × 100%
   ```

**Output:** Backward traceability complete, tested AC counts, total tests, test coverage %

**Halt If:** None (proceed even if no tests, will generate gaps)

**See:** `references/templates.md#step-2-backward-traceability-output` for complete format

---

### Step 3: Identify Coverage Gaps

**Purpose:** Identify and classify gaps in implementation and test coverage with severity ratings

**Actions:**

1. **Identify implementation gaps:**
   - ACs with status: Not Implemented, Partial, or Unclear
   - Document missing functionality
   - Estimate impact and effort

   Document missing functionality, estimate impact and effort

2. **Identify test gaps:**
   - ACs with test coverage: Not Tested or Partial
   - Document missing test scenarios
   - Identify missing edge cases, error cases, security tests

   Document missing test scenarios, identify edge cases/error cases

3. **Classify gap severity:**
   Use risk profile (if available) to inform severity:

   - **CRITICAL (Score 9):**
     - Security requirement not implemented or tested
     - Data integrity requirement missing
     - Core functionality not implemented
     - High-risk area (from risk profile) not tested

   - **HIGH (Score 6-8):**
     - Important requirement not implemented
     - Security test missing (but implementation exists)
     - Performance requirement not validated
     - P0 test missing

   - **MEDIUM (Score 3-5):**
     - Minor requirement not implemented
     - Edge case test missing
     - P1 test missing
     - Partial implementation without full test coverage

   - **LOW (Score 1-2):**
     - Nice-to-have requirement missing
     - P2 test missing
     - Documentation-only gap

4. **Cross-reference with risk profile (if available):**
   - Gaps in high-risk areas → Increase severity
   - Gaps with existing mitigation → Decrease severity
   - Gaps without test coverage for high-risk area → CRITICAL

5. **Calculate gap metrics:**
   ```
   Total Gaps = Implementation Gaps + Test Gaps
   Critical Gaps = Gaps with severity CRITICAL
   High Gaps = Gaps with severity HIGH
   Medium Gaps = Gaps with severity MEDIUM
   Low Gaps = Gaps with severity LOW

   Gap Coverage = (Total AC - Total Gaps) / Total AC × 100%
   ```

**Output:**
```
⚠ Coverage gaps identified
⚠ Total Gaps: {count}
⚠ Critical: {count} (Security/core functionality issues)
⚠ High: {count} (Important requirements missing)
⚠ Medium: {count} (Minor gaps, edge cases)
⚠ Low: {count} (Nice-to-have items)
⚠ Gap Coverage: {percentage}%
```

**Halt Conditions:**
- More than 50% implementation gaps (incomplete implementation, not ready for traceability)

**Reference:** See [gap-analysis.md](references/gap-analysis.md) for gap classification and severity assessment

---

### Step 4: Create Traceability Matrix

**Purpose:** Build comprehensive bidirectional traceability matrix combining all data

**Actions:**

1. **Build full traceability matrix (table format):**
   ```markdown
   | AC | Requirement | Implementation | Tests | Gaps | Status |
   |----|-------------|----------------|-------|------|--------|
   | AC-1 | User can sign up with email and password | ✅ signup.ts:15-42 | ✅ 3 tests (P0) | None | ✅ Complete |
   | AC-2 | Password must be at least 8 characters | ✅ validators/auth.ts:23 | ⚠️ 1 test (missing edge cases) | GAP-2 (MEDIUM) | ⚠️ Partial |
   | AC-3 | Email must be validated | ✅ signup.ts:40, email.ts:12 | ✅ 2 tests (P1) | None | ✅ Complete |
   | AC-4 | Rate-limit login attempts | ❌ Not implemented | ❌ No tests | GAP-1 (HIGH) | ❌ Incomplete |
   ```

2. **Generate detailed entries for each AC:**
   ```markdown
   ## AC-1: User can sign up with email and password

   **Implementation Status:** ✅ Implemented

   **Implementation Evidence:**
   - **File:** src/routes/auth/signup.ts:15-42
   - **Function:** handleSignup()
   - **Description:** Implements signup endpoint accepting email/password,
                      hashing password, creating user, sending verification email
   - **Code Snippet:** [5-10 lines showing implementation]

   **Test Coverage:** ✅ Tested

   **Test Evidence:**
   1. **Test:** "should create user with valid email and password"
      - **File:** src/routes/auth/__tests__/signup.test.ts:12-24
      - **Type:** Integration, Priority: P0
      - **Scenario:** Given valid inputs, When signup, Then user created

   2. **Test:** "should return 400 for invalid email format"
      - **File:** src/routes/auth/__tests__/signup.test.ts:26-35
      - **Type:** Integration, Priority: P0
      - **Scenario:** Given invalid email, When signup, Then 400 error

   **Coverage Status:** ✅ Complete
   - Implementation: ✅ Complete
   - Tests: ✅ Complete (3 tests covering happy path, validation, errors)
   - Gaps: None
   ```

3. **Generate gap details:** Document each gap with severity, impact, required action, effort, priority

4. **Calculate overall traceability score:**
   ```
   Traceability Score = (
     (Implementation Coverage × 0.5) +
     (Test Coverage × 0.4) +
     (Gap Coverage × 0.1)
   )

   Example:
   - Implementation Coverage: 85%
   - Test Coverage: 80%
   - Gap Coverage: 90% (10% gaps)

   Traceability Score = (85 × 0.5) + (80 × 0.4) + (90 × 0.1)
                      = 42.5 + 32 + 9
                      = 83.5%
   ```

**Output:** Matrix complete with entry counts, traceability score

**Halt If:** None

**See:** `references/templates.md#complete-traceability-matrix-example` for matrix format

---

### Step 5: Generate Recommendations

**Purpose:** Provide actionable recommendations for closing gaps and improving traceability

**Actions:**

1. **Prioritize gaps:**
   Sort by:
   1. Severity (CRITICAL → HIGH → MEDIUM → LOW)
   2. Priority (P0 → P1 → P2)
   3. Effort (Small → Medium → Large)

2. **Generate action plan:** Prioritized actions (P0/P1/P2) with impact, effort, required actions, tests

3. **Quality gate impact assessment:** Determine status (PASS/CONCERNS/FAIL), provide reasoning, list actions to achieve PASS with effort estimates

4. **Best practices:** Future task guidance (TDD, reference AC IDs, update traceability), current task guidance (close P0 gaps, document waivers, re-run after fixes)

**Output:** Recommendations with P0/P1/P2 counts, effort estimates, quality gate prediction

**Halt If:** None

**See:** `references/templates.md` for recommendation formats and action plans

---

### Step 6: Generate Traceability Report and Present Summary

**Purpose:** Create comprehensive traceability report and present concise summary to user

**Actions:**

1. **Load template (if exists):**
   - Read `.claude/templates/trace-requirements.md`
   - Use default structure if template missing

2. **Populate template variables:**
   - Metadata: task ID, title, date, assessor
   - Metrics: implementation coverage, test coverage, traceability score
   - Counts: total AC, total gaps, critical/high/medium/low gaps
   - Data: traceability matrix, detailed entries, gap details, recommendations

3. **Generate file path:**
   - Format: `.claude/quality/assessments/{taskId}-trace-{YYYYMMDD}.md`
   - Example: `.claude/quality/assessments/task-006-trace-20251029.md`
   - Create directory if needed

4. **Write traceability report:**
   - Complete report with all sections
   - Validate all template variables replaced
   - No placeholder text remaining

5. **Present concise summary:** Task metadata, coverage metrics (implementation/test/gap/traceability score), gap breakdown by severity, quality gate impact + reasoning, actions to achieve PASS with estimates, report path, next steps

**Output:** Report generated at output path, summary presented

**Halt If:** File write fails

**See:** `references/templates.md#step-4-complete-summary-format` for full summary output

---

## Integration with Other Skills

### Integration with risk-profile

**Input:** Risk scores for high-risk areas | **Usage:** Gaps in high-risk areas → increase severity (e.g., HIGH → CRITICAL), missing tests for high-risk → CRITICAL

### Integration with test-design

**Input:** Test scenarios with priorities (P0/P1/P2), AC-to-test mappings | **Usage:** Validate test-to-AC mappings, identify missing test scenarios, use test priorities for gap severity

### Integration with quality-gate

**Output to quality-gate:**
- Traceability score (contributes to gate decision)
- Coverage gaps (may block gate if critical)
- Action items for closing gaps
- Evidence for requirements traceability dimension

**How quality-gate uses it:**
```markdown
Quality Gate Decision:
1. Check traceability score:
   - Score ≥95% → PASS
   - Score 80-94% → CONCERNS
   - Score <80% → FAIL

2. Check critical gaps:
   - 0 critical gaps → continue evaluation
   - 1+ critical gaps → CONCERNS (or FAIL if security)

3. Check overall coverage:
   - Implementation ≥90% AND Test ≥85% → PASS
   - Implementation ≥80% OR Test ≥70% → CONCERNS
   - Implementation <80% OR Test <70% → FAIL
```

## Best Practices

1. **Reference AC IDs in Code:**
   ```typescript
   // Implements AC-1: User signup with email and password
   export async function handleSignup(req: Request, res: Response) {
     // ...
   }
   ```

2. **Reference AC IDs in Commits:**
   ```bash
   git commit -m "feat: implement user signup (AC-1, AC-2, AC-3)"
   ```

3. **Reference AC IDs in Test Names:**
   ```typescript
   it('should satisfy AC-1: user can sign up with email and password', async () => {
     // ...
   });
   ```

4. **Run Before Code Review:**
   - Check traceability before marking task as "Review"
   - Close gaps before requesting review
   - Re-run trace-requirements after closing gaps

5. **Use for Audit Trail:**
   - Demonstrate requirements → implementation → test chain
   - Show evidence for compliance
   - Cross-reference with risk profile for risk coverage

## Configuration

### In `.claude/config.yaml`

```yaml
quality:
  # Quality assessment location
  assessmentLocation: ".claude/quality/assessments"

  # Risk score threshold for gap severity amplification
  riskScoreThreshold: 6  # Gaps in areas with risk ≥6 get higher severity

  # Traceability thresholds
  traceability:
    implementationCoverage: 90    # Minimum implementation coverage
    testCoverage: 85               # Minimum test coverage
    traceabilityScore: 80          # Minimum overall traceability score
```

### Template File

`.claude/templates/trace-requirements.md` - Template for traceability report output (optional)

---

**Version:** 2.0 (Refactored for skill-creator compliance and Minimal V2 architecture)
**Category:** Quality
**Depends On:** risk-profile (optional, enhances gap severity), test-design (optional, enhances test mapping)
**Used By:** quality-gate (uses traceability score and gaps for gate decision)
