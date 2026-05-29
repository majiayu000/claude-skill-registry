---
name: codex-safe-experiment
description: Use Codex CLI sandbox mode to try risky changes safely. Isolated experimentation with network disabled and directory restrictions.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
x-version: 1.0.0
x-category: platforms
x-tags:
  - codex
  - sandbox
  - experimentation
  - multi-model
  - safe-refactoring
x-author: context-cascade
x-verix-description: |
  [assert|neutral] codex-safe-experiment skill for sandboxed experimentation [ground:given] [conf:0.95] [state:confirmed]
---

<!-- S0 META-IDENTITY -->

# Codex Safe Experiment Skill



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

## Purpose

Use Codex CLI's sandbox mode to experiment with risky changes in complete isolation. Network is disabled, only CWD is accessible, providing safe experimentation.

## When to Use This Skill

- Risky refactoring that might break things
- Experimental approaches before committing
- Testing destructive operations safely
- Trying new libraries or patterns
- Major architectural changes
- Security-sensitive experiments

## When NOT to Use This Skill

- Simple, low-risk changes
- When network access is needed
- When accessing files outside project
- Production debugging
- Quick fixes (use codex-iterative-fix)

## Workflow

### Phase 1: Experiment Design

1. Define what you want to try
2. Identify risk factors
3. Plan verification steps
4. Set success criteria

### Phase 2: Sandbox Execution

```bash
# Full sandbox mode (network disabled, CWD only)
./scripts/multi-model/codex-yolo.sh "Refactor auth system" task-id "." 10 sandbox

# Via delegate.sh
./scripts/multi-model/delegate.sh codex "Try experimental approach" --sandbox

# Direct Codex
bash -lc "codex --full-auto --sandbox true --network disabled exec 'Experiment with X'"
```

### Phase 3: Evaluation

1. Review what Codex tried
2. Evaluate if experiment succeeded
3. Decide: Apply to real codebase?
4. If yes: Apply changes outside sandbox

## Sandbox Isolation Layers

| Layer | Protection |
|-------|------------|
| Network | DISABLED - no external connections |
| Filesystem | CWD only - no parent access |
| OS-Level | Seatbelt (macOS) / Docker |
| Commands | Blocked: rm -rf, sudo, etc. |

## Success Criteria

- Experiment ran safely in sandbox
- Results evaluated
- Decision made: apply or discard
- No unintended side effects

## Example Usage

### Example 1: Major Refactoring

```text
User: "Refactor entire auth system to use new pattern"

Sandbox Process:
1. Clone relevant files to sandbox context
2. Codex implements new pattern
3. Run tests in sandbox
4. Evaluate results
5. If good: Apply to real codebase

Output:
- Experiment: Success
- Tests: 45/47 passing (2 need adjustment)
- Recommendation: Apply with minor fixes
```

### Example 2: Library Migration

```text
User: "Try migrating from moment.js to dayjs"

Sandbox Process:
1. Install dayjs in sandbox
2. Replace moment calls
3. Run tests
4. Compare bundle size

Output:
- Migration: Feasible
- Breaking changes: 3 date format strings
- Bundle reduction: 65KB
- Recommendation: Proceed with migration
```

## Integration with Meta-Loop

```
META-LOOP IMPLEMENT PHASE:
    |
    +---> High-risk change detected
    |         |
    |         +---> codex-safe-experiment
    |         |         |
    |         |         +---> Sandbox: Try change
    |         |         +---> Evaluate: Success?
    |         |         +---> If yes: Apply for real
    |         |
    |         +---> Continue to TEST phase
```

## Memory Integration

Results stored at:
- Key: `multi-model/codex/experiment/{project}/{task_id}`
- Tags: WHO=codex-safe-experiment, WHY=sandboxed-trial
- Contains: Experiment results, recommendation, diffs

## Invocation Pattern

```bash
# Via router with experiment keywords
./scripts/multi-model/multi-model-router.sh "Try refactoring X approach"

# Direct sandbox mode
bash -lc "codex --sandbox workspace-write exec 'Experiment with X'"
```

## Guardrails

NEVER:
- Apply sandbox results without review
- Skip the evaluation phase
- Use sandbox for production debugging
- Trust sandbox results blindly

ALWAYS:
- Review sandbox diffs before applying
- Document what was tried
- Store results for future reference
- Have rollback plan ready

## Decision Framework

| Experiment Result | Action |
|------------------|--------|
| All tests pass | Apply changes |
| Minor failures | Fix then apply |
| Major failures | Discard, try different approach |
| Unexpected behavior | Investigate before deciding |

## Related Skills

- `codex-iterative-fix`: After experiment, for cleanup
- `codex-audit`: Audit experimental changes
- `testing-quality`: Generate tests for experiments
- `llm-council`: Decide on experimental approaches

<!-- S4 SUCCESS CRITERIA -->

## Verification Checklist

- [ ] Experiment ran in sandbox
- [ ] Results captured and evaluated
- [ ] Decision documented
- [ ] If applied: Changes verified
- [ ] Memory-MCP updated

<!-- PROMISE -->

[commit|confident] <promise>CODEX_SAFE_EXPERIMENT_COMPLETE</promise>
