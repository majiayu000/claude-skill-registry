---
name: argument-evaluation
description: Systematic evaluation of arguments for structure, validity, soundness, and charitable interpretation. Covers premise identification, conclusion extraction, argument mapping, steel-manning, and the distinction between validity (form) and soundness (form plus true premises). Use when assessing an argument, reconstructing an opponent's position fairly, or preparing a rebuttal.
type: skill
category: critical-thinking
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/critical-thinking/argument-evaluation/SKILL.md
superseded_by: null
---
# Argument Evaluation

An argument is a set of statements in which some (the premises) are offered as reasons for believing another (the conclusion). Critical thinkers evaluate arguments by reconstructing them, testing their logical form, checking the truth of the premises, and engaging with the strongest version of the opposing case. This skill provides a systematic procedure for doing all four.

**Agent affinity:** paul (overall framing, elements of reasoning), elder (structural reconstruction)

**Concept IDs:** crit-argument-structure, crit-deductive-reasoning, crit-inductive-reasoning, crit-charitable-interpretation

## The Evaluation Toolbox at a Glance

| # | Operation | Purpose | Key signal |
|---|---|---|---|
| 1 | Premise extraction | Pull claims that support the conclusion | "Because," "since," "given that" |
| 2 | Conclusion extraction | Identify what is being argued for | "Therefore," "so," "thus," "hence" |
| 3 | Argument mapping | Show dependency structure | Some premises support sub-conclusions |
| 4 | Reconstruction | Restate in standard form | Numbered premises, explicit conclusion |
| 5 | Validity check | Does conclusion follow if premises are true? | Counterexample to form |
| 6 | Soundness check | Are the premises actually true? | Independent fact check |
| 7 | Strength check | For inductive arguments, how probable is the conclusion? | Sample quality, base rates |
| 8 | Steel-manning | Reconstruct the strongest version | Add missing support the author could have given |
| 9 | Hidden premise detection | Find the unstated assumption | The argument leaks if the premise is removed |
| 10 | Scope check | Does the conclusion overreach the evidence? | "All" from "some," universal from single case |

## Operation 1 — Premise Extraction

**Pattern:** Isolate statements the author offers as reasons. These are the building blocks of the argument.

**Indicator words:** "because," "since," "given that," "in light of," "as shown by," "for the reason that."

**Worked example.** *"Because the economy is slowing and interest rates are still high, a recession is likely within six months."*

Premises:
- P1: The economy is slowing.
- P2: Interest rates are still high.

Notice that indicator words are cues, not guarantees. Some premises appear without indicators; some indicator words are used rhetorically without introducing real premises.

## Operation 2 — Conclusion Extraction

**Pattern:** Identify the statement the premises are meant to support.

**Indicator words:** "therefore," "thus," "so," "hence," "it follows that," "we can conclude," "which shows."

**Worked example (continued).** The conclusion of the example above is:
- C: A recession is likely within six months.

**Common mistake.** Treating a rhetorical question as a conclusion. "Why should we trust them?" is not a conclusion; it is a question that implies one.

## Operation 3 — Argument Mapping

**Pattern:** Show which premises support which conclusions, including intermediate sub-conclusions.

**Worked example.** *"Social media harms adolescent mental health because it promotes comparison with curated images. Therefore, schools should restrict phone use during the day."*

```
P1: Social media promotes comparison with curated images.
                |
                v
SC1: Social media harms adolescent mental health.  (sub-conclusion)
                |
                v
C:  Schools should restrict phone use during the day.
```

The map reveals that the argument has two logical steps, only one of which was explicitly signaled. Mapping often exposes gaps.

## Operation 4 — Reconstruction in Standard Form

**Pattern:** Restate the argument as numbered premises followed by a single conclusion.

**Worked example.** *"You shouldn't drink the water here. The EPA says it has lead contamination."*

Standard form:
```
P1. The EPA says this water has lead contamination.
P2. [Hidden] Water with lead contamination is unsafe to drink.
P3. [Hidden] You should not drink unsafe water.
C.  You should not drink the water here.
```

Reconstruction often surfaces hidden premises. An argument is not a shapeless cloud of sentences — it is a chain, and every link needs to be visible before you can test it.

## Operation 5 — Validity Check

**Pattern:** Ask whether, if the premises were all true, the conclusion would have to be true.

**Logical basis:** Validity is a property of the argument's form, not of its content. An argument can be valid with false premises, and invalid with true premises.

**Worked example (valid).**
```
P1. All ravens are birds.
P2. All birds have feathers.
C.  All ravens have feathers.
```
This is valid because the form (All A are B; All B are C; therefore All A are C) guarantees the conclusion whenever the premises are true.

**Worked example (invalid).**
```
P1. All ravens are birds.
P2. Some birds are flightless.
C.  Some ravens are flightless.
```
The premises are both true, but the conclusion does not follow. There is no logical guarantee connecting the particular birds that are flightless to ravens specifically.

**The counterexample test.** To show an argument form is invalid, produce an instance with the same form where the premises are true and the conclusion is false.

## Operation 6 — Soundness Check

**Pattern:** An argument is sound if and only if it is valid and all premises are actually true.

Validity is a relationship among statements. Soundness is validity plus real-world accuracy. A valid argument with a false premise proves nothing about the world.

**Worked example.**
```
P1. All mammals lay eggs.          [FALSE]
P2. Whales are mammals.            [TRUE]
C.  Whales lay eggs.               [Valid form, unsound argument]
```
The form is valid. The first premise is false. The conclusion is false. Soundness failed at P1.

**Discipline.** When evaluating a valid argument, interrogate each premise independently. Which evidence supports it? Which evidence could refute it? What would change your mind about this specific premise?

## Operation 7 — Strength Check (Inductive Arguments)

**Pattern:** Inductive arguments do not guarantee their conclusions; they make them more or less probable. Strength measures the probability given the premises.

**Worked example (strong induction).**
```
P1. A random sample of 10,000 adults from the population shows
    a 62% approval rating for policy X.
P2. The sample was drawn using standard random-digit dialing with
    stratification by age, region, and household income.
C.  Approximately 62% of adults in the population approve of policy X.
```
Strong because the sample is large, randomized, and stratified. Conclusion is probabilistic, not certain.

**Worked example (weak induction).**
```
P1. I know three people who got sick after eating at that restaurant.
C.  That restaurant causes people to get sick.
```
Weak because the sample is tiny, self-selected, and confounded with many other causes.

**Strength indicators:** sample size, representativeness, sampling method, absence of confounds, replicability. Weakness indicators: small n, selection bias, anecdote, single source.

## Operation 8 — Steel-Manning (Charitable Interpretation)

**Pattern:** When reconstructing an argument you disagree with, build the strongest version possible before criticizing it. Add missing support the author could reasonably have given, interpret ambiguous phrases in the most defensible way, and acknowledge which parts of the opposing view are correct.

**Worked example.** Suppose the opposing claim is: *"We shouldn't raise the minimum wage because it will cause job losses."*

**Straw-man version (weak).** "They think rich employers matter more than poor workers."

**Steel-man version (strong).**
```
P1. Some studies find that minimum wage increases above the local equilibrium
    cause reductions in low-wage employment, especially in small businesses.
P2. Low-wage workers include many first-job seekers and those with low bargaining power.
P3. Job losses for these workers fall disproportionately on the most vulnerable.
P4. A policy intended to help low-wage workers should not make them worse off on net.
C.  The minimum wage should not be raised, at least not substantially and not
    above the local equilibrium wage.
```

Now you are arguing against the strongest version. If you can refute the steel-man, your position is solid. If you cannot, you learned something.

**Why it matters.** Straw-manning wins arguments cheaply and teaches nothing. Steel-manning loses arguments expensively and teaches you the domain.

## Operation 9 — Hidden Premise Detection

**Pattern:** Many arguments rely on unstated assumptions. Surface them by asking: "What would have to be true for the conclusion to follow from the stated premises?"

**Worked example.** *"She's a lawyer, so she must be good at arguing."*

Stated premise: She is a lawyer.
Stated conclusion: She is good at arguing.

Hidden premise: All (or most) lawyers are good at arguing.

Once surfaced, the hidden premise can be evaluated directly. Is it true? Partially true? True for some kinds of lawyers but not others? Hidden premises often carry the weight of an argument without ever being defended.

## Operation 10 — Scope Check

**Pattern:** Compare the scope of the conclusion to the scope of the premises. A conclusion that claims more than the premises support has overreach.

**Worked example.**
```
P1. In three randomized trials, drug X reduced symptoms of condition Y
    in adult women aged 30-50.
C.  Drug X is effective for condition Y.
```
The conclusion dropped the scope restrictions: adults, women, ages 30-50. The premises say nothing about children, men, elderly patients, or patients with co-occurring conditions. Fixed:
```
C'. Drug X is effective for condition Y in adult women aged 30-50.
```

Scope errors are a leading cause of bad science communication. The paper reports a narrow finding; the headline reports the universal claim.

## Standard Evaluation Procedure

When you encounter an argument in the wild, run this procedure:

1. **Find the conclusion.** What is this argument trying to get you to believe?
2. **Find the premises.** What reasons are offered?
3. **Map the structure.** Are there sub-conclusions? Are all premises offered in support of the main conclusion, or do some support sub-conclusions?
4. **Reconstruct in standard form.** Surface hidden premises as you go.
5. **Test validity.** If the premises were all true, would the conclusion have to be true?
6. **If invalid,** identify the invalid step and stop. The argument does not support its conclusion.
7. **If valid,** check soundness. Are the premises actually true?
8. **For inductive arguments,** check strength and scope.
9. **Steel-man before rejecting.** Could the author have given a better argument? If so, address the steel-man.
10. **Deliver the assessment.** State what you accept, what you reject, and why.

## When to Use

- Reading a policy argument, editorial, or op-ed
- Evaluating a research paper's discussion section
- Preparing a response to an opposing position
- Checking your own reasoning for gaps before committing to a claim
- Teaching someone how to disagree productively

## When NOT to Use

- Pure factual claims with no argumentative structure — use `evidence-assessment` instead
- Emotional or aesthetic claims where logic is not the appropriate frame
- Situations where time pressure makes full evaluation impossible — fall back on rapid heuristics for the most important weak points

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Attacking the author instead of the argument | Ad hominem; leaves the argument untouched | Separate person from position; evaluate the argument on its own terms |
| Declaring victory after refuting the weakest version | Straw-manning; opposing view may still hold | Steel-man first, then critique |
| Treating validity as soundness | Valid arguments can still have false conclusions | Check each premise against evidence |
| Missing hidden premises | Unstated assumptions do the real work | Ask "what would have to be true for this to follow?" |
| Overreaching the scope | Claiming more than evidence supports | Restrict the conclusion to match the premises |
| Confusing disagreement with invalidity | An argument can be valid but still wrong on premises | Say which premise you reject and why |

## Cross-References

- **paul agent:** Applies the elements of reasoning framework to argument evaluation.
- **elder agent:** Specializes in argument reconstruction and structural analysis.
- **dewey-ct agent:** Reflective thinking — the overall stance that makes careful evaluation possible.
- **logical-reasoning skill:** Validity, soundness, and formal logical structure.
- **evidence-assessment skill:** Evaluating the truth of premises.
- **cognitive-biases skill:** Biases that distort argument evaluation.

## References

- Paul, R., & Elder, L. (2019). *The Miniature Guide to Critical Thinking: Concepts and Tools*. Foundation for Critical Thinking.
- Walton, D. (2006). *Fundamentals of Critical Argumentation*. Cambridge University Press.
- Bowell, T., & Kemp, G. (2014). *Critical Thinking: A Concise Guide*. 4th edition. Routledge.
- Hitchcock, D. (2017). *On Reasoning and Argument: Essays in Informal Logic and on Critical Thinking*. Springer.
- Toulmin, S. (2003). *The Uses of Argument*. Updated edition. Cambridge University Press.
