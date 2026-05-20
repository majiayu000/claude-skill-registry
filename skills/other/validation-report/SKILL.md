---
name: validation-report
description: Validation report format and testing conventions for verifying implementation against spec. Use when planning, executing, or reporting validation of the runtime against its specification.
---

# Validation Report — Skill

## Purpose

Define the format and approach for independently validating that the implementation satisfies all spec requirements and scenarios.

## When to Use

- Planning a validation phase
- Executing validation tests
- Writing the final validation report

## Output Template

```markdown
# VALIDATION.md — [Project Name]

## 1. Validation Summary
- **Date**: [date]
- **Spec version**: [commit hash of SPEC.md]
- **Implementation version**: [commit hash]
- **Verdict**: PASS | FAIL | PARTIAL

## 2. Environment
- **Node.js version**: [version]
- **OS**: [os]
- **Setup steps**: [how environment was prepared]

## 3. Automated Test Results
- **Command**: `npm test`
- **Exit code**: [0 or non-zero]
- **Output**: [full test output]

## 4. Scenario Coverage Matrix

| Scenario | Spec Section | Requirements | Result | Evidence |
|----------|-------------|-------------|--------|----------|
| [name]   | 6.N         | REQ-XX-NNN  | PASS/FAIL | [output excerpt or test name] |

## 5. Requirement Coverage Matrix

| Requirement | Scenarios Covering It | All Pass? |
|-------------|----------------------|-----------|
| REQ-XX-NNN  | 6.N, 6.M            | Yes/No    |

## 6. Issues Found
[List any failures, with: what failed, expected vs actual, severity, affected requirements.]

## 7. Verdict Rationale
[Evidence-based summary explaining the verdict. Cite specific scenario results.]
```

## Conventions

1. **Clean environment.** Validation starts from a fresh state — no inherited runtime process, no cached modules.
2. **Automated first.** Run `npm test` before any manual checks. The automated suite is the primary evidence.
3. **Every spec scenario (Section 6) must be covered.** If a scenario is not tested by the automated suite, test it manually and document the result.
4. **Every requirement must appear in the coverage matrix.** Requirements not covered by any scenario are flagged.
5. **Evidence is specific.** "It works" is not evidence. Cite test names, HTTP status codes, response bodies, and exact output.
6. **Verdict is conservative.** Any failing scenario means FAIL unless the failure is cosmetic and all requirements are still met.
7. **Use different test data than implementation demos where possible.** Validation should not just replay the happy path the developer tested.

## Quality Checklist

- [ ] All 12 spec scenarios (6.1–6.12) have a row in the coverage matrix
- [ ] All 18 requirements have a row in the requirement coverage matrix
- [ ] `npm test` output is included verbatim
- [ ] Every FAIL result has a specific issue description
- [ ] Verdict matches the evidence (no optimistic overrides)
- [ ] Environment section is complete and reproducible
