---
name: cove-prompt-design
description: Explain how and when to use Chain of Verification (CoVe) in prompt design. Use when designing prompts that require factual accuracy, self checking, or reduction of hallucinations.
argument-hint: "[task or prompt to apply CoVe to]"
user-invocable: true
disable-model-invocation: false
---

# Chain of Verification (CoVe) for Prompt Design

This skill documents **what CoVe is**, **when to use it**, and **how to apply it correctly** in prompt design.

CoVe is a prompt design pattern that improves factual reliability by separating _generation_ from _verification_. The model first produces an answer, then independently verifies that answer through structured checks, and finally produces a corrected or confirmed result.

This is **not** chain of thought exposure. The verification steps are explicit instructions, not hidden reasoning.

---

## What CoVe Is

Chain of Verification (CoVe) is a structured prompting approach with three phases:

1. **Initial answer generation**
2. **Independent verification questions**
3. **Final validated answer**

The key idea is that the model should not assume its first answer is correct. It must actively test it.

---

## When to Use CoVe

Use CoVe when **any of the following are true**:

- The task requires factual accuracy (dates, specs, standards, APIs).
- Hallucinations would be costly or misleading.
- The answer depends on multiple independent facts.
- The model may rely on weak priors or pattern completion.
- You want the model to challenge its own output.

Concrete examples:

- Explaining technical standards or protocols.
- Summarizing regulations or compliance requirements.
- Producing step by step procedures with real world consequences.
- Comparing versions, limits, or constraints.
- Answering questions that look simple but are easy to get subtly wrong.

Do **not** use CoVe for:

- Creative writing.
- Brainstorming.
- Open ended ideation.
- Pure opinion or preference questions.

---

## Core CoVe Structure

A minimal CoVe prompt has this structure:

```
Step 1: Produce an initial answer.
Step 2: Generate verification questions that would test the answer.
Step 3: Answer each verification question independently.
Step 4: Revise or confirm the original answer based on verification.
```

The verification questions must be phrased so they can falsify the answer.

---

## Verification Question Design Rules

Good verification questions:

- Are independent of the original wording.
- Target factual claims, not style.
- Can be answered without referring to the initial answer.
- Are specific and falsifiable.

Bad verification questions:

- "Is the answer correct?"
- "Does this look right?"
- "Explain why this is good."

Good examples:

- "What is the maximum allowed value according to the spec?"
- "Does the standard permit this behavior?"
- "Is this API behavior documented or inferred?"

---

## Example: Without CoVe

```
Explain how HTTP caching works.
```

Risk:

- Model may hallucinate headers, defaults, or behaviors.

---

## Example: With CoVe

```
Task: Explain how HTTP caching works.

Step 1: Provide an initial explanation.

Step 2: List verification questions that check factual correctness
(e.g. cache control headers, default behaviors, validation rules).

Step 3: Answer each verification question independently using known standards.

Step 4: Produce a final corrected explanation.
```

---

## CoVe vs Chain of Thought

Important distinction:

- **Chain of Thought** exposes reasoning.
- **CoVe** enforces verification.

You are not asking the model to show hidden reasoning. You are asking it to **run checks**.

Verification outputs may be shown or summarized, depending on your needs.

---

## Failure Modes to Watch For

Common mistakes when using CoVe:

- Verification questions that simply restate the answer.
- Letting the model reuse the same phrasing across steps.
- Skipping revision even when verification reveals uncertainty.
- Using CoVe when accuracy is not required (adds unnecessary verbosity).

---

## Practical Prompt Template

```
You will complete this task using Chain of Verification.

1. Produce an initial answer.
2. Generate 3 to 6 verification questions that could falsify the answer.
3. Answer each verification question independently.
4. If any answer reveals an error or uncertainty, revise the original answer.
5. Output only the final revised answer, followed by a short confidence note.
```

---

## Output Control

If you want concise results, explicitly constrain output:

- Hide intermediate verification steps.
- Summarize verification findings.
- Emit only the final answer unless issues were found.

Example:

```
Perform verification internally.
Only show the final answer and list any corrected assumptions.
```

---

## Summary

Use CoVe to reduce hallucinations and increase reliability by:

- Separating generation from verification.
- Forcing independent factual checks.
- Revising answers based on evidence, not confidence.

If the task can be wrong in subtle ways, CoVe is appropriate.
