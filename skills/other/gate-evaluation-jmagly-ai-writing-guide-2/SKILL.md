# gate-evaluation

Validate phase gate criteria with multi-agent review and generate pass/fail reports.

## Triggers

- "check gate for [phase]"
- "can we transition to [phase]"
- "validate [LOM/ABM/IOC/PRM]"
- "are we ready for [phase]"
- "gate check"
- "phase readiness"

## Purpose

This skill validates that all exit criteria for a phase are met before transitioning to the next phase. It orchestrates multiple validators to ensure comprehensive assessment.

## Behavior

When triggered, this skill:

1. **Identifies target gate**:
   - Parse phase name or milestone
   - Load gate criteria for that phase
   - Map criteria to validator agents

2. **Inventories artifacts**:
   - Check required artifacts exist
   - Verify artifact status (baselined vs draft)
   - Check version requirements

3. **Dispatches validators**:
   - Launch parallel validators via `parallel-dispatch`
   - Each validator checks their domain criteria
   - Collect pass/fail per criterion

4. **Aggregates results**:
   - Calculate gate score
   - Identify blocking issues
   - Generate recommendations

5. **Produces gate report**:
   - Structured report with all criteria
   - Clear pass/fail status
   - Remediation guidance for failures

## Gate Definitions

### LOM - Lifecycle Objective Milestone (Inception Exit)

```yaml
gate: LOM
phase: inception
description: Validate problem, vision, and business case

criteria:
  vision:
    description: Vision document exists and is approved
    artifacts: [".aiwg/requirements/vision.md"]
    status: approved
    validator: product-strategist

  business_case:
    description: Business case with ROI justification
    artifacts: [".aiwg/management/business-case.md"]
    status: approved
    validator: executive-orchestrator

  stakeholders:
    description: Stakeholder agreement documented
    artifacts: [".aiwg/management/stakeholder-agreement.md"]
    status: approved
    validator: project-manager

  scope:
    description: Initial scope and boundaries defined
    artifacts: [".aiwg/requirements/scope.md"]
    status: draft  # can be draft at this stage
    validator: requirements-analyst

  risks:
    description: Initial risk list with top 10 risks
    artifacts: [".aiwg/risks/risk-register.md"]
    min_risks: 10
    validator: project-manager

  architecture_sketch:
    description: High-level architecture concept
    artifacts: [".aiwg/architecture/architecture-sketch.md"]
    status: draft
    validator: architecture-designer

  security_screening:
    description: Initial security classification
    artifacts: [".aiwg/security/data-classification.md"]
    validator: security-architect
```

### ABM - Architecture Baseline Milestone (Elaboration Exit)

```yaml
gate: ABM
phase: elaboration
description: Architecture stable, major risks retired

criteria:
  sad:
    description: Software Architecture Document baselined
    artifacts: [".aiwg/architecture/sad.md"]
    status: baselined
    validator: architecture-designer

  adrs:
    description: Key Architecture Decision Records
    artifacts: [".aiwg/architecture/adr-*.md"]
    min_count: 3
    validator: architecture-designer

  requirements_baseline:
    description: Requirements documented and traced
    artifacts:
      - ".aiwg/requirements/use-cases/*.md"
      - ".aiwg/requirements/supplementary-spec.md"
    validator: requirements-analyst

  risk_retirement:
    description: Top risks retired or mitigated
    artifacts: [".aiwg/risks/risk-register.md"]
    check: risks_retired_percentage >= 60
    validator: project-manager

  test_strategy:
    description: Test strategy defined
    artifacts: [".aiwg/testing/test-strategy.md"]
    status: approved
    validator: test-architect

  security_architecture:
    description: Security architecture reviewed
    artifacts: [".aiwg/security/threat-model.md"]
    status: approved
    validator: security-architect
```

### IOC - Initial Operational Capability (Construction Exit)

```yaml
gate: IOC
phase: construction
description: System functional, ready for deployment

criteria:
  features_complete:
    description: All planned features implemented
    check: features_completion >= 100
    validator: product-manager

  tests_passing:
    description: All automated tests pass
    check: test_pass_rate >= 95
    validator: test-architect

  coverage:
    description: Adequate test coverage
    check: test_coverage >= 80
    validator: test-architect

  security_scan:
    description: Security scan clean (no critical/high)
    check: security_critical == 0 AND security_high == 0
    validator: security-auditor

  performance:
    description: Performance meets NFRs
    artifacts: [".aiwg/testing/performance-results.md"]
    validator: performance-engineer

  defects_triaged:
    description: All defects triaged, no P0/P1 open
    check: critical_defects == 0
    validator: test-architect

  deployment_plan:
    description: Deployment plan approved
    artifacts: [".aiwg/deployment/deployment-plan.md"]
    status: approved
    validator: deployment-manager
```

### PRM - Product Release Milestone (Transition Exit)

```yaml
gate: PRM
phase: transition
description: Product ready for production

criteria:
  deployment_proven:
    description: Deployment validated in staging
    artifacts: [".aiwg/deployment/staging-validation.md"]
    validator: devops-engineer

  user_acceptance:
    description: UAT passed
    artifacts: [".aiwg/testing/uat-results.md"]
    check: uat_pass_rate >= 100
    validator: test-architect

  support_ready:
    description: Support team trained, runbooks ready
    artifacts:
      - ".aiwg/deployment/support-runbook.md"
      - ".aiwg/deployment/training-completion.md"
    validator: support-lead

  rollback_plan:
    description: Rollback procedure documented and tested
    artifacts: [".aiwg/deployment/rollback-plan.md"]
    validator: devops-engineer

  monitoring:
    description: Monitoring and alerting configured
    artifacts: [".aiwg/deployment/monitoring-config.md"]
    validator: reliability-engineer

  compliance:
    description: All compliance requirements met
    validator: legal-liaison
```

## Validation Process

```
┌─────────────────────────────────────────────────────────┐
│ 1. LOAD GATE CRITERIA                                   │
│    • Identify target gate (LOM, ABM, IOC, PRM)          │
│    • Load criteria definitions                          │
│    • Map validators                                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. ARTIFACT INVENTORY                                   │
│    • Check each required artifact exists                │
│    • Verify artifact status (draft/approved/baselined)  │
│    • Record missing or invalid artifacts                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. PARALLEL VALIDATION                                  │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │
│    │ architecture│ │ security    │ │ test        │     │
│    │ designer    │ │ gatekeeper  │ │ architect   │     │
│    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘     │
│           │               │               │            │
│           ▼               ▼               ▼            │
│    [arch criteria] [sec criteria] [test criteria]      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. AGGREGATE RESULTS                                    │
│    • Count pass/fail per criterion                      │
│    • Calculate gate score (passed/total)                │
│    • Identify blocking issues                           │
│    • Generate recommendations                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 5. GENERATE REPORT                                      │
│    • Gate status: PASS / CONDITIONAL / FAIL             │
│    • Detailed criteria results                          │
│    • Blocking issues list                               │
│    • Remediation guidance                               │
│    • Output: .aiwg/gates/{phase}-gate-report.md         │
└─────────────────────────────────────────────────────────┘
```

## Gate Report Format

```markdown
# Gate Evaluation Report: ABM (Architecture Baseline)

**Date**: 2025-12-08
**Evaluator**: gate-evaluation skill
**Status**: CONDITIONAL

## Summary

| Metric | Value |
|--------|-------|
| Criteria Evaluated | 6 |
| Passed | 5 |
| Conditional | 1 |
| Failed | 0 |
| Gate Score | 83% |

## Criteria Results

### ✅ PASS: SAD Baselined
- Artifact: .aiwg/architecture/sad.md
- Status: baselined (v1.0.0)
- Validator: architecture-designer
- Notes: Comprehensive, all sections complete

### ✅ PASS: ADRs Complete
- Artifacts: 5 ADRs found
- Required: 3 minimum
- Validator: architecture-designer

### ⚠️ CONDITIONAL: Risk Retirement
- Current: 55% risks retired
- Required: 60%
- Validator: project-manager
- **Action Required**: Retire 2 more risks or document mitigation

### ✅ PASS: Test Strategy
- Artifact: .aiwg/testing/test-strategy.md
- Status: approved
- Validator: test-architect

### ✅ PASS: Security Architecture
- Artifact: .aiwg/security/threat-model.md
- Status: approved
- Validator: security-architect

### ✅ PASS: Requirements Baseline
- Artifacts: 12 use cases, supplementary spec
- Validator: requirements-analyst

## Blocking Issues

1. **Risk Retirement Short** (CONDITIONAL)
   - Gap: 5% below threshold
   - Remediation: Complete spike for RISK-007, document mitigation for RISK-012

## Recommendations

1. Address the conditional risk retirement before proceeding
2. Consider re-validating in 3-5 days after risk work
3. Gate can proceed with documented exception if stakeholder approves

## Next Steps

- [ ] Complete risk mitigation actions
- [ ] Re-run gate check: `/flow-gate-check elaboration`
- [ ] On PASS, proceed to: `/flow-elaboration-to-construction`
```

## Usage Examples

### Check Elaboration Gate

```
User: "Can we transition to Construction?"

Skill evaluates ABM criteria:
- Checks SAD, ADRs, requirements
- Validates security architecture
- Verifies risk retirement
- Generates report

Output:
"ABM Gate Evaluation: CONDITIONAL

5/6 criteria passed
1 conditional: Risk retirement at 55% (need 60%)

Blocking:
- Retire 2 more risks or get exception approval

Recommendation: Address risks, re-check in 3-5 days"
```

### Quick Gate Status

```
User: "Gate check"

Skill detects current phase from project-awareness:
- Phase: Elaboration
- Runs ABM check
- Returns summary
```

## Integration

This skill uses:
- `parallel-dispatch`: For launching validator agents
- `project-awareness`: For detecting current phase
- `artifact-metadata`: For checking artifact status

## Gate Status Definitions

| Status | Meaning | Action |
|--------|---------|--------|
| PASS | All criteria met | Proceed to next phase |
| CONDITIONAL | Minor gaps, workarounds exist | Proceed with documented exceptions |
| FAIL | Blocking issues present | Must remediate before proceeding |

## Output Location

Gate reports: `.aiwg/gates/{phase}-gate-report.md`

Examples:
- `.aiwg/gates/inception-gate-report.md`
- `.aiwg/gates/elaboration-gate-report.md`
- `.aiwg/gates/construction-gate-report.md`
- `.aiwg/gates/transition-gate-report.md`

## References

- Gate criteria: docs/gate-criteria.md
- Phase transitions: flows/
- Validator agents: agents/
