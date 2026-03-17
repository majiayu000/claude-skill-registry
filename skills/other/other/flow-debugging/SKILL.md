---
name: flow-debugging
description: "4-phase systematic debugging for flow-fix. NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST."
---

# Flow Debugging - Systematic Debugging Method

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Bug fixing is not a guessing game. Systematic debugging = faster fixes + fewer regressions.

## The 4-Phase Process

```
Phase 1: ROOT CAUSE INVESTIGATION (NO FIXES YET)
    ↓
Phase 2: PATTERN ANALYSIS
    ↓
Phase 3: HYPOTHESIS AND TESTING
    ↓
Phase 4: IMPLEMENTATION (TDD)
```

## Phase 1: Root Cause Investigation

**Iron Law**: In this phase, **NO FIX CODE ALLOWED**.

```yaml
Step 1: Read Error Completely
  - Don't skip any details
  - Record: error type, message, stack trace
  - Record: when it happens, frequency, impact

Step 2: Stable Reproduction
  - Find reliable reproduction steps
  - Record: inputs, environment, preconditions
  - If can't reproduce → gather more information

Step 3: Check Recent Changes
  - git log --oneline -20
  - git diff HEAD~5
  - Ask: What changed? When did it start failing?

Step 4: Trace Data Flow Backwards
  - Start from error point
  - Trace upstream
  - Find where data goes wrong
```

**Output**: Root cause hypothesis (evidence-based, not a guess)

## Phase 2: Pattern Analysis

```yaml
Step 1: Find Working Examples
  - Where does similar functionality work?
  - Compare: working vs broken

Step 2: Compare with Reference
  - What does official documentation say?
  - How do other projects do it?
  - What's different?

Step 3: Identify Patterns
  - Is this a known bug pattern?
  - Search: error message + framework name
```

**Output**: Confirmed or refined root cause hypothesis

## Phase 3: Hypothesis and Testing

```yaml
Step 1: Form Single Hypothesis
  - "The problem is because X"
  - Hypothesis must be verifiable

Step 2: Test One Variable at a Time
  - Change only one factor
  - Observe result
  - Record: what changed, what happened

Step 3: 3+ Failed Fixes → STOP
  - If 3+ fix attempts fail
  - Stop and question architecture
  - Problem may be deeper than thought
```

**Red Flag**: If you're "trying this, trying that", you're guessing, not debugging.

## Phase 4: Implementation (TDD)

**Prerequisite**: Phases 1-3 complete, root cause confirmed

```yaml
Step 1: Write Failing Test First
  - Test must reproduce the bug
  - Run test, confirm it fails
  - This is your "red light"

Step 2: Implement Single Fix
  - Fix only the root cause
  - Don't "while I'm here" other things
  - Minimal change

Step 3: Verify
  - Run test, confirm it passes
  - Run related tests, confirm no regression
  - Manual verify original issue resolved
```

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "I know where the problem is" | Prove it. Investigate first. |
| "Quick fix" | Quick fix = quick regression. Systematic debug. |
| "No time for tests" | No tests = don't know if really fixed. |
| "Small change" | Small changes can introduce big bugs. Test it. |
| "Fix first, investigate later" | Fixing without understanding = guessing. |
| "Let me try this" | "Trying" is not debugging. Form hypothesis, verify it. |
| "It's obvious" | Nothing is obvious. Prove with evidence. |
| "I've seen this before" | Every bug is unique. Investigate this one. |

## Red Flags - STOP

If you find yourself:
- Fixing without reproduction
- "Trying this, trying that"
- 3+ failed fix attempts
- Saying "fixed" without tests
- Changing many files for one bug

**STOP. Go back to Phase 1. Investigate root cause.**

## Debug Output Template

```markdown
# Bug Analysis - ${BUG_ID}

## Phase 1: Root Cause Investigation

### Error Details
- Type: [error type]
- Message: [error message]
- Stack: [key stack frames]

### Reproduction
- Steps: [1, 2, 3...]
- Frequency: [always/sometimes/rare]
- Environment: [conditions]

### Recent Changes
- [relevant commits]

### Data Flow Analysis
- [where data goes wrong]

### Root Cause Hypothesis
[Evidence-based hypothesis]

## Phase 2: Pattern Analysis

### Working Example
[Where similar code works]

### Comparison
[Difference between working and broken]

### Confirmed Root Cause
[Refined hypothesis]

## Phase 3: Hypothesis Testing

### Hypothesis
[Single testable hypothesis]

### Test Results
| Change | Result |
|--------|--------|
| [change 1] | [result] |

## Phase 4: Implementation

### Failing Test
[Test code that reproduces bug]

### Fix
[Minimal fix code]

### Verification
- [ ] Test passes
- [ ] No regression
- [ ] Manual verification
```

## Integration with flow-fix

This skill is the core methodology for `/flow-fix` command:

```yaml
/flow-fix phases:
  阶段 1: Root Cause Investigation → This skill Phase 1
  阶段 2: Pattern Analysis & Planning → This skill Phase 2
  阶段 3: 修复执行 (TDD) → This skill Phase 3-4
  阶段 4: 验证与发布 → verification-before-completion
```

## Cross-Reference

- [flow-fix.md](../../commands/flow-fix.md) - Bug fix command
- [flow-tdd/SKILL.md](../flow-tdd/SKILL.md) - TDD enforcement
- [verification-before-completion](../verification-before-completion/SKILL.md) - Verification skill

---

**[PROTOCOL]**: 变更时更新此头部，然后检查 CLAUDE.md
