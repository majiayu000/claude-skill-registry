---
name: spec-validation
description: |
  Use to validate spec documents for correctness, completeness, and consistency.
  Ensures specs follow SuperSpec format and are ready for implementation.
---

# Spec Validation

## Overview

Validate spec documents to ensure they are correct, complete, and ready for implementation.

**Core principle:** Invalid specs lead to invalid implementations. Validate early, validate often.

**Announce at start:** "I'm using the spec-validation skill to check these specifications."

## When to Use

- After completing Phase 4 (SPEC) of brainstorm
- Before creating implementation plan
- After modifying existing specs
- Before running `superspec verify`

## What Gets Validated

```
┌─────────────────────────────────────────────────────────────────┐
│                    Validation Layers                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   1. Structure Validation                                        │
│      └─→ Required sections present                              │
│      └─→ Correct header hierarchy                               │
│      └─→ Valid frontmatter (if any)                             │
│                                                                   │
│   2. Content Validation                                          │
│      └─→ Requirements have proper format                        │
│      └─→ Scenarios have WHEN/THEN                               │
│      └─→ No orphan content                                       │
│                                                                   │
│   3. Consistency Validation                                      │
│      └─→ Cross-references valid                                 │
│      └─→ No duplicate names                                     │
│      └─→ Delta references exist                                 │
│                                                                   │
│   4. Completeness Validation                                     │
│      └─→ Every Requirement has Scenarios                        │
│      └─→ Every Scenario has WHEN + THEN                         │
│      └─→ No empty sections                                       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Validation Rules

### Structure Rules

**Required Sections:**
```markdown
# [Capability Name] Specification

## Purpose
[Why this capability exists]

## Requirements

### Requirement: [Name]
[Description with SHALL/MUST statements]

#### Scenario: [Name]
- **WHEN** [condition]
- **THEN** [result]
```

**Header Hierarchy:**
- `#` - Capability name (only one)
- `##` - Major sections (Purpose, Requirements)
- `###` - Requirements
- `####` - Scenarios

### Content Rules

**Requirement Format:**
```markdown
### Requirement: [Unique Name]

The system SHALL [behavior description].
```

- Name must be unique within spec
- Description should use SHALL/MUST for mandatory behavior
- Description should use SHOULD/MAY for optional behavior

**Scenario Format:**
```markdown
#### Scenario: [Descriptive Name]
- **WHEN** [precondition or trigger]
- **THEN** [expected result]
- **AND** [additional result] (optional)
```

- Name should describe the scenario clearly
- WHEN must specify trigger condition
- THEN must specify verifiable outcome
- AND for additional outcomes (optional)

### Delta Spec Rules

**For changes (not main specs):**

```markdown
## ADDED Requirements
[New requirements]

## MODIFIED Requirements
[Changed requirements - must match existing name exactly]

## REMOVED Requirements
[Deleted requirements - must include reason]

## RENAMED Requirements
[Name changes - FROM/TO format]
```

**MODIFIED must reference existing:**
- Name must match exactly
- Original requirement must exist in main spec

**REMOVED must include reason:**
```markdown
### Requirement: [Name]
**Reason**: [Why removing]
**Migration**: [How to handle existing usage]
```

## CLI Command

```bash
# Validate single change
superspec validate [change-id]

# Strict mode (fail on warnings)
superspec validate [change-id] --strict

# Validate all specs
superspec validate --all

# Verbose output
superspec validate [change-id] --verbose
```

## Validation Output

### Success
```
✅ Validation passed for [change-id]

Structure: ✅
Content: ✅
Consistency: ✅
Completeness: ✅

Requirements: 3
Scenarios: 8
```

### Failure
```
❌ Validation failed for [change-id]

Errors:
1. [ERROR] Requirement "User Login" missing Scenarios
2. [ERROR] Scenario "Valid login" missing THEN clause

Warnings:
1. [WARN] Requirement "Session Management" uses SHOULD instead of SHALL

Fix errors before proceeding.
```

## Error Categories

### Critical Errors (Must Fix)

| Error | Description | Fix |
|-------|-------------|-----|
| Missing WHEN | Scenario has no trigger | Add WHEN clause |
| Missing THEN | Scenario has no outcome | Add THEN clause |
| Orphan Scenario | Scenario outside Requirement | Move under Requirement |
| Duplicate Name | Two items with same name | Rename one |
| Invalid Reference | MODIFIED refs non-existent | Fix name or add original |

### Warnings (Should Fix)

| Warning | Description | Recommendation |
|---------|-------------|----------------|
| Weak Language | Uses "should" in SHALL context | Consider if mandatory |
| Empty Section | Section with no content | Add content or remove |
| Long Scenario | Too many AND clauses | Split into multiple |
| Vague THEN | Non-verifiable outcome | Make specific |

## Integration with Workflow

### Before Plan Writing

```
brainstorm (Phase 4: SPEC)
    ↓
superspec validate [id] --strict
    ↓ (must pass)
plan-writing
```

### Before Archive

```
verify (all tests pass)
    ↓
superspec validate [id] --strict
    ↓ (must pass)
archive
```

## Manual Validation Checklist

When validating manually:

### Structure
- [ ] Single `#` header with capability name
- [ ] `## Purpose` section exists
- [ ] `## Requirements` section exists
- [ ] Requirements use `###` headers
- [ ] Scenarios use `####` headers

### Content
- [ ] Each Requirement has unique name
- [ ] Each Requirement has description
- [ ] Each Scenario has WHEN clause
- [ ] Each Scenario has THEN clause

### Consistency
- [ ] No duplicate Requirement names
- [ ] No duplicate Scenario names within Requirement
- [ ] MODIFIED references exist in main spec
- [ ] Cross-references are valid

### Completeness
- [ ] Every Requirement has at least one Scenario
- [ ] No empty sections
- [ ] All edge cases covered

## Red Flags

**Never:**
- Skip validation before plan writing
- Proceed with validation errors
- Ignore warnings in strict mode

**Always:**
- Validate after any spec change
- Use `--strict` before major milestones
- Fix all errors before proceeding

## Integration

**Called by:**
- `brainstorm` - After Phase 4 completion
- `plan-writing` - As prerequisite
- `archive` - Before applying deltas

**Pairs with:**
- `verify` - Validates implementation against validated specs
