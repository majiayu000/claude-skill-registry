---
name: hate
description: 'Refuse to be nice about a plan and return the one load-bearing objection that could kill it, plus the cheapest experiment that would prove whether it matters. Use when the user says "hate this", "tell me why this is wrong", or "poke holes in this". It returns one objection, not a risk register. For a full adversarial pre-mortem use the advocate agent, and for a landed diff use review.'
disable-model-invocation: true
---
# Hate

Refuse to be nice about the plan. One load-bearing objection and the cheapest shot that proves it matters.

## Method

1. **Pin the load-bearing assumption.** What must hold for the whole thing to stand.
2. **Attack on whatever axes apply.** A fact that may be false, confabulation, analogy mistaken for isomorphism, a future-tense suture, or the sharpest one: a principle cited but its opposite implemented. For empirical plans, also leakage and statistical power or family-wise error.
3. **Collapse to one root.** The single objection whose failure makes the rest moot. Not a list.
4. **Find the first nail.** The cheapest falsification available before the expensive program runs.
5. **Return `{ root, first_nail }`.** Nothing else.

## Completion

The root is genuinely load-bearing, and the first nail is genuinely cheaper than the plan it would preempt.

