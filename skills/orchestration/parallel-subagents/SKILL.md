---
name: parallel-subagents
description: Use when executing independent tasks concurrently. Launch multiple agents simultaneously for 50-70% speedup.
---

# SKILL: Parallel Subagents

> **Purpose**: Concurrent agent execution for independent tasks, 50-70% speedup
> **Target**: Orchestrators executing multiple independent SCs/tasks

---

## Quick Start

### When to Use This Skill
- Multiple independent SCs (no shared files, no dependencies)
- Independent code changes (different files/directories)
- Parallel verification (testing, type-check, linting)
- Multi-angle review (codereviewer, security-analyst in parallel)

### Quick Reference
```markdown
# Use per-SC dynamically selected agent type (from execute-plan Step 3)
Task:
  subagent_type: $SC_AGENT
  prompt: Implement SC-1: Create authentication service

Task:
  subagent_type: $SC_AGENT
  prompt: Implement SC-2: Create user service

Task:
  subagent_type: $SC_AGENT
  prompt: Implement SC-3: Create database migrations
```

**Note**: `$SC_AGENT` is selected per-SC (not per-plan) in execute-plan Step 3 based on each SC's file paths and keywords. Different SCs may use different specialized agents (e.g., SC-1 → frontend-engineer, SC-2 → backend-engineer).

### ⚠️ What "Parallel" Means (CRITICAL)

**Parallel = Multiple Task calls in SAME response**:
```markdown
# ✅ TRUE PARALLEL (single response, multiple Task calls)
Task: subagent_type: coder, prompt: "Execute SC-1..."
Task: subagent_type: coder, prompt: "Execute SC-2..."
Task: subagent_type: coder, prompt: "Execute SC-3..."
```

**Sequential = One Task per response (loop dispatch)**:
```markdown
# ❌ NOT PARALLEL (even if called "parallel")
for SC in $SC_LIST; do
    Task: subagent_type: coder, prompt: "Execute $SC..."
done
```

**If platform cannot true-parallelize**: Rename to "batched delegation" (do not claim parallelism)

## Core Concepts

### Parallel Execution Patterns

**Pattern 1: Independent SCs**
```markdown
Task: subagent_type: explorer, prompt: Search for auth patterns
Task: subagent_type: explorer, prompt: Search for database patterns
Task: subagent_type: explorer, prompt: Search for API patterns
```

**Pattern 2: Parallel Verification**
```markdown
Task: subagent_type: tester, prompt: Run tests and verify coverage
Task: subagent_type: validator, prompt: Run type check and lint
Task: subagent_type: code-reviewer, prompt: Review for async bugs
```

**Pattern 3: Multi-Angle Review**
```markdown
Task: subagent_type: plan-reviewer, prompt: Review plan completeness
Task: subagent_type: code-reviewer, prompt: Review code quality
Task: subagent_type: security-analyst, prompt: Review security issues
```

### Dependency Analysis

**Before launching parallel agents**, check for conflicts:

1. **File Overlap**: Do SCs mention same files?
2. **Dependency Keywords**: "after", "depends", "requires", "follows"
3. **ParallelGroup Annotation**: Group independent SCs in plan

### Coordination

**Result Integration**:
- Wait for all parallel agents to complete
- Check for file conflicts (rare if analysis correct)
- Update todos atomically (all parallel items together)

**Performance**: 50-70% faster for independent tasks

## Anti-Patterns

**Don't parallelize**:
- Tasks with shared file modifications (causes merge conflicts)
- Tasks with dependencies (later task will fail)
- Sequential workflows (e.g., build then test)

## Test Execution Concurrency

**Critical**: Multiple tester agents in parallel can cause worker explosion (6 agents × 16 workers = 96 processes, Load 85+)

**Pattern**: Test type-aware concurrency
- **E2E/Integration**: Sequential execution (one at a time)
- **Unit/Lint/Type**: Parallel allowed with `--maxWorkers=50%`

**Detection** (from `execute-plan` Step 3):
- Path: `**/e2e/**`, `**/integration/**`, `**/*.e2e.*`
- Keywords: "e2e", "integration", "playwright", "cypress"
- Fail-safe: Unknown → `unit` (parallel with worker limit)

**Implementation**: `@.claude/agents/tester.md` applies `--maxWorkers=50%` (Jest) or `--workers=1` (Playwright E2E)

**Full examples**: See `@.claude/skills/parallel-subagents/REFERENCE.md#test-execution-concurrency`

## Single Agent Delegation Pattern

### When to Use
- Single SC execution (no parallelism needed)
- Sequential workflow steps
- Context protection for main orchestrator

### Why Delegate Single Tasks

Main orchestrator context is limited (~200K tokens). By delegating:
- Subagent runs in isolated context (~80K tokens internally)
- Returns concise summary (~1K tokens) to orchestrator
- Orchestrator maintains clean context for coordination

### Pattern

```markdown
Task:
  subagent_type: [agent-type]
  prompt: |
    [Clear task description with all context needed]
    Skills to use: [skill1, skill2]
    Expected output: <MARKER_COMPLETE> or <MARKER_BLOCKED>
```

### Examples

**Single Coder Delegation**:
```markdown
Task:
  subagent_type: coder
  prompt: |
    Execute SC-1: Create authentication service
    Skills to use: tdd, ralph-loop, vibe-coding
    Expected output: <CODER_COMPLETE> or <CODER_BLOCKED>
```

**Single Plan-Reviewer Delegation**:
```markdown
Task:
  subagent_type: plan-reviewer
  prompt: |
    Review plan at $PLAN_FILE for gaps and issues
    Review criteria: requirements coverage, success criteria clarity
    Expected output: <PLAN_COMPLETE> or <PLAN_BLOCKED>
```

**Single Documenter Delegation**:
```markdown
Task:
  subagent_type: documenter
  prompt: |
    Invoke the three-tier-docs skill to sync documentation
    Project root: $PROJECT_ROOT
    Expected output: <DOCS_COMPLETE> or <DOCS_BLOCKED>
```

## Verification

```bash
# Launch 3 independent tasks
Task: subagent_type: explorer, prompt: Find TypeScript files
Task: subagent_type: explorer, prompt: Find test files
Task: subagent_type: explorer, prompt: Find config files

# Verify all complete, no conflicts
```

## Further Reading

**Internal**: @.claude/skills/parallel-subagents/REFERENCE.md - Detailed dependency analysis, command-specific patterns, coordination examples | @.claude/skills/using-git-worktrees/SKILL.md - Parallel development in isolated worktrees

**External**: None
