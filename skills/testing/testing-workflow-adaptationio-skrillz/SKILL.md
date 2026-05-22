---
name: testing-workflow
description: Comprehensive testing workflow orchestrating functional testing, example validation, integration testing, and usability assessment. Sequential workflow for complete skill testing from examples through scenarios to integration validation. Use when conducting thorough testing, pre-deployment validation, ensuring skill functionality, or comprehensive quality checks.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Testing Workflow

## Overview

testing-workflow provides comprehensive skill testing by orchestrating skill-tester operations with validation checks.

**Component Skills**:
- **skill-tester** (all 4 operations)
- **skill-validator** (validation checks)

**Workflow** (4 steps):
1. **Example Validation** - All examples execute correctly
2. **Scenario Testing** - Test in real-world use cases
3. **Integration Testing** - Test with other skills
4. **Validation Check** - Ensure tests didn't reveal structural issues

**Result**: Complete functional validation ensuring skill works correctly

## When to Use

- Pre-deployment functional testing
- After implementing new features
- Validating examples and documentation
- Integration validation for workflow skills

## Testing Workflow

### Step 1: Example Validation
Extract and execute all examples from skill, verify they work correctly.

**Time**: 15-30 minutes

---

### Step 2: Scenario Testing
Test skill in 2-3 realistic scenarios from "When to Use" section.

**Time**: 30-90 minutes

---

### Step 3: Integration Testing
Test skill works with other skills it depends on or composes.

**Time**: 20-45 minutes (if applicable)

---

### Step 4: Validation Check
Run skill-validator to ensure tests didn't reveal structure issues.

**Time**: 10-15 minutes

---

## Quick Reference

| Step | Focus | Time | Pass Criteria |
|------|-------|------|---------------|
| 1 | Examples | 15-30m | All examples execute correctly |
| 2 | Scenarios | 30-90m | Scenarios complete successfully |
| 3 | Integration | 20-45m | Integration smooth (if applicable) |
| 4 | Validation | 10-15m | Structure still passes |

**Total Time**: 1.5-3 hours

**Result**: ✅ TESTS PASS or ❌ TESTS FAIL (with issues to fix)

---

**testing-workflow ensures skills function correctly through comprehensive hands-on testing.**
