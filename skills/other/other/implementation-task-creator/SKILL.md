---
name: implementation-task-creator
description: Use when breaking down a component for implementation - creates task file in implementation_process/in_progress/ with TDD steps and acceptance criteria
version: 1.1.0
---

# Implementation Task Creator

Create task files that break down components into implementable TDD steps.

## Activation

Activate when you detect:
- "Break down X for implementation"
- "Create task for X"
- Moving from Phase 2 to Phase 3
- Need implementation tasks for a component

## Workflow

### 1. Load Component Architecture

Use `Read` on `{project_path}/architecture/{component}.md`

If file doesn't exist, ask: "No architecture found for {component}. Create architecture first?"

Extract:
- Component purpose
- Interface (methods, parameters)
- Dependencies
- Pattern reference
- Acceptance criteria

### 2. Determine Task Scope

Ask user:
```
How should this component be broken down?
1. Single task (small component)
2. Multiple tasks by method/feature
3. Multiple tasks by layer (test, implementation, integration)

Your choice:
```

### 3. Define Task Order

Based on dependencies, determine implementation order. Ask:
```
Proposed task order:
1. {task 1} - {why first}
2. {task 2} - {depends on 1}
3. {task 3} - {depends on 2}

Adjust order? (yes/no)
```

### 4. Create Task File(s)

For each task, use `Write` to create `{project_path}/implementation_process/in_progress/{nn}_{task_name}.md`:

```markdown
# Task: {Task Name}

**Component:** {component name}
**Created:** {YYYY-MM-DD}
**Status:** Not Started
**Priority:** {nn}

## Objective
{What this task accomplishes - one paragraph}

## Prerequisites
- [ ] {Task that must be complete first, or "None"}

## Acceptance Criteria
- [ ] {Criterion 1 - specific and testable}
- [ ] {Criterion 2}
- [ ] {Criterion 3}
- [ ] All tests pass
- [ ] Code follows Drupal standards

## TDD Steps

### Step 1: Write Failing Test
Create test file:
```
tests/src/{Unit|Kernel}/{TestClass}Test.php
```

Test case:
```php
public function test{MethodName}(): void {
  // Arrange: {setup}
  // Act: {action}
  // Assert: {expected result}
}
```

### Step 2: Verify Test Fails
Run: `ddev phpunit {test_path}`
Expected: Test fails (class/method not found)

### Step 3: Write Minimum Implementation
Create: `src/{Type}/{ClassName}.php`
Implement only enough to pass the test.

### Step 4: Verify Test Passes
Run: `ddev phpunit {test_path}`
Expected: Test passes

### Step 5: Refactor
Clean up code while keeping tests green.

## Files to Create/Modify
| File | Action | Purpose |
|------|--------|---------|
| `src/{path}` | Create | Main implementation |
| `tests/src/{path}` | Create | Test coverage |
| `*.services.yml` | Modify | Service registration |

## Pattern Reference
Follow: `{core path from architecture}`

Key aspects:
- {what to copy from pattern}
- {what to adapt}

## Notes
{Any specific considerations from architecture}
```

### 5. Update project_state.md

Use `Edit` to update the project state:
```markdown
## Current Focus
Implementation Phase - {component name}

## Next Steps
1. Complete task: {first task name}
```

### 6. Confirm

Show user:
```
Created {count} task(s) for {component}:
1. {task 1} - in_progress/{filename}
2. {task 2} - in_progress/{filename}

Start with task 1? Use: /drupal-dev-framework:implement {task_name}
```

## Stop Points

STOP and wait for user:
- If architecture file not found
- After asking about task breakdown
- After showing proposed order
- After creating files (confirm before proceeding)
