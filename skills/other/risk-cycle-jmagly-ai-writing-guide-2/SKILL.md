# risk-cycle

Continuous risk identification, assessment, tracking, and retirement throughout SDLC.

## Triggers

- "risk review"
- "update risks"
- "new risk"
- "risk status"
- "mitigate risk"
- "retire risk"
- "risk cycle"

## Purpose

This skill manages continuous risk management by:
- Identifying new risks from project activities
- Assessing risk severity and probability
- Tracking mitigation progress
- Escalating overdue or critical risks
- Retiring completed risk mitigations
- Generating risk reports for stakeholders

## Behavior

When triggered, this skill:

1. **Reviews current state**:
   - Load risk register
   - Check mitigation status
   - Identify overdue items

2. **Identifies new risks**:
   - Analyze recent changes
   - Review technical decisions
   - Check external factors
   - Gather team input

3. **Assesses risks**:
   - Score probability and impact
   - Calculate risk score
   - Prioritize by exposure

4. **Plans mitigations**:
   - Assign owners
   - Define mitigation actions
   - Set target dates

5. **Tracks progress**:
   - Update mitigation status
   - Escalate overdue items
   - Retire completed risks

6. **Reports status**:
   - Generate risk dashboard
   - Highlight top risks
   - Show trend over time

## Risk Categories

### Technical Risks

```yaml
technical_risks:
  architecture:
    examples:
      - Scalability bottleneck
      - Single point of failure
      - Technology obsolescence
      - Integration complexity
    indicators:
      - Performance degradation
      - System failures
      - Upgrade difficulties

  development:
    examples:
      - Technical debt accumulation
      - Code quality issues
      - Testing gaps
      - Dependency vulnerabilities
    indicators:
      - Increasing bug count
      - Slower velocity
      - Failed deployments

  security:
    examples:
      - Data breach potential
      - Authentication weaknesses
      - Compliance gaps
      - Third-party risks
    indicators:
      - Security scan findings
      - Audit failures
      - Incident reports
```

### Project Risks

```yaml
project_risks:
  schedule:
    examples:
      - Scope creep
      - Delayed dependencies
      - Unrealistic estimates
      - Resource constraints
    indicators:
      - Missed milestones
      - Velocity decline
      - Scope changes

  resource:
    examples:
      - Key person dependency
      - Skill gaps
      - Team turnover
      - Burnout risk
    indicators:
      - Unbalanced workload
      - Low morale
      - Resignation signals

  stakeholder:
    examples:
      - Changing requirements
      - Sponsor availability
      - Organizational changes
      - Competing priorities
    indicators:
      - Decision delays
      - Priority conflicts
      - Reduced engagement
```

### External Risks

```yaml
external_risks:
  market:
    examples:
      - Competitor actions
      - Market shift
      - Economic factors
      - Regulatory changes
    indicators:
      - Market news
      - Competitor releases
      - Industry reports

  vendor:
    examples:
      - Vendor stability
      - API changes
      - Price increases
      - Support quality
    indicators:
      - Vendor communications
      - Service issues
      - Contract terms

  compliance:
    examples:
      - Regulatory requirements
      - Industry standards
      - Audit requirements
      - Data regulations
    indicators:
      - Regulatory updates
      - Audit findings
      - Compliance gaps
```

## Risk Assessment Matrix

### Probability Scoring

```yaml
probability:
  certain:
    score: 5
    likelihood: ">90%"
    description: "Almost certain to occur"

  likely:
    score: 4
    likelihood: "60-90%"
    description: "More likely than not"

  possible:
    score: 3
    likelihood: "30-60%"
    description: "Could occur"

  unlikely:
    score: 2
    likelihood: "10-30%"
    description: "Not expected but possible"

  rare:
    score: 1
    likelihood: "<10%"
    description: "Very unlikely"
```

### Impact Scoring

```yaml
impact:
  catastrophic:
    score: 5
    schedule: ">3 months delay"
    cost: ">50% budget"
    quality: "Unusable product"
    reputation: "Major damage"

  major:
    score: 4
    schedule: "1-3 months delay"
    cost: "25-50% budget"
    quality: "Significant defects"
    reputation: "Serious concern"

  moderate:
    score: 3
    schedule: "2-4 weeks delay"
    cost: "10-25% budget"
    quality: "Noticeable issues"
    reputation: "Some concern"

  minor:
    score: 2
    schedule: "1-2 weeks delay"
    cost: "5-10% budget"
    quality: "Minor issues"
    reputation: "Limited impact"

  negligible:
    score: 1
    schedule: "<1 week delay"
    cost: "<5% budget"
    quality: "Trivial issues"
    reputation: "No impact"
```

### Risk Score Matrix

```
           │ Impact
           │ 1   2   3   4   5
───────────┼─────────────────────
Prob    5  │ 5  10  15  20  25 ←Critical
        4  │ 4   8  12  16  20
        3  │ 3   6   9  12  15 ←High
        2  │ 2   4   6   8  10
        1  │ 1   2   3   4   5  ←Medium
           └─────────────────────
              ↑        ↑
              Low    Medium
```

```yaml
risk_levels:
  critical:
    range: [20, 25]
    response: "Immediate action required"
    escalation: "Executive notification"

  high:
    range: [12, 19]
    response: "Priority mitigation"
    escalation: "Manager notification"

  medium:
    range: [6, 11]
    response: "Planned mitigation"
    escalation: "Team lead notification"

  low:
    range: [1, 5]
    response: "Monitor and accept"
    escalation: "None required"
```

## Risk Register Format

```markdown
# Risk Register

**Project**: [Name]
**Last Updated**: 2025-12-08
**Next Review**: 2025-12-15

## Summary Dashboard

| Risk Level | Count | Trend |
|------------|-------|-------|
| Critical | 1 | ↑ +1 |
| High | 3 | → 0 |
| Medium | 8 | ↓ -2 |
| Low | 12 | → 0 |
| **Total** | **24** | - |

### Risk Trend

```
Week 1: ████████████████████████ 24 risks
Week 2: ██████████████████████ 22 risks
Week 3: ████████████████████████ 24 risks (2 new)
Week 4: ████████████████████████ 24 risks
                                   ↑ Stable with critical +1
```

## Active Risks

### RISK-001: Database Scalability [CRITICAL]

| Attribute | Value |
|-----------|-------|
| ID | RISK-001 |
| Title | Database Scalability Bottleneck |
| Category | Technical / Architecture |
| Probability | 4 (Likely) |
| Impact | 5 (Catastrophic) |
| Score | 20 (Critical) |
| Owner | Sarah Chen |
| Status | Mitigating |

**Description**:
Current PostgreSQL single-instance architecture cannot handle projected 10x traffic growth. Performance degradation expected within 6 months.

**Impact if Realized**:
- Service degradation or outage
- Customer churn
- Revenue loss estimated at $500K/month

**Mitigation Plan**:
1. [x] Evaluate sharding options (complete)
2. [x] Design read replica architecture (complete)
3. [ ] Implement connection pooling (in progress, due Dec 15)
4. [ ] Deploy read replicas (planned, due Jan 15)
5. [ ] Implement sharding (planned, due Feb 15)

**Contingency**:
Emergency vertical scaling + temporary traffic limiting

**Progress**:
```
[████████████░░░░░░░░] 60%
```

---

### RISK-002: Key Person Dependency [HIGH]

| Attribute | Value |
|-----------|-------|
| ID | RISK-002 |
| Title | Key Person Dependency on Lead Architect |
| Category | Project / Resource |
| Probability | 3 (Possible) |
| Impact | 4 (Major) |
| Score | 12 (High) |
| Owner | David Kim |
| Status | Mitigating |

**Description**:
Lead architect holds critical system knowledge. No backup identified.

**Mitigation Plan**:
1. [ ] Document architecture decisions (in progress)
2. [ ] Schedule knowledge transfer sessions
3. [ ] Identify and train backup

---

## Recently Retired Risks

### RISK-012: Third-Party API Stability [RETIRED]

- **Retired**: 2025-12-01
- **Original Score**: 12 (High)
- **Mitigation**: Implemented circuit breaker and fallback
- **Outcome**: Risk eliminated through technical solution

---

## Risk Review Actions

### This Week
- [ ] Complete RISK-001 connection pooling
- [ ] Schedule RISK-002 knowledge transfer
- [ ] Review new vendor contract for RISK-008

### Overdue
- ⚠️ RISK-005: Security audit (2 days overdue)
  - Owner: Elena Rodriguez
  - Escalated to: Team Lead
```

## Usage Examples

### Risk Review

```
User: "Risk review"

Skill executes:
1. Load current risk register
2. Check mitigation status
3. Identify overdue items
4. Prompt for new risks

Output:
"Risk Review Summary

Current Status:
- Critical: 1 (RISK-001: DB Scalability) ← Action needed
- High: 3
- Medium: 8
- Low: 12

Mitigation Progress:
✅ RISK-001: 60% complete (on track)
✅ RISK-002: 40% complete (on track)
⚠️ RISK-005: Security audit 2 days overdue

Top Priority:
RISK-001 needs connection pooling by Dec 15

Questions:
1. Any new risks identified this week?
2. Update on RISK-005 delay?"
```

### Add New Risk

```
User: "New risk: vendor pricing increase"

Skill guides:
1. Capture risk details
2. Assess probability/impact
3. Add to register

Output:
"Adding New Risk

Let me capture the details:

**Title**: Vendor Pricing Increase
**Category**: External / Vendor

Assessment Questions:
1. How likely is this? (1-5)
2. What's the potential impact? (1-5)
3. When might this occur?
4. Who should own mitigation?

Or say 'quick add' to use defaults."
```

### Mitigate Risk

```
User: "Mitigate RISK-002"

Skill guides:
1. Review current mitigation plan
2. Update progress
3. Adjust actions if needed

Output:
"RISK-002: Key Person Dependency

Current Mitigation Plan:
1. [ ] Document architecture decisions (in progress)
2. [ ] Schedule knowledge transfer sessions
3. [ ] Identify and train backup

Current Progress: 40%

What would you like to update?
1. Mark task complete
2. Add new mitigation action
3. Adjust timeline
4. Escalate issue"
```

### Retire Risk

```
User: "Retire RISK-012"

Skill processes:
1. Verify mitigation complete
2. Document outcome
3. Move to retired list

Output:
"Retiring RISK-012: Third-Party API Stability

Verification:
- Circuit breaker: ✅ Implemented
- Fallback mechanism: ✅ Tested
- Monitoring: ✅ Active

Outcome Documentation:
Risk eliminated through technical solution.
No incidents since mitigation deployed (30 days).

✅ RISK-012 moved to retired risks.
Risk count: 24 → 23"
```

## Integration

This skill uses:
- `project-awareness`: Current phase and activity context
- `artifact-metadata`: Track risk artifact versions
- `decision-support`: Complex risk decisions

## Agent Orchestration

```yaml
agents:
  risk_assessment:
    agent: project-manager
    focus: Project risk evaluation

  technical_analysis:
    agent: architecture-designer
    focus: Technical risk assessment
    condition: risk_category == "technical"

  security_assessment:
    agent: security-architect
    focus: Security risk evaluation
    condition: risk_category == "security"
```

## Configuration

### Review Schedule

```yaml
review_schedule:
  weekly:
    day: "Monday"
    time: "10:00"
    scope: active_risks

  monthly:
    day: 1
    scope: full_register

  phase_gate:
    trigger: gate_check
    scope: blocking_risks
```

### Escalation Rules

```yaml
escalation:
  overdue:
    threshold: 2_days
    notify: owner_manager

  critical_new:
    threshold: score >= 20
    notify: [project_manager, sponsor]

  trend_increase:
    threshold: 3_consecutive_increases
    notify: project_manager
```

## Output Locations

- Risk register: `.aiwg/risks/risk-register.md`
- Risk reports: `.aiwg/risks/reports/`
- Retired risks: `.aiwg/risks/retired/`
- Risk trends: `.aiwg/risks/trends/`

## References

- Risk templates: templates/management/risk-*.md
- Risk matrix: docs/risk-assessment-matrix.md
- Escalation procedures: docs/risk-escalation.md
