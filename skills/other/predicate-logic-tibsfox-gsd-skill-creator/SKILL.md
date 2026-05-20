---
name: predicate-logic
description: First-order logic with quantifiers, predicates, functions, and identity. Covers syntax, interpretation over a domain, the universal and existential quantifiers, quantifier scope and binding, translation from natural language with multi-variable predicates, natural deduction for quantifiers, undecidability at first order, and the soundness/completeness theorems. Use when propositional logic is insufficient -- whenever "for all" or "there exists" matters to the argument.
type: skill
category: logic
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/logic/predicate-logic/SKILL.md
superseded_by: null
---
# Predicate Logic (First-Order Logic)

Predicate logic -- also called first-order logic (FOL) or quantificational logic -- extends propositional logic with the machinery of quantification. Where propositional logic can express "Socrates is mortal" as an atomic sentence, predicate logic can express "every man is mortal" as `∀x (Man(x) → Mortal(x))` and then actually derive "Socrates is mortal" from it. This expressive jump is what allows logic to capture mathematical reasoning, natural-language quantifier interactions, and the semantics of programming languages. This skill covers the syntax, semantics, proof theory, and translation discipline of first-order logic.

**Agent affinity:** frege (foundational framing), russell (type-theoretic discipline), tarski (semantic definition of truth)

**Concept IDs:** log-predicate-logic, log-argument-structure, log-deductive-reasoning, log-proof-techniques

## Syntax: The Alphabet Expanded

First-order logic adds to the propositional alphabet:

- **Variables**: x, y, z, ..., ranging over objects in a domain
- **Constants**: a, b, c, ..., naming specific objects
- **Predicate symbols**: P, Q, R, ..., of arity 1, 2, 3, ... (one-place, two-place, etc.)
- **Function symbols**: f, g, h, ..., of positive arity
- **Quantifiers**: ∀ (universal, "for all"), ∃ (existential, "there exists")
- **Equality**: = (in FOL with identity)

**Terms** are built from variables, constants, and function applications. If f is a 2-place function symbol, then f(x, a) is a term.

**Atomic formulas** are predicate applications: P(t) or R(t, s), where t, s are terms.

**Formulas** are built from atomic formulas using the propositional connectives plus the two quantifier rules:

- If φ is a formula and x is a variable, then ∀x φ is a formula
- If φ is a formula and x is a variable, then ∃x φ is a formula

**Free and bound variables.** A variable x in a formula is **bound** if it lies inside the scope of a quantifier ∀x or ∃x. Otherwise it is **free**. A formula with no free variables is a **sentence** -- it has a definite truth value once the interpretation is fixed. A formula with free variables is **open** -- it is a property that some objects may satisfy.

## Semantics: Interpretation Over a Domain

An interpretation of a first-order language consists of:

1. A nonempty **domain** (also called universe) D of objects
2. For each constant c, an object c^I in D
3. For each n-place function symbol f, a function f^I : D^n → D
4. For each n-place predicate symbol P, a relation P^I ⊆ D^n

Given an interpretation and an assignment of domain elements to the free variables, every formula has a truth value, determined recursively:

- **∀x φ** is true if φ is true for every assignment of x to an element of D
- **∃x φ** is true if φ is true for at least one assignment of x to an element of D

This is Tarski's inductive definition of truth, which is why Tarski is the semantics specialist in this department.

## The Two Quantifiers

### Universal quantifier ∀

"For every x in the domain, property φ(x) holds."

In natural language: "all," "every," "any," "each," and sometimes "a" or "the" (depending on context -- "a whale is a mammal" usually means "every whale is a mammal").

Translation pattern: `∀x (P(x) → Q(x))`. Not `∀x (P(x) ∧ Q(x))` -- that says "every object in the domain has both P and Q," which is almost never what English "every P is Q" means.

### Existential quantifier ∃

"There is at least one x in the domain such that property φ(x) holds."

In natural language: "some," "there is," "there exists," "at least one," and sometimes "a" or "the" (again context-dependent -- "a student failed" usually means "some student failed").

Translation pattern: `∃x (P(x) ∧ Q(x))`. Not `∃x (P(x) → Q(x))` -- that is vacuously true as long as any object lacks P.

**The translation asymmetry** (universal uses →, existential uses ∧) is a persistent source of student confusion and is worth drilling until reflexive.

## Quantifier Scope and Alternation

### Scope

A quantifier's **scope** is the formula it governs, usually the smallest formula immediately following. Parentheses disambiguate. In `∀x (P(x) → Q(x))`, the scope of ∀x is the full conditional. In `∀x P(x) → Q(x)`, the scope is only P(x), and Q(x) has a free variable.

### Alternation order matters

`∀x ∃y Loves(x, y)` means: for every person, there is someone they love. Different person y for different x.

`∃y ∀x Loves(x, y)` means: there is one person y that everyone loves. Same y for every x.

These are not equivalent. In fact, `∃y ∀x φ(x, y)` **implies** `∀x ∃y φ(x, y)` but the reverse does not hold. This is the single deepest pitfall of quantifier logic.

### Quantifier duality (De Morgan for quantifiers)

| | |
|---|---|
| ¬∀x φ | ≡ ∃x ¬φ |
| ¬∃x φ | ≡ ∀x ¬φ |
| ¬∀x P(x) | "Not everything is P" ≡ "something is not P" |
| ¬∃x P(x) | "Nothing is P" ≡ "everything is not P" |

## Worked Example: Aristotle's Syllogism

**Argument:** All humans are mortal. Socrates is human. Therefore, Socrates is mortal.

**Formalization:** Let Human(x), Mortal(x) be one-place predicates, and let s denote Socrates.

```
Premise 1: ∀x (Human(x) → Mortal(x))
Premise 2: Human(s)
Conclusion: Mortal(s)
```

**Proof:**

1. ∀x (Human(x) → Mortal(x))        (Premise 1)
2. Human(s)                          (Premise 2)
3. Human(s) → Mortal(s)              (Universal elimination from 1, substituting s for x)
4. Mortal(s)                         (Modus ponens from 3 and 2)

This is the paradigm derivation of predicate logic. It looks trivial only because we have seen it a thousand times.

## Natural Deduction for Quantifiers

### Universal introduction (∀I)

If you can prove φ(x) for an arbitrary x (meaning x does not appear in any undischarged assumptions), you can conclude ∀x φ(x).

The "arbitrary" restriction is critical. You cannot introduce ∀ if you have been using specific properties of x.

### Universal elimination (∀E)

From ∀x φ(x), conclude φ(t) for any term t.

Substitution must be **capture-avoiding**: if t contains a variable y, and y would become bound by a quantifier in φ, rename bound variables first.

### Existential introduction (∃I)

From φ(t) for a specific term t, conclude ∃x φ(x).

### Existential elimination (∃E)

From ∃x φ(x), introduce a fresh variable (or constant) c and assume φ(c). If you can derive ψ from this assumption without using c outside the sub-derivation, conclude ψ.

The "fresh" restriction is critical. You cannot use ∃E on a variable that appears elsewhere.

## Translation Discipline

Translating English to FOL requires careful attention:

### "All" + "is" usually needs →

"All dogs bark" → `∀x (Dog(x) → Bark(x))`

### "Some" + "is" usually needs ∧

"Some dogs bark" → `∃x (Dog(x) ∧ Bark(x))`

### "No" requires negation

"No dogs meow" → `∀x (Dog(x) → ¬Meow(x))` ≡ `¬∃x (Dog(x) ∧ Meow(x))`

### Restricted quantification

"Every student passed" uses the restricted quantifier over students. Formalize: `∀x (Student(x) → Passed(x))`.

### Two-place predicates

"Alice loves Bob" → `Loves(a, b)` with constants a, b.

"Everyone loves Bob" → `∀x Loves(x, b)`.

"Alice loves everyone" → `∀x Loves(a, x)`.

"Everyone loves someone" → `∀x ∃y Loves(x, y)` (different someone for different x).

"Someone loves everyone" → `∃y ∀x Loves(x, y)` (same y for every x).

### Uniqueness and numerical quantifiers

"There is exactly one x such that P(x)" → `∃x (P(x) ∧ ∀y (P(y) → y = x))`.

"There are at least two P" → `∃x ∃y (P(x) ∧ P(y) ∧ x ≠ y)`.

"There are exactly two P" → combine both: at least two and at most two.

## Soundness and Completeness

**Soundness**: If a formula is provable in the deduction system, it is true in every interpretation. This guarantees you cannot derive a false conclusion from true premises.

**Completeness**: If a formula is true in every interpretation, it is provable. This is Godel's completeness theorem for first-order logic (1929, dissertation; published 1930) -- not to be confused with the incompleteness theorems, which are about specific theories within first-order logic.

The soundness + completeness pair means that "true in every interpretation" and "derivable in the deduction system" are exactly the same set. This is philosophically significant: it means first-order logic captures its own semantic notion of validity.

## Undecidability at First Order

Propositional logic is decidable. First-order logic is **undecidable** -- there is no algorithm that, given any first-order formula, always correctly determines whether it is valid in finite time. This is Church's theorem (1936) and independently Turing's proof via the halting problem.

First-order logic is **semi-decidable**: if a formula is valid, you can find a proof (given enough time), but if it is not valid, the search may run forever without terminating.

This is the first-order inflection point where logic meets computability theory. It is not a minor technical detail -- it sets the limits of what automated reasoning can do.

## When NOT to Use This Skill

- **Arguments with no quantifier structure.** Use `propositional-logic`.
- **Arguments essentially involving necessity or possibility.** Use `modal-logic`.
- **Rhetorical error classification.** Use `informal-fallacies`.
- **Mathematical proofs that use FOL as a tool but are really about math.** Use `mathematical-proof-logic`.

## Decision Guidance

When formalizing an argument into FOL:

1. **Identify the domain.** What are the objects? Humans? Numbers? Sets?
2. **Identify the predicates.** What properties and relations are being asserted?
3. **Identify the quantifier structure.** Where is "every," "some," "none"? What is the scope of each quantifier?
4. **Translate carefully.** All-is-→, some-is-∧, no requires negation. Alternation order matters.
5. **Derive or countermodel.** For valid arguments, give a natural-deduction proof. For invalid arguments, exhibit an interpretation where premises are true and conclusion false.

## Cross-References

- **frege agent:** Invention of quantifiers, Begriffsschrift, foundational framing
- **russell agent:** Type discipline, Russell's paradox, Principia
- **tarski agent:** Semantic definition of truth, model theory
- **propositional-logic skill:** The base system FOL extends
- **mathematical-proof-logic skill:** FOL as the working language of proof

## References

- Enderton, H. B. (2001). *A Mathematical Introduction to Logic*. 2nd edition. Academic Press.
- Mendelson, E. (2015). *Introduction to Mathematical Logic*. 6th edition. CRC Press.
- Frege, G. (1879). *Begriffsschrift*. Halle.
- Tarski, A. (1933/1956). "The Concept of Truth in Formalized Languages," in *Logic, Semantics, Metamathematics*. Oxford University Press.
- Church, A. (1936). "An unsolvable problem of elementary number theory." *American Journal of Mathematics* 58, 345-363.
- Godel, K. (1930). "Die Vollstandigkeit der Axiome des logischen Funktionenkalkuls." *Monatshefte fur Mathematik und Physik* 37, 349-360.
