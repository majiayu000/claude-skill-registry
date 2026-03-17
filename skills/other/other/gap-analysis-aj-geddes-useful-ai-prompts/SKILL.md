---
name: gap-analysis
description: Identify differences between current state and desired future state. Analyze gaps in capabilities, processes, skills, and technology to plan improvements and investments.
---

# Gap Analysis

## Overview

Gap analysis systematically compares current capabilities with desired future state, revealing what needs to change and what investments are required.

## When to Use

- Strategic planning and goal setting
- Technology modernization assessment
- Process improvement initiatives
- Skills and training planning
- System evaluation and selection
- Organizational change planning
- Capability building programs

## Instructions

### 1. **Gap Identification Framework**

```python
# Systematic gap identification

class GapAnalysis:
    GAP_CATEGORIES = {
        'Business Capability': 'Functions organization can perform',
        'Process': 'How work gets done',
        'Technology': 'Tools and systems available',
        'Skills': 'Knowledge and expertise',
        'Data': 'Information available',
        'People/Culture': 'Team composition and mindset',
        'Organization': 'Structure and roles',
        'Metrics': 'Ability to measure performance'
    }

    def identify_gaps(self, current_state, future_state):
        """Compare current vs desired and find gaps"""
        gaps = []

        for capability in future_state['capabilities']:
            current_capability = self.find_capability(
                capability['name'],
                current_state['capabilities']
            )

            if current_capability is None:
                gaps.append({
                    'capability': capability['name'],
                    'gap_type': 'Missing',
                    'description': f"Organization lacks {capability['name']}",
                    'importance': capability['importance'],
                    'impact': 'High' if capability['importance'] == 'Critical' else 'Medium'
                })
            elif current_capability['maturity'] < capability['target_maturity']:
                gaps.append({
                    'capability': capability['name'],
                    'gap_type': 'Maturity',
                    'current_maturity': current_capability['maturity'],
                    'target_maturity': capability['target_maturity'],
                    'gap_size': capability['target_maturity'] - current_capability['maturity'],
                    'importance': capability['importance'],
                    'impact': 'Medium'
                })

        return gaps

    def prioritize_gaps(self, gaps):
        """Rank gaps by importance and effort"""
        scored_gaps = []

        for gap in gaps:
            importance = self.score_importance(gap)
            effort = self.estimate_effort(gap)
            value = importance / effort if effort > 0 else 0

            scored_gaps.append({
                **gap,
                'importance_score': importance,
                'effort_score': effort,
                'value_score': value,
                'priority': self.assign_priority(value)
            })

        return sorted(scored_gaps, key=lambda x: x['value_score'], reverse=True)

    def score_importance(self, gap):
        """Score how important gap is"""
        if gap['importance'] == 'Critical':
            return 10
        elif gap['importance'] == 'High':
            return 7
        else:
            return 4

    def estimate_effort(self, gap):
        """Estimate effort to close gap"""
        # Returns 1-10 scale
        return gap.get('effort_estimate', 5)

    def assign_priority(self, value_score):
        """Assign priority based on value"""
        if value_score > 2:
            return 'High'
        elif value_score > 1:
            return 'Medium'
        else:
            return 'Low'
```

### 2. **Gap Analysis Template**

```yaml
Gap Analysis Report:

Organization: Customer Analytics Platform
Analysis Date: January 2025
Prepared For: Executive Team

---

Executive Summary:

Current State: Legacy on-premise system with manual processes
Future State: Cloud-native platform with real-time analytics
Gap Magnitude: Significant

Key Findings:
  - 7 critical capability gaps
  - Estimated investment: $500K - $750K
  - Timeline: 12-18 months
  - Primary gaps: Technology, Process, Skills

---

Detailed Gap Analysis:

## Category: Technology

Gap 1: Cloud Infrastructure
  Current: On-premise data center
  Desired: Multi-cloud (AWS primary, Azure backup)
  Gap Size: Large
  Effort: 16 weeks
  Cost: $200K
  Dependencies: None (can start immediately)
  Priority: Critical

Gap 2: Real-Time Data Processing
  Current: Batch processing (nightly)
  Desired: Streaming (sub-second latency)
  Gap Size: Large
  Effort: 20 weeks
  Cost: $150K
  Dependencies: Cloud infrastructure (Gap 1)
  Priority: High

Gap 3: Analytics Tools
  Current: Custom-built dashboard
  Desired: Enterprise BI platform (Tableau/Power BI)
  Gap Size: Medium
  Effort: 8 weeks
  Cost: $80K (software + training)
  Dependencies: Data warehouse modernization
  Priority: High

---

## Category: Skills

Gap 4: Cloud Engineering Expertise
  Current: 0 cloud engineers
  Desired: 3 dedicated cloud engineers
  Gap Size: Large
  Solution: Hire 2, train 1 existing
  Effort: 8 weeks hiring + 4 weeks training
  Cost: $300K annual
  Priority: Critical

Gap 5: Data Science Capability
  Current: 1 analyst (spreadsheet based)
  Desired: 3 data scientists (ML/Python)
  Gap Size: Large
  Solution: Hire 2 data scientists
  Effort: 12 weeks recruiting
  Cost: $400K annual
  Priority: High

---

## Category: Process

Gap 6: Continuous Integration/Deployment
  Current: Manual deployment (quarterly)
  Desired: Automated CI/CD (daily)
  Gap Size: Medium
  Effort: 12 weeks
  Cost: $60K (tools + training)
  Dependencies: Cloud infrastructure
  Priority: High

Gap 7: Data Governance
  Current: Informal, ad-hoc
  Desired: Formal governance framework
  Gap Size: Small
  Effort: 4 weeks
  Cost: $20K (training + tools)
  Dependencies: None
  Priority: Medium

---

## Gap Closure Plan

High Priority Gaps (Start Now):
  1. Cloud Infrastructure - 16 weeks
  2. Cloud Engineering Skills - 8 weeks + training
  3. Data Governance Framework - 4 weeks

Medium Priority Gaps (Start after Cloud ready):
  1. Real-Time Data Processing - 20 weeks (depends on Gap 1)
  2. Analytics Tools - 8 weeks
  3. CI/CD Implementation - 12 weeks

---

Investment Summary:

Capital Expenditure:
  - Cloud infrastructure setup: $200K
  - Technology/tools: $250K
  - Hiring/recruitment: $50K
  - Total CapEx: $500K

Operational Expenditure (Annual):
  - Cloud services: $150K
  - Tool licenses: $80K
  - Salary (3 engineers): $700K
  - Total OpEx: $930K

---

Timeline: 12-18 Months

Q1 2025: Planning & Infrastructure
  - Finalize architecture
  - Begin cloud migration
  - Recruit cloud engineers

Q2 2025: Development & Hiring
  - Cloud infrastructure operational
  - Data engineering foundation
  - Hire data scientists

Q3 2025: Analytics Platform
  - Deploy real-time pipeline
  - Implement BI tools
  - User training

Q4 2025: Production Launch
  - Full platform operational
  - Legacy system decommission
  - Performance optimization

---

Success Metrics:

Before:
  - Query time: 24 hours (batch)
  - Data freshness: 1 day old
  - Cost: $100K/month
  - User satisfaction: 2.5/5

After:
  - Query time: <1 second (real-time)
  - Data freshness: Real-time
  - Cost: $60K/month (40% reduction)
  - User satisfaction: 4.5/5

ROI: Break-even in 18 months
```

### 3. **Gap Closure Planning**

```javascript
// Create action plans to close gaps

class GapClosurePlanning {
  createClosurePlan(gap) {
    return {
      gap_id: gap.id,
      gap_description: gap.description,
      target_state: gap.target_state,

      approach: gap.gap_type === 'Maturity'
        ? this.createMaturityPlan(gap)
        : this.createCapabilityPlan(gap),

      timeline: {
        start_date: gap.start_date,
        target_completion: gap.target_date,
        duration_weeks: Math.ceil(gap.effort_estimate),
        milestones: this.defineMilestones(gap)
      },

      resources: {
        people: gap.required_staff,
        budget: gap.estimated_cost,
        tools: gap.required_tools
      },

      success_criteria: gap.success_metrics,

      risks: this.identifyClosureRisks(gap),

      dependencies: gap.dependencies
    };
  }

  createMaturityPlan(gap) {
    // Plan for improving existing capability
    return {
      strategy: 'Improve capability maturity',
      phases: [
        {
          phase: 'Assess Current',
          activities: ['Document current state', 'Identify improvement areas'],
          duration: '2 weeks'
        },
        {
          phase: 'Plan Improvements',
          activities: ['Define target maturity', 'Create roadmap', 'Allocate resources'],
          duration: '2 weeks'
        },
        {
          phase: 'Implement',
          activities: ['Execute improvement', 'Training', 'Process changes'],
          duration: gap.effort_estimate + ' weeks'
        },
        {
          phase: 'Validate',
          activities: ['Measure against targets', 'Validate maturity', 'Document learnings'],
          duration: '2 weeks'
        }
      ]
    };
  }

  createCapabilityPlan(gap) {
    // Plan for building new capability
    return {
      strategy: 'Build new capability',
      phases: [
        {
          phase: 'Design',
          activities: ['Define requirements', 'Design solution', 'Get approvals'],
          duration: '4 weeks'
        },
        {
          phase: 'Build',
          activities: ['Develop', 'Test', 'Integrate'],
          duration: gap.effort_estimate + ' weeks'
        },
        {
          phase: 'Deploy',
          activities: ['Pilot', 'Roll out', 'Support transition'],
          duration: '4 weeks'
        }
      ]
    };
  }

  defineMilestones(gap) {
    return [
      { name: 'Gap closure initiated', date_offset: 'Week 0' },
      { name: 'First deliverable', date_offset: `Week ${Math.ceil(gap.effort_estimate / 3)}` },
      { name: 'Mid-point review', date_offset: `Week ${Math.ceil(gap.effort_estimate / 2)}` },
      { name: 'Final validation', date_offset: `Week ${gap.effort_estimate}` }
    ];
  }
}
```

### 4. **Communication & Tracking**

```yaml
Gap Analysis Communication:

Stakeholder Updates:

Executive Summary (1 page):
  - What gaps exist?
  - Why do they matter?
  - What's the investment?
  - When will we close them?

Detailed Report (10 pages):
  - Gap identification methodology
  - Gap descriptions and impacts
  - Priority and sequencing
  - Detailed closure plans
  - Risk assessment

Team Briefing (30 min):
  - Overview of gaps
  - Impact on team
  - Their role in closure
  - Timeline and changes

---

Tracking Dashboard:

Gap 1: Cloud Infrastructure
  Status: In Progress (40%)
  Timeline: On track
  Budget: On budget ($200K allocated, $80K spent)
  Next Milestone: Infrastructure provisioning (due Feb 15)

Gap 2: Cloud Engineering Skills
  Status: Not started
  Timeline: At risk (delayed by hiring)
  Budget: On budget
  Next Milestone: 2nd engineer hire (due Feb 28)

Gap 3: Data Governance
  Status: Completed
  Timeline: Complete
  Budget: Under budget ($18K vs $20K)
  Business Impact: 30% improvement in data quality
```

## Best Practices

### ✅ DO
- Compare current to clearly defined future state
- Include all relevant capability areas
- Involve stakeholders in gap identification
- Prioritize by value and effort
- Create detailed closure plans
- Track progress to closure
- Document gap analysis findings
- Review and update analysis quarterly
- Link gaps to business strategy
- Communicate findings transparently

### ❌ DON'T
- Skip current state assessment
- Create vague future state
- Identify gaps without solutions
- Ignore implementation effort
- Plan all gaps in parallel
- Forget about dependencies
- Ignore resource constraints
- Hide difficult findings
- Plan for 100% effort allocation
- Forget about change management

## Gap Analysis Tips

- Involve people doing the work
- Be realistic about effort estimates
- Start with highest-value gaps
- Build dependencies and sequencing
- Monitor progress weekly
