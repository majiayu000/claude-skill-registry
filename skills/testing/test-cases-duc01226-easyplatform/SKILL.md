---
name: test-cases
description: Generate detailed executable test cases from specifications. Use when creating detailed test cases, expanding test specs, or generating TC-IDs. Triggers on keywords like "test cases", "generate tests", "detailed tests", "TC-", "executable tests".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, TodoWrite
infer: true
---

# Test Case Generation

Create detailed, executable test cases from specifications.

## Pre-Workflow

### Activate Skills

- Activate `qa-engineer` skill for test case design and coverage analysis

## When to Use
- Test spec ready for expansion
- Need detailed test steps
- Generating test case IDs

## Quick Reference

### Workflow
1. Read test specification
2. Extract test scenarios
3. Generate detailed test cases per scenario
4. Assign TC IDs (TC-{MOD}-{NNN})
5. Find code evidence for each case
6. Verify evidence (read each file, confirm line numbers)
7. Update test spec with cases and summary counts
8. Suggest next: `/quality-gate {testspec}`

### Test Case Format
```markdown
#### TC-{MOD}-{NNN}: {Title}
- **Priority:** P1 | P2 | P3
- **Type:** Positive | Negative | Boundary
- **Preconditions:** {Setup}
- **Test Data:** {Requirements}

**Steps:**
1. {Action}
2. {Action}
3. {Verify}

**Expected Result:**
- {Outcome}

**Evidence:** `{file}:{line}`
```

### Module Codes
| Module      | Code |
| ----------- | ---- |
| TextSnippet | TXT  |
| ExampleApp  | EXP  |
| Accounts    | ACC  |
| Common      | COM  |

### Evidence Requirements
**MANDATORY:** Every TC must have evidence.
- Format: `{FilePath}:{LineNumber}`
- Sources: ErrorMessages, validators, handlers

### Related
- **Role Skill:** `qa-engineer`
- **Command:** `/test-cases`
- **Input:** `/test-spec` output
- **Next Step:** `/quality-gate`

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
