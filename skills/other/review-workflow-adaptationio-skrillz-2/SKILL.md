---
name: review-workflow
description: Complete quality assurance workflow orchestrating validation, comprehensive review, and functional testing. Sequential workflow from quality gating through multi-dimensional review to scenario testing. Use when conducting complete skill quality assurance, pre-deployment validation, or comprehensive quality checks combining multiple review approaches.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Review Workflow

## Overview

review-workflow provides complete quality assurance by orchestrating three complementary review skills into a comprehensive validation workflow.

**Purpose**: Complete quality assurance from quality gating through comprehensive review to functional testing

**Component Skills**:
1. **skill-validator** - Pass/fail quality gate (minimum standards)
2. **review-multi** - Comprehensive multi-dimensional review (1-5 scoring)
3. **skill-tester** - Functional testing in real scenarios

**Workflow Pattern**: Sequential (validator → review → testing)

**Result**: Complete quality assessment with deployment decision, quality scores, and functional validation

## When to Use

- Pre-deployment quality assurance (complete validation before release)
- Comprehensive quality checks (all aspects validated)
- Certification process (validate skill meets all standards)
- Major update validation (ensure quality maintained after changes)
- Quality audit (periodic comprehensive checks)

## Review Workflow

### Step 1: Quality Gate Validation (skill-validator)

**Purpose**: Fast pass/fail check - ensures minimum standards met before deeper review

**Component Skill**: skill-validator

**Process**:
1. Run skill-validator on skill
2. Check all 4 validation operations:
   - Structure validation
   - Content validation
   - Pattern validation
   - Production readiness
3. Result: PASS or FAIL

**Decision Point**:
- **PASS** → Proceed to Step 2 (comprehensive review)
- **FAIL** → Stop, fix critical issues, re-run Step 1

**Outputs**:
- Validation report (pass/fail)
- Critical issues list (if failed)
- Go/no-go decision

**Time Estimate**: 30-45 minutes

---

### Step 2: Comprehensive Review (review-multi)

**Purpose**: Multi-dimensional quality assessment with 1-5 scoring

**Component Skill**: review-multi

**Process**:
1. Run all 5 review operations:
   - Operation 1: Structure Review (5-10 min, automated)
   - Operation 2: Content Review (15-30 min, manual)
   - Operation 3: Quality Review (20-40 min, mixed)
   - Operation 4: Usability Review (30-60 min, manual testing)
   - Operation 5: Integration Review (15-25 min, manual)
2. Calculate weighted overall score
3. Map to grade (A/B/C/D/F)
4. Assess production readiness
5. Generate improvement recommendations

**Outputs**:
- Overall score (1.0-5.0)
- Grade (A/B/C/D/F)
- Per-dimension scores
- Production readiness assessment
- Prioritized improvement recommendations

**Time Estimate**: 1.5-2.5 hours

---

### Step 3: Functional Testing (skill-tester)

**Purpose**: Validate skill works correctly in real scenarios

**Component Skill**: skill-tester

**Process**:
1. Run testing operations:
   - Scenario Testing (test in realistic use case)
   - Example Validation (verify examples execute)
   - Integration Testing (test with other skills if applicable)
   - Usability Testing (assess ease of use)
2. Document test results
3. Identify any functional issues

**Outputs**:
- Scenario test results (success/failure)
- Example validation results (all pass/some fail)
- Integration test results
- Usability assessment
- Functional issues list (if any)

**Time Estimate**: 45-90 minutes

---

## Post-Workflow: Deployment Decision

After completing all 3 steps:

### Aggregate Results

**Quality Gate** (Step 1):
- PASS/FAIL status
- Critical issues (if any)

**Comprehensive Review** (Step 2):
- Overall score: X.X/5.0
- Grade: A/B/C/D/F
- Production readiness assessment
- Improvement recommendations

**Functional Testing** (Step 3):
- Scenario tests: Pass/Fail
- Examples: All working/Some broken
- Integration: Working/Issues
- Usability: Good/Needs improvement

### Make Deployment Decision

**Deploy Immediately**:
- Quality Gate: PASS
- Overall Score: ≥4.5 (Grade A)
- Functional Tests: All passing
- **Action**: Deploy to production

**Deploy with Notes**:
- Quality Gate: PASS
- Overall Score: 4.0-4.4 (Grade B+)
- Functional Tests: Passing
- **Action**: Deploy, note improvements for next iteration

**Hold for Improvements**:
- Quality Gate: PASS
- Overall Score: 3.5-3.9 (Grade B-)
- OR Functional Tests: Some failures
- **Action**: Fix identified issues, re-run workflow

**Do Not Deploy**:
- Quality Gate: FAIL
- OR Overall Score: <3.5 (Grade C-F)
- OR Functional Tests: Major failures
- **Action**: Significant rework required

---

## Best Practices

### 1. Always Run Complete Workflow
**Practice**: Run all 3 steps before deployment (don't skip)

**Rationale**: Each step catches different issues - comprehensive coverage

### 2. Fix Critical Issues Immediately
**Practice**: If Step 1 fails, fix issues before proceeding

**Rationale**: Wastes time to do comprehensive review on skill failing basic validation

### 3. Document All Findings
**Practice**: Record results from each step for complete record

**Rationale**: Enables tracking improvements over time, learning from patterns

### 4. Apply Improvements Iteratively
**Practice**: Use Step 2 recommendations to plan next version

**Rationale**: Continuous improvement - each iteration gets better

### 5. Re-Run After Major Changes
**Practice**: Re-run workflow after applying significant improvements

**Rationale**: Validates improvements effective, no regressions introduced

---

## Quick Reference

### The 3-Step Review Workflow

| Step | Skill | Purpose | Time | Output |
|------|-------|---------|------|--------|
| 1 | skill-validator | Quality gate (pass/fail) | 30-45m | PASS/FAIL, deploy decision |
| 2 | review-multi | Comprehensive review (1-5) | 1.5-2.5h | Score, grade, recommendations |
| 3 | skill-tester | Functional testing | 45-90m | Test results, functional validation |

**Total Time**: 3-4 hours for complete QA

### Workflow Pattern

```
skill-validator (Quality Gate)
    ↓
  PASS? ──No──> Fix issues, retry
    ↓ Yes
review-multi (Comprehensive Review)
    ↓
Overall Score + Grade + Recommendations
    ↓
skill-tester (Functional Testing)
    ↓
Test Results + Usability Assessment
    ↓
Deployment Decision (Deploy/Hold/Rework)
```

### Deployment Decision Matrix

| Validator | Review Score | Tests | Decision |
|-----------|--------------|-------|----------|
| PASS | ≥4.5 (A) | All Pass | ✅ Deploy Now |
| PASS | 4.0-4.4 (B+) | All Pass | ✅ Deploy + Note Improvements |
| PASS | 3.5-3.9 (B-) | Pass/Some Fail | ⚠️ Hold - Fix Issues |
| PASS | <3.5 (C-F) | Any | ❌ Rework Required |
| FAIL | Any | Any | ❌ Fix Critical, Retry |

### Integration with Development

```
Build skill (development-workflow) →
Review workflow (this skill) →
Apply improvements (skill-updater) →
Re-validate (review-workflow) →
Deploy
```

---

**review-workflow provides complete quality assurance through orchestrated validation, review, and testing.**
