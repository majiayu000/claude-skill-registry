---
name: agent-teams
description: Coordinate specialized teammates in Agent Teams for execution, review, and planning. Delegate mode mandatory with TaskCompleted/TeammateIdle hooks.
---

# SKILL: Agent Teams

> **Purpose**: Native Claude Code Agent Teams coordination with team templates and quality gates
> **Target**: Team Leads coordinating execution-team, review-team, planning-team

---

## Quick Start

### When to Use
- Execute SCs with specialized agents (coder, frontend-engineer, backend-engineer)
- Multi-angle review with cross-discussion
- Parallel exploration and research

### Quick Reference
```markdown
# Spawn teammate for SC implementation
Spawn teammate "sc1-impl" with prompt:
  "You are a coder (see @.claude/agents/coder.md).
  Execute SC-1 from $PLAN_PATH. Skills: tdd, ralph-loop, vibe-coding.
  When complete, mark task as done. If blocked, message the team lead."

# Delegate mode (Shift+Tab): coordinate only, never implement
# TaskCompleted hook auto-verifies tests/coverage/todos
```

---

## What This Skill Covers

### In Scope
- Agent Teams coordination patterns
- Team templates (execution, review, planning)
- Teammate spawning with role-specific prompts
- TaskCompleted and TeammateIdle hook integration

### Out of Scope
- Hook implementation details → @.claude/hooks/verify-task-completion.sh
- Individual agent definitions → @.claude/agents/
- Test frameworks and coverage → @.claude/skills/tdd/SKILL.md

---

## Core Concepts

### Architecture
- **Team Lead**: Coordinates in delegate mode (Shift+Tab), never implements directly
- **Teammates**: Independent agents, full context, direct communication, shared Task List
- **Quality Gates**: TaskCompleted hook (auto-verify), TeammateIdle hook (prevent premature idle)
- **Communication**: Multi-directional (teammate ↔ teammate ↔ lead)

### Delegate Mode (MANDATORY)
Team Lead MUST coordinate only (spawn teammates, monitor, aggregate) and NEVER implement (edit files, write tests).

**Pattern**: Spawn → Monitor → Handle messages → Aggregate

### Team Templates
1. **execution-team**: SC implementation (coder, frontend-engineer, backend-engineer)
2. **review-team**: Multi-angle review (tester, validator, code-reviewer, security-analyst)
3. **planning-team**: Exploration/research (explorer, researcher)

---

## Team Templates

### execution-team

**Purpose**: Implement SCs with specialized agents (coder, frontend-engineer, backend-engineer)

**Spawn Pattern**:
```markdown
Spawn teammate "sc1-impl" with prompt:
  "You are a [role] (see @.claude/agents/[role].md).
  Execute SC-1: [description] from $PLAN_PATH. Skills: tdd, ralph-loop, vibe-coding.
  When complete, mark done. If blocked, message team lead."
```

**Coordination**: Parallel (independent SCs) / Sequential (dependent SCs) / Blocked → GPT delegation

**Quality Gates**: Tests pass, coverage ≥80%, todos checked (TaskCompleted hook)

### review-team

**Purpose**: Multi-angle review with cross-discussion (tester, validator, code-reviewer, security-analyst, design-reviewer)

**Spawn Pattern**:
```markdown
Spawn teammate "test-reviewer" with prompt:
  "You are a tester (see @.claude/agents/tester.md).
  Review test coverage for $PLAN_PATH.
  Evaluate: completeness, coverage ≥80%, verification commands.
  Discuss findings with other reviewers via Message.
  Output: PASS or FAIL with details."
```

**Key Enhancement**: Reviewers cross-reference and debate findings via direct messaging

**Quality Gates**: All PASS required, any FAIL blocks completion

### planning-team

**Purpose**: Parallel exploration/research for plan creation (explorer, researcher)

**Spawn Pattern**:
```markdown
Spawn teammate "codebase-explorer" with prompt:
  "You are an explorer (see @.claude/agents/explorer.md).
  Explore codebase for [domain] related to [task].
  Find: files, patterns, config, tests. Share findings via Message.
  Output: File list with descriptions."

Spawn teammate "docs-researcher" with prompt:
  "You are a researcher (see @.claude/agents/researcher.md).
  Research external docs for [task].
  Find: official docs, best practices, security. Share findings via Message.
  Output: Research summary with links."
```

**Coordination**: Teammates share findings, lead synthesizes for plan

---

## Quality Gates

### TaskCompleted Hook
**Trigger**: Teammate marks task done
**Verification**: `.claude/hooks/verify-task-completion.sh` checks tests pass, coverage ≥80%, todos checked
**Result**: Exit 0 (allow) / Exit 2 (reject with feedback)

### TeammateIdle Hook
**Trigger**: Teammate attempts idle
**Check**: `.claude/hooks/teammate-idle-check.sh` verifies SC complete and quality gates pass
**Purpose**: Prevent premature idle

---

## Environment Setup

**Required**: `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json env
**Hooks**: Register TaskCompleted and TeammateIdle in settings.json (see REFERENCE.md)
**Terminal**: tmux/iTerm2 for split-pane (recommended), in-process works in all terminals

---

## Further Reading

**Internal**: @.claude/skills/agent-teams/REFERENCE.md - Full teammate spawn templates, hook examples, before/after comparison | @.claude/agents/CONTEXT.md - Agent ecosystem | @.claude/skills/parallel-subagents/SKILL.md - Dependency analysis patterns | @.claude/skills/tdd/SKILL.md - Test-driven development | @.claude/skills/ralph-loop/SKILL.md - Autonomous iteration

**External**: [Claude Code Agent Teams Documentation](https://docs.anthropic.com/claude-code/agent-teams)

---

**Version**: claude-pilot 5.0.0
