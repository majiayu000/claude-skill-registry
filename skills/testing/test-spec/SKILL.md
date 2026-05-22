---
name: test-spec
description: Generate test specifications from PBIs and acceptance criteria. Use when creating test specs, defining test strategy, or planning QA coverage. Triggers on keywords like "test spec", "test specification", "qa spec", "test strategy", "what to test".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
---

# Test Specification

Generate comprehensive test specifications from requirements.

## When to Use
- PBI ready for QA planning
- Need test coverage strategy
- Defining test scope

## Quick Reference

### Workflow
1. Read PBI and user stories
2. Extract acceptance criteria
3. Identify test scenarios (positive/negative/edge)
4. Define test categories and coverage
5. Create test spec artifact
6. Save to `team-artifacts/test-specs/`
7. Suggest next: `/test-cases`

### Test Categories
| Category | Purpose |
|----------|---------|
| Positive | Happy path verification |
| Negative | Error handling |
| Boundary | Edge values |
| Integration | Component interaction |
| Security | Auth, injection, XSS |

### Output
- **Path:** `team-artifacts/test-specs/{YYMMDD}-testspec-{feature}.md`
- **ID Pattern:** `TS-{MOD}-{NNN}`

### Spec Structure
1. Overview
2. Test Scope
3. Test Categories
4. Test Scenarios (high-level)
5. Coverage Requirements
6. Test Data Needs

### Related
- **Role Skill:** `qa-engineer`
- **Command:** `/test-spec`
- **Input:** `/story` output
- **Next Step:** `/test-cases`

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
