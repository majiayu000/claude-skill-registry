---
name: devils-advocate
description: "Systematically challenge current assumptions before major decisions. Counters confirmation bias, groupthink, and overconfidence."
---

# Devil's Advocate

Run before every major diamond transition and architecture decision. Source: Kahneman, Shotton.

## Technique 1: Pre-Mortem
Imagine it's 6 months from now and this decision FAILED spectacularly.
1. What went wrong?
2. What assumption was the weakest link?
3. What signal did we ignore?
4. Who was affected and how?

## Technique 2: Assumption Reversal
For each key assumption:
- State the assumption explicitly
- Ask: "What if the OPPOSITE is true?"
- What evidence would support the opposite?
- Is there any evidence we've dismissed?

## Technique 3: Red Team
Attack your own position:
- What would a competitor say about this approach?
- What would a skeptical user say?
- What would a security auditor find?
- What would an accessibility advocate flag?

## 10 Challenge Questions
1. What are we most confident about? (That's where overconfidence hides)
2. What evidence have we dismissed or downweighted?
3. Are we anchored on our first idea? (Shotton - anchoring bias)
4. Have we tested with users who DON'T match our ideal profile?
5. What would make us abandon this direction entirely?
6. Are we building for ourselves or for actual users?
7. What's the simplest version that could validate/invalidate this?
8. What have we NOT measured that we should?
9. If we had to start over, would we make the same choice?
10. Who disagrees with us and what's their strongest argument?

## When to Use
- Before every diamond scale transition (L2->L3, L3->L4)
- Before architecture decisions
- Before committing to a specific solution
- When the team feels "certain" (certainty is a bias signal)

## Output
Log the challenge results in decision-log.md alongside the decision.
