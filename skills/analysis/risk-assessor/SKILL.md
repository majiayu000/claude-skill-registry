---
name: Risk Assessor
slug: risk-assessor
description: Identify, analyze, and mitigate project risks using systematic risk management frameworks
category: project
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "assess risks"
  - "identify risks"
  - "risk analysis"
  - "risk management"
  - "what could go wrong"
tags:
  - risk
  - assessment
  - mitigation
  - planning
  - management
---

# Risk Assessor

The Risk Assessor skill helps teams proactively identify, analyze, prioritize, and mitigate project risks before they become problems. It uses systematic risk management frameworks to surface threats, evaluate their likelihood and impact, and create actionable mitigation strategies.

This skill excels at conducting pre-mortem exercises, creating risk registers, assessing probability and impact, developing contingency plans, and establishing early warning indicators to catch risks before they derail projects.

Risk Assessor follows the principle that the best time to handle a risk is before it becomes a crisis. Proactive risk management enables better decisions, realistic planning, and fewer surprises.

## Core Workflows

### Workflow 1: Conduct Risk Assessment

**Steps:**
1. **Risk Identification**
   - **Pre-mortem exercise**: Imagine project failed; what caused it?
   - **Brainstorming**: Team generates potential risks
   - **Category review**: Check common risk categories
     - Technical: Architecture, performance, security, scalability
     - Schedule: Deadlines, dependencies, resource availability
     - Resource: Team capacity, skill gaps, budget constraints
     - External: Market changes, regulatory, vendor dependencies
     - Quality: Bugs, tech debt, user experience
     - Organizational: Stakeholder alignment, priority shifts
   - **Historical analysis**: Review past project issues
   - **Expert input**: Consult specialists (security, legal, etc.)

2. **Risk Documentation**
   - For each risk, document:
     - **Description**: What is the risk?
     - **Category**: What type of risk?
     - **Trigger**: What would cause this risk to occur?
     - **Impact**: What happens if risk occurs?
     - **Owner**: Who monitors and manages this risk?

3. **Probability Assessment**
   - Rate likelihood of occurrence:
     - **Low (1)**: < 10% chance
     - **Medium (2)**: 10-50% chance
     - **High (3)**: > 50% chance
   - Base on data, experience, and expert judgment
   - Document assumptions behind probability

4. **Impact Assessment**
   - Rate severity if risk occurs:
     - **Low (1)**: Minor delay or cost increase
     - **Medium (2)**: Significant schedule or scope impact
     - **High (3)**: Project failure or major business impact
   - Consider multiple dimensions: time, cost, quality, reputation
   - Use worst-case scenario thinking

5. **Risk Prioritization**
   - Calculate Risk Score = Probability × Impact
   - Prioritize by score (1-9 scale):
     - **Critical (7-9)**: Address immediately
     - **High (4-6)**: Develop mitigation plan
     - **Medium (2-3)**: Monitor regularly
     - **Low (1)**: Track but no active mitigation
   - Focus on top 5-10 highest-priority risks

**Output:** Risk register with identified, assessed, and prioritized risks.

### Workflow 2: Develop Mitigation Strategies

**For each high-priority risk:**

1. **Choose Strategy Type**
   - **Avoid**: Eliminate the risk (change approach, remove feature)
   - **Mitigate**: Reduce probability or impact (add testing, hire expert)
   - **Transfer**: Shift risk to third party (insurance, vendor SLA)
   - **Accept**: Acknowledge risk, plan response if occurs

2. **Create Mitigation Plan**
   - Specific actions to reduce risk
   - Assign owners and due dates
   - Define success criteria
   - Estimate cost and effort
   - Identify dependencies

3. **Develop Contingency Plan**
   - "If risk occurs, we will..."
   - Fallback options and alternatives
   - Recovery time objectives
   - Communication plan for stakeholders
   - Resource requirements

4. **Define Early Warning Indicators**
   - Leading indicators that risk is materializing
   - Monitoring frequency and method
   - Threshold for triggering contingency
   - Who watches and who gets alerted

**Output:** Risk mitigation and contingency plans with clear ownership.

### Workflow 3: Monitor and Update Risks

**Weekly:**
1. Review early warning indicators
2. Update probability/impact if conditions change
3. Check status of mitigation actions
4. Add newly identified risks
5. Close resolved or obsolete risks

**Monthly:**
1. Full risk register review
2. Assess effectiveness of mitigations
3. Report top risks to stakeholders
4. Adjust priorities based on new information
5. Update contingency plans

**When triggered:**
- If risk occurs, activate contingency plan
- Document what happened and lessons learned
- Update risk models for future projects

### Workflow 4: Pre-Mortem Exercise

**Facilitated team session (60 min):**

1. **Set the Stage (5 min)**
   - "Imagine it's 6 months from now and this project failed spectacularly"
   - "We're conducting a post-mortem to understand what went wrong"
   - "What caused the failure?"

2. **Individual Brainstorm (10 min)**
   - Each person silently writes failure scenarios
   - Encourage creative and uncomfortable thinking
   - No censoring or filtering

3. **Share Round-Robin (20 min)**
   - Each person shares their scenarios
   - Capture all on shared board
   - No debate or defense, just listen

4. **Group and Prioritize (15 min)**
   - Cluster similar failure modes
   - Vote on most likely or most impactful
   - Identify top 5-10 failure scenarios

5. **Convert to Risks (10 min)**
   - Reframe failures as current risks
   - Add to risk register
   - Assign initial owners

**Output:** List of identified risks from team's collective wisdom.

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Assess risks | "assess risks for [project]" |
| Pre-mortem | "run pre-mortem for [project]" |
| Risk register | "create risk register" |
| Update risks | "update risk status" |
| Top risks | "what are the top risks" |
| Mitigation plan | "create mitigation plan for [risk]" |
| Contingency plan | "plan contingency for [risk]" |
| Risk report | "generate risk report" |

## Best Practices

- **Make it safe**: Encourage honest risk identification; reward raising concerns early
- **Think like a pessimist**: When identifying risks, assume Murphy's Law (what can go wrong, will)
- **Quantify when possible**: Use data and metrics, not just gut feel, for probability and impact
- **Focus on top risks**: Can't mitigate everything; focus on highest-priority risks
- **Own every risk**: Each risk needs a named owner who monitors and drives mitigation
- **Plan before crisis**: Contingency plans made in calm are better than in panic
- **Review regularly**: Risks evolve; weekly review keeps register current and actionable
- **Learn from history**: Past project failures are excellent teachers for future risk identification
- **Update probability as you learn**: As project progresses, adjust probabilities based on new information
- **Don't ignore uncomfortable truths**: The risks you avoid discussing are often the most dangerous
- **Communicate transparently**: Share top risks with stakeholders; surprises destroy trust
- **Balance paranoia and progress**: Risk management shouldn't paralyze; it should inform action

## Risk Categories Checklist

### Technical Risks
- [ ] Unproven or new technology
- [ ] Performance or scalability concerns
- [ ] Security vulnerabilities
- [ ] Integration complexity
- [ ] Technical debt burden
- [ ] Infrastructure reliability
- [ ] Data migration challenges

### Schedule Risks
- [ ] Aggressive or unrealistic timeline
- [ ] Dependencies on other teams/projects
- [ ] Key milestones misaligned
- [ ] Underestimated complexity
- [ ] Holiday or vacation conflicts
- [ ] External deadline pressure

### Resource Risks
- [ ] Insufficient team capacity
- [ ] Key person dependencies (bus factor)
- [ ] Skill gaps or training needs
- [ ] Budget constraints
- [ ] Competing priorities
- [ ] Attrition or turnover

### External Risks
- [ ] Vendor reliability or changes
- [ ] Regulatory or compliance changes
- [ ] Market condition shifts
- [ ] Competitor actions
- [ ] Customer demand uncertainty
- [ ] Third-party API stability

### Quality Risks
- [ ] Inadequate testing coverage
- [ ] Complex or unclear requirements
- [ ] Poor code quality or architecture
- [ ] User experience concerns
- [ ] Accessibility or compliance gaps
- [ ] Browser/device compatibility

### Organizational Risks
- [ ] Stakeholder misalignment
- [ ] Unclear decision-making authority
- [ ] Changing priorities mid-project
- [ ] Political or organizational dynamics
- [ ] Communication breakdowns
- [ ] Cross-team coordination challenges

## Risk Matrix

```
                    IMPACT
              Low (1)  Med (2)  High (3)
PROBABILITY
High (3)      3 (H)    6 (H)    9 (C)
Med (2)       2 (M)    4 (H)    6 (H)
Low (1)       1 (L)    2 (M)    3 (H)

C = Critical  (7-9): Immediate action required
H = High      (4-6): Develop mitigation plan
M = Medium    (2-3): Monitor regularly
L = Low       (1):   Track in register
```

## Mitigation Strategy Decision Tree

```
Can we eliminate this risk entirely?
  YES → AVOID strategy (change approach)
  NO ↓

Can we significantly reduce probability or impact?
  YES → MITIGATE strategy (take action)
  NO ↓

Can someone else manage this better?
  YES → TRANSFER strategy (outsource, insure)
  NO ↓

ACCEPT strategy (plan contingency)
```

## Risk Register Template

```markdown
## Risk Register - [Project Name]

Last Updated: [Date]

### Critical Risks (Score 7-9)

#### R-001: [Risk Title]
- **Description**: [What is the risk?]
- **Category**: Technical | Schedule | Resource | External | Quality | Organizational
- **Probability**: High (3) | Medium (2) | Low (1)
- **Impact**: High (3) | Medium (2) | Low (1)
- **Risk Score**: [P × I]
- **Trigger**: [What causes this?]
- **Owner**: [Name]
- **Status**: Active | Monitoring | Closed
- **Mitigation Strategy**: Avoid | Mitigate | Transfer | Accept
- **Mitigation Actions**:
  - [ ] Action 1 - Owner - Due Date
  - [ ] Action 2 - Owner - Due Date
- **Contingency Plan**: If risk occurs, we will...
- **Early Warning Indicators**: [What to watch for]
- **Last Reviewed**: [Date]

### High Risks (Score 4-6)
[Same format as above]

### Medium Risks (Score 2-3)
[Same format as above]
```

## Common Project Risks & Mitigations

### Risk: Key Developer Leaves Mid-Project
- **Mitigation**: Pair programming, documentation, knowledge sharing
- **Contingency**: Contractor backup, timeline extension
- **Indicator**: Team member disengagement, job searching signals

### Risk: Requirements Change Significantly
- **Mitigation**: Agile approach, frequent stakeholder check-ins, MVP focus
- **Contingency**: Scope negotiation, timeline adjustment
- **Indicator**: Stakeholder dissatisfaction, market feedback

### Risk: Third-Party API Becomes Unreliable
- **Mitigation**: Implement caching, retry logic, circuit breakers
- **Contingency**: Alternative vendor, build in-house
- **Indicator**: Increased error rates, latency spikes

### Risk: Performance Doesn't Meet Requirements
- **Mitigation**: Early performance testing, architecture review
- **Contingency**: Optimization sprint, infrastructure scaling
- **Indicator**: Load test failures, user complaints

### Risk: Security Vulnerability Discovered
- **Mitigation**: Security reviews, penetration testing, dependency scanning
- **Contingency**: Incident response plan, rollback procedure
- **Indicator**: Security alerts, CVE notifications

### Risk: Project Runs Over Budget
- **Mitigation**: Accurate estimation, buffer allocation, cost tracking
- **Contingency**: Scope reduction, additional funding request
- **Indicator**: Burn rate exceeds projections

## Integration Points

- **Project Planner**: Identifies risks during planning phase
- **Sprint Planner**: Reviews risks at sprint planning
- **Task Manager**: Tracks mitigation action items
- **Retrospective Facilitator**: Captures risk learnings
- **Stakeholder Communication**: Reports risk status
- **Incident Management**: Triggers contingency plans
