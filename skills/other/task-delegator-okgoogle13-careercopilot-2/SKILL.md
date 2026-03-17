---
name: task-delegator
description: "Delegate tasks to specialized agents and coordinate multi-agent workflows for parallel test generation"
---

# Task Delegator Skill - Jules Coordination

This skill coordinates parallel execution of test generation across 8 Jules instances for accelerated coverage improvement.

## Overview

**Purpose:** Orchestrate massive-scale test generation by delegating work to multiple Jules instances running in parallel

**Scope:** Manage 8 parallel batches (66 components) for Week 1 coverage acceleration

**Success Metric:** Week 1 target = 66 components tested, 53% coverage achieved

## Workflow Overview

### Phase 1: Preparation (Days 1-2)

**Step 1: Prepare Batch Configuration**

- Create 8 component batch lists (10-13 components each)
- Document batch characteristics:
  - Component count
  - Average test count per component (15-25 tests)
  - Expected pass rate (70%+ initially)
  - Special considerations (API mocks, Context, Portal, etc.)

**Step 2: Create Delegation Instructions**

- Generate prompt template for each batch
- Include component list with full paths
- Include success metrics and validation steps
- Include error handling and fallback procedures

**Step 3: Prepare Execution Environment**

- Verify jest-test-scaffolder skill is available
- Verify test-runner agent is configured
- Set up result consolidation process
- Create metrics tracking sheet

### Phase 2: Batch Configuration

**Batch 1: UI Components (Feedback)**

- Components: Dialog, Toast, EmptyState, Popover, Snackbar, Alert, Skeleton
- Count: 10-12 components
- Task: Generate tests with Material-UI theme setup
- Special: Most already have baseline tests, focus on edge cases
- Expected: 150-200 tests, 80%+ pass rate

**Batch 2: UI Components (Loading)**

- Components: LoadingSpinner, FullPageLoading, LoadingSkeleton, LinearProgress, CircularProgress
- Count: 8-10 components
- Task: Generate tests with Portal and positioning
- Special: Portal tests need jsdom workarounds
- Expected: 100-150 tests, 70%+ pass rate

**Batch 3: UI Components (Navigation)**

- Components: Sidebar, Navbar, Breadcrumbs, Tabs, Stepper, Pagination
- Count: 10-12 components
- Task: Generate tests with routing awareness
- Special: May need React Router context mocking
- Expected: 150-200 tests, 65%+ pass rate (routing complexity)

**Batch 4: UI Components (Surfaces)**

- Components: Card, Paper, Container, Grid, Box, Panel
- Count: 8-10 components
- Task: Generate basic render and variant tests
- Special: Simplest batch, should have high pass rate
- Expected: 120-150 tests, 85%+ pass rate

**Batch 5: Common Components**

- Components: Header, Footer, Layout, PageWrapper, Sidebar, NavBar
- Count: 8-10 components
- Task: Generate tests with composition and layout
- Special: May involve Context or layout calculations
- Expected: 120-150 tests, 70%+ pass rate

**Batch 6: Library Components**

- Components: Modal, Dropdown, Tooltip, Menu, Popover, DatePicker
- Count: 10-12 components
- Task: Generate tests with user interactions
- Special: Complex interactions, positioning tests
- Expected: 150-200 tests, 65%+ pass rate

**Batch 7: Feature Components**

- Components: Forms, FormGroup, FormControl, Inputs, Buttons, SelectField
- Count: 10-12 components
- Task: Generate tests with form interactions
- Special: React Hook Form integration, validation
- Expected: 150-200 tests, 60%+ pass rate (complexity)

**Batch 8: Career-Specific Components**

- Components: KSCGenerator, TailoredResumeGenerator, CoverLetterGenerator, ApplicationTracker
- Count: 10-12 components
- Task: Generate tests with API service mocks
- Special: Requires Firebase mock, Genkit mock
- Expected: 150-200 tests, 50%+ pass rate (highest complexity)

## Delegation Prompt Template

For each batch, use this structure:

```
You are testing a batch of React components for the CareerCopilot project.

BATCH INFORMATION:
- Batch: [N] ([Description])
- Components: [Count]
- Focus Area: [Special considerations]

COMPONENT LIST:
[List of 10-13 component paths with descriptions]

YOUR TASK:
1. For each component in the list above:
   a. Use jest-test-scaffolder skill to generate tests
   b. Run: yarn test [ComponentName] to verify
   c. Document pass rate and failures

2. Generate comprehensive test coverage:
   - Render tests (does it show up?)
   - Props tests (do props work?)
   - Interaction tests (do clicks work?)
   - State tests (do state variations work?)
   - Edge cases (empty props, null values, etc.)

3. Special Handling for Batch [N]:
   [Batch-specific instructions]

4. Document Results:
   - Components tested: [X]
   - Tests generated: [Y]
   - Pass rate: [Z]%
   - Failed tests: [List]
   - Blockers: [List]

TIMELINE:
- Expected time: 60-90 minutes per batch
- Target completion: End of Day 4
- Validation: Day 5 with test-runner

SUCCESS METRICS:
- 10-13 components tested
- 100-150 tests generated
- 60%+ pass rate minimum
- Clear documentation of failures
```

## Execution Steps (Days 3-4)

**Step 1: Launch Jules Instances (Simultaneous)**

```
Deploy 8 Jules instances at the same time:
- Instance 1: Batch 1 (Feedback components)
- Instance 2: Batch 2 (Loading components)
- Instance 3: Batch 3 (Navigation components)
- Instance 4: Batch 4 (Surfaces components)
- Instance 5: Batch 5 (Common components)
- Instance 6: Batch 6 (Library components)
- Instance 7: Batch 7 (Feature components)
- Instance 8: Batch 8 (Career components)
```

**Step 2: Monitor Execution**

- Track progress per batch
- Watch for early blockers
- Capture metrics: tests generated, pass rate, failures
- Document issues for Day 5 remediation

**Step 3: Capture Results**

- Save test files generated per batch
- Record pass/fail metrics
- Identify pattern blockers (e.g., "Portal not supported in jsdom")
- Create failure categorization (test bug vs code bug)

## Consolidation Steps (Day 5)

**Step 1: Merge Results**

- Collect test files from 8 batches
- Verify no duplicate testing
- Organize by component directory
- Commit batches to git

**Step 2: Validate with test-runner**

```
Run in parallel:
yarn test:ci          # Full test suite with coverage
yarn test:watch       # Watch for failures
npm run test:all      # All layers (frontend + e2e + backend)
```

**Step 3: Fix High-Impact Failures**

- Analyze failures from each batch
- Identify common patterns:
  - Jest configuration issues
  - Component implementation issues
  - Test pattern issues
  - Mock setup issues
- Prioritize fixes: Quick wins first (30 minutes)

**Step 4: Document Patterns**

- What worked well (high pass rate patterns)
- What needs special handling (Portal, Context, etc.)
- Reusable patterns for Week 2
- Update test-runner agent with new patterns

**Step 5: Generate Metrics Report**

```
WEEK 1 SUMMARY:
- Components tested: 66 (up from 10)
- Tests generated: 800-1200
- Pass rate: 60-70% (initial)
- Pass rate target: 50%+ (hit on first run)
- Coverage achieved: 53% (exceeded 50% target)

BATCH PERFORMANCE:
- Batch 1: X components, Y tests, Z% pass
- [... all 8 batches ...]

FAILURE CATEGORIES:
- Jest config issues: X
- Component bugs: Y
- Test pattern issues: Z
- Mock setup issues: W

LESSONS LEARNED:
- [Key insights for Week 2]
- [Pattern improvements needed]
- [Documentation updates needed]
```

## Quality Checkpoints

### Per-Batch Checkpoint (During Days 3-4)

- ✅ Component count matches batch config
- ✅ Tests generated for all components
- ✅ Test files in correct locations
- ✅ Metrics documented
- ✅ Blockers identified early

### Consolidation Checkpoint (Day 5)

- ✅ All 8 batches completed
- ✅ No duplicate tests
- ✅ Git history clean (8 commits, one per batch)
- ✅ 50%+ pass rate on first run
- ✅ Failure analysis complete
- ✅ Patterns documented

### Week 1 Success Checkpoint

- ✅ 66 components tested (up from 10)
- ✅ 800-1200 tests generated
- ✅ 53% coverage achieved (exceeded target)
- ✅ 50%+ pass rate on Week 1 output
- ✅ Test patterns documented and reusable
- ✅ Clear path to Week 2 fixes

## Handling Failures

### Common Batch Issues

**Issue: "Cannot find module" during test run**

- Cause: Component import path incorrect or component doesn't exist
- Solution: Verify component exists at path, check import in generated test
- Action: Fix import path in test file

**Issue: "Theme provider missing" error**

- Cause: Material-UI component needs ThemeProvider wrapper
- Solution: jest-test-scaffolder should handle this automatically
- Action: Verify setupTests.ts has ThemeProvider mock, add if missing

**Issue: "Portal is not supported" error**

- Cause: jsdom doesn't support React Portals
- Solution: Use snapshot test or skip positioning assertions
- Action: Document as "Portal components need jsdom workaround"

**Issue: High failure rate on entire batch**

- Cause: Systemic issue (bad batch config, bad component list, jest config)
- Solution: Stop batch, diagnose root cause, fix, restart
- Action: Flag for Day 5 investigation before scaling

### Recovery Procedures

**If a batch fails midway:**

1. Stop Jules instance for that batch
2. Investigate root cause (single component vs systemic)
3. Fix in staging environment
4. Restart batch with fixed configuration
5. Document fix for other batches

**If multiple batches show same error:**

1. Stop all instances
2. Diagnose: Is it jest config? setupTests.ts? jest-test-scaffolder?
3. Fix at source (not in individual batches)
4. Restart all instances with updated configuration

**If pass rate is very low (< 40%) on first run:**

1. Expected: 60-70% initial pass rate
2. If lower: May indicate component implementation bugs (not test bugs)
3. Action: Flag for Week 2 investigation with testing-specialist
4. Continue with remaining batches, collect data

## Metrics to Track

### Per Batch (Update continuously)

- Components assigned: [Number]
- Components completed: [Number]
- Tests generated: [Number]
- Tests passing: [Number]
- Pass rate: [X%]
- Blockers: [List]
- Special issues: [List]

### Daily (End of Days 1-2, 3-4, 5)

```
Date: [Day]
Batches active: [Number]
Total components: [Number]
Total tests: [Number]
Average pass rate: [X%]
Critical blockers: [Y]
Progress to target: [Z%]
```

### Weekly (End of Week 1)

```
Week 1 Summary:
- Starting coverage: 8.1% (10 components)
- Ending coverage: 53% (66 components)
- Coverage gain: +45 percentage points
- Tests added: 800-1200
- Pass rate achieved: 50%+ (target met on first run)
- Ready for Week 2: YES
```

## Success Indicators

### Immediate (During Execution)

- ✅ 8 Jules instances launch simultaneously on Day 3
- ✅ Each batch progresses independently
- ✅ Metrics captured per batch in real-time
- ✅ Issues documented for consolidation

### Short-term (Day 5 Consolidation)

- ✅ 66 components tested across 8 batches
- ✅ 800-1200 tests generated
- ✅ 50%+ pass rate achieved (exceeds target)
- ✅ Failure patterns identified and categorized
- ✅ Reusable patterns documented

### Long-term (Beyond Week 1)

- ✅ Patterns proven and documented for future scaling
- ✅ Week 2 fixes bring pass rate to 90%+
- ✅ 70+ components (56% coverage) by end of Week 2
- ✅ Path to 100% coverage clear and documented
- ✅ Cascade and testing-specialist agents have proven patterns

## References

**Related Skills:**

- jest-test-scaffolder: Component test generation
- test-runner: Test execution and validation
- testing-specialist: Complex component testing

**Documentation:**

- FAST_TRACK_DELEGATION_STRATEGY.md: Complete strategy overview
- TEST_RUNNER_GUIDE.md: Test command reference
- CLAUDE.md: Accelerated coverage improvement strategy

**Timeline:**

- Days 1-2: Preparation
- Days 3-4: Execution (8 parallel batches)
- Day 5: Consolidation and validation
- Week 1 Goal: 66 components, 53% coverage
- Week 2 Goal: 70+ components, 56% coverage
