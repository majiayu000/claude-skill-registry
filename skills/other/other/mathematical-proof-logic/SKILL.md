---
name: mathematical-proof-logic
description: The logical structure of mathematical proof -- how first-order logic, natural deduction, and semantic reasoning combine to produce rigorous mathematical arguments. Covers the logical skeleton of direct proof, contraposition, contradiction, cases, and induction; the role of definitions, lemmas, and theorems; how informal mathematical prose maps to formal deductive structure; and the difference between proof-as-object and proof-as-activity. Use when the question is "why is this a valid proof?" rather than "what proof technique applies?"
type: skill
category: logic
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/logic/mathematical-proof-logic/SKILL.md
superseded_by: null
---
# Mathematical Proof Logic

Mathematical proof is the oldest and most rigorous form of argumentation humans have developed. Its rigor comes from logic: every legitimate step in a proof must correspond to a rule of inference in some underlying logical system -- usually first-order logic with a background theory like ZFC set theory or Peano arithmetic. This skill is about the logical structure of proof, not the pragmatic heuristics for finding one. It answers the question "what makes this sequence of sentences a valid proof?" rather than "what trick should I try?" The complementary `proof-techniques` skill in the math department covers the latter.

**Agent affinity:** godel (metamathematics), tarski (semantic grounding), russell (Principia heritage)

**Concept IDs:** log-predicate-logic, log-proof-techniques, log-deductive-reasoning, log-mathematical-proof

## Proof as Logical Object

A mathematical proof is, formally, a finite sequence of sentences in a formal language such that every sentence is either:

1. An axiom of the background theory,
2. A previously established theorem (lemma), or
3. Inferred from earlier sentences by an inference rule of the logic.

The final sentence is the theorem proved. This is the **Hilbert-style** view of proof: a proof is a tree (or list) of formulas with rule-applications as its edges.

In practice, working mathematicians almost never write proofs in this fully formal style. They write prose that could, in principle, be expanded into a formal proof. The logical skeleton is always there underneath -- it is what verification, peer review, and automated proof assistants check against.

## The Underlying Logic

Most of mathematics runs on **first-order logic** (FOL) with a chosen background theory:

- **ZFC set theory** is the default for most of mathematics. Everything -- numbers, functions, groups, topological spaces -- is definable as a set.
- **Peano arithmetic (PA)** for number theory proper.
- **Second-order logic** in some contexts, but most practitioners prefer to stay first-order and handle second-order features set-theoretically.

Classical FOL is assumed unless the proof is explicitly constructive. In classical logic, double negation elimination (`¬¬p → p`) and the law of excluded middle (`p ∨ ¬p`) are available. In intuitionistic logic, they are not -- and proofs by contradiction that rely on them are rejected. Most mathematicians work classically; constructive mathematicians deliberately restrict themselves.

## Proof Structures as Logical Patterns

The famous "proof techniques" of undergraduate math classes are all specific deduction patterns in FOL. Understanding them as logical patterns clarifies why they work.

### Direct proof

To prove `P → Q`:
1. Assume P.
2. Derive Q.
3. Discharge the assumption, conclude `P → Q` (→I rule).

This is implication introduction, plain and simple.

### Proof by contrapositive

To prove `P → Q`, instead prove `¬Q → ¬P`. This works because `P → Q ≡ ¬Q → ¬P` (contrapositive equivalence in classical logic). Sometimes the contrapositive is much easier to work with.

### Proof by contradiction (reductio ad absurdum)

To prove P:
1. Assume ¬P.
2. Derive a contradiction (some formula of the form `φ ∧ ¬φ`).
3. Conclude P (negation elimination + double negation).

This relies on classical logic's double negation elimination. Constructivists accept a narrower form: you can prove ¬P by deriving a contradiction from P, but not P by deriving a contradiction from ¬P.

### Proof by cases

To prove Q from `P₁ ∨ P₂ ∨ ... ∨ Pₙ`:
1. Show Q follows from P₁.
2. Show Q follows from P₂.
3. ... and so on.
4. Conclude Q (disjunction elimination, ∨E).

The case split must be **exhaustive** -- every possibility must be covered -- and it is the author's job to state why.

### Proof by induction

Mathematical induction is a schema. To prove ∀n ∈ ℕ P(n):
1. **Base case**: Show P(0) (or P(1), depending on where you start).
2. **Inductive step**: Show ∀k (P(k) → P(k+1)).
3. Conclude ∀n P(n) by the principle of induction.

The principle of induction is an axiom of Peano arithmetic. It is not derivable from the other axioms; it is a primitive claim about the natural numbers. **Strong induction** (assume P holds for all m < n, prove P(n)) is equivalent.

### Existence proofs

To prove ∃x φ(x), two styles:

- **Constructive**: Exhibit a specific object t and show φ(t). This is ∃I on a concrete term.
- **Non-constructive**: Assume ¬∃x φ(x), derive a contradiction, conclude ∃x φ(x). This only works classically and does not tell you *which* x satisfies φ.

The distinction matters in some branches of mathematics (constructive analysis, type theory) and is invisible in most of ordinary mathematics.

### Uniqueness proofs

To prove "there is exactly one x such that P(x)":
1. **Existence**: prove ∃x P(x).
2. **Uniqueness**: prove ∀x ∀y (P(x) ∧ P(y) → x = y).

The two halves are separate obligations.

## Definitions, Axioms, Lemmas, Theorems

Mathematical texts distinguish several kinds of statements. The distinctions are mostly pragmatic but logically meaningful.

- **Definition**: A new symbol is introduced and given meaning in terms of already-established concepts. Logically, definitions are conservative extensions -- they add no new content but allow more compact expression.
- **Axiom**: A statement taken as true without proof. In a given theory, axioms are the base. Across theories, they are choices -- different axioms give different mathematics (Euclidean vs non-Euclidean geometry is the classic example).
- **Lemma**: A theorem proved as an intermediate step toward a larger result. Logically identical to a theorem, but flagged for the reader as auxiliary.
- **Proposition**: A minor theorem, usually stated without much fanfare.
- **Theorem**: A major result, the destination of a proof.
- **Corollary**: A result that follows immediately (often in a line or two) from a theorem.

All of these except definitions are **claims to be proved**, and the proof must be valid under the chosen logic and background theory.

## Informal Prose and Its Formal Shadow

Mathematical writing is prose that encodes a formal proof. Reading it requires parsing the prose back into deductive structure. Some common phrases and their logical meaning:

| Prose | Logical meaning |
|---|---|
| "Let x be ..." | Universal generalization setup (∀I preparation) or ∃E witness |
| "Assume for contradiction that ..." | Assumption for ¬I or indirect proof |
| "Without loss of generality ..." | Implicit case reduction, often by symmetry |
| "Clearly ..." | Author claims a step is obvious; reader must verify |
| "It suffices to show ..." | Replace current goal with a sufficient condition |
| "Conversely ..." | Proving the other direction of a biconditional |
| "By hypothesis ..." | Reference to an earlier assumption |
| "By definition ..." | Unfolding a definition |

**The "without loss of generality" pitfall.** "WLOG" is legitimate when a symmetry argument justifies it. It is fallacious when the author is actually doing only one case and pretending the other is symmetric without checking. Readers should always ask: what is the symmetry, and does it actually hold?

## Worked Example: A Classical Proof

**Theorem:** √2 is irrational.

**Proof.** Assume for contradiction that √2 is rational. Then √2 = p/q for some integers p, q with q ≠ 0, where p/q is in lowest terms (i.e., gcd(p, q) = 1).

Then 2 = p²/q², so p² = 2q².

Thus p² is even, so p is even (since the square of an odd number is odd).

Write p = 2k for some integer k. Then (2k)² = 2q², so 4k² = 2q², so q² = 2k².

Thus q² is even, so q is even.

But p and q are both even, contradicting the assumption that gcd(p, q) = 1.

Therefore √2 is not rational. ∎

**Logical skeleton:**

1. Assumption for contradiction: ∃p ∃q (integers, q ≠ 0, gcd(p,q) = 1, √2 = p/q)
2. ∃E: introduce witnesses p, q.
3. Algebraic manipulation: p² = 2q² (arithmetic and definition of /).
4. Lemma: p² even → p even. (Contrapositive of: p odd → p² odd.)
5. ∃I: witness p = 2k for some k.
6. Algebraic manipulation: q² = 2k².
7. Lemma: q² even → q even.
8. Derive: 2 | p and 2 | q, contradicting gcd(p, q) = 1.
9. ¬I: conclude ¬(√2 rational).
10. Double negation elimination: √2 irrational.

This makes visible what the prose hides: the proof uses classical logic (step 10), it invokes a sub-lemma (steps 4, 7), and it uses existential elimination (step 2). The informal phrase "assume for contradiction" corresponds to opening a sub-proof that will end in ¬I.

## Common Errors in Proofs

### Missing cases

The proof handles some cases and silently skips others. Detection: for every "without loss of generality," ask whether the skipped case genuinely reduces to the handled one.

### Circular reasoning

The proof uses its own conclusion (or a near-equivalent) as a premise. Detection: check whether the definitions and lemmas actually preceded the current proof, or whether they implicitly assume what is being proved.

### Quantifier-scope errors

"For every ε > 0 there exists δ > 0" (∀ε ∃δ) is confused with "there exists δ > 0 such that for every ε > 0" (∃δ ∀ε). This is the single most common error in undergraduate real analysis.

### Wrong domain

A claim is proved for one structure and silently applied to another. "All groups are abelian" -- true for some groups, false in general.

### Appeal to intuition

"Obviously" when it is not obvious. The reader should be able to fill in every "obviously" with a line of formal reasoning; if not, the step is a gap.

## Proof Assistants and Formal Verification

Automated proof assistants (Coq, Lean, Isabelle/HOL, Agda) require proofs to be written in a formal language where every step is machine-checkable. This is the Hilbert vision realized.

The **Four Color Theorem** (proved 1976 with computer assistance, formalized in Coq 2005) and the **Kepler conjecture** (proved 1998, formalized in Isabelle 2014) are the landmark cases showing that even the most ambitious proofs can be formalized.

Most working mathematicians do not yet use proof assistants in their daily practice, but the gap is narrowing. The **Lean mathlib** project, in particular, has assembled a large library of formalized undergraduate and graduate mathematics.

## Godel's Incompleteness Theorems

A metamathematical result that every student of proof logic should know:

**First incompleteness theorem (1931):** Any consistent formal theory that is sufficiently strong to encode elementary arithmetic is **incomplete** -- there exist true statements in the language of the theory that cannot be proved within it.

**Second incompleteness theorem:** Such a theory cannot prove its own consistency.

Incompleteness does not say "some math is unprovable in principle" -- it says no single formal system captures all mathematical truth. Different systems may prove different things; choosing a stronger system can prove more, but at the cost of stronger (and potentially more suspect) axioms.

This is why Godel is the metamathematics specialist in the logic department.

## When NOT to Use This Skill

- **Finding a proof.** Use `proof-techniques` (math department) for heuristics.
- **Informal argumentation.** Use `critical-argumentation`.
- **Fallacy classification.** Use `informal-fallacies`.
- **Pure propositional or predicate logic exercises with no mathematical content.** Use `propositional-logic` or `predicate-logic`.

## Decision Guidance

When evaluating a mathematical proof:

1. **Identify the theorem** and its logical form (conditional, universal, existential, biconditional).
2. **Identify the proof structure** (direct, contrapositive, contradiction, cases, induction).
3. **Check each step** against a rule of inference or a cited lemma.
4. **Verify quantifier scope** carefully -- alternation order is the most common failure point.
5. **Flag implicit assumptions** -- WLOG, "clearly," unstated lemmas. Ask whether each is defensible.
6. **Confirm the conclusion matches the stated theorem** -- proofs sometimes drift into proving something weaker.

## Cross-References

- **godel agent:** Incompleteness, metamathematics
- **tarski agent:** Semantic definition of truth, model theory
- **russell agent:** Principia Mathematica, type theory
- **predicate-logic skill:** The working language of proof
- **proof-techniques skill (math):** Heuristics for finding proofs

## References

- Velleman, D. J. (2006). *How to Prove It: A Structured Approach*. 2nd edition. Cambridge University Press.
- Hammack, R. (2018). *Book of Proof*. 3rd edition. Virginia Commonwealth University.
- Polya, G. (1945). *How to Solve It*. Princeton University Press.
- Lakatos, I. (1976). *Proofs and Refutations*. Cambridge University Press.
- Godel, K. (1931). "Uber formal unentscheidbare Satze der Principia Mathematica und verwandter Systeme I." *Monatshefte fur Mathematik und Physik* 38, 173-198.
- Avigad, J. (2021). *Mathematical Logic and Computation*. Cambridge University Press.
