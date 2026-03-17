---
name: requirement-clarification
description: Detect ambiguous user instructions and guide users through structured clarification. Produces execution plans requiring explicit approval before proceeding.
version: 1.1
author: agent
---

# Requirement Clarification

Intercept and clarify ambiguous user instructions before execution.

---

## When to Use

Use this skill when:
- User instruction contains missing critical information
- References are vague ("that", "this", "there" without context)
- Statement is non-affirmative (questions, conditionals, suggestions)
- Scope or quality criteria are unclear
- High-risk operations (Git, file changes, config updates) are requested

**Trigger Threshold:** Score >= 30 or any mandatory trigger condition

---

## Prerequisites

- Understanding of the user's current context
- Knowledge of state-changing vs read-only operations
- Familiarity with confirmation vocabulary (preparing vs approving)

---

## Workflow

### Step 1: Ambiguity Detection

Calculate ambiguity score (0-100):

| Factor | Score |
|--------|-------|
| Missing critical parameter | +25 each |
| Vague reference | +15 each |
| Non-affirmative statement | +20 |
| Scope ambiguity | +10 |
| Conditional clause | +15 |
| High-risk operation | +25 |
| Non-confirmation word (准备/考虑/研究/讨论) | +20 |

**Thresholds:**
- 0-29: Proceed directly
- 30-59: Light clarification (1-2 questions)
- 60-89: Deep clarification (structured interview)
- 90+: Reject (too ambiguous)

### Step 2: Mandatory Pause Check

Before ANY state-changing action, ask:
> "Stop. Does this change state? Yes. Is it confirmed? No. Go confirm."

**Triggers mandatory pause:**
- Score >= 30
- Git operations (branch, commit, push, merge)
- File creation/deletion/moving
- Configuration changes
- "Preparing" words detected without "approving" context

### Step 3: Clarification Strategy

**Single Question Focus:**
Ask ONE critical question at a time.

**Provide Sensible Defaults:**
```
Target path?
- A) ./backup/ (backup directory)
- B) ./archive/ (archive directory)
- C) Other: _____
```

**Use Concrete Examples:**
```
Performance target?
Examples:
- "Startup time < 3 seconds"
- "Memory usage < 100MB"
- "QPS > 1000"
```

### Step 4: Build Execution Plan

Standard format:
```markdown
📋 Task Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 Goal: [Clear description of final state]

Steps:
1. [Step 1 with full parameters]
2. [Step 2 with full parameters]
...

Expected Output:
- [Output 1]
- [Output 2]

Risks:
- [Risk 1]
- [Risk 2]

Estimated Time: [X] minutes
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Confirmation: Reply "批准计划" to proceed
```

### Step 5: Wait for Approval

**Valid confirmations:**
- 批准 / Approve
- 确认 / Confirm
- 同意 / Agree
- 执行 / Execute
- 可以 / Yes/OK
- 行 / OK

**NOT confirmations (require clarification):**
- 准备 / Prepare
- 考虑 / Consider
- 研究 / Study
- 讨论 / Discuss
- 看看 / Take a look
- 想一下 / Think about it

### Step 6: Execute (Within Plan Boundaries)

Once "批准计划" received:
- Execute autonomously
- Follow plan exactly
- Report progress for long operations

**PAUSE and re-confirm if:**
- Need to modify files outside plan scope
- Encounter unexpected errors
- Discover significant plan deviation

### Step 7: Post-Execution Report

```markdown
✅ Task Complete Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed Steps:
✓ Step 1
✓ Step 2
...

Actual Output:
- [Output 1] - [description]
- [Output 2] - [description]

Deviations from Plan: [None / explanation]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Best Practices

### Do's
✅ Ask ONE question at a time for simple gaps
✅ Provide sensible defaults with options
✅ Use concrete examples to illustrate
✅ Acknowledge when clarification is needed
✅ Keep tone collaborative, not interrogative
✅ Respect "you decide" but still require final approval

### Don'ts
❌ Ask more than 3 questions in one turn
❌ Proceed with assumptions without confirmation
❌ Treat questions as directives
❌ Ignore conditionals ("if", "when", "maybe")
❌ Pressure user for perfect precision

### High-Risk Exceptions

Even with plan approval, require separate confirmation:
- `git push` (pushing to remote)
- `git reset --hard` (force reset)
- `rm -rf` or permanent deletion
- External API calls with costs
- Modifying secrets/critical configs
- Operations affecting external systems

---

## Common Issues

### Issue 1: Clarification Loop

**Symptom:** User provides multiple answers that don't converge.

**Solution:**
```
ℹ️ After multiple clarifications, requirements still have uncertainties.

Options:
A) Split task into smaller steps
B) I provide a recommendation for your approval

Choose?
```

### Issue 2: "You Decide" Delegation

**Symptom:** User says "你决定" / "you decide".

**Solution:**
```
📝 Recommended Plan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Based on common scenarios, I suggest:

[Plan details]

Reply "批准计划" to proceed, or tell me specific changes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Issue 3: "Preparing" vs "Approving" Confusion

**Symptom:** User uses "准备实施" (preparing to implement).

**Solution:**
```
ℹ️ Clarification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You used "准备" (preparing), which indicates planning phase.

Please confirm:
- A) Continue planning/discussion (no execution)
- B) Approve execution (say "批准实施" or "确认执行")

Current status: Waiting for explicit approval
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Issue 4: User Changes Mind

**Symptom:** User contradicts previous clarifications.

**Solution:**
```
ℹ️ Received new information. Updated plan:

[Revised plan]

Confirm execution of this updated version?
```

### Issue 5: Too Ambiguous (>90 score)

**Symptom:** Cannot form reliable plan.

**Solution:**
```
⚠️ Instruction too ambiguous for reliable plan.

Please rephrase in format:
"对 [具体对象] 执行 [具体操作]，要求 [具体标准/条件]"

Example:
"对 memory/2026-02-11.md 添加今天的 git 操作记录，要求包含完整的命令输出"
```

---

## Decision Tree

```
Input: User instruction
│
├─ Read-only query? (查看/读取/显示)
│  └─ YES → Skip, proceed directly
│
├─ High-risk operation? (git, file ops, config)
│  └─ YES → Trigger (+25, mandatory pause)
│
├─ Non-confirmation words? (准备/考虑/研究/讨论)
│  └─ YES → Trigger (+20)
│
├─ Action without confirmation? ("Do it" / "Go ahead")
│  └─ YES → Trigger (intent ≠ approval)
│
├─ Vague reference? ("this", "that", "it")
│  └─ YES → Trigger
│
├─ Question format? (吗？/？)
│  └─ YES → Trigger
│
├─ Conditional? ("if", "when", "maybe")
│  └─ YES → Trigger
│
├─ Missing parameters?
│  └─ YES → Trigger
│
└─ Final Check
   ├─ Score < 30 AND no mandatory triggers?
   │  └─ YES → Proceed
   └─ Score ≥ 30 OR mandatory trigger?
      └─ YES → Trigger skill
```

---

## See Also

- [git-workflow](./git-workflow) - Safe Git operations
- [code-analysis](./code-analysis) - Structured code understanding
- [code-generator](./code-generator) - Implementation from design

---

## Version History

- **v1.1** (2026-02-11) - Integration with agent policies
  - Added mandatory pause mechanism
  - Added habitual violation blacklist
  - Added "preparing vs approving" detection
  - Aligned with Batch Confirmation Mode

- **v1.0** (2026-02-11) - Initial release
  - Ambiguity detection framework
  - Clarification strategies
  - Plan template
  - Edge case handling
