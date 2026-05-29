---
name: informal-fallacies
description: Catalog of informal fallacies with definitions, canonical examples, and detection heuristics. Covers relevance fallacies (ad hominem, straw man, red herring, appeal to authority, appeal to emotion), presumption fallacies (false dichotomy, complex question, begging the question), ambiguity fallacies (equivocation, amphiboly, accent), causal fallacies (post hoc, slippery slope, correlation-causation), and statistical fallacies (hasty generalization, cherry-picking). Use when evaluating arguments for rhetorical or informal reasoning errors.
type: skill
category: logic
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/logic/informal-fallacies/SKILL.md
superseded_by: null
---
# Informal Fallacies

An informal fallacy is a pattern of reasoning that can look persuasive but fails to actually support its conclusion. Unlike formal fallacies (which are detectable by structure alone), informal fallacies depend on context, content, or rhetorical framing. They are the failure modes of everyday argument, the traps in political discourse, and the stock repertoire of bad faith. This skill catalogs the most common informal fallacies, grouped by family, with canonical examples and detection heuristics. It is not a complete taxonomy -- the literature catalogs over a hundred named fallacies -- but it covers the ones that actually appear in ordinary discourse.

**Agent affinity:** russell (critical analysis), quine (linguistic precision), langer (pedagogical framing)

**Concept IDs:** log-informal-fallacies, log-argument-evaluation, log-cognitive-biases, log-propaganda-techniques

## Using Fallacy Labels Responsibly

Before the catalog, a warning: **fallacy labels are tools, not weapons**. Calling an argument a fallacy is not the same as refuting it. A flawed argument may still have a correct conclusion; a fallacy label is a reason to ask for a better argument, not to dismiss the position. The "fallacy fallacy" -- rejecting a conclusion because an argument for it is fallacious -- is itself a fallacy.

The productive use of fallacy labels is to name a specific weakness so that the argument can be improved or replaced. The unproductive use is rhetorical point-scoring.

## Family 1: Relevance Fallacies

These fallacies substitute something emotionally or socially compelling for something that would actually support the conclusion.

### Ad Hominem (Against the Person)

**Pattern:** Attacking the person making an argument rather than the argument itself.

**Example:** "You can't trust her analysis of tax policy because she's a lawyer and they all lie." The analysis stands or falls on its merits, independent of the analyst's profession.

**Subtypes:**
- *Abusive*: direct insult ("you're an idiot")
- *Circumstantial*: impugning motives ("you only say that because you benefit")
- *Tu quoque* ("you too"): "you do it too, so your criticism is invalid"

**When attacks are legitimate.** Questioning a source's credibility is not ad hominem when credibility is actually relevant. "This study was funded by the tobacco industry" is a legitimate concern about bias, not an ad hominem -- it is information about the reliability of the evidence, not about the argument's logical structure.

### Straw Man

**Pattern:** Misrepresenting an opponent's position to make it easier to attack.

**Example:** "Senator Smith wants to cut defense spending. So Senator Smith wants to leave us defenseless." The caricature replaces the actual position.

**Detection heuristic:** Can the person being argued against recognize their view in the description? If not, it is probably a straw man.

### Red Herring

**Pattern:** Changing the subject to a related but different issue to avoid addressing the original point.

**Example:** "Yes, the budget has a deficit, but look at how much we spend on education -- isn't that more important?" The deficit question remains unanswered.

### Appeal to Authority (Argumentum ad Verecundiam)

**Pattern:** Citing an authority whose expertise is irrelevant or questionable as support for a claim.

**Example:** "Einstein believed in God, so God exists." Einstein was a physicist, not a theologian; his religious views are not authoritative on theology.

**When authority is legitimate.** Citing a specialist in their field is not a fallacy. "The CDC says this vaccine is safe" is an appropriate appeal to legitimate authority. The fallacy is invoking authority outside its domain, or invoking a fabricated or contested authority.

### Appeal to Emotion (Argumentum ad Passiones)

**Pattern:** Using emotional manipulation (fear, pity, anger, flattery) instead of evidence.

**Example:** "If you don't donate, children will suffer." The emotional appeal may be true, but it does not by itself establish that donating to *this* charity is effective, efficient, or necessary.

**Subtypes:**
- *Ad misericordiam* (to pity)
- *Ad baculum* (to force/threat)
- *Ad populum* (to the crowd, "everyone thinks so")

### Appeal to Ignorance (Argumentum ad Ignorantiam)

**Pattern:** Claiming something is true because it has not been proven false, or false because it has not been proven true.

**Example:** "No one has proved that ghosts don't exist, so they must exist." Absence of disproof is not proof of presence.

**The exception.** In some contexts (criminal law, scientific hypothesis testing) the burden of proof is structurally placed on one side, and failure to meet it does count against the claim. This is a legitimate asymmetry, not a fallacy, when the burden-of-proof convention is agreed.

## Family 2: Presumption Fallacies

These fallacies smuggle an unjustified assumption into the argument.

### False Dichotomy (False Dilemma)

**Pattern:** Presenting two options as the only possibilities when others exist.

**Example:** "Either we cut education or we raise taxes." This ignores reallocation, bond issuance, economic growth, and other options.

**Detection heuristic:** Whenever "either/or" is asserted, ask "or what else?"

### Begging the Question (Petitio Principii)

**Pattern:** Assuming what you are trying to prove.

**Example:** "Smoking is bad for you because it is harmful to your health." The conclusion and the premise are the same claim.

**Note.** The phrase "begs the question" is often misused in modern English to mean "raises the question." In its logical sense, it specifically means circular reasoning.

### Complex Question (Loaded Question)

**Pattern:** A question that contains a presupposition the answerer has not agreed to.

**Example:** "Have you stopped cheating on your exams?" Both "yes" and "no" concede that you were cheating. The fallacy is accepting the question at face value.

**Response:** Reject the presupposition explicitly. "I was never cheating, so there is nothing to stop."

### Slippery Slope

**Pattern:** Claiming that accepting one proposition will lead, through a chain of ever-worse consequences, to an unacceptable result, without establishing each link in the chain.

**Example:** "If we allow gay marriage, next we'll allow polygamy, and then people marrying their pets." Each step is asserted, none is argued.

**When it is legitimate.** Slippery-slope concerns are reasonable when the chain of consequences is actually established with evidence. The fallacy is asserting the chain without the evidence.

## Family 3: Ambiguity Fallacies

These fallacies exploit linguistic ambiguity -- a word or phrase that shifts meaning between premises.

### Equivocation

**Pattern:** Using a word with two meanings as if it had only one.

**Example:** "The sign said 'fine for parking here.' Since it says 'fine,' that means it's okay to park here." "Fine" means "penalty" in one context and "acceptable" in another.

**Classic philosophical example.** "Man is rational. No woman is a man. Therefore no woman is rational." Trades on "man" meaning both "human" and "male."

### Amphiboly

**Pattern:** Exploiting structural ambiguity in sentences.

**Example:** "I once shot an elephant in my pajamas. How it got in my pajamas, I'll never know." (Groucho Marx) The sentence is ambiguous about whose pajamas.

### Accent (Emphasis)

**Pattern:** Changing the meaning of a statement by shifting emphasis.

**Example:** "*I* didn't say he stole the money" (someone else said it) vs "I didn't say *he* stole the money" (someone else stole it). Same sentence, different emphases, different meanings.

## Family 4: Causal Fallacies

These fallacies confuse correlation with causation or misdiagnose causal structure.

### Post Hoc Ergo Propter Hoc

**Pattern:** "After this, therefore because of this." Assuming that because B followed A, A caused B.

**Example:** "I took vitamin C and my cold went away the next day. Vitamin C cures colds." The cold may have run its course independently.

**Detection heuristic:** Ask "what else happened between A and B? What would have happened without A?"

### Cum Hoc Ergo Propter Hoc

**Pattern:** "With this, therefore because of this." Assuming that because A and B occur together, A causes B (or vice versa).

**Example:** "Ice cream sales and drowning deaths both rise in summer. Ice cream causes drowning." Both are caused by summer weather; neither causes the other.

### Single Cause Fallacy

**Pattern:** Assuming an effect has only one cause.

**Example:** "The recession was caused by trade policy." Most large economic effects have many contributing causes. Oversimplifying to one cause for rhetorical force is a fallacy when the one cause is insufficient to explain the effect.

## Family 5: Statistical and Inductive Fallacies

These fallacies misapply evidence from data.

### Hasty Generalization

**Pattern:** Drawing a general conclusion from a sample too small, biased, or unrepresentative.

**Example:** "My grandfather smoked and lived to 95. Therefore smoking isn't dangerous." One data point does not generalize.

### Cherry-Picking

**Pattern:** Presenting only the data that supports your claim and ignoring data that contradicts it.

**Example:** "In 2023, Stock X had its best quarter in ten years" while omitting that it also had three of its worst quarters in ten years that same year.

### Base Rate Neglect

**Pattern:** Ignoring the baseline frequency of an event when reasoning about probabilities.

**Example:** "A 99% accurate test for a disease came back positive, so I'm 99% likely to have it." If the disease affects 1 in 10,000 people, the positive test still makes you more likely *not* to have it than to have it. Bayes' theorem governs this.

### Texas Sharpshooter Fallacy

**Pattern:** Selecting where to draw the target after the shots are fired. Finding patterns in random noise and declaring them meaningful.

**Example:** "Companies with green logos outperform the market." The search space of features is large enough that random-looking associations exist; the discovery is the product of search, not pattern.

## Detection Workflow

When evaluating an argument for informal fallacies:

1. **Identify the conclusion.** What is the argument actually trying to establish?
2. **Identify the premises.** What is offered as support?
3. **Ask: does each premise actually support the conclusion?** If the answer is no but the argument feels persuasive, a fallacy is likely present.
4. **Check the families.** Relevance (is the premise even about the conclusion?), presumption (is something being assumed?), ambiguity (are terms being used consistently?), causal (is correlation being mistaken for causation?), statistical (is the evidence adequate?).
5. **Name the specific fallacy** and state why it is a fallacy, not just label it.

## When NOT to Use This Skill

- **Arguments that are formally invalid.** Use `propositional-logic` or `predicate-logic`.
- **Claims that are simply wrong about facts** (not bad reasoning about facts). Fact-checking is a different discipline.
- **Disputes about values** rather than reasoning. Not every disagreement is a fallacy.
- **Rhetorical effectiveness** (which is not the same as correctness). An argument can be rhetorically powerful and also fallacious; both assessments have their place.

## Decision Guidance

When you spot an argument that feels off:

1. **Name the specific fallacy** you think is present.
2. **Quote the exact wording** that contains the fallacy.
3. **Explain why it is fallacious** in that specific context.
4. **Offer the steel-manned version** -- the best reconstruction of the argument without the fallacy -- and see whether it still supports the conclusion.
5. **Grant the conclusion** if the steel-manned version holds; reject it if it does not. This is the discipline that distinguishes analysis from point-scoring.

## Cross-References

- **russell agent:** Critical analysis, Principia heritage
- **quine agent:** Linguistic precision, equivocation detection
- **langer agent:** Pedagogical framing of fallacy detection
- **critical-argumentation skill:** Broader argument-evaluation practice
- **propositional-logic skill:** The formal-validity counterpart

## References

- Walton, D. (2008). *Informal Logic: A Pragmatic Approach*. 2nd edition. Cambridge University Press.
- Copi, I. M., Cohen, C., & McMahon, K. (2014). *Introduction to Logic*. 14th edition. Pearson.
- Hurley, P. J. (2018). *A Concise Introduction to Logic*. 13th edition. Cengage.
- Tindale, C. W. (2007). *Fallacies and Argument Appraisal*. Cambridge University Press.
- Hamblin, C. L. (1970). *Fallacies*. Methuen.
