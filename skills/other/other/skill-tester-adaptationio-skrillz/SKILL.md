---
name: skill-tester
description: Test Claude Code skills in real-world scenarios to validate functionality, usability, and effectiveness. Task-based testing operations for scenario testing, example validation, integration testing, and usability assessment. Use when testing skill functionality, validating examples work correctly, ensuring real-world effectiveness, or conducting scenario-based quality assurance.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Skill Tester

## Overview

skill-tester validates Claude Code skills work correctly in real-world scenarios through hands-on testing operations.

**Purpose**: Functional and usability testing through actual usage

**The 4 Testing Operations**:
1. **Scenario Testing** - Test skill in realistic use cases
2. **Example Validation** - Verify all examples execute correctly
3. **Integration Testing** - Test skill works with other skills
4. **Usability Testing** - Assess ease of use and effectiveness

**Integration with review-multi**:
- review-multi Operation 4 (Usability Review): Comprehensive assessment with scoring
- skill-tester: Focused on functional testing (does it work?)

## When to Use

- Pre-deployment testing (ensure functionality)
- Example validation (all examples work?)
- Integration testing (works with other skills?)
- Real-world validation (effective in practice?)

## Operations

### Operation 1: Scenario Testing

**Purpose**: Test skill in realistic scenarios

**Process**:
1. Select scenario from "When to Use"
2. Actually follow skill instructions
3. Complete the task
4. Document success/failure and issues

**Validation**: PASS if scenario completes successfully

---

### Operation 2: Example Validation

**Purpose**: Verify all code/command examples execute correctly

**Process**:
1. Extract all examples from SKILL.md
2. Execute each example
3. Verify output matches expectations
4. Document any failures

**Validation**: PASS if all examples work

---

### Operation 3: Integration Testing

**Purpose**: Test skill works with other skills (for workflows/dependencies)

**Process**:
1. Identify dependent skills
2. Test integration points
3. Verify data flows correctly
4. Check composition works

**Validation**: PASS if integrations work smoothly

---

### Operation 4: Usability Testing

**Purpose**: Assess if skill is easy to use and effective

**Process**:
1. First-time user test (can someone use it without prior knowledge?)
2. Task completion test (can users achieve goals?)
3. Efficiency test (reasonable time?)
4. Satisfaction assessment (positive experience?)

**Validation**: PASS if usable and effective

---

## Quick Reference

| Operation | Focus | Pass Criteria |
|-----------|-------|---------------|
| Scenario Testing | Real-world usage | Scenario completes successfully |
| Example Validation | Examples work | All examples execute correctly |
| Integration Testing | Works with others | Integrations smooth |
| Usability Testing | Easy and effective | Usable by target users |

**Use with**: review-multi (comprehensive) + skill-tester (functional validation)

---

**skill-tester ensures skills work correctly through hands-on testing in real scenarios.**
