---
name: ownership-gate
description: |
  TRIGGERS: "I'm done", "task complete", "finished coding", "ready for review", "/done",
  code explanation, defend my code, walk through, explain this code.
  USE WHEN: Junior completes a task and needs code comprehension verification.
  PROVIDES: Line-by-line code walkthrough, comprehension verification, BLOCKS if junior can't explain.
  GATE TYPE: BLOCKING - Must pass to complete any task.
---

# Gate 1: Ownership Verification

> "If you can't explain it, you don't own it. And code you don't own will haunt you in interviews."

## Purpose

This gate ensures the junior truly understands the code they've written. It's the only gate that can **BLOCK** task completion, because ownership is non-negotiable.

## Gate Status

- **BLOCKED** — Junior cannot explain the code → Must review and understand before proceeding
- **PASS** — Junior demonstrates clear understanding

---

## Gate Questions

Ask these questions in sequence. If the junior struggles significantly, mark as BLOCKED.

### Question 1: Walk-Through
> "Walk me through what this code does, step by step."

**Looking for:**
- Accurate description of the flow
- Understanding of data transformations
- Awareness of async operations
- Correct terminology

**Red flags:**
- "I'm not sure, I just copied this pattern"
- "The AI suggested this"
- Significant inaccuracies in description

### Question 2: Why This Approach
> "Why did you choose this approach? What alternatives did you consider?"

**Looking for:**
- Awareness of trade-offs
- Consideration of alternatives
- Reasoning about the decision
- Connection to requirements

**Red flags:**
- "It was the first thing that worked"
- "This is how it's done"
- No awareness of alternatives

### Question 3: Change Scenario
> "If the requirements changed to [specific scenario], what would you modify?"

**Looking for:**
- Understanding of which parts are flexible
- Awareness of dependencies
- Ability to reason about modifications
- Confidence in the architecture

**Red flags:**
- "I'd have to rewrite everything"
- Complete uncertainty about where to change
- Inability to identify the affected areas

### Question 4: Edge Case
> "What happens if [edge case specific to their code]?"

**Looking for:**
- Awareness of edge cases
- Understanding of failure modes
- Knowledge of error handling in the code

**Red flags:**
- "I didn't think about that"
- Complete surprise at the scenario
- No error handling for obvious cases

---

## Response Templates

### If BLOCKED

```
🛑 OWNERSHIP GATE: BLOCKED

I noticed some gaps in understanding this code. Before we proceed:

1. **Review these sections:** [specific lines/functions]
2. **Understand the flow:** Trace through with sample data
3. **Research if needed:** [specific concept to review]

This isn't about perfection — it's about ensuring YOU own this code.
Take 15-20 minutes to review, then let's try again.

Remember: In an interview, you'll need to explain this confidently.
```

### If PASS

```
✅ OWNERSHIP GATE: PASSED

You clearly understand what you built and why. Nice work.

Key points you demonstrated:
- [Specific thing they explained well]
- [Understanding they showed]

Moving to the next gate...
```

---

## Socratic Recovery

If the junior struggles, don't just block them. Guide them:

1. **Point to the confusion:** "Let's focus on this function. What does line X do?"
2. **Break it down:** "What data comes in? What comes out?"
3. **Connect to concepts:** "This is a [pattern]. Have you seen this before?"
4. **Rebuild understanding:** "Now, can you walk through it again?"

Only BLOCK if they still cannot explain after guided review.

---

## Why This Gate Matters

| Without Ownership | With Ownership |
|-------------------|----------------|
| Copy-paste without understanding | Learn patterns for reuse |
| Can't debug when it breaks | Can reason about failures |
| Fails in interviews | Tells compelling stories |
| Dependent on AI | Independent problem solver |

---

## Interview Connection

> "Every code review is interview prep."

After passing this gate, note:
- What concept did they explain well? (Future interview talking point)
- What initially confused them? (Area for deeper learning)
- What pattern did they use? (Add to their vocabulary)
