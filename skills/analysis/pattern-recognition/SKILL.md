---
name: pattern-recognition
description: Conjecture generation, sequence analysis, and experimental mathematics for mathematical discovery. Covers sequence analysis (OEIS lookups, recurrence relations, generating functions), pattern detection methods (finite differences, ratio analysis, modular patterns), conjecture generation workflow, classical integer sequences (Fibonacci, Catalan, partition numbers, Bernoulli numbers), combinatorial identities, the probabilistic method (Erdos, expected value arguments, Lovasz Local Lemma), AI-assisted discovery (FunSearch, Ramanujan Machine), and confidence calibration with cautionary tales (Mertens conjecture, Polya conjecture). Use when discovering patterns, analyzing sequences, generating conjectures, or working with combinatorial identities.
type: skill
category: math
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/math/pattern-recognition/SKILL.md
superseded_by: null
---
# Pattern Recognition

Mathematics advances by the interplay of conjecture and proof. Pattern recognition — the art of observing regularity in data and formulating precise conjectures — is the creative engine that drives discovery. Euler, Gauss, and Ramanujan were supreme pattern-finders whose conjectures shaped centuries of subsequent mathematics. This skill covers systematic methods for detecting patterns, generating conjectures, and calibrating confidence before committing to a proof attempt.

**Agent affinity:** ramanujan (intuitive pattern discovery, sequence analysis, identity generation)

**Concept IDs:** math-pattern-recognition, math-experimental-probability, math-data-representation, math-functions

## Part I — Sequence Analysis

### The OEIS (On-Line Encyclopedia of Integer Sequences)

The OEIS (oeis.org), founded by Neil Sloane in 1964 and now containing over 370,000 sequences, is the single most important resource for pattern recognition in mathematics. Given the first several terms of a sequence, searching the OEIS often identifies the sequence, its name, its generating function, known formulas, and references.

**Strategy.** When encountering an unfamiliar sequence:
1. Compute at least 6-8 terms.
2. Search the OEIS by the terms.
3. If no match, compute the sequence of first differences, second differences, or ratios and search those.
4. If still no match, try looking at the sequence modulo small primes.

### Recurrence Relations

A recurrence relation defines each term as a function of previous terms.

**Linear recurrences with constant coefficients.** The general form a_n = c_1 * a_{n-1} + c_2 * a_{n-2} + ... + c_k * a_{n-k} has solutions determined by the roots of the characteristic polynomial x^k - c_1 * x^{k-1} - ... - c_k = 0.

**Worked example.** *Find a closed form for the Fibonacci sequence: F_n = F_{n-1} + F_{n-2}, F_0 = 0, F_1 = 1.*

Characteristic equation: x^2 - x - 1 = 0. Roots: phi = (1 + sqrt(5))/2 and psi = (1 - sqrt(5))/2.

General solution: F_n = A * phi^n + B * psi^n. From F_0 = 0: A + B = 0. From F_1 = 1: A*phi + B*psi = 1. Solving: A = 1/sqrt(5), B = -1/sqrt(5).

Closed form (Binet's formula): F_n = (phi^n - psi^n) / sqrt(5).

Since |psi| < 1, for large n, F_n is approximately phi^n / sqrt(5), and F_n is always the nearest integer to phi^n / sqrt(5).

### Generating Functions

A generating function encodes a sequence {a_n} as the coefficients of a formal power series:

A(x) = sum_{n=0}^{infinity} a_n * x^n (ordinary generating function)
A(x) = sum_{n=0}^{infinity} a_n * x^n / n! (exponential generating function)

**Why they matter.** Algebraic operations on generating functions correspond to operations on sequences: multiplication corresponds to convolution, differentiation to index-shifting, and composition to certain substitution operations. Many sequence identities that are hard to prove combinatorially become routine algebra on generating functions.

**Worked example.** *Find the generating function for the Fibonacci sequence.*

From F_n = F_{n-1} + F_{n-2}: multiply by x^n and sum over n >= 2.

sum_{n>=2} F_n x^n = sum_{n>=2} F_{n-1} x^n + sum_{n>=2} F_{n-2} x^n

F(x) - F_0 - F_1 x = x(F(x) - F_0) + x^2 F(x)

F(x) - x = xF(x) + x^2 F(x)

F(x)(1 - x - x^2) = x

F(x) = x / (1 - x - x^2)

Partial fraction decomposition recovers Binet's formula.

## Part II — Pattern Detection Methods

### Finite Differences

The first difference of a sequence {a_n} is Delta(a_n) = a_{n+1} - a_n. Higher differences are defined recursively.

**Key insight.** If the k-th differences are constant, the sequence is a polynomial of degree k.

| Sequence type | 1st diff | 2nd diff | 3rd diff |
|---|---|---|---|
| Linear (an + b) | Constant | Zero | Zero |
| Quadratic (an^2 + bn + c) | Linear | Constant | Zero |
| Cubic | Quadratic | Linear | Constant |

**Worked example.** *Identify the pattern: 1, 5, 14, 30, 55, 91, ...*

First differences: 4, 9, 16, 25, 36 (perfect squares!)
Second differences: 5, 7, 9, 11 (arithmetic)
Third differences: 2, 2, 2 (constant)

Third differences are constant, so the sequence is a cubic polynomial. The first differences being perfect squares suggests a_n = sum_{k=1}^{n} k^2 = n(n+1)(2n+1)/6.

Verify: a_1 = 1, a_2 = 5, a_3 = 14, a_4 = 30, a_5 = 55, a_6 = 91. Confirmed.

### Ratio Analysis

Compute successive ratios a_{n+1}/a_n. Convergence to a constant L suggests geometric growth (a_n is approximately C * L^n). Convergence to 1 from above suggests polynomial growth.

**Worked example.** *For 1, 1, 2, 3, 5, 8, 13, 21, ..., compute ratios: 1, 2, 1.5, 1.667, 1.6, 1.625, 1.615...*

The ratios converge to phi = (1 + sqrt(5))/2 approximately 1.618, confirming Fibonacci-like exponential growth at rate phi.

### Modular Patterns

Reduce a sequence modulo small numbers to reveal periodic structure.

**Worked example.** *Fibonacci numbers mod 3: 0, 1, 1, 2, 0, 2, 2, 1, 0, 1, 1, 2, ...*

The sequence is periodic with period 8. This is the Pisano period pi(3) = 8. Every Fibonacci sequence mod m is periodic (a theorem), and the Pisano periods themselves form a fascinating sequence (OEIS A001175).

## Part III — Conjecture Generation Workflow

The process from observation to theorem follows a structured workflow:

### Step 1: Gather Data

Compute many examples. For sequence problems, compute at least 10-15 terms. For structural problems (graphs, groups, partitions), enumerate small cases completely.

### Step 2: Look for Patterns

Apply the detection methods above: differences, ratios, modular reduction, OEIS lookup. Also look for:
- **Symmetry:** Is a_n = a_{N-n} for some N?
- **Monotonicity:** Is the sequence always increasing/decreasing?
- **Divisibility:** Do certain primes always divide certain terms?
- **Recurrence:** Can each term be expressed in terms of earlier terms?

### Step 3: Formulate a Precise Conjecture

A conjecture must be a precise mathematical statement, not a vague observation. "The sequence seems to grow" is not a conjecture. "a_n = 2^n - 1 for all n >= 1" is a conjecture.

### Step 4: Test the Conjecture

Verify the conjecture on data not used in its formation. If the conjecture predicts the next 5-10 terms correctly, confidence increases. If any prediction fails, revise.

### Step 5: Attempt a Proof

If the conjecture survives testing, attempt a proof using the techniques from the proof-techniques skill. Common approaches: induction for sequences indexed by N, combinatorial arguments for identity conjectures, generating function methods for recurrence conjectures.

### Step 6: Calibrate Confidence

See the cautionary tales section below. Even extensive numerical evidence can be misleading.

## Part IV — Classical Integer Sequences

### Fibonacci Numbers (A000045)

F_0 = 0, F_1 = 1, F_n = F_{n-1} + F_{n-2}. Closed form: Binet's formula (above).

Key properties: gcd(F_m, F_n) = F_{gcd(m,n)}. F_n divides F_{mn}. sum_{k=0}^{n} F_k = F_{n+2} - 1.

Appearance: rabbit populations (the original Fibonacci problem, Liber Abaci, 1202), phyllotaxis in plants, tilings of 2xn boards, Zeckendorf representation.

### Catalan Numbers (A000108)

C_n = (2n choose n) / (n + 1) = 1, 1, 2, 5, 14, 42, 132, 429, ...

The Catalan numbers count an astonishing variety of combinatorial objects:
- Balanced parentheses strings with n pairs
- Full binary trees with n + 1 leaves
- Triangulations of a convex (n + 2)-gon
- Monotonic lattice paths from (0,0) to (n,n) that stay below the diagonal
- Non-crossing partitions of {1, ..., n}

Generating function: C(x) = (1 - sqrt(1 - 4x)) / (2x).

Recurrence: C_0 = 1, C_{n+1} = sum_{k=0}^{n} C_k * C_{n-k}.

### Partition Numbers (A000041)

p(n) = number of ways to write n as a sum of positive integers (order doesn't matter). p(0) = 1, p(1) = 1, p(2) = 2, p(3) = 3, p(4) = 5, p(5) = 7, ...

Ramanujan discovered stunning congruences: p(5n + 4) = 0 mod 5, p(7n + 5) = 0 mod 7, p(11n + 6) = 0 mod 11. These congruences, initially discovered by pattern recognition on computed values, were later proved using modular forms.

Hardy-Ramanujan asymptotic formula (1918): p(n) ~ (1/(4n*sqrt(3))) * exp(pi * sqrt(2n/3)) as n -> infinity.

### Bernoulli Numbers (A027642)

B_0 = 1, B_1 = -1/2, B_2 = 1/6, B_3 = 0, B_4 = -1/30, ...

Key role: sum_{k=1}^{n} k^m = (1/(m+1)) * sum_{j=0}^{m} (m+1 choose j) * B_j * n^{m+1-j}. This is Faulhaber's formula, connecting Bernoulli numbers to power sums. Bernoulli numbers also appear in the Taylor series of x/(e^x - 1), the Euler-Maclaurin formula, and the values of the Riemann zeta function at negative integers.

## Part V — Combinatorial Identities

### The Vandermonde Identity

sum_{k=0}^{r} (m choose k)(n choose r-k) = (m+n choose r)

**Combinatorial proof.** Choose r elements from a set of m + n elements by choosing k from the first m and r - k from the remaining n, then sum over all valid k.

### The Hockey Stick Identity

sum_{i=0}^{r} (n+i choose n) = (n+r+1 choose n+1)

The name comes from the shape of the entries in Pascal's triangle when this sum is visualized.

### Binomial Theorem

(a + b)^n = sum_{k=0}^{n} (n choose k) * a^{n-k} * b^k

Setting a = b = 1: sum (n choose k) = 2^n. Setting a = 1, b = -1: sum (-1)^k (n choose k) = 0.

### Discovering New Identities

When a combinatorial identity is suspected:
1. Verify numerically for small cases.
2. Try to find a combinatorial proof (count the same set two ways).
3. Try generating function methods (algebraic proof).
4. Try Zeilberger's algorithm (computer-aided proof of hypergeometric identities).

Wilf-Zeilberger theory (1990s) provides algorithms that can automatically prove or disprove a wide class of combinatorial identities. Petkovsek, Wilf, and Zeilberger's *A = B* (1996) is the definitive reference.

## Part VI — The Probabilistic Method

### Expected Value Arguments

The simplest probabilistic method: if the expected value of a random variable X is mu, then there exists an outcome where X >= mu and an outcome where X <= mu.

**Worked example.** *Every tournament on n vertices has a Hamiltonian path.*

**Proof.** A tournament is a complete directed graph. Consider a random permutation sigma of the vertices. For each consecutive pair (sigma(i), sigma(i+1)), the probability that the edge goes from sigma(i) to sigma(i+1) is 1/2 (by symmetry). The expected number of "forward" edges is (n-1)/2. Since the total number of consecutive pairs is n-1, there exists a permutation with at least (n-1)/2 forward edges. (This doesn't complete the Hamiltonian path proof directly, but the probabilistic lens motivates the approach.)

### The Erdos Probabilistic Method

Paul Erdos (1913-1996) created the probabilistic method as a systematic tool for combinatorics. His 1947 paper on Ramsey numbers was the landmark:

**Theorem (Erdos, 1947).** R(k, k) > 2^{k/2} for k >= 3.

**Proof sketch.** Color each edge of K_n (n = floor(2^{k/2})) randomly red or blue with probability 1/2. For any set S of k vertices, the probability that S forms a monochromatic K_k is 2 * (1/2)^{C(k,2)} = 2^{1-C(k,2)}. The expected number of monochromatic K_k subgraphs is C(n,k) * 2^{1-C(k,2)}. For n = floor(2^{k/2}), this expected count is less than 1, so there exists a coloring with no monochromatic K_k.

### The Lovasz Local Lemma (Introduction)

The Local Lemma (Erdos and Lovasz, 1975) handles situations where events are not independent but each event depends on only a few others.

**Symmetric form.** If each event has probability at most p, each event is independent of all but at most d other events, and e*p*(d+1) <= 1, then with positive probability none of the events occur.

This is dramatically stronger than a union bound when d is small relative to the number of events. It has applications in graph coloring, satisfiability, and combinatorial geometry.

## Part VII — AI-Assisted Mathematical Discovery

### FunSearch (2023)

DeepMind's FunSearch (Romera-Paredes et al., 2023) uses large language models to search for mathematical functions that optimize specific objectives. Applied to the cap set problem (finding large subsets of Z_3^n with no three-term arithmetic progressions), FunSearch discovered constructions beating all previously known results for certain dimensions.

The paradigm: LLMs generate candidate functions, an evaluator scores them, the best are used to prompt further generation. This is not proof but discovery — the constructions must still be verified.

### The Ramanujan Machine (2019)

The Ramanujan Machine (Raayoni et al., 2019, Technion) is an algorithmic framework for discovering new formulas for mathematical constants. It uses pattern-matching algorithms (MITM-RF, Conservative Matrix Field) to generate continued fraction representations of pi, e, and the Catalan constant.

Example discovery: a new continued fraction for 4/pi that was not previously in the literature, later proved correct.

### Confidence Calibration

AI-discovered patterns require rigorous verification. The LLM is an oracle for conjectures, not proofs. Every AI-generated conjecture must be subjected to the same proof-or-disproof workflow as any human conjecture.

## Part VIII — Cautionary Tales

### The Mertens Conjecture (1897-1985)

Mertens conjectured that |M(n)| < sqrt(n) for all n, where M(n) = sum_{k=1}^{n} mu(k) is the Mertens function. This was verified computationally for all n up to 10^8. In 1985, Odlyzko and te Riele proved the conjecture FALSE — but the first counterexample exceeds 10^30. Numerical evidence was compelling yet misleading.

**Lesson.** Computational verification, no matter how extensive, is not proof. A statement can hold for all tested values and still be false.

### The Polya Conjecture (1919-1958)

Polya conjectured that for most integers, the number of prime factors (counted with multiplicity) is odd — formally, that L(n) = sum_{k=1}^{n} lambda(k) <= 0 for all n >= 2. This holds for all n up to 906,150,257. The first counterexample was found by Haselgrove in 1958 using analytic methods.

### Borwein's Integral (A Beautiful Trap)

Consider the sequence of integrals:
- integral_0^inf sinc(x) dx = pi/2
- integral_0^inf sinc(x) sinc(x/3) dx = pi/2
- integral_0^inf sinc(x) sinc(x/3) sinc(x/5) dx = pi/2
- ...continuing with odd denominators...

The pattern gives pi/2 for the first SEVEN terms. The eighth integral is strictly less than pi/2 (by approximately 4.6 * 10^{-11}). This was discovered by David and Jonathan Borwein and is a famous example of a "pattern" that breaks precisely when intuition says it shouldn't.

**Lesson.** Seven data points (or seventy, or seven thousand) are not proof.

## When to Use This Skill

- Analyzing an unfamiliar sequence or pattern
- Generating mathematical conjectures from data
- Working with combinatorial identities or integer sequences
- Applying the probabilistic method in combinatorics
- Evaluating confidence in observed patterns

## When NOT to Use This Skill

- For proving a conjecture once formulated — use proof-techniques
- For algebraic manipulation — use algebraic-reasoning
- For calculus computations — use numerical-analysis
- For real-world data modeling — use mathematical-modeling

## Cross-References

- **ramanujan agent:** Intuitive pattern discovery, sequence analysis, and identity generation. Named for Srinivasa Ramanujan (1887-1920), whose notebooks contain thousands of formulas discovered through extraordinary pattern recognition, many still being proved today.
- **euler agent:** Generating functions, analytic combinatorics, and connections between sequences and analysis.
- **proof-techniques skill:** Converting conjectures into theorems. Pattern recognition generates the "what"; proof-techniques provides the "why."
- **algebraic-reasoning skill:** Algebraic manipulation of generating functions and recurrence relations.
- **numerical-analysis skill:** Computational methods for verifying patterns and generating data.

## References

- Sloane, N. J. A. (2003). "The On-Line Encyclopedia of Integer Sequences." *Notices of the AMS*, 50(8), 912-915.
- Wilf, H. S. (2005). *Generatingfunctionology*. 3rd edition. AK Peters. (Free online.)
- Petkovsek, M., Wilf, H. S., & Zeilberger, D. (1996). *A = B*. AK Peters. (Free online.)
- Aigner, M., & Ziegler, G. M. (2018). *Proofs from THE BOOK*. 6th edition. Springer. (Probabilistic method chapter.)
- Erdos, P. (1947). "Some remarks on the theory of graphs." *Bulletin of the AMS*, 53, 292-294.
- Erdos, P., & Lovasz, L. (1975). "Problems and results on 3-chromatic hypergraphs." *Colloquia Mathematica Societatis Janos Bolyai*, 10, 609-627.
- Romera-Paredes, B., et al. (2023). "Mathematical discoveries from program search with large language models." *Nature*, 625, 468-475.
- Raayoni, G., et al. (2019). "Generating conjectures on fundamental constants with the Ramanujan Machine." *Nature*, 590, 67-73.
- Odlyzko, A. M., & te Riele, H. J. J. (1985). "Disproof of the Mertens conjecture." *Journal fur die reine und angewandte Mathematik*, 357, 138-160.
- Borwein, D., & Borwein, J. M. (2001). "Some remarkable properties of sinc and related integrals." *Ramanujan Journal*, 5, 73-89.
