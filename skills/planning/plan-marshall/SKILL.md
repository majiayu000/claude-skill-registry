---
name: plan-marshall
description: Unified plan lifecycle management - create, outline, execute, verify, and finalize plans
user-invocable: true
allowed-tools: Read, Skill, Bash, AskUserQuestion, Task
---

# Plan Marshall Skill

Unified entry point for plan lifecycle management covering all 7 phases.

**CRITICAL: DO NOT USE CLAUDE CODE'S BUILT-IN PLAN MODE**

This skill implements its **OWN** plan system. You must:

1. **NEVER** use `EnterPlanMode` or `ExitPlanMode` tools
2. **IGNORE** any system-reminder about `.claude/plans/` paths
3. **ONLY** use plans via `pm-workflow:manage-*` skills

## 7-Phase Model

```
1-init -> 2-refine -> 3-outline -> 4-plan -> 5-execute -> 6-verify -> 7-finalize
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | optional | Explicit action: `list`, `init`, `outline`, `execute`, `verify`, `finalize`, `cleanup`, `lessons` (default: list) |
| `task` | optional | Task description for creating new plan |
| `issue` | optional | GitHub issue URL for creating new plan |
| `lesson` | optional | Lesson ID to convert to plan |
| `plan` | optional | Plan name for specific operations (e.g., `jwt-auth`, not path) |
| `stop-after-init` | optional | If true, stop after 1-init phase without continuing to 2-refine (default: false) |

**Note**: The `plan` parameter accepts the plan **name** (plan_id) only, not the full path.

## Workflow

### Action Routing

Route based on action parameter. Load the appropriate workflow document and follow its instructions:

| Action | Workflow Document | Description |
|--------|-------------------|-------------|
| `list` (default) | `Read workflows/planning.md` | List all plans |
| `init` | `Read workflows/planning.md` | Create new plan, auto-continue to refine |
| `outline` | `Read workflows/planning.md` | Run outline and plan phases |
| `cleanup` | `Read workflows/planning.md` | Remove completed plans |
| `lessons` | `Read workflows/planning.md` | List and convert lessons |
| `execute` | `Read workflows/execution.md` | Execute implementation tasks |
| `verify` | `Read workflows/execution.md` | Run quality verification |
| `finalize` | `Read workflows/execution.md` | Commit, push, PR |

### Auto-Detection (plan parameter without action)

When `plan` is specified but no `action`, auto-detect from plan phase:

```bash
python3 .plan/execute-script.py pm-workflow:plan-marshall:manage-lifecycle get-routing-context \
  --plan-id {plan_id}
```

| Current Phase | Workflow Document | Action |
|---------------|-------------------|--------|
| 1-init | `Read workflows/planning.md` | `init` |
| 2-refine | `Read workflows/planning.md` | `init` (continues refine) |
| 3-outline | `Read workflows/planning.md` | `outline` |
| 4-plan | `Read workflows/planning.md` | `outline` (continues plan) |
| 5-execute | `Read workflows/execution.md` | `execute` |
| 6-verify | `Read workflows/execution.md` | `verify` |
| 7-finalize | `Read workflows/execution.md` | `finalize` |

### Execution

After determining the action and workflow document:

1. **Read** the workflow document (`workflows/planning.md` or `workflows/execution.md`)
2. **Navigate** to the section for the resolved action
3. **Follow** the workflow instructions in that section

## Usage Examples

```bash
# List all plans (interactive selection)
/plan-marshall

# Create new plan from task description
/plan-marshall action=init task="Add user authentication"

# Create new plan from GitHub issue
/plan-marshall action=init issue="https://github.com/org/repo/issues/42"

# Create plan but stop after 1-init
/plan-marshall action=init task="Complex feature" stop-after-init=true

# Outline specific plan
/plan-marshall action=outline plan="user-auth"

# Execute specific plan
/plan-marshall action=execute plan="jwt-auth"

# Run verification
/plan-marshall action=verify plan="jwt-auth"

# Finalize (commit, PR)
/plan-marshall action=finalize plan="jwt-auth"

# Auto-detect: continues from current phase
/plan-marshall plan="jwt-auth"

# Cleanup completed plans
/plan-marshall action=cleanup

# List lessons and convert to plan
/plan-marshall action=lessons
```

## Continuous Improvement

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with component: `{type: "skill", name: "plan-marshall", bundle: "pm-workflow"}`

## Related

| Skill | Purpose |
|-------|---------|
| `pm-workflow:phase-1-init` | Init phase implementation |
| `pm-workflow:phase-3-outline` | Outline phase implementation |
| `pm-workflow:phase-6-verify` | Verify phase implementation |
| `pm-workflow:phase-7-finalize` | Finalize phase implementation |
| `pm-workflow:workflow-extension-api` | Extension points for domain customization |

| Agent | Purpose |
|-------|---------|
| `pm-workflow:phase-init-agent` | Init phase: creates plan, detects domains |
| `pm-workflow:task-plan-agent` | Plan phase: creates tasks from deliverables |
| `pm-dev-java:java-implement-agent` | Java task implementation |
| `pm-dev-frontend:js-implement-agent` | JavaScript task implementation |
