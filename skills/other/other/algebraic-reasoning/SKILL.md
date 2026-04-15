---
name: algebraic-reasoning
description: Symbolic manipulation, equation solving, and algebraic structures for mathematical reasoning. Covers distributive law, factoring, completing the square, linear through polynomial equation solving, systems of equations (substitution, elimination, Gaussian elimination, matrix methods), algebraic structures (groups, rings, fields), modular arithmetic, polynomial theory, and inequalities. Use when solving equations, simplifying expressions, working with algebraic structures, or performing symbolic manipulation.
type: skill
category: math
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/math/algebraic-reasoning/SKILL.md
superseded_by: null
---
# Algebraic Reasoning

Algebra is the study of structure, relation, and quantity expressed through symbols and the rules for manipulating those symbols. It is the language in which most mathematics is written and the engine behind equation solving, function analysis, and abstract structure theory. This skill covers concrete manipulation techniques, equation-solving strategies, and the algebraic structures that underpin modern mathematics.

**Agent affinity:** gauss (systems, elimination, number theory), noether (abstract structures, ring/field theory)

**Concept IDs:** math-variables-unknowns, math-equations-expressions, math-systems-polynomials, math-pattern-recognition, math-fractions-ratios

## Part I — Symbolic Manipulation

### The Distributive Law and Its Consequences

The distributive law a(b + c) = ab + ac is the single most important algebraic identity. Nearly every manipulation technique — factoring, expanding, completing the square, polynomial long division — is an application of distributivity in one direction or the other.

**Expansion** applies the law left-to-right: 3(x + 4) = 3x + 12.

**Factoring** applies it right-to-left: 3x + 12 = 3(x + 4).

### Core Factoring Techniques

| Technique | Pattern | Example |
|---|---|---|
| Common factor | ab + ac = a(b + c) | 6x^2 + 9x = 3x(2x + 3) |
| Difference of squares | a^2 - b^2 = (a-b)(a+b) | x^2 - 25 = (x-5)(x+5) |
| Perfect square trinomial | a^2 +/- 2ab + b^2 = (a +/- b)^2 | x^2 + 6x + 9 = (x+3)^2 |
| Sum/difference of cubes | a^3 +/- b^3 = (a +/- b)(a^2 -/+ ab + b^2) | x^3 - 8 = (x-2)(x^2+2x+4) |
| Grouping | ab + ac + db + dc = (a+d)(b+c) | x^3 + x^2 + x + 1 = (x^2+1)(x+1) |
| Quadratic trinomial | ax^2 + bx + c | Factor by finding two numbers whose product is ac and sum is b |

### Completing the Square

Completing the square converts ax^2 + bx + c into vertex form a(x - h)^2 + k, revealing the parabola's vertex and providing a path to the quadratic formula.

**Worked example.** *Rewrite 2x^2 + 12x + 7 in vertex form.*

Step 1: Factor the leading coefficient from the first two terms.
2(x^2 + 6x) + 7

Step 2: Inside the parentheses, add and subtract (6/2)^2 = 9.
2(x^2 + 6x + 9 - 9) + 7

Step 3: Separate the perfect square and distribute.
2(x + 3)^2 - 18 + 7 = 2(x + 3)^2 - 11

The vertex is at (-3, -11) and the parabola opens upward.

### Deriving the Quadratic Formula

Completing the square on the general quadratic ax^2 + bx + c = 0 (with a != 0) yields the quadratic formula:

x = (-b +/- sqrt(b^2 - 4ac)) / (2a)

**Derivation.** Start with ax^2 + bx + c = 0. Divide by a: x^2 + (b/a)x + c/a = 0. Move the constant: x^2 + (b/a)x = -c/a. Complete the square: x^2 + (b/a)x + (b/(2a))^2 = -c/a + b^2/(4a^2). Factor the left side: (x + b/(2a))^2 = (b^2 - 4ac)/(4a^2). Take the square root: x + b/(2a) = +/- sqrt(b^2 - 4ac)/(2a). Solve for x.

The discriminant D = b^2 - 4ac determines the nature of the roots: D > 0 gives two distinct real roots, D = 0 gives one repeated real root, D < 0 gives two complex conjugate roots.

## Part II — Equation Solving

### Linear Equations

A linear equation in one variable has the form ax + b = 0 (a != 0), with solution x = -b/a.

**Strategy:** Isolate the variable through inverse operations. Add/subtract to move terms, multiply/divide to clear coefficients. Preserve the equality by performing the same operation on both sides.

### Quadratic Equations

Three methods in order of preference:

1. **Factoring** (when applicable): x^2 - 5x + 6 = 0 factors as (x-2)(x-3) = 0, giving x = 2 or x = 3.
2. **Completing the square** (always works): useful when the vertex form is also needed.
3. **Quadratic formula** (always works): the universal fallback.

**Worked example (factoring).** *Solve 6x^2 + x - 2 = 0.*

We seek two numbers whose product is 6(-2) = -12 and whose sum is 1. These are 4 and -3. Rewrite the middle term: 6x^2 + 4x - 3x - 2 = 0. Factor by grouping: 2x(3x + 2) - 1(3x + 2) = 0, so (2x - 1)(3x + 2) = 0. Therefore x = 1/2 or x = -2/3.

### Polynomial Equations (Degree >= 3)

**Rational Root Theorem.** If the polynomial p(x) = a_n x^n + ... + a_0 has a rational root p/q in lowest terms, then p divides a_0 and q divides a_n. This gives a finite list of candidates to test.

**Factor Theorem.** r is a root of p(x) if and only if (x - r) divides p(x).

**Strategy for cubics and quartics:**
1. List rational root candidates via the Rational Root Theorem.
2. Test candidates using synthetic division or direct substitution.
3. Once a root r is found, divide by (x - r) to reduce the degree.
4. Repeat until the remaining factor is quadratic, then use the quadratic formula.

**Worked example.** *Solve x^3 - 6x^2 + 11x - 6 = 0.*

Rational root candidates: +/-1, +/-2, +/-3, +/-6. Test x = 1: 1 - 6 + 11 - 6 = 0. Yes. Divide by (x - 1) via synthetic division to get x^2 - 5x + 6 = (x - 2)(x - 3). Solutions: x = 1, 2, 3.

## Part III — Systems of Equations

### Substitution

Solve one equation for one variable, substitute into the other.

**Worked example.** *Solve: x + y = 5 and 2x - y = 1.*

From equation 1: y = 5 - x. Substitute into equation 2: 2x - (5 - x) = 1, so 3x = 6, x = 2, y = 3.

### Elimination

Add or subtract multiples of equations to eliminate a variable.

**Worked example.** *Solve: 3x + 2y = 7 and 5x - 2y = 9.*

Add the equations: 8x = 16, so x = 2. Back-substitute: 6 + 2y = 7, y = 1/2.

### Gaussian Elimination

For larger systems, reduce the augmented matrix to row echelon form using three row operations: swap rows, multiply a row by a nonzero scalar, add a multiple of one row to another.

**Worked example.** *Solve: x + 2y + 3z = 9, 2x - y + z = 8, 3x + 0y - z = 3.*

Augmented matrix:
[1  2  3 | 9]
[2 -1  1 | 8]
[3  0 -1 | 3]

R2 <- R2 - 2*R1: [0 -5 -5 | -10]
R3 <- R3 - 3*R1: [0 -6 -10 | -24]

R2 <- R2 / (-5): [0 1 1 | 2]
R3 <- R3 + 6*R2: [0 0 -4 | -12]

R3 <- R3 / (-4): [0 0 1 | 3]

Back-substitute: z = 3, y + 3 = 2 so y = -1, x + 2(-1) + 3(3) = 9 so x = 2.

Solution: (x, y, z) = (2, -1, 3).

**Gauss-Jordan variation.** Continue to reduced row echelon form (RREF) so each pivot is 1 and all other entries in pivot columns are 0. This eliminates back-substitution.

### Matrix Methods

A system Ax = b has solution x = A^(-1)b when A is invertible. For 2x2 matrices, the inverse has a closed form. For larger systems, use Gaussian elimination to find A^(-1) or apply Cramer's rule (determinant-based, practical only for small systems).

**Cramer's Rule.** For an n x n system Ax = b where det(A) != 0, x_i = det(A_i) / det(A), where A_i is A with column i replaced by b.

## Part IV — Algebraic Structures

### Groups

A **group** (G, *) is a set G with a binary operation * satisfying:
1. **Closure:** a * b is in G for all a, b in G.
2. **Associativity:** (a * b) * c = a * (b * c).
3. **Identity:** There exists e in G such that a * e = e * a = a for all a.
4. **Inverses:** For each a in G, there exists a^(-1) such that a * a^(-1) = a^(-1) * a = e.

If additionally a * b = b * a for all a, b, the group is **abelian** (commutative).

**Examples.** (Z, +) is an abelian group with identity 0. The symmetric group S_n (all permutations of n elements under composition) is non-abelian for n >= 3.

### Rings

A **ring** (R, +, *) is a set with two operations where (R, +) is an abelian group, multiplication is associative, and multiplication distributes over addition. A ring with multiplicative identity 1 is a **ring with unity**. A ring where multiplication is commutative is a **commutative ring**.

**Example.** (Z, +, *) is a commutative ring with unity. The ring of n x n matrices over R is a ring with unity (the identity matrix) but is non-commutative for n >= 2.

### Fields

A **field** (F, +, *) is a commutative ring with unity where every nonzero element has a multiplicative inverse.

**Examples.** Q, R, and C are fields. Z is NOT a field (2 has no multiplicative inverse in Z). The integers modulo p (Z/pZ) form a field when p is prime.

**Why it matters for equation solving.** The quadratic formula works over any field of characteristic != 2. Gaussian elimination works over any field. Understanding when you're working in a field vs. a ring determines which algebraic manipulations are valid.

## Part V — Modular Arithmetic

Working modulo n means computing remainders upon division by n. Two integers a and b are congruent modulo n (written a = b mod n) if n divides (a - b).

**Arithmetic rules.** If a = b (mod n) and c = d (mod n), then:
- a + c = b + d (mod n)
- a * c = b * d (mod n)
- a - c = b - d (mod n)

Division requires care: a/c (mod n) exists only when gcd(c, n) = 1, in which case the modular inverse c^(-1) exists.

**Worked example.** *Compute 7^100 mod 11.*

By Fermat's Little Theorem, since 11 is prime and gcd(7, 11) = 1: 7^10 = 1 (mod 11). Therefore 7^100 = (7^10)^10 = 1^10 = 1 (mod 11).

**Fermat's Little Theorem.** If p is prime and gcd(a, p) = 1, then a^(p-1) = 1 (mod p).

**Euler's Theorem (generalization).** If gcd(a, n) = 1, then a^(phi(n)) = 1 (mod n), where phi(n) is Euler's totient function.

**The Chinese Remainder Theorem.** If gcd(m, n) = 1, then the system x = a (mod m), x = b (mod n) has a unique solution modulo mn. This decomposes modular problems into simpler components.

## Part VI — Polynomial Theory

### The Division Algorithm

For polynomials f(x) and g(x) with g != 0, there exist unique polynomials q(x) (quotient) and r(x) (remainder) such that f(x) = g(x) * q(x) + r(x) with deg(r) < deg(g) or r = 0.

### The Fundamental Theorem of Algebra

Every non-constant polynomial with complex coefficients has at least one complex root. Consequently, every degree-n polynomial over C factors completely into n linear factors (counted with multiplicity).

This theorem (proved by Gauss in his doctoral dissertation, 1799) explains why the complex numbers are algebraically closed — no further extension is needed to solve polynomial equations.

### Vieta's Formulas

For the polynomial a_n x^n + a_{n-1} x^{n-1} + ... + a_0 with roots r_1, ..., r_n:
- Sum of roots: r_1 + r_2 + ... + r_n = -a_{n-1}/a_n
- Sum of products of pairs: sum(r_i * r_j) = a_{n-2}/a_n
- Product of all roots: r_1 * r_2 * ... * r_n = (-1)^n * a_0/a_n

These relate coefficients to roots without solving the polynomial.

## Part VII — Inequalities

### Properties of Inequalities

- Adding the same quantity to both sides preserves direction.
- Multiplying by a positive number preserves direction.
- Multiplying by a negative number **reverses** direction. (The most common source of inequality errors.)
- Squaring both sides is valid only when both sides are non-negative.

### Key Inequalities

**AM-GM (Arithmetic Mean - Geometric Mean).** For non-negative reals a_1, ..., a_n:
(a_1 + a_2 + ... + a_n)/n >= (a_1 * a_2 * ... * a_n)^(1/n),
with equality iff all a_i are equal.

**Cauchy-Schwarz.** For real numbers a_i, b_i:
(sum a_i * b_i)^2 <= (sum a_i^2)(sum b_i^2),
with equality iff a_i/b_i is constant.

**Triangle Inequality.** |a + b| <= |a| + |b|, with equality iff a and b have the same sign (or one is zero).

**Worked example (AM-GM).** *Prove that for positive reals x and y, x/y + y/x >= 2.*

**Proof.** By AM-GM applied to x/y and y/x: (x/y + y/x)/2 >= sqrt((x/y)(y/x)) = sqrt(1) = 1. Multiply by 2: x/y + y/x >= 2. Equality holds iff x/y = y/x, i.e., x = y.

## When to Use This Skill

- Solving equations of any type (linear, quadratic, polynomial, systems)
- Simplifying or factoring algebraic expressions
- Working with modular arithmetic or number theory
- Proving algebraic identities or inequalities
- Analyzing algebraic structures (groups, rings, fields)

## When NOT to Use This Skill

- For geometric reasoning — use geometric-intuition instead
- For calculus-based computation (limits, derivatives, integrals) — use numerical-analysis
- For sequence discovery or conjecture generation — use pattern-recognition
- For real-world problem formulation — use mathematical-modeling

## Cross-References

- **gauss agent:** Systems of equations, Gaussian elimination, number theory applications. Primary agent for computational algebra.
- **noether agent:** Abstract algebraic structures, symmetry, ring and field theory. Named for Emmy Noether, whose work on abstract algebra and conservation laws transformed modern mathematics.
- **proof-techniques skill:** Proof methods used to establish algebraic results.
- **pattern-recognition skill:** Conjecture generation from algebraic patterns (e.g., discovering Vieta's formulas experimentally).
- **numerical-analysis skill:** Numerical root-finding when algebraic methods reach their limits.

## References

- Artin, M. (2011). *Algebra*. 2nd edition. Pearson.
- Axler, S. (2015). *Linear Algebra Done Right*. 3rd edition. Springer.
- Gauss, C. F. (1799). *Demonstratio nova theorematis omnem functionem algebraicam rationalem integram unius variabilis in factores reales primi vel secundi gradus resolvi posse*. Doctoral dissertation.
- Hardy, G. H., & Wright, E. M. (2008). *An Introduction to the Theory of Numbers*. 6th edition. Oxford University Press.
- Lang, S. (2002). *Algebra*. 3rd edition. Springer GTM 211.
- Strang, G. (2016). *Introduction to Linear Algebra*. 5th edition. Wellesley-Cambridge Press.
