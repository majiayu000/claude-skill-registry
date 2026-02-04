---
activation_code: E2E_VALIDATOR_V1
phase: 10
prerequisites:
  - Integration tests passing
outputs:
  - E2E test results
  - .signals/phase10-complete.json
  - Go/No-Go decision
description: |
  Validates end-to-end user workflows and system behavior.
  Activates via codeword [ACTIVATE:E2E_VALIDATOR_V1] injected by hooks
  when entering Phase 10 E2E testing.
  
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

**CRITICAL**: This skill MUST operate in a dedicated worktree `phase-10-task-1`:

```bash
# Before skill activation:
./lib/worktree-manager.sh create 5 1
cd ./worktrees/phase-10-task-1

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

Automates Phase 5: End-to-end & production validation in isolated worktree

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
  "phase": 5,
  "status": "success",
  "summary": {
    "e2e_workflows": N,
    "e2e_coverage": 100,
    "production_score": 92,
    "decision": "GO"
  },
  "next_phase": 6,
  "trigger_next": true
}
```

## Output Files

```
tests/e2e/
├── [workflow].e2e.test.js
└── ...

.taskmaster/
├── PHASE5_COMPLETION_REPORT.md
└── .signals/phase10-complete.json
```

## CRITICAL: Automatic Phase Transition

**DO NOT ASK THE USER FOR PERMISSION TO PROCEED TO PHASE 6.**

When Phase 10 is complete (E2E tests passing, production readiness score ≥90%), you MUST:

1. Output the completion signal:
   ```
   ✅ PHASE 5 COMPLETE
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
- Integration Validator (Phase 4, provides input)
- Deployment Orchestrator (Phase 11, triggered by signal)