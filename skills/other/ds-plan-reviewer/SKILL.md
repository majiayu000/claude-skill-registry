---
name: ds-plan-reviewer
description: "Internal skill used by ds-plan at Phase 2 exit gate. Dispatches a reviewer subagent to verify PLAN.md quality before implementation. NOT user-facing."
user-invocable: false
disable-model-invocation: true
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-reviewer-readonly-guard.py"
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-reviewer-readonly-guard.py"
---

# Plan Document Reviewer (Data Science)

**Purpose:** Catch plan gaps BEFORE they survive into implementation. Bad task decomposition, missing data profiling, and spec misalignment cost 10x more to fix during implementation than during review.

## When to Dispatch

After Phase 2 (ds-plan) writes `.planning/PLAN.md` and before Phase 3 (ds-implement) begins.

```
Phase 2: ds-plan -> PLAN.md written
  -> [THIS SKILL] Dispatch plan reviewer subagent
  -> For plans with >15 tasks: review per-chunk
  -> Issues found? Fix PLAN.md -> re-dispatch reviewer
  -> Approved? -> Phase 3: ds-implement
```

<EXTREMELY-IMPORTANT>
## The Iron Law of Plan Review

**NO IMPLEMENTATION WITHOUT REVIEWED PLAN. This is not negotiable.**

A bad plan that survives into implementation means:
- Subagents struggling with tasks that lack intermediate output definitions
- Missing data profiling steps discovered mid-analysis
- Spec requirements silently dropped
- Rework when task ordering ignores data dependencies

**Catching a plan gap NOW costs 1 minute. Catching it during implementation costs hours.**
</EXTREMELY-IMPORTANT>

### Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "The plan looks fine to me" | Self-review is rubber-stamping | Dispatch independent reviewer |
| "User already approved the plan" | User approves the approach, not task granularity | Reviewer checks what user might miss |
| "This will slow us down" | 30-second review saves hours of implementation rework | Dispatch the reviewer |
| "It's a simple analysis, no review needed" | Simple plans hide the most missing steps | Review it anyway |
| "I'll catch issues during implementation" | Implementation subagents don't know the spec | Review BEFORE implementing |

### Red Flags - STOP If You Catch Yourself:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "The plan looks fine to me" | Self-assessment is rubber-stamping — check EVERY task against the checklist | Read each task individually, verify outputs and verification steps defined |
| "Plan looks similar to a prior analysis" | Similar structure ≠ complete tasks — prior plans had different data sources | Evaluate THIS plan against THIS spec's requirements |
| "Tasks are obvious, they don't need intermediate output definitions" | Subagents receiving these tasks have no context — vague tasks produce wrong analysis | Verify EVERY task defines what it produces and what proves completion |
| "Missing verification steps are fine, ds-implement handles that" | ds-implement enforces output-first per step, but missing task-level verification means no one checks the task's overall outcome | Flag missing verification criteria NOW |

## Chunking Rule

**If PLAN.md has >15 tasks:** Break into ordered chunks using `## Chunk N: <name>` headings. Each chunk should be logically self-contained (e.g., "data cleaning", "feature engineering", "analysis", "visualization"). Review each chunk separately.

**If PLAN.md has <=15 tasks:** Review the entire plan in one pass.

**Why chunk:** Monolithic review of large documents produces shallow feedback. Focused review per chunk catches more issues.

## Dispatch Template (Single Plan or Per-Chunk)

Use this Task invocation to dispatch the plan reviewer:

```
Agent(
  subagent_type="general-purpose",
  description="Review DS plan document",
  allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"],
  prompt="""
You are a data science plan document reviewer. Verify this plan is complete, matches the spec, and is ready for implementation.

**Tool Restrictions:** The plan reviewer is READ-ONLY. It reads `.planning/PLAN.md` and `.planning/SPEC.md`, evaluates against checklist, returns verdict. It MUST NOT use Write or Edit.

**Plan to review:** .planning/PLAN.md [-- Chunk N only, if chunked]
**Spec for reference:** .planning/SPEC.md

Read BOTH files, then evaluate the plan against ALL categories below.

## What to Check

| Category | What to Look For |
|----------|------------------|
| Completeness | TODOs, placeholders, incomplete tasks, missing steps |
| Spec Alignment | Plan covers ALL spec requirements, no scope creep, no requirements silently dropped |
| Data Profiling | Data profile section present with shape, types, quality issues documented |
| Task Decomposition | Tasks atomic enough for a single subagent, clear boundaries, steps actionable |
| Task Ordering | Dependencies correct (cleaning before analysis), no circular dependencies |
| Intermediate Outputs | Each task defines what it produces and what proves completion |
| Output-First Verification | Each task includes verification steps (print shape, check nulls, sample output) |
| ETL Strategy | If data > 1M rows or multiple sources: filter strategy, parallelism plan, caching documented |
| Reproducibility | Random seeds, package versions, data snapshots documented where relevant |

## CRITICAL - Look Especially Hard For:

- Any TODO markers or placeholder text
- Steps that say "similar to X" without actual content
- Tasks missing intermediate output definitions (what does this task produce?)
- Tasks missing verification steps (how do you know it worked?)
- Missing data profiling tasks (should always come before analysis)
- Data cleaning tasks that lack strategy for each quality issue found in profiling
- Spec requirements not covered by ANY task (silently dropped)
- Tasks too large for a single subagent (>100 lines of change or multiple distinct operations)
- ETL strategy missing when data is large (>1M rows) or from multiple sources
- Missing output verification plan section

## Output Format

## Plan Review

**Status:** APPROVED | ISSUES_FOUND

**Issues (if any):**
- [Task X, Step Y]: [specific issue] - [why it matters for implementation]

**Spec Coverage Check:**
- [Requirement 1]: Covered by Task N | NOT COVERED
- [Requirement 2]: Covered by Task N | NOT COVERED

**Recommendations (advisory - don't block approval):**
- [suggestions for improvement that aren't blocking]
""")
```

## Handling Reviewer Output

### If APPROVED
Proceed immediately to Phase 3 (ds-implement). Discover and load:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-implement/SKILL.md` and follow its instructions.

### If ISSUES_FOUND
1. Fix the specific issues in `.planning/PLAN.md`
2. Re-dispatch the reviewer (same template)
3. Repeat until APPROVED or max 5 iterations

### If 5 Iterations Without Approval
Escalate to user:
```
"Plan reviewer has flagged issues 5 times. Remaining issues:
[list issues]
Should I: (A) Fix these, (B) Proceed with known gaps, (C) Rethink the plan?"
```

## Model Tier Hints

When the reviewed plan proceeds to implementation, add model tier guidance to task dispatch:

| Task Complexity | Model Tier | Signals |
|----------------|------------|---------|
| Mechanical | Cheapest capable | Data loading, simple filtering, descriptive stats, file format conversion |
| Integration | Standard | Merges/joins across sources, aggregations, visualization, data reshaping |
| Architecture/Review | Most capable | Feature engineering strategy, model selection, statistical assumption validation, methodology review |

**Advisory only** -- Claude Code doesn't yet support model routing. Document intent for future use.

## Drive-Aligned Framing

**Proceeding to implementation with a flawed plan is NOT HELPFUL — implementation subagents will fail on gaps you could have caught now.**

You know the plan has gaps. Implementation subagents will struggle with tasks that lack intermediate output definitions, miss data profiling steps that aren't documented, and build the wrong analysis when spec requirements are silently dropped.

**Fix the plan now. It costs minutes, not hours.**

## Gate Function

**Checkpoint type:** human-verify (plan quality is machine-verifiable)

```
1. IDENTIFY: `.planning/PLAN.md` exists
2. DISPATCH: Send to reviewer subagent (per-chunk if >15 tasks)
3. READ: Reviewer returns APPROVED or ISSUES_FOUND
4. VERIFY: If ISSUES_FOUND, fix and re-dispatch (max 5)
5. CLAIM: Only proceed to ds-implement when ALL chunks APPROVED
```
