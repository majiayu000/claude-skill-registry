---
name: create-story-tasks
description: Use to decompose user stories into individual development tasks. Creates task documents that can be assigned, estimated, and tracked.
version: 1.0.0
---
<!-- Powered by Prism Coreâ„¢ -->

# create-story-tasks

Break down a user story into individual development tasks, creating task documents for each.

## Purpose

Decompose a user story into specific, actionable development tasks that can be assigned, estimated, and tracked independently. Each task should be small enough to complete in a single development session but meaningful enough to deliver value toward the story's acceptance criteria.

## SEQUENTIAL Task Execution

### 1. Load User Story
```yaml
inputs:
  - Story document from docs/stories/
  - Story ID, title, and description
  - Acceptance criteria list
  - Technical notes and requirements
  - Initial task breakdown from story
```

### 2. Analyze Story Scope

```yaml
analysis:
  acceptance_criteria_coverage:
    - Map each AC to required implementation work
    - Identify technical components affected
    - Determine task dependencies
    
  technical_assessment:
    - Frontend components needed
    - Backend services/APIs needed
    - Database changes required
    - Testing requirements
    
  task_granularity:
    - Each task should be 2-8 hours of work
    - Tasks should be independently testable
    - Tasks should align with PRISM principles
```

### 3. Generate Task Breakdown

```yaml
task_structure:
  naming_convention: "{{story_id}}-T{{task_num}}"
  # Example: US-001-T1, US-001-T2, etc.
  
  task_categories:
    - Database/Schema changes
    - Backend API implementation
    - Frontend component development
    - Testing implementation
    - Documentation updates
    - Integration/deployment tasks
    
  task_template_per_task:
    task_id: "{{story_id}}-T{{number}}"
    task_title: "{{brief_description}}"
    acceptance_criteria_refs: [{{ac_numbers}}]
    estimated_hours: "{{2-8}}"
    dependencies: [{{other_task_ids}}]
```

### 4. Create Individual Task Documents

For each identified task, create a task document:

```markdown
# Task {{story_id}}-T{{number}}: {{task_title}}

## Story Reference
- **Parent Story:** {{story_id}} - {{story_title}}
- **Story Link:** [{{story_id}}](../stories/{{story_file}})

## Task Description

{{detailed_description_of_what_needs_to_be_done}}

## Acceptance Criteria Coverage

This task contributes to the following story acceptance criteria:
- AC #{{number}}: {{criteria_text}}
- AC #{{number}}: {{criteria_text}}

## Implementation Requirements

### Functional Requirements
1. {{requirement_1}}
2. {{requirement_2}}
3. {{requirement_3}}

### Technical Details
- **Component/Module:** {{component_name}}
- **Files to Modify:** 
  - {{file_path_1}}
  - {{file_path_2}}
- **New Files to Create:**
  - {{file_path_3}}

### PRISM Principles Application
- **Predictability:** {{how_task_ensures_predictable_outcome}}
- **Resiliency:** {{testing_strategy}}
- **Intentionality:** {{design_decisions_and_rationale}}
- **Sustainability:** {{maintainable_approach}}
- **Maintainability:** {{clear_code_structure}}

## Dependencies

### Upstream Dependencies (must complete first)
- {{task_id}}: {{brief_reason}}

### Downstream Dependencies (waiting on this)
- {{task_id}}: {{brief_reason}}

### External Dependencies
- {{service/resource}}: {{what_is_needed}}

## Testing Requirements

### Unit Tests
- Test: {{test_case_1}}
- Test: {{test_case_2}}

### Integration Tests
- Test: {{integration_scenario}}

### Manual Testing Steps
1. {{step_1}}
2. {{step_2}}
3. {{step_3}}

## Definition of Done
- [ ] Implementation complete per requirements
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] Acceptance criteria validated
- [ ] No regression in existing functionality

## Estimation

### PSP/PROBE Estimation
- **Estimated Hours:** {{optimistic}}-{{likely}}-{{pessimistic}}
- **Story Points:** {{1|2|3}} (task level)
- **Size Category:** {{very_small|small|medium}}
- **Similar Tasks:** {{references}}
- **Confidence:** {{high|medium|low}}

### Tracking
- **Started:** {{date_time}}
- **Completed:** {{date_time}}
- **Actual Hours:** {{hours}}
- **Variance:** {{percentage}}

## Technical Notes

{{any_architecture_patterns_to_follow}}
{{coding_standards_references}}
{{security_considerations}}
{{performance_requirements}}

## Implementation Notes

{{dev_agent_records_implementation_details}}
{{challenges_encountered}}
{{decisions_made}}
{{files_actually_modified}}

---

**Status:** {{Not Started|In Progress|Review|Testing|Done}}
**Assigned To:** {{agent_or_developer}}
**Created:** {{date}}
**Updated:** {{date}}
```

### 5. Task Ordering Strategy

```yaml
recommended_task_order:
  phase_1_foundation:
    - Database schema changes
    - Data models/entities
    - Migration scripts
    
  phase_2_backend:
    - API endpoints
    - Business logic
    - Service layer
    
  phase_3_frontend:
    - UI components
    - State management
    - Integration with APIs
    
  phase_4_testing:
    - E2E tests
    - Integration tests
    - Performance tests
    
  phase_5_finalization:
    - Documentation
    - Deployment configuration
    - Monitoring/observability

dependency_rules:
  - Backend tasks before frontend tasks
  - Database changes before API changes
  - Component creation before integration
  - Implementation before testing
  - Testing before documentation
```

### 6. Create Task Index

Update the parent story document:

```markdown
## Tasks Created

| Task ID | Title | Status | Estimated | Actual | AC Refs |
|---------|-------|--------|-----------|--------|---------|
| {{story_id}}-T1 | {{title}} | {{status}} | {{est_hours}} | {{actual_hours}} | #1, #2 |
| {{story_id}}-T2 | {{title}} | {{status}} | {{est_hours}} | {{actual_hours}} | #3 |
| {{story_id}}-T3 | {{title}} | {{status}} | {{est_hours}} | {{actual_hours}} | #2, #4 |

**Total Estimated Hours:** {{sum_of_estimates}}
**Total Actual Hours:** {{sum_of_actuals}}
**Task Count:** {{number_of_tasks}}
```

### 7. Quality Checks

```yaml
validation_checklist:
  coverage:
    - [ ] All acceptance criteria mapped to tasks
    - [ ] All technical components addressed
    - [ ] Testing tasks included
    - [ ] Documentation tasks present
    
  task_quality:
    - [ ] Each task has clear, actionable description
    - [ ] Dependencies identified and documented
    - [ ] Estimates provided using PROBE method
    - [ ] Testing requirements specified
    - [ ] PRISM principles applied
    
  sizing:
    - [ ] No task exceeds 8 hours estimate
    - [ ] Tasks are independently deliverable
    - [ ] Task breakdown is logical and sequential
```

## Success Criteria
- [ ] All story acceptance criteria covered by tasks
- [ ] Task documents created in docs/tasks/
- [ ] Task dependencies mapped
- [ ] Estimates provided for all tasks
- [ ] Parent story document updated with task index
- [ ] Tasks ordered by logical implementation sequence
- [ ] Each task aligns with PRISM principles

## Output
- Task document files: `docs/tasks/{{story_id}}-T{{n}}-{{slug}}.md`
- Updated story document with task index
- Task dependency graph (if complex)
- Total effort estimate for story

## Integration with PRISM Workflow

This task integrates with:
- **Before:** Story creation and refinement
- **After:** Individual task execution by Dev agent
- **Parallel:** QA test design from acceptance criteria
- **Quality Gates:** Story estimation, sprint planning

## Notes

- Keep tasks focused and atomic
- Ensure clear handoff between tasks
- Document assumptions and constraints
- Use consistent naming conventions
- Reference architecture and coding standards
- Consider rollback/revert strategy for each task

