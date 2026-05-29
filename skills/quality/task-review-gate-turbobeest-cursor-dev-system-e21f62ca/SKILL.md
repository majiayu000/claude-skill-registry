# Task Review Gate Skill

## Metadata
- skill_name: task-review-gate
- activation_code: TASK_REVIEW_GATE_V1
- version: 1.0.0
- category: review
- phase: 5.1

## Description
Interactive review and refinement gate after PRD-to-Tasks generation. Allows human review, discussion, and fine-tuning before proceeding with full automation.

## Activation Criteria
- Triggered after PRD_TO_TASKS_V1 completes
- Before coupling analysis begins
- When tasks.json is created
- Requires human interaction

## Review Process

### 1. Task Presentation
```
════════════════════════════════════════════
  TASK REVIEW & REFINEMENT GATE
════════════════════════════════════════════

Generated 30 tasks from PRD analysis:

PHASE 1: Requirements & Design (Tasks 1-5)
  Task 1: Set up project structure
  Task 2: Design system architecture
  Task 3: Define API contracts
  ...

PHASE 2: Core Development (Tasks 6-15)
  Task 6: Implement database schema
  Task 7: Build authentication service
  ...

[Full task list displayed with details]
```

### 2. Review Options
```
Review Options:
  1) View detailed task breakdown
  2) Modify a specific task
  3) Add new task
  4) Remove task
  5) Reorder tasks
  6) Adjust dependencies
  7) View coupling analysis
  8) APPROVE and continue
  9) REJECT and regenerate
  
Select option (1-9): _
```

### 3. Interactive Refinement

#### Viewing Task Details
```python
def show_task_details(task_id):
    task = tasks[task_id]
    print(f"""
    Task #{task_id}: {task['title']}
    ═══════════════════════════════════
    Description: {task['description']}
    
    Dependencies: {task['dependencies']}
    Acceptance Criteria:
    {format_criteria(task['criteria'])}
    
    Estimated Effort: {task['effort']}
    Critical Path: {task['critical']}
    """)
```

#### Modifying Tasks
```python
def modify_task(task_id):
    print(f"Current task: {tasks[task_id]['title']}")
    print("\nWhat would you like to modify?")
    print("1) Title")
    print("2) Description")
    print("3) Dependencies")
    print("4) Acceptance criteria")
    print("5) Priority")
    
    # Interactive modification with validation
    # Natural language input accepted
    # Claude helps refine the changes
```

### 4. Natural Language Refinement

User can provide feedback like:
- "Task 7 should come before Task 6"
- "Add a task for security audit after Task 15"
- "The database task needs to include migration setup"
- "Split the authentication task into JWT and OAuth2"
- "These tasks look good but add monitoring setup"

Claude processes and applies refinements intelligently.

### 5. Validation Before Approval

```python
def validate_before_approval():
    issues = []
    
    # Check for circular dependencies
    if has_circular_dependencies(tasks):
        issues.append("Circular dependency detected")
    
    # Check for missing critical components
    if not has_required_components(tasks, prd):
        issues.append("Missing critical PRD requirements")
    
    # Check task count reasonability
    if len(tasks) > 50:
        issues.append("Warning: High task count may impact timeline")
    
    return issues
```

## Review States

### DRAFT
- Initial task generation complete
- Awaiting human review
- Full modification allowed

### UNDER_REVIEW
- Human actively reviewing
- Real-time refinements happening
- Claude assists with changes

### APPROVED
- Human has approved tasks
- Minor refinements still allowed
- Ready for automation

### REJECTED
- Significant issues found
- Requires regeneration
- Returns to PRD analysis

## Integration Points

### Inputs
- tasks.json from PRD-to-Tasks
- PRD.md for reference
- User feedback and refinements

### Outputs
- tasks-reviewed.json (refined version)
- review-log.json (audit trail)
- approval-signal.json

### Signals
- TASKS_UNDER_REVIEW
- TASKS_APPROVED
- TASKS_REJECTED
- PROCEED_TO_AUTOMATION

## Review Commands

### During Review Session
- `show all` - Display all tasks
- `show phase X` - Display specific phase
- `detail X` - Show task X details
- `modify X` - Edit task X
- `add after X` - Insert new task
- `remove X` - Delete task
- `deps X` - Show/edit dependencies
- `couple` - Run coupling analysis
- `validate` - Check for issues
- `approve` - Confirm and proceed
- `reject` - Start over

## Example Interaction

```
User: "The authentication task should be split into two - one for JWT setup and another for OAuth2 integration"

Claude: I'll split Task 7 into two subtasks:
  
  Task 7a: Implement JWT Authentication
  - Setup JWT token generation
  - Configure refresh tokens
  - Add token validation middleware
  
  Task 7b: Implement OAuth2 Integration  
  - Configure OAuth2 providers
  - Setup callback handlers
  - Add social login flows

This will also adjust dependencies for Task 8 and 9.
Shall I apply these changes? (y/n)

User: "Yes, and make sure both are required before Task 10"

Claude: Updated! Both 7a and 7b are now prerequisites for Task 10.
Current dependency chain: 6 → 7a,7b → 10

Continue reviewing? (show all/approve/more changes)
```

## Approval Criteria

Before allowing progression:
1. ✓ All tasks have clear descriptions
2. ✓ Dependencies are valid (no cycles)
3. ✓ Critical PRD requirements covered
4. ✓ Effort estimates reasonable
5. ✓ User explicitly approves

## Time Estimates

- Initial review: 5-10 minutes
- Per modification: 1-2 minutes
- Full refinement session: 10-20 minutes
- Re-generation if rejected: 5 minutes

## Benefits

1. **Quality Control**: Catch issues before automation
2. **Customization**: Tailor tasks to specific needs
3. **Learning**: Claude learns from refinements
4. **Confidence**: User knows exactly what will be built
5. **Flexibility**: Easy to adjust without stopping pipeline

## Post-Approval Flow

Once approved:
```
TASKS_APPROVED signal → 
  Coupling Analysis (automatic) →
    Task Decomposition (automatic) →
      Full automation begins
```

No further interruptions unless error occurs.