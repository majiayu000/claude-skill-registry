---
name: quality-gate
description: Run quality gate checklists for development stages. Covers 4 stage gates (Idea>PBI, PBI>Dev, Dev>QA, QA>Release), compliance verification (architecture, security, accessibility, performance), audit trails, and quality metrics. Triggers on "quality gate", "qa gate", "pre-release", "checklist", "gate check", "compliance", "quality metrics", "QC review".
infer: true
allowed-tools: Read, Write, Grep, Glob, Bash, TodoWrite
---

# Quality Gate

Verify artifacts meet quality criteria at development stages.

## When to Use
- Before starting development (pre-dev)
- Before QA handoff (pre-qa)
- Before release (pre-release)
- Compliance verification needed
- Quality metrics tracking

## ⚠️ MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **⚠️ MUST READ** `references/quality-checklists.md` — stage gate details, pre-dev/pre-release checklists, compliance verification, audit trail format, metrics dashboard template, output naming conventions

## Quick Reference: Gate Types

### Pre-Development
- [ ] Problem statement clear
- [ ] Acceptance criteria in GIVEN/WHEN/THEN
- [ ] Out of scope defined
- [ ] Dependencies identified
- [ ] Design approved (if UI)

### Pre-QA
- [ ] Code review approved
- [ ] Unit tests >80% coverage
- [ ] No P1 linting errors
- [ ] Documentation updated

### Pre-Release
- [ ] All test cases executed
- [ ] No open P1/P2 bugs
- [ ] Regression suite passed
- [ ] PO sign-off received

## Workflow
1. Identify gate type (from target arg or artifact type)
2. Load appropriate checklist (see `references/quality-checklists.md`)
3. Verify each criterion against artifact/code
4. Check compliance areas: Architecture, Security, Accessibility, Performance
5. Note pass/fail/conditional for each item
6. Generate report with audit trail
7. Save to `team-artifacts/qc-reports/`

## Report Template
```markdown
## Quality Gate: {Type}

**Target:** {artifact/PR}
**Date:** {date}

### Results
| Criterion | Status         | Notes  |
| --------- | -------------- | ------ |
| {item}    | PASS/FAIL/WARN | {note} |

### Compliance
| Area          | Status    |
| ------------- | --------- |
| Architecture  | PASS/FAIL |
| Security      | PASS/FAIL |
| Accessibility | PASS/FAIL |
| Performance   | PASS/FAIL |

### Gate Status: PASS / FAIL / CONDITIONAL
```

## Output
- **Path:** `team-artifacts/qc-reports/{YYMMDD}-gate-{type}-{slug}.md`
- **Status:** PASS | FAIL | CONDITIONAL

## Example
```bash
/quality-gate pre-dev team-artifacts/pbis/260119-pbi-dark-mode-toggle.md
/quality-gate pre-release PR#123
```


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
