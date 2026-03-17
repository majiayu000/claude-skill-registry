---
# VERSION: 2.88.0
name: plan
description: "Plan-State Management for Ralph. Create, track, and manage implementation plans with LSA verification"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

# Plan-State Management

Create, track, and manage implementation plans with Lead Software Architect verification.

## Subcommands

### init - Initialize new plan
```
/plan init "Implement user authentication"
```
Creates `.claude/plan-state.json` with:
- Task title, phases, risk level
- File modifications list
- Test strategy
- Validation criteria

### status - Show plan status
```
/plan status
```
Displays:
- Current phase
- Completed vs pending steps
- Overall progress percentage
- Next action required

### add-step - Add implementation step
```
/plan add-step "Create User model with validation"
```
Appends step to phases array with:
- Step description
- Assigned agent/model
- Dependencies
- Validation criteria

### start - Begin implementation
```
/plan start
```
Triggers:
- LSA pre-verification
- Plan-Sync monitoring activation
- First phase execution

### complete - Mark step complete
```
/plan complete --step 2
```
Updates plan-state.json and logs completion in ledger.

### verify - Verify plan completion
```
/plan verify
```
Runs full validation against requirements:
- LSA architecture check
- Quality gate verification
- Requirements coverage

### sync - Synchronize with execution
```
/plan sync
```
Detects drift between plan and execution, patches downstream references.

## Workflow

```
/plan init "Feature description"
  ↓ (creates plan-state.json)
/plan add-step "Step 1"
/plan add-step "Step 2"
  ↓
/plan start
  ↓ (LSA verification)
/plan complete --step 1
/plan complete --step 2
  ↓
/plan verify
  ↓
VERIFIED_DONE
```

## Output Examples

### Plan Status Output
```
========================================
      PLAN STATE: Feature Implementation
========================================
Status: In Progress
Phase: 2/4 - Backend Implementation
Progress: 45%

Steps:
  ✅ 1. Database Schema - COMPLETE
  ⏳ 2. API Endpoints - IN PROGRESS
  🔲 3. Frontend Integration
  🔲 4. Testing & Validation

Next Action: /plan complete --step 2
========================================
```

## Related Skills

- `/orchestrator` - Full orchestration with plan integration
- `/loop` - Iterative execution following plan steps
- `/gates` - Quality validation at plan milestones
- `/retrospective` - Post-completion analysis
