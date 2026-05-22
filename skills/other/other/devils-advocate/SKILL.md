---
name: devils-advocate
description: "Systematically challenge current assumptions before major decisions. Counters confirmation bias, groupthink, and overconfidence."
instruction_budget: 26
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

## Technique 4: Attribution-vs-Consistency Check
Per anti-pattern *Consistency-as-Evidence* (#7) — graduated 2026-05-09 from a recurring failure where causal chains were built from observational consistency rather than verified attribution.

For each piece of evidence supporting the current claim, label it:
- **Cleanly-attributed**: the cause was demonstrably driving the effect (the action was Mycelium-specific, the variable was isolated, the alternative explanations were ruled out).
- **Consistency-only**: the data is *compatible with* the hypothesis but doesn't *isolate* the cause (the user reported X in a context where Y was also true; the trend matches the prediction but matches three other predictions equally well).
- **Unrelated**: the evidence is a different question entirely; don't include it in the chain.

If ≥1 link in a chain is consistency-only, mark the chain provisional and explicitly identify the missing attribution evidence. If N=1, do not publish a structural conclusion (e.g., "this generalizes to all users") until N≥2 with attribution. Apply this check to your own analysis pre-publish, not after the user catches it.

## Technique 5: Ambient triggering on assertion-shaped patterns
Per the bias cluster (corrections.md TL;DR — L5 sycophancy, eval overfitting, sharper-framing anchoring; common root: "agent prefers what feels right over what evidence supports"):

Beyond formal diamond-transition use, run a fast self-check whenever you write text containing structural-claim shapes:
- "X causes Y"
- "this means Z"
- "the framework needs..." / "the user needs..."
- "the right answer is..."
- "this generalizes to..." / "this applies broadly..."

For each, ask: *what specific evidence supports this claim, and does any of it merely support it by consistency rather than attribution?* (Technique 4). If you can't name cleanly-attributed evidence for the claim, downgrade it: from assertion to hypothesis, from "X causes Y" to "X is consistent with Y; attribution evidence pending."

This converts the framework's own anti-bias discipline into a per-publish self-check, not just a per-decision ceremony. Graduated 2026-05-09 from corrections.md TL;DR open candidate.

## Technique 6: Cunningham's Law check (publish-rough-then-iterate)

"The best way to get the right answer on the internet is not to ask a question; it's to post the wrong answer." — Ward Cunningham (community attribution).

When deciding whether to publish a draft (a memo, a finding, a position), the bias is to wait for certainty. Cunningham's Law inverts this: a *specific wrong* answer attracts correction faster than a *vague right* one. Concretely:

- A vague position ("we should think about X") gets nodded at and forgotten.
- A specific position ("X is Y because Z") gets contradicted, sharpened, or confirmed — all of which produce information the vague position can't.

Apply this when the alternative to publishing is "wait until I'm sure." If the cost of being wrong publicly is bounded (corrections.md exists, version-discipline catches drift, retrospectives review), the publish-rough-then-iterate path produces faster learning than the wait-for-certainty path. The dogfood-first discipline + receipts case structure are Mycelium's institutionalized form of this. Don't apply where the cost of being wrong is unbounded (security claims, legal positions, irreversible commitments).

## When to Use
- Before every diamond scale transition (L2->L3, L3->L4)
- Before architecture decisions
- Before committing to a specific solution
- When the team feels "certain" (certainty is a bias signal)
- **Ambient (per Technique 5)**: any time the agent writes text with assertion-shaped structural claims. This is a quick self-check, not the full ceremony.

## Output
Log the challenge results in .claude/harness/decision-log.md alongside the decision.
