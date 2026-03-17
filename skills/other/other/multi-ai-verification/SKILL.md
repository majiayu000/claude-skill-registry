---
name: multi-ai-verification
description: Multi-layer quality assurance with 5-layer verification pyramid (Rules → Functional → Visual → Integration → Quality Scoring). Independent verification with LLM-as-judge and Agent-as-a-Judge patterns. Score 0-100 with ≥90 threshold. Use when verifying code quality, security scanning, preventing test gaming, comprehensive QA, or ensuring production readiness through multi-layer validation.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Verification

## Overview

multi-ai-verification provides comprehensive quality assurance through a 5-layer verification pyramid, from automated rules to LLM-as-judge evaluation.

**Purpose**: Multi-layer independent verification ensuring production-ready quality

**Pattern**: Task-based (5 independent verification operations, one per layer)

**Key Innovation**: **5-layer pyramid** (95% automated at base → 0% at apex) with **independent verification** preventing bias and test gaming

**Core Principles** (validated by tri-AI research):
1. **Multi-Layer Defense** - 5 layers catch different types of issues
2. **Independent Verification** - Separate agent from implementation/testing
3. **Progressive Automation** - Automate what can be automated (95% → 0%)
4. **Quality Scoring** - Objective 0-100 scoring with ≥90 threshold
5. **Actionable Feedback** - 100% feedback is specific and actionable (What/Where/Why/How/Priority)

**Quality Gates**: All 5 layers must pass for production approval

---

## When to Use

Use multi-ai-verification when:

- Final quality check before commit/deployment
- Independent code review (preventing bias)
- Security verification (OWASP, vulnerabilities)
- Comprehensive QA (all layers)
- Test quality verification (prevent gaming)
- Production readiness validation

---

## Prerequisites

### Required
- Code to verify (implementation complete)
- Tests available (for functional verification)
- Quality standards defined

### Recommended
- **multi-ai-testing** - For generating/running tests
- **multi-ai-implementation** - For implementing fixes

### Tools Available
- Linters (ESLint, Pylint)
- Type checkers (TypeScript, mypy)
- Coverage tools (c8, pytest-cov)
- Security scanners (Semgrep, Bandit)
- Test frameworks (Jest, pytest)

---

## The 5-Layer Verification Pyramid

```
         Layer 5: Quality Scoring
         (LLM-as-Judge, 0-20% automated)
              /\
             /  \
        Layer 4: Integration
        (E2E, System, 20-30% automated)
          /      \
         /        \
    Layer 3: Visual
    (UI, Screenshots, 30-50% automated)
      /          \
     /            \
Layer 2: Functional
(Tests, Coverage, 60-80% automated)
  /              \
 /                \
Layer 1: Rules-Based
(Linting, Types, Schema, 95% automated)
```

**Principle**: Fail fast at automated layers (cheap, fast) before expensive LLM-as-judge evaluation

---

## Verification Operations

### Operation 1: Rules-Based Verification (Layer 1)

**Purpose**: Automated validation of code structure, formatting, types

**Automation**: 95% automated
**Speed**: Seconds (fast feedback)
**Confidence**: High (deterministic)

**Process**:

1. **Schema Validation** (if applicable):
   ```bash
   # Validate JSON/YAML against schemas
   ajv validate -s plan.schema.json -d plan.json
   ajv validate -s task.schema.json -d tasks/*.json
   ```

2. **Linting**:
   ```bash
   # JavaScript/TypeScript
   npx eslint src/**/*.{ts,tsx,js,jsx}

   # Python
   pylint src/**/*.py

   # Expected: Zero linting errors
   ```

3. **Type Checking**:
   ```bash
   # TypeScript
   npx tsc --noEmit

   # Python
   mypy src/

   # Expected: Zero type errors
   ```

4. **Format Validation**:
   ```bash
   # Check formatting
   npx prettier --check src/**/*.{ts,tsx}

   # Or auto-fix
   npx prettier --write src/**/*.{ts,tsx}
   ```

5. **Security Scanning** (SAST):
   ```bash
   # Static security analysis
   npx semgrep --config=auto src/

   # Or for Python
   bandit -r src/

   # Check for:
   # - Hardcoded secrets
   # - SQL injection risks
   # - XSS vulnerabilities
   # - Insecure dependencies
   ```

6. **Generate Layer 1 Report**:
   ```markdown
   # Layer 1: Rules-Based Verification

   ## Schema Validation
   ✅ plan.json validates
   ✅ All task files validate

   ## Linting
   ✅ 0 linting errors
   ⚠️ 3 warnings (non-blocking)

   ## Type Checking
   ✅ 0 type errors

   ## Formatting
   ✅ All files formatted correctly

   ## Security Scan (SAST)
   ✅ No critical vulnerabilities
   ⚠️ 1 medium: Weak password hashing rounds (bcrypt)

   **Layer 1 Status**: ✅ PASS (0 critical issues)
   **Issues to Address**: 1 medium security issue
   ```

**Outputs**:
- Lint report (errors/warnings)
- Type check results
- Schema validation results
- Security scan findings
- Layer 1 status (PASS/FAIL)

**Validation**:
- [ ] All automated checks run
- [ ] Results documented
- [ ] Critical issues = 0 for PASS
- [ ] Actionable feedback for warnings

**Time Estimate**: 15-30 minutes (mostly automated)

**Gate 1**: ✅ PASS if no critical issues (warnings acceptable)

---

### Operation 2: Functional Verification (Layer 2)

**Purpose**: Validate functionality through test execution and coverage

**Automation**: 60-80% automated
**Speed**: Minutes (medium feedback)
**Confidence**: High (measurable outcomes)

**Process**:

1. **Execute Complete Test Suite**:
   ```bash
   # Run all tests with coverage
   npm test -- --coverage --verbose

   # Capture results
   # - Tests passed/failed
   # - Coverage metrics
   # - Execution time
   ```

2. **Validate Example Code** (from documentation):
   ```bash
   # Extract examples from SKILL.md
   # Execute each example automatically
   # Verify outputs match expected

   # Target: ≥90% examples work
   ```

3. **Check Coverage**:
   ```markdown
   # Coverage Report

   **Line Coverage**: 87% ✅ (gate: ≥80%)
   **Branch Coverage**: 82% ✅
   **Function Coverage**: 92% ✅
   **Path Coverage**: 74% ✅

   **Gate Status**: PASS ✅ (all ≥80%)

   **Uncovered Code**:
   - src/admin/legacy.ts: 23% (low priority)
   - src/utils/deprecated.ts: 15% (deprecated, ok)
   ```

4. **Regression Testing** (for updates):
   ```bash
   # Compare before/after
   git diff main...feature --stat

   # Run all tests
   npm test

   # Verify: No new failures (regression prevention)
   ```

5. **Performance Validation**:
   ```bash
   # Run performance tests
   npm run test:performance

   # Check response times
   # Verify: Within acceptable ranges
   ```

6. **Generate Layer 2 Report**:
   ```markdown
   # Layer 2: Functional Verification

   ## Test Execution
   ✅ 245/245 tests passing (100%)
   ⏱️ Execution time: 8.3 seconds

   ## Coverage
   ✅ Line: 87% (gate: ≥80%)
   ✅ Branch: 82%
   ✅ Function: 92%

   ## Example Validation
   ✅ 18/20 examples work (90%)
   ❌ 2 examples fail (outdated)

   ## Regression
   ✅ All existing tests still pass

   ## Performance
   ✅ All endpoints <200ms

   **Layer 2 Status**: ✅ PASS
   **Issues**: 2 outdated examples (update docs)
   ```

**Outputs**:
- Test execution results
- Coverage report
- Example validation results
- Regression check
- Performance metrics
- Layer 2 status

**Validation**:
- [ ] All tests executed
- [ ] Coverage meets gate (≥80%)
- [ ] Examples validated (≥90%)
- [ ] No regressions
- [ ] Performance acceptable

**Time Estimate**: 30-60 minutes

**Gate 2**: ✅ PASS if tests pass + coverage ≥80%

---

### Operation 3: Visual Verification (Layer 3)

**Purpose**: Validate UI appearance, layout, accessibility (for UI features)

**Automation**: 30-50% automated
**Speed**: Minutes-Hours
**Confidence**: Medium (subjective elements)

**Process**:

1. **Screenshot Generation**:
   ```bash
   # Generate screenshots of UI
   npx playwright test --screenshot=on

   # Or manually:
   # Open application
   # Capture screenshots of key views
   ```

2. **Visual Comparison** (if previous version exists):
   ```bash
   # Compare against baseline
   npx playwright test --update-snapshots=missing

   # Or use Percy/Chromatic for visual regression
   npx percy snapshot screenshots/
   ```

3. **Layout Validation**:
   ```markdown
   # Visual Checklist

   ## Layout
   - [ ] Components positioned correctly
   - [ ] Spacing/margins match mockup
   - [ ] Alignment proper
   - [ ] No overlapping elements

   ## Styling
   - [ ] Colors match design system
   - [ ] Typography correct (fonts, sizes)
   - [ ] Icons/images display properly

   ## Responsiveness
   - [ ] Mobile view (320px-480px): ✅
   - [ ] Tablet view (768px-1024px): ✅
   - [ ] Desktop view (>1024px): ✅
   ```

4. **Accessibility Testing**:
   ```bash
   # Automated accessibility scan
   npx axe-core src/

   # Check WCAG compliance
   npx pa11y http://localhost:3000

   # Manual checks:
   # - Keyboard navigation
   # - Screen reader compatibility
   # - Color contrast ratios
   ```

5. **Generate Layer 3 Report**:
   ```markdown
   # Layer 3: Visual Verification

   ## Screenshot Comparison
   ✅ Login page matches mockup
   ✅ Dashboard layout correct
   ⚠️ Profile page: Avatar alignment off by 5px

   ## Responsiveness
   ✅ Mobile: All components visible
   ✅ Tablet: Layout adapts correctly
   ✅ Desktop: Full functionality

   ## Accessibility
   ✅ WCAG 2.1 AA compliance
   ✅ Keyboard navigation works
   ⚠️ 2 color contrast warnings (non-critical)

   **Layer 3 Status**: ✅ PASS (minor issues acceptable)
   **Issues**: Avatar alignment (cosmetic), contrast warnings
   ```

**Outputs**:
- Screenshots of UI
- Visual comparison results
- Responsiveness validation
- Accessibility report
- Layer 3 status

**Validation**:
- [ ] Screenshots captured
- [ ] Visual comparison done (if applicable)
- [ ] Layout validated
- [ ] Responsiveness tested
- [ ] Accessibility checked
- [ ] No critical visual issues

**Time Estimate**: 30-90 minutes (skip if no UI)

**Gate 3**: ✅ PASS if no critical visual/a11y issues

---

### Operation 4: Integration Verification (Layer 4)

**Purpose**: Validate system-level integration, data flow, API compatibility

**Automation**: 20-30% automated
**Speed**: Hours (complex)
**Confidence**: Medium-High

**Process**:

1. **Component Integration Tests**:
   ```bash
   # Run integration test suite
   npm test -- tests/integration/

   # Verify components work together
   # - Database ← → API
   # - API ← → Frontend
   # - Frontend ← → User
   ```

2. **Data Flow Validation**:
   ```markdown
   # Data Flow Verification

   **Flow 1: User Registration**
   Frontend form → API endpoint → Validation → Database → Email service
   ✅ Data flows correctly
   ✅ No data loss
   ✅ Transactions atomic

   **Flow 2: Authentication**
   Login request → API → Database lookup → Token generation → Response
   ✅ Token generated correctly
   ✅ Session stored
   ✅ Response includes token
   ```

3. **API Integration Tests**:
   ```bash
   # Test all API endpoints
   npm run test:api

   # Verify:
   # - All endpoints respond
   # - Status codes correct
   # - Response formats match spec
   # - Error handling works
   ```

4. **End-to-End Workflow Tests**:
   ```typescript
   // Complete user journeys
   test('Complete registration and login flow', async () => {
     // 1. Register new user
     const registerResponse = await api.post('/register', userData);
     expect(registerResponse.status).toBe(201);

     // 2. Confirm email
     const confirmResponse = await api.get(confirmLink);
     expect(confirmResponse.status).toBe(200);

     // 3. Login
     const loginResponse = await api.post('/login', credentials);
     expect(loginResponse.status).toBe(200);
     expect(loginResponse.data.token).toBeDefined();

     // 4. Access protected resource
     const profileResponse = await api.get('/profile', {
       headers: { Authorization: `Bearer ${loginResponse.data.token}` }
     });
     expect(profileResponse.status).toBe(200);
   });
   ```

5. **Dependency Compatibility**:
   ```bash
   # Check external dependencies work
   npm audit

   # Check for breaking changes
   npm outdated

   # Verify integration with services
   # - Database connection
   # - Redis/cache
   # - External APIs
   ```

6. **Generate Layer 4 Report**:
   ```markdown
   # Layer 4: Integration Verification

   ## Component Integration
   ✅ 12/12 integration tests passing
   ✅ All components integrate correctly

   ## Data Flow
   ✅ All 5 data flows validated
   ✅ No data loss or corruption

   ## API Integration
   ✅ All 15 endpoints functional
   ✅ Response formats correct
   ✅ Error handling works

   ## E2E Workflows
   ✅ 8/8 user journeys complete successfully
   ✅ No workflow breaks

   ## Dependencies
   ✅ 0 critical vulnerabilities
   ⚠️ 2 moderate (non-blocking)

   **Layer 4 Status**: ✅ PASS
   ```

**Outputs**:
- Integration test results
- Data flow validation
- API compatibility report
- E2E workflow results
- Dependency audit
- Layer 4 status

**Validation**:
- [ ] Integration tests pass
- [ ] Data flows validated
- [ ] APIs integrate correctly
- [ ] E2E workflows function
- [ ] Dependencies secure

**Time Estimate**: 45-90 minutes

**Gate 4**: ✅ PASS if all integration tests pass, no critical dependencies

---

### Operation 5: Quality Scoring (Layer 5)

**Purpose**: Holistic quality assessment using LLM-as-judge and Agent-as-a-Judge patterns

**Automation**: 0-20% automated
**Speed**: Hours (expensive)
**Confidence**: Medium (requires judgment)

**Process**:

1. **Spawn Independent Quality Assessor** (Agent-as-a-Judge):

   **Key**: Use different model family if possible (prevent self-preference bias)

   ```typescript
   const qualityAssessment = await task({
     description: "Assess code quality holistically",
     prompt: `Evaluate code quality in src/ and tests/.

     DO NOT read implementation conversation history.

     You have access to tools:
     - Read files
     - Execute tests
     - Run linters
     - Query database (if needed)

     Assess 5 dimensions (score each /20):

     1. CORRECTNESS (/20):
        - Logic correctness
        - Edge case handling
        - Error handling completeness
        - Security considerations

     2. FUNCTIONALITY (/20):
        - Meets all requirements
        - User workflows work
        - Performance acceptable
        - No regressions

     3. QUALITY (/20):
        - Code maintainability
        - Best practices followed
        - Anti-patterns avoided
        - Documentation complete

     4. INTEGRATION (/20):
        - Components integrate smoothly
        - API contracts correct
        - Data flow works
        - Backward compatible

     5. SECURITY (/20):
        - No vulnerabilities
        - Input validation
        - Authentication/authorization
        - Data protection

     TOTAL: /100 (sum of 5 dimensions)

     For each dimension, provide:
     - Score (/20)
     - Strengths (what's good)
     - Weaknesses (what needs improvement)
     - Evidence (file:line references)
     - Recommendations (specific, actionable)

     Write comprehensive report to: quality-assessment.md`
   });
   ```

2. **Multi-Agent Ensemble** (for critical features):

   **3-5 Agent Voting Committee**:
   ```typescript
   // Spawn 3 independent quality assessors
   const [judge1, judge2, judge3] = await Promise.all([
     task({description: "Quality Judge 1", prompt: assessmentPrompt}),
     task({description: "Quality Judge 2", prompt: assessmentPrompt}),
     task({description: "Quality Judge 3", prompt: assessmentPrompt})
   ]);

   // Aggregate scores
   const scores = {
     correctness: median([judge1.correctness, judge2.correctness, judge3.correctness]),
     functionality: median([...]),
     quality: median([...]),
     integration: median([...]),
     security: median([...])
   };

   const totalScore = sum(Object.values(scores)); // Total /100

   // Check variance
   const totalScores = [judge1.total, judge2.total, judge3.total];
   const variance = max(totalScores) - min(totalScores);

   if (variance > 15) {
     // High disagreement → spawn 2 more judges (total 5)
     // Use 5-agent ensemble for final score
   }

   // Final score: median of 3 or 5
   ```

3. **Calibration Against Rubric**:
   ```markdown
   # Scoring Calibration

   ## Correctness: 18/20 (Excellent)
   **20**: Zero errors, all edge cases handled perfectly
   **18**: Minor edge case missing, otherwise excellent ✅ (achieved)
   **15**: 1-2 significant edge cases missing
   **10**: Some logic errors present
   **0**: Major functionality broken

   **Evidence**: All tests pass, edge cases covered except timezone DST edge case (minor)

   ## Functionality: 19/20 (Excellent)
   [Similar rubric with evidence]

   ## Quality: 17/20 (Good)
   [Similar rubric with evidence]

   ## Integration: 18/20 (Excellent)
   [Similar rubric with evidence]

   ## Security: 16/20 (Good)
   [Similar rubric with evidence]

   **Total**: 88/100 ⚠️ (Below ≥90 gate)
   ```

4. **Gap Analysis** (if <90):
   ```markdown
   # Quality Gap Analysis

   **Current Score**: 88/100
   **Target**: ≥90/100
   **Gap**: 2 points

   ## Critical Gaps (Blocking Approval)
   None

   ## High Priority (Should Fix for ≥90)
   1. **Security: Weak bcrypt rounds**
      - **What**: bcrypt using 10 rounds (outdated)
      - **Where**: src/auth/hash.ts:15
      - **Why**: Current standard is 12-14 rounds
      - **How**: Change `bcrypt.hash(password, 10)` to `bcrypt.hash(password, 12)`
      - **Priority**: High
      - **Impact**: +2 points → 90/100

   ## Medium Priority
   1. **Quality: Missing JSDoc for 3 functions**
      - Impact: +1 point → 91/100

   **Recommendation**: Fix high priority issue to reach ≥90 threshold
   **Estimated Effort**: 15 minutes
   ```

5. **Generate Comprehensive Quality Report**:
   ```markdown
   # Layer 5: Quality Scoring Report

   ## Executive Summary
   **Total Score**: 88/100 ⚠️ (Below ≥90 gate)
   **Status**: NEEDS MINOR REVISION

   ## Dimension Scores
   - Correctness: 18/20 ⭐⭐⭐⭐⭐
   - Functionality: 19/20 ⭐⭐⭐⭐⭐
   - Quality: 17/20 ⭐⭐⭐⭐
   - Integration: 18/20 ⭐⭐⭐⭐⭐
   - Security: 16/20 ⭐⭐⭐⭐

   ## Strengths
   1. Comprehensive test coverage (87%)
   2. All functionality working correctly
   3. Clean integration with all components
   4. Good error handling

   ## Weaknesses
   1. Bcrypt rounds below current standard (security)
   2. Missing documentation for helper functions (quality)
   3. One timezone edge case not handled (correctness)

   ## Recommendations (Prioritized)

   ### Priority 1 (High - Needed for ≥90)
   1. Increase bcrypt rounds: 10 → 12
      - File: src/auth/hash.ts:15
      - Effort: 5 min
      - Impact: +2 points

   ### Priority 2 (Medium - Nice to Have)
   1. Add JSDoc to helper functions
      - Files: src/utils/validation.ts
      - Effort: 30 min
      - Impact: +1 point

   2. Handle timezone DST edge case
      - File: src/auth/tokens.ts:78
      - Effort: 20 min
      - Impact: +1 point

   **Next Steps**: Apply Priority 1 fix, re-verify to reach ≥90
   ```

**Outputs**:
- Quality score (0-100) with dimension breakdown
- Calibrated against rubric
- Gap analysis
- Prioritized recommendations (Critical/High/Medium/Low)
- Evidence-based feedback (file:line references)
- Action plan to reach ≥90

**Validation**:
- [ ] All 5 dimensions scored
- [ ] Scores calibrated against rubric
- [ ] Evidence provided for each score
- [ ] Gap analysis if <90
- [ ] Recommendations actionable
- [ ] Ensemble used for critical features (optional)

**Time Estimate**: 60-120 minutes (ensemble adds 30-60 min)

**Gate 5**: ✅ PASS if total score ≥90/100

---

## Quality Gates Summary

**All 5 Gates Must Pass** for production approval:

```
Gate 1: Rules Pass ✅
   ↓ (Linting, types, schema, security)

Gate 2: Tests Pass ✅
   ↓ (All tests, coverage ≥80%)

Gate 3: Visual OK ✅
   ↓ (UI validated, a11y checked)

Gate 4: Integration OK ✅
   ↓ (E2E works, APIs integrate)

Gate 5: Quality ≥90 ✅
   ↓ (LLM-as-judge score ≥90/100)

✅ PRODUCTION APPROVED
```

**If Any Gate Fails**:
```
Failed Gate → Gap Analysis → Apply Fixes → Re-Verify → Repeat Until Pass
```

---

## Appendix A: Independence Protocol

### How Verification Independence is Maintained

**Verification Agent Spawning**:
```typescript
// After implementation and testing complete
const verification = await task({
  description: "Independent quality verification",
  prompt: `Verify code quality independently.

  DO NOT read prior conversation history.

  Review:
  - Code: src/**/*.ts
  - Tests: tests/**/*.test.ts
  - Specs: specs/requirements.md

  Verify against specifications ONLY (not implementation decisions).

  Use tools:
  - Read files to inspect code
  - Run tests to verify functionality
  - Execute linters for quality checks

  Score quality (0-100) with evidence.
  Write report to: independent-verification.md`
});
```

**Bias Prevention Checklist**:
- [ ] Specifications written BEFORE implementation
- [ ] Verification agent prompt has no implementation context
- [ ] Agent evaluates against specs, not what code does
- [ ] Fresh context (via Task tool)
- [ ] Different model family used (if possible)

**Validation of Independence**:
```markdown
## Independence Audit

**Expected Behavior**:
- ✅ Verifier finds 1-3 issues (healthy skepticism)
- ✅ Verifier references specifications
- ✅ Verifier uses tools to verify claims

**Warning Signs**:
- ⚠️ Verifier finds 0 issues (possible rubber stamp)
- ⚠️ Verifier doesn't use tools
- ⚠️ Verifier parrots implementation justifications

**If Warning**: Re-verify with stronger independence prompt
```

---

## Appendix B: Operational Scoring Rubrics

### Complete Rubrics for All 5 Dimensions

#### Correctness (/20)

**20 (Perfect)**: Zero logic errors, all edge cases handled, security perfect
**18 (Excellent)**: 1 minor edge case missing, otherwise flawless
**15 (Good)**: 2-3 edge cases missing, no critical errors
**12 (Acceptable)**: Some edge cases missing, 1 minor logic issue
**10 (Needs Work)**: Multiple edge cases missing or 1 significant logic error
**5 (Poor)**: Major logic errors present
**0 (Broken)**: Critical functionality broken

#### Functionality (/20)

**20**: All requirements met, exceeds expectations
**18**: All requirements met, well implemented
**15**: All requirements met, basic implementation
**12**: 1 requirement partially missing
**10**: 2+ requirements partially missing
**5**: Several requirements not met
**0**: Core functionality missing

#### Quality (/20)

**20**: Exceptional code quality, best practices exemplified
**18**: High quality, follows best practices
**15**: Good quality, minor style issues
**12**: Acceptable quality, several style issues
**10**: Below standard, needs refactoring
**5**: Poor quality, significant issues
**0**: Unmaintainable code

#### Integration (/20)

**20**: Perfect integration, all touch points verified
**18**: Excellent integration, minor docs needed
**15**: Good integration, all major points work
**12**: Acceptable, 1-2 integration issues
**10**: Integration issues present
**5**: Multiple integration problems
**0**: Does not integrate

#### Security (/20)

**20**: Passes all security scans, OWASP compliant, hardened
**18**: Passes scans, 1 minor non-critical issue
**15**: Passes, 2-3 minor issues
**12**: 1 medium security issue
**10**: Multiple medium issues
**5**: 1 critical issue present
**0**: Multiple critical vulnerabilities

---

## Appendix C: Technical Foundation

### Verification Tools

**Linting**:
- ESLint (JavaScript/TypeScript)
- Pylint/Ruff (Python)

**Type Checking**:
- TypeScript compiler (tsc)
- mypy (Python)

**Security (SAST)**:
- Semgrep (multi-language)
- Bandit (Python)
- npm audit (JavaScript)

**Visual Testing**:
- Playwright (screenshot, visual regression)
- Percy/Chromatic (visual diff)
- axe-core (accessibility)

**Coverage**:
- c8/nyc (JavaScript)
- pytest-cov (Python)

### Cost Controls

**Budget Caps**:
- LLM-as-judge: $50/month
- Ensemble verification: $20/month
- Total verification: $70/month

**Optimization**:
- Cache quality scores for 24h (same code → same score)
- Skip Layer 5 for changes <50 lines
- Use ensemble (3-5 agents) only for critical features
- Use cheaper models for pre-filtering (Haiku for Layer 1-2)

---

## Quick Reference

### The 5 Layers

| Layer | Purpose | Automation | Time | Tools |
|-------|---------|------------|------|-------|
| 1 | Rules-based | 95% | 15-30m | Linters, types, SAST |
| 2 | Functional | 60-80% | 30-60m | Test execution, coverage |
| 3 | Visual | 30-50% | 30-90m | Screenshots, a11y |
| 4 | Integration | 20-30% | 45-90m | E2E, API tests |
| 5 | Quality Scoring | 0-20% | 60-120m | LLM-as-judge, ensemble |

**Total**: 3-6 hours for complete 5-layer verification

### Quality Thresholds

- **≥90**: ✅ Excellent (production-ready)
- **80-89**: ⚠️ Good (needs minor improvements)
- **70-79**: ❌ Acceptable (needs work before production)
- **<70**: ❌ Poor (significant rework required)

### Gates

**All 5 Must Pass**:
1. Rules pass (no critical lint/type/security)
2. Tests pass + coverage ≥80%
3. Visual OK (no critical UI issues)
4. Integration OK (E2E works)
5. Quality ≥90/100

---

**multi-ai-verification provides comprehensive, multi-layer quality assurance with independent LLM-as-judge evaluation, ensuring production-ready code through systematic verification from automated rules to holistic quality assessment.**

For rubrics, see Appendix B. For independence protocol, see Appendix A.
