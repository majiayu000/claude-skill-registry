---
name: team-workflow
description: Deterministic team development workflow for Claude Code. Enforces a mandatory
  sequence of phases (Setup → Brainstorm → Plan → Execute → Quality Check → Ship)
  with Linear integration, TDD requirements,
---

---
name: team-workflow
description: Deterministic team development workflow for Claude Code. Enforces a mandatory sequence of phases (Setup → Brainstorm → Plan → Execute → Quality Check → Ship) with Linear integration, TDD requirements, and quality gates. Activates when working on issues/tasks, when user mentions Linear issues (e.g., ENG-123), when starting development work, or when preparing to ship code. Commands: /team:task, /team:quality-check, /team:ship.
---

# Team Workflow Skill

Enforces a deterministic, phase-gated development workflow with Linear integration and quality enforcement.

## Workflow Overview

```
/team:task ENG-123
    ↓
Phase 0: Setup (fetch issue, update status, create branch)
    ↓
Phase 1: Brainstorm (design thinking, post to Linear)
    ↓
Phase 2: Plan (task breakdown, post to Linear)
    ↓
Phase 3: Execute (TDD for every change)
    ↓
Phase 4: Quality Check (/team:quality-check)
    ↓
Phase 5: Ship (/team:ship → PR + Linear update)
```

## Commands

### `/team:task $ISSUE_ID`
Start work on a Linear issue. Enforces all workflow phases.

### `/team:quality-check`
Run all quality gates. Blocks PR creation on failure.

Gates:
- `npm test` - ZERO failures
- `npm run lint` - ZERO errors
- `npm run typecheck` - ZERO errors
- `/code-review` - ZERO high-confidence (≥80%) issues

### `/team:ship`
Create PR, update Linear to "In Review", post PR link.

## Linear Integration

Uses Linear MCP server for:
- `mcp__linear__get_issue` - Fetch issue details
- `mcp__linear__update_issue` - Update status
- `mcp__linear__create_comment` - Post design/plan/PR links

## TDD Requirements

**Every change requires tests first:**
1. Write failing test
2. Implement minimum code to pass
3. Refactor
4. Run tests

There is NO change too small for TDD.

## Quality Gate Zero-Tolerance

All gates must pass with ZERO errors before shipping:
- Tests must all pass
- No lint errors (warnings OK)
- No type errors
- No high-confidence code review issues

## Git Workflow

**Branch naming:** `feat/$ISSUE_ID-slugified-title`

**Commit format:**
```
feat(ENG-123): brief description

- Main change
- Secondary change

Closes ENG-123
```

## Hooks

The plugin includes hooks that:
- Format files on save (Prettier)
- Run tests/lint before push
- Verify quality before stopping

## Integration with Superpowers

Phases 1-3 integrate with the Superpowers plugin:
- Brainstorm phase uses Superpowers design thinking
- Plan phase uses Superpowers task breakdown
- Execute phase uses Superpowers TDD enforcement
