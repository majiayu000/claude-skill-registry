---
name: logical-reasoning
description: Deductive and inductive reasoning, formal and informal logical structure, validity, soundness, and rules of inference. Covers propositional logic, quantified reasoning, syllogisms, common inference patterns (modus ponens, modus tollens, hypothetical syllogism, disjunctive syllogism), and the distinction between deductive certainty and inductive probability. Use when the question is not whether a premise is true but whether the reasoning from premises to conclusion is logically valid.
type: skill
category: critical-thinking
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/critical-thinking/logical-reasoning/SKILL.md
superseded_by: null
---
# Logical Reasoning

Logic is the study of what follows from what. A valid logical argument has a form that preserves truth — if the premises are true, the conclusion cannot be false. This skill covers the core machinery of deductive and inductive reasoning: the rules of inference, the standard argument forms, the common errors, and the boundary between the two styles of reasoning.

**Agent affinity:** paul (chair-level framing), elder (inference-pattern drills), tversky (inductive strength)

**Concept IDs:** crit-deductive-reasoning, crit-inductive-reasoning, crit-argument-structure

## The Reasoning Toolbox at a Glance

| # | Pattern | Form | Type |
|---|---|---|---|
| 1 | Modus ponens | If P then Q; P; therefore Q | Deductive, valid |
| 2 | Modus tollens | If P then Q; not Q; therefore not P | Deductive, valid |
| 3 | Hypothetical syllogism | If P then Q; if Q then R; therefore if P then R | Deductive, valid |
| 4 | Disjunctive syllogism | P or Q; not P; therefore Q | Deductive, valid |
| 5 | Constructive dilemma | (P or Q); (if P then R); (if Q then S); therefore (R or S) | Deductive, valid |
| 6 | Universal instantiation | All A are B; x is an A; therefore x is a B | Deductive, valid |
| 7 | Existential generalization | a has property P; therefore something has property P | Deductive, valid |
| 8 | Affirming the consequent | If P then Q; Q; therefore P | Deductive, INVALID |
| 9 | Denying the antecedent | If P then Q; not P; therefore not Q | Deductive, INVALID |
| 10 | Enumerative induction | Every observed A has been B; therefore all A are B | Inductive, probable |
| 11 | Statistical generalization | n% of sampled A are B; therefore about n% of all A are B | Inductive, probable |
| 12 | Inference to the best explanation | H explains the observations better than alternatives; therefore H | Inductive, probable |
| 13 | Analogical reasoning | A and B share features F1..Fn; A has Fm; therefore B has Fm | Inductive, probable |

## Deductive Reasoning: Form Preserves Truth

A deductive argument is valid when the premises entail the conclusion. If the form is valid and all premises are true, the conclusion must be true. This is the only style of reasoning that guarantees its conclusions.

### Pattern 1 — Modus Ponens

**Form:** If P then Q. P. Therefore Q.

**Worked example.**
```
P1. If it is raining, then the street is wet.
P2. It is raining.
C.  The street is wet.
```

Modus ponens is the engine of deductive reasoning. Most chained arguments reduce to sequences of modus ponens applications.

### Pattern 2 — Modus Tollens

**Form:** If P then Q. Not Q. Therefore not P.

**Worked example.**
```
P1. If the theory is correct, the experiment will show effect X.
P2. The experiment did not show effect X.
C.  The theory is not correct (or is incomplete).
```

Modus tollens is the engine of scientific falsification. Popper built his philosophy of science on it.

### Pattern 3 — Hypothetical Syllogism (Chain Rule)

**Form:** If P then Q. If Q then R. Therefore if P then R.

**Worked example.**
```
P1. If interest rates rise, then borrowing becomes more expensive.
P2. If borrowing becomes more expensive, then business investment slows.
C.  If interest rates rise, then business investment slows.
```

Long conditional chains can be built by repeated hypothetical syllogism. Breaks in the chain (any false sub-implication) invalidate the whole.

### Pattern 4 — Disjunctive Syllogism

**Form:** P or Q. Not P. Therefore Q.

**Worked example.**
```
P1. The problem is either the cable or the router.
P2. We tested the cable and it works fine.
C.  The problem is the router.
```

**Caution.** Requires that the disjunction be genuinely exhaustive. If the problem could also be the ISP, the modem, or the wall jack, P1 is false and the argument is unsound.

### Pattern 5 — Constructive Dilemma

**Form:** P or Q. If P then R. If Q then S. Therefore R or S.

**Worked example.**
```
P1. Either we cut spending or we raise revenue.
P2. If we cut spending, services will degrade.
P3. If we raise revenue, taxes will increase.
C.  Either services will degrade or taxes will increase.
```

Constructive dilemma shows how binary choices push the consequence forward.

### Pattern 6 — Universal Instantiation

**Form:** All A are B. x is an A. Therefore x is a B.

**Worked example.**
```
P1. All mammals have a four-chambered heart.
P2. A platypus is a mammal.
C.  A platypus has a four-chambered heart.
```

This is the most basic application of quantified reasoning to particular cases.

### Pattern 7 — Existential Generalization

**Form:** a has property P. Therefore there exists something with property P.

**Worked example.**
```
P1. Kepler-452b is an exoplanet.
C.  There exists at least one exoplanet.
```

Existential generalization moves from specific evidence to existence claims. It is logically weaker than universal generalization but is always valid when the premise is.

## Invalid Deductive Forms (Formal Fallacies)

### Fallacy 8 — Affirming the Consequent

**Form:** If P then Q. Q. Therefore P. (INVALID)

**Worked example.**
```
P1. If it is raining, then the street is wet.
P2. The street is wet.
C.  It is raining.  [DOES NOT FOLLOW]
```

The street could be wet because a truck sprayed it, a pipe broke, or the street cleaners came by. Q can hold for reasons other than P.

### Fallacy 9 — Denying the Antecedent

**Form:** If P then Q. Not P. Therefore not Q. (INVALID)

**Worked example.**
```
P1. If you study hard, you will pass the exam.
P2. You did not study hard.
C.  You will not pass the exam.  [DOES NOT FOLLOW]
```

Not studying is not the only route to failing, and studying is not the only route to passing. The conditional tells us what one path to Q looks like; it does not say all paths must go through P.

**The valid/invalid pair.** Modus ponens and modus tollens are valid; affirming the consequent and denying the antecedent are not. Learning these four patterns together — and being able to name each one — is the single highest-leverage step in deductive reasoning fluency.

## Inductive Reasoning: Probability, Not Certainty

Inductive arguments do not guarantee their conclusions. They make them more or less probable given the evidence. The goal is strength, not validity.

### Pattern 10 — Enumerative Induction

**Form:** Every observed A has been B. Therefore all A are B (or: the next A will be B).

**Worked example.**
```
P1. Every observed swan in Europe was white.
C.  All swans are white.
```

This was widely believed until black swans were discovered in Australia. Enumerative induction is only as strong as the range of observations. A sample confined to one region, time, or context generalizes only to that context.

### Pattern 11 — Statistical Generalization

**Form:** n% of sampled A are B. Therefore about n% of all A are B, within a margin determined by sample size and sampling method.

**Worked example.**
```
P1. In a random sample of 1,500 US adults, 54% approve of policy X
    (margin of error +/- 3%).
C.  Approximately 51-57% of all US adults approve of policy X.
```

Strength depends on sample size, randomness, representativeness, and absence of systematic bias. A sample of 1,500 drawn randomly is very different from a sample of 1.5 million that self-selected.

### Pattern 12 — Inference to the Best Explanation (Abduction)

**Form:** Hypothesis H explains the observations. H is better than the alternative hypotheses considered. Therefore H is (probably) true.

**Worked example.**
```
P1. The patient has fever, productive cough, and infiltrates on chest X-ray.
P2. Bacterial pneumonia explains all three findings.
P3. Viral pneumonia and pulmonary embolism explain the findings less well.
C.  The patient likely has bacterial pneumonia.
```

Strength depends on whether the alternatives considered are actually exhaustive. A hypothesis that is the best among three is not necessarily the best among all possible explanations.

### Pattern 13 — Analogical Reasoning

**Form:** A and B share features F1..Fn. A has feature Fm. Therefore B (probably) has feature Fm.

**Worked example.**
```
P1. Rats and humans share much of their digestive biology, liver enzymes,
    and toxicity pathways.
P2. Substance X was toxic to rats at dose D.
C.  Substance X is likely toxic to humans at comparable dose.
```

Strength depends on how many relevant features the two objects share, and whether any key disanalogy exists. Analogies are strongest when the shared features are the same features that would determine the outcome.

## Deductive vs. Inductive: The Boundary

| Property | Deductive | Inductive |
|---|---|---|
| Guarantee | Valid deduction: premises true implies conclusion true | Probable at best |
| Truth preservation | Yes (when valid) | No |
| Adding premises | Cannot invalidate a valid argument | Can strengthen or weaken |
| Role of form | Validity determined by form alone | Strength depends on content and context |
| When to use | Math, logic, formal systems, definitional claims | Empirical science, everyday reasoning, prediction |

**Common mistake.** Treating a probable inductive conclusion as if it had deductive force. Scientific generalizations are inductive. They can be well-supported and still be wrong.

## Quantifiers and Scope

Logical reasoning hinges on distinguishing "all," "some," "no," and "most."

- **All A are B.** Universal affirmative. Every member of A is in B.
- **No A are B.** Universal negative. No member of A is in B.
- **Some A are B.** Particular affirmative. At least one member of A is in B.
- **Some A are not B.** Particular negative. At least one member of A is outside B.

Valid moves: from "All A are B" you can infer "Some A are B" (assuming A is non-empty). Invalid moves: from "Some A are B" you cannot infer "All A are B," and from "All A are B" you cannot infer "All B are A" (conversion error).

**Worked example (conversion error).**
```
P1. All Seattle residents are Americans.
C.  All Americans are Seattle residents.  [INVALID]
```

## Proof Structure Quick Guide

When constructing a deductive argument:

1. **State the conclusion** you intend to prove.
2. **List premises** that are individually defensible.
3. **Apply inference rules** step by step, labeling each step with the rule used.
4. **Arrive at the conclusion** from the last inference step.
5. **Verify no invalid moves** appear in the chain.

## When to Use

- Evaluating a formal argument in philosophy, mathematics, or computer science
- Analyzing legal reasoning where rules of inference matter
- Testing whether a claimed conclusion follows from stated assumptions
- Building a chain of reasoning that must hold under adversarial scrutiny
- Teaching the difference between valid reasoning and true conclusions

## When NOT to Use

- Pure empirical questions where the issue is data quality, not inference — use `evidence-assessment`
- Decisions under uncertainty where probability distributions matter more than logical form — use `decision-making`
- Questions about bias-driven belief formation — use `cognitive-biases`

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Affirming the consequent | Many causes can produce Q besides P | Recognize the pattern; demand additional evidence |
| Denying the antecedent | P is not the only way to Q | Recognize the pattern; check other paths |
| Conversion error | "All A are B" is not the same as "All B are A" | Distinguish subject and predicate |
| Treating induction as deduction | Probable conclusions can still be wrong | State the conclusion with its uncertainty |
| Undistributed middle | Syllogism fails when the middle term does not cover all cases | Check that the middle term connects the premises genuinely |
| Equivocation | Using a word with two meanings in the same argument | Fix the meaning at the outset |

## Cross-References

- **paul agent:** Applies the elements of reasoning framework — inference is one element among eight.
- **elder agent:** Uses standard inference patterns as drills for developing reasoning fluency.
- **tversky agent:** Focuses on inductive reasoning and its systematic biases.
- **argument-evaluation skill:** How inference rules are applied to evaluate real arguments.
- **cognitive-biases skill:** Cognitive biases that distort even valid logical reasoning.
- **evidence-assessment skill:** Inductive reasoning from evidence to conclusions.

## References

- Copi, I. M., Cohen, C., & McMahon, K. (2014). *Introduction to Logic*. 14th edition. Pearson.
- Tomassi, P. (1999). *Logic*. Routledge.
- Hurley, P. J. (2014). *A Concise Introduction to Logic*. 12th edition. Cengage.
- Salmon, W. C. (1984). *Logic*. 3rd edition. Prentice-Hall.
- Jeffrey, R. C. (2006). *Formal Logic: Its Scope and Limits*. 4th edition. Hackett.
