---
name: ln-513-auto-test-planner
description: Plans automated tests (E2E/Integration/Unit) using Risk-Based Testing after manual testing. Calculates priorities, delegates to ln-301-task-creator. Worker for ln-510.
---

# Automated Test Planner

Creates Story test task with comprehensive automated test coverage (E2E/Integration/Unit) based on Risk-Based Testing methodology and REAL manual testing results.

## Purpose & Scope
- **Create** comprehensive test task for Story automation
- **Calculate** risk-based priorities (Impact × Probability)
- **Generate** 11-section test plan from manual test results
- **Delegate** to ln-301-task-creator (CREATE) or ln-302-task-replanner (REPLAN)
- **NOT** for: manual testing (ln-512), research (ln-511), orchestration (ln-510)

## When to Use This Skill

This skill should be used when:
- **Invoked by ln-510-test-planner** after ln-511 research and ln-512 manual testing
- All implementation tasks in Story are Done
- Manual testing results documented in Linear comment (from ln-512)
- Research findings available in Linear comment (from ln-511)

**Prerequisites:**
- All implementation Tasks in Story status = Done
- ln-511-test-researcher completed (research comment exists)
- ln-512-manual-tester completed (manual test results in Linear comment)

**Automation:** Supports `autoApprove: true` (default when invoked by ln-510) to skip manual confirmation.

## When NOT to Use

Do NOT use if:
- Manual testing NOT completed → Wait for ln-512
- Research NOT completed → Wait for ln-511
- Implementation tasks NOT all Done → Complete impl tasks first

## Workflow

### Phase 1: Discovery (Automated)

Auto-discovers Team ID from `docs/tasks/kanban_board.md` (see CLAUDE.md "Configuration Auto-Discovery").

**Input:** Story ID from orchestrator (ln-510)

### Phase 2: Story + Tasks Analysis (NO Dialog)

**Step 0: Study Project Test Files**
1. Scan for test-related files:
   - tests/README.md (commands, setup, environment)
   - Test configs (jest.config.js, vitest.config.ts, pytest.ini)
   - Existing test structure (tests/, __tests__/ directories)
   - Coverage config (.coveragerc, coverage.json)
2. Extract: test commands, framework, patterns, coverage thresholds
3. Ensures test planning aligns with project practices

**Step 1: Load Research and Manual Test Results**
1. Fetch Story from Linear (must have label "user-story")
2. Extract Story.id (UUID) - Use UUID, NOT short ID (required for Linear API)
3. Load research comment (from ln-511): "## Test Research: {Feature}"
4. Load manual test results comment (from ln-512): "## Manual Testing Results"
   - If not found → ERROR: Run ln-510-test-planner pipeline first
5. Parse sections: AC results (PASS/FAIL), Edge Cases, Error Handling, Integration flows
6. Map to test design: PASSED AC → E2E, Edge cases → Unit, Errors → Error handling, Flows → Integration

**Step 2: Analyze Story + Tasks**
1. Parse Story: Goal, Test Strategy, Technical Notes
2. Fetch **all child Tasks** (parentId = Story.id, status = Done) from Linear
3. Analyze each Task:
   - Components implemented
   - Business logic added
   - Integration points created
   - Conditional branches (if/else/switch)
4. Identify what needs testing

### Phase 3: Parsing Strategy for Manual Test Results

**Process:** Locate Linear comment with "Manual Testing Results" header → Verify Format Version 1.0 → Extract structured sections (Acceptance Criteria, Test Results by AC, Edge Cases, Error Handling, Integration Testing) using regex → Validate (at least 1 PASSED AC, AC count matches Story, completeness check) → Map parsed data to test design structure

**Error Handling:** Missing comment → ERROR (run ln-512 first), Missing format version → WARNING (try legacy parsing), Required section missing → ERROR (re-run ln-512), No PASSED AC → ERROR (fix implementation)

### Phase 4: Risk-Based Test Planning (Automated)

**Reference:** See `references/risk_based_testing_guide.md` for complete methodology.

**E2E-First Approach:** Prioritize by business risk (Priority = Impact x Probability), not coverage metrics.

**Workflow:**

**Step 1: Risk Assessment**

Calculate Priority for each scenario from manual testing:

```
Priority = Business Impact (1-5) x Probability (1-5)
```

**Decision Criteria:**
- Priority >=15 → **MUST test**
- Priority 9-14 → **SHOULD test** if not covered
- Priority <=8 → **SKIP** (manual testing sufficient)

**Step 2: E2E Test Selection (2-5):** Baseline 2 (positive + negative) ALWAYS + 0-3 additional (Priority >=15 only)

**Step 3: Unit Test Selection (0-15):** DEFAULT 0. Add ONLY for complex business logic (Priority >=15): financial, security, algorithms

**Step 4: Integration Test Selection (0-8):** DEFAULT 0. Add ONLY if E2E gaps AND Priority >=15: rollback, concurrency, external API errors

**Step 5: Validation:** Limits 2-28 total (realistic goal: 2-7). Auto-trim if >7 (keep 2 baseline + top 5 by Priority)

### Phase 5: Test Task Generation (Automated)

Generates complete test task per `test_task_template.md` (11 sections):

**Sections 1-7:** Context, Risk Matrix, E2E/Integration/Unit Tests (with Priority scores + justifications), Coverage, DoD

**Section 8:** Existing Tests to Fix (analysis of affected tests from implementation tasks)

**Section 9:** Infrastructure Changes (packages, Docker, configs - based on test dependencies)

**Section 10:** Documentation Updates (README, CHANGELOG, tests/README, config docs)

**Section 11:** Legacy Code Cleanup (deprecated patterns, backward compat, dead code)

Shows preview for review.

### Phase 6: Confirmation & Delegation

**Step 1:** Preview generated test plan (always displayed for transparency)

**Step 2:** Confirmation logic:
- **autoApprove: true** (default from ln-510) → proceed automatically
- **Manual run** → prompt user to type "confirm"

**Step 3:** Check for existing test task

Query Linear: `list_issues(parentId=Story.id, labels=["tests"])`

**Decision:**
- **Count = 0** → **CREATE MODE** (Step 4a)
- **Count >= 1** → **REPLAN MODE** (Step 4b)

**Step 4a: CREATE MODE** (if Count = 0)

Invoke ln-301-task-creator worker with taskType: "test"

**Pass to worker:**
- taskType, teamId, storyData (Story.id, title, AC, Technical Notes, Context)
- researchFindings (from ln-511 comment)
- manualTestResults (from ln-512 comment)
- testPlan (e2eTests, integrationTests, unitTests, riskPriorityMatrix)
- infrastructureChanges, documentationUpdates, legacyCleanup

**Worker returns:** Task URL + summary

**Step 4b: REPLAN MODE** (if Count >= 1)

Invoke ln-302-task-replanner worker with taskType: "test"

**Pass to worker:**
- Same data as CREATE MODE + existingTaskIds

**Worker returns:** Operations summary + warnings

**Step 5:** Return summary to orchestrator (ln-510)

---

## Definition of Done

**Research and Manual Results Loaded:**
- [ ] Research comment "## Test Research: {Feature}" found (from ln-511)
- [ ] Manual test results "## Manual Testing Results" found (from ln-512)
- [ ] At least 1 AC marked as PASSED

**Risk-Based Test Plan Generated:**
- [ ] Risk Priority Matrix calculated for all scenarios
- [ ] E2E tests (2-5): Baseline 2 + additional 0-3 with Priority >=15
- [ ] Integration tests (0-8): ONLY if E2E doesn't cover AND Priority >=15
- [ ] Unit tests (0-15): ONLY complex business logic with Priority >=15
- [ ] **Total tests: 2-7 realistic goal** (hard limit: 2-28)
- [ ] No framework/library testing: Each test validates OUR business logic only

**Test Task Description Complete (11 sections):**
- [ ] All 11 sections populated per template
- [ ] Risk Priority Matrix included
- [ ] Each test beyond baseline 2 justified

**Worker Delegation Executed:**
- [ ] CREATE MODE: Delegated to ln-301-task-creator
- [ ] REPLAN MODE: Delegated to ln-302-task-replanner
- [ ] Linear Issue URL returned

**Output:**
- **CREATE MODE:** Linear Issue URL + confirmation
- **REPLAN MODE:** Operations summary + URLs

## Reference Files

### risk_based_testing_guide.md

**Purpose**: Risk-Based Testing methodology

**Location**: [references/risk_based_testing_guide.md](references/risk_based_testing_guide.md)

### test_task_template.md (CENTRALIZED)

**Location**: `shared/templates/test_task_template.md`

**Usage**: Workers (ln-301, ln-302) load via Template Loading logic

## Best Practices

**Minimum Viable Testing:** Start with 2 E2E tests (positive + negative). Add more ONLY with critical justification. Realistic goal: 2-7 tests per Story.

**Risk-Based Testing:** Prioritize by Business Impact x Probability. E2E-first from ACTUAL manual testing results. Priority >=15 scenarios covered by tests.

**Expected-Based Testing:** For deterministic tests, compare actual vs expected using `diff`. See [ln-512-manual-tester Test Design Principles](../ln-512-manual-tester/SKILL.md#test-design-principles).

---

**Version:** 1.0.0 (Initial release - extracted from ln-510-test-planner)
**Last Updated:** 2026-01-15
