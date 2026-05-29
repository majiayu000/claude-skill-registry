---
name: create-dev-task
description: Use to generate development task documents for the Dev agent. Creates specifications describing WHAT needs fixing based on validated issues and investigations.
version: 1.0.0
---
<!-- Powered by Prism Coreâ„¢ -->

# create-dev-task

Generate a development task document for the Dev agent to implement based on validated issue and investigation.

## When to Use

- After QA or Support has validated and investigated an issue
- When a bug needs to be assigned to the Dev agent
- Before sprint planning to prepare development specifications
- When creating fix specifications from customer-reported issues

## Quick Start

1. Gather investigation results (validation report, root cause, affected components)
2. Create dev task document with problem statement
3. Define fix requirements (functional and non-functional)
4. Add risk assessment and deployment considerations
5. Package handoff notes for Dev agent

## Purpose

Create a comprehensive development task that describes WHAT needs fixing and WHY, not HOW to code it. The Dev agent will use this specification to implement the actual fix.

## SEQUENTIAL Task Execution

### 1. Compile Investigation Results
```yaml
inputs:
  - Issue validation report with evidence
  - Root cause analysis findings
  - Affected components identified
  - Business impact assessment
  - QA test specification (if created)
```

### 2. Create Development Task Document

```yaml
dev_task_specification:
  ticket_id: "ISSUE-{number}"
  priority: "P0|P1|P2|P3"
  estimated_effort: "1-2 hours|2-4 hours|1 day|2-3 days"
  
  problem_statement: |
    When {user action}, the system {current behavior}
    instead of {expected behavior}, causing {impact}.
  
  investigation_summary:
    root_cause: "{Brief description of why it happens}"
    affected_areas:
      - "{Component/Service 1}"
      - "{Component/Service 2}"
    first_occurred: "{Date or version}"
    frequency: "{Always|Sometimes|Under specific conditions}"
```

### 3. Define Fix Requirements

```yaml
fix_requirements:
  functional_requirements:
    - System must {specific behavior}
    - Error handling for {edge case}
    - Maintain backward compatibility
    
  non_functional_requirements:
    - Performance: Response time < {threshold}
    - Security: Validate {input/authorization}
    - Reliability: Handle {failure scenario}
    
  constraints:
    - Minimal code changes preferred
    - No breaking changes to API
    - Must be deployable without downtime
    
  suggested_approach: |
    Based on investigation, consider:
    - {High-level approach 1}
    - {High-level approach 2}
    Note: Dev agent determines actual implementation
```

### 4. Development Task Package

```markdown
# Dev Task: Fix for Issue #{ticket}

## Issue Summary
**Customer Impact:** {severity and scope}
**Business Priority:** {P0|P1|P2|P3}
**First Reported:** {date}
**Frequency:** {occurrence rate}

## Problem Description

### What's Happening
{Detailed description of the issue from user perspective}

### Root Cause Analysis
**Investigation Result:** {what was found}
**Component:** {affected component/service}
**Introduced:** {when/which version if known}

### Evidence
- Screenshot: {reference to validation evidence}
- Error Logs: {key error messages}
- Stack Trace: {if available}
- Reproduction Rate: {percentage}

## Requirements for Fix

### Functional Requirements
1. {Requirement 1}
2. {Requirement 2}
3. {Requirement 3}

### Technical Constraints
- {Constraint 1}
- {Constraint 2}

### Suggested Investigation Areas
- Check: {file/component 1}
- Review: {logic/flow}
- Consider: {potential approach}

## Definition of Done
- [ ] Issue no longer reproduces with validation steps
- [ ] QA test passes (will be created separately)
- [ ] No performance regression
- [ ] Code reviewed and approved
- [ ] Deployment plan documented

## Testing Requirements
- QA team will create regression test
- Dev to ensure fix doesn't break existing tests
- Manual validation in staging required

## Deployment Considerations
- Risk Level: {Low|Medium|High}
- Rollback Strategy: {approach if issues}
- Monitoring: {what to watch}

## Handoff Notes
- Support validated issue via Playwright
- QA task created for test implementation
- Architecture team consulted if needed
```

### 5. Risk and Impact Assessment

```yaml
risk_assessment:
  fix_complexity:
    low: "Single line/simple logic change"
    medium: "Multiple files, moderate logic"
    high: "Architecture change, multiple services"
    
  regression_risk:
    low: "Isolated feature, good test coverage"
    medium: "Shared component, some dependencies"
    high: "Core functionality, many dependencies"
    
  deployment_risk:
    low: "Feature flag available, easy rollback"
    medium: "Standard deployment, monitoring needed"
    high: "Database changes, careful coordination"
```

### 6. Sprint Planning Information

```yaml
sprint_planning:
  story_points: {1|2|3|5|8}
  
  acceptance_criteria:
    - Customer issue resolved
    - QA test passes
    - No new issues introduced
    - Performance maintained
    
  dependencies:
    - QA test implementation
    - Environment access
    - External team approval (if needed)
    
  deliverables:
    - Code fix implemented
    - Tests passing
    - Documentation updated
    - Deployment plan ready
```

### 7. Communication Template

```markdown
## Dev Team Handoff

**Ticket:** #{ticket}
**Priority:** {priority}
**Assigned to:** Dev Agent

**Summary:** Customer experiencing {issue}. Support has validated and investigated. Need fix implementation.

**Key Files:** 
- Investigation report: {link}
- Validation evidence: {link}
- QA test spec: {link}

**Timeline:**
- Target Sprint: {sprint}
- Customer Commitment: {date if any}

**Questions:** Contact Support team via {channel}
```

## Success Criteria
- [ ] Complete dev task specification created
- [ ] Problem clearly described without prescribing solution
- [ ] Requirements defined without implementation details
- [ ] Risk assessment completed
- [ ] Handoff package ready for Dev agent

## Output
- Development task document
- Sprint planning metadata
- Risk assessment
- Clear requirements for Dev team
