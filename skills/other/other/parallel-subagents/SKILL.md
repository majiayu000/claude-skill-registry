---
name: parallel-subagents
description: Coordinate independent teammates concurrently in Agent Teams for 50-70% speedup. Launch multiple teammates simultaneously.
---

# SKILL: Parallel Teammates (Agent Teams Coordination)

> **Purpose**: Concurrent teammate execution for independent tasks, 50-70% speedup
> **Target**: Team Leads coordinating multiple independent SCs/tasks in Agent Teams

---

## Quick Start

### When to Use This Skill
- Multiple independent SCs (no shared files, no dependencies)
- Independent code changes (different files/directories)
- Parallel verification (testing, type-check, linting)
- Multi-angle review (code-reviewer, security-analyst in parallel)

### Quick Reference
```markdown
# Spawn teammates for independent SCs (from execute-plan Step 3)
Spawn teammate "sc1-impl" with prompt:
  "You are a $SC_AGENT. Execute SC-1: Create authentication service.
  Skills: tdd, ralph-loop, vibe-coding. Mark task done when complete."

Spawn teammate "sc2-impl" with prompt:
  "You are a $SC_AGENT. Execute SC-2: Create user service.
  Skills: tdd, ralph-loop, vibe-coding. Mark task done when complete."

Spawn teammate "sc3-impl" with prompt:
  "You are a $SC_AGENT. Execute SC-3: Create database migrations.
  Skills: tdd, ralph-loop, vibe-coding. Mark task done when complete."
```

**Note**: `$SC_AGENT` is selected per-SC (not per-plan) in execute-plan Step 3 based on each SC's file paths and keywords. Different SCs may use different specialized agents (e.g., SC-1 → frontend-engineer, SC-2 → backend-engineer).

### ⚠️ What "Parallel" Means (CRITICAL)

**Parallel = Multiple teammates spawned simultaneously in Agent Team**:
```markdown
# ✅ TRUE PARALLEL (single response, multiple Spawn calls)
Spawn teammate "sc1-impl" with prompt: "Execute SC-1..."
Spawn teammate "sc2-impl" with prompt: "Execute SC-2..."
Spawn teammate "sc3-impl" with prompt: "Execute SC-3..."
```

**Sequential = One teammate per response (loop dispatch)**:
```markdown
# ❌ NOT PARALLEL (even if called "parallel")
for SC in $SC_LIST; do
    Spawn teammate "impl-$SC" with prompt: "Execute $SC..."
done
```

**Team Lead delegate mode**: Coordinate only (Shift+Tab), never implement directly

## Core Concepts

### Parallel Execution Patterns

**Pattern 1: Independent SCs**
```markdown
Spawn teammate "explore-auth" with prompt:
  "You are an explorer. Search for auth patterns. Share findings via Message."

Spawn teammate "explore-db" with prompt:
  "You are an explorer. Search for database patterns. Share findings via Message."

Spawn teammate "explore-api" with prompt:
  "You are an explorer. Search for API patterns. Share findings via Message."
```

**Pattern 2: Parallel Verification**
```markdown
Spawn teammate "test-reviewer" with prompt:
  "You are a tester. Run tests and verify coverage. Mark task done when complete."

Spawn teammate "quality-reviewer" with prompt:
  "You are a validator. Run type check and lint. Mark task done when complete."

Spawn teammate "deep-reviewer" with prompt:
  "You are a code-reviewer (Opus). Review for async bugs. Mark task done when complete."
```

**Pattern 3: Multi-Angle Review**
```markdown
Spawn teammate "plan-review" with prompt:
  "You are a plan-reviewer. Review plan completeness. Message other reviewers with findings."

Spawn teammate "code-review" with prompt:
  "You are a code-reviewer. Review code quality. Message other reviewers with findings."

Spawn teammate "security-review" with prompt:
  "You are a security-analyst. Review security issues. Message other reviewers with findings."
```

### Dependency Analysis

**Before launching parallel teammates**, check for conflicts:

1. **File Overlap**: Do SCs mention same files?
2. **Dependency Keywords**: "after", "depends", "requires", "follows"
3. **ParallelGroup Annotation**: Group independent SCs in plan

### Coordination

**Result Integration**:
- Wait for all parallel teammates to complete (TaskCompleted hook auto-verifies)
- Check for file conflicts (rare if analysis correct)
- Aggregate results from completed teammates

**Performance**: 50-70% faster for independent tasks

## Anti-Patterns

**Don't parallelize**:
- Tasks with shared file modifications (causes merge conflicts)
- Tasks with dependencies (later task will fail)
- Sequential workflows (e.g., build then test)

## Test Execution Concurrency

**Critical**: Multiple tester teammates in parallel can cause worker explosion (6 teammates × 16 workers = 96 processes, Load 85+)

**Pattern**: Test type-aware concurrency
- **E2E/Integration**: Sequential execution (E2E sequential, one at a time)
- **Unit/Lint/Type**: Parallel allowed with `--maxWorkers=50%` (unit parallel)

**Detection** (from `execute-plan` Step 3):
- Path: `**/e2e/**`, `**/integration/**`, `**/*.e2e.*`
- Keywords: "e2e", "integration", "playwright", "cypress"
- Fail-safe: Unknown → `unit` (parallel with worker limit)

**Implementation**: `@.claude/agents/tester.md` applies `--maxWorkers=50%` (Jest) or `--workers=1` (Playwright E2E)

**Full examples**: See `@.claude/skills/parallel-subagents/REFERENCE.md#test-execution-concurrency`

## Single Teammate Delegation Pattern

### When to Use
- Single SC execution (no parallelism needed)
- Sequential workflow steps
- Context protection for Team Lead

### Why Delegate Single Tasks

Team Lead context is limited (~200K tokens). By delegating:
- Teammate runs in isolated context (~80K tokens internally)
- Returns concise summary (~1K tokens via Task List)
- Team Lead maintains clean context for coordination

### Pattern

```markdown
Spawn teammate "[role-name]" with prompt:
  """
  You are a [agent-type] (see @.claude/agents/[agent-type].md).
  [Clear task description with all context needed]
  Skills to use: [skill1, skill2]
  When complete, mark task as done. If blocked, message the team lead.
  """
```

### Examples

**Single Coder Delegation**:
```markdown
Spawn teammate "sc1-impl" with prompt:
  """
  You are a coder (see @.claude/agents/coder.md).
  Execute SC-1: Create authentication service from $PLAN_PATH.
  Skills to use: tdd, ralph-loop, vibe-coding.
  When complete, mark task as done. If blocked, message the team lead.
  """
```

**Single Plan-Reviewer Delegation**:
```markdown
Spawn teammate "plan-review" with prompt:
  """
  You are a plan-reviewer (see @.claude/agents/plan-reviewer.md).
  Review plan at $PLAN_FILE for gaps and issues.
  Review criteria: requirements coverage, success criteria clarity.
  When complete, mark task as done. If blocked, message the team lead.
  """
```

**Single Documenter Delegation**:
```markdown
Spawn teammate "doc-sync" with prompt:
  """
  You are a documenter (see @.claude/agents/documenter.md).
  Invoke the three-tier-docs skill to sync documentation.
  Project root: $PROJECT_ROOT.
  When complete, mark task as done. If blocked, message the team lead.
  """
```

## Verification

```bash
# Launch 3 independent teammates
Spawn teammate "find-ts" with prompt: "You are an explorer. Find TypeScript files."
Spawn teammate "find-tests" with prompt: "You are an explorer. Find test files."
Spawn teammate "find-config" with prompt: "You are an explorer. Find config files."

# Team Lead operates in delegate mode (Shift+Tab)
# TaskCompleted hook auto-verifies quality gates
# Shared Task List shows completion status
```

## Further Reading

**Internal**: @.claude/skills/parallel-subagents/REFERENCE.md - Detailed dependency analysis, command-specific patterns, coordination examples | @.claude/skills/agent-teams/SKILL.md - Agent Teams core concepts | @.claude/skills/using-git-worktrees/SKILL.md - Parallel development in isolated worktrees

**External**: None
