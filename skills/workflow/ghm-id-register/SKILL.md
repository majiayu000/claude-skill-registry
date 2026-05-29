---
name: ghm-id-register
description: >
  Validates and registers new SoT IDs with cross-reference integrity.
  Triggers when creating BR-XXX, UJ-XXX, API-XXX, or CFD-XXX entries.
  Outputs formatted SoT entry with validated cross-references.
---

# ID Register

Validate and register new Source of Truth IDs with cross-reference integrity checks.

## Workflow Overview

1. **Validate Format** → Check ID follows `[PREFIX]-[3-digit]` pattern
2. **Check Uniqueness** → Ensure ID doesn't already exist
3. **Verify Cross-Refs** → All referenced IDs must exist
4. **Register Entry** → Add to appropriate SoT file

## Core Output Template

| Element | Definition | Evidence |
|---------|------------|----------|
| **ID** | Unique identifier | `BR-101`, `UJ-045`, `API-012` |
| **Title** | Short descriptive name | Clear, specific |
| **Cross-References** | Links to related IDs | All referenced IDs exist |
| **Status** | Current state | Draft / Active / Deprecated |

## ID Format Reference

| Prefix | Domain | File |
|--------|--------|------|
| `BR-` | Business Rules | `SoT/SoT.BUSINESS_RULES.md` |
| `UJ-` | User Journeys | `SoT/SoT.USER_JOURNEYS.md` |
| `API-` | API Contracts | `SoT/SoT.API_CONTRACTS.md` |
| `CFD-` | Customer Feedback | `SoT/SoT.CUSTOMER_FEEDBACK.md` |

## Step 1: Validate Format

Check ID follows the pattern:

```
[PREFIX]-[XXX]
```

Where:
- PREFIX = BR, UJ, API, or CFD
- XXX = 3-digit number (zero-padded)

### Checklist
- [ ] Prefix is valid (BR, UJ, API, CFD)
- [ ] Number is 3 digits
- [ ] Format matches `[A-Z]+-[0-9]{3}`

## Step 2: Check Uniqueness

1. Read target SoT file
2. Extract all existing IDs of same prefix
3. Verify new ID doesn't exist
4. If auto-assigning: use highest existing + 1

### Checklist
- [ ] Target SoT file read
- [ ] Existing IDs enumerated
- [ ] New ID is unique

## Step 3: Verify Cross-References

For each ID referenced in the new entry:
1. Identify the prefix
2. Check that ID exists in its SoT file
3. Flag any missing references

### Checklist
- [ ] All `BR-XXX` references exist in BUSINESS_RULES
- [ ] All `UJ-XXX` references exist in USER_JOURNEYS
- [ ] All `API-XXX` references exist in API_CONTRACTS
- [ ] All `CFD-XXX` references exist in CUSTOMER_FEEDBACK

## Step 4: Register Entry

Add formatted entry to SoT file:

```markdown
### [ID]: [Title]

**Status**: Draft
**Created**: YYYY-MM-DD
**Cross-References**: [List of related IDs]

[Description]

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2
```

## Quality Gates

### Pass Checklist
- [ ] ID format is valid
- [ ] ID is unique within its domain
- [ ] All cross-references resolve
- [ ] Entry follows SoT template

### Testability Check
- [ ] ID can be searched and found
- [ ] Cross-references are bidirectional (if required)

## Anti-Patterns

| Pattern | Example | Fix |
|---------|---------|-----|
| Duplicate ID | Creating BR-101 when it exists | → Check uniqueness first |
| Orphan reference | References UJ-999 that doesn't exist | → Verify all cross-refs |
| Wrong prefix | Using BR- for an API contract | → Match prefix to domain |
| Missing zero-pad | BR-5 instead of BR-005 | → Always use 3 digits |

## Boundaries

**DO**:
- Format validation
- Uniqueness checks
- Cross-reference verification
- Entry formatting

**DON'T**:
- Content decisions about ID meaning
- Approve/reject based on business logic
- Modify existing IDs

## Handoff

After ID registration:
- New ID is in SoT file
- Cross-references are valid
- EPIC Section 3A updated with new ID
- Ready for implementation
