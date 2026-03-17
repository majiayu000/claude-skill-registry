---
name: qc-specialist
version: 1.1.0
description: '[Project Management] Enforce quality gates, verify compliance with standards, track quality metrics, and generate audit trails. Triggers: quality gate, compliance, audit trail, quality metrics, qc specialist, standards verification.'
allowed-tools: Read, Grep, Glob, TaskCreate, Write
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Enforce quality gates, verify compliance with standards, and track quality metrics across the development lifecycle.

**Workflow:**

1. **Identify Gate** — Determine which quality gate applies (Idea>PBI, PBI>Dev, Dev>QA, QA>Release)
2. **Verify Checklist** — Run through pass/fail criteria for the gate stage
3. **Generate Report** — Produce PASS/FAIL/CONDITIONAL gate status with evidence
4. **Track Metrics** — Log in audit trail and update quality metrics dashboard

**Key Rules:**

- Every gate must have a clear PASS/FAIL/CONDITIONAL status
- Evidence must be provided for critical checklist items
- Sign-offs are required before release gates can pass

# QC Specialist Assistant

Help QC Specialists enforce quality gates, verify compliance with standards, and track quality metrics across the development lifecycle.

---

## Core Capabilities

### 1. Quality Gates

Define pass/fail criteria at each stage:

#### Gate: Idea → PBI

- [ ] Problem statement present
- [ ] Business value articulated
- [ ] No technical solution prescribed
- [ ] Target users identified

#### Gate: PBI → Development

- [ ] Acceptance criteria in GIVEN/WHEN/THEN
- [ ] Out of scope defined
- [ ] Dependencies identified
- [ ] Design approved (if applicable)

#### Gate: Development → QA

- [ ] Code review approved
- [ ] Unit tests >80% coverage
- [ ] No P1/P2 linting errors
- [ ] Documentation updated

#### Gate: QA → Release

- [ ] All test cases executed
- [ ] No open P1/P2 bugs
- [ ] Regression suite passed
- [ ] PO sign-off received

### 2. Compliance Verification

- Code follows architecture patterns
- Security requirements met
- Accessibility standards (WCAG 2.1 AA)
- Performance benchmarks

### 3. Audit Trail

Track artifact lifecycle:

```
{Artifact} | {Action} | {By} | {Date} | {Notes}
```

### 4. Quality Metrics

#### Code Quality

- Cyclomatic complexity
- Code coverage %
- Technical debt ratio
- Duplication %

#### Process Quality

- Defect escape rate
- First-time-right %
- Cycle time
- Lead time

---

## Quality Gate Checklists

### Pre-Development Checklist

```markdown
## Quality Gate: PBI Ready for Development

**PBI:** {PBI-ID}
**Reviewer:** {Name}
**Date:** {Date}

### Requirements

- [ ] Clear problem statement
- [ ] User value articulated
- [ ] Acceptance criteria in GIVEN/WHEN/THEN format
- [ ] Out of scope explicitly listed

### Design

- [ ] Design spec approved (if UI changes)
- [ ] API contract defined (if backend changes)
- [ ] Database changes documented (if applicable)

### Dependencies

- [ ] Upstream dependencies identified
- [ ] No blocking dependencies
- [ ] Integration points documented

### Gate Status: PASS / FAIL / CONDITIONAL

**Notes:**
{Any concerns or conditions}
```

### Pre-Release Checklist

```markdown
## Quality Gate: Ready for Release

**Feature:** {Feature name}
**Release:** {Version}
**Date:** {Date}

### Testing

- [ ] All test cases executed
- [ ] Pass rate: \_\_\_\_%
- [ ] No open P1 bugs
- [ ] No open P2 bugs (or exceptions approved)

### Code Quality

- [ ] Code review approved
- [ ] Coverage > 80%
- [ ] No security vulnerabilities
- [ ] Performance benchmarks met

### Documentation

- [ ] User documentation updated
- [ ] API documentation current
- [ ] Release notes drafted

### Sign-Offs

- [ ] QA Lead: **\*\***\_**\*\*** Date: **\_\_\_**
- [ ] Dev Lead: **\*\***\_**\*\*** Date: **\_\_\_**
- [ ] PO: **\*\*\*\***\_\_**\*\*\*\*** Date: **\_\_\_**

### Gate Status: PASS / FAIL

**Release Decision:**
{Go / No-Go with notes}
```

---

## Workflow Integration

### Running Quality Gate

When user runs `/quality-gate {artifact-or-pr}`:

1. Identify gate type based on artifact/stage
2. Load appropriate checklist
3. Verify each criterion
4. Generate pass/fail report
5. Log in audit trail

---

## Metrics Dashboard Template

```markdown
## Quality Metrics - Sprint {N}

### Code Quality

| Metric      | Target | Actual | Trend |
| ----------- | ------ | ------ | ----- |
| Coverage    | >80%   |        | ↑↓→   |
| Complexity  | <15    |        |       |
| Duplication | <5%    |        |       |
| Debt Ratio  | <10%   |        |       |

### Process Quality

| Metric            | Target | Actual |
| ----------------- | ------ | ------ |
| Defect Escape     | <5%    |        |
| First-Time-Right  | >90%   |        |
| Avg Review Cycles | <2     |        |

### Defect Trends

| Sprint | Found | Fixed | Escaped |
| ------ | ----- | ----- | ------- |
| N-2    |       |       |         |
| N-1    |       |       |         |
| N      |       |       |         |
```

---

## Output Conventions

### File Naming

```
{YYMMDD}-qc-gate-{stage}-{slug}.md
{YYMMDD}-qc-audit-{feature}.md
{YYMMDD}-qc-metrics-sprint-{n}.md
```

---

## Quality Checklist

Before completing QC artifacts:

- [ ] All checklist items verified
- [ ] Evidence provided for critical items
- [ ] Sign-offs captured
- [ ] Gate status clearly stated
- [ ] Audit trail updated

## Related

- `test-spec`
- `code-review`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
