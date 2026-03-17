---
name: sdlc-handoff
version: 1.0.0
description: Use for SDLC phase transitions. Ensures proper handoff between development phases with documentation.
---
<!-- Powered by Prism Core™ -->

# sdlc-handoff

Create complete handoff package for Dev and QA teams to handle customer issue through proper SDLC process.

## When to Use

- When customer issue is validated and ready for development
- When transitioning from Support to Dev/QA teams
- When creating SDLC workflow documentation for issues
- When coordinating cross-team handoffs

## Quick Start

1. Compile complete issue package (validation, investigation, impact)
2. Create SDLC workflow document with executive summary
3. Generate Dev story with technical requirements
4. Create QA testing checklist with acceptance criteria
5. Schedule collaboration sync if high priority

## Purpose

Coordinate the transition of validated customer issues from Support to Dev and QA teams, ensuring all necessary information is documented and tasks are properly assigned.

## SEQUENTIAL Task Execution

### 1. Compile Complete Issue Package
```yaml
issue_package:
  validation:
    - Playwright reproduction evidence
    - Screenshots and error logs
    - Console output and network traces
    - Reproduction steps documented
    
  investigation:
    - Root cause analysis
    - Affected components
    - Code areas identified
    - Risk assessment
    
  impact:
    - Number of customers affected
    - Business impact statement
    - Revenue/operational impact
    - Workaround availability
```

### 2. Create SDLC Workflow Document

```markdown
# SDLC Handoff: Issue #{ticket}

## Executive Summary
**Issue:** {one-line description}
**Priority:** {P0|P1|P2|P3}
**Customer Impact:** {High|Medium|Low}
**Target Resolution:** Sprint {number}

## Issue Lifecycle Status

### âœ… Completed by Support
- [x] Customer issue validated
- [x] Issue reproduced via Playwright
- [x] Root cause investigated
- [x] Impact assessed
- [x] Documentation created

### ðŸ“‹ Ready for SDLC Teams
- [ ] Dev: Fix implementation needed
- [ ] QA: Test creation needed
- [ ] Dev: Code review required
- [ ] QA: Test validation required
- [ ] DevOps: Deployment planning
- [ ] Support: Customer communication

## Detailed Issue Information

### Customer Report
- **Reporter:** {customer identifier}
- **Date:** {reported date}
- **Description:** {customer's description}
- **Business Impact:** {what's blocked}

### Validation Results
- **Reproduction Rate:** {100%|Intermittent}
- **Environment:** {browser/device/conditions}
- **Evidence:** [Link to screenshots/videos]
- **Playwright Script:** [Link to validation code]

### Investigation Findings
- **Root Cause:** {identified cause}
- **Affected Component:** {service/module}
- **Introduced:** {version/date if known}
- **Related Issues:** {linked tickets}
```

### 3. Task Assignment Matrix

```yaml
task_assignments:
  dev_team:
    task_id: "DEV-{ticket}"
    assignee: "Dev Agent"
    priority: "{priority}"
    deliverables:
      - Fix implementation
      - Code review
      - Unit tests updated
      - Documentation updated
    timeline: "{sprint}"
    
  qa_team:
    task_id: "QA-{ticket}"
    assignee: "QA Agent"
    priority: "{priority}"
    deliverables:
      - E2E regression test
      - Test documentation
      - Test validation post-fix
      - Coverage report
    timeline: "{sprint}"
    
  devops_team:
    task_id: "OPS-{ticket}"
    assignee: "DevOps"
    priority: "{priority}"
    deliverables:
      - Deployment plan
      - Rollback procedure
      - Monitoring setup
      - Post-deployment validation
    timeline: "{sprint+1}"
```

### 4. Communication Plan

```yaml
communication_matrix:
  internal:
    dev_standup:
      message: "New {priority} issue handed off from Support"
      action: "Review and estimate"
      
    qa_planning:
      message: "Test specification ready for {ticket}"
      action: "Include in sprint planning"
      
    management:
      message: "Customer issue {ticket} in SDLC pipeline"
      action: "Monitor progress"
      
  external:
    customer_update:
      message: "Issue validated and assigned to engineering"
      timeline: "Fix targeted for {date}"
      
    support_team:
      message: "Issue transitioned to Dev/QA"
      action: "Monitor for updates"
```

### 5. SDLC Checklist

```markdown
## SDLC Process Checklist

### Phase 1: Development (Dev Agent)
- [ ] Review handoff documentation
- [ ] Implement fix per requirements
- [ ] Update/create unit tests
- [ ] Submit for code review
- [ ] Address review feedback

### Phase 2: Testing (QA Agent)
- [ ] Create E2E test from specification
- [ ] Verify test fails with current code
- [ ] Validate fix resolves issue
- [ ] Run regression suite
- [ ] Update test documentation

### Phase 3: Review & Approval
- [ ] Code review completed
- [ ] QA sign-off obtained
- [ ] Performance validated
- [ ] Security review (if needed)
- [ ] Documentation updated

### Phase 4: Deployment
- [ ] Deployment plan created
- [ ] Staging validation
- [ ] Production deployment
- [ ] Post-deployment verification
- [ ] Customer notification

### Phase 5: Closure
- [ ] Customer confirms resolution
- [ ] Lessons learned documented
- [ ] Knowledge base updated
- [ ] Ticket closed
```

### 6. Tracking Dashboard

```yaml
tracking_metrics:
  sla_tracking:
    p0_resolution: "4 hours"
    p1_resolution: "24 hours"
    p2_resolution: "3 days"
    p3_resolution: "Next sprint"
    
  status_indicators:
    green: "On track"
    yellow: "At risk"
    red: "Blocked/Delayed"
    
  milestone_tracking:
    - validation_complete: "{timestamp}"
    - dev_started: "pending"
    - qa_started: "pending"
    - fix_completed: "pending"
    - deployed_prod: "pending"
    - customer_verified: "pending"
```

### 7. Escalation Triggers

```yaml
escalation_rules:
  auto_escalate_if:
    - "P0 not resolved in 2 hours"
    - "P1 not assigned in 4 hours"
    - "Customer executive complaint"
    - "Multiple customers affected"
    - "Revenue impact > $10k"
    
  escalation_path:
    level_1: "Team Lead"
    level_2: "Engineering Manager"
    level_3: "Director/VP"
    level_4: "C-Level"
```

## Success Criteria
- [ ] Complete handoff package created
- [ ] Dev task assigned and acknowledged
- [ ] QA task assigned and acknowledged
- [ ] Timeline agreed and communicated
- [ ] Customer updated on status

## Output
- SDLC workflow document
- Task assignments for Dev and QA
- Communication plan executed
- Tracking metrics established
- Escalation rules defined
