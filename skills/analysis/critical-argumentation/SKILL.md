---
name: critical-argumentation
description: Practical argument analysis and construction -- how to identify, evaluate, reconstruct, and build real arguments in natural language. Covers argument identification (premises, conclusions, intermediate steps), charity and steel-manning, argument mapping, the distinction between deductive validity and inductive strength, burden of proof, and the rhetorical context in which arguments operate. Use when the goal is to engage with real-world argument rather than to formalize it.
type: skill
category: logic
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/logic/critical-argumentation/SKILL.md
superseded_by: null
---
# Critical Argumentation

Formal logic tells you when an argument is valid given its premises. It does not tell you whether the premises are true, whether the argument is relevant, whether it is charitable, or whether it deserves a response. Those are questions of **critical argumentation** -- the practical discipline of engaging with arguments in the form they actually appear: in prose, in speech, in debate, in ordinary disagreement. This skill covers how to identify real arguments, evaluate them fairly, reconstruct them at their best, and build arguments of your own that others can engage with productively.

**Agent affinity:** russell (critical tradition), langer (pedagogy), quine (linguistic precision)

**Concept IDs:** log-argument-evaluation, log-informal-fallacies, log-burden-of-proof, log-charity-principle

## What Counts as an Argument

An **argument** in the logical sense is a set of claims where some (the **premises**) are offered as reasons for accepting another (the **conclusion**). Not every piece of discourse is an argument:

- **Description**: "The report found that the program reduced costs." Not an argument unless a conclusion is drawn.
- **Explanation**: "The program reduced costs because of economies of scale." Explanatory, not persuasive -- the "because" gives a reason for the fact, not for believing the fact.
- **Assertion**: "This policy is good." A claim, not an argument.
- **Argument**: "This policy is good because it reduces costs without harming quality, and no alternative achieves both." Premises offered, conclusion drawn.

The boundary is not always sharp. Many arguments in the wild are compressed or implicit; part of the skill is recognizing an argument when its structure is not marked out.

## Premise and Conclusion Markers

Natural language signals that mark the parts of an argument:

**Premise markers** (the reason-giving side):
- because, since, for, given that, as, in view of the fact that, assuming that

**Conclusion markers** (the conclusion-drawing side):
- therefore, so, thus, hence, consequently, it follows that, accordingly, we can conclude that

Not every sentence with "because" is an argument, and many real arguments have no markers at all. The markers are helpful but not definitive.

## The Standard Form of an Argument

When analyzing or reconstructing an argument, write it in **standard form**:

```
Premise 1: ...
Premise 2: ...
Premise 3: ...
Conclusion: ...
```

With the conclusion clearly labeled, the logical structure becomes visible. Any missing or implicit premise should be made explicit -- bringing out the hidden assumptions is often the most important step in evaluation.

**Example.** "Smith would make a bad senator. He lies on his tax returns."

Standard form:
- Premise 1: Smith lies on his tax returns.
- (Implicit premise 2: Someone who lies on tax returns would make a bad senator.)
- Conclusion: Smith would make a bad senator.

Making the implicit premise explicit is often where the argument's real weight lies. In this case, the implicit premise is debatable -- does tax dishonesty predict senatorial performance? -- and that is where the argument actually stands or falls.

## Charity and Steel-Manning

The **principle of charity** says: interpret an argument in its strongest reasonable form before evaluating it. Do not attack a misreading. Do not attack a misstatement. Find the best version of the argument the author could have intended, and engage with that.

**Steel-manning** is the active form of charity: reconstruct the argument as powerfully as possible, possibly better than the author actually made it. Then see if even the steel-manned version fails. If it does, your criticism is strong. If the steel-manned version survives, you owe it a response.

The opposite is **straw-manning** -- attacking a weak or distorted version of the argument. Straw-manning is easy and produces a feeling of victory; it produces no actual progress.

**When charity bottoms out.** Charity has limits. If an argument is bad in multiple ways and no reasonable reconstruction saves it, the right move is to say so -- not to invent a different, better argument the author did not make and respond to that one. Charity is interpretation, not substitution.

## Deductive Validity vs Inductive Strength

Two very different standards for good argument:

### Deductive validity

An argument is **deductively valid** if its conclusion follows necessarily from its premises -- no possible situation makes the premises true and the conclusion false. Validity is absolute: either the argument is valid or it is not.

An argument is **sound** if it is valid AND its premises are actually true.

Deductive validity is the standard for mathematical proof, formal derivation, and some legal arguments.

### Inductive strength

An argument is **inductively strong** if its premises make the conclusion likely, even if not certain. Inductive strength is a matter of degree -- arguments can be very strong, moderately strong, weak, or negligible.

**Cogency** is the inductive counterpart of soundness: a strong argument with true premises.

Scientific inference, everyday reasoning, and most policy argument are inductive. Demanding deductive validity where only inductive strength is available is a common philosophical mistake.

### The mismatch error

A common error is judging an inductive argument by deductive standards. "You said X is likely, but I can imagine it being false, so your argument fails." This misunderstands what an inductive argument claims -- it does not claim impossibility, only likelihood.

## Burden of Proof

The **burden of proof** is the obligation to supply evidence for a claim. In any argument, some party is making the claim that requires justification; the other party is, by default, free to withhold agreement until the evidence is supplied.

Default burden-of-proof rules:

- **Positive claims** have a heavier burden than negative claims. "There is a god" carries more burden than "I do not believe there is a god."
- **Extraordinary claims** (those that contradict well-established knowledge) have a heavier burden than ordinary claims. Carl Sagan: "Extraordinary claims require extraordinary evidence."
- **Claims that invite action** (policy proposals, predictions, recommendations) carry the burden of showing their basis.

**Shifting the burden** is a rhetorical tactic where one side tries to put the burden on the other by framing the question in a way that reverses the default. "Prove God does not exist" shifts the burden from the claimant to the skeptic.

Burden-of-proof disputes are often more productive to address than the underlying substantive disagreement.

## Argument Mapping

For complex arguments, a diagram helps. The two main conventions:

### Linear form

```
P1 + P2 → Intermediate conclusion → Final conclusion
```

Premises combine (via +) to support intermediate conclusions, which combine to support final conclusions.

### Tree form

```
        Final conclusion
          /        \
   Sub-argument   Sub-argument
     /    \         /    \
    P1    P2       P3    P4
```

Tree diagrams make the hierarchical structure of multi-step arguments visible.

Tools like Rationale, Argdown, and Kialo support computer-aided argument mapping.

## Convergent, Linked, and Serial Arguments

Three ways premises can relate in an argument:

### Convergent

Each premise independently supports the conclusion. Removing one premise weakens the argument but does not destroy it.

**Example.** "We should hire Alice because she has excellent credentials, she writes well, and she interviewed brilliantly." Three independent reasons.

### Linked

Premises work together; removing one makes the argument collapse.

**Example.** "All dogs are mammals. All mammals are vertebrates. Therefore all dogs are vertebrates." The premises are linked -- neither alone supports the conclusion.

### Serial

One premise supports an intermediate conclusion that supports the final conclusion.

**Example.** "The witness was lying [because he had a motive to lie, and people with motives often lie]. Therefore the testimony is unreliable."

Distinguishing these structures matters for evaluation: the linked-premise failure mode is "one weak link breaks the chain," while the convergent-premise failure mode is "all the reasons are bad."

## Rhetorical Context

Arguments do not happen in a vacuum. Their evaluation depends on:

- **The audience**: who is being asked to accept the conclusion?
- **The stakes**: what hinges on acceptance?
- **The speaker's goals**: are they trying to persuade, inform, or win a point?
- **The background assumptions**: what does everyone in the conversation already grant?

Ignoring rhetorical context leads to sterile logic-chopping that misses why arguments matter. Overweighting rhetorical context leads to relativism that dissolves the distinction between good and bad argument. The skill is calibrating between.

## The Argument Evaluation Checklist

When evaluating an argument, run through these questions:

1. **What is the conclusion?** State it in one sentence.
2. **What are the premises?** List them, making implicit ones explicit.
3. **Is the argument deductive or inductive?** Apply the right standard.
4. **Is it valid / strong?** If deductive, is the inference valid? If inductive, how strong is the support?
5. **Are the premises true?** Each one. Ask for evidence on contested ones.
6. **Is the argument charitable?** Did you steel-man it first?
7. **What would change your mind?** If nothing would, you are not engaging honestly.
8. **What is the strongest counter-argument?** State it, and see if the original survives.

## Building Your Own Arguments

When constructing an argument, mirror the evaluation checklist:

1. **Start with your conclusion.** What are you asking the audience to accept?
2. **Identify your strongest premises.** What are the best reasons?
3. **Check your inference.** Does the conclusion actually follow?
4. **Anticipate objections.** What would a thoughtful critic say? Answer them in the argument, not after.
5. **Acknowledge what you are not claiming.** Narrow the thesis to what you can actually defend.
6. **Attribute contested premises.** "As the CBO reported ..." is more defensible than an unsourced claim.
7. **Distinguish evidence from interpretation.** Your facts should be separable from your spin on them.

## Worked Example: A Real Argument

**Original.** "We shouldn't raise the minimum wage. Every time it has been raised in the past, unemployment has gone up. Economists agree it reduces employment for low-skill workers, and anyway small businesses can't afford it."

**Standard form with implicit premises made explicit:**

- P1: In past cases, minimum wage increases have been followed by unemployment increases.
- P2: (Implicit) Past cases are representative of future cases.
- P3: Economists agree that minimum wage increases reduce employment for low-skill workers.
- P4: Small businesses cannot afford higher wages.
- P5: (Implicit) Policies that harm low-skill employment and small businesses should not be enacted.
- Conclusion: The minimum wage should not be raised.

**Evaluation:**
- P1 is factually contested. Many studies find no employment effect, others find small effects. "Every time" is a hasty generalization.
- P2 is a standard inductive assumption but depends on whether the economic environment is comparable.
- P3 is a disputed claim about professional consensus. Economists do not agree uniformly on this.
- P4 is plausible for some small businesses but false for others; it depends on the industry and size.
- P5 is a value claim that may be accepted or rejected depending on how much weight is given to affected workers.

**Steel-manned version:** "There is evidence that minimum wage increases may reduce employment for the lowest-skill workers, and there are real small businesses that operate on thin margins. Therefore, any minimum wage increase should be studied carefully for its distributional effects and phased in gradually."

The steel-manned version is much weaker than the original but also much more defensible. It opens conversation rather than closing it.

## When NOT to Use This Skill

- **Formal-logic exercises.** Use `propositional-logic` or `predicate-logic`.
- **Fallacy-spotting.** Use `informal-fallacies`.
- **Mathematical proof evaluation.** Use `mathematical-proof-logic`.
- **Pure rhetoric or persuasion craft.** Use a writing or rhetoric skill; critical argumentation is evaluative, not persuasive.

## Decision Guidance

When encountering a real-world argument:

1. **Find the conclusion first.** What is being claimed?
2. **Identify the premises**, including unstated ones.
3. **Steel-man the argument** before criticizing.
4. **Distinguish validity / strength from truth of premises.** An argument can be valid and still wrong.
5. **Apply the right standard** (deductive vs inductive).
6. **Evaluate charitably but honestly.** Name weaknesses without exaggeration.
7. **State what would change your mind.** If nothing would, the exercise is not evaluation but confirmation.

## Cross-References

- **russell agent:** Critical tradition, pacifist-era public argument
- **langer agent:** Pedagogical framing for students
- **quine agent:** Linguistic precision, finding ambiguity
- **informal-fallacies skill:** Specific failure modes
- **propositional-logic skill:** Formal counterpart

## References

- Walton, D. (2006). *Fundamentals of Critical Argumentation*. Cambridge University Press.
- Govier, T. (2010). *A Practical Study of Argument*. 7th edition. Wadsworth.
- Weston, A. (2018). *A Rulebook for Arguments*. 5th edition. Hackett.
- Tindale, C. W. (2004). *Rhetorical Argumentation: Principles of Theory and Practice*. Sage.
- van Eemeren, F. H., & Grootendorst, R. (2004). *A Systematic Theory of Argumentation: The Pragma-Dialectical Approach*. Cambridge University Press.
- Fisher, A. (2004). *The Logic of Real Arguments*. 2nd edition. Cambridge University Press.
