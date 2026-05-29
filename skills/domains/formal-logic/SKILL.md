---
name: formal-logic
description: Formal and informal logic for philosophical reasoning. Covers propositional logic (connectives, truth tables, tautologies), predicate logic (quantifiers, validity), syllogistic logic (Aristotle's original forms), natural deduction (introduction/elimination rules), modal logic (necessity, possibility, possible worlds), and a catalog of 15+ informal fallacies. Use when analyzing arguments, identifying logical form, evaluating validity and soundness, or detecting fallacious reasoning.
type: skill
category: philosophy
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/philosophy/formal-logic/SKILL.md
superseded_by: null
---
# Formal Logic

Logic is the study of valid reasoning. It provides the scaffolding on which all philosophical argument rests — without it, philosophy is rhetoric. This skill covers formal systems (propositional, predicate, syllogistic, modal) and informal reasoning (fallacy detection, argument mapping), with worked examples drawn from the philosophical tradition.

**Agent affinity:** aristotle (logic and epistemology, Opus)

**Concept IDs:** philo-argument-structure, philo-deductive-reasoning, philo-logical-fallacies

## The Logic Landscape at a Glance

| # | Domain | Core question | Key tools |
|---|---|---|---|
| 1 | Propositional logic | Is the compound statement true? | Connectives, truth tables, tautologies |
| 2 | Predicate logic | Does the claim hold for all/some objects? | Quantifiers, domains, free/bound variables |
| 3 | Syllogistic logic | What follows from categorical premises? | Figures, moods, Venn diagrams |
| 4 | Natural deduction | Can we derive the conclusion step by step? | Introduction/elimination rules |
| 5 | Modal logic | Is it necessarily or possibly true? | Box/diamond, possible worlds, accessibility |
| 6 | Informal fallacies | Where does the reasoning go wrong? | Fallacy taxonomy, argument reconstruction |
| 7 | Argument mapping | What is the logical structure of this passage? | Premise identification, diagram construction |

## 1 — Propositional Logic

**Core idea.** Propositional logic studies the truth-functional relationships between whole statements (propositions) connected by logical operators.

### The Five Connectives

| Symbol | Name | English | True when |
|---|---|---|---|
| neg | Negation | "not P" | P is false |
| /\ | Conjunction | "P and Q" | Both P and Q are true |
| \/ | Disjunction | "P or Q" | At least one is true |
| -> | Conditional | "if P then Q" | P is false, or Q is true |
| <-> | Biconditional | "P if and only if Q" | Both have the same truth value |

### Truth Tables

A truth table exhaustively lists all possible truth-value assignments for a compound proposition.

**Worked example.** *Show that P -> Q is logically equivalent to neg-P \/ Q.*

| P | Q | P -> Q | neg-P | neg-P \/ Q |
|---|---|--------|-------|-----------|
| T | T | T | F | T |
| T | F | F | F | F |
| F | T | T | T | T |
| F | F | T | T | T |

The columns for P -> Q and neg-P \/ Q are identical. The equivalence holds. This is the material conditional — a fact that surprises students, since "if P then Q" in ordinary language carries pragmatic implications (relevance, causation) that the material conditional does not.

### Tautologies, Contradictions, Contingencies

- **Tautology:** True under every assignment. Example: P \/ neg-P (law of excluded middle).
- **Contradiction:** False under every assignment. Example: P /\ neg-P.
- **Contingency:** True under some assignments, false under others. Example: P -> Q.

**Key tautologies for philosophy:**
- Modus ponens: ((P -> Q) /\ P) -> Q
- Modus tollens: ((P -> Q) /\ neg-Q) -> neg-P
- Hypothetical syllogism: ((P -> Q) /\ (Q -> R)) -> (P -> R)
- De Morgan's laws: neg(P /\ Q) <-> (neg-P \/ neg-Q) and neg(P \/ Q) <-> (neg-P /\ neg-Q)
- Contraposition: (P -> Q) <-> (neg-Q -> neg-P)
- Double negation: neg-neg-P <-> P (classical logic; fails in intuitionistic logic)

## 2 — Predicate Logic

**Core idea.** Predicate logic extends propositional logic by analyzing the internal structure of propositions — subjects, predicates, and quantifiers.

### Quantifiers

- **Universal (forall x):** "For every x in the domain, P(x) holds."
- **Existential (exists x):** "There is at least one x in the domain such that P(x) holds."

### Validity in Predicate Logic

**Worked example.** *Analyze: "All philosophers are mortal. Socrates is a philosopher. Therefore Socrates is mortal."*

Let P(x) = "x is a philosopher," M(x) = "x is mortal," s = Socrates.

1. forall x (P(x) -> M(x))  [Premise]
2. P(s)                      [Premise]
3. P(s) -> M(s)              [Universal instantiation from 1]
4. M(s)                      [Modus ponens from 2, 3]

The argument is valid. The conclusion follows necessarily from the premises. Whether it is sound depends on whether the premises are true — a separate question.

### Validity vs. Soundness

This distinction is among the most important in philosophy:

- **Valid:** The conclusion follows logically from the premises (the form is truth-preserving).
- **Sound:** The argument is valid AND all premises are true.
- **Invalid arguments can have true conclusions.** "All cats are mammals. All mammals are cats. Therefore all cats are mammals." The conclusion is true, but the argument is invalid (the second premise is false, and the form is flawed).

**Worked example.** *A valid but unsound argument:*

1. All birds can fly.          [False premise — penguins, ostriches]
2. Penguins are birds.         [True]
3. Therefore penguins can fly.  [False conclusion]

The argument is valid (the conclusion follows from the premises) but unsound (premise 1 is false).

## 3 — Syllogistic Logic

**Core idea.** Aristotle (384-322 BCE) systematized reasoning about categorical propositions — statements asserting that all, no, or some members of one category belong to another.

### The Four Categorical Forms

| Form | Name | Example |
|------|------|---------|
| A: All S are P | Universal affirmative | All humans are mortal |
| E: No S are P | Universal negative | No reptiles are mammals |
| I: Some S are P | Particular affirmative | Some philosophers are scientists |
| O: Some S are not P | Particular negative | Some animals are not domesticated |

### Figures and Moods

A categorical syllogism has two premises and a conclusion, each in one of the four forms, with exactly three terms (major, minor, middle). The four figures are determined by the position of the middle term:

- **Figure 1:** Middle is subject of major, predicate of minor (Barbara, Celarent, Darii, Ferio)
- **Figure 2:** Middle is predicate of both (Cesare, Camestres, Festino, Baroco)
- **Figure 3:** Middle is subject of both (Darapti, Disamis, Datisi, Felapton, Bocardo, Ferison)
- **Figure 4:** Middle is predicate of major, subject of minor (Bramantip, Camenes, Dimaris, Fesapo, Fresison)

**Worked example — Barbara (AAA-1):**

1. All mammals are animals.     [A: All M are P]
2. All dogs are mammals.        [A: All S are M]
3. Therefore all dogs are animals. [A: All S are P]

The medieval mnemonic names encode the mood: "Barbara" = A-A-A in Figure 1. There are exactly 24 valid syllogistic forms (15 without existential import assumptions).

## 4 — Natural Deduction

**Core idea.** Natural deduction formalizes reasoning as a sequence of rule applications, each introducing or eliminating a logical connective. Developed independently by Gentzen (1934) and Jaskowski (1934).

### Introduction and Elimination Rules

| Connective | Introduction | Elimination |
|------------|-------------|-------------|
| /\ | From A and B, infer A /\ B | From A /\ B, infer A (or B) |
| \/ | From A, infer A \/ B | From A \/ B, if A leads to C and B leads to C, infer C |
| -> | Assume A, derive B; discharge assumption, infer A -> B | From A -> B and A, infer B (modus ponens) |
| neg | Assume A, derive contradiction; infer neg-A | From neg-neg-A, infer A (classical) |
| forall | If P(a) for arbitrary a, infer forall x P(x) | From forall x P(x), infer P(t) for any term t |
| exists | From P(t), infer exists x P(x) | From exists x P(x), if P(a) leads to C (a fresh), infer C |

**Worked example.** *Prove: from (P -> Q) and (Q -> R), derive (P -> R).*

1. P -> Q          [Premise]
2. Q -> R          [Premise]
3. | P             [Assumption for conditional proof]
4. | Q             [Modus ponens: 1, 3]
5. | R             [Modus ponens: 2, 4]
6. P -> R          [Conditional introduction: 3-5, discharge assumption P]

This is the hypothetical syllogism derived as a theorem rather than taken as an axiom.

## 5 — Modal Logic

**Core idea.** Modal logic extends classical logic with operators for necessity (box, "it must be the case that") and possibility (diamond, "it could be the case that"). Formalized by C. I. Lewis (1918), given possible-worlds semantics by Kripke (1959, 1963).

### Possible Worlds Semantics

A proposition is:
- **Necessarily true (box-P):** True in every possible world accessible from the actual world.
- **Possibly true (diamond-P):** True in at least one accessible possible world.
- **Contingent:** True in some worlds, false in others.

**Duality:** box-P is equivalent to neg-diamond-neg-P. diamond-P is equivalent to neg-box-neg-P.

### The Five Standard Systems

| System | Axiom | Accessibility relation | Philosophical use |
|--------|-------|----------------------|-------------------|
| K | box(P -> Q) -> (box-P -> box-Q) | No constraints | Minimal modal logic |
| T | box-P -> P | Reflexive | What is necessary is actual |
| S4 | box-P -> box-box-P | Reflexive + transitive | Logical necessity |
| B | P -> box-diamond-P | Reflexive + symmetric | If P, then necessarily P is possible |
| S5 | diamond-P -> box-diamond-P | Equivalence relation | Metaphysical necessity (Kripke, Plantinga) |

**Worked example — Ontological argument in modal logic (Plantinga's version):**

1. It is possible that a maximally great being exists. [diamond-G]
2. If it is possible that a maximally great being exists, then a maximally great being exists in some possible world. [From 1, by possible-worlds semantics]
3. If a maximally great being exists in some possible world, it exists in every possible world (by definition of maximal greatness). [box-G in that world; S5 propagation]
4. If it exists in every possible world, it exists in the actual world. [T axiom: box-G -> G]
5. Therefore a maximally great being exists. [G]

The philosophical controversy is not the logic (which is valid in S5) but premise 1: is it genuinely possible that such a being exists, or does the premise smuggle in the conclusion? This illustrates how formal logic clarifies where the real disagreement lies.

## 6 — Informal Fallacies: A Catalog of 18

Informal fallacies are errors in reasoning that cannot be captured by formal invalidity alone — they involve content, context, or pragmatic violations.

### Fallacies of Relevance

| # | Fallacy | Latin name | Pattern | Example |
|---|---------|-----------|---------|---------|
| 1 | Ad hominem | argumentum ad hominem | Attack the person, not the argument | "You can't trust her ethics paper — she cheated on her taxes." |
| 2 | Straw man | — | Misrepresent the opponent's position, then attack the misrepresentation | "Vegetarians want to ban all farming." |
| 3 | Appeal to authority | argumentum ad verecundiam | Cite an irrelevant authority | "A famous actor says vaccines are dangerous, so they must be." |
| 4 | Appeal to emotion | argumentum ad passiones | Substitute emotion for evidence | "Think of the children!" (without relevant policy argument) |
| 5 | Appeal to popularity | argumentum ad populum | "Everyone believes it, so it's true" | "Millions of people believe in astrology." |
| 6 | Red herring | ignoratio elenchi | Introduce an irrelevant topic to divert attention | Answering "What about your policy on X?" with an unrelated issue |
| 7 | Tu quoque | — | "You do it too" | "You say smoking is bad, but you smoke." |

### Fallacies of Presumption

| # | Fallacy | Pattern | Example |
|---|---------|---------|---------|
| 8 | Begging the question (petitio principii) | Assume the conclusion in the premises | "God exists because the Bible says so, and the Bible is true because it is the word of God." |
| 9 | False dilemma | Present only two options when more exist | "You're either with us or against us." |
| 10 | Slippery slope | Claim one step inevitably leads to extreme consequences without justification | "If we allow X, next they'll allow Y, then Z..." |
| 11 | Hasty generalization | Conclude from too few cases | "I met two rude people from that city; everyone there is rude." |
| 12 | Composition | What is true of parts must be true of the whole | "Every player on the team is excellent, so the team must be excellent." |
| 13 | Division | What is true of the whole must be true of every part | "The university is prestigious, so every department must be prestigious." |

### Fallacies of Ambiguity and Causation

| # | Fallacy | Pattern | Example |
|---|---------|---------|---------|
| 14 | Equivocation | Shift the meaning of a term mid-argument | "The end of a thing is its perfection; death is the end of life; therefore death is the perfection of life." |
| 15 | Post hoc ergo propter hoc | Assume temporal sequence implies causation | "I wore my lucky socks and we won." |
| 16 | Affirming the consequent | If P then Q; Q; therefore P | "If it rains, the ground is wet. The ground is wet. Therefore it rained." (Sprinklers?) |
| 17 | Denying the antecedent | If P then Q; not P; therefore not Q | "If you study, you'll pass. You didn't study. Therefore you won't pass." (Natural talent?) |
| 18 | No true Scotsman | Redefine terms to exclude counterexamples | "No true philosopher would reject free will." "What about hard determinists?" "Well, they're not true philosophers." |

**Worked example — Detecting a straw man in philosophical debate:**

*Original argument:* "Singer argues that we have a moral obligation to donate to effective charities when doing so would prevent suffering without sacrificing anything of comparable moral importance."

*Straw man:* "Singer wants everyone to give away all their money and live in poverty."

*Analysis:* Singer's actual position includes the qualifier "without sacrificing anything of comparable moral importance." The straw man removes this qualifier, making the position appear extreme and easy to dismiss. A charitable reconstruction would engage with the actual threshold Singer proposes.

## 7 — Argument Mapping

**Core idea.** Argument mapping extracts the logical structure of a passage of natural language, identifying premises, conclusions, sub-arguments, and inferential connections.

### The Reconstruction Process

1. **Identify the conclusion.** What is the author trying to establish?
2. **Identify stated premises.** What reasons are explicitly given?
3. **Identify unstated premises.** What assumptions are required to make the argument valid?
4. **Map the structure.** Which premises support which conclusions? Are there sub-arguments?
5. **Evaluate.** Are the premises true? Is the inference valid? Are there fallacies?

**Worked example — Reconstructing Descartes' Cogito:**

*Text:* "I resolved to pretend that everything that had ever entered my mind was no more true than the illusions of my dreams. But immediately I noticed that, while I was thus trying to think everything false, it was necessary that I, who was thinking this, was something. And observing that this truth 'I think, therefore I am' was so firm and sure that the most extravagant suppositions of the sceptics were incapable of shaking it..." (Discourse on Method, Part IV)

*Reconstruction:*

- P1: I can doubt everything I have ever believed. [Stated]
- P2: The act of doubting is itself a form of thinking. [Unstated but required]
- P3: If I am thinking, then I must exist as a thinking thing. [Stated implicitly: "it was necessary that I... was something"]
- C1: Even under maximal doubt, I cannot doubt that I exist. [From P1, P2, P3]
- C2: "I think, therefore I am" (cogito ergo sum) is indubitable. [From C1]

*Evaluation:* The argument is deductively valid. The controversial premise is P2 — does doubting require a "doubter"? Lichtenberg (1793) and Nietzsche later questioned whether the cogito smuggles in the concept of a unified "I" that goes beyond what the bare experience of thinking warrants.

## Logical Form Identification

A critical skill in philosophy is translating natural language into logical form to test validity.

**Worked example.** *"If knowledge requires certainty, and nothing based on sensory experience is certain, then no empirical belief counts as knowledge."*

Let K = "knowledge requires certainty," C = "nothing based on sensory experience is certain," E = "no empirical belief counts as knowledge."

Logical form: (K /\ C) -> E

This is a valid conditional. The philosophical debate is over the premises: foundationalists may accept K (and try to save empirical knowledge by arguing against C), while fallibilists reject K entirely.

## When to Use This Skill

- Analyzing the logical structure of philosophical arguments
- Evaluating whether conclusions follow from premises
- Detecting fallacies in reasoning (philosophical, political, everyday)
- Translating natural-language arguments into formal notation
- Assessing the validity and soundness of complex multi-premise arguments
- Constructing truth tables or formal proofs
- Understanding modal claims about necessity and possibility

## When NOT to Use This Skill

- When the philosophical work is primarily interpretive or hermeneutic (use critical-thinking skill instead)
- When the question is about the truth of premises rather than the validity of inference (use epistemology or ethics skills)
- When formal logic would obscure rather than illuminate — some philosophical insights resist formalization, and forcing them into symbolic form distorts the original reasoning
- When the argument is primarily dialectical or conversational (use critical-thinking skill for Socratic method)

## Cross-References

- **aristotle agent:** Primary agent for logic and epistemology. Expert in syllogistic reasoning, argument evaluation, and the Organon.
- **socrates agent:** Socratic questioning that generates the arguments this skill analyzes.
- **dewey agent:** Connects formal logic to practical reasoning and educational contexts.
- **critical-thinking skill:** Informal reasoning, Socratic method, and argument analysis in natural language.
- **epistemology skill:** Logic applied to questions about knowledge, justification, and evidence.
- **ethics skill:** Logic applied to moral reasoning — identifying valid and invalid ethical arguments.

## References

- Aristotle. *Prior Analytics* and *Posterior Analytics*. (~350 BCE). The foundational texts of formal logic.
- Gentzen, G. (1934). "Untersuchungen uber das logische Schliessen." *Mathematische Zeitschrift*, 39, 176-210, 405-431.
- Kripke, S. (1963). "Semantical Considerations on Modal Logic." *Acta Philosophica Fennica*, 16, 83-94.
- Copi, I. M., Cohen, C., & McMahon, K. (2014). *Introduction to Logic*. 14th edition. Routledge.
- Hurley, P. J. (2014). *A Concise Introduction to Logic*. 12th edition. Cengage.
- Priest, G. (2008). *An Introduction to Non-Classical Logic*. 2nd edition. Cambridge University Press.
- Hamblin, C. L. (1970). *Fallacies*. Methuen. The definitive historical study of fallacy theory.
- Walton, D. (2008). *Informal Logic: A Pragmatic Approach*. 2nd edition. Cambridge University Press.
