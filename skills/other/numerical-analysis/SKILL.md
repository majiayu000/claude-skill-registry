---
name: numerical-analysis
description: Calculus, series, numerical methods, and optimization for computational mathematics. Covers limits (epsilon-delta, L'Hopital, squeeze theorem), derivatives (rules, optimization, related rates), integrals (Riemann sums, Fundamental Theorem of Calculus, integration techniques), series (convergence tests, Taylor and Maclaurin expansions), differential equations (separable, linear, exact), numerical methods (Newton-Raphson, Euler method, Simpson's rule), and computational pitfalls (floating-point arithmetic, catastrophic cancellation, numerical stability). Use when computing derivatives, integrals, limits, series, solving differential equations, or analyzing numerical accuracy.
type: skill
category: math
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/math/numerical-analysis/SKILL.md
superseded_by: null
---
# Numerical Analysis

Calculus and numerical methods form the computational backbone of applied mathematics. Calculus provides exact analytical tools — limits, derivatives, integrals, series — while numerical methods provide approximate algorithms for problems where exact solutions are unavailable or impractical. This skill covers both the analytical foundations and the computational techniques, including the pitfalls that arise when mathematics meets finite-precision arithmetic.

**Agent affinity:** euler (series, differential equations, numerical methods)

**Concept IDs:** math-computational-fluency, math-functions, math-expected-value, math-descriptive-statistics

## Part I — Limits

### The Epsilon-Delta Definition

A function f(x) has limit L as x approaches a (written lim_{x->a} f(x) = L) if for every epsilon > 0, there exists delta > 0 such that whenever 0 < |x - a| < delta, we have |f(x) - L| < epsilon.

This definition — due to Weierstrass, formalizing Cauchy's intuition — is the foundation of rigorous analysis. Every subsequent concept in calculus (continuity, derivatives, integrals) is built on limits.

**Worked example.** *Prove that lim_{x->3} (2x + 1) = 7.*

**Proof.** Let epsilon > 0 be given. We need |f(x) - 7| < epsilon whenever 0 < |x - 3| < delta. Compute: |(2x + 1) - 7| = |2x - 6| = 2|x - 3|. Choose delta = epsilon/2. Then 0 < |x - 3| < delta implies |f(x) - 7| = 2|x - 3| < 2(epsilon/2) = epsilon.

### Limit Laws

For lim_{x->a} f(x) = L and lim_{x->a} g(x) = M:
- Sum: lim(f + g) = L + M
- Product: lim(f * g) = L * M
- Quotient: lim(f / g) = L / M (when M != 0)
- Composition: lim f(g(x)) = f(M) if f is continuous at M

### L'Hopital's Rule

If lim_{x->a} f(x)/g(x) yields an indeterminate form (0/0 or infinity/infinity), and the limit of f'(x)/g'(x) exists, then:

lim_{x->a} f(x)/g(x) = lim_{x->a} f'(x)/g'(x)

**Worked example.** *Compute lim_{x->0} sin(x)/x.*

Direct substitution gives 0/0. Apply L'Hopital: lim_{x->0} cos(x)/1 = cos(0) = 1.

**When NOT to use.** L'Hopital requires an indeterminate form. Applying it to a determinate form (e.g., a nonzero numerator with zero denominator) gives wrong results.

### The Squeeze Theorem

If g(x) <= f(x) <= h(x) near a, and lim g(x) = lim h(x) = L, then lim f(x) = L.

**Worked example.** *Prove lim_{x->0} x^2 * sin(1/x) = 0.*

Since -1 <= sin(1/x) <= 1, we have -x^2 <= x^2 sin(1/x) <= x^2. Both -x^2 and x^2 approach 0, so by the squeeze theorem, the limit is 0.

## Part II — Derivatives

### Definition and Rules

The derivative of f at x = a is f'(a) = lim_{h->0} (f(a + h) - f(a)) / h, when this limit exists. It measures the instantaneous rate of change.

**Differentiation rules:**

| Rule | Formula |
|---|---|
| Power | d/dx [x^n] = n*x^(n-1) |
| Sum | (f + g)' = f' + g' |
| Product | (f*g)' = f'*g + f*g' |
| Quotient | (f/g)' = (f'*g - f*g') / g^2 |
| Chain | d/dx [f(g(x))] = f'(g(x)) * g'(x) |
| Exponential | d/dx [e^x] = e^x |
| Logarithm | d/dx [ln(x)] = 1/x |
| Trig | d/dx [sin(x)] = cos(x), d/dx [cos(x)] = -sin(x) |

### Applications of Derivatives

**Optimization.** Find critical points where f'(x) = 0 or f'(x) is undefined. Use the second derivative test: f''(c) > 0 means local minimum, f''(c) < 0 means local maximum, f''(c) = 0 is inconclusive.

**Worked example.** *Find the dimensions of a rectangle with perimeter 20 that maximizes area.*

Let the sides be x and y with 2x + 2y = 20, so y = 10 - x. Area A = x(10 - x) = 10x - x^2. Then A'(x) = 10 - 2x = 0 gives x = 5, y = 5. A''(x) = -2 < 0, confirming a maximum. The optimal rectangle is a 5 x 5 square with area 25.

**Related rates.** When two or more quantities change with time, differentiate their relationship implicitly with respect to time.

**Mean Value Theorem.** If f is continuous on [a, b] and differentiable on (a, b), then there exists c in (a, b) with f'(c) = (f(b) - f(a)) / (b - a). This theorem is the foundation for many proofs in analysis.

## Part III — Integration

### Riemann Sums and the Definite Integral

The definite integral from a to b of f(x)dx is defined as the limit of Riemann sums:

integral_a^b f(x)dx = lim_{n->infinity} sum_{i=1}^{n} f(x_i*) * Delta_x

where Delta_x = (b - a)/n and x_i* is a sample point in the i-th subinterval.

### The Fundamental Theorem of Calculus

**Part 1 (FTC1).** If f is continuous on [a, b], then F(x) = integral_a^x f(t)dt is differentiable and F'(x) = f(x). Integration and differentiation are inverse operations.

**Part 2 (FTC2).** If F is any antiderivative of f on [a, b], then integral_a^b f(x)dx = F(b) - F(a).

### Integration Techniques

**Substitution (u-substitution).** For integral f(g(x)) * g'(x) dx, let u = g(x), du = g'(x)dx.

**Worked example.** *Compute integral 2x * cos(x^2) dx.*

Let u = x^2, du = 2x dx. The integral becomes integral cos(u) du = sin(u) + C = sin(x^2) + C.

**Integration by parts.** integral u dv = uv - integral v du. Choose u and dv using the LIATE heuristic: Logarithmic, Inverse trig, Algebraic, Trigonometric, Exponential — u should be the type appearing earliest in this list.

**Worked example.** *Compute integral x * e^x dx.*

Let u = x (algebraic), dv = e^x dx. Then du = dx, v = e^x. By parts: x*e^x - integral e^x dx = x*e^x - e^x + C = e^x(x - 1) + C.

**Partial fractions.** Decompose a rational function into simpler fractions before integrating. Factor the denominator, then express as a sum of fractions with linear and irreducible quadratic denominators.

**Trigonometric substitution.** For integrands involving sqrt(a^2 - x^2), sqrt(a^2 + x^2), or sqrt(x^2 - a^2), substitute x = a*sin(theta), x = a*tan(theta), or x = a*sec(theta) respectively.

## Part IV — Series

### Convergence Tests

A series sum_{n=1}^{infinity} a_n converges if the sequence of partial sums S_N = sum_{n=1}^{N} a_n has a finite limit.

| Test | Statement | Use when |
|---|---|---|
| **Divergence** | If lim a_n != 0, the series diverges | Quick first check |
| **Geometric** | sum r^n converges iff |r| < 1, to 1/(1-r) | Series is geometric |
| **p-series** | sum 1/n^p converges iff p > 1 | Power-law terms |
| **Integral** | sum a_n and integral f(x)dx converge/diverge together | f is positive, decreasing, continuous |
| **Comparison** | 0 <= a_n <= b_n and sum b_n converges => sum a_n converges | Can bound by a known series |
| **Limit comparison** | lim a_n/b_n = L (0 < L < infinity) => same behavior | Asymptotic comparison |
| **Ratio** | lim |a_{n+1}/a_n| < 1 => converges, > 1 => diverges | Factorial or exponential terms |
| **Root** | lim |a_n|^{1/n} < 1 => converges, > 1 => diverges | n-th power terms |
| **Alternating series** | sum (-1)^n b_n converges if b_n decreases to 0 | Alternating sign |

### Taylor and Maclaurin Series

The Taylor series of f about x = a is:

f(x) = sum_{n=0}^{infinity} f^(n)(a) / n! * (x - a)^n

The Maclaurin series is the Taylor series about a = 0.

**Key Maclaurin series:**

| Function | Series | Radius of convergence |
|---|---|---|
| e^x | sum x^n / n! | infinity |
| sin(x) | sum (-1)^n x^(2n+1) / (2n+1)! | infinity |
| cos(x) | sum (-1)^n x^(2n) / (2n)! | infinity |
| 1/(1-x) | sum x^n | 1 |
| ln(1+x) | sum (-1)^(n+1) x^n / n | 1 |
| arctan(x) | sum (-1)^n x^(2n+1) / (2n+1) | 1 |

**Taylor's remainder theorem.** If f has n+1 continuous derivatives on an interval containing a and x, then:

f(x) = P_n(x) + R_n(x)

where P_n is the n-th degree Taylor polynomial and |R_n(x)| <= M * |x - a|^(n+1) / (n+1)! for M = max |f^(n+1)(t)| on the interval. This bounds the approximation error.

## Part V — Differential Equations

### Separable Equations

Form: dy/dx = f(x) * g(y). Separate: dy/g(y) = f(x) dx. Integrate both sides.

**Worked example.** *Solve dy/dx = xy, y(0) = 1.*

Separate: dy/y = x dx. Integrate: ln|y| = x^2/2 + C. Exponentiate: y = A * e^(x^2/2). Initial condition y(0) = 1 gives A = 1. Solution: y = e^(x^2/2).

### First-Order Linear Equations

Form: dy/dx + P(x)*y = Q(x). Multiply by integrating factor mu(x) = e^(integral P(x) dx):

d/dx [mu(x) * y] = mu(x) * Q(x)

Integrate both sides to solve.

**Worked example.** *Solve dy/dx + 2y = e^(-x), y(0) = 3.*

Integrating factor: mu = e^(2x). Multiply: d/dx [e^(2x) y] = e^(2x) * e^(-x) = e^x. Integrate: e^(2x) y = e^x + C. So y = e^(-x) + C * e^(-2x). Initial condition: 3 = 1 + C, so C = 2. Solution: y = e^(-x) + 2e^(-2x).

### Exact Equations

Form: M(x,y) dx + N(x,y) dy = 0 is exact if dM/dy = dN/dx. Then there exists F(x,y) with dF/dx = M and dF/dy = N. The solution is F(x,y) = C.

### Second-Order Linear with Constant Coefficients

Form: ay'' + by' + cy = 0. The characteristic equation ar^2 + br + c = 0 yields:
- Two distinct real roots r_1, r_2: y = C_1 e^(r_1 x) + C_2 e^(r_2 x)
- Repeated root r: y = (C_1 + C_2 x) e^(rx)
- Complex roots alpha +/- beta*i: y = e^(alpha x) (C_1 cos(beta x) + C_2 sin(beta x))

## Part VI — Numerical Methods

### Newton-Raphson Method

To find a root of f(x) = 0, iterate: x_{n+1} = x_n - f(x_n) / f'(x_n).

**Convergence:** Quadratic when it converges (errors square each iteration). Requires f'(x_n) != 0 and a sufficiently good initial guess.

**Worked example.** *Approximate sqrt(2) as a root of f(x) = x^2 - 2.*

f'(x) = 2x. Starting at x_0 = 1:
x_1 = 1 - (1 - 2)/(2) = 1.5
x_2 = 1.5 - (2.25 - 2)/(3) = 1.5 - 0.0833... = 1.41667
x_3 = 1.41667 - (2.00694 - 2)/(2.83333) = 1.41422

After 3 iterations, we have 5 correct digits.

**Failure modes.** Diverges when the initial guess is near a stationary point (f' near 0), near an inflection point, or when the function oscillates. Always verify convergence.

### Euler's Method

For dy/dx = f(x, y) with y(x_0) = y_0, approximate: y_{n+1} = y_n + h * f(x_n, y_n), where h is the step size.

**Error.** Global error is O(h) — first-order method. Halving the step size halves the error but doubles the work.

**Improved Euler (Heun's method).** Use the average of slopes at the start and end of each step. Global error is O(h^2).

**Runge-Kutta (RK4).** The workhorse of ODE solvers. Fourth-order accuracy (global error O(h^4)) with four function evaluations per step. The standard formulas:

k_1 = h * f(x_n, y_n)
k_2 = h * f(x_n + h/2, y_n + k_1/2)
k_3 = h * f(x_n + h/2, y_n + k_2/2)
k_4 = h * f(x_n + h, y_n + k_3)
y_{n+1} = y_n + (k_1 + 2*k_2 + 2*k_3 + k_4) / 6

### Simpson's Rule

For numerical integration: integral_a^b f(x) dx approximately equals (h/3) [f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + ... + 4f(x_{n-1}) + f(x_n)], where h = (b - a)/n and n is even.

**Error bound.** |E_S| <= M * (b - a)^5 / (180 * n^4), where M = max |f^(4)(x)| on [a, b]. Fourth-order accuracy — far superior to the trapezoidal rule (O(n^2)) for smooth functions.

## Part VII — Computational Pitfalls

### Floating-Point Arithmetic

IEEE 754 double-precision floating point provides about 15-16 significant decimal digits. Every floating-point operation introduces a rounding error of relative magnitude at most epsilon_machine approximately 2.2e-16.

### Catastrophic Cancellation

When two nearly equal numbers are subtracted, leading significant digits cancel and the result retains only the trailing (noisy) digits. Example: computing f(x) = (1 - cos(x)) / x^2 near x = 0 suffers catastrophic cancellation because both 1 and cos(x) are near 1.

**Fix:** Use the identity 1 - cos(x) = 2*sin^2(x/2), so f(x) = 2*sin^2(x/2)/x^2 = (sin(x/2)/(x/2))^2 / 2, which is numerically stable.

### Numerical Stability

An algorithm is **numerically stable** if small perturbations in the input produce small perturbations in the output. An **unstable** algorithm amplifies errors.

**Example.** Forward recurrence for the integral I_n = integral_0^1 x^n * e^(x-1) dx using I_n = 1 - n*I_{n-1} is unstable (errors grow by factor n). Backward recurrence from a large N down is stable.

### Conditioning

The **condition number** kappa(A) of a matrix A measures how sensitive Ax = b is to perturbations in A or b. For linear systems: relative error in x <= kappa(A) * relative error in b. When kappa(A) is large, the problem is ill-conditioned and even a stable algorithm produces inaccurate results.

## When to Use This Skill

- Computing limits, derivatives, or integrals (exact or numerical)
- Solving differential equations (exact or numerical)
- Analyzing series convergence and computing Taylor approximations
- Performing optimization (finding maxima/minima)
- Assessing numerical accuracy and stability of computations

## When NOT to Use This Skill

- For algebraic equation solving without calculus — use algebraic-reasoning
- For geometric reasoning — use geometric-intuition
- For conjecture generation from patterns — use pattern-recognition
- For real-world problem formulation — use mathematical-modeling (though this skill handles the computational engine once the model is formulated)

## Cross-References

- **euler agent:** Differential equations, series, numerical methods, and connections between analysis and computation. Named for Leonhard Euler, the most prolific mathematician in history, who contributed foundationally to calculus, series theory, and numerical methods.
- **algebraic-reasoning skill:** Algebraic manipulation used in integration, differential equations, and series computation.
- **geometric-intuition skill:** Geometric interpretation of derivatives (tangent lines), integrals (area under curves), and series (geometric series).
- **mathematical-modeling skill:** Formulating real-world problems that this skill then solves computationally.

## References

- Rudin, W. (1976). *Principles of Mathematical Analysis*. 3rd edition. McGraw-Hill.
- Spivak, M. (2008). *Calculus*. 4th edition. Publish or Perish.
- Stewart, J. (2015). *Calculus: Early Transcendentals*. 8th edition. Cengage.
- Burden, R. L., & Faires, J. D. (2010). *Numerical Analysis*. 9th edition. Brooks/Cole.
- Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*. 2nd edition. SIAM.
- Goldberg, D. (1991). "What every computer scientist should know about floating-point arithmetic." *ACM Computing Surveys*, 23(1), 5-48.
