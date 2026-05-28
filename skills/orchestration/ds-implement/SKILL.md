---
name: ds-implement
description: "REQUIRED Phase 3 of /ds workflow. Enforces output-first verification at each step."
---

## Overview

Apply output-first verification at every step of analysis implementation. This is Phase 3 of the `/ds` workflow.

## Contents

- [Delegation Pattern](#delegation-pattern) - Main chat orchestrates, subagents analyze
- [The Iron Law](#the-iron-law-of-ds-implementation) - EVERY step MUST produce visible output
- [Output-First Protocol](#output-first-protocol) - Required outputs by operation type
- [Implementation Process](#implementation-process) - Step-by-step workflow
- [Task Agent Invocation](#task-agent-invocation) - Spawning sub-agents
- [Verification Patterns](#verification-patterns) - See `references/verification-patterns.md`
- [Common Failures](#common-failures-to-avoid) - Silent data loss, hidden nulls

# Implementation (Output-First Verification)

<EXTREMELY-IMPORTANT>
## The Iron Law of Delegation

**YOU MUST NOT WRITE ANALYSIS CODE. This is not negotiable.**

You orchestrate. Subagents analyze. STOP if you're about to write Python/R code.

Allowed in main chat:
- Spawn Task agents
- Review Task agent output
- Verify outputs exist and are reasonable
- Write to .claude/*.md files

NOT allowed in main chat:
- Write/Edit code files (.py, .R, .ipynb, etc.)
- Direct data manipulation
- "Quick analysis"

**If you're about to write analysis code directly, STOP and spawn a Task agent instead.**

### Rationalization Prevention

Stop immediately when you encounter these rationalizations:

| Rationalization | Reality |
|---------|---------|
| "It's just a quick plot" | You'll hide data issues. Delegate instead. |
| "I'll just check the shape" | Your shape checks need output-first protocol. Delegate. |
| "The subagent will take too long" | Your impatience costs more in context than subagent time. Delegate. |
| "I already know this data" | Your knowledge ≠ verified output. Delegate and see. |
| "Let me just run this merge" | Your merges will silently fail. Delegate with verification. |
| "This is too simple for a subagent" | Your simple code hides errors. Delegate. |
| "I'm already looking at the data" | Your looking ≠ analyzing. Delegate. |
| "Results are needed fast" | Your wrong results are worse than slow right results. Delegate. |
</EXTREMELY-IMPORTANT>

## Delegation Pattern

For each task in PLAN.md:
1. Dispatch analyst subagent (does the work with output-first)
2. Verify outputs are present and reasonable
3. Dispatch methodology reviewer (for statistical tasks)
4. Log findings to LEARNINGS.md

**Why delegate?**
- Fresh context per task (no pollution from previous analysis)
- Enforced output verification (can't skip)
- Error isolation (bad analysis doesn't corrupt main context)

**REQUIRED SUB-SKILL:** For Task templates and detailed flow:
```
Skill(skill="workflows:ds-delegate")
```

---

Implement analysis with mandatory visible output at every step.
**NO TDD** - instead, every code step MUST produce and verify output.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Implementation

**EVERY CODE STEP YOU WRITE MUST PRODUCE VISIBLE OUTPUT. This is not negotiable.**

Before moving to the next step, you MUST execute the following:
1. Run the code
2. See the output (print, display, plot)
3. Verify output is correct/reasonable
4. Document in LEARNINGS.md
5. Only THEN proceed to next step

This applies even when YOU think:
- "I know this works"
- "It's just a simple transformation"
- "I'll check results at the end"
- "The code is straightforward"

**If you're about to write code without outputting results, STOP.**
</EXTREMELY-IMPORTANT>

## What Output-First Means

| DO | DON'T |
|-------|----------|
| Print shape after each transform | Chain operations silently |
| Display sample rows | Trust transformations work |
| Show summary stats | Wait until end to check |
| Verify row counts | Assume merges worked |
| Check for unexpected nulls | Skip intermediate checks |
| Plot distributions | Move on without looking |

**The Mantra:** If not visible, it cannot be trusted.

## Red Flags - STOP Immediately

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "I'll check at the end" | STOP - you're letting errors compound silently | Check after every step |
| "This transform is simple" | STOP - simple code can still be wrong | Output and verify |
| "I know merge worked" | STOP - you've assumed this before and been wrong | Check row counts |
| "Data looks fine" | STOP - you're confusing "looks" with verification | Print stats, show samples |
| "I'll batch the outputs" | STOP - you're about to lose your ability to isolate issues | Output per operation |

## Output-First Protocol

### For Every Data Operation:

```python
# BEFORE
print(f"Before: {df.shape}")

# OPERATION
df = df.merge(other, on='key')

# AFTER - MANDATORY
print(f"After: {df.shape}")
print(f"Nulls introduced: {df.isnull().sum().sum()}")
df.head()
```

### Required Outputs by Operation Type

| Operation | Required Output |
|-----------|-----------------|
| Load data | shape, dtypes, head() |
| Filter | shape before/after, % removed |
| Merge/Join | shape, null check, sample |
| Groupby | result shape, sample groups |
| Transform | before/after comparison, sample |
| Model fit | metrics, convergence info |
| Prediction | distribution, sample predictions |

## Implementation Process

### Step 1: Read Plan

Read the plan to understand task order:

```bash
cat .claude/PLAN.md  # View analysis plan and task sequence
```

Follow the task order defined in the plan.

### Step 2: Implement with Output

For each task:

```python
# Task N: [Description]
print("=" * 50)
print("Task N: [Description]")
print("=" * 50)

# Before state
print(f"Input shape: {df.shape}")

# Operation
result = do_operation(df)

# After state - MANDATORY
print(f"Output shape: {result.shape}")
print(f"Sample output:")
display(result.head())

# Verification
assert result.shape[0] > 0, "No rows returned!"
print("Task N complete")
```

### Step 3: Log to LEARNINGS.md

Document every significant step:

```markdown
## Step N: [Task Description]

**Input:** DataFrame with shape (10000, 15)

**Operation:** Merged with reference table on 'id'

**Output:**
- Shape: (9500, 20)
- 500 rows dropped (no match)
- 5 new columns added
- No new nulls introduced

**Verification:**
- Row count reasonable (5% drop expected due to filtering)
- Sample output matches expected format
- Key columns preserved

**Notes:** [Any observations, issues, or decisions]
```

## Task Agent Invocation

Main chat spawns Task agent:

```
Task(subagent_type="general-purpose", prompt="""
Implement [TASK] following output-first protocol.

Context:
- Read .claude/LEARNINGS.md for prior steps
- Read .claude/PLAN.md for task details
- Read .claude/SPEC.md for objectives

Output-First Protocol:
1. Print state BEFORE each operation
2. Execute the operation
3. Print state AFTER with verification
4. Display sample output
5. Document in LEARNINGS.md

Required outputs per operation:
- Shape before/after
- Null counts
- Sample rows (head)
- Sanity checks (row counts, value ranges)

DO NOT proceed to next task without:
- Visible output showing operation worked
- LEARNINGS.md entry documenting the step

Report back: what was done, output observed, any issues.
""")
```

## Verification Patterns

See [references/verification-patterns.md](references/verification-patterns.md) for detailed code patterns for:
- Data loading, filtering, merging
- Aggregation and model training
- Quick reference table by operation type

## Common Failures to Avoid

| Failure | Why It Happens | Prevention |
|---------|----------------|------------|
| Silent data loss | Merge drops rows | Print row counts before/after |
| Hidden nulls | Join introduces nulls | Check null counts after joins |
| Wrong aggregation | Groupby logic error | Display sample groups |
| Type coercion | Pandas silent conversion | Verify dtypes after load |
| Off-by-one | Date filtering edge cases | Print min/max dates |

## Logging

Append each step to `.claude/LEARNINGS.md`:

```markdown
## Step N: [Description] - [STATUS]

**Input:** [Describe input state]

**Operation:** [What was done]

**Output:** [Shape, stats, sample]
```
[Paste actual output here]
```

**Verification:** [How you confirmed it worked]

**Next:** [What comes next]
```

## If Output Looks Wrong

1. **STOP** - do not proceed
2. **Investigate** - print more details
3. **Document** - log the issue in LEARNINGS.md
4. **Ask** - if unclear, ask user for guidance
5. **Fix** - only proceed after output verified

**Never hide failures.** Bad output documented is better than silent failure.

## No Pause Between Tasks

<EXTREMELY-IMPORTANT>
**After completing task N, IMMEDIATELY start task N+1. You MUST NOT pause.**

| Thought | Reality |
|---------|---------|
| "Task done, should check in with user" | You're wasting context. User wants ALL tasks done. Keep going. |
| "User might want to see intermediate results" | You're assuming wrong. User will see results at the END. Continue. |
| "Natural pause point" | You're making excuses. Only pause when ALL tasks complete or you're blocked. |
| "Should summarize this step" | You're procrastinating. Summarize AFTER all tasks. Keep moving. |

**Your pausing between tasks is procrastination disguised as courtesy.**
</EXTREMELY-IMPORTANT>

## Phase Complete

**REQUIRED SUB-SKILL:** After all analysis steps complete with verified output, IMMEDIATELY invoke:
```
Skill(skill="workflows:ds-review")
```
