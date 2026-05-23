---
name: propositional-logic
description: The logic of sentential connectives -- and, or, not, if-then, if-and-only-if -- as a formal system. Covers syntax (well-formed formulas), semantics (truth tables), satisfiability, validity, logical equivalence, normal forms (CNF, DNF), natural-deduction rules, and common translation pitfalls. Use when formalizing arguments with propositional structure, checking validity mechanically, or teaching the foundations of formal reasoning.
type: skill
category: logic
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/logic/propositional-logic/SKILL.md
superseded_by: null
---
# Propositional Logic

Propositional logic (also called sentential logic or zeroth-order logic) is the formal study of how truth values combine under sentential connectives. It is the entry point to formal logic and the foundation of every downstream system: predicate logic extends it with quantifiers, modal logic extends it with possibility and necessity, and computer science uses it everywhere from circuit design to SAT solvers. This skill covers the syntax, semantics, proof theory, and translation discipline of propositional logic as taught in introductory logic courses.

**Agent affinity:** boole (algebraic treatment), frege (axiomatic framing), russell (translation from natural language)

**Concept IDs:** log-propositional-logic, log-truth-tables, log-if-then-relationships, log-argument-structure

## Syntax: Well-Formed Formulas

The alphabet of propositional logic consists of:

- **Atomic propositions** (propositional variables): p, q, r, s, ..., usually lowercase letters, standing for indivisible declarative sentences
- **Connectives**: negation (not, symbolized as ¬ or ~), conjunction (and, ∧), disjunction (or, ∨), conditional (if...then, →), biconditional (if and only if, ↔)
- **Parentheses**: ( and ), used for grouping

A **well-formed formula (WFF)** is defined recursively:

1. Every atomic proposition is a WFF.
2. If φ is a WFF, then ¬φ is a WFF.
3. If φ and ψ are WFFs, then (φ ∧ ψ), (φ ∨ ψ), (φ → ψ), and (φ ↔ ψ) are WFFs.
4. Nothing else is a WFF.

**Precedence** (to reduce parentheses): ¬ binds tightest, then ∧, then ∨, then →, then ↔. So p ∨ q → r means (p ∨ q) → r, not p ∨ (q → r).

## Semantics: Truth Tables

Every connective is defined by a truth table -- a function from truth values of inputs to truth value of output. T denotes true, F denotes false.

| p | q | ¬p | p ∧ q | p ∨ q | p → q | p ↔ q |
|---|---|----|-------|-------|-------|-------|
| T | T | F  | T     | T     | T     | T     |
| T | F | F  | F     | T     | F     | F     |
| F | T | T  | F     | T     | T     | F     |
| F | F | T  | F     | F     | T     | T     |

**Note on the conditional.** "p → q" is **false only when p is true and q is false**. When p is false, p → q is true regardless of q. This "vacuous truth" is the single most common source of confusion for beginners. The textbook example: "If the moon is made of cheese, then 2 + 2 = 5" is true in propositional logic because the antecedent is false.

## Satisfiability, Validity, Equivalence

Three central concepts:

- **Satisfiable**: A formula has at least one truth assignment making it true. `p ∧ q` is satisfiable (T, T).
- **Unsatisfiable (contradiction)**: No assignment makes it true. `p ∧ ¬p` is unsatisfiable.
- **Valid (tautology)**: Every assignment makes it true. `p ∨ ¬p` is valid.
- **Equivalent**: Two formulas have the same truth table. `p → q` is equivalent to `¬p ∨ q`.

**The dual principle.** A formula φ is valid if and only if ¬φ is unsatisfiable. This is the foundation of proof-by-contradiction and of SAT-solver-based validity checking.

## Key Equivalences (Memorize)

These equivalences appear constantly and must be known cold:

| Name | Equivalence |
|---|---|
| Double negation | ¬¬p ≡ p |
| Idempotence | p ∧ p ≡ p; p ∨ p ≡ p |
| Commutativity | p ∧ q ≡ q ∧ p; p ∨ q ≡ q ∨ p |
| Associativity | (p ∧ q) ∧ r ≡ p ∧ (q ∧ r); same for ∨ |
| Distribution | p ∧ (q ∨ r) ≡ (p ∧ q) ∨ (p ∧ r); dual for ∨ over ∧ |
| De Morgan | ¬(p ∧ q) ≡ ¬p ∨ ¬q; ¬(p ∨ q) ≡ ¬p ∧ ¬q |
| Implication | p → q ≡ ¬p ∨ q |
| Contrapositive | p → q ≡ ¬q → ¬p |
| Biconditional | p ↔ q ≡ (p → q) ∧ (q → p) |
| Excluded middle | p ∨ ¬p is valid |
| Contradiction | p ∧ ¬p is unsatisfiable |

## Normal Forms

Every propositional formula can be rewritten into two canonical forms:

### Conjunctive Normal Form (CNF)

A conjunction of disjunctions of literals. Example: `(p ∨ ¬q) ∧ (¬p ∨ q ∨ r) ∧ (¬r)`.

CNF is the input format for most SAT solvers. The Tseitin transformation converts any formula to equisatisfiable CNF in linear time.

### Disjunctive Normal Form (DNF)

A disjunction of conjunctions of literals. Example: `(p ∧ q) ∨ (¬p ∧ r) ∨ (q ∧ ¬r)`.

DNF is useful for defining functions by case but can blow up exponentially. The Karnaugh map technique in digital logic is DNF minimization.

## Natural Deduction Rules

Natural deduction is the most common proof system for beginners because its rules match the way humans actually reason.

### Introduction rules

| Connective | Rule |
|---|---|
| ∧I | From φ and ψ, conclude φ ∧ ψ |
| ∨I | From φ, conclude φ ∨ ψ (for any ψ) |
| →I | Assume φ, derive ψ, conclude φ → ψ |
| ¬I | Assume φ, derive a contradiction, conclude ¬φ |
| ↔I | From φ → ψ and ψ → φ, conclude φ ↔ ψ |

### Elimination rules

| Connective | Rule |
|---|---|
| ∧E | From φ ∧ ψ, conclude φ; from φ ∧ ψ, conclude ψ |
| ∨E | From φ ∨ ψ, if assuming φ lets you conclude χ and assuming ψ lets you conclude χ, then χ |
| →E (modus ponens) | From φ → ψ and φ, conclude ψ |
| ¬E | From φ and ¬φ, conclude anything (ex falso) |
| ↔E | From φ ↔ ψ and φ, conclude ψ (and vice versa) |

## Translation from Natural Language

Most practical use of propositional logic starts with translating English sentences into formulas. Pitfalls:

### "If...then" is NOT causation

"If it rains, the street gets wet" formalizes as `R → W`. The conditional asserts truth-functional implication, not causal connection. "If 2 + 2 = 4, then grass is green" is true in propositional logic.

### "Unless" is the inclusive or

"The picnic is on unless it rains" formalizes as `picnic ∨ rain`. The natural reading "if it does not rain, the picnic is on" is logically equivalent: `¬rain → picnic` ≡ `rain ∨ picnic`.

### "Only if" is the converse of "if"

"Only if p, then q" formalizes as `q → p`. The "only if" direction is the implication *from* q *to* p. The most common error is conflating "only if" with "if," which gives the wrong direction.

### "Neither...nor" is joint negation

"Neither p nor q" is `¬p ∧ ¬q` (equivalently `¬(p ∨ q)`).

### "Either...or" is usually inclusive

"Either it's Tuesday or it's Wednesday" is typically `T ∨ W` (inclusive -- true if both, which is impossible for days but logically fine). Exclusive or is rare in natural language.

### Tense and modality are lost

Propositional logic has no tense and no modality. "It might rain" cannot be distinguished from "it will rain" at this level. This is the motivation for modal logic.

## Worked Example: Validity Check

**Claim:** The argument "If Socrates is a man, then Socrates is mortal. Socrates is a man. Therefore, Socrates is mortal" is valid.

**Formalization:** Let p = "Socrates is a man," q = "Socrates is mortal." The argument is:

```
Premise 1: p → q
Premise 2: p
Conclusion: q
```

**Validity check by truth table:**

| p | q | p → q | p | q |
|---|---|-------|---|---|
| T | T | T     | T | T |
| T | F | F     | T | F |
| F | T | T     | F | T |
| F | F | T     | F | F |

We need: every row where both premises are true, the conclusion is also true. Row 1 is the only row where `p → q` and `p` are both T; in that row, `q` is also T. Valid.

This is modus ponens, the single most-used rule in all of logic.

## Decision Procedures

Propositional logic is **decidable**: there is an algorithm that, given any formula, determines in finite time whether it is valid, satisfiable, or unsatisfiable.

### Truth tables

Exhaustive enumeration. Guaranteed to work. Exponential in the number of variables ($2^n$ rows for $n$ variables). Practical for up to 10-12 variables.

### DPLL / CDCL (SAT solvers)

Modern SAT solvers use the Davis-Putnam-Logemann-Loveland algorithm with conflict-driven clause learning. They routinely solve formulas with millions of variables, though the worst case remains exponential. NP-complete in theory, practically efficient for most real instances.

### Natural deduction

Not a decision procedure by itself -- finding a proof requires search -- but valid formulas always have natural-deduction proofs (completeness) and found proofs are trustworthy (soundness).

## When NOT to Use This Skill

- **Arguments that depend on quantifiers.** Use `predicate-logic`.
- **Arguments involving necessity or possibility.** Use `modal-logic`.
- **Arguments that are primarily about persuasion or rhetoric.** Use `critical-argumentation`.
- **Classification of rhetorical errors.** Use `informal-fallacies`.
- **Mathematical proofs.** Use `mathematical-proof-logic` for the proof structure; propositional logic is a building block within it.

## Decision Guidance

When formalizing an argument, follow this sequence:

1. **Identify the atomic propositions.** What are the indivisible declarative sentences?
2. **Identify the connectives.** Where does the argument use "and," "or," "not," "if...then," "if and only if"?
3. **Translate carefully.** Watch for the "unless," "only if," and "neither...nor" patterns that trip beginners.
4. **Check validity.** If the number of variables is small, use a truth table. For larger problems, apply known equivalences to simplify before testing.
5. **Name the rule.** Modus ponens, modus tollens, disjunctive syllogism, etc. Named rules are easier to verify and communicate.

## Cross-References

- **boole agent:** Algebraic treatment, Boolean laws
- **frege agent:** Axiomatic framing, Begriffsschrift heritage
- **russell agent:** Natural-language translation, type discipline
- **predicate-logic skill:** Extension with quantifiers
- **modal-logic skill:** Extension with necessity and possibility
- **mathematical-proof-logic skill:** Use of propositional rules in proofs

## References

- Enderton, H. B. (2001). *A Mathematical Introduction to Logic*. 2nd edition. Academic Press.
- Bergmann, M., Moor, J., & Nelson, J. (2013). *The Logic Book*. 6th edition. McGraw-Hill.
- Hurley, P. J. (2018). *A Concise Introduction to Logic*. 13th edition. Cengage.
- Boole, G. (1854). *An Investigation of the Laws of Thought*. Walton and Maberly.
- Frege, G. (1879). *Begriffsschrift*. Halle.
