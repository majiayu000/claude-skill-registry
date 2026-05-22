---
name: test-scenario-framework
description: Define and run end-to-end test scenarios for medical residency scheduling. Use when validating complex scheduling logic, testing edge cases, verifying ACGME compliance under stress, or running regression scenarios. Includes 20+ pre-built scenarios covering N-1 failures, multi-swap operations, holiday conflicts, and moonlighting.
---

# Test Scenario Framework Skill

Comprehensive framework for defining, executing, and validating complex scheduling test scenarios.

## When This Skill Activates

- Running regression tests before release
- Validating complex scheduling edge cases
- Testing N-1 contingency scenarios
- Verifying ACGME compliance under load
- Multi-swap operation validation
- Holiday/vacation conflict testing
- Moonlighting schedule validation
- Schedule generation stress testing
- Integration testing of scheduling engine
- Reproducing reported bugs with scenarios

## Overview

The Test Scenario Framework provides a structured approach to test scheduling operations end-to-end. Each scenario includes:

1. **Setup**: Initial state (persons, rotations, assignments)
2. **Test Case**: Operations to perform (swaps, generation, validation)
3. **Expected Outcome**: Success criteria and expected results
4. **Validation**: Automated checks against expectations

## Skill Phases

### Phase 1: Scenario Selection
**Identify the appropriate scenario(s) to run**

```
Options:
1. Select from pre-built scenario library (20+ scenarios)
2. Define custom scenario for specific test case
3. Combine multiple scenarios for integration testing
4. Create scenario from bug report
```

### Phase 2: Scenario Definition
**Define or load scenario specification**

```yaml
scenario:
  name: "N-1 Failure During Holiday Coverage"
  id: "n1-holiday-coverage-001"
  category: "resilience"
  tags: ["n-1", "holiday", "acgme"]

  setup:
    persons:
      - id: "resident-1"
        role: "RESIDENT"
        pgy_level: 2
        max_hours_per_week: 80
      # ... more persons

    assignments:
      - person_id: "resident-1"
        block_date: "2024-12-25"
        rotation: "inpatient"
        hours: 12
      # ... more assignments

  test_case:
    operation: "simulate_unavailability"
    parameters:
      person_id: "resident-1"
      start_date: "2024-12-25"
      end_date: "2024-12-27"
      reason: "illness"

  expected_outcome:
    success: true
    coverage_maintained: true
    acgme_compliant: true
    backup_activated: true
    max_reassignments: 5
```

### Phase 3: Scenario Execution
**Run scenario with monitoring and timeout protection**

```python
from app.testing.scenario_executor import ScenarioExecutor

executor = ScenarioExecutor()
result = await executor.run_scenario(
    scenario_id="n1-holiday-coverage-001",
    timeout=300,  # 5 minutes
    capture_metrics=True
)
```

### Phase 4: Result Validation
**Compare results against expected outcomes**

```python
validator = ScenarioValidator()
validation_result = validator.validate(
    actual=result,
    expected=scenario.expected_outcome,
    tolerance={
        "numeric_fields": 0.05,  # 5% tolerance
        "assignment_count": 2     # Allow ±2 assignments
    }
)
```

### Phase 5: Reporting
**Generate comprehensive test report**

```
## Scenario Test Report

**Scenario:** N-1 Failure During Holiday Coverage
**Status:** ✅ PASSED
**Execution Time:** 3.2s
**Coverage Impact:** 0 gaps detected

### Validations
✅ Coverage maintained after failure
✅ ACGME compliance preserved
✅ Backup assignments within threshold
✅ No cascade failures detected

### Metrics
- Assignments modified: 3
- Persons affected: 2
- Compliance checks: 12/12 passed
- Performance: 3.2s (target: <5s)
```

## Key Files

### Scenario Definition Files
```
backend/tests/scenarios/
├── n1_failures/              # N-1 contingency scenarios
│   ├── holiday_coverage.yaml
│   ├── multi_absence.yaml
│   └── cascade_failure.yaml
├── swap_scenarios/           # Swap operation scenarios
│   ├── one_to_one_simple.yaml
│   ├── multi_swap_chain.yaml
│   └── absorb_with_coverage.yaml
├── acgme_edge_cases/        # ACGME compliance edge cases
│   ├── 80_hour_boundary.yaml
│   ├── one_in_seven_strict.yaml
│   └── supervision_ratio.yaml
└── integration/             # Multi-operation scenarios
    ├── full_month_generation.yaml
    └── concurrent_swaps.yaml
```

### Execution Engine
```
backend/app/testing/
├── scenario_executor.py      # Main execution engine
├── scenario_validator.py     # Result validation
├── scenario_fixtures.py      # Test data generators
├── scenario_metrics.py       # Performance tracking
└── scenario_reporter.py      # Report generation
```

## Output

### Successful Scenario Run
```json
{
  "scenario_id": "n1-holiday-coverage-001",
  "status": "passed",
  "execution_time_seconds": 3.2,
  "validations": {
    "coverage_maintained": {"expected": true, "actual": true, "passed": true},
    "acgme_compliant": {"expected": true, "actual": true, "passed": true},
    "backup_activated": {"expected": true, "actual": true, "passed": true}
  },
  "metrics": {
    "assignments_modified": 3,
    "persons_affected": 2,
    "compliance_checks_passed": 12,
    "compliance_checks_total": 12
  },
  "artifacts": {
    "initial_state": "snapshots/scenario-001-initial.json",
    "final_state": "snapshots/scenario-001-final.json",
    "execution_log": "logs/scenario-001.log"
  }
}
```

### Failed Scenario Run
```json
{
  "scenario_id": "multi-swap-chain-003",
  "status": "failed",
  "execution_time_seconds": 2.1,
  "failure_reason": "ACGME compliance violation after swap chain",
  "validations": {
    "swap_chain_completed": {"expected": true, "actual": false, "passed": false},
    "acgme_compliant": {"expected": true, "actual": false, "passed": false}
  },
  "errors": [
    {
      "type": "ACGMEViolation",
      "person_id": "resident-3",
      "rule": "80_hour_rule",
      "actual_hours": 84,
      "max_hours": 80,
      "affected_weeks": ["2024-W52"]
    }
  ]
}
```

## Error Handling

### Timeout Protection
```python
# All scenarios run with timeout
try:
    result = await asyncio.wait_for(
        executor.run_scenario(scenario),
        timeout=scenario.timeout or 300
    )
except asyncio.TimeoutError:
    return ScenarioResult(
        status="timeout",
        error="Scenario exceeded timeout limit"
    )
```

### State Rollback
```python
# Automatic rollback on failure
async with executor.transaction_context() as ctx:
    try:
        result = await executor.execute_operations(scenario)
        if not result.success:
            await ctx.rollback()
    except Exception as e:
        await ctx.rollback()
        raise
```

### Artifact Capture
```python
# Always capture state for debugging
executor.capture_snapshot("pre_execution")
try:
    result = await executor.run_scenario(scenario)
finally:
    executor.capture_snapshot("post_execution")
    executor.save_execution_log()
```

## Integration with Other Skills

### With acgme-compliance
```
Scenario execution automatically triggers ACGME validation
- Pre-execution compliance check
- Post-execution compliance verification
- Continuous monitoring during operations
```

### With safe-schedule-generation
```
Before running schedule generation scenarios:
1. Trigger database backup
2. Execute scenario in transaction
3. Validate results
4. Rollback if validation fails
```

### With systematic-debugger
```
When scenario fails:
1. Capture full execution trace
2. Generate hypothesis list
3. Create minimal reproduction scenario
4. Debug with context
```

### With test-writer
```
Convert successful scenarios to automated tests:
1. Extract scenario parameters
2. Generate pytest test case
3. Add to regression suite
4. Configure CI execution
```

## Workflow References

- **[Scenario Definition](Workflows/scenario-definition.md)** - How to write scenario specs
- **[Scenario Execution](Workflows/scenario-execution.md)** - Running scenarios end-to-end
- **[Scenario Validation](Workflows/scenario-validation.md)** - Validating results

## Reference Library

- **[Scenario Library](Reference/scenario-library.md)** - 20+ pre-built scenarios
- **[Success Criteria](Reference/success-criteria.md)** - Pass/fail criteria definitions

## Common Scenario Patterns

### Pattern 1: N-1 Failure Scenario
```python
"""Test system resilience when one person becomes unavailable."""
setup:
  - Create schedule with minimum coverage
  - Ensure N-1 backups are defined
test:
  - Mark person as unavailable
  - Trigger contingency activation
validate:
  - Coverage maintained
  - ACGME compliance preserved
  - Backup used efficiently
```

### Pattern 2: Multi-Operation Chain
```python
"""Test cascading operations maintain consistency."""
setup:
  - Create baseline schedule
test:
  - Execute swap operation
  - Generate new assignments
  - Validate compliance
  - Execute another swap
validate:
  - All operations succeeded
  - Final state is valid
  - No intermediate violations
```

### Pattern 3: Boundary Condition Test
```python
"""Test exact boundary conditions for rules."""
setup:
  - Create schedule at exact limit (e.g., 80 hours)
test:
  - Attempt operation that would exceed limit
validate:
  - Operation rejected or compensated
  - Limit not exceeded
  - Clear error message
```

## Running Scenarios

### Single Scenario
```bash
cd /home/user/Autonomous-Assignment-Program-Manager/backend

# Run specific scenario
pytest -m scenario -k "n1_holiday_coverage"

# Run with verbose output
pytest -m scenario -k "n1_holiday_coverage" -v

# Capture artifacts
pytest -m scenario -k "n1_holiday_coverage" --capture-artifacts
```

### Scenario Suite
```bash
# Run all N-1 scenarios
pytest -m scenario -k "n1_"

# Run all swap scenarios
pytest -m scenario -k "swap_"

# Run all ACGME edge cases
pytest -m scenario -k "acgme_edge"

# Run full regression suite
pytest -m scenario
```

### CI Integration
```yaml
# .github/workflows/scenario-tests.yml
name: Scenario Tests

on: [push, pull_request]

jobs:
  scenarios:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run N-1 scenarios
        run: pytest -m scenario -k "n1_"
      - name: Run swap scenarios
        run: pytest -m scenario -k "swap_"
      - name: Upload artifacts
        uses: actions/upload-artifact@v2
        with:
          name: scenario-artifacts
          path: tests/artifacts/
```

## Escalation Rules

**Escalate to human when:**
1. Scenario consistently times out (may need optimization)
2. Expected behavior unclear from requirements
3. Scenario reveals fundamental design flaw
4. Multiple related scenarios failing (systemic issue)
5. Performance degradation detected across scenarios

**Can handle automatically:**
1. Running pre-defined scenarios
2. Validating against expected outcomes
3. Generating test reports
4. Creating scenario variants
5. Regression testing

## Best Practices

### 1. Scenario Isolation
- Each scenario must be completely independent
- No shared state between scenarios
- Clean database state before each run
- Use fixtures for setup/teardown

### 2. Deterministic Results
- Avoid randomness unless testing random operations
- Use fixed dates and times
- Set random seeds when needed
- Mock external dependencies

### 3. Clear Naming
```
Format: {category}_{operation}_{edge_case}_{number}
Examples:
- n1_failure_holiday_coverage_001
- swap_multi_chain_acgme_boundary_002
- acgme_80hour_strict_limit_001
```

### 4. Comprehensive Documentation
```yaml
scenario:
  name: "Clear, descriptive name"
  description: "What this scenario tests and why"
  rationale: "Why this edge case matters"
  related_bugs: ["#123", "#456"]
  related_scenarios: ["swap_001", "acgme_005"]
```

### 5. Progressive Complexity
- Start with simple scenarios
- Build to complex multi-operation scenarios
- Use scenario composition for integration tests
- Keep individual scenarios focused

## References

- `backend/tests/scenarios/` - Scenario definition files
- `backend/app/testing/` - Execution framework
- `docs/testing/SCENARIO_TESTING.md` - Detailed guide (if exists)
- `CLAUDE.md` - Testing requirements
