---
name: risk-assessment
description: Identify, analyze, and prioritize project risks using qualitative and quantitative methods. Develop mitigation strategies to minimize impact and maximize project success probability.
---

# Risk Assessment

## Overview

Risk assessment is a systematic process of identifying potential threats to project success and developing strategies to mitigate, avoid, or accept them.

## When to Use

- Project initiation and planning phases
- Before major milestones or decisions
- When introducing new technologies
- Third-party dependencies or integration
- Organizational or resource changes
- Budget or timeline constraints
- Regulatory or compliance concerns

## Instructions

### 1. **Risk Identification Techniques**

```python
# Risk identification framework

class RiskIdentification:
    RISK_CATEGORIES = {
        'Technical': [
            'Technology maturity',
            'Integration complexity',
            'Performance requirements',
            'Security vulnerabilities',
            'Data integrity'
        ],
        'Resource': [
            'Team skill gaps',
            'Staff availability',
            'Budget constraints',
            'Equipment/infrastructure',
            'Vendor availability'
        ],
        'Schedule': [
            'Unrealistic deadlines',
            'Dependency delays',
            'Scope creep',
            'Approval delays',
            'Resource conflicts'
        ],
        'External': [
            'Regulatory changes',
            'Market conditions',
            'Vendor stability',
            'Political/economic factors',
            'Natural disasters'
        ],
        'Organizational': [
            'Stakeholder misalignment',
            'Priority changes',
            'Organizational restructuring',
            'Politics/conflicts',
            'Requirement changes'
        ]
    }

    @staticmethod
    def brainstorm_risks(project_context):
        """
        Facilitated brainstorming session to identify risks
        """
        risks = []
        for category, risk_types in RiskIdentification.RISK_CATEGORIES.items():
            for risk_type in risk_types:
                risks.append({
                    'category': category,
                    'description': risk_type,
                    'identified_by': [],
                    'probability': None,
                    'impact': None
                })

        return risks

    @staticmethod
    def analyze_assumptions_as_risks(assumptions):
        """
        Convert project assumptions into potential risks
        """
        assumption_risks = []
        for assumption in assumptions:
            assumption_risks.append({
                'risk_type': 'Assumption Violation',
                'description': f"Assumption '{assumption}' is invalid",
                'trigger': f"Evidence that {assumption} is false",
                'impact': 'High' if assumption.startswith('Critical') else 'Medium'
            })

        return assumption_risks
```

### 2. **Risk Analysis Matrix**

```javascript
// Qualitative and quantitative risk analysis

class RiskAnalysis {
  constructor() {
    this.riskMatrix = [];
    this.priorityMap = [];
  }

  // Probability scale 1-5
  static PROBABILITY = {
    1: { name: 'Very Low', percentage: 0.1, color: 'Green' },
    2: { name: 'Low', percentage: 0.3, color: 'Green' },
    3: { name: 'Medium', percentage: 0.5, color: 'Yellow' },
    4: { name: 'High', percentage: 0.7, color: 'Orange' },
    5: { name: 'Very High', percentage: 0.9, color: 'Red' }
  };

  // Impact scale 1-5
  static IMPACT = {
    1: { name: 'Negligible', value: 1, scope: 'Minor inconvenience' },
    2: { name: 'Minor', value: 10, scope: 'Some delay or cost' },
    3: { name: 'Moderate', value: 100, scope: 'Significant delay or cost' },
    4: { name: 'Major', value: 1000, scope: 'Critical failure risk' },
    5: { name: 'Catastrophic', value: 10000, scope: 'Project cancellation' }
  };

  analyzeRisk(risk) {
    const probability = this.PROBABILITY[risk.probability];
    const impact = this.IMPACT[risk.impact];

    // Risk Score = Probability × Impact
    const riskScore = risk.probability * risk.impact;

    // Risk Exposure = Probability × Financial Impact
    const riskExposure = probability.percentage * impact.value;

    return {
      riskId: risk.id,
      riskScore,
      riskExposure,
      priority: this.calculatePriority(riskScore),
      severity: this.calculateSeverity(riskScore),
      mitigationUrgency: riskExposure > 100 ? 'Immediate' : 'Planned'
    };
  }

  calculatePriority(riskScore) {
    if (riskScore >= 16) return 'Critical';
    if (riskScore >= 12) return 'High';
    if (riskScore >= 6) return 'Medium';
    if (riskScore >= 2) return 'Low';
    return 'Very Low';
  }

  calculateSeverity(riskScore) {
    return {
      score: riskScore,
      rating: this.calculatePriority(riskScore),
      responseNeeded: riskScore >= 12
    };
  }

  // Risk Matrix
  createRiskMatrix(risks) {
    const matrix = {
      critical: [],
      high: [],
      medium: [],
      low: [],
      veryLow: []
    };

    risks.forEach(risk => {
      const analysis = this.analyzeRisk(risk);
      const priority = analysis.priority.toLowerCase();

      if (matrix[priority]) {
        matrix[priority].push({
          ...risk,
          ...analysis
        });
      }
    });

    return matrix;
  }
}
```

### 3. **Risk Response Planning**

```yaml
Risk Response Strategies:

Risk 1: Integration Delay with Third-Party API
  Probability: High (4/5)
  Impact: Major (4/5)
  Risk Score: 16 (Critical)

  Response Strategy: MITIGATION

  Actions:
    - Engage vendor early in planning (Week 1)
    - Develop fallback solution in parallel (Week 2-4)
    - Allocate 20% more development time (buffer)
    - Weekly sync with vendor team
    - Performance testing starts Month 2

  Owner: Technical Lead
  Budget Impact: +$15,000
  Timeline: 6 weeks vs. 4 weeks planned

---

Risk 2: Scope Creep from Stakeholders
  Probability: High (4/5)
  Impact: Moderate (3/5)
  Risk Score: 12 (High)

  Response Strategy: AVOIDANCE & MITIGATION

  Actions:
    - Establish change control process (Week 1)
    - Lock requirements for Phase 1 (Week 2)
    - Monthly scope review meetings
    - Create feature backlog for Phase 2
    - Strict change request evaluation criteria

  Owner: Project Manager
  Cost of Avoidance: 5 hours/week PM time
  Alternative: Accept 2-week timeline extension

---

Risk 3: Key Person Departure
  Probability: Medium (3/5)
  Impact: Major (4/5)
  Risk Score: 12 (High)

  Response Strategy: MITIGATION & CONTINGENCY

  Actions:
    - Knowledge transfer documentation (ongoing)
    - Cross-training second developer (Week 1)
    - Maintain up-to-date runbooks
    - Competitive salary review (HR)
    - Mentoring program setup

  Owner: HR Manager
  Contingency: Hire contractor within 1 week
  Estimated Cost: $20,000
```

### 4. **Risk Monitoring & Control**

```javascript
// Risk tracking and monitoring dashboard

class RiskMonitoring {
  constructor() {
    this.risks = [];
    this.triggers = [];
    this.escalations = [];
  }

  createRiskRegister(risks) {
    return risks.map((risk, index) => ({
      id: `RK-${String(index + 1).padStart(3, '0')}`,
      description: risk.description,
      category: risk.category,
      probability: risk.probability,
      impact: risk.impact,
      riskScore: risk.probability * risk.impact,
      responseStrategy: risk.strategy,
      owner: risk.owner,
      status: 'Active',
      triggers: risk.triggers,
      contingencyPlan: risk.contingency,
      createdDate: new Date(),
      lastReviewDate: new Date(),
      closeDate: null
    }));
  }

  identifyRiskTriggers(risk) {
    return {
      riskId: risk.id,
      triggers: [
        {
          trigger: 'Vendor communication delay >1 week',
          indicator: 'No response from vendor',
          escalationAction: 'Contact vendor PM, evaluate alternatives'
        },
        {
          trigger: 'Team member absence >3 days',
          indicator: 'Unplanned time off',
          escalationAction: 'Activate cross-training plan'
        },
        {
          trigger: 'Performance test fails baseline',
          indicator: 'Response time > 500ms',
          escalationAction: 'Emergency optimization sprint'
        }
      ],
      reviewFrequency: 'Weekly standup'
    };
  }

  monitorRisks(riskRegister) {
    const statusReport = {
      timestamp: new Date(),
      summary: {
        total: riskRegister.length,
        active: riskRegister.filter(r => r.status === 'Active').length,
        mitigated: riskRegister.filter(r => r.status === 'Mitigated').length,
        closed: riskRegister.filter(r => r.status === 'Closed').length
      },
      criticalRisks: riskRegister.filter(r => r.riskScore >= 16),
      highRisks: riskRegister.filter(r => r.riskScore >= 12 && r.riskScore < 16),
      triggeredRisks: riskRegister.filter(r => r.triggered === true)
    };

    return statusReport;
  }
}
```

## Best Practices

### ✅ DO
- Identify risks early in project planning
- Involve diverse team members in risk identification
- Quantify risk impact when possible
- Prioritize based on risk score and exposure
- Develop specific mitigation plans
- Assign clear risk ownership
- Monitor triggers regularly
- Review and update risk register monthly
- Document lessons learned from realized risks
- Communicate risks transparently to stakeholders

### ❌ DON'T
- Wait until problems occur to identify risks
- Assume risks will not materialize
- Treat all risks as equal priority
- Plan mitigation without clear trigger conditions
- Ignore early warning signs
- Make risk management a one-time activity
- Skip contingency planning for critical risks
- Hide negative risks from stakeholders
- Eliminate all risk (impossible and uneconomical)
- Blame individuals for realized risks

## Risk Management Tips

- Risk ownership motivates accountability
- Regular risk review prevents surprises
- Risk response should be cost-effective
- Some risk tolerance is healthy and necessary
- Documented risks are easier to manage
