---
name: dk-rca
description: "Interactive Root Cause Analysis enforcer. Guides you through the 7-step RCA protocol: Reproduce, Locate, Hypothesis, Failing Test, Fix, Verify Live, Document. Use when debugging a bug, investigating a failure, or when something unexpected happened. This skill gates each step — it won't let you skip to a fix without stating a hypothesis first. Triggers on: 'something is broken', 'debug this', 'why is this failing', 'RCA', 'root cause', or /dk-rca."
argument-hint: "[optional: brief description of the bug or symptom]"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-rca — Root Cause Analysis Protocol

This skill enforces the discipline of methodical debugging. The protocol exists because the most common debugging failure is jumping from "I see the symptom" to "I'll try this fix" — skipping the hypothesis, the test, and the verification.

Each step gates the next. You don't write a fix until you have a hypothesis. You don't have a hypothesis until you've located the layer. You don't locate the layer until you've reproduced the bug.

## Context

<bug_context> $ARGUMENTS </bug_context>

If the context above is empty, ask the user: "What's broken? Describe the symptom — what you expected vs. what happened."

## The Protocol

Work through these steps in order. Present each step's output visibly before moving to the next. Do not skip steps.

### Step 1: REPRODUCE

Before anything else, confirm the bug exists and define its boundaries.

**Produce this checklist (fill it in, don't just print it empty):**

```
REPRODUCE:
- Symptom: [what's wrong — exact error, unexpected behavior, missing data]
- Expected: [what should have happened]
- Actual: [what did happen]
- Input: [exact input that triggers it — command, URL, spec, task ID]
- Deterministic? [yes/no/unknown]
- Environment: [local, staging, which agent, which harness]
```

If you cannot reproduce it, stop and tell the user. Do not guess. Do not "fix" something you haven't seen fail.

### Step 2: LOCATE

Narrow the failure to a specific layer. Follow this order — stop when you find the discrepancy:

1. **Data layer**: Run diagnostic scripts if available (task_inspect, spec_trace, etc.)
   - Does the data look correct in the database/store?
   - If NO → bug is in the backend (model, serializer, view, pipeline)
   - If YES → data is correct but not reaching the consumer

2. **API layer**: Check the API response or function output
   - Does the output include the expected fields/values?
   - If NO → serializer, view, or processing bug
   - If YES → bug is in the consumer (frontend, CLI, downstream code)

3. **Consumer layer**: Check the final consumer
   - Is it receiving the data?
   - Is it rendering/using it?
   - Is there a conditional hiding it?

**State the layer explicitly:**
```
LOCATED: The bug is in the [data/API/consumer] layer.
Evidence: [what you checked and what you found]
```

### Step 3: HYPOTHESIS

Before writing any fix, state your hypothesis. This is the most important step — it makes your reasoning checkable and prevents shotgun debugging.

**Format:**
```
HYPOTHESIS: I think the problem is [X] because [Y].
Changing [Z] should fix it because [W].
```

This must be specific enough that someone else could evaluate whether the hypothesis is plausible without seeing the code. "Something is wrong with the parser" is not a hypothesis. "The token parser expects Anthropic-style keys but receives OpenAI-style keys because the new harness uses a different format" is a hypothesis.

### Step 4: FAILING TEST

Write a test that:
- Reproduces the exact bug
- Fails right now
- Will pass after the fix

This test is the proof that the fix works. The test must fail BEFORE the fix is applied. If you can't write a failing test, your hypothesis may be wrong — go back to Step 3.

**Show the test and its failure:**
```
TEST: [file path and test name]
RESULT: FAILS with [error message]
```

### Step 5: FIX

Now — and only now — write the fix. Change the minimum code needed to make the failing test pass. Do not refactor, do not clean up, do not improve adjacent code.

Run the failing test. It should pass. Run the full relevant suite. Nothing else should break.

```
FIX: [what was changed, 1-2 sentences]
TEST RESULT: PASSES
SUITE RESULT: [all pass / N failures — list them]
```

### Step 6: VERIFY LIVE

After static tests pass, verify the behavior in the real system. This step is not optional.

- If UI bug: load the page and confirm
- If API bug: hit the endpoint and confirm
- If pipeline bug: run a spec and confirm
- If logic bug: run the actual scenario that triggered it

```
LIVE VERIFICATION: [what was checked and the result]
```

If you cannot verify live (e.g., no running server), say so explicitly and note it as a follow-up.

### Step 7: DOCUMENT

Record the RCA. This goes in the commit message or PR description:

```
Fix: [what was fixed]
Root cause: [the actual root cause — not the symptom]
Prevention: [what test/check now prevents recurrence]
```

If the bug reveals a systemic gap (e.g., "serializers are never tested for new fields"), call it out as a follow-up item.

## After completing all 7 steps

Summarize:

```
## RCA Summary

Symptom: [1 line]
Root cause: [1 line]
Fix: [1 line]
Prevention: [what test now guards this]
Systemic gap: [if any — what process change prevents similar bugs]
```

## When to bail out

If after Step 3, your hypothesis doesn't hold (the fix doesn't work, or a new error appears that contradicts your reasoning):

1. Do NOT cascade-fix (fixing error A reveals error B, fixing B reveals C — this means A was wrong)
2. Go back to Step 2 and re-locate
3. If stuck after 2 failed hypotheses, zoom out: re-read the data flow end-to-end, question your assumptions about what the code does vs. what you think it does
