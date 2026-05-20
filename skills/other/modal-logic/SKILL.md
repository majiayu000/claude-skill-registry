---
name: modal-logic
description: Extending propositional and predicate logic with modal operators -- necessity and possibility, and their relatives (obligation, knowledge, belief, time). Covers Kripke possible-worlds semantics, accessibility relations, the main modal systems (K, T, S4, S5), translation from natural language, and applications in epistemic, deontic, and temporal reasoning. Use when ordinary logic is insufficient to capture distinctions like "must" vs "might," "knows" vs "believes," "always" vs "sometimes."
type: skill
category: logic
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/logic/modal-logic/SKILL.md
superseded_by: null
---
# Modal Logic

Modal logic extends standard logic with operators for modes of truth -- most centrally necessity (□, "box") and possibility (◇, "diamond"). "It is possible that it will rain" is not the same claim as "it will rain," and ordinary propositional logic cannot distinguish them. Modal logic can. The framework also generalizes: the same machinery handles obligation and permission (deontic logic), knowledge and belief (epistemic logic), past and future (temporal logic), and provability (provability logic). The common semantic foundation is Saul Kripke's possible-worlds model. This skill covers the syntax, semantics, proof theory, and applications of modal logic at the level of an upper-undergraduate or early-graduate logic course.

**Agent affinity:** frege (foundational framing), quine (resistance and critique), tarski (semantic discipline)

**Concept IDs:** log-propositional-logic, log-predicate-logic, log-proof-techniques, log-logic-in-law

## The Modal Operators

The basic modal operators are:

- **□φ** -- "It is necessary that φ" (necessarily φ)
- **◇φ** -- "It is possible that φ" (possibly φ)

They are interdefinable:

- ◇φ ≡ ¬□¬φ -- "possibly φ" means "not necessarily not φ"
- □φ ≡ ¬◇¬φ -- "necessarily φ" means "not possibly not φ"

These duality relations are the modal counterparts of the quantifier dualities in predicate logic, and in Kripke semantics they will turn out to be exactly that.

## Possible Worlds: Kripke Semantics

Saul Kripke's 1959 paper "A Completeness Theorem in Modal Logic" gave the semantic foundation that made modal logic rigorous. The idea:

A **Kripke frame** is a pair ⟨W, R⟩:

- W is a nonempty set of **possible worlds**
- R ⊆ W × W is an **accessibility relation** between worlds

A **Kripke model** adds a valuation V that assigns a truth value to each atomic proposition at each world.

Truth at a world w in a model:

- Atomic p is true at w iff V(w, p) = T
- ¬φ is true at w iff φ is not true at w
- φ ∧ ψ (and other connectives) work as in propositional logic, evaluated locally at w
- **□φ is true at w iff φ is true at every world v such that wRv**
- **◇φ is true at w iff φ is true at some world v such that wRv**

So □ quantifies universally and ◇ quantifies existentially over *accessible* worlds.

**The intuition.** A "possible world" is a complete alternative way things might be. The actual world is one such alternative. The accessibility relation encodes which alternatives are "live" from a given standpoint. Different modal notions (necessity, obligation, knowledge, time) correspond to different accessibility relations.

## The Main Modal Systems

Different modal logics result from different constraints on the accessibility relation R. Each extra constraint validates additional axioms.

### System K

The minimal normal modal logic. Axioms:

- All propositional tautologies
- **K axiom**: □(φ → ψ) → (□φ → □ψ) (necessitation distributes over implication)
- **Necessitation rule**: from ⊢ φ, infer ⊢ □φ

K imposes no constraints on R. It is sound and complete for the class of all Kripke frames.

### System T (Reflexivity)

Add **T axiom**: □φ → φ. "Whatever is necessary is actually true."

Valid iff R is **reflexive**: every world accesses itself.

### System S4 (Reflexive + Transitive)

T plus **4 axiom**: □φ → □□φ. "What is necessary is necessarily necessary."

Valid iff R is reflexive and **transitive**: if wRv and vRu, then wRu.

### System S5 (Equivalence Relation)

S4 plus **5 axiom**: ◇φ → □◇φ. "What is possible is necessarily possible."

Valid iff R is an **equivalence relation**: reflexive, symmetric, and transitive.

S5 is the strongest commonly studied modal system. In S5, the accessibility structure collapses -- every world accesses every other world in its equivalence class. This matches our intuition about logical (or metaphysical) necessity: something is necessary if it holds in every possible world, period, without the filtering that weaker accessibility relations provide.

## Translation from Natural Language

Translating English modal sentences requires care.

### Necessity and possibility

"It is necessary that it is raining" → □R.

"It is possible that it is raining" → ◇R.

### Ambiguous scope

"A bachelor is necessarily unmarried." Two readings:

- **De dicto** (about the sentence): □∀x (Bachelor(x) → Unmarried(x)) -- "necessarily, all bachelors are unmarried"
- **De re** (about the thing): ∀x (Bachelor(x) → □Unmarried(x)) -- "for every bachelor, he is necessarily unmarried"

These are not equivalent. De dicto says the sentence is necessarily true; de re says each bachelor has a necessary property. The de re reading is much stronger and more contentious.

### "Must" is ambiguous

"It must be raining" can be epistemic (I conclude from the wet ground) or deontic (it is obligatory that it rain -- strange in English but possible in other contexts). Modal logics distinguish these with different operators.

## Epistemic Logic

In epistemic logic, the modal operator is interpreted as knowledge:

- **Kᵢφ** -- "Agent i knows that φ"

The accessibility relation connects worlds that are epistemically indistinguishable for agent i. If w and v are indistinguishable to agent i from w's standpoint, then agent i cannot rule out v as the actual world, so Kᵢφ requires φ to hold in both.

### Standard axioms

- **K**: Kᵢ(φ → ψ) → (Kᵢφ → Kᵢψ). Logical omniscience: agents know all logical consequences of what they know. (This is an idealization.)
- **T**: Kᵢφ → φ. Knowledge implies truth. Agents cannot "know" falsehoods.
- **4**: Kᵢφ → KᵢKᵢφ. Positive introspection: if you know something, you know that you know it.
- **5**: ¬Kᵢφ → Kᵢ¬Kᵢφ. Negative introspection: if you don't know something, you know that you don't.

Systems vary on which introspection axioms to accept. Most uncontroversial is T.

### Distinguishing knowledge and belief

Belief is sometimes formalized with a separate operator **Bᵢφ** that satisfies K and 4 but not T -- you can believe falsehoods.

## Deontic Logic

In deontic logic, the modal operator represents obligation:

- **Oφ** -- "It ought to be the case that φ"
- **Pφ** -- "It is permitted that φ"
- **Fφ** -- "It is forbidden that φ" = O¬φ

### Standard axioms

- **K**: O(φ → ψ) → (Oφ → Oψ)
- **D**: Oφ → ¬O¬φ. "Ought implies consistency" -- you cannot be obligated to do contradictory things. (Though real moral systems sometimes produce genuine dilemmas, which is one reason deontic logic is philosophically contested.)

The T axiom (Oφ → φ) is NOT adopted in deontic logic -- what ought to be is not always the case.

## Temporal Logic

Temporal logic replaces necessity and possibility with operators about time:

- **Gφ** -- "Always in the future, φ"
- **Fφ** -- "Sometime in the future, φ"
- **Hφ** -- "Always in the past, φ"
- **Pφ** -- "Sometime in the past, φ"

The accessibility relation is an earlier-later ordering. Different temporal logics model linear vs branching time, discrete vs continuous, etc. Temporal logic is critical in verification of concurrent systems (LTL, CTL, CTL*).

## Philosophical Issues

### Quine's skepticism

W. V. O. Quine was a famous skeptic of modal logic, especially quantified modal logic (QML). His central worry was about de re modality: quantifying into modal contexts raises questions about whether modal properties attach to objects themselves or only to descriptions. "The number of planets is necessarily greater than 7" -- what is the "number of planets" as a referent, independent of the actual astronomical fact?

This debate drove a great deal of 20th-century philosophical logic and is why the logic department's Quine agent carries a skeptical stance as a matter of role.

### Kripke's response

Kripke argued that de re modality was coherent and that rigid designators (terms that refer to the same object in every possible world) resolved Quine's puzzles. Kripke's *Naming and Necessity* (1980) is the landmark text.

### The necessity of origin

Kripke also argued for striking metaphysical claims like "a human being could not have had different parents" (necessity of origin). These claims are modal metaphysics, not modal logic per se, but they motivate much of the field.

## Worked Example: A Modal Proof

**Claim:** In system K, the formula □φ ∧ □ψ → □(φ ∧ ψ) is valid.

**Proof sketch:** Suppose □φ and □ψ are true at world w. By the semantics, φ is true at every world v with wRv, and ψ is true at every world v with wRv. Therefore at every such v, both φ and ψ are true, so φ ∧ ψ is true at v. Since this holds for every accessible v, □(φ ∧ ψ) is true at w.

This is a typical modal-semantic argument: chase the semantics across worlds.

## When NOT to Use This Skill

- **Arguments with no modal content.** Use `propositional-logic` or `predicate-logic`.
- **Arguments that are actually about informal persuasion.** Use `informal-fallacies` or `critical-argumentation`.
- **Mathematical proofs that happen to mention "necessarily."** Use `mathematical-proof-logic` -- "necessarily" in math usually means "in every model," which is first-order.

## Decision Guidance

When you encounter an argument involving modality:

1. **Identify the modal operators.** Is the key word "must," "could," "ought," "knows," "sometime"?
2. **Choose the system.** Alethic (necessity/possibility)? Epistemic? Deontic? Temporal?
3. **Pick the right strength.** K, T, S4, or S5? The choice depends on what introspection or reflexivity properties are intended.
4. **Check de dicto vs de re.** Where is the quantifier with respect to the modal operator?
5. **Evaluate in a Kripke model.** If you want to show validity, prove it for arbitrary accessibility relations in the system. If you want to show invalidity, construct a countermodel.

## Cross-References

- **frege agent:** Invention of quantifiers, foundational role
- **quine agent:** Skeptical framing, critique of QML
- **tarski agent:** Semantic discipline, model theory
- **propositional-logic skill:** The base system modal logic extends
- **predicate-logic skill:** Combined with modal to give quantified modal logic

## References

- Hughes, G. E., & Cresswell, M. J. (1996). *A New Introduction to Modal Logic*. Routledge.
- Kripke, S. (1959). "A Completeness Theorem in Modal Logic." *Journal of Symbolic Logic* 24(1), 1-14.
- Kripke, S. (1980). *Naming and Necessity*. Harvard University Press.
- Blackburn, P., de Rijke, M., & Venema, Y. (2001). *Modal Logic*. Cambridge University Press.
- Fagin, R., Halpern, J. Y., Moses, Y., & Vardi, M. Y. (2003). *Reasoning About Knowledge*. MIT Press.
- Quine, W. V. O. (1953). "Reference and Modality," in *From a Logical Point of View*. Harvard University Press.
