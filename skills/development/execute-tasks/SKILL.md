---
name: execute-tasks
description: Sequentially executes tasks from tasks.yaml with proper context gathering,
  skill invocation, and result tracking. Ensures consistent execution across all development
  tasks.
---

# Execute-Tasks Skill

## Purpose
Sequentially executes tasks from tasks.yaml with proper context gathering, skill invocation, and result tracking. Ensures consistent execution across all development tasks.

## Tier
**Tier 0** - Pre-Launch Foundation

## When to Use
- After write-plan creates tasks.yaml
- Starting development work
- Resuming work after breaks
- Processing task backlog
- Executing sprint work

## Process

### 1. Task Loading
- Read tasks.yaml
- Filter by sprint/status
- Check dependencies
- Verify prerequisites

### 2. Context Gathering
Before each task:
- Load relevant documentation
- Check related code
- Review previous task outputs
- Gather test data
- Save context to ai-state/contexts/

### 3. Skill Invocation
- Identify assigned orchestrator
- Prepare context package
- Invoke appropriate skill
- Monitor execution
- Capture outputs

### 4. Execution Monitoring
- Track execution time
- Monitor resource usage
- Log all operations
- Capture errors
- Update progress

### 5. Result Processing
- Validate outputs
- Run initial tests
- Update task status
- Log completion
- Trigger next steps

## Execution Flow
```
┌─────────────┐
│ Load Tasks  │
└──────┬──────┘
       ▼
┌─────────────┐
│Check Status │◄────┐
└──────┬──────┘     │
       ▼            │
┌─────────────┐     │
│Get Next Task│     │
└──────┬──────┘     │
       ▼            │
┌─────────────┐     │
│Gather Context│    │
└──────┬──────┘     │
       ▼            │
┌─────────────┐     │
│Execute Skill│     │
└──────┬──────┘     │
       ▼            │
┌─────────────┐     │
│ Run Tests   │     │
└──────┬──────┘     │
       ▼            │
┌─────────────┐     │
│Update Status│─────┘
└─────────────┘
```

## Context Package Format
```yaml
task_context:
  task_id: "task-001"
  epic: "epic-001"
  sprint: "sprint-001"

  dependencies:
    completed_tasks: ["task-000"]
    required_files: ["src/models/User.py"]
    external_services: ["database", "redis"]

  relevant_code:
    - file: "src/models/User.py"
      functions: ["create_user", "validate_email"]
    - file: "tests/test_user.py"
      tests: ["test_user_creation"]

  knowledge:
    patterns: ["Repository pattern"]
    decisions: ["Use PostgreSQL"]
    standards: ["backend-standard.md"]

  test_data:
    users: ["test_user_1.json"]
    transactions: ["test_transactions.json"]

  previous_outputs:
    - task: "task-000"
      output: "Database schema created"
      artifacts: ["schema.sql"]
```

## Task Execution Rules

### Sequential Execution
- One task at a time
- Complete before moving to next
- Respect dependencies
- No parallel execution within skill

### Dependency Management
- Check all dependencies met
- Wait for blocking tasks
- Skip if prerequisites missing
- Alert on circular dependencies

### Error Handling
- Retry failed tasks (max 3)
- Log all errors
- Save partial progress
- Mark as blocked if unresolvable
- Escalate to user

## Status Transitions
```
pending → in_progress → testing → completed
           ↓             ↓
        blocked       failed
           ↓             ↓
        unblocked    retrying
```

## Integration Points
- **Reads from**: tasks.yaml
- **Invokes**: All orchestrator skills
- **Updates**: Task status, operations.log
- **Triggers**: task-completion-hook

## Quality Standards
- Context gathering < 30 seconds
- Skill invocation success rate > 95%
- Test execution on every task
- Status updates within 5 seconds
- Complete logging of all operations

## Example Usage
```bash
/execute-tasks
```

This will:
1. Load pending tasks for current sprint
2. Execute each task sequentially
3. Gather context before execution
4. Run tests after completion
5. Update status and logs

## Execution Strategies

### Sprint Execution
```yaml
mode: "sprint"
sprint_id: "sprint-001"
strategy: "priority_order"
stop_on_failure: false
```

### Milestone Rush
```yaml
mode: "milestone"
milestone_id: "milestone-001"
strategy: "dependency_order"
stop_on_failure: true
```

### Continuous Flow
```yaml
mode: "continuous"
batch_size: 5
strategy: "fifo"
stop_on_failure: false
```

## Performance Metrics
- Task throughput: 2-3 tasks/hour
- Context gathering: < 30 seconds
- Test execution: < 5 minutes
- Status update latency: < 5 seconds
- Error recovery rate: > 80%

## Common Patterns
- **Morning Sync**: Load tasks, check blockers
- **Task Batching**: Group similar tasks
- **Context Caching**: Reuse for similar tasks
- **Progressive Testing**: Quick tests first
- **Checkpoint Saves**: Regular progress saves

## Anti-Patterns to Avoid
- Skipping context gathering
- Parallel task execution
- Ignoring dependencies
- Missing test execution
- Poor error handling
- Incomplete logging

## Troubleshooting

### Task Stuck in Progress
1. Check operations.log
2. Verify skill availability
3. Check for deadlocks
4. Reset task status
5. Retry execution

### Context Gathering Fails
1. Verify file paths
2. Check permissions
3. Validate dependencies
4. Review previous outputs
5. Manual context provision

### Test Failures
1. Review test output
2. Check test data
3. Verify environment
4. Run tests individually
5. Update test expectations