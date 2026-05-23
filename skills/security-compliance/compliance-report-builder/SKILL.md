---
name: compliance-report-builder
description: Эксперт по compliance отчётам. Используй для SOX, GDPR, HIPAA, SOC 2 аудитов и документации соответствия.
---

# Compliance Report Builder

Эксперт по регуляторной compliance документации и отчётности.

## Основные принципы

### Evidence-Based Documentation
- Контроли должны быть связаны с конкретными артефактами
- Audit trail с timestamps и ответственными
- Количественные метрики для preventive и detective мер

### Risk-Oriented Approach
- Приоритизация high-risk областей
- Mapping контролей к threat vectors
- Документирование residual risk

### Regulatory Alignment
- Привязка требований к конкретным статьям регуляций
- Guidance для неоднозначных стандартов
- Compensating controls документация

## Executive Summary Template

```markdown
# Compliance Status Report
**Period:** Q4 2024
**Prepared:** 2024-12-10
**Classification:** Confidential

## Overall Status: 🟡 YELLOW

### Coverage Summary
| Framework | Controls | Compliant | Gaps | Coverage |
|-----------|----------|-----------|------|----------|
| SOC 2 | 85 | 79 | 6 | 93% |
| GDPR | 42 | 40 | 2 | 95% |
| ISO 27001 | 114 | 108 | 6 | 95% |

### Key Findings
| Priority | Count | Trend |
|----------|-------|-------|
| Critical | 0 | ⬇️ |
| High | 3 | ➡️ |
| Medium | 8 | ⬆️ |
| Low | 12 | ➡️ |

### Action Items
1. [CRITICAL] None
2. [HIGH] Complete MFA rollout by Jan 15
3. [HIGH] Update data retention policy
4. [HIGH] Implement logging for System X
```

## Control Assessment Framework

```yaml
Control:
  ID: AC-001
  Title: Access Control Policy
  Framework: SOC 2, ISO 27001
  Category: Security

Implementation:
  Status: Implemented
  Owner: Security Team
  Last Review: 2024-12-01

Testing:
  Method: Inspection + Inquiry
  Frequency: Quarterly
  Last Test: 2024-11-15
  Result: Effective

Evidence:
  - Policy document v2.3
  - Access review logs
  - Training completion records

Gaps:
  - None identified

Recommendations:
  - Automate quarterly access reviews
```

## SOC 2 Trust Services

```markdown
## Security (Common Criteria)

### CC1: Control Environment
| Control | Description | Status | Evidence |
|---------|-------------|--------|----------|
| CC1.1 | Board oversight | ✅ | Board minutes |
| CC1.2 | Management philosophy | ✅ | Policy docs |
| CC1.3 | Organizational structure | ✅ | Org chart |
| CC1.4 | HR practices | ✅ | HR policies |

### CC2: Communication and Information
| Control | Description | Status | Evidence |
|---------|-------------|--------|----------|
| CC2.1 | Information quality | ✅ | Data governance |
| CC2.2 | Internal communication | ✅ | Slack, email logs |
| CC2.3 | External communication | ✅ | Customer portal |

### CC3: Risk Assessment
| Control | Description | Status | Evidence |
|---------|-------------|--------|----------|
| CC3.1 | Risk identification | ✅ | Risk register |
| CC3.2 | Risk analysis | ✅ | Risk assessment |
| CC3.3 | Fraud risk | ✅ | Fraud controls |
| CC3.4 | Change management | ⚠️ | Partial automation |
```

## GDPR Checklist

```yaml
Article 30 - Records of Processing:
  - [ ] Processing purposes documented
  - [ ] Data categories listed
  - [ ] Recipient categories identified
  - [ ] Transfer safeguards documented
  - [ ] Retention periods defined
  - [ ] Security measures described

Article 13/14 - Privacy Notices:
  - [ ] Controller identity stated
  - [ ] DPO contact provided
  - [ ] Purposes explained
  - [ ] Legal basis identified
  - [ ] Rights information included
  - [ ] Complaint procedure described

Article 17 - Right to Erasure:
  - [ ] Process documented
  - [ ] Timeframes defined (30 days)
  - [ ] Exceptions listed
  - [ ] Verification procedure
  - [ ] Third-party notification

Article 33 - Breach Notification:
  - [ ] Detection procedures
  - [ ] Assessment criteria
  - [ ] 72-hour notification process
  - [ ] DPA contact established
  - [ ] Subject notification criteria
```

## Risk Assessment Matrix

```javascript
const riskMatrix = {
  likelihood: {
    rare: 1,      // < 5%
    unlikely: 2,  // 5-25%
    possible: 3,  // 25-50%
    likely: 4,    // 50-75%
    certain: 5    // > 75%
  },

  impact: {
    negligible: 1, // < $10k
    minor: 2,      // $10k-$100k
    moderate: 3,   // $100k-$1M
    major: 4,      // $1M-$10M
    severe: 5      // > $10M
  },

  calculateRisk(likelihood, impact) {
    const score = likelihood * impact;
    if (score >= 15) return 'Critical';
    if (score >= 10) return 'High';
    if (score >= 5) return 'Medium';
    return 'Low';
  }
};
```

## Finding Classification

```yaml
Critical:
  Response: 24-48 hours
  Escalation: Executive + Board
  Examples:
    - Active data breach
    - Regulatory violation with penalties
    - System-wide security failure

High:
  Response: 1-2 weeks
  Escalation: Senior Management
  Examples:
    - Missing critical controls
    - Significant gaps in coverage
    - Failed audit controls

Medium:
  Response: 30-60 days
  Escalation: Department Head
  Examples:
    - Incomplete documentation
    - Process inefficiencies
    - Minor policy violations

Low:
  Response: 90 days
  Escalation: Control Owner
  Examples:
    - Optimization opportunities
    - Documentation updates
    - Training gaps
```

## Gap Analysis Template

```markdown
## Gap Analysis: [Control Area]

### Current State
[Description of current implementation]

### Required State
[Regulatory requirement or best practice]

### Gap Description
[Specific gaps identified]

### Risk Assessment
- Likelihood: [1-5]
- Impact: [1-5]
- Risk Score: [calculated]
- Risk Level: [Critical/High/Medium/Low]

### Remediation Plan
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| Action 1 | Name | Date | In Progress |
| Action 2 | Name | Date | Pending |

### Success Metrics
- [ ] Metric 1
- [ ] Metric 2
```

## Audit Sampling

```python
def calculate_sample_size(population: int, confidence: float = 0.95,
                         margin_error: float = 0.05) -> int:
    """
    Calculate statistical sample size for audit testing.

    Args:
        population: Total population size
        confidence: Confidence level (default 95%)
        margin_error: Acceptable margin of error (default 5%)

    Returns:
        Required sample size
    """
    import math

    # Z-score for confidence level
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence, 1.96)

    # Assume 50% response distribution for max sample
    p = 0.5

    # Sample size formula
    n = (z**2 * p * (1-p)) / (margin_error**2)

    # Finite population correction
    if population < 10000:
        n = n / (1 + (n - 1) / population)

    return math.ceil(n)

# Example usage
# population=1000, 95% confidence, 5% margin
# Result: ~278 samples needed
```

## Continuous Monitoring

```yaml
Real-time Dashboards:
  - Control effectiveness scores
  - Compliance coverage %
  - Open findings count
  - Risk heat map

Automated Alerts:
  Critical:
    - Failed security controls
    - Unauthorized access attempts
    - Data breach indicators

  Warning:
    - Controls approaching expiry
    - Overdue remediations
    - Anomaly detection triggers

Reporting Cadence:
  Daily: Critical events
  Weekly: Status summary
  Monthly: Detailed report
  Quarterly: Executive review
  Annually: Full assessment
```

## Report Templates

### Finding Report

```markdown
# Finding Report

**ID:** FND-2024-042
**Date:** 2024-12-10
**Severity:** High

## Summary
[One-sentence description]

## Background
[Context and relevant history]

## Finding Details
[Technical details of the issue]

## Impact Assessment
- Business Impact: [description]
- Regulatory Impact: [description]
- Reputational Impact: [description]

## Root Cause
[Why this happened]

## Recommendation
[Specific remediation steps]

## Management Response
[Owner's response and commitment]

## Timeline
| Milestone | Date | Status |
|-----------|------|--------|
| Finding identified | 2024-12-10 | Complete |
| Remediation plan | 2024-12-15 | Pending |
| Implementation | 2024-01-15 | Pending |
| Verification | 2024-01-30 | Pending |
```

## Лучшие практики

1. **Evidence first** — каждый контроль должен иметь доказательства
2. **Risk-based prioritization** — фокус на high-risk областях
3. **Continuous monitoring** — не ждите годового аудита
4. **Clear ownership** — каждый контроль имеет ответственного
5. **Regular testing** — проверяйте effectiveness, не только design
6. **Documentation discipline** — версионирование и audit trail
