---
name: derive
scope: partial
description: |
  Derive BDD scenarios and TDD test skeletons from approved SDD specifications.
  ATDD acceptance test tables are optional output for specialized needs.
  Use when: spec is approved, starting BDD/TDD implementation, generating test structures.
  Keywords: forward derivation, spec to test, BDD generation, TDD skeleton, test derivation, 正向推演, 規格轉測試, 測試生成.
---

# Forward Derivation Guide

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/forward-derivation/SKILL.md)

**Version**: 2.0.0
**Last Updated**: 2026-01-25
**Applicability**: Claude Code Skills

> **Core Standard**: This skill implements [Forward Derivation Standards](../../core/forward-derivation-standards.md). For comprehensive methodology documentation accessible by any AI tool, refer to the core standard.

---

## Purpose

This skill guides you through deriving BDD scenarios and TDD test skeletons from approved SDD specifications, with strict adherence to Anti-Hallucination standards.

> **Note**: ATDD test tables are optional and available via `/derive-atdd`. BDD scenarios already serve as executable acceptance tests, making ATDD tables redundant for most use cases.

Forward Derivation is the symmetrical counterpart to [Reverse Engineering](../reverse-engineer/SKILL.md):
- **Reverse Engineering**: Code → Specification
- **Forward Derivation**: Specification → Tests

## Quick Reference

### Forward Derivation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│              Forward Derivation Workflow                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣  SPEC Parsing (AI Automated)                               │
│      ├─ Read approved specification                             │
│      ├─ Extract Acceptance Criteria (GWT or bullet)             │
│      └─ Validate SPEC structure and completeness                │
│                                                                 │
│  2️⃣  Derivation (AI Automated)                                 │
│      ├─ AC → BDD Gherkin scenarios                             │
│      ├─ AC → TDD test skeletons with TODOs                     │
│      └─ (Optional) AC → ATDD acceptance test tables            │
│                                                                 │
│  3️⃣  Human Review (Required)                                   │
│      ├─ Verify generated scenarios match AC intent              │
│      ├─ Fill in [TODO] sections                                │
│      └─ Refine step definitions if needed                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Commands Overview

| Command | Input | Output | Purpose |
|---------|-------|--------|---------|
| `/derive-bdd` | SPEC-XXX.md | .feature | AC → Gherkin scenarios |
| `/derive-tdd` | SPEC-XXX.md | .test.ts | AC → Test skeletons |
| `/derive-all` | SPEC-XXX.md | .feature + .test.ts | Full derivation pipeline |
| `/derive-atdd` | SPEC-XXX.md | acceptance.md | AC → Acceptance test tables (optional) |

## Core Principles

### 1. Spec-Bounded Generation

**CRITICAL**: Only derive content that exists in the specification. Never add scenarios, tests, or features beyond what the Acceptance Criteria explicitly define.

```
# Anti-Hallucination Rule
Input:  SPEC with N Acceptance Criteria
Output: Exactly N scenarios (BDD)
        Exactly N test groups (TDD)
        Exactly N acceptance tests (ATDD, if requested)

If output count ≠ input count → VIOLATION
```

### 2. Source Attribution

Every generated item MUST include traceability:

```gherkin
# Generated from: specs/SPEC-001.md
# AC: AC-1

@SPEC-001 @AC-1
Scenario: User login with valid credentials
```

### 3. Derivation Tags (from Unified Tag System)

This skill uses **Derivation Tags** for generating new content from specifications. See [Anti-Hallucination Standards](../../core/anti-hallucination.md#unified-tag-system) for the complete tag reference.

| Tag | Use When | Example |
|-----|----------|---------|
| `[Source]` | Direct content from SPEC | Feature title, AC text |
| `[Derived]` | Transformed from SPEC content | GWT from bullet AC |
| `[Generated]` | AI-generated structure | Test skeleton |
| `[TODO]` | Requires human implementation | Assertions, step definitions |

## Workflow Stages

### Stage 1: SPEC Parsing

**Input**: Approved specification file
**Output**: Structured Acceptance Criteria list

**Actions**:
1. Read specification file
2. Identify Acceptance Criteria section
3. Parse AC format (Given-When-Then or Bullet)
4. Validate AC completeness

**Validation Checklist**:
- [ ] SPEC status is "Approved" or "Ready"
- [ ] Acceptance Criteria section exists
- [ ] Each AC has unique identifier (AC-1, AC-2, etc.)
- [ ] AC format is parseable (GWT or bullet)

### Stage 2: BDD Derivation

**Input**: Parsed Acceptance Criteria
**Output**: Gherkin .feature file

**Transformation Rules**:

| AC Format | Transformation |
|-----------|----------------|
| Given-When-Then | Direct mapping to Gherkin |
| Bullet points | Convert using GWT pattern matching |
| Checklist | Convert conditions → Given, actions → When, outcomes → Then |

**Example**:
```markdown
# Input AC (Bullet)
- [ ] User can login with email and password
- [ ] Login shows error for invalid credentials
```

```gherkin
# Output BDD
@SPEC-001 @AC-1
Scenario: User login with email and password
  Given a user with valid credentials
  When the user submits login form
  Then the user is logged in successfully

@SPEC-001 @AC-2
Scenario: Login shows error for invalid credentials
  Given a user with invalid credentials
  When the user submits login form
  Then an error message is displayed
```

### Stage 3: TDD Derivation

**Input**: Parsed Acceptance Criteria
**Output**: Test skeleton file

**Actions**:
1. Create describe block for SPEC
2. Create describe block per AC
3. Generate it blocks with descriptive names
4. Add AAA structure with TODO comments
5. Include placeholder assertions

**Parameters**:
| Parameter | Options | Default |
|-----------|---------|---------|
| `--lang` | typescript, javascript, python, java, go | typescript |
| `--framework` | vitest, jest, pytest, junit, go-test | vitest |

### Stage 4: ATDD Derivation (Optional)

> **Note**: ATDD test tables are optional. BDD scenarios already serve as executable acceptance tests. Use ATDD tables only when:
> - Manual testing workflows are required
> - Stakeholders prefer tabular test documentation
> - Regulatory compliance requires specific test evidence format

**Input**: Parsed Acceptance Criteria
**Output**: Acceptance test table document

**Actions**:
1. Create test table per AC
2. Generate step-by-step action columns
3. Add expected result columns
4. Include Pass/Fail checkboxes
5. Add tester sign-off section

### Stage 5: Human Review

**Input**: Generated files
**Output**: Reviewed and refined files

**Review Checklist**:
- [ ] Generated scenarios match AC intent
- [ ] No extra scenarios beyond AC count
- [ ] Source attribution is correct
- [ ] [TODO] sections identified for implementation
- [ ] Step language is business-level (not technical)

## Output Formats

### BDD Feature File

```gherkin
# Generated from: specs/SPEC-001.md
# Generator: /derive-bdd v1.0.0
# Generated at: 2026-01-19T10:00:00Z

@SPEC-001
Feature: User Authentication
  [Source] From SPEC-001 Summary

  @AC-1 @happy-path
  Scenario: User login with valid credentials
    # [Source] From SPEC-001 AC-1
    Given a registered user with valid credentials
    When the user submits login form
    Then the user is redirected to dashboard

  @AC-2 @error-handling
  Scenario: Login fails with invalid credentials
    # [Source] From SPEC-001 AC-2
    Given a user with invalid credentials
    When the user submits login form
    Then an error message is displayed
```

### TDD Test Skeleton

```typescript
/**
 * Tests for SPEC-001: User Authentication
 * Generated from: specs/SPEC-001.md
 * Generated at: 2026-01-19T10:00:00Z
 * AC Coverage: AC-1, AC-2
 */

describe('SPEC-001: User Authentication', () => {
  describe('AC-1: User login with valid credentials', () => {
    it('should redirect to dashboard on successful login', async () => {
      // Arrange
      // [TODO] Set up registered user with valid credentials

      // Act
      // [TODO] Submit login form

      // Assert
      // [TODO] Verify redirect to dashboard
      expect(true).toBe(true); // Placeholder
    });
  });

  describe('AC-2: Login fails with invalid credentials', () => {
    it('should display error message', async () => {
      // Arrange
      // [TODO] Set up user with invalid credentials

      // Act
      // [TODO] Submit login form

      // Assert
      // [TODO] Verify error message is displayed
      expect(true).toBe(true); // Placeholder
    });
  });
});
```

### ATDD Acceptance Test Table (Optional)

> Generated via `/derive-atdd` when ATDD test tables are needed.

```markdown
# SPEC-001 Acceptance Tests

**Specification**: SPEC-001
**Generated**: 2026-01-19
**Status**: Pending

## AT-001: User login with valid credentials
**Source**: AC-1

| Step | Action | Expected | Pass/Fail |
|------|--------|----------|-----------|
| 1 | Navigate to login page | Login form displayed | [ ] |
| 2 | Enter valid credentials | Fields accept input | [ ] |
| 3 | Click Login | Form submitted | [ ] |
| 4 | Verify redirect | Dashboard displayed | [ ] |

**Tester**: _______________
**Date**: _______________
**Result**: [ ] Pass / [ ] Fail
```

## Integration with Other Skills

### With /spec (Spec-Driven Development)

1. Complete SPEC using `/spec` workflow
2. Get SPEC approved through review
3. Run `/derive-all` to generate test structures
4. Use generated outputs in BDD/TDD workflows

### With /bdd (Behavior-Driven Development)

1. Generate BDD scenarios using `/derive-bdd`
2. Review and refine scenarios with stakeholders
3. Continue with BDD formulation using `/bdd`
4. Implement step definitions

### With /tdd (Test-Driven Development)

1. Generate TDD skeletons using `/derive-tdd`
2. Fill in [TODO] sections with actual assertions
3. Enter TDD Red phase with generated test structure
4. Implement code to make tests pass

### With Integrated Flow

Forward Derivation fits in the Integrated Flow methodology:

```
spec-review (approved) → forward-derivation → discovery (BDD)
                              │
                              ├─→ .feature files for BDD
                              └─→ .test.ts skeletons for TDD

Optional: /derive-atdd → acceptance.md for manual testing
```

## Complete Derivation Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Complete Forward Derivation Pipeline                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Approved SPEC                                                         │
│        │                                                                │
│        ▼                                                                │
│   /derive-all specs/SPEC-XXX.md                                        │
│        │                                                                │
│        ├─→ /derive-bdd                                                  │
│        │    └─→ features/SPEC-XXX.feature                              │
│        │                                                                │
│        └─→ /derive-tdd                                                  │
│             └─→ tests/SPEC-XXX.test.ts                                 │
│                                                                         │
│   Optional: /derive-atdd specs/SPEC-XXX.md                              │
│        └─→ acceptance/SPEC-XXX-acceptance.md                           │
│                                                                         │
│   Human Review                                                          │
│        │                                                                │
│        ├─→ Verify 1:1 AC mapping                                       │
│        ├─→ Fill [TODO] sections                                        │
│        └─→ Refine step definitions                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Usage Examples

```bash
# Generate BDD scenarios
/derive-bdd specs/SPEC-001.md

# Generate TDD skeleton with Python/pytest
/derive-tdd specs/SPEC-001.md --lang python --framework pytest

# Generate all test structures
/derive-all specs/SPEC-001.md

# Preview without creating files
/derive-all specs/SPEC-001.md --dry-run

# Specify output directory
/derive-all specs/SPEC-001.md --output-dir ./generated
```

## Anti-Patterns to Avoid

### ❌ Don't Do This

1. **Adding Extra Scenarios**
   - Wrong: SPEC has 3 AC, generated 5 scenarios
   - Right: SPEC has 3 AC, generated exactly 3 scenarios

2. **Deriving from Draft SPEC**
   - Wrong: Running `/derive-all` on unapproved spec
   - Right: Only derive from approved specifications

3. **Skipping Source Attribution**
   - Wrong: Scenario without @SPEC-XXX tag
   - Right: Every scenario tagged with source SPEC and AC

4. **Over-Specifying Technical Details**
   - Wrong: `Given database connection is established using PostgreSQL driver`
   - Right: `Given user data exists in the system`

5. **Treating Skeletons as Complete**
   - Wrong: Using generated tests without filling [TODO]
   - Right: Fill all [TODO] sections before running tests

## Best Practices

### Do's

- ✅ Only derive from approved specifications
- ✅ Maintain strict 1:1 AC to output mapping
- ✅ Include source attribution in all outputs
- ✅ Use [TODO] markers for implementation sections
- ✅ Review generated outputs with stakeholders
- ✅ Keep step language at business level

### Don'ts

- ❌ Add scenarios beyond what AC defines
- ❌ Derive from draft or unapproved specs
- ❌ Skip human review of generated outputs
- ❌ Treat generated skeletons as complete tests
- ❌ Remove source attribution comments
- ❌ Over-specify implementation details

---

## Configuration Detection

This skill auto-detects project configuration:

1. Check for existing `specs/` directory structure
2. Detect test framework from package.json/pyproject.toml
3. Identify preferred output directories
4. Configure language-specific templates

---

## Related Standards

- [Forward Derivation Standards](../../core/forward-derivation-standards.md) - **Core methodology standard (primary reference)**
- [Reverse Engineering Standards](../../core/reverse-engineering-standards.md) - Symmetrical counterpart
- [Spec-Driven Development](../../core/spec-driven-development.md) - Input specification format
- [Behavior-Driven Development](../../core/behavior-driven-development.md) - BDD output format
- [Test-Driven Development](../../core/test-driven-development.md) - TDD output usage
- [Anti-Hallucination Guidelines](../../core/anti-hallucination.md) - Generation compliance

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-25 | ATDD changed from required to optional output; /derive-all now outputs BDD + TDD only |
| 1.1.0 | 2026-01-25 | Added: Reference to Unified Tag System |
| 1.0.0 | 2026-01-19 | Initial release |

---

## License

This skill is released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

**Source**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
