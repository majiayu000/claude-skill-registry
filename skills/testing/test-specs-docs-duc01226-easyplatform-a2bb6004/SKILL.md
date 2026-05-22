---
name: test-specs-docs
description: Create or update EasyPlatform test specifications in docs/test-specs/{Module}/. Covers external memory-driven analysis, 4-priority test generation, comprehensive document structure with ERD and traceability. Triggers on "test specs", "test specifications", "test cases", "test scenarios", "QA documentation", "Given-When-Then", "BDD", "TDD", "coverage".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

> **Skill Variant:** Use this skill for **interactive test writing**. For autonomous test generation, use `tasks-test-generation`.

# EasyPlatform Test Specifications Documentation

Generate comprehensive test specifications with Given-When-Then format and code evidence.

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **⚠️ MUST READ** `references/test-case-templates.md` — document structure, test case template, priority groups, analysis methodology
- **⚠️ MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` — BDD/Gherkin format templates
- **⚠️ MUST READ** `.claude/skills/shared/anti-hallucination-protocol.md` — validation checkpoints, confidence levels

## Output Structure
```
docs/test-specs/
  README.md                     # Master index
  PRIORITY-INDEX.md             # Tests by P0-P3
  INTEGRATION-TESTS.md          # Cross-module scenarios
  VERIFICATION-REPORT.md        # Verification status
  {Module}/README.md            # Module test specs
```

## Test Case ID Format
```
TC-[MODULE]-[FEATURE]-[NUM]
```
Examples: `TC-TXT-SNP-001`, `TC-ACC-AUTH-001`

## Priority Classification
| Priority | Level    | Description                    |
| -------- | -------- | ------------------------------ |
| **P0**   | Critical | Security, auth, data integrity |
| **P1**   | High     | Core business workflows        |
| **P2**   | Medium   | Secondary features, filters    |
| **P3**   | Low      | UI enhancements, non-essential |

## Workflow

### Phase 1: Context Gathering
1. Identify target module from user input or codebase search
2. Read existing specs: `docs/test-specs/README.md`, `{Module}/README.md`, `PRIORITY-INDEX.md`
3. Gather code evidence: Validate() methods, entity rules, [PlatformAuthorize], handler conditionals

### Phase 2: Test Generation
1. Build knowledge model using external memory-driven analysis (see `references/test-case-templates.md`)
2. Generate test cases in 4 priority groups: Critical, High, Medium, Low
3. Use mandatory document structure from references
4. Include: Feature Overview, ERD, Test Cases, Traceability Matrix, Coverage Analysis

### Phase 3: Index Updates
- Update `PRIORITY-INDEX.md` with new test cases
- Update master `README.md` with module links

### Phase 4: Approval Gate
Present test plan with coverage analysis for explicit approval before finalizing.

## Evidence Requirements
Every test case MUST include:
1. Controller reference with authorization policies
2. Handler/Command reference with line numbers
3. Code snippet in `<details>` block
4. Related files table (Backend/Frontend layers)

## Quality Checklist
- [ ] IDs follow TC-[MODULE]-[FEATURE]-[NUM] format
- [ ] All IDs unique (verified against PRIORITY-INDEX.md)
- [ ] Given-When-Then format for all test steps
- [ ] Both success and failure acceptance criteria
- [ ] Test data in JSON format
- [ ] Edge cases documented
- [ ] Code evidence with file paths and line numbers
- [ ] PRIORITY-INDEX.md updated


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
