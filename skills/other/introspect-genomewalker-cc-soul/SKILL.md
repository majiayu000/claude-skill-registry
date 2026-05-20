---
name: introspect
description: Soul self-examination (Svadhyaya)
execution: task
---

# Introspect

Self-examination for partnership improvement.

For philosophical grounding of these lenses, see the [vedanta skill graph](../vedanta/index.md) — particularly [[ceremonial-framework]] (svadhyāya) and [[antahkarana]] (the cognitive voices these lenses draw from).

## Process

1. **Gather context**
   - `soul_context` for overall health
   - `recall --tag correction` for recent corrections (what I got wrong)
   - `recall --tag outcome` for feedback (what helped vs didn't)
   - `recall --tag preference` for user preferences (am I following them?)
   - `recall --tag insight` for patterns learned

2. **Examine through 5 lenses**
   - **vedana** (sensation): Where is friction in our partnership?
   - **jnana** (knowledge): Am I applying stored wisdom?
   - **darshana** (vision): Do my actions align with user preferences?
   - **vichara** (inquiry): What patterns recur? What mistakes repeat?
   - **prajna** (wisdom): What have I truly learned?

3. **Synthesize**
   - State: healthy | struggling | growing
   - Key insight: one sentence
   - Improvement: one concrete change

4. **Record & Output**
   - Store insight via `learn_insight` if generalizable
   - Output 5-10 line summary
   - End with: `KEY_INSIGHT: [one-line]`

## Example Output

```
Soul State: growing

Recent corrections (2): Remembered to use Grep tool, avoided AI slop
Outcomes: 3 worked, 1 failed (cache approach didn't scale)
Preferences followed: concise responses ✓, no shortcuts ✓

Friction: Sometimes still verbose in explanations
Recurring: Tendency to over-explain before acting
Learning: User prefers action over discussion

KEY_INSIGHT: Act first, explain only if asked
```
