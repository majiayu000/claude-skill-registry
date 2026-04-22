---
name: project-specification
description: "Transform project briefs into testable specifications with user stories, acceptance criteria, and measurable outcomes."
version: 1.9.0
alwaysApply: false
# Custom metadata (not used by Claude for matching):
model_preference: claude-sonnet-4
category: workflow
tags: [specification, requirements, acceptance-criteria, spec-driven-development]
complexity: intermediate
model_hint: standard
estimated_tokens: 800
---
## Delegation

For detailed specification writing workflows, this skill delegates to `spec-kit:spec-writing` as the canonical implementation. Use this skill for quick specification needs; use spec-kit for comprehensive specification documents.

## When To Use

- After brainstorming phase completes
- Have project brief but need detailed requirements
- Need testable acceptance criteria for implementation
- Planning validation and testing strategy
- Translating business requirements into technical specs
- Defining scope boundaries and out-of-scope items

## When NOT To Use

- Still exploring problem space (use `Skill(attune:project-brainstorming)` instead)
- Already have detailed specification (use `Skill(attune:project-planning)` instead)
- Refining existing implementation (use code review skills)
- Making strategic decisions (use `Skill(attune:war-room)` for complex choices)

## Integration

**With spec-kit**:
- Delegates to `Skill(spec-kit:spec-writing)` for methodology
- Uses spec-kit templates and validation
- Enables clarification workflow

**Without spec-kit**:
- Standalone specification framework
- Requirement templates
- Acceptance criteria patterns

## Post-Completion: Workflow Continuation (REQUIRED)

**Automatic Trigger**: After Quality Checks pass and `docs/specification.md` is saved, MUST auto-invoke the next phase.

**When continuation is invoked**:
1. Verify `docs/specification.md` exists and is non-empty
2. Display checkpoint message to user:
   ```
   Specification complete. Saved to docs/specification.md.
   Proceeding to planning phase...
   ```
3. Invoke next phase:
   ```
   Skill(attune:project-planning)
   ```

**Bypass Conditions** (ONLY skip continuation if ANY true):
- `--standalone` flag was provided by the user
- `docs/specification.md` does not exist or is empty (phase failed)
- User explicitly requests to stop after specification

**Do NOT prompt the user for confirmation** — this is a lightweight checkpoint, not an interactive gate. The user can always interrupt if needed.

## Related Skills

- `Skill(spec-kit:spec-writing)` - Spec-kit methodology (if available)
- `Skill(attune:project-brainstorming)` - Previous phase
- `Skill(attune:project-planning)` - **AUTO-INVOKED** next phase after specification
- `Skill(attune:mission-orchestrator)` - Full lifecycle orchestration

## Related Commands

- `/attune:specify` - Invoke this skill
- `/attune:specify --clarify` - Run clarification workflow
- `/attune:blueprint` - Next step in workflow

## Examples

See `/attune:specify` command documentation for complete examples.
