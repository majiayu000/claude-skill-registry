---
name: ralph-loop
description: Use after first code change. Autonomous iteration until all quality gates pass (max 7 iterations).
---

# SKILL: Ralph Loop

> **Purpose**: Autonomous completion loop - iterate until all tests pass, coverage met, type-check clean
> **Target**: Coder, Tester, Validator agents
> **⚠️ Subagents Only**: This skill is for coder/tester subagents. Main orchestrator must delegate via Task tool.

---

## Quick Start

### When to Use This Skill
- After first code change (Entry point)
- Tests failing or coverage low
- Type-check errors present
- Lint violations found

### Quick Reference
```bash
# Ralph Loop: Autonomous iteration
iteration=0
max_iterations=7
early_escalation=false

# Check for --early flag or architecture-related failure
if [[ "$*" == *"--early"* ]] || is_architecture_failure; then
  max_iterations=2
  early_escalation=true
fi

while [ $iteration -lt $max_iterations ]; do
  echo "Iteration $((iteration + 1))/$max_iterations"

  # Run verification
  if run_all_checks; then
    echo "✓ All quality gates passed"
    break
  fi

  # Fix failures
  fix_failures

  # Update state
  update_state "$SC" "in_progress" $((iteration + 1))
  ((iteration++))
done

# Complete or escalate
if [ $iteration -eq $max_iterations ]; then
  echo "<CODER_BLOCKED>"  # Escalate to GPT Architect
else
  echo "<CODER_COMPLETE>"  # All checks pass
fi
```

---

## Core Concepts

### Entry Point

**Trigger**: Immediately after first code change

**Detection**:
- Coder agent makes first edit/write
- Tests run and fail
- Ralph Loop begins automatically

### Quality Gates

**All must pass** before completion:
1. **Tests**: `npm test` - All tests pass
2. **Coverage**: ≥80% overall, ≥90% core modules
3. **Type-check**: `npm run type-check` or `tsc --noEmit`
4. **Lint**: `npm run lint` - Zero violations
5. **TODOs**: All SC TODOs must be `[x]` before `<CODER_COMPLETE>`
   - PLAN_PATH from execute-plan prompt OR auto-detect in `.pilot/plan/in_progress/`
   - `grep -q "^- \[ \]" "$PLAN_PATH"` must return false (no unchecked items)

### Iteration Pattern

| Mode | Max Iter | Trigger | Escalation |
|------|----------|---------|------------|
| **Standard** | 7 | Default (after failed attempts) | GPT Architect at iteration 7 |
| **Early** | 2 | `--early` flag OR architecture failure | GPT Architect at iteration 2 |

**Triggers for Early Escalation**: `--early` flag OR architecture keywords (architecture, tradeoff, design, scalability, pattern, choice) OR confidence < 0.5 (see @.claude/skills/gpt-delegation/SKILL.md)

**Flow**: Code change → Run checks → All pass? → Complete : Check trigger → Fix → Repeat (max iterations) → Escalate to GPT Architect if blocked

---

## Implementation

### Verification Function
```bash
run_all_checks() {
  # Tests
  npm test || return 1

  # Coverage (≥80%)
  coverage=$(npm test -- --coverage 2>&1 | grep -oP 'Lines\s+:\s+\K[\d.]+')
  (( $(echo "$coverage < 80" | bc -l) )) && return 1

  # Type-check
  npm run type-check || return 1

  # Lint
  npm run lint || return 1

  # TODOs (PLAN_PATH from execute-plan OR auto-detect)
  PLAN_PATH="${PLAN_PATH:-$(find .pilot/plan/in_progress -name "*.md" -type f | head -1)}"
  if [ -f "$PLAN_PATH" ]; then
    grep -q "^- \[ \]" "$PLAN_PATH" && return 1
  fi

  return 0
}
```

### Fix Function
```bash
fix_failures() {
  # Priority: tests → type-check → lint → coverage
  npm test || { echo "Fixing test failures..."; }
  npm run type-check || { echo "Fixing type errors..."; }
  npm run lint || { echo "Fixing lint violations..."; }
}
```

### Architecture Failure Detection
```bash
is_architecture_failure() {
  # Check for architecture keywords in error output
  local error_log=$(last_error 2>/dev/null || echo "")
  local arch_keywords="architecture|tradeoff|design|scalability|pattern|choice"

  if echo "$error_log" | grep -qiE "$arch_keywords"; then
    return 0  # True
  fi

  # Check confidence score (see @.claude/skills/gpt-delegation/SKILL.md)
  # confidence = 1.0 - (architecture_keywords * 0.3) - (multiple_approaches * 0.2) - (uncertainty_markers * 0.2)
  # If confidence < 0.5, trigger early escalation

  return 1  # False
}
```

---

## Escalation

### When Blocked

**Condition**: Max iterations reached (7 standard, 2 early escalation), still failing

**Action**: Delegate to GPT Architect
```bash
echo "<CODER_BLOCKED>"
echo "Iterations: $iteration"
echo "Early Escalation: $early_escalation"
echo "Last error: $(last_error)"
```

**Orchestrator handles escalation**: Reads `.claude/rules/delegator/prompts/architect.md`, builds delegation prompt with history, calls `codex-sync.sh` (workspace-write mode), applies GPT recommendations, re-invokes Coder

### Early Escalation

**Purpose**: Rapid escalation for architecture-related failures (max 2 iterations instead of 7)

**Triggers**: 1) `--early` flag (explicit request), 2) Architecture keywords in errors (architecture, tradeoff, design, scalability, pattern, choice), 3) Low confidence < 0.5 (see @.claude/skills/gpt-delegation/SKILL.md rubric)

**Behavior**: Faster delegation to GPT Architect, ideal for complex design decisions requiring expert input

---

## No-Excuses Enforcement

**PROHIBITED Phrases**: "I cannot", "Too complex", "Out of scope", "Unable to"

**Required Pattern**: on_blocker_detected → GPT delegation → User collaboration (never "give up")

**Details**: @.claude/skills/ralph-loop/REFERENCE.md - Full enforcement algorithm

---

## Further Reading

**Internal**: @.claude/skills/ralph-loop/REFERENCE.md - Advanced patterns, state machine details | @.claude/skills/tdd/SKILL.md - Red-Green-Refactor cycle | @.claude/skills/gpt-delegation/SKILL.md - GPT escalation patterns

**External**: [The Pragmatic Programmer](https://www.amazon.com/Pragmatic-Programmer-journey-mastery-Anniversary/dp/0135957052) | [Working Effectively with Legacy Code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)

---

**Version**: claude-pilot 4.4.50
