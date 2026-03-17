---
name: superspec:verify
description: |
  Use after implementation is complete to verify that code matches specifications.
  Ensures every Requirement is implemented and every Scenario has a corresponding test.
---

# Verify Implementation

## Overview

Verify that implementation matches specifications before archiving.

**Core principle:** Every Scenario becomes a test, every test traces to a Scenario.

**Announce at start:** "I'm using the verify skill to check implementation against specs."

## When to Use

- After all tasks in plan are complete
- Before running `/superspec:archive`
- After final code review passes

## Prerequisites

- Implementation complete
- All tests pass
- Final code review approved
- Specs exist: `superspec/changes/[id]/specs/**/*.md`

## The Verification Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    Verification Flow                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   1. Load Specs                                                   │
│      └─→ Read all specs/*.md files                               │
│                                                                   │
│   2. Extract Requirements + Scenarios                            │
│      └─→ Parse ### Requirement: and #### Scenario:               │
│                                                                   │
│   3. Match Against Tests                                          │
│      └─→ Find test for each Scenario                             │
│                                                                   │
│   4. Check for Extras                                             │
│      └─→ Identify code/tests not in Specs                        │
│                                                                   │
│   5. Generate Report                                              │
│      └─→ Coverage summary + issues                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## Step 1: Load Specs

```bash
# List all spec files
find superspec/changes/[id]/specs -name "spec.md"

# Read each spec
cat superspec/changes/[id]/specs/[capability]/spec.md
```

## Step 2: Extract Requirements and Scenarios

Parse the spec files for:

```markdown
### Requirement: [Name]
The system SHALL [behavior]

#### Scenario: [Name]
- **WHEN** [condition]
- **THEN** [result]
```

Build a checklist:
```
□ Requirement: User Authentication
  □ Scenario: Valid login accepted
  □ Scenario: Invalid password rejected
  □ Scenario: Account locked after 5 failures

□ Requirement: 2FA Setup
  □ Scenario: Generate QR code
  □ Scenario: Verify setup code
```

## Step 3: Match Against Tests

For each Scenario, find corresponding test:

```typescript
// Looking for test matching "#### Scenario: Valid login accepted"

test('Valid login accepted', () => { ... })  // ✅ Match
test('login works', () => { ... })           // ⚠️ Unclear match
// No test found                              // ❌ Missing
```

**Matching criteria:**
- Test name contains Scenario name
- Test covers WHEN condition
- Test verifies THEN result

## Step 4: Check for Extras

Identify:
- Tests not matching any Scenario
- Code implementing features not in Specs

**Extras are red flags:**
- May indicate scope creep
- May indicate missing Scenarios in Specs
- Should be discussed before archiving

## Step 5: Generate Report

```markdown
## Verification Report for [change-id]

### Coverage Summary
- Requirements: 3/3 (100%)
- Scenarios: 8/8 (100%)
- Tests: 10 (2 extra)

### Requirement Coverage

#### Requirement: User Authentication ✅
- [x] Scenario: Valid login accepted → test/auth.test.ts:15
- [x] Scenario: Invalid password rejected → test/auth.test.ts:32
- [x] Scenario: Account locked after 5 failures → test/auth.test.ts:48

#### Requirement: 2FA Setup ✅
- [x] Scenario: Generate QR code → test/2fa.test.ts:10
- [x] Scenario: Verify setup code → test/2fa.test.ts:35

### Issues Found

#### Missing Tests
(none)

#### Extra Tests (not in Specs)
- test/auth.test.ts:65 - 'handles network timeout'
- test/auth.test.ts:78 - 'retries on failure'

### Verdict
[✅ READY TO ARCHIVE / ❌ NEEDS WORK]
```

## Verification Rules

### Every Requirement Must Have Implementation

Check that code exists implementing the Requirement's behavior.

### Every Scenario Must Have Test

1:1 mapping between Scenarios and tests (minimum).

Complex Scenarios may have multiple tests:
```markdown
#### Scenario: Rate limiting
- WHEN 5 failed attempts
- THEN account locked
- AND notification sent
```

May need:
- Test for account locking
- Test for notification

### No Features Outside Specs

If you find code/tests not covered by Specs:
1. **Add to Specs** - If it's a legitimate feature
2. **Remove code** - If it's scope creep
3. **Discuss** - If unclear

## CLI Command

```bash
superspec verify [change-id]
```

**Options:**
- `--strict` - Fail on any extra code/tests
- `--verbose` - Show detailed matching

## Handling Issues

### Missing Test for Scenario

```
❌ Scenario: Account locked after 5 failures
   No test found
```

**Action:** Write the missing test before archiving.

### Extra Test Not in Specs

```
⚠️ Extra test: 'handles network timeout'
   Not matching any Scenario
```

**Options:**
1. Add Scenario to Spec (if valid feature)
2. Remove test (if out of scope)
3. Mark as infrastructure test (if not feature test)

### Unclear Test Match

```
⚠️ Scenario: Valid login accepted
   Possible match: 'login works' (confidence: low)
```

**Action:** Rename test to match Scenario name.

## Red Flags

**Never:**
- Archive with missing tests
- Archive with unexplained extra features
- Skip verification because "tests pass"

**Always:**
- Run verification before archive
- Address all issues before proceeding
- Update Specs if legitimate features are missing

## Integration

**Called by:**
- `/superspec:verify` command
- Before `/superspec:archive`

**Pairs with:**
- `archive` - Verify must pass before archiving
- `subagent-development` - After final review
- `verification-before-completion` - Evidence before claims

**Must use:**
- `verification-before-completion` - Before marking verification as complete, ensure fresh evidence exists
