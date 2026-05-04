---
name: proof-techniques
description: Proof writing and verification techniques for mathematical reasoning. Covers 13 proof strategies with canonical worked examples — direct, contrapositive, contradiction, cases, WLOG, vacuous/trivial, biconditional, counterexample, existence (constructive and non-constructive), uniqueness, induction (weak, strong, structural), pigeonhole/double-counting, and diagonal argument/invariants. Use when writing, verifying, or selecting proof strategies for any mathematical claim.
type: skill
category: math
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/math/proof-techniques/SKILL.md
superseded_by: null
---
# Proof Techniques

Mathematical proof is the mechanism by which conjectures become theorems. A proof is a finite sequence of logical steps, each justified by axioms, definitions, or previously established results, that establishes the truth of a mathematical statement beyond doubt. This skill catalogs 13 proof techniques with canonical worked examples, strategy selection heuristics, and readability guidance.

**Agent affinity:** euclid (geometric and structural proofs), polya (strategy selection)

**Concept IDs:** math-equations-expressions, math-systems-polynomials, math-pattern-recognition

## The Proof Toolbox at a Glance

| # | Technique | Best for | Key signal |
|---|---|---|---|
| 1 | Direct proof | Default for implications | Can build Q from P step by step |
| 2 | Contrapositive | P is hard to use directly | neg-Q gives a more concrete hypothesis |
| 3 | Contradiction | Non-existence, irrationality, infinity | Negation yields a concrete object that self-destructs |
| 4 | Cases | Natural partition of hypotheses | Parity, sign, size, set membership |
| 5 | WLOG | Symmetric variables | Cases would repeat the same argument |
| 6 | Vacuous/Trivial | Empty-set or always-true conclusions | Antecedent is false or consequent is always true |
| 7 | Biconditional | "If and only if" statements | Must prove both directions |
| 8 | Counterexample | Disproving universal claims | One witness to failure suffices |
| 9 | Existence | "There exists" statements | Constructive (exhibit) or non-constructive (probabilistic/LEM) |
| 10 | Uniqueness | "There exists exactly one" | Assume two, show equal |
| 11 | Induction | Claims over N or recursive structures | Weak, strong, or structural depending on domain |
| 12 | Pigeonhole / Double counting | Combinatorial existence, identities | More objects than containers; count the same set two ways |
| 13 | Diagonal / Invariants | Uncountability, impossibility | Construct a witness that differs from every listed element; find a preserved quantity |

## Technique 1 — Direct Proof

**Pattern:** To prove P implies Q, assume P and derive Q.

**Logical basis:** Implication introduction. This is the default technique and should be attempted first for any implication.

**Worked example.** *If n is an even integer, then n-squared is even.*

**Proof.** Let n be an even integer. Then n = 2k for some integer k. We compute n^2 = (2k)^2 = 4k^2 = 2(2k^2). Since 2k^2 is an integer, n^2 = 2m where m = 2k^2, so n^2 is even.

**When to use.** Always try direct proof first. Most theorems in undergraduate courses yield to direct proof. Only switch techniques when the direct path stalls — typically when the hypothesis P does not provide enough structure to build toward Q.

**When it stalls.** You cannot find a way to use P to construct Q. This often signals that the natural reasoning direction is from neg-Q to neg-P (contrapositive), or that assuming neg-Q produces an immediate contradiction.

## Technique 2 — Proof by Contrapositive

**Pattern:** To prove P implies Q, prove the logically equivalent statement: neg-Q implies neg-P.

**Logical basis:** Contraposition equivalence. P => Q is equivalent to (not Q) => (not P). The proof mechanism after forming the contrapositive is direct proof.

**Worked example.** *If n^2 is even, then n is even.*

*Why direct proof stalls:* Assuming n^2 = 2k, we need to extract n = 2m, but taking square roots of integers is not a direct algebraic operation.

*Contrapositive:* If n is odd, then n^2 is odd.

**Proof.** Suppose n is odd. Then n = 2k + 1 for some integer k. We compute n^2 = (2k + 1)^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1. Since 2k^2 + 2k is an integer, n^2 is odd. The contrapositive holds, so the original implication holds.

**When to use.** When neg-Q gives a more concrete, manipulable hypothesis than P. In this example, "n is odd" lets you write n = 2k + 1 and compute directly; "n^2 is even" leaves you fighting the square root.

## Technique 3 — Proof by Contradiction (Reductio ad Absurdum)

**Pattern:** To prove P, assume neg-P and derive a contradiction.

**Logical basis:** (neg-P => contradiction) implies P. This is classically valid. In intuitionistic logic, it gives only neg-neg-P; the jump to P requires the law of excluded middle.

**Worked example.** *The square root of 2 is irrational.*

**Proof.** Suppose for contradiction that sqrt(2) is rational. Then sqrt(2) = p/q where p, q are integers, q is nonzero, and gcd(p, q) = 1. Squaring: 2 = p^2/q^2, so p^2 = 2q^2. Thus p^2 is even, so p is even (by Technique 2). Write p = 2r. Then 4r^2 = 2q^2, so q^2 = 2r^2, meaning q is even. But then both p and q are even, contradicting gcd(p, q) = 1. Therefore sqrt(2) is irrational.

**When to use.** When the negation of the conclusion gives you a concrete object to reason about, and that object collides with known facts. Especially useful for:

- **Non-existence claims:** "There is no x such that P(x)" — assume such x exists, derive contradiction.
- **Infinity arguments:** "There are infinitely many primes" — assume finitely many, construct a new one (Euclid).
- **Irrationality:** Assume rational form, derive coprimality contradiction (as above).

**When NOT to use.** Do not reach for contradiction when a direct proof or contrapositive works cleanly. Unnecessary contradiction proofs obscure the logical structure and make verification harder.

## Technique 4 — Proof by Cases

**Pattern:** To prove P, partition the hypothesis space into cases C_1, C_2, ..., C_n that exhaust all possibilities, and prove P separately in each case.

**Logical basis:** Disjunction elimination.

**Worked example.** *For any integer n, n^2 + n is even.*

**Proof.** Let n be an integer. We consider two cases.

*Case 1: n is even.* Then n = 2k. So n^2 + n = 4k^2 + 2k = 2(2k^2 + k), which is even.

*Case 2: n is odd.* Then n = 2k + 1. So n^2 + n = (2k+1)^2 + (2k+1) = 4k^2 + 4k + 1 + 2k + 1 = 4k^2 + 6k + 2 = 2(2k^2 + 3k + 1), which is even.

In both cases, n^2 + n is even.

**When to use.** When the hypothesis or object has a natural partition: parity (even/odd), sign (positive/zero/negative), size comparisons, set membership (x in S vs x not in S).

**Common mistake.** Forgetting to cover a case. Splitting into "x > 0" and "x < 0" without addressing x = 0 invalidates the proof.

## Technique 5 — Without Loss of Generality (WLOG)

**Pattern:** When multiple symmetric cases would require identical arguments, argue one case and assert the others follow by symmetry.

**Worked example.** *For any real numbers x and y, |x - y| >= ||x| - |y||.*

**Proof.** Without loss of generality, assume |x| >= |y|. (If |y| > |x|, swap x and y; the inequality is symmetric.) Then ||x| - |y|| = |x| - |y|. By the triangle inequality: |x| = |(x - y) + y| <= |x - y| + |y|. So |x| - |y| <= |x - y|, which is the desired result.

**Critical discipline.** WLOG is only valid when cases are genuinely interchangeable. Asserting "WLOG x > 0" when the argument for x < 0 would differ is a logical error. Whenever you write WLOG, verify that the full proof reconstructs by substitution alone.

## Technique 6 — Vacuous and Trivial Proofs

**Vacuous proof pattern:** To prove P => Q, show that P is false. The implication holds vacuously because an implication with a false antecedent is true.

**Example.** *For every x in the empty set, x is positive.* There are no elements, so the statement holds vacuously.

**Trivial proof pattern:** To prove P => Q, show that Q is true regardless of P.

**Example.** *For every real number x, if x >= 0, then x^2 + 1 > 0.* Since x^2 >= 0 for all real x, we have x^2 + 1 >= 1 > 0 independently of the hypothesis. The implication holds trivially.

**When to use.** Rarely as primary techniques. More commonly they appear as observations within larger proofs — "this case is vacuous because the set is empty" or "the inequality holds trivially since both sides are positive."

## Technique 7 — Biconditional Proof

**Pattern:** To prove P if and only if Q, prove both P => Q and Q => P.

**Worked example.** *An integer n is even if and only if n^2 is even.*

**Proof.** (=>) If n is even, then n^2 is even. (Direct proof, Technique 1.)
(<=) If n^2 is even, then n is even. (Contrapositive proof, Technique 2.)
Both directions hold, so n is even iff n^2 is even.

**When to use.** Whenever a theorem is stated as "if and only if," "necessary and sufficient," or involves set equality (A = B is proved via A subset-of B and B subset-of A).

**Chain form.** For equivalences among three or more statements (P iff Q iff R), it suffices to prove P => Q => R => P rather than all pairwise implications. This saves work when the chain is natural.

## Technique 8 — Counterexample (Disproof)

**Pattern:** To disprove a universal statement "for all x, P(x)," exhibit a single x where P(x) fails.

**Logical basis:** neg(forall x, P(x)) is equivalent to exists x, neg-P(x).

**Worked example.** *Not every continuous function is differentiable.*

**Proof.** The function f(x) = |x| is continuous everywhere. At x = 0, the left-hand derivative is -1 and the right-hand derivative is +1, so f'(0) does not exist. Therefore not every continuous function is differentiable.

**When to use.** When you suspect a universal claim is false. One good counterexample settles it. Professional mathematicians alternate between trying to prove and trying to disprove, following whichever yields first.

**Counterexample quality.** The simplest counterexample is the best. An elaborate counterexample may be correct but harder to verify. Prefer small numbers, simple functions, and well-known objects.

## Technique 9 — Existence Proofs

### 9a — Constructive Existence

**Pattern:** To prove "there exists x with P(x)," produce a specific x and verify P(x).

**Worked example.** *For any odd integer n, there exist integers r, s with r^2 - s^2 = n.*

**Proof.** Let n = 2k + 1. Set r = k + 1, s = k. Then r^2 - s^2 = (k+1)^2 - k^2 = 2k + 1 = n.

**When to use.** Default for existence claims. Try constructive proof first.

### 9b — Non-Constructive Existence

**Pattern:** Argue that the negation (no x satisfies P) leads to a contradiction, without producing a specific x.

**Worked example.** *There exist irrational numbers a, b such that a^b is rational.*

**Proof.** Consider sqrt(2)^sqrt(2). Either it is rational or irrational.

*Case 1:* It is rational. Set a = b = sqrt(2). Both are irrational, and a^b is rational.

*Case 2:* It is irrational. Set a = sqrt(2)^sqrt(2), b = sqrt(2). Then a^b = (sqrt(2)^sqrt(2))^sqrt(2) = sqrt(2)^2 = 2, which is rational.

In either case, such a and b exist. (The proof never reveals which case holds. By the Gelfond-Schneider theorem, Case 2 is the actual one.)

**When to use.** When constructive approaches fail and a clever case split using the law of excluded middle establishes existence without explicit witnesses. This is characteristically classical reasoning.

## Technique 10 — Uniqueness Proofs

**Pattern:** To prove at most one x satisfies P(x), assume x_1 and x_2 both satisfy P, and show x_1 = x_2.

**Worked example.** *The equation ax = b, where a is nonzero, has at most one solution in R.*

**Proof.** Suppose x_1 and x_2 are both solutions. Then ax_1 = b and ax_2 = b, so ax_1 = ax_2. Since a is nonzero, divide: x_1 = x_2. The solution is unique.

**Existence + Uniqueness.** A "there exists a unique x" claim requires two separate proofs: existence (Technique 9) and uniqueness (this technique). The notation "exists-unique x, P(x)" abbreviates this conjunction.

## Technique 11 — Induction

### 11a — Weak (Mathematical) Induction

**Pattern:** To prove P(n) for all natural numbers n >= n_0: (1) prove the base case P(n_0), (2) prove that P(k) implies P(k+1).

**Worked example.** *For all n >= 1, 1 + 2 + ... + n = n(n+1)/2.*

**Proof.** Base case (n = 1): 1 = 1(2)/2 = 1. Holds.

Inductive step: Assume 1 + 2 + ... + k = k(k+1)/2. Then:
1 + 2 + ... + k + (k+1) = k(k+1)/2 + (k+1) = (k(k+1) + 2(k+1))/2 = (k+1)(k+2)/2.

By induction, the formula holds for all n >= 1.

**Critical discipline.** The inductive hypothesis is P(k), which you may assume freely. The inductive goal is P(k+1), which you must derive. Conflating these is the most common student error.

### 11b — Strong (Complete) Induction

**Pattern:** Assume P(n_0), P(n_0 + 1), ..., P(k) all hold, and prove P(k+1).

**Worked example.** *Every integer n >= 2 has a prime factorization.*

**Proof.** Base case (n = 2): 2 is prime, so 2 = 2 is its factorization.

Inductive step: Assume every m with 2 <= m <= k has a prime factorization. If k+1 is prime, it is its own factorization. If k+1 is composite, k+1 = ab with 2 <= a, b <= k. By the inductive hypothesis, both a and b have prime factorizations. Their product gives a prime factorization of k+1.

**When to use strong vs. weak.** When the step from k to k+1 requires not just P(k) but possibly P(j) for some j < k that you cannot predict in advance.

### 11c — Structural Induction

**Pattern:** For recursively defined structures (trees, lists, formulas), prove the property for base constructors and then for each recursive constructor assuming it holds for sub-components.

**Worked example.** *Every propositional formula has equal numbers of left and right parentheses.*

**Proof.** Base: A variable p has 0 left and 0 right parentheses. Equal.

Binary connective step: If phi has L(phi) = R(phi) and psi has L(psi) = R(psi), then (phi /\ psi) has L(phi) + L(psi) + 1 left and R(phi) + R(psi) + 1 right. Equal.

Negation step: (neg phi) adds one left and one right. Equal.

By structural induction, the property holds for all formulas.

**When to use.** Whenever the domain is inductively generated — abstract syntax trees, formal languages, recursive data types, Peano naturals themselves.

## Technique 12 — Pigeonhole Principle and Double Counting

### 12a — Pigeonhole

**Statement:** If n+1 objects are placed in n boxes, at least one box contains at least 2 objects. Generalized: kn+1 objects in n boxes forces at least k+1 in some box.

**Worked example.** *Among any n+1 integers chosen from {1, 2, ..., 2n}, two of them are such that one divides the other.*

**Proof.** Write each chosen integer as 2^a * q where q is odd. The odd parts q lie in {1, 3, 5, ..., 2n-1}, which has n elements. By pigeonhole, among the n+1 chosen integers, two share the same odd part q. If they are 2^a * q and 2^b * q with a < b, then the first divides the second.

### 12b — Double Counting

**Pattern:** Count the same set in two different ways; the counts must be equal.

**Worked example.** *C(n,k) = C(n, n-k).*

**Combinatorial proof.** C(n,k) counts ways to choose k elements from n. C(n, n-k) counts ways to choose n-k elements to leave out. Each inclusion corresponds to exactly one exclusion. The counts are equal.

**When to use pigeonhole.** When a problem asks "must there exist..." with bounds. **When to use double counting.** For combinatorial identities where two natural counting interpretations exist.

## Technique 13 — Diagonal Arguments and Invariants

### 13a — Cantor's Diagonal Argument

**Pattern:** To show a set S cannot be indexed by a set T, assume a surjection T -> S exists and construct an element of S that differs from every element in the range.

**Worked example.** *The real numbers in (0,1) are uncountable.*

**Proof.** Suppose f: N -> (0,1) is a bijection. Write f(n) in decimal as 0.d_{n,1} d_{n,2} d_{n,3}... Define r = 0.r_1 r_2 r_3... where r_n = 5 if d_{n,n} != 5, and r_n = 6 if d_{n,n} = 5. Then r is in (0,1) but r != f(n) for any n (they differ at position n). So f is not surjective — contradiction. Therefore (0,1) is uncountable.

**Reach:** Cantor's argument generalizes to Cantor's theorem (|S| < |P(S)|), Russell's paradox, the halting problem (Turing, 1936), and Godel's first incompleteness theorem (1931).

### 13b — Invariant Arguments

**Pattern:** To show a system cannot reach a target state, find a quantity preserved by every allowed move that differs between initial and target states.

**Worked example.** *An 8x8 chessboard with two diagonally opposite corners removed cannot be tiled by dominoes.*

**Proof.** Color the board in the standard checkerboard pattern. Each domino covers one black and one white square, so any tiling covers equal numbers of each color. The two removed corners are the same color (say white), leaving 32 black and 30 white squares. Equal coverage is impossible, so no tiling exists.

**When to use.** Impossibility proofs in games, puzzles, and combinatorial processes. Common invariants: parity, sums modulo n, colorings, algebraic expressions.

## Proof Readability

A correct proof that nobody can follow is a failed proof. Readability is not cosmetic — it is structural.

### The Knuth/Larrabee/Roberts Standard

Knuth, Larrabee, and Roberts (1989, "Mathematical Writing") established that a proof should read as correct English prose. Every symbol should be embedded in a sentence. The reader should never have to decode a wall of symbols.

**Bad:** "n = 2k. n^2 = 4k^2 = 2(2k^2). QED."

**Good:** "Since n is even, we may write n = 2k for some integer k. Then n^2 = (2k)^2 = 4k^2 = 2(2k^2). Because 2k^2 is an integer, this shows n^2 is even."

### The "Mugga Mugga" Test

A proof should be audible. If you replace every symbol with "mugga," can you still detect the logical flow? If not, the connective tissue between formulas is missing.

**Fails mugga test:** "Let mugga. mugga = mugga. mugga mugga. QED."

**Passes mugga test:** "Since mugga is mugga, we may write mugga equals mugga for some mugga. Then mugga equals mugga, which shows mugga is mugga."

### Practical Guidelines

1. **State what you will prove** before proving it. "We show that P(k+1) holds."
2. **Announce the technique.** "We proceed by contradiction." "We prove the contrapositive."
3. **Name your objects.** "Let epsilon > 0 be given" not just "epsilon > 0."
4. **Flag the key insight.** "The crucial observation is that..."
5. **Conclude explicitly.** "Therefore P holds" or "This completes the inductive step."

## Strategy Selection Heuristics

When approaching an unfamiliar problem, use this decision tree:

1. **Is it an implication (P => Q)?** Try direct proof. If stuck, try contrapositive. If both stall, try contradiction.
2. **Is it a universal statement (for all x, P(x))?** If over N, try induction. If you doubt it, try counterexample.
3. **Is it an existence statement (exists x, P(x))?** Try constructive. If too hard, try non-constructive.
4. **Does the hypothesis split naturally?** Use cases.
5. **Are variables symmetric?** Use WLOG.
6. **Is it "if and only if"?** Prove both directions.
7. **Is it an impossibility?** Look for an invariant.
8. **Does it involve counting or combinatorics?** Try pigeonhole or double counting.
9. **Does it involve "too many" or uncountability?** Try a diagonal argument.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Assuming what you need to prove | Circular reasoning | Clearly separate hypothesis from conclusion |
| "Proof by example" for universal claims | One example does not prove "for all" | Use induction, direct proof, or another valid technique |
| Incomplete case analysis | Missing cases invalidate the proof | Verify cases exhaust all possibilities |
| Invalid WLOG | Claimed symmetry does not exist | Verify interchangeability explicitly |
| Confusing inductive hypothesis and goal | Deriving P(k) instead of P(k+1) | Label clearly: "Assume P(k). We show P(k+1)." |
| Unnecessary contradiction | Obscures structure | Use direct proof or contrapositive when possible |
| Missing quantifiers | Ambiguous scope | Every variable needs "for all" or "there exists" |

## Cross-References

- **euclid agent:** Geometric proof construction and axiomatic reasoning. Primary agent for proof verification tasks.
- **polya agent:** Strategy selection via Polya's "How to Solve It" framework — understand, plan, carry out, look back.
- **ramanujan agent:** Pattern recognition that generates conjectures requiring proof.
- **algebraic-reasoning skill:** Algebraic manipulation techniques used within proofs.
- **geometric-intuition skill:** Geometric proof techniques (congruence, similarity, coordinate methods).
- **pattern-recognition skill:** Conjecture generation that feeds into proof obligations.

## References

- Hammack, R. (2018). *Book of Proof*. 3rd edition. Virginia Commonwealth University. (Open access.)
- Velleman, D. J. (2019). *How to Prove It*. 3rd edition. Cambridge University Press.
- Polya, G. (1945). *How to Solve It*. Princeton University Press.
- Knuth, D. E., Larrabee, T., & Roberts, P. M. (1989). *Mathematical Writing*. MAA Notes.
- Schwarz, E. Proof writing lecture deck (slides 15-47, 108-115, 119). Course materials.
- Cantor, G. (1891). "Ueber eine elementare Frage der Mannigfaltigkeitslehre." *Jahresbericht der DMV*, 1, 75-78.
- Erdos, P. (1947). "Some remarks on the theory of graphs." *Bulletin of the AMS*, 53, 292-294.
