---
name: plan-template
description: Implementation plan templates with format specifications, validation criteria, and examples. Use when creating plans for features, bug fixes, or refactoring. Provides the complete plan structure and writing guidance.
argument-hint: "[template-type: bugfix | refactor | feature | format | help]"
allowed-tools: Read, Glob
---

# Plan Template Skill

This skill provides everything needed to write implementation plans: templates, format specifications, and examples.

## Quick Reference

| Command | Description |
|---------|-------------|
| `/plan-template` | Show available templates and help |
| `/plan-template feature` | Template for new features (any complexity) |
| `/plan-template bugfix` | Template for bug fixes (TDD approach) |
| `/plan-template refactor` | Template for architectural changes |
| `/plan-template format` | Show complete plan document format |

---

## Available Templates

| Template | Use For | Pattern |
|----------|---------|---------|
| **feature** | New features of any complexity (from utility functions to multi-module systems) | Setup → Component 1 (write→test→validate) → Component 2 → ... → Integration → Final QA |
| **bugfix** | Bug fixes following TDD pattern | Identify → Reproduce with test → Fix → Edge cases → Validate |
| **refactor** | Architectural changes, code restructuring, multi-module work | Module 1 → Module 2 → Module 3 → Integration → Final QA |

### Template Selection Guide

**Choose `feature` when:**
- Adding new functionality (greenfield development)
- Implementing anything from simple utility functions to complex multi-module features
- Building new APIs, services, or components
- Requirements involve creating new code rather than fixing or restructuring existing code

**Choose `bugfix` when:**
- Fixing a bug of any size
- Issue requires root cause analysis
- Dealing with regressions or unexpected behavior
- Need to follow TDD (test-first) approach

**Choose `refactor` when:**
- Making architectural changes to existing code
- Restructuring code across multiple files
- Reorganizing modules without changing behavior
- Implementing breaking changes with migration needs
- Maintaining backward compatibility is important

---

## Plan Document Format

**Every plan MUST follow this structure.** This is the canonical format for all implementation plans.

### Required Frontmatter

```yaml
---
scope: <scope-name>                # lowercase with hyphens
created: <YYYY-MM-DDTHHmmssZ>      # creation timestamp (UTC)
updated: <YYYY-MM-DDTHHmmssZ>      # last update timestamp (UTC)
version: <int>                     # increment on updates
---
```

### Required Sections

```markdown
# Implementation Plan: [Feature Name]

## Overview
[2-3 sentence summary of what this feature does and why it's needed]

## Phases

- [ ] [Phase 1: Phase Name](#phase-1-phase-name)
- [ ] [Phase 2: Phase Name](#phase-2-phase-name)
- [ ] [Phase N: End-to-End Validation](#phase-n-end-to-end-validation)

## Requirements

### Functional Requirements
- [FR1: Specific functional requirement]
- [FR2: Specific functional requirement]

### Non-Functional Requirements
- [NFR1: Performance, scalability, security requirements]
- [NFR2: Code quality, testing, documentation requirements]

### Assumptions & Constraints
- [Assumption 1]
- [Constraint 1]

## Architecture Analysis

### Current State
- [Description of relevant existing architecture]
- [Key files/modules that will be affected]

### Proposed Changes
- [Change 1: file path and high-level description]
- [Change 2: file path and high-level description]

### Design Decisions
1. **[Decision 1]**: [Rationale]
2. **[Decision 2]**: [Rationale]

## File Inventory

### Files to Create
- `path/to/new_file.py` - [Purpose]
- `path/to/test_new_file.py` - [Test coverage]

### Files to Modify
- `path/to/existing_file.py` - [What changes]

### Files to Delete (if any)
- `path/to/deprecated_file.py` - [Reason for removal]

## Implementation Steps
[See Phase Structure below]

## Testing Requirements
[See Testing Format below]

## Code Quality Requirements
[See Quality Checklist below]

## Dependencies

### External Dependencies
- [New package: version and purpose]

### Internal Dependencies
- [Other features or modules this depends on]

### Blocking Items
- [Items that must be completed first]

## Acceptance Criteria
[See Acceptance Criteria Format below]

## Future Enhancements
[Optional features to consider for future iterations]
```

---

## Phase Structure

**One Phase = One Complete Feature/Function/Component**

Each phase produces working, tested, validated code before moving to the next.

### Phase Organization Principles

- **Organize by feature, not by activity**: Each feature is its own phase containing implementation, testing, and validation steps
- **Enable incremental progress**: Complete Phase 1 fully before starting Phase 2
- **Prioritize by dependencies**: If Function B depends on Function A, make Function A Phase 1
- **Include integration checks**: Each phase verifies compatibility with existing code
- **Always end with E2E validation**: Final phase verifies all work meets acceptance criteria

### Phase Template

```markdown
### Phase N: [Phase Name - e.g., Implement process_dataframe Function]
**Goal**: [What this phase accomplishes - be specific about the single feature/function]

**Dependencies**: None / Requires Phase X completion

#### Implementation Steps

##### Step N.1: [Specific Implementation Step]
- **File**: `path/to/file.py`
- **Action**: [Detailed, specific action - what code to write]
- **Details**:
  - Create class/function `ClassName` with methods `method1()`, `method2()`
  - Key signatures: `def method1(param: Type) -> ReturnType:`
  - Important implementation notes
- **Why**: [Business/technical reason]
- **Dependencies**: None / Requires Step X.Y
- **Validation**:
  - **Command**: `uv run pytest tests/test_<module>.py::test_<function> -v`
  - **Expected**: Test passes, verifying functionality works correctly
  - **Manual Check**: Function has type hints and docstring

#### Test Steps

##### Step N.T1: Write Unit Tests
- **File**: `tests/test_<module>.py`
- **Action**: Create comprehensive unit tests
- **Details**:
  - Test success cases
  - Test edge cases
  - Test error handling
- **Validation**:
  - **Command**: `uv run pytest tests/test_<module>.py -v`
  - **Expected**: All tests pass with >90% coverage

#### Validation Steps

##### Step N.V1: Validate Implementation
- **Action**: Run all quality checks
- **Validation**:
  - **Command**: `uv run pytest tests/test_<module>.py && uv run ty check . && uv run ruff check`
  - **Expected**: All checks pass
  - **Manual Check**: Code follows project conventions
```

### Final Phase: End-to-End Validation

Every plan MUST end with an E2E validation phase:

```markdown
### Phase N: End-to-End Validation
**Goal**: Verify all phases work together and meet acceptance criteria

#### Step N.1: Run Full Test Suite
- **Validation**:
  - **Command**: `uv run pytest -v`
  - **Expected**: All tests pass
  - **Manual Check**: Code coverage >= 90%

#### Step N.2: Verify Acceptance Criteria
- **Action**: Check all acceptance criteria from plan overview
- **Validation**:
  - **Command**: `uv run ruff check && uv run ty check . && uv tool run pydoclint`
  - **Expected**: All quality checks pass
  - **Manual Check**: All acceptance criteria checkboxes complete
```

---

## Step Granularity Rules

**One step = One atomic, testable change**

Each step must be:
- **Atomic**: Can be completed independently without partial states
- **Time-bounded**: Should take 5-15 minutes to implement
- **Verifiable**: Has clear validation criteria
- **Focused**: Does one thing well

**When to break down steps:**
- If a step seems >15 minutes, split it into substeps
- If a step has multiple unrelated actions, separate them
- If a step crosses multiple files/modules, consider breaking it up
- If validation requires multiple checks, each check might be its own step

---

## Validation Criteria Format

**CRITICAL**: Every step MUST have specific, actionable validation criteria.

Generic validation like "make sure it works" or "verify correctness" is **NOT acceptable**.

### Required Components

Every validation must include:

1. **Command** - Exact command to run for automated verification
   - Must be copy-pasteable
   - Should be deterministic (same input = same output)
   - **PREFER tests that exercise the code** over simple import checks

2. **Expected** - Precise expected outcome
   - Specific output, return code, or behavior
   - Measurable and verifiable
   - Examples: "Test passes", "All 3 tests pass", "Returns exit code 0"

3. **Manual Check** (when automated verification isn't sufficient)
   - Code quality checks (docstrings, type hints present)
   - Visual/structural verification

### Validation Philosophy

**DO**: Write tests that exercise the code
- Run pytest tests that call the function with real inputs
- Verify the function produces expected outputs
- Test edge cases and error handling

**DON'T**: Use simple import checks as primary validation
- Importing only verifies the function exists, not that it works
- Import checks are acceptable as "smoke tests" but should be supplemented with real tests

---

## Testing Requirements Format

Use Given/When/Then format for test scenarios:

```markdown
## Testing Requirements

### Unit Tests

#### Test File: `tests/test_<module>.py`
- **Test 1**: `test_<function_name>_success_case`
  - Given: [Initial state]
  - When: [Action]
  - Then: [Expected outcome]

- **Test 2**: `test_<function_name>_edge_case`
  - Given: [Edge case setup]
  - When: [Action]
  - Then: [Expected handling]

- **Test 3**: `test_<function_name>_error_handling`
  - Given: [Error condition]
  - When: [Action]
  - Then: [Expected error/exception]

### Integration Tests
- **Scenario 1**: [End-to-end flow description]
- **Scenario 2**: [Integration between components]
```

---

## Code Quality Checklist

Include this checklist in every plan:

```markdown
## Code Quality Requirements

- [ ] All functions have type hints
- [ ] All public APIs have Google-style docstrings
- [ ] Code follows project conventions
- [ ] No code duplication (DRY principle)
- [ ] Error handling with clear messages
- [ ] Passes `uv run ruff check`
- [ ] Passes `uv run ty check .`
- [ ] Passes docstring linting
```

---

## Acceptance Criteria Format

```markdown
## Acceptance Criteria

### Functional Acceptance
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

### Quality Acceptance
- [ ] All unit tests pass (`uv run pytest`)
- [ ] All public functions have a test
- [ ] Code coverage >= 90%
- [ ] Type checking passes (`uv run ty check .`)
- [ ] Linting passes (`uv run ruff check`)
- [ ] Docstring validation passes
- [ ] No security vulnerabilities

### Documentation Acceptance
- [ ] Code is documented with Google-style docstrings
- [ ] README updated (if applicable)
- [ ] Examples provided in docstrings
```

---

## Bug Fix Pattern (TDD)

Bug fixes follow Test-Driven Development:

### Pattern: Identify → Reproduce → Fix → Validate

1. **Identify**: Locate buggy code and understand root cause
2. **Reproduce**: Write test FIRST that reproduces the bug (verify test FAILS)
3. **Fix**: Make minimal change to fix bug (verify test now PASSES)
4. **Edge Cases**: Add tests for related scenarios (prevent similar bugs)
5. **Validate**: Run full test suite (ensure no regressions)

### Key Principles

- **Test-Driven**: Write reproduction test before fixing code
- **Verify Failure**: Confirm test fails with current code (proves bug exists)
- **Minimal Fix**: Smallest change necessary to fix the bug
- **No Regressions**: All existing tests must continue to pass
- **Document Root Cause**: Explain why bug occurred and how fix prevents it

---

## Refactoring Guidelines

When planning refactors:

1. **Identify code smells and technical debt**
2. **List specific improvements needed**
3. **Preserve existing functionality** (all existing tests must pass)
4. **Create backwards-compatible changes** when possible
5. **Plan for gradual migration** if needed

---

## Action Instructions

Based on the argument provided, perform one of these actions:

### `/plan-template` (no args) or `/plan-template help`
Show this overview with available templates and commands.

### `/plan-template feature`
Read and display: `.claude/skills/plan-template/example-feature.md`

### `/plan-template bugfix`
Read and display: `.claude/skills/plan-template/example-bugfix.md`

### `/plan-template refactor`
Read and display: `.claude/skills/plan-template/example-refactor.md`

### `/plan-template format`
Display the "Plan Document Format" section from this skill.

---

## Template File Locations

All example templates are in this skill directory:

- `example-feature.md` - Complete example for new features (any complexity)
- `example-bugfix.md` - Complete example for bug fixes
- `example-refactor.md` - Complete example for refactoring
