---
name: codex-iterative-fix
description: Use Codex CLI in full-auto mode to fix issues iteratively until tests pass. Autonomous debugging and test-fixing loop with sandbox safety.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
x-version: 1.0.0
x-category: platforms
x-tags:
  - codex
  - debugging
  - testing
  - multi-model
  - autonomous
x-author: context-cascade
x-verix-description: |
  [assert|neutral] codex-iterative-fix skill for autonomous test fixing [ground:given] [conf:0.95] [state:confirmed]
---

<!-- S0 META-IDENTITY -->

# Codex Iterative Fix Skill



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

Use Codex CLI's autonomous iteration capability to fix failing tests and debug issues until they pass. This skill leverages Codex's strength at long-horizon coding tasks.

## When to Use This Skill

- Multiple tests failing that need iterative fixing
- Debugging issues requiring trial-and-error
- Refactoring with test validation
- CI/CD failures needing automated fixes
- Build errors requiring multiple attempts

## When NOT to Use This Skill

- Research tasks (use multi-model-discovery)
- Understanding codebase (use gemini-codebase-onboard)
- Critical production code (use sandbox mode first)
- Architecture decisions (use llm-council)

## Workflow

### Phase 1: Initial Assessment

1. Identify failing tests/errors
2. Determine scope of fixes needed
3. Choose appropriate mode:
   - `full-auto`: Standard autonomous mode
   - `sandbox`: For risky changes
   - `yolo`: When speed is critical

### Phase 2: Codex Execution

```bash
# Standard iterative fix
./scripts/multi-model/codex-yolo.sh "Fix all failing tests" task-id "." 15 full-auto

# With sandbox protection
./scripts/multi-model/codex-yolo.sh "Fix tests" task-id "." 10 sandbox

# Via delegate.sh
./scripts/multi-model/delegate.sh codex "Fix all failing tests and verify they pass" --full-auto
```

### Phase 3: Verification

1. Codex runs tests after each fix
2. Iterates until all tests pass
3. Claude reviews final changes
4. Summary of what was fixed

## Success Criteria

- All targeted tests passing
- No new regressions introduced
- Changes reviewed and validated
- Clear documentation of fixes

## Example Usage

### Example 1: Test Suite Failures

```text
User: "CI is failing with 12 test errors"

Codex Process:
1. Run tests, capture failures
2. Analyze first failure
3. Implement fix
4. Re-run tests
5. Repeat until all pass

Output:
- Fixed: 12 tests
- Changes: 8 files modified
- Root causes: Missing null checks, outdated mocks
```

### Example 2: Type Errors

```text
User: "TypeScript build has 47 type errors"

Codex Process:
1. Run tsc, capture errors
2. Fix type errors systematically
3. Re-run after each batch
4. Verify build succeeds

Output:
- Fixed: 47 type errors
- Patterns: Missing types, incorrect generics
- Added: 3 new type definitions
```

## Modes Explained

| Mode | Command | Use Case | Risk |
|------|---------|----------|------|
| full-auto | `--full-auto` | Standard iteration | Medium |
| sandbox | `--sandbox workspace-write` | Risky refactors | Low |
| yolo | `--yolo` | Speed critical | High |

## Integration with Meta-Loop

```
META-LOOP IMPLEMENT PHASE:
    |
    +---> codex-iterative-fix
    |         |
    |         +---> Codex: Run tests
    |         +---> Codex: Fix failures
    |         +---> Codex: Iterate until pass
    |
    +---> Continue to TEST phase (verification)
```

## Memory Integration

Results stored at:
- Key: `multi-model/codex/iterative-fix/{project}/{task_id}`
- Tags: WHO=codex-iterative-fix, WHY=autonomous-fixing

## Invocation Pattern

```bash
# Via router (automatic detection)
./scripts/multi-model/multi-model-router.sh "Fix all failing tests"

# Direct Codex call
bash -lc "codex --full-auto exec 'Fix all failing tests and verify they pass'"
```

## Guardrails

NEVER:
- Run on production without review
- Skip final verification
- Ignore new test failures
- Exceed iteration limit without human check

ALWAYS:
- Review changes before commit
- Document what was fixed
- Check for regressions
- Store results in Memory-MCP

## Related Skills

- `codex-safe-experiment`: Sandbox experimentation
- `smart-bug-fix`: Systematic debugging
- `testing-quality`: Test generation
- `multi-model-discovery`: Find existing fixes

<!-- S4 SUCCESS CRITERIA -->

## Verification Checklist

- [ ] All targeted tests passing
- [ ] No new regressions
- [ ] Changes reviewed
- [ ] Memory-MCP updated
- [ ] Documentation complete

<!-- PROMISE -->

[commit|confident] <promise>CODEX_ITERATIVE_FIX_COMPLETE</promise>
