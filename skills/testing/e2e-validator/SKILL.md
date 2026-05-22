---
activation_code: E2E_VALIDATOR_V1
phase: 10
prerequisites:
  - Integration tests passing
outputs:
  - E2E test results
  - .signals/phase5-complete.json
  - Go/No-Go decision
description: |
  Validates end-to-end user workflows and system behavior.
  Activates via codeword [ACTIVATE:E2E_VALIDATOR_V1] injected by hooks
  when entering Phase 5 E2E testing.
  
  Activation trigger: [ACTIVATE:E2E_VALIDATOR_V1]
---

# E2E Validator Skill

## Activation Method

This skill activates when the hook system injects the codeword:
```
[ACTIVATE:E2E_VALIDATOR_V1]
```

This occurs when:
- Phase 9 integration tests pass
- Task #25 (E2E testing) is active
- Preparing for production validation

## Worktree Isolation Requirements

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-5-task-1`:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 5 1
cd ./worktrees/phase-5-task-1

# Validate isolation:
./hooks/worktree-enforcer.sh enforce

# E2E validation with isolation
```

### E2E Testing Isolation
1. **Clean E2E environment**: E2E tests run in completely isolated workspace
2. **Workflow isolation**: Each user journey tested without interference
3. **Production readiness assessment**: Scoring done in isolation from other activities
4. **Browser test isolation**: Cross-browser validation isolated per environment
5. **Decision isolation**: Go/No-Go decision based on isolated test results


## What This Skill Does

Automates Phase 10: End-to-end & production validation in isolated worktree

- **E2E workflow testing** (Task 25) in isolated environment
- **Production readiness scoring** (Task 26) with clean assessment
- **Cross-browser validation** without test contamination
- **Mobile viewport testing** in dedicated workspace
- **Go/No-Go decision** based on isolated validation results
- **NEW**: Worktree isolation ensures clean E2E testing environment
- **NEW**: Production validation free from development artifacts

## Execution Flow

```
Stage 1: E2E Workflow Analysis
         - Extract user journeys from PRD
         - Analyze existing E2E tests
         - Calculate coverage gaps
Stage 2: Create Missing E2E Tests
         - Happy paths
         - Error scenarios
         - Cross-browser
         - Mobile viewports
Stage 3: Production Readiness Scoring
         - Testing (30%)
         - Security (25%)
         - Ops (20%)
         - Docs (15%)
         - Stakeholders (10%)
Stage 4: Go/No-Go Decision
         - Score ≥90% → GO
         - Score <90% → NO-GO + remediation plan
Stage 5: Generate Report & Signal
```

## E2E Test Coverage

**Per workflow:**
- ✅ Happy path
- ✅ Error scenarios
- ✅ Edge cases
- ✅ Chrome, Firefox, Safari
- ✅ iOS & Android viewports

## Visual Validation (PRD Section 8.3)

For components with spatial/fusion operations, visual validation is required per PRD Template v2.0 Section 8.3.

### When Visual Tests Are Required

1. PRD Section 8.3 contains visualization definitions
2. Component category is "Spatial Processing" or "Fusion"
3. FRs reference visual validation in acceptance criteria

### Visual Test Structure

Test files follow convention `tests/visual/viz_[feature].py`:
```
tests/visual/
├── viz_[feature]_accuracy.py    # Numerical accuracy validation
├── viz_[feature]_performance.py # Performance target validation
├── viz_[feature]_coverage.py    # Spatial coverage validation
└── output/
    ├── [feature]_accuracy.png
    └── visual-test-results.json
```

### Visual Test Template

Generate visual tests using this pattern:

```python
#!/usr/bin/env python3
"""
Visual validation for FR-XXX-X.X
Generated from PRD Section 8.3
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def visualize_[feature]():
    """
    Validates [requirement description]
    Returns: bool - True if validation passes
    """
    # 1. Generate test data
    test_inputs = np.linspace(0, 10, 100)
    expected_outputs = [...]  # From requirement spec
    actual_outputs = [...]    # From component under test

    # 2. Compute errors
    errors = np.abs(actual_outputs - expected_outputs)
    max_error = np.max(errors)
    threshold = 0.1  # From PRD requirement

    # 3. Create visualization
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Plot 1: Results comparison
    axes[0].plot(test_inputs, expected_outputs, 'b-', label='Expected')
    axes[0].plot(test_inputs, actual_outputs, 'r--', label='Actual')
    axes[0].legend()
    axes[0].set_title('[Feature]: Results Comparison')

    # Plot 2: Error distribution with threshold
    axes[1].hist(errors, bins=50, alpha=0.7)
    axes[1].axvline(x=threshold, color='r', linestyle='--',
                    label=f'Requirement: {threshold}')
    axes[1].legend()
    axes[1].set_title('Error Distribution vs Requirement')

    # 4. Save output
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    plt.savefig(output_dir / "[feature]_validation.png", dpi=150)

    # 5. Determine pass/fail
    passed = np.all(errors < threshold)

    if passed:
        print(f"✅ PASS: All errors below threshold ({threshold})")
    else:
        print(f"❌ FAIL: Max error {max_error:.6f} exceeds threshold")

    return passed

if __name__ == "__main__":
    import sys
    passed = visualize_[feature]()
    sys.exit(0 if passed else 1)
```

### Visual Test Pass/Fail Criteria

| Failure Type | FR Priority | Action |
|--------------|-------------|--------|
| Accuracy violation | SHALL | **BLOCK** deployment |
| Accuracy violation | SHOULD | WARN |
| Performance threshold | SHALL | **BLOCK** deployment |
| Performance threshold | SHOULD | WARN |
| Spatial coverage gap | SHALL | **BLOCK** deployment |
| Infrastructure error | Any | **BLOCK** deployment |

### Visual Test Output

Generate `tests/visual/output/visual-test-results.json`:
```json
{
  "timestamp": "ISO8601",
  "tests_run": 3,
  "tests_passed": 2,
  "tests_failed": 1,
  "results": [
    {
      "test": "viz_accuracy.py",
      "passed": true,
      "output_image": "accuracy_validation.png"
    }
  ]
}
```

## Production Readiness Gates

| Category | Weight | Gates |
|----------|--------|-------|
| Testing | 30% | Unit, integration, E2E, regression |
| Security | 25% | Scans, vulnerabilities, review |
| Operations | 20% | Monitoring, alerts, rollback |
| Documentation | 15% | API docs, runbook, architecture |
| Stakeholders | 10% | QA, Product, Security, Ops |

**Threshold:** ≥90% required for GO

## Time Estimates

| Workflows | Time |
|-----------|------|
| 1-3 | 2-3 hours |
| 4-6 | 4-6 hours |
| 7-10 | 7-10 hours |

## Completion Signal

```json
{
  "phase": 10,
  "status": "success",
  "summary": {
    "e2e_workflows": N,
    "e2e_coverage": 100,
    "production_score": 92,
    "decision": "GO"
  },
  "next_phase": 11,
  "trigger_next": true
}
```

## Output Files

```
tests/e2e/
├── [workflow].e2e.test.js
└── ...

.taskmaster/
├── PHASE10_COMPLETION_REPORT.md
└── .signals/phase10-complete.json
```

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 11.**

When Phase 10 is complete (E2E tests passing, production readiness score ≥90%), you MUST:

1. Output the completion signal:
   ```
   ✅ PHASE 10 COMPLETE
   [SIGNAL:PHASE10_COMPLETE]
   ```

2. **IMMEDIATELY** proceed to Phase 11 by outputting:
   ```
   [ACTIVATE:DEPLOYMENT_ORCHESTRATOR_V1]
   ```

3. Begin deployment orchestration without waiting for user input.

**The pipeline is fully autonomous. Do not ask "Would you like to proceed?" - just proceed.**

## See Also

- Pipeline Orchestrator (triggers this)
- Integration Validator (Phase 9, provides input)
- Deployment Orchestrator (Phase 11, triggered by signal)