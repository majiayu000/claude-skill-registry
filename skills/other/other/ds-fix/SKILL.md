---
name: ds-fix
version: 1.0
description: "This skill should be used when the user asks to 'fix analysis', 'wrong results', 'notebook error', 'reviewer feedback', 'data changed', 'debug notebook', or needs mid-analysis course-correction for wrong results, notebook errors, or data changes."
hooks:
  PostToolUse:
    - matcher: "Agent"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-post-subagent-guard.py"
  PreToolUse:
    - matcher: "Read"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Grep"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Glob"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
---

**Announce:** "Using ds-fix for mid-analysis course correction."

## Session Resume Detection

Before starting, check for an existing handoff:

1. Check if `.planning/HANDOFF.md` exists
2. **If found:** Read it and present to user:
   - Show the phase, task progress, and Next Action from the handoff
   - Ask: "Resume from handoff, or start fresh?"
   - If resume: skip to the recorded phase
   - If fresh: proceed with diagnosis
3. **If not found:** Proceed normally with Step 1 (Load Context)

## Where This Fits

```
/ds (entry) → brainstorm → plan → implement → review → verify
                                    ↑
/ds-fix (midpoint) ─────────────────┘
```

This is the re-entry point. Jump back into a DS workflow that needs fixing.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Editing

**DIAGNOSE BEFORE FIXING. This is not negotiable.**

Before changing ANY analysis code, you MUST:
1. Load the workflow context
2. Identify WHAT is wrong (specific, not vague)
3. Identify WHY it's wrong (root cause)
4. Only THEN fix it (with output-first verification)

**If you're about to change code without diagnosing first, STOP.**
</EXTREMELY-IMPORTANT>

### Drive-Aligned Framing

**Skipping diagnosis is NOT HELPFUL — guessing at a root cause wastes the user's time when the real bug resurfaces.** Your guess is not a diagnosis. Your assumption is not evidence.

### Drive-Aligned Framing (Consequences)

| Shortcut | Consequence |
|----------|-------------|
| Skipping diagnosis | You skipped diagnosis because you thought you were smart enough to guess. A checklist would outperform you. |
| Fixing without understanding | You applied a patch without understanding the root cause. The bug returns in a different form — your fix was cosmetic. |

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I can see the bug from the error message" | Error messages show symptoms, not causes. The traceback tells you WHERE, not WHY. | Trace backwards through the pipeline to find the first divergence point |
| "This is the same bug as last time" | Similar symptoms can have different root causes. Pattern-matching from memory is not diagnosis. | Diagnose fresh — compare against LEARNINGS.md for prior context, but verify independently |
| "The fix is obvious" | Obvious fixes mask deeper issues. The "obvious" fix is usually a patch over the symptom. | Identify root cause first, then fix. If it's truly obvious, diagnosis takes 30 seconds. |
| "I'll just rerun and see if it works" | Retry without understanding is cargo cult debugging. If you don't know why it failed, you don't know why it passed. | Diagnose the failure, fix the cause, then rerun to verify |
| "The data probably changed" | Verify before assuming external cause. Blaming data without evidence is a cop-out. | Compare data profiles before/after — shape, dtypes, distributions, nulls |

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "I'll just re-run everything" | Brute force hides root cause | Trace to the specific failing step |
| "The data probably changed" | Your guess isn't a diagnosis | Compare data profiles before/after |
| "Let me tweak the parameters" | Tweaking without understanding is p-hacking | Understand WHY parameters are wrong first |
| "I'll fix it and check later" | You're skipping output-first | Fix AND verify in the same step |

## Step 1: Load Context

Read workflow state, shared enforcement, AND shared check definitions:

Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-constraints.md` for the full constraint index.

As the midpoint, load ALL common constraints (can route to any phase):
Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-data-quality-checks.md`
Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-post-subagent-boundary.md`
Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-deviation-rules.md`

Load ALL common conventions (midpoint can route to any phase):
Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-conventions.md` for the full convention index.
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-assumption-over-evidence.md`
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-deferred-verification.md`
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-impatience-over-process.md`
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-topic-change-protocol.md`
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-escape-patterns.md`

```
Read(".planning/SPEC.md")
Read(".planning/PLAN.md")
Read(".planning/LEARNINGS.md")
```

Read `${CLAUDE_SKILL_DIR}/../../skills/ds-implement/references/ds-checks.md` and follow its instructions.

**The shared checks file contains data quality check definitions (DQ1-DQ6, M1, R1) used by both ds-review and ds-fix.** Loading it here ensures the midpoint runs identical checks to the entry point's review phase. Without it, checks drift apart and the midpoint misses issues review would catch.

If no workflow state exists, suggest starting with `/ds` instead.

### SAS Project Detection

After loading PLAN.md, check if `Implementation Language` is `SAS` or `Mixed`. If so, reload SAS enforcement before any fix:

Read `${CLAUDE_SKILL_DIR}/../../skills/wrds/references/sas-etl.md` and follow its instructions.

**SAS projects have unique failure modes** (hash merge memory, WHERE function wrapping, SGE array misconfiguration). The SAS enforcement must be loaded BEFORE diagnosing — otherwise you will misdiagnose SAS-specific issues as generic bugs.

### Context Monitoring

Before starting diagnosis, check context availability:

| Level | Remaining Context | Action |
|-------|------------------|--------|
| Normal | >35% | Proceed with diagnosis and fix |
| Warning | 25-35% | Complete current fix, then invoke ds-handoff |
| Critical | ≤25% | Invoke ds-handoff immediately — no new fixes |

**At Warning level:** After current fix completes, invoke:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-handoff/SKILL.md` and follow its instructions.

**Why:** A multi-step fix pipeline with 20% context remaining produces degraded output. Better to handoff cleanly and resume fresh.

## Step 2: Diagnose

Identify the issue category:

| Category | Symptoms | Route To |
|----------|----------|----------|
| **Runtime Error** | Traceback, cell failure, import error | Debug Protocol |
| **Wrong Results** | Numbers don't match expectations, sanity checks fail | Re-analysis Protocol |
| **Unclear Root Cause** | 3+ plausible explanations, mysterious data quality issues | Competing Hypothesis Investigation |
| **Reviewer Feedback** | Specific methodology concerns, requested changes | Revision Protocol |
| **Data Change** | New data available, source updated, schema changed | Re-profiling Protocol |
| **Scope Change** | New questions, expanded requirements | Spec Update → re-plan |

Ask user if ambiguous:

```
AskUserQuestion(questions=[
  {
    "question": "What needs fixing in your analysis?",
    "header": "Issue type",
    "options": [
      {"label": "Runtime error", "description": "Code fails, traceback, import error"},
      {"label": "Wrong results", "description": "Numbers don't look right, sanity checks fail"},
      {"label": "Unclear root cause", "description": "Multiple plausible explanations, mysterious data quality"},
      {"label": "Reviewer feedback", "description": "Specific changes requested by reviewer"},
      {"label": "Data/scope change", "description": "New data, updated requirements, new questions"}
    ],
    "multiSelect": false
  }
])
```

### Diagnostic Routing Flowchart

```
┌───────────────────────┐
│  Load Context (Step 1) │
│  SPEC + PLAN + LEARN   │
└───────────┬───────────┘
            ▼
┌───────────────────────┐
│  Identify Symptoms     │
│  (Step 2)              │
└───────────┬───────────┘
            ▼
     ┌──────┴──────┐
     │  Traceback?  │─── YES ──→ Debug Protocol
     └──────┬──────┘              (Runtime Error)
            │ NO
            ▼
     ┌──────────────┐
     │ Numbers wrong │─── YES ──→ Re-analysis Protocol
     │ or unexpected?│              (Trace backwards)
     └──────┬───────┘
            │ NO
            ▼
     ┌──────────────┐
     │ 3+ plausible │─── YES ──→ Competing Hypothesis
     │ explanations?│              (Parallel investigation)
     └──────┬───────┘
            │ NO
            ▼
     ┌──────────────┐
     │ Reviewer      │─── YES ──→ Revision Protocol
     │ feedback?     │              (Fix per feedback)
     └──────┬───────┘
            │ NO
            ▼
     ┌──────────────┐
     │ Data or scope │─── YES ──→ Re-profiling / Spec Update
     │ changed?      │
     └──────────────┘
```

**This flowchart IS the diagnostic spec.** If the category table and flowchart disagree, the flowchart wins.

## Step 3: Fix by Category

### Runtime Error → Debug Protocol

1. Identify the failing cell/script
2. Read the error traceback
3. Check LEARNINGS.md for prior context on this step
4. Fix with output-first verification:
   - Print state BEFORE the failing operation
   - Fix the operation
   - Print state AFTER
   - Verify output matches expectations from PLAN.md

For notebook-specific errors, load notebook-debug patterns:

Read `${CLAUDE_SKILL_DIR}/../../skills/notebook-debug/SKILL.md` and follow its instructions.

### Wrong Results → Re-analysis Protocol

<EXTREMELY-IMPORTANT>
**Trace backwards. Do NOT guess forward.**

The bug is at the FIRST step where output diverges from expected. Find that step.
</EXTREMELY-IMPORTANT>

1. Identify WHICH results are wrong
2. Trace backwards through the pipeline:
   - Check final output → is the aggregation wrong?
   - Check intermediate data → is the transformation wrong?
   - Check input data → is the loading/filtering wrong?
3. Find the FIRST step where output diverges from expected
4. Fix that step with output-first verification
5. Re-run downstream steps and verify

### Reviewer Feedback → Revision Protocol

1. Document each piece of feedback as a task
2. For each task:
   - Locate the relevant code/output
   - Apply the change
   - Verify with output-first protocol
   - Document in LEARNINGS.md
3. After all changes, re-run review checks:

Read `${CLAUDE_SKILL_DIR}/../../skills/ds-review/SKILL.md` and follow its instructions.

### Data/Scope Change → Re-profiling Protocol

1. Profile the new data (shape, dtypes, distributions)
2. Compare to original data profile in LEARNINGS.md
3. Identify what changed (schema, volume, distributions)
4. Update PLAN.md if pipeline steps need changing
5. Re-run affected pipeline steps with output-first verification
6. Update LEARNINGS.md with new observations

### Scope Change → Spec Update

If the question itself changed:

1. Update SPEC.md with new objectives
2. Review PLAN.md — which tasks are still valid?
3. Add new tasks for new objectives
4. Return to implement phase for new tasks

### Unclear Root Cause → Competing Hypothesis Investigation

When 3+ plausible explanations exist, sequential investigation failed, or contradictory evidence is found, use the competing hypothesis protocol.

**MANDATORY:** Before proceeding, load the protocol:
```
Read("references/competing-hypothesis.md")
```

Key steps:
1. Generate 3-5 competing hypotheses (Data Quality, Methodology, Implementation, Domain)
2. Spawn investigation team (one agent per hypothesis)
3. Scientific debate with cross-examination
4. Evidence synthesis with confidence scoring (≥90 to proceed)
5. Fix implementation via ds-delegate

## Step 4: Verify Fix

After fixing, apply output-first verification:

1. Re-run the fixed step: verify output shape, sample, stats
2. Re-run downstream steps: verify no cascading issues
3. Check against SPEC.md success criteria
4. Update LEARNINGS.md with fix documentation

### Gate: Fix Verification

**Checkpoint type:** human-verify (fix output is machine-verifiable)

Before claiming any fix is done, execute this gate:

```
1. IDENTIFY → What specific behavior was broken? (not vague — exact symptom)
2. RUN      → Execute the fixed code with output-first verification
3. READ     → Read the output: does it match SPEC.md success criteria?
4. VERIFY   → Re-run downstream steps — no cascading failures introduced
5. CLAIM    → Only declare "fix complete" if ALL gates pass
```

**Skipping this gate means your fix is unverified. An unverified fix is not a fix — it's a guess.**

## Post-Subagent Boundary

<EXTREMELY-IMPORTANT>
**After a fix agent returns, constraints C5 from ds-common-constraints.md apply.**

**ALLOWED:** Read the agent's returned report. Check LEARNINGS.md. Confirm file existence with `ls`.
**FORBIDDEN:** Read project source code, run analysis code, inspect data files, Grep/Glob project files.

**If the fix looks incomplete, re-dispatch a Task agent. Do NOT investigate yourself.**
</EXTREMELY-IMPORTANT>

## Topic Change Protocol

**If user sends an off-topic message during ds-fix, follow C6 from ds-common-constraints.md:**

1. Announce: "Pausing ds-fix to address your request."
2. Handle the request.
3. Announce: "Resuming ds-fix. Reading state files for current progress."
4. Reload: Read `.planning/SPEC.md`, `.planning/PLAN.md`, `.planning/LEARNINGS.md`.
5. Resume from where you left off.

## Delegation

Main chat orchestrates. Task agents do the fixing:

```
Task(subagent_type="general-purpose", prompt="""
Fix [SPECIFIC ISSUE] in the analysis.

Context:
- Read .planning/LEARNINGS.md for prior steps
- Read .planning/PLAN.md for task details
- Read .planning/SPEC.md for objectives

Fix Protocol:
1. Trace to root cause (do NOT guess)
2. Fix with output-first verification
3. Print state BEFORE and AFTER fix
4. Re-run downstream steps
5. Update LEARNINGS.md

Report: what was wrong, what was fixed, verification output.
""")
```

## When Fix Requires Rethinking

If the fix reveals the analysis approach is fundamentally wrong:

1. Document findings in LEARNINGS.md
2. Report to user: "The approach needs rethinking because [specific reason]"
3. Suggest returning to `/ds` for re-planning

Don't try to salvage a broken approach with patches. A fresh plan costs less than cascading fixes.
