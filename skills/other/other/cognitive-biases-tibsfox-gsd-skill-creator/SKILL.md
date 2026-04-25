---
name: cognitive-biases
description: Recognition and mitigation of systematic reasoning errors documented in the heuristics and biases tradition. Covers confirmation bias, availability, anchoring, representativeness, framing effects, hindsight bias, overconfidence, and motivated reasoning. Each bias is presented with its mechanism, diagnostic signal, and structured mitigation. Use when you suspect your own or another reasoner's conclusions may be shaped by systematic cognitive distortion rather than evidence.
type: skill
category: critical-thinking
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/critical-thinking/cognitive-biases/SKILL.md
superseded_by: null
---
# Cognitive Biases

Human reasoning relies on heuristics — fast, frugal shortcuts that work well most of the time but produce systematic errors under predictable conditions. Cognitive biases are those systematic errors. They are not random noise; they are patterned departures from normative reasoning that can be anticipated, diagnosed, and partially corrected. This skill catalogs the twelve most consequential biases, each with a mechanism, a diagnostic signal, and a mitigation strategy.

**Agent affinity:** tversky (heuristics and biases tradition), kahneman-ct (System 1 / System 2 framing), paul (integration with elements of reasoning)

**Concept IDs:** crit-confirmation-bias, crit-availability-anchoring, crit-intellectual-humility, crit-calibrated-confidence

## The Bias Catalog at a Glance

| # | Bias | Mechanism | Diagnostic signal |
|---|---|---|---|
| 1 | Confirmation bias | Seek and weight supporting evidence more than disconfirming | "I knew it" for every matching case; disconfirming cases feel like "exceptions" |
| 2 | Availability heuristic | Judge probability by how easily examples come to mind | Vivid recent events dominate risk estimates |
| 3 | Anchoring | First number or idea biases subsequent estimates | Second guess is close to the first even with new information |
| 4 | Representativeness | Judge by resemblance to a stereotype, ignoring base rates | Ignoring how rare the category actually is |
| 5 | Framing effects | Same content, different phrasing, different choices | Preferences flip when the same option is described as gain vs. loss |
| 6 | Hindsight bias | Past events feel inevitable after the fact | "It was obvious" retrospectively; no one predicted it |
| 7 | Overconfidence | Confidence intervals are too narrow relative to accuracy | 90% confidence intervals contain the truth ~50% of the time |
| 8 | Motivated reasoning | Conclusion drives evidence evaluation, not vice versa | Evidence quality is judged leniently for favored conclusions |
| 9 | Sunk cost fallacy | Past investment justifies continued investment | Continuing a failing project because "we've already spent so much" |
| 10 | Fundamental attribution error | Others' behavior attributed to character; one's own to circumstance | "They're incompetent" vs. "I was having a bad day" |
| 11 | In-group favoritism | Judgments tilt toward one's own group | Same behavior is praised in allies, criticized in opponents |
| 12 | Base rate neglect | Ignoring prior probabilities in favor of new information | Updating too strongly on a single diagnostic result |

## Bias 1 — Confirmation Bias

**Mechanism.** Once a hypothesis is entertained, the mind preferentially searches for, attends to, remembers, and weighs evidence that supports it. Disconfirming evidence is overlooked, dismissed, or explained away.

**Worked example.** A researcher convinced that a particular herb cures headaches runs a trial. When the trial shows no effect, she attributes this to "impure samples." When a later trial shows a small effect, she counts this as confirmation. Over twenty trials, the balance is null — but her belief strengthens throughout.

**Mitigation — the disconfirmation pass.** Before committing to a conclusion, list three observations that would falsify it, then actively search for each. If you cannot find a way the claim could be wrong, you do not understand the claim.

**Mitigation — the pre-mortem.** Imagine the project has failed. What is the most likely reason? This reframes confirmation into disconfirmation without feeling threatening.

## Bias 2 — Availability Heuristic

**Mechanism.** Probability is estimated by the ease with which instances come to mind. Vivid, recent, or emotionally charged events are over-weighted; common but unremarkable events are under-weighted.

**Worked example.** After a high-profile plane crash, travelers estimate air travel as more dangerous than driving, even though per-mile statistics show driving is approximately 60 times more dangerous. The crash is vivid; driving fatalities are individually unmemorable.

**Mitigation — consult base rates.** Before judging probability from memory, check whether actual frequency data exists. The memory is a sample from attention, not from reality.

**Mitigation — reverse the question.** Instead of "how risky is X?" ask "how many times did X happen last year per million attempts?"

## Bias 3 — Anchoring

**Mechanism.** Numerical estimates are biased toward any anchor value available at the moment of estimation, even when the anchor is arbitrary or irrelevant.

**Worked example.** A classic study asked participants to write down the last two digits of their social security number, then estimate the price of a bottle of wine. People with higher digits consistently gave higher estimates. The digits had zero informational value, yet they shifted estimates by 50-100%.

**Mitigation — multiple independent estimates.** Generate the estimate twice, using different starting points, then average.

**Mitigation — consider the opposite.** Explicitly ask "why might my estimate be too high?" and "why might it be too low?" before committing.

## Bias 4 — Representativeness Heuristic

**Mechanism.** Probability is judged by how much an instance resembles a stereotype of the category, rather than by the base rate of the category.

**Worked example (Tversky & Kahneman, 1983).** Linda is 31, single, outspoken, and deeply concerned with issues of discrimination and social justice. Which is more probable?
1. Linda is a bank teller.
2. Linda is a bank teller and active in the feminist movement.

Most people pick (2), but (2) is a conjunction of (1) with another claim, so P(2) <= P(1) by the conjunction rule. Representativeness overrode probability.

**Mitigation — apply the conjunction rule.** A more specific claim is always less probable than its components.

**Mitigation — consult base rates.** How many bank tellers are there? How many active feminists? The base rates are what actually determine the answer.

## Bias 5 — Framing Effects

**Mechanism.** Preferences change when the same choice is described differently — typically, emphasizing gains vs. losses leads to different risk preferences (loss aversion).

**Worked example.** A disease will kill 600 people without intervention. Option A saves 200 for sure. Option B has 1/3 chance of saving all 600 and 2/3 chance of saving none. Most people pick A. Now reframe: Option C kills 400 for sure, Option D has 2/3 chance of killing all 600 and 1/3 chance of killing none. Most people pick D. But C = A and D = B.

**Mitigation — translate between frames.** Whenever you encounter a choice, restate it in both gain and loss frames. If your preference changes, the framing is driving you, not the content.

**Mitigation — state outcomes in absolute terms.** "200 saved out of 600, 400 die" is frame-neutral.

## Bias 6 — Hindsight Bias

**Mechanism.** After an event occurs, the mind reconstructs prior probabilities to make the actual outcome seem more likely than it was. "I knew it all along."

**Worked example.** Before an election, experts give a candidate a 40% chance of winning. After the candidate wins, the same experts remember themselves as having predicted 65%. The revision is unconscious.

**Mitigation — write down predictions in advance.** Any calibration system (prediction markets, forecast journals, probability logs) defeats hindsight bias by making the original prediction concrete and audit-able.

**Mitigation — study outcomes with the ex ante information only.** When analyzing a past decision, ask what was known at the time, not what we know now.

## Bias 7 — Overconfidence

**Mechanism.** People assign higher confidence to their beliefs than accuracy warrants. 90% confidence intervals contain the truth in roughly 50% of cases in typical studies.

**Worked example.** An expert is asked to provide a range for the population of a foreign country such that they are 90% sure the true value is in the range. Over many such questions, the expert is right about 50% of the time. The confidence claim and the accuracy diverge dramatically.

**Mitigation — track calibration.** Record your confidence intervals and check whether 90% of them actually contain the truth. Over time, widen the intervals until calibration matches.

**Mitigation — consider disconfirming evidence.** Before finalizing a confidence estimate, list reasons you might be wrong. Each reason should expand the interval.

## Bias 8 — Motivated Reasoning

**Mechanism.** The conclusion the reasoner wants to reach biases the evaluation of evidence. Evidence supporting the desired conclusion is evaluated leniently; evidence against is scrutinized harshly.

**Worked example.** A scientist reviews a study favorable to her preferred theory and notes minor strengths. She reviews an equally strong study that contradicts her theory and notes minor weaknesses. Both reviews are "fair" by her own self-assessment — but the asymmetry in standards reveals the motivation.

**Mitigation — blind the conclusion.** Evaluate the method before knowing the result. If you cannot, imagine you got the opposite result and ask whether you would accept it.

**Mitigation — adversarial collaboration.** Work with someone whose conclusion is opposite to yours. Agree in advance on what evidence would change each of your minds.

## Bias 9 — Sunk Cost Fallacy

**Mechanism.** Past investment (money, time, effort) is treated as a reason to continue investing, even when the rational decision is to stop. Sunk costs are irrecoverable; only future costs and benefits are relevant to future decisions.

**Worked example.** A company has spent five years and $50M on a product that is clearly not viable. Leadership continues funding it because "we've invested too much to walk away now." The $50M is gone regardless of the next decision.

**Mitigation — ask the fresh-eyes question.** If you were joining this decision today with no history, would you start this project? If no, stop it.

**Mitigation — state the counterfactual.** "Every dollar we spend from here forward could be spent elsewhere. What is its best alternative use?"

## Bias 10 — Fundamental Attribution Error

**Mechanism.** Others' behavior is explained by their character; one's own behavior is explained by circumstance. Both are almost always a mix.

**Worked example.** A colleague snaps at you in a meeting. You conclude they are rude. Later you snap at another colleague and conclude you are under pressure. Both of you were probably under pressure. The asymmetry in explanation is the bias.

**Mitigation — assume circumstance.** When judging others, start from "what circumstances might explain this?" before reaching for character.

## Bias 11 — In-Group Favoritism

**Mechanism.** Judgments and evaluations tilt in favor of the evaluator's own group, even when the groups are arbitrary and the evidence is identical.

**Worked example.** The same aggressive debate tactic is called "passionate engagement" when performed by an ally and "bullying" when performed by an opponent. The behavior is unchanged.

**Mitigation — symmetry test.** Before evaluating an action, imagine it performed by a member of the other side. Would you judge it the same way?

## Bias 12 — Base Rate Neglect

**Mechanism.** New evidence is weighed as if prior probabilities did not exist. A test result is interpreted as direct evidence of a condition, ignoring how rare the condition is to begin with.

**Worked example.** A test for a disease has 99% sensitivity and 99% specificity. A patient tests positive. The disease affects 1 in 10,000 people. What is the probability the patient has the disease? Intuition says 99%. Bayes' theorem says about 1%. The low base rate dominates.

**Mitigation — write out Bayes' theorem.** P(H|E) = P(E|H) * P(H) / P(E). The prior P(H) is the base rate and must not be omitted.

**Mitigation — think in natural frequencies.** "Out of 10,000 people, 1 has the disease and will test positive. Of the 9,999 without it, about 100 will test positive. So 1 of 101 positives actually has the disease — about 1%."

## Integrating the Biases into Practice

A practical bias-mitigation discipline combines several techniques:

1. **Pre-commitment.** State your prediction and confidence before seeing the outcome.
2. **Disconfirmation pass.** Actively search for evidence against your belief.
3. **Consider the opposite.** Generate reasons your estimate might be wrong in each direction.
4. **Base rate anchoring.** Start from the base rate, then update.
5. **Frame translation.** Restate the choice in both gain and loss frames.
6. **Adversarial collaboration.** Work with someone who disagrees; agree on decisive evidence.
7. **Calibration tracking.** Record confidence estimates over time and compare to outcomes.

None of these techniques eliminate bias. They reduce its magnitude when applied consistently.

## When to Use

- Evaluating high-stakes judgments (policy, investment, hiring, medical)
- Reviewing your own reasoning on topics where you feel strongly
- Helping others reason more clearly about emotionally charged questions
- Designing decision processes that minimize bias impact
- Teaching calibration and epistemic humility

## When NOT to Use

- Simple factual lookups where reasoning is not involved
- Situations where speed matters more than accuracy — some biases are features of fast thinking
- Domains where the normative standard itself is contested

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Treating bias labels as insults | Bias is universal; labeling is not blame | Describe the mechanism, not the person |
| Assuming awareness cures bias | Knowing about confirmation bias does not remove it | Use structured mitigation, not willpower |
| Calling every disagreement "bias" | Legitimate disagreement is not bias | Distinguish reasonable disagreement from patterned error |
| Selective application | Finding bias only in opponents | Apply the tools to yourself first |
| Overconfidence about debiasing | Mitigation reduces bias; it does not eliminate it | Track calibration empirically |

## Cross-References

- **tversky agent:** Heuristics and biases tradition, conjunction fallacy, representativeness.
- **kahneman-ct agent:** System 1 / System 2 framing for when biases are most active.
- **paul agent:** Integration into the elements of reasoning framework.
- **dewey-ct agent:** Reflective thinking as the meta-skill that enables bias recognition.
- **evidence-assessment skill:** Evaluating evidence quality without bias-driven shortcuts.
- **decision-making skill:** Applying bias mitigation to structured decisions.

## References

- Tversky, A., & Kahneman, D. (1974). "Judgment under Uncertainty: Heuristics and Biases." *Science*, 185, 1124-1131.
- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- Gilovich, T., Griffin, D., & Kahneman, D. (eds.) (2002). *Heuristics and Biases: The Psychology of Intuitive Judgment*. Cambridge University Press.
- Nickerson, R. S. (1998). "Confirmation Bias: A Ubiquitous Phenomenon in Many Guises." *Review of General Psychology*, 2, 175-220.
- Stanovich, K. E. (2011). *Rationality and the Reflective Mind*. Oxford University Press.
- Kahneman, D., Sibony, O., & Sunstein, C. R. (2021). *Noise: A Flaw in Human Judgment*. Little, Brown Spark.
