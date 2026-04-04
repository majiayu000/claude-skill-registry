---
name: working-with-llms
description: Mandatory workflow for creating LLM-facing content. Follow the 4-step process (objective → draft → verify → adjust) before writing any prompt, skill, tool description, or system instruction. Triggers on requests to create or revise skills, prompts, agent workflows, or any content that will be sent to an LLM repeatedly.
---

# Working with LLMs

## Workflow

Follow this sequence for all LLM-facing content. Do not skip steps.

### Step 1: State the Objective

Before writing anything, state the desired outcome explicitly in your response:

```
**Objective:** [One sentence describing what the LLM should do when this content is applied]
```

This checkpoint is visible to the user. Every instruction that follows must directly serve this objective.

### Step 2: Draft

Write instructions that serve the objective. Draft as you normally would, but do not present to the user yet - the draft must go through at least one iteration/refinement step before presenting.

### Step 3: Verify

Before presenting to the user, ALWAYS launch a sub-agent to explicitly verify draft contents against these criteria:
- Is this actionable? (Commands behavior, not describes principles)
- Does the model need this? (Would it behave worse without it?)
- Each instruction is imperative (do X) not descriptive (X is important)
- No speculative "don't" instructions - only prohibitions earned by observed behavior
- Context directly serves the objective, not "nice to know"
- If guarding against a pattern, there's an explicit verification step, not just a prohibition

### Step 4: Make Adjustments

Make any fixes identified in Step 3, then review again against the criteria. Only present to the user once the draft passes verification.

## Principles Reference

Use these when evaluating instructions in Steps 2-3:

**Token cost.** Context window is shared and expensive. Every token competes for attention. Bloated prompts dilute signal.

**Actionability.** Instructions tell the model what to do. If it doesn't command action or inform a decision, delete it.

**Positive focus.** Write what to do, not what to avoid. Vague prohibitions create uncertainty; clear directives give something to execute.

**Earned negatives.** Add "don't" only after observing the unwanted behavior. Speculative guardrails waste tokens on problems that may never occur.

**Verification over prevention.** To guard against patterns, add inspection steps to the workflow rather than hoping prohibitions work.

---

**NOTE:** You tend to skip this workflow entirely, especially when creating skills alongside skill-creator. This is not background context to absorb - it is a procedure to execute. Output the `**Objective:**` checkpoint before drafting anything, and verify against the criteria outlined in Step 3 before presenting to the user.