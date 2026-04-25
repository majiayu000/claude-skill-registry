---
name: decision-making
description: Structured approaches to decisions under uncertainty and complexity. Covers expected value, decision trees, multi-criteria decision analysis, System 1 vs System 2 allocation, pre-mortems, reversible vs irreversible decisions, and the distinction between good decisions and good outcomes. Use when choosing among alternatives with uncertain or multi-dimensional consequences, especially when the stakes justify a deliberate rather than intuitive process.
type: skill
category: critical-thinking
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/critical-thinking/decision-making/SKILL.md
superseded_by: null
---
# Decision Making

A decision is a commitment to one of several possible actions in the face of uncertainty about their consequences. Good decision-making is not the same as getting good outcomes — luck intervenes — but consistently good decisions produce better outcomes over time. This skill covers the structured methods decision scientists use to bring rigor to choices that matter.

**Agent affinity:** kahneman-ct (System 1 / System 2 allocation), tversky (expected value and biases), paul (integration with elements of reasoning)

**Concept IDs:** crit-decision-frameworks, crit-calibrated-confidence, crit-intellectual-humility

## The Decision Toolbox at a Glance

| # | Method | Purpose | When to use |
|---|---|---|---|
| 1 | Expected value calculation | Weigh probabilities and payoffs | Repeatable decisions with quantifiable outcomes |
| 2 | Decision trees | Map sequential choices and chance nodes | Multi-stage decisions with contingencies |
| 3 | Multi-criteria decision analysis (MCDA) | Weigh multiple incommensurable criteria | Choices involving trade-offs across dimensions |
| 4 | Pros and cons with weights | Simple MCDA for everyday decisions | Personal choices, not enough data for formal analysis |
| 5 | Pre-mortem | Imagine failure to surface risks | Before committing to a major plan |
| 6 | Reversibility check | Decide how much deliberation is needed | Every decision |
| 7 | Two-way door vs. one-way door | Distinguish easily-undoable from locked-in | Speed decisions for reversible, delay for irreversible |
| 8 | Minimax regret | Minimize worst-case regret instead of maximizing expected value | Extreme uncertainty; loss aversion is justified |
| 9 | Satisficing | Pick the first option meeting minimum criteria | When the cost of searching exceeds the benefit of finding the best |
| 10 | Stopping rules | Decide in advance when to stop deliberating | When analysis paralysis is a risk |

## The Fundamental Distinction — Good Decision vs. Good Outcome

A decision can be good even if the outcome is bad, and a decision can be bad even if the outcome is good. Confusing these is the root of most decision-making errors.

**Good decision, bad outcome.** You evaluated the options carefully, weighed the probabilities, chose the highest expected value action. The low-probability bad outcome happened anyway. This is not a decision error; it is luck. Recording it as a decision error would corrupt future decisions.

**Bad decision, good outcome.** You took a reckless action that had a high probability of failure. It worked out anyway. Do not learn "reckless action is good" from this. Over time, bad decisions produce bad outcomes on average.

**Discipline.** Evaluate decisions by the process at the time, not by the outcome in retrospect. Annie Duke calls this "resulting" — judging decisions by outcomes — and identifies it as a primary corruption of the decision-making process.

## Method 1 — Expected Value

**Pattern:** For each option, compute the sum over outcomes of (probability of outcome) × (value of outcome). Choose the option with the highest expected value.

**Formula.** EV(option) = Σ P(outcome_i) × V(outcome_i)

**Worked example.** Deciding whether to accept a 50% chance of winning $1000 or a guaranteed $400.

- Option A (gamble): 0.5 × $1000 + 0.5 × $0 = $500
- Option B (guaranteed): 1.0 × $400 = $400

EV favors option A. But EV is only the right criterion when the decision repeats many times. For a one-shot decision, loss aversion and risk tolerance matter.

**Limitations.**
- Requires probability estimates that are often unavailable or unreliable.
- Treats all values as commensurable (all convertible to a single currency).
- Ignores risk aversion, which is a legitimate preference for one-shot high-stakes decisions.
- Ignores variance — two options with the same EV but different variance are not equivalent for most humans.

## Method 2 — Decision Trees

**Pattern:** Draw a tree with choice nodes (where the decision-maker picks) and chance nodes (where the world picks). Compute expected value back from the leaves to the root.

**Worked example.** Should you enter a new market?

```
Enter market (cost $1M)
├── Market succeeds (p=0.4) → +$5M
│   └── Net: +$4M
└── Market fails (p=0.6) → $0
    └── Net: -$1M

Do not enter
└── Net: $0
```

EV(Enter) = 0.4 × $4M + 0.6 × (-$1M) = $1.6M - $0.6M = $1M
EV(Do not enter) = $0

Expected value favors entering, but risk tolerance, capital at stake, and opportunity cost all modify the final decision.

**When trees help.** Multi-stage decisions with contingencies. The tree forces explicit statement of all probabilities and payoffs, which exposes hidden assumptions.

## Method 3 — Multi-Criteria Decision Analysis

**Pattern:** When a decision involves multiple criteria that cannot be converted to a single number (money, time, quality, risk, ethics), use a structured weighting.

**Steps:**

1. List the criteria that matter.
2. Assign each a weight (either by importance ranking or by paired comparison).
3. For each option, score it on each criterion (0-10 scale or similar).
4. Compute weighted sum: score(option) = Σ weight_i × rating_i
5. Compare.

**Worked example.** Choosing a job.

| Criterion | Weight | Job A | Job B | Job C |
|---|---|---|---|---|
| Salary | 0.3 | 8 | 6 | 9 |
| Growth | 0.2 | 7 | 9 | 5 |
| Work-life balance | 0.2 | 5 | 8 | 3 |
| Mission alignment | 0.2 | 6 | 9 | 4 |
| Commute | 0.1 | 8 | 6 | 9 |

- Job A: 0.3(8) + 0.2(7) + 0.2(5) + 0.2(6) + 0.1(8) = 6.8
- Job B: 0.3(6) + 0.2(9) + 0.2(8) + 0.2(9) + 0.1(6) = 7.6
- Job C: 0.3(9) + 0.2(5) + 0.2(3) + 0.2(4) + 0.1(9) = 6.0

The process does not replace judgment — the weights and scores reflect subjective values. But the structure prevents one criterion from dominating the decision by loudness or salience.

## Method 4 — Pre-Mortem

**Pattern:** Before committing to a decision, imagine the decision has been made and failed spectacularly. Ask the team: "What were the reasons for failure?" Then treat the reasons as risks to mitigate.

**Why it works.** Standard risk analysis asks "what could go wrong?" which triggers defensiveness and optimism bias. Pre-mortem asks "why did it go wrong?" which treats the failure as a fact and surfaces reasons that would otherwise be suppressed.

**Worked example.** Planning a product launch. Pre-mortem question: "It is six months from now and the launch failed. What happened?"

Surfaced reasons:
- Delays in manufacturing caused missed launch window
- Marketing messaging did not resonate with target demographic
- Competitor launched similar product two weeks earlier
- Initial reviews were negative due to Day 1 bug
- Key partnership fell through

Each surfaced reason becomes a risk mitigation. Pre-mortem typically generates 30-50% more risk identifications than standard risk reviews.

## Method 5 — Reversibility and the Two-Way Door

**Pattern:** Distinguish decisions by whether they can be easily reversed. Spend deliberation in proportion to reversibility.

- **Two-way door (reversible).** You can change your mind later at low cost. Decide quickly. The cost of delay usually exceeds the cost of a wrong choice.
- **One-way door (irreversible).** Once taken, the decision cannot be undone or can be undone only at great cost. Deliberate thoroughly. The cost of a wrong choice exceeds the cost of delay.

**Worked example.** Deciding which text editor to use (two-way door) should take a few minutes at most. Deciding whether to move to another country for a job (one-way door for at least months, often years) warrants substantial deliberation.

**Common error.** Treating reversible decisions as irreversible. This produces analysis paralysis on low-stakes choices and leaves no time for the decisions that actually matter.

## Method 6 — Minimax Regret

**Pattern:** Instead of maximizing expected value, minimize the maximum regret across scenarios. Useful when uncertainty is extreme and loss aversion is justified.

**Worked example.** Deciding whether to buy earthquake insurance in a low-probability zone.

- Option A (buy insurance): Cost $500/year. Regret if no earthquake: $500. Regret if earthquake: Small residual from deductibles.
- Option B (no insurance): Cost $0. Regret if no earthquake: $0. Regret if earthquake: Total loss, ~$500,000.

Max regret for Option A: $500. Max regret for Option B: $500,000. Minimax regret chooses A despite low probability of earthquake, because the asymmetry of regret justifies the premium.

## Method 7 — Satisficing

**Pattern:** Instead of searching for the best option, set minimum criteria and take the first option that meets them. Simon's concept — bounded rationality accepts "good enough" because searching for "best" has costs.

**When satisficing is appropriate.**
- The cost of search (time, effort, opportunity cost) exceeds the marginal value of a better option.
- The option space is unbounded or poorly defined.
- Multiple options are roughly equivalent.
- The decision is not worth extensive deliberation.

**Worked example.** Choosing a restaurant for dinner. There are 200 restaurants in the city. Visiting all is impossible. Set minimum criteria (under $30, opens now, walking distance, positive reviews). Go to the first one that matches. Do not second-guess.

**Common error.** Maximizing on trivial decisions. Spending an hour on which brand of pasta to buy is a sign that the satisficing threshold is badly calibrated.

## Method 8 — System 1 vs. System 2 Allocation

**Pattern:** Match the cognitive mode to the decision. System 1 is fast, intuitive, automatic. System 2 is slow, deliberate, effortful. Most decisions should use System 1, but high-stakes ones warrant System 2.

**System 1 is appropriate when:**
- The decision is routine.
- Expert pattern recognition applies.
- The stakes are low relative to decision cost.
- Speed is more valuable than precision.

**System 2 is appropriate when:**
- The decision is novel.
- Biases are likely to distort System 1 judgment.
- The stakes justify the effort.
- The decision is irreversible.

**Discipline.** System 1 cannot be fully disabled; the question is whether System 2 is engaged on top of it. For high-stakes decisions, actively slow down — write things out, sleep on it, consult others.

## Method 9 — Pros and Cons with Weights

**Pattern:** For everyday decisions where formal MCDA is overkill, list pros and cons for each option and assign rough weights (high/medium/low). The output is more transparent than unstructured gut feel and faster than a full MCDA matrix.

**Franklin's moral algebra.** Benjamin Franklin's 1772 letter to Joseph Priestley describes the technique: write pros and cons in two columns, then strike out a pro and con of equal weight. The remaining items reveal the dominant side.

## Method 10 — Stopping Rules

**Pattern:** Decide in advance when you will stop deliberating. Write the rule down before analysis begins.

**Examples of stopping rules.**
- "I will decide by Friday at 5pm regardless of whether I have more information."
- "If the top two options are within 10% on the weighted criteria, I will pick by flipping a coin."
- "I will gather three quotes, then decide."

**Why it matters.** Without a stopping rule, deliberation expands to fill available time (Parkinson's law for decisions). Analysis paralysis is not a personality trait; it is the absence of a stopping rule.

## Standard Decision Procedure

When facing a decision that warrants deliberate thought:

1. **State the decision.** What choice are you actually making? What are the real alternatives?
2. **Reversibility check.** Two-way door or one-way door?
3. **Clarify the criteria.** What do you actually care about? Rank or weight.
4. **Gather evidence proportionally.** More evidence for irreversible decisions.
5. **Set a stopping rule.** When will you decide?
6. **Pre-mortem.** Imagine the decision failed. What went wrong?
7. **Apply the appropriate method.** EV for repeatable, MCDA for multi-criteria, satisficing for routine.
8. **Sleep on it** if the decision is non-urgent and reversible overnight.
9. **Commit.** Make the decision and move on.
10. **Record the reasoning** so the decision can be evaluated later on process, not outcome.

## When to Use

- Choices where the stakes justify deliberation
- Decisions made by a group that need a shared structure
- Irreversible or high-consequence decisions
- When you suspect your intuition is being distorted by bias
- When you need to explain the decision to others afterward

## When NOT to Use

- Routine decisions where intuition is reliable
- Trivial choices where the deliberation cost exceeds the value
- Emergency situations where speed matters more than precision
- Decisions about pure preferences where "correct" does not apply

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Resulting (judging by outcome) | Confuses luck with skill | Evaluate the process at decision time, not after |
| Treating reversible as irreversible | Wastes deliberation on low-stakes choices | Apply reversibility check first |
| Treating irreversible as reversible | Commits too quickly to binding choices | Slow down for one-way doors |
| Ignoring base rates | Miscalibrates probability estimates | Use historical frequencies as starting points |
| Letting one criterion dominate | Over-weights salient concerns | Use MCDA or weighted pros/cons |
| No stopping rule | Produces analysis paralysis | Write the rule at the start |

## Cross-References

- **kahneman-ct agent:** System 1 / System 2 framework and dual-process decision-making.
- **tversky agent:** Expected value, base rates, biases in decision-making.
- **paul agent:** Integration of decision-making into the elements of reasoning.
- **dewey-ct agent:** Reflective thinking as the meta-skill behind deliberate decision-making.
- **argument-evaluation skill:** Evaluating the reasons for a decision.
- **cognitive-biases skill:** Biases that corrupt even structured decisions.
- **evidence-assessment skill:** Assessing the evidence that feeds into decisions.

## References

- Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux.
- Duke, A. (2018). *Thinking in Bets: Making Smarter Decisions When You Don't Have All the Facts*. Portfolio.
- Klein, G. (2007). "Performing a Project Premortem." *Harvard Business Review*, September.
- Simon, H. A. (1956). "Rational Choice and the Structure of the Environment." *Psychological Review*, 63, 129-138.
- Hammond, J. S., Keeney, R. L., & Raiffa, H. (1999). *Smart Choices: A Practical Guide to Making Better Decisions*. Harvard Business School Press.
- Franklin, B. (1772). Letter to Joseph Priestley, September 19. (Moral algebra.)
