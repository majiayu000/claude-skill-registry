---
name: process-mapping
description: Visualize and document current and future business processes. Identify inefficiencies, dependencies, and improvement opportunities through detailed process mapping and analysis.
---

# Process Mapping

## Overview

Process mapping creates visual representations of workflows, helping teams understand current operations, identify bottlenecks, and design improvements.

## When to Use

- Documenting existing workflows
- Identifying process improvements
- Onboarding new team members
- Discovering inefficiencies and bottlenecks
- Planning system implementations
- Analyzing customer journeys
- Automating manual processes
- Training and documentation

## Instructions

### 1. **Process Mapping Techniques**

```yaml
Mapping Approaches:

Current State (AS-IS):
  Purpose: Understand existing process
  Participants: People doing the work
  Timeline: 2-4 hours
  Output: Current workflow diagram
  Benefits: Identifies real bottlenecks

Future State (TO-BE):
  Purpose: Design improved process
  Participants: Cross-functional team
  Timeline: 4-8 hours
  Output: Improved workflow design
  Benefits: Clear vision for change

Value Stream Mapping:
  Purpose: Focus on value-added vs waste
  Participants: Process owners, operations
  Timeline: Full day
  Output: Detailed flow with timing
  Benefits: Identifies waste and delays

Swimlane Diagram:
  Purpose: Show roles and responsibilities
  Participants: All roles involved
  Timeline: 2-3 hours
  Output: Role-based process flow
  Benefits: Clear accountability

---

## Mapping Symbols:

Start/End: Oval
Process: Rectangle
Decision: Diamond
Document: Document shape
Data: Database cylinder
Delay: Hourglass
Off-page: Arrow
Connector: Lines with arrows
```

### 2. **Process Documentation**

```python
# Document process steps and details

class ProcessDocumentation:
    def create_process_map(self, process_name, steps):
        """Document complete process"""
        return {
            'process_name': process_name,
            'owner': '',
            'last_updated': '',
            'version': '1.0',
            'steps': self.document_steps(steps),
            'metrics': self.define_metrics(process_name),
            'risks': self.identify_risks(steps),
            'improvements': []
        }

    def document_steps(self, steps):
        """Detail each process step"""
        documented = []

        for i, step in enumerate(steps, 1):
            documented.append({
                'step_number': i,
                'action': step.name,
                'actor': step.responsible_party,
                'input': step.inputs,
                'output': step.outputs,
                'decision': step.decision_point or None,
                'duration': step.estimated_time,
                'system': step.system_involved,
                'exceptions': step.error_cases,
                'documents': step.documents_used
            })

        return documented

    def identify_bottlenecks(self, process_map):
        """Find inefficiencies"""
        bottlenecks = []

        for step in process_map['steps']:
            # Long duration steps
            if step['duration'] > 2:  # hours
                bottlenecks.append({
                    'step': step['step_number'],
                    'issue': 'Long duration',
                    'duration': step['duration'],
                    'impact': 'Delays overall process',
                    'improvement_opportunity': 'Parallelization or automation'
                })

            # Manual data entry
            if 'manual' in step['action'].lower():
                bottlenecks.append({
                    'step': step['step_number'],
                    'issue': 'Manual task',
                    'impact': 'Slow and error-prone',
                    'improvement_opportunity': 'Automation'
                })

        return bottlenecks

    def calculate_total_time(self, process_map):
        """Calculate end-to-end duration"""
        sequential_time = sum(s['duration'] for s in process_map['steps'])
        parallel_time = max(s['duration'] for s in process_map['steps'])

        return {
            'current_sequential': sequential_time,
            'if_parallelized': parallel_time,
            'potential_improvement': f"{(1 - parallel_time/sequential_time)*100:.0f}%"
        }
```

### 3. **Current State Analysis**

```yaml
Process Map: Customer Onboarding

Current State (AS-IS):

Step 1: Application Submission
  Time: 15 minutes
  Actor: Customer
  System: Web portal
  Output: Application data

Step 2: Admin Review (BOTTLENECK)
  Time: 2 days
  Actor: Onboarding specialist
  System: Email + spreadsheet
  Notes: Manual verification, no automation
  Output: Approved/rejected decision

Step 3: Document Verification
  Time: 4 hours
  Actor: Compliance officer
  System: PDF review
  Output: Verified documents

Step 4: Account Setup
  Time: 30 minutes
  Actor: System (automated)
  System: Automation script
  Output: User account created

Step 5: Welcome Communication (MANUAL)
  Time: 1 hour
  Actor: Support team
  System: Email template
  Notes: Manual personalization
  Output: Welcome email sent

Step 6: First Login Onboarding
  Time: 15 minutes
  Actor: Customer
  System: Web app
  Output: Initial data entry

---

Current State Metrics:
  Total Time: 2.5 days
  Manual Steps: 4 (67%)
  Automated Steps: 1 (17%)
  Error Rate: 8% (manual review errors)
  Cost per Onboarding: $150

---

Bottleneck Analysis:

#1 Admin Review (2 days - 80% of total time)
  Cause: Manual spreadsheet-based review
  Impact: Customer waits for access
  Solution: Implement workflow automation

#2 Manual Welcome Email (1 hour of specialist time)
  Cause: Manual personalization
  Impact: Support team overloaded
  Solution: Template-based automation

#3 Manual Document Verification
  Cause: PDF manual review
  Impact: Compliance risk, slowness
  Solution: OCR + automated validation
```

### 4. **Future State Design**

```javascript
// Design improved process

class FutureStateDesign {
  designImprovedProcess(currentState) {
    return {
      target_state: 'TO-BE',
      goals: [
        'Reduce total time from 2.5 days to 4 hours',
        'Eliminate manual review steps',
        'Reduce error rate to <1%',
        'Reduce cost per onboarding to $30'
      ],
      improvements: [
        {
          step: 'Admin Review',
          current_time: '2 days',
          future_time: '5 minutes',
          approach: 'Automated verification rules',
          technology: 'Business rules engine'
        },
        {
          step: 'Document Verification',
          current_time: '4 hours',
          future_time: '1 minute',
          approach: 'OCR + AI validation',
          technology: 'ML-based document processing'
        },
        {
          step: 'Welcome Communication',
          current_time: '1 hour manual',
          future_time: '2 minutes automated',
          approach: 'Automated email workflow',
          technology: 'Email automation + CRM'
        }
      ],
      new_total_time: '4 hours',
      new_cost_per_onboarding: '$30',
      automation_percentage: '95%',
      implementation_timeline: '8 weeks',
      required_systems: [
        'Workflow automation platform',
        'Document processing API',
        'CRM integration'
      ]
    };
  }

  createImplementationPlan(futureState) {
    return {
      phase_1: {
        duration: '2 weeks',
        focus: 'Admin review automation',
        tasks: [
          'Define approval rules',
          'Build workflow engine',
          'Test with sample data'
        ]
      },
      phase_2: {
        duration: '3 weeks',
        focus: 'Document verification',
        tasks: [
          'Integrate OCR service',
          'Build validation rules',
          'Manual QA',
          'Compliance review'
        ]
      },
      phase_3: {
        duration: '3 weeks',
        focus: 'Email automation',
        tasks: [
          'Configure email templates',
          'Workflow triggers',
          'User testing'
        ]
      }
    };
  }
}
```

### 5. **Process Improvement Metrics**

```yaml
Key Process Metrics:

Cycle Time (End-to-End Duration):
  Before: 2.5 days (onboarding)
  After: 4 hours
  Improvement: 93% reduction

Process Cost:
  Before: $150 per customer
  After: $30 per customer
  Savings: $120 per customer, $600K annually (5K customers)

Quality Metrics:
  Error Rate Before: 8%
  Error Rate After: <1%
  Rework Reduction: 90%

Efficiency:
  Manual Steps Before: 4
  Automated Steps After: 5
  Manual %: 67% → 5%

Customer Satisfaction:
  Speed Improvement: 2.5 days → 4 hours
  First-time success: 92% → 99%

---

Monitoring Dashboard:

Daily Metrics:
  - Customers onboarded: 15
  - Avg time: 3.8 hours
  - Error rate: 0.7%
  - Cost per customer: $28

Weekly Metrics:
  - Total onboarded: 105
  - On-time percentage: 98%
  - Escalations: 2
  - Manual interventions: 1

Monthly Trends:
  - Continuous improvement: 2% faster each month
  - Error rate trending: Down 10% monthly
  - Cost trending: Down 3% monthly
```

## Best Practices

### ✅ DO
- Map current state first before designing changes
- Include all stakeholders in mapping sessions
- Document actual processes, not theoretical ones
- Identify waste and bottlenecks
- Design future state with team input
- Include decision points and exceptions
- Add timing and resource information
- Keep processes simple and visual
- Update maps when processes change
- Use mapping to drive continuous improvement

### ❌ DON'T
- Skip documenting current state
- Design future state without understanding current
- Over-complicate process diagrams
- Forget about edge cases and exceptions
- Ignore process performance metrics
- Create maps that nobody can understand
- Design improvements without involving people doing work
- Implement changes without validating process
- Leave outdated maps in documentation
- Ignore customer perspective

## Process Mapping Tips

- Use standard symbols for consistency
- Limit diagrams to one page when possible
- Include timing information
- Show decision points clearly
- Involve people doing the work, not just managers
- Measure before and after improvement
