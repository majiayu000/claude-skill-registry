---
name: prp-wizard
version: 1.0.0
description: PRP Framework wizard for PRD-driven development. Gathers requirements, generates PRD, creates implementation plan, and executes with validation loops. Part of the unified project wizard. Use when user wants PRD-driven development, selects PRP framework in project wizard, or starts feature development or enhancement projects.
---

# PRP Wizard: PRD-Driven Development Framework

Interactive wizard for implementing features using the Product Requirements Planning (PRP) framework. This skill handles the complete lifecycle from requirements gathering through validated implementation.

## Triggers

Use this skill when:
- User selected PRP framework in project wizard
- User wants PRD-driven development
- Feature development or enhancement projects
- Creating comprehensive technical specifications
- Planning multi-phase implementations
- Building features with formal validation requirements
- Keywords: PRP wizard, PRD development, feature planning, implementation plan, requirements driven, PRP framework, product requirements, technical specification

## Core Mission

Guide users through the complete PRP workflow:

1. **Requirements Gathering**: Structured questionnaire to capture all requirements
2. **Complexity Assessment**: Determine effort level and approach
3. **PRD Generation**: Create comprehensive Product Requirements Document
4. **Implementation Planning**: Break down into phases and tasks
5. **Archon Integration**: Create trackable tasks for execution
6. **Validated Execution**: Implement with validation loops

---

## PRP Workflow Overview

```
PRP WIZARD FLOW

  +-------------+     +-------------+     +-------------+     +-------------+
  |  Feature    |---->|  Complexity |---->|    PRD      |---->|Implementation|
  | Definition  |     | Assessment  |     | Generation  |     |   Planning   |
  +-------------+     +-------------+     +-------------+     +-------------+
                                                                     |
        +------------------------------------------------------------+
        |
        v
  +-------------+     +-------------+     +-------------+     +-------------+
  |   Archon    |---->|  Validated  |---->|   Review &  |---->|   Feature   |
  |   Tasks     |     | Execution   |     |  Validation |     |  Complete   |
  +-------------+     +-------------+     +-------------+     +-------------+
```

---

## Phase 1: Feature Definition

Gather comprehensive information about the feature being built.

### Feature Definition Questions

```markdown
## PRP Wizard - Phase 1: Feature Definition

**1. Feature Name**
   What is the feature called? (Clear, descriptive name)
   > Example: "User Authentication System", "Dashboard Analytics Module"

**2. Feature Description**
   Detailed description of what this feature does and why it's needed.
   Include:
   - What problem does it solve?
   - What value does it provide?
   - Who benefits from this feature?

**3. User Stories**
   Who are the primary users and what do they want to accomplish?

   **Primary User**:
   - Role: [Job title or persona name]
   - Goal: [What they want to achieve]
   - Scenario: "As a [role], I want to [action] so that [benefit]"

   **Secondary User(s)** (if applicable):
   - Role: [Job title or persona name]
   - Goal: [What they want to achieve]
   - Scenario: "As a [role], I want to [action] so that [benefit]"

**4. Success Criteria**
   How will we know when this feature is complete and successful?

   - [ ] Criterion 1: [Measurable outcome]
   - [ ] Criterion 2: [Measurable outcome]
   - [ ] Criterion 3: [Measurable outcome]

**5. Acceptance Criteria (Technical)**
   What technical requirements must be met?

   - [ ] Given [context], when [action], then [outcome]
   - [ ] Given [context], when [action], then [outcome]
   - [ ] Given [context], when [action], then [outcome]
```

### Feature Context Questions

```markdown
## Feature Context

**6. Existing Codebase Integration**
   - Is this feature for an existing project? [Yes/No]
   - If yes, what is the tech stack?
   - What existing components will this feature interact with?
   - Are there existing patterns to follow?

**7. Related Features**
   - What existing features does this relate to?
   - Are there dependencies on other features?
   - Will this feature enable future features?

**8. Constraints**
   - Timeline constraints?
   - Budget constraints?
   - Technical constraints (browser support, performance, etc.)?
   - Compliance constraints (GDPR, HIPAA, accessibility)?
```

---

## Phase 2: Complexity Assessment

Determine the appropriate approach based on feature complexity.

### Complexity Matrix

| Estimated Effort | Description | Approach |
|-----------------|-------------|----------|
| **Low** (< 1 day) | Simple feature, clear requirements | Direct Implementation |
| **Medium** (1-5 days) | Moderate complexity, some unknowns | Plan -> Implement |
| **High** (1-2 weeks) | Complex feature, multiple components | PRD -> Plan -> Implement |
| **Very High** (2+ weeks) | Large feature, many phases | PRD with Multiple Phases |

### Complexity Assessment Questions

```markdown
## PRP Wizard - Phase 2: Complexity Assessment

**9. Estimated Effort**
   How long do you expect this feature to take?
   - [ ] Low (< 1 day): Simple, straightforward implementation
   - [ ] Medium (1-5 days): Some complexity, needs planning
   - [ ] High (1-2 weeks): Complex, multiple components
   - [ ] Very High (2+ weeks): Large scope, phased rollout

**10. Technical Complexity Factors**
    Select all that apply:
    - [ ] New technology or framework needed
    - [ ] Complex data models or relationships
    - [ ] Third-party API integrations
    - [ ] Real-time or streaming requirements
    - [ ] High performance requirements
    - [ ] Complex UI/UX interactions
    - [ ] Security-sensitive functionality
    - [ ] Database migrations required
    - [ ] Breaking changes to existing APIs

**11. Dependencies**
    External dependencies:
    - [ ] External APIs/services: [List]
    - [ ] Third-party libraries: [List]
    - [ ] Infrastructure changes: [List]

    Internal dependencies:
    - [ ] Database changes: [Describe]
    - [ ] Other features: [List features]
    - [ ] Team dependencies: [Other teams/people]

**12. Risk Factors**
    Identify potential risks:
    - [ ] Technical unknowns (need research/spikes)
    - [ ] Integration complexity
    - [ ] Performance risks
    - [ ] Security considerations
    - [ ] Data migration risks
    - [ ] User adoption risks
    - [ ] Rollback complexity
```

### Complexity Scoring

Calculate complexity score based on responses:

```python
# Complexity scoring logic
complexity_score = 0

# Effort level
effort_scores = {"low": 1, "medium": 3, "high": 5, "very_high": 8}
complexity_score += effort_scores[effort_level]

# Technical factors (1 point each)
complexity_score += len(technical_factors)

# Dependencies (2 points each external, 1 each internal)
complexity_score += len(external_dependencies) * 2
complexity_score += len(internal_dependencies)

# Risk factors (1.5 points each)
complexity_score += len(risk_factors) * 1.5

# Determine approach
if complexity_score < 5:
    approach = "direct_implementation"
elif complexity_score < 10:
    approach = "plan_then_implement"
elif complexity_score < 18:
    approach = "prd_with_plan"
else:
    approach = "prd_multi_phase"
```

---

## Phase 3: PRD Generation

Generate a comprehensive Product Requirements Document based on gathered information.

### PRD Structure

```markdown
# PRD: [Feature Name]

## Document Information

| Field | Value |
|-------|-------|
| **Feature** | [Feature Name] |
| **Owner** | [From project config or user input] |
| **Status** | Draft |
| **Created** | [Current date] |
| **Version** | 1.0 |
| **Complexity** | [Low/Medium/High/Very High] |
| **Estimated Effort** | [Duration] |

---

## Executive Summary

[2-3 paragraph overview of the feature, its purpose, and expected impact]

---

## Problem Statement

### Current State
[Description of the current situation and existing pain points]

### Desired State
[Description of the ideal end state after feature implementation]

### Impact of Not Solving
[What happens if we don't build this feature?]

---

## Goals & Objectives

### Primary Goal
[The main outcome we're trying to achieve]

### Secondary Goals
- [Secondary goal 1]
- [Secondary goal 2]

### Success Metrics
| Metric | Current | Target | Measurement Method |
|--------|---------|--------|-------------------|
| [Metric 1] | [Baseline] | [Target] | [How measured] |
| [Metric 2] | [Baseline] | [Target] | [How measured] |

---

## User Stories

### Epic: [Feature Name]

#### US-001: [Primary User Story]
**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]
- [ ] Given [context], when [action], then [outcome]

**Priority:** P1
**Estimate:** [Size]

#### US-002: [Secondary User Story]
[Same format as above]

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR-001 | System MUST [capability] | P1 (Must Have) | [Notes] |
| FR-002 | System MUST [capability] | P1 (Must Have) | [Notes] |
| FR-003 | System SHOULD [capability] | P2 (Should Have) | [Notes] |
| FR-004 | System MAY [capability] | P3 (Nice to Have) | [Notes] |

---

## Non-Functional Requirements

| ID | Category | Requirement | Target | Notes |
|----|----------|-------------|--------|-------|
| NFR-001 | Performance | [Requirement] | [Target value] | [Notes] |
| NFR-002 | Scalability | [Requirement] | [Target value] | [Notes] |
| NFR-003 | Security | [Requirement] | [Standard] | [Notes] |
| NFR-004 | Accessibility | [Requirement] | [WCAG level] | [Notes] |
| NFR-005 | Availability | [Requirement] | [SLA %] | [Notes] |

---

## Technical Considerations

### Architecture Impact
[How does this feature affect existing architecture?]

### Technology Stack
- **Frontend**: [Technologies]
- **Backend**: [Technologies]
- **Database**: [Technologies]
- **Infrastructure**: [Technologies]

### Data Model
```
[Entity definitions, schema changes, or diagram description]
```

### API Design
```
[Endpoint definitions, request/response formats]
```

### Dependencies
| Dependency | Type | Status | Risk Level |
|------------|------|--------|------------|
| [Dependency 1] | External | [Status] | [Low/Medium/High] |
| [Dependency 2] | Internal | [Status] | [Low/Medium/High] |

---

## Implementation Phases

[Generated based on complexity assessment - see Phase 4 section]

---

## Testing Strategy

### Unit Tests
- [ ] [Test category 1]
- [ ] [Test category 2]

### Integration Tests
- [ ] [Integration scenario 1]
- [ ] [Integration scenario 2]

### End-to-End Tests
- [ ] [User flow 1]
- [ ] [User flow 2]

### Performance Tests
- [ ] [Performance scenario 1]

### Security Tests
- [ ] [Security test 1]

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation Strategy | Owner |
|------|-------------|--------|---------------------|-------|
| [Risk 1] | [Low/Med/High] | [Low/Med/High] | [Strategy] | [Owner] |
| [Risk 2] | [Low/Med/High] | [Low/Med/High] | [Strategy] | [Owner] |

---

## Out of Scope

Explicitly excluded from this feature:
- [Excluded item 1]
- [Excluded item 2]
- [Excluded item 3]

---

## Open Questions

- [ ] [Question 1 that needs resolution]
- [ ] [Question 2 that needs resolution]

---

## Timeline

| Milestone | Target Date | Status | Owner |
|-----------|-------------|--------|-------|
| PRD Approved | [Date] | [Status] | [Owner] |
| Phase 1 Complete | [Date] | [Status] | [Owner] |
| Phase 2 Complete | [Date] | [Status] | [Owner] |
| Testing Complete | [Date] | [Status] | [Owner] |
| Release | [Date] | [Status] | [Owner] |

---

## Appendix

### Related Documents
- [Link to design mockups]
- [Link to API specification]
- [Link to architecture docs]

### Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | [Date] | [Author] | Initial draft |
```

---

## Phase 4: Implementation Planning

Break down the PRD into actionable phases and tasks.

### Phase Structure by Complexity

#### Low Complexity (Direct Implementation)

```markdown
## Implementation Plan: Direct Implementation

### Phase 1: Implementation (< 1 day)
**Duration**: [Hours]

**Tasks**:
1. [ ] Set up feature structure
2. [ ] Implement core functionality
3. [ ] Write tests
4. [ ] Update documentation
5. [ ] Submit for review

**Validation**:
- [ ] All tests passing
- [ ] Code review approved
```

#### Medium Complexity (Plan -> Implement)

```markdown
## Implementation Plan: Plan Then Implement

### Phase 1: Planning & Setup (0.5-1 day)
**Duration**: [Hours/Days]

**Tasks**:
1. [ ] Review existing codebase
2. [ ] Design component structure
3. [ ] Define interfaces/contracts
4. [ ] Set up feature branch
5. [ ] Create test scaffolding

### Phase 2: Core Implementation (1-3 days)
**Duration**: [Days]

**Tasks**:
1. [ ] Implement data models
2. [ ] Build core business logic
3. [ ] Create API endpoints
4. [ ] Build UI components
5. [ ] Write unit tests

### Phase 3: Integration & Testing (0.5-1 day)
**Duration**: [Hours/Days]

**Tasks**:
1. [ ] Integration testing
2. [ ] End-to-end testing
3. [ ] Performance validation
4. [ ] Documentation
5. [ ] Code review

**Validation Checkpoints**:
- [ ] After Phase 1: Design review
- [ ] After Phase 2: Feature functionality verified
- [ ] After Phase 3: All tests passing, ready for merge
```

#### High Complexity (PRD -> Plan -> Implement)

```markdown
## Implementation Plan: PRD-Driven Implementation

### Phase 1: Foundation (2-3 days)
**Duration**: [Days]
**Focus**: Data models, basic structure, infrastructure

**Tasks**:
1. [ ] Database schema design and migrations
2. [ ] Core data models and types
3. [ ] Base service/repository patterns
4. [ ] Initial API contracts
5. [ ] Feature flag setup
6. [ ] Base test infrastructure

**Validation**:
- [ ] Schema migrations successful
- [ ] Base models compile/type-check
- [ ] API contracts documented

### Phase 2: Core Functionality (3-5 days)
**Duration**: [Days]
**Focus**: Business logic, primary features

**Tasks**:
1. [ ] Core business logic implementation
2. [ ] Primary API endpoints
3. [ ] Service layer implementation
4. [ ] Error handling and validation
5. [ ] Unit tests for core logic

**Validation**:
- [ ] Unit tests > 80% coverage
- [ ] API endpoints functional
- [ ] Business logic verified

### Phase 3: User Interface (2-4 days)
**Duration**: [Days]
**Focus**: UI components, user interactions

**Tasks**:
1. [ ] Component architecture
2. [ ] UI component implementation
3. [ ] State management
4. [ ] Form handling and validation
5. [ ] Accessibility implementation

**Validation**:
- [ ] Components render correctly
- [ ] User flows functional
- [ ] Accessibility audit passed

### Phase 4: Integration (1-2 days)
**Duration**: [Days]
**Focus**: Connect all pieces, external integrations

**Tasks**:
1. [ ] Frontend-backend integration
2. [ ] External API integrations
3. [ ] End-to-end user flows
4. [ ] Error boundary implementation
5. [ ] Loading/error states

**Validation**:
- [ ] Integration tests passing
- [ ] External APIs connected
- [ ] Error handling verified

### Phase 5: Polish & Optimization (1-2 days)
**Duration**: [Days]
**Focus**: Performance, UX polish, documentation

**Tasks**:
1. [ ] Performance optimization
2. [ ] UX polish and refinements
3. [ ] Security hardening
4. [ ] Documentation updates
5. [ ] Final code review

**Validation**:
- [ ] Performance targets met
- [ ] Security review passed
- [ ] Documentation complete
```

#### Very High Complexity (PRD with Multiple Phases)

```markdown
## Implementation Plan: Multi-Phase PRD Implementation

### Epic 1: Foundation & Infrastructure (Week 1-2)

#### Phase 1.1: Architecture Setup
**Tasks**:
- [ ] System architecture design
- [ ] Database design
- [ ] API design
- [ ] Infrastructure setup

#### Phase 1.2: Core Data Layer
**Tasks**:
- [ ] Database migrations
- [ ] Data models
- [ ] Repository patterns
- [ ] Data validation

**Milestone Validation**:
- [ ] Architecture review completed
- [ ] Data layer functional
- [ ] Documentation updated

### Epic 2: Core Features (Week 3-4)

#### Phase 2.1: Backend Implementation
**Tasks**:
- [ ] Business logic services
- [ ] API endpoints
- [ ] Authentication/authorization
- [ ] Error handling

#### Phase 2.2: Frontend Implementation
**Tasks**:
- [ ] Component library setup
- [ ] Core UI components
- [ ] State management
- [ ] API integration

**Milestone Validation**:
- [ ] Core features functional
- [ ] Unit tests passing
- [ ] Integration tests passing

### Epic 3: Advanced Features (Week 5)

#### Phase 3.1: Secondary Features
**Tasks**:
- [ ] [Feature-specific tasks]

#### Phase 3.2: Integrations
**Tasks**:
- [ ] Third-party integrations
- [ ] Webhook implementations

**Milestone Validation**:
- [ ] All features complete
- [ ] Integration tests passing

### Epic 4: Hardening & Release (Week 6)

#### Phase 4.1: Testing & QA
**Tasks**:
- [ ] E2E test suite
- [ ] Performance testing
- [ ] Security audit
- [ ] Accessibility audit

#### Phase 4.2: Documentation & Release
**Tasks**:
- [ ] User documentation
- [ ] API documentation
- [ ] Release notes
- [ ] Deployment

**Milestone Validation**:
- [ ] All tests passing
- [ ] Security audit passed
- [ ] Documentation complete
- [ ] Stakeholder sign-off
```

---

## Phase 5: Validation Requirements

Define validation requirements for each phase of implementation.

### Validation Types

```markdown
## Validation Framework

### 1. Build Validation
Commands to verify the project builds successfully:
- [ ] `npm run build` / `python -m build` / `dotnet build`
- [ ] No compilation errors
- [ ] No TypeScript/type errors
- [ ] No linting errors

### 2. Test Validation
Test commands and coverage requirements:
- [ ] Unit tests: `npm test` / `pytest` / `dotnet test`
- [ ] Coverage threshold: [X]% minimum
- [ ] Integration tests: [command]
- [ ] E2E tests: [command]

### 3. Lint Validation
Code quality checks:
- [ ] ESLint/Ruff/StyleCop passing
- [ ] Prettier/Black formatting
- [ ] No security vulnerabilities in dependencies

### 4. Integration Validation
API and service checks:
- [ ] Health endpoints responding
- [ ] Database connections working
- [ ] External APIs accessible
- [ ] Authentication flow functional

### 5. Manual Validation
Human verification steps:
- [ ] UI matches designs
- [ ] User flow works as expected
- [ ] Edge cases handled
- [ ] Accessibility testing
```

### Validation Checkpoints

```python
# Validation checkpoint structure
validation_checkpoint = {
    "phase": "Phase 2: Core Implementation",
    "task_count": 5,
    "required_validations": [
        {
            "type": "build",
            "command": "npm run build",
            "expected": "exit_code_0"
        },
        {
            "type": "test",
            "command": "npm test -- --coverage",
            "expected": "coverage >= 80%"
        },
        {
            "type": "lint",
            "command": "npm run lint",
            "expected": "no_errors"
        }
    ],
    "manual_validations": [
        "Code review by team member",
        "Feature demo to stakeholder"
    ],
    "blocking": True  # Must pass before moving to next phase
}
```

---

## Phase 6: Documentation Requirements

Define documentation to be created alongside implementation.

### Documentation Types

```markdown
## Documentation Framework

### 1. Code Documentation
- [ ] Inline comments for complex logic
- [ ] JSDoc/docstrings for public APIs
- [ ] README for new directories/modules
- [ ] Type definitions documented

### 2. API Documentation
- [ ] OpenAPI/Swagger specification
- [ ] Request/response examples
- [ ] Authentication documentation
- [ ] Error code reference

### 3. User Documentation
- [ ] Feature overview
- [ ] Getting started guide
- [ ] Configuration options
- [ ] FAQ section

### 4. Architecture Documentation
- [ ] Design decisions (ADR format)
- [ ] Component diagrams
- [ ] Data flow diagrams
- [ ] Integration points

### 5. Operations Documentation
- [ ] Deployment guide
- [ ] Monitoring/alerting setup
- [ ] Troubleshooting guide
- [ ] Rollback procedures
```

---

## Archon Integration

Create Archon tasks from the PRD and implementation plan.

### PRD Storage

```python
# Store PRD as Archon document
manage_document("create",
    project_id=PROJECT_ID,
    title=f"PRD: {feature_name}",
    document_type="prp",
    content={
        "version": "1.0",
        "status": "draft",
        "feature_name": feature_name,
        "complexity": complexity_level,
        "sections": {
            "executive_summary": executive_summary,
            "problem_statement": problem_statement,
            "goals": goals,
            "user_stories": user_stories,
            "functional_requirements": functional_requirements,
            "non_functional_requirements": nfr,
            "technical_design": technical_design,
            "implementation_phases": phases,
            "testing_strategy": testing_strategy,
            "risks": risks,
            "timeline": timeline
        },
        "created_at": timestamp,
        "updated_at": timestamp
    },
    tags=["prd", "prp", feature_name.lower().replace(" ", "-")]
)
```

### Task Generation

```python
# Generate tasks from implementation phases
for phase_index, phase in enumerate(implementation_phases):
    # Create phase parent task
    phase_task = manage_task("create",
        project_id=PROJECT_ID,
        title=f"[{feature_name}] Phase {phase_index + 1}: {phase['name']}",
        description=f"""
## Phase Overview
{phase['description']}

## Duration
{phase['duration']}

## Focus Areas
{phase['focus']}

## Success Criteria
{format_criteria(phase['validation'])}

## Related PRD
See document: PRD: {feature_name}
""",
        status="todo",
        task_order=100 - (phase_index * 10),
        feature=feature_name
    )

    # Create individual tasks within phase
    for task_index, task in enumerate(phase['tasks']):
        manage_task("create",
            project_id=PROJECT_ID,
            title=f"[{feature_name}] {task['title']}",
            description=f"""
## Task Description
{task['description']}

## Acceptance Criteria
{format_acceptance_criteria(task['criteria'])}

## Validation
- Build: {task.get('build_validation', 'N/A')}
- Test: {task.get('test_validation', 'N/A')}
- Manual: {task.get('manual_validation', 'N/A')}

## Parent Phase
Phase {phase_index + 1}: {phase['name']}
""",
            status="todo",
            task_order=100 - (phase_index * 10) - (task_index + 1),
            feature=f"{feature_name}:Phase{phase_index + 1}"
        )
```

### Task Status Flow

```
Task Status Flow:
  todo -> doing -> review -> done

When moving to next phase:
  1. All tasks in current phase must be "done"
  2. All validation checkpoints must pass
  3. Update phase task status
  4. Begin next phase tasks
```

---

## Execution Workflow

Step-by-step execution with validation loops.

### Execution Steps

```markdown
## Execution Protocol

### Step 1: Load Context
1. Read PRD from Archon documents
2. Load implementation plan
3. Identify current phase and task
4. Check validation checkpoint status

### Step 2: Execute Task
1. Mark task as "doing"
2. Implement according to task description
3. Follow acceptance criteria
4. Run validation commands

### Step 3: Validate
1. Run build validation
2. Run test validation
3. Run lint validation
4. Perform manual checks if required

### Step 4: Report
1. Update task status based on validation
2. If PASS: Mark task "review" or "done"
3. If FAIL: Document failure, keep task "doing"
4. Update Archon with progress notes

### Step 5: Next Task
1. Check if phase complete
2. If phase complete, run phase validation
3. If phase validation passes, start next phase
4. If all phases complete, feature is done
```

### Validation Loop

```python
def execute_with_validation(task_id):
    """Execute task with validation loop."""

    # 1. Get task details
    task = find_tasks(task_id=task_id)
    manage_task("update", task_id=task_id, status="doing")

    # 2. Execute implementation
    implement_task(task)

    # 3. Run validation
    validation_results = {
        "build": run_build_validation(),
        "test": run_test_validation(),
        "lint": run_lint_validation()
    }

    # 4. Check results
    all_passed = all(v["passed"] for v in validation_results.values())

    if all_passed:
        # Move to review/done
        manage_task("update",
            task_id=task_id,
            status="done" if task["is_auto_mergeable"] else "review",
            description=f"{task['description']}\n\n## Validation Results\n{format_results(validation_results)}"
        )
        return True
    else:
        # Keep as doing, add failure notes
        manage_task("update",
            task_id=task_id,
            description=f"{task['description']}\n\n## Validation Failed\n{format_failures(validation_results)}"
        )
        return False
```

### Implementation Report

```markdown
## Implementation Report: [Feature Name]

### Summary
- **Feature**: [Name]
- **Status**: [In Progress / Complete / Blocked]
- **Current Phase**: [Phase Name]
- **Completion**: [X]% ([Y] of [Z] tasks)

### Progress by Phase

| Phase | Tasks | Complete | Status |
|-------|-------|----------|--------|
| Phase 1: Foundation | 5 | 5 | Done |
| Phase 2: Core | 8 | 6 | In Progress |
| Phase 3: Integration | 4 | 0 | Pending |

### Recent Completions
- [Task 1]: Completed [Date]
- [Task 2]: Completed [Date]

### Current Work
- [Task Name]: [Status]
- Blocker: [None / Description]

### Next Steps
1. Complete [Task X]
2. Begin [Task Y]
3. Run phase validation

### Validation Status
- Build: Passing
- Tests: 85% coverage (target: 80%)
- Lint: Passing
```

---

## Quick Start Templates

### Quick PRP (Low Complexity)

For features under 1 day:

```markdown
# Quick PRP: [Feature Name]

## What
[1-2 sentences describing the change]

## Why
[Business/technical justification]

## How
[High-level approach]

## Tasks
1. [ ] [Task 1]
2. [ ] [Task 2]
3. [ ] [Task 3]

## Validation
- [ ] Build passes
- [ ] Tests pass
- [ ] Manual verification

## Done When
- [ ] [Acceptance criterion 1]
- [ ] [Acceptance criterion 2]
```

### Enhancement PRP (Medium Complexity)

For enhancements to existing features:

```markdown
# Enhancement PRP: [Feature Enhancement Name]

## Current Behavior
[How the feature works now]

## Desired Behavior
[How it should work after enhancement]

## User Impact
[Who benefits and how]

## Technical Approach
[How we'll implement this]

## Tasks
### Phase 1: Analysis
1. [ ] Review existing code
2. [ ] Identify change points

### Phase 2: Implementation
1. [ ] Implement changes
2. [ ] Update tests
3. [ ] Update documentation

### Phase 3: Validation
1. [ ] Run all tests
2. [ ] Manual QA
3. [ ] Performance check

## Rollback Plan
[How to revert if issues arise]
```

---

## Error Handling

### Common Issues and Resolutions

| Issue | Resolution |
|-------|------------|
| PRD too vague | Re-run Phase 1 with more detailed questions |
| Complexity underestimated | Regenerate implementation plan with higher complexity |
| Validation failing | Identify failing validation, fix, re-run |
| Task blocked by dependency | Mark as blocked, work on other tasks |
| Scope creep | Document in "Out of Scope", create separate PRD |
| Missing requirements | Update PRD, regenerate affected tasks |

### Recovery Procedures

```markdown
## Recovery Procedures

### Validation Failure Recovery
1. Identify failing validation
2. Analyze error output
3. Fix the issue
4. Re-run validation
5. If still failing, document and escalate

### Blocked Task Recovery
1. Identify blocking dependency
2. Create task for dependency if missing
3. Update task with blocker reference
4. Work on unblocked tasks
5. Return when blocker resolved

### Scope Change Recovery
1. Document requested change
2. Assess impact on existing PRD
3. Update PRD with changes
4. Regenerate affected tasks
5. Update timeline estimates
6. Get stakeholder approval
```

---

## Best Practices

### PRD Writing

1. **Be Specific**: Vague requirements lead to rework
2. **Define Success**: Every goal needs a measurable metric
3. **Include Edge Cases**: Document error handling up front
4. **Set Boundaries**: Out of scope is as important as in scope
5. **Living Document**: Update PRD as you learn more

### Implementation

1. **One Phase at a Time**: Complete and validate before moving on
2. **Validate Often**: Run validations after each significant change
3. **Document Decisions**: Record why you chose specific approaches
4. **Keep Tests Current**: Tests should evolve with implementation
5. **Clean Commits**: Each commit should be a logical, working unit

### Archon Integration

1. **Update Status**: Always update task status when state changes
2. **Add Notes**: Document blockers, decisions, and discoveries
3. **Track Time**: Note actual duration vs. estimates
4. **Link Related Items**: Connect tasks to PRD and each other

---

## Command Reference

| Command | Description |
|---------|-------------|
| `/prp-wizard` | Start PRP wizard |
| `/prp-wizard --quick` | Quick PRP for simple features |
| `/prp-wizard --resume` | Resume existing PRP |
| `/prp-status` | Check PRP implementation status |
| `/prp-validate` | Run validation checkpoint |
| `/prp-tasks` | Generate Archon tasks from PRD |

---

## Integration with Project Wizard

When invoked from project-wizard skill:

```python
# Project wizard hands off to PRP wizard
if selected_framework == "prp":
    # Pass context from project wizard
    prp_context = {
        "project_name": project_name,
        "project_type": project_type,
        "tech_stack": tech_stack,
        "archon_project_id": project_id,
        "working_directory": working_dir
    }

    # PRP wizard continues with Phase 1
    # Skip redundant questions already answered
```

---

## Notes

- PRD quality directly impacts implementation quality
- Complexity assessment helps choose the right approach
- Validation checkpoints catch issues early
- Archon integration enables progress tracking across sessions
- Templates are starting points - adapt to project needs
- Always update PRD when requirements change
