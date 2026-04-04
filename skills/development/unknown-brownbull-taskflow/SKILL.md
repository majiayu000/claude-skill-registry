# Task Completion Hook Skill V3 - Pragmatic Testing

## Purpose
Triggered when a task completes, runs phase-appropriate tests (not all 8), moves passing tests to regression folders, and updates task status.

## Core Change from V2
**Instead of requiring all 8 test types to pass:**
- Prototype: Just 2 tests (smoke + happy path)
- MVP: 4 tests
- Growth: 5 tests
- Scale: 6-8 tests (only if needed)

## Phase-Aware Workflow

### 1. Detect Current Phase
```python
def get_required_tests(task, project_phase):
    """Return only tests required for current phase"""

    PHASE_REQUIREMENTS = {
        'prototype': ['smoke', 'happy_path'],
        'mvp': ['smoke', 'happy_path', 'critical_errors', 'auth'],
        'growth': ['happy_path', 'errors', 'edge_cases', 'performance', 'security'],
        'scale': task.get('required_tests', [])  # Custom per task
    }

    return PHASE_REQUIREMENTS[project_phase]
```

### 2. Run Only Required Tests
```python
def run_task_tests(task):
    phase = detect_project_phase()
    required_tests = get_required_tests(task, phase)

    # Only run what's required, not all 8
    for test_type in required_tests:
        if test_type in task['check']:
            run_test(task['check'][test_type])
```

### 3. Success Criteria V3
```yaml
success_criteria:
  prototype:
    required_pass: ['smoke', 'happy_path']
    acceptable_failures: ['all_others']

  mvp:
    required_pass: ['smoke', 'happy_path', 'auth']
    acceptable_failures: ['edge_cases', 'performance']

  growth:
    required_pass: ['happy_path', 'errors', 'security']
    acceptable_failures: ['visual', 'rare_edge_cases']
```

## Escape Hatches

### Skip Tests Temporarily
```python
if task.get('overrides', {}).get('skip_tests'):
    log("Tests skipped due to override")
    mark_task_complete_with_debt()
    return
```

### Defer Test Failures
```python
if task.get('overrides', {}).get('defer_failures'):
    move_failures_to_tech_debt()
    mark_task_complete_with_warning()
    return
```

## Test Movement Rules V3

### Only Move Passing Tests
```python
def move_tests_to_regression(task):
    """Only move tests that actually exist and pass"""

    for test_file in task['test_files']:
        if test_passed(test_file):
            move_to_regression(test_file)
        elif test_is_critical(test_file):
            create_fix_task(test_file)
        else:
            # Non-critical failing test
            log_as_technical_debt(test_file)
```

### Smart Test Classification
```python
def classify_test_importance(test):
    """Determine if test failure should block"""

    CRITICAL_PATTERNS = [
        'login', 'auth', 'payment', 'data_loss',
        'security', 'user_registration'
    ]

    if any(pattern in test.name for pattern in CRITICAL_PATTERNS):
        return 'CRITICAL'  # Must fix

    if project_phase in ['prototype', 'mvp']:
        return 'DEFERRABLE'  # Can fix later

    return 'NORMAL'
```

## Implementation-First Test Fix

### Auto-Fix Test Mismatches
```python
def fix_test_implementation_mismatch(test, implementation):
    """Update test to match actual implementation"""

    # Extract actual method signatures
    actual_signature = extract_signature(implementation)
    test_signature = extract_test_signature(test)

    if actual_signature != test_signature:
        # Update test to match reality
        updated_test = align_test_to_implementation(
            test,
            actual_signature
        )
        save_test(updated_test)
        return True

    return False
```

## ROI-Based Test Priority

### Skip Low-Value Tests
```python
def should_run_test(test, phase):
    """Determine if test is worth running"""

    test_roi = calculate_roi(test)

    if phase == 'prototype':
        return test_roi > 2.0  # Only high-value

    if phase == 'mvp':
        return test_roi > 1.0  # Medium and up

    if phase == 'growth':
        return test_roi > 0.5  # Most tests

    return True  # Scale: run everything
```

## Failure Handling V3

### Progressive Response to Failures
```yaml
failure_responses:
  prototype:
    action: "Log and continue"
    create_ticket: false
    block_completion: false

  mvp:
    action: "Fix if critical, defer others"
    create_ticket: true
    block_completion: "Only for auth/payment"

  growth:
    action: "Fix most failures"
    create_ticket: true
    block_completion: "For customer-facing issues"

  scale:
    action: "Fix all failures"
    create_ticket: true
    block_completion: true
```

## Quick Decision Flow

```python
def handle_task_completion(task):
    phase = detect_project_phase()

    # Prototype? Just check basics
    if phase == 'prototype':
        if basic_smoke_test_passes():
            mark_complete()
            return

    # MVP? Check critical paths
    if phase == 'mvp':
        if critical_tests_pass():
            mark_complete()
            defer_non_critical_failures()
            return

    # Growth/Scale? More comprehensive
    run_phase_appropriate_tests()
    handle_failures_by_importance()
```

## Metrics V3

### Track What Matters
```python
metrics = {
    'tests_run': count_by_phase(),
    'tests_skipped': count_deferred(),
    'time_saved': estimate_time_not_writing_tests(),
    'false_failures_fixed': count_mismatches_fixed(),
    'tech_debt_created': track_deferred_tests()
}
```

## Migration from V2

### Reduce Test Requirements
```python
def migrate_task_requirements(task):
    """Reduce from 8 tests to phase-appropriate"""

    current_phase = detect_project_phase()

    if current_phase == 'prototype':
        # Reduce to 2 tests
        task['required_tests'] = ['smoke', 'happy_path']
        task['optional_tests'] = []

    elif current_phase == 'mvp':
        # Reduce to 4 tests
        task['required_tests'] = [
            'smoke', 'happy_path',
            'critical_errors', 'auth'
        ]

    return task
```

## Example Execution

### Prototype Phase
```yaml
Task: "Create user API"
Phase: prototype
Tests Required: 2

Execution:
  1. Run smoke test ✅
  2. Run happy path ✅
  3. Mark complete ✅
  4. Skip other 6 test types
  5. Move to next task

Time: 10 minutes (vs 60 minutes with 8 tests)
```

### MVP Phase
```yaml
Task: "Add payment processing"
Phase: mvp
Tests Required: 4

Execution:
  1. Run smoke ✅
  2. Run happy path ✅
  3. Run auth test ✅
  4. Run error handling ❌
  5. Fix critical error
  6. Re-run and pass ✅
  7. Mark complete

Time: 30 minutes (vs 120 minutes with 8 tests)
```

## Summary

Task Completion Hook V3:
- Runs only phase-appropriate tests
- Fixes test-implementation mismatches
- Provides escape hatches
- Tracks meaningful metrics
- Saves significant time

**Result**: Tasks complete faster with appropriate quality for current phase.