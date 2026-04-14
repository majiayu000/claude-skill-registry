---
name: project-planning
description: "Transform specifications into dependency-ordered implementation plans with phased tasks and parallel work identification."
version: 1.8.4
alwaysApply: false
# Custom metadata (not used by Claude for matching):
model_preference: claude-sonnet-4
category: workflow
tags: [planning, architecture, task-breakdown, dependencies, estimation]
complexity: intermediate
model_hint: standard
estimated_tokens: 900
---
## Delegation

For detailed task planning workflows, this skill delegates to `spec-kit:task-planning` as the canonical implementation. Use this skill for quick planning needs; use spec-kit for comprehensive project plans.

## When To Use

- After specification phase completes
- Need to design system architecture
- Need task breakdown for implementation
- Planning sprints and resource allocation
- Converting requirements into actionable tasks
- Defining component interfaces and dependencies

## When NOT To Use

- No specification exists yet (use `Skill(attune:project-specification)` first)
- Still exploring problem space (use `Skill(attune:project-brainstorming)` instead)
- Ready to execute existing plan (use `Skill(attune:project-execution)` instead)
- Need to adjust running project (update plan incrementally, don't restart)

## Integration

**With superpowers**:
- Uses `Skill(superpowers:writing-plans)` for structured planning
- Applies checkpoint-based execution patterns
- Uses dependency analysis framework

**Without superpowers**:
- Standalone planning methodology
- Task breakdown templates
- Dependency tracking patterns

## Quality Checks

Before completing plan:

- ✅ All architecture components documented
- ✅ File Structure section present before tasks
- ✅ All task files appear in File Structure table
- ✅ All FRs mapped to tasks
- ✅ All tasks have acceptance criteria
- ✅ Dependencies are acyclic
- ✅ Effort estimates provided
- ✅ Critical path identified
- ✅ Risks assessed with mitigations
- ✅ Sprints balanced by capacity

## Post-Completion: Workflow Continuation (REQUIRED)

**Automatic Trigger**: After Quality Checks pass and `docs/implementation-plan.md` is saved, MUST auto-invoke the next phase.

**When continuation is invoked**:
1. Verify `docs/implementation-plan.md` exists and is non-empty
2. Display checkpoint message to user:
   ```
   Implementation plan complete. Saved to docs/implementation-plan.md.
   Proceeding to execution phase...
   ```
3. Invoke next phase:
   ```
   Skill(attune:project-execution)
   ```

**Bypass Conditions** (ONLY skip continuation if ANY true):
- `--standalone` flag was provided by the user
- `docs/implementation-plan.md` does not exist or is empty (phase failed)
- User explicitly requests to stop after planning

**Do NOT prompt the user for confirmation** — this is a lightweight checkpoint, not an interactive gate. The user can always interrupt if needed.

## Related Skills

- `Skill(superpowers:writing-plans)` - Planning methodology (if available)
- `Skill(spec-kit:task-planning)` - Task breakdown (if available)
- `Skill(attune:project-specification)` - Previous phase
- `Skill(attune:project-execution)` - **AUTO-INVOKED** next phase after planning
- `Skill(attune:mission-orchestrator)` - Full lifecycle orchestration

## Related Commands

- `/attune:blueprint` - Invoke this skill
- `/attune:execute` - Next step in workflow

## Examples

See `/attune:blueprint` command documentation for complete examples.
## Troubleshooting

### Common Issues

If you find circular dependencies in your task graph, break one of the tasks into smaller sub-tasks. If sprint capacity is consistently exceeded, re-estimate tasks using the Fibonacci scale or reduce sprint scope.
