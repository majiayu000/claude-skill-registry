---
name: test-spec
description: Generate test specifications from PBIs and acceptance criteria. Use when creating test specs, defining test strategy, or planning QA coverage. Triggers on keywords like "test spec", "test specification", "qa spec", "test strategy", "what to test".
infer: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

# Test Specification

Generate comprehensive test specifications from requirements.

## When to Use
- PBI ready for QA planning
- Need test coverage strategy
- Defining test scope

## Pre-Workflow

### Activate Skills

- Activate `qa-engineer` skill for test specification best practices

## Quick Reference

### Workflow
1. Read PBI file and user stories
2. Extract acceptance criteria and identify test scope
3. Define test strategy (unit / integration / E2E)
4. Identify test scenarios (positive/negative/boundary/edge)
5. Find code evidence (see below)
6. Create test spec artifact using template
7. Save to `team-artifacts/test-specs/`
8. Suggest next: `/test-cases {testspec}`

### Test Categories
| Category    | Purpose                        |
| ----------- | ------------------------------ |
| Positive    | Happy path verification        |
| Negative    | Error handling, invalid inputs |
| Boundary    | Edge values, limits            |
| Integration | Component interaction          |
| Security    | Auth, injection, XSS           |

### Output
- **Path:** `team-artifacts/test-specs/{YYMMDD}-testspec-{feature}.md`
- **ID Pattern:** `TC-{MOD}-{NNN}` (module-based, not date-based)
  - Rationale: Test cases are tied to modules/services, enabling easier filtering and traceability

### Spec Structure
1. Overview
2. Test Scope
3. Test Categories
4. Test Scenarios (high-level)
5. Coverage Requirements
6. Test Data Needs

## Find Code Evidence

Before writing test scenarios, search the codebase for supporting evidence:

1. **Search for validation logic** - find validators, constraints, rules
2. **Find error messages** - locate user-facing error strings
3. **Locate entity constraints** - property attributes, DB constraints
4. **Map evidence to files** - reference as `{file}:{line}` in each test case

This step grounds test scenarios in actual implementation and prevents speculative tests.

## Module Code Mapping

| Service     | Code |
| ----------- | ---- |
| TextSnippet | TXT  |
| ExampleApp  | EXP  |
| Accounts    | ACC  |
| Common      | COM  |

### Related
- **Role Skill:** `qa-engineer`
- **Command:** `/test-spec`
- **Input:** `/story` output
- **Next Step:** `/test-cases`

## Example

```bash
/test-spec team-artifacts/pbis/260119-pbi-dark-mode-toggle.md
```

Creates: `team-artifacts/test-specs/260119-testspec-dark-mode-toggle.md`

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
