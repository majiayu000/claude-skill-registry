---
name: execute-plan
description: Plan execution workflow - parallel SC implementation, worktree mode, verification patterns, GPT delegation. Use for executing plans with TDD + Ralph Loop.
---

# SKILL: Execute Plan (Plan Execution Workflow)

> **Purpose**: Execute plans using TDD + Ralph Loop with parallel execution
> **Target**: Coder Agent implementing Success Criteria from plans

**When to Use**: Execute plans from `/01_confirm`, implement SCs with TDD, parallel execution of independent SCs, worktree mode for isolated development

**Quick Reference**:
```bash
PROJECT_ROOT="$(pwd)"
PLAN_PATH="$(find "$PROJECT_ROOT/.pilot/plan/pending" "$PROJECT_ROOT/.pilot/plan/in_progress" -name "*.md" -type f 2>/dev/null | sort | head -1)"

# Spawn teammate for SC execution
Spawn teammate "sc1-impl" with prompt: "You are a coder (see agents/coder.md).
Execute SC-1 from $PLAN_PATH. Skills: tdd, ralph-loop, vibe-coding.
Mark task done when complete. Message lead if blocked."
```

**Scope**: Plan detection, SC dependency analysis, parallel execution, worktree mode, GPT delegation. Team Lead operates in delegate mode (coordinate only, never implement). TDD/Ralph/Vibe → teammate skills.

---

## Execution Steps

**⚠️ EXECUTION DIRECTIVE**: Execute ALL steps IMMEDIATELY. NEVER move plan to done/ (only `/03_close` has this authority), do NOT call close-plan automatically, plan MUST remain in `.pilot/plan/in_progress/`

**Team Lead Role**: Operate in delegate mode (Shift+Tab). Coordinate teammates, never implement code directly. Spawn teammates for all SC execution.

---

## Step 1: Plan Detection & SC Extraction

**⚠️ CRITICAL**: Always use absolute path based on Claude Code's initial working directory.

**Full Implementation**: See @REFERENCE.md - Step 1: Plan Detection (Full Bash)

---

## Step 2.7: Pre-Execution Confidence

**Purpose**: Evaluate confidence before complex SCs. If < 0.5 → consult GPT Architect (rubric: @.claude/skills/gpt-delegation/SKILL.md).

**Full Implementation**: See @REFERENCE.md - Step 2.7: Pre-Execution Confidence (Full Bash)

---

## Step 3: Execute with Ralph Loop (Per-SC Agent Selection)

**Dependency Analysis, File Extraction & Agent Selection** (supports both `### SC-N:` and `- [ ] **SC-N**` formats):

**Full Implementation**: See @REFERENCE.md - Step 3: Dependency Analysis (Full Bash)

**Test Type Detection Rules**: Path-based (`**/e2e/**`, `**/integration/**`, `**/*.e2e.*`) + Keyword-based (e2e, integration, playwright, cypress) + Script-based (package.json script name). **Fail-Safe**: Defaults to `unit` (parallel allowed, safe with `--maxWorkers=50%` from SC-1). **Routing**: `e2e` → Sequential (environment-bound, stateful), `unit` → Parallel allowed.

**Smart Grouping**: When SCs follow Atomic SC Principle (@.claude/skills/spec-driven-workflow/SKILL.md), parallel execution naturally emerges. SCs modifying same file type automatically group for specialized agents (e.g., frontend-engineer for `src/components/*`, backend-engineer for `src/api/*`). Test type detection automatically groups E2E SCs sequentially (path: `**/e2e/**`, `**/integration/**`, `**/*.e2e.*`; keywords: e2e, integration, playwright, cypress).

**Execution Strategies**:
- **Parallel** (Independent SCs, 50-70% speedup): Spawn multiple teammates simultaneously
  ```
  Spawn teammate "sc{N}-impl" (role: $SC_AGENT) with prompt:
  "You are a $SC_AGENT (see agents/$SC_AGENT.md).
  Execute SC-{N} from $PLAN_PATH.
  Skills to use: tdd, ralph-loop, vibe-coding.
  Mark task done when complete. Message lead if blocked."
  ```
- **Sequential** (Dependent SCs): Spawn teammates with dependency ordering
- **Single Teammate** (1-2 SCs): Spawn one teammate with all SCs

**Note**: `$SC_AGENT` is selected per-SC (not per-plan), so parallel SCs may use different specialized teammates (e.g., SC-1 → frontend-engineer, SC-2 → backend-engineer).

**Process Results**: TaskCompleted hook auto-verifies tests pass, coverage ≥80%, type-check clean, lint clean. Quality Gates enforced automatically.

**Handle CODER_BLOCKED**: Teammate messages Team Lead → Team Lead delegates to GPT Architect (gpt-5.2, workspace-write, reasoning_effort=medium). Fallback: Continue with Claude.

```bash
# Teammate messages Team Lead when blocked
# Team Lead delegates to GPT Architect
if command -v codex &> /dev/null; then
    codex exec -m gpt-5.2 -s workspace-write -c reasoning_effort=medium --json "$ARCHITECT_PROMPT"
fi
```

**TaskCompleted Hook Integration**: verify-task-completion.sh runs automatically when teammate marks task done. Checks: tests pass, coverage ≥80%, TODOs checked. Exit 0 allows completion, Exit 2 rejects with feedback.

**No-Excuses Enforcement**: PROHIBITED phrases ("I cannot", "Too complex", "Out of scope"). Required pattern: "To achieve X, I will: [alternative]" or "Breaking down into: [steps]". Exception: User explicit abort only. Details: @REFERENCE.md

**Mandatory Oracle Consultation** (mandatory_oracle_consultation): Per-SC execution (GPT Role: Engineer), Blocker resolution (GPT Role: Problem Solver). Pattern: `codex exec -m gpt-5.2 -s read-only -c reasoning_effort=medium`. Graceful fallback if unavailable. Full table: @REFERENCE.md

**No-Partial-Delivery Policy**: No "simplified version", "basic implementation", "you can extend later". On BLOCKED: 1) GPT delegation, 2) User collaboration (not "give up"). All SCs must be fully completed.

---

## Step 3.5: Per-SC TODO Verification (BLOCKING)

After each SC execution, TaskCompleted hook verifies all TODO checkboxes are marked `[x]`. If unchecked items remain, hook rejects completion (Exit 2) until teammate completes them. Full implementation: @REFERENCE.md - Per-SC TODO Verification

---

## Step 3.9: Final TODO Sweep (BLOCKING)

Before E2E verification, Team Lead verifies entire plan for unchecked TODOs. If any remain, spawn verification teammate. Max 50 retries with GPT escalation at 10, user escalation at 50. Full implementation: @REFERENCE.md - Final TODO Sweep

---

## Step 4: Completion & E2E Verification

All SCs complete → E2E verification. Detect project type: Web (Chrome in Claude), CLI (exit code/stdout), Library (tests). Retry max 3 → GPT → user. Full: @REFERENCE.md

---

## Further Reading

**Internal**: @.claude/skills/execute-plan/REFERENCE.md | @.claude/skills/tdd/SKILL.md | @.claude/skills/ralph-loop/SKILL.md | @.claude/skills/gpt-delegation/SKILL.md

**External**: [Test-Driven Development](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) | [Working Effectively with Legacy Code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)

---

**Version**: claude-pilot 4.4.14
