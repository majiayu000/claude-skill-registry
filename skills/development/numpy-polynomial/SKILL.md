---
name: numpy-polynomial
description: 'Modern polynomial API for fitting, root finding, and working with orthogonal
  series like Chebyshev and Legendre. Triggers: polynomial, polyfit, Chebyshev, Legendre,
  root finding.'
---

---
name: numpy-polynomial
description: Modern polynomial API for fitting, root finding, and working with orthogonal series like Chebyshev and Legendre. Triggers: polynomial, polyfit, Chebyshev, Legendre, root finding.
---

## Overview
NumPy's `polynomial` package provides a modern, class-based API for handling power series. It replaces the legacy `poly1d` conventions with objects that handle domain scaling, root finding, and advanced orthogonal polynomials (Chebyshev, Legendre) for numerical stability.

## When to Use
- Fitting a curve to noisy experimental data using least-squares.
- Finding the zeros (roots) of a mathematical function approximated by a polynomial.
- Performing high-precision function approximation using Chebyshev series.
- Computing integrals or derivatives of polynomial models.

## Decision Tree
1. Creating a new polynomial from coefficients?
   - Use `Polynomial([c0, c1, c2])`. Note: coefficients are in **increasing** degree.
2. Fitting data?
   - Use `Polynomial.fit(x, y, deg)`. It automatically scales the domain for stability.
3. Need to evaluate the fit?
   - Use the returned object directly: `p(x)`.

## Workflows
1. **Stable Data Fitting**
   - Identify noisy data (x, y).
   - Use `p = Polynomial.fit(x, y, deg=3)` to find the best fit.
   - Evaluate the model over a range using `p.linspace()` to visualize the result.

2. **Polynomial Root Finding**
   - Define coefficients `[c0, c1, c2]` (constant, linear, quadratic).
   - Instantiate the polynomial: `p = Polynomial(coefs)`.
   - Call `p.roots()` to find the values of x where `p(x) = 0`.

3. **Orthogonal Series Interpolation**
   - Import the `Chebyshev` class.
   - Use `Chebyshev.interpolate(func, deg)` to create a series that matches a function at Chebyshev points.
   - Utilize the resulting object for high-precision function approximation.

## Non-Obvious Insights
- **Increasing Degree:** The modern API uses coefficients in order (0, 1, 2...), reversing the `poly1d` convention (highest degree first). This is a common source of bugs during migration.
- **Domain Scaling:** `Polynomial.fit()` maps the input $x$ values to a internal window (usually $[-1, 1]$). Evaluating using `p.convert().coef` directly on raw $x$ values without scaling will fail; always use the class instance `p(x)`.
- **Arithmetic Restrictions:** Polynomials with different domain or window attributes cannot be mixed in arithmetic operations; they must be converted to a shared domain first.

## Evidence
- "The various routines in numpy.polynomial all deal with series whose coefficients go from degree zero upward, which is the reverse order of the poly1d convention." [Source](https://numpy.org/doc/stable/reference/routines.polynomials.html)
- "Polynomials with different domain and window attributes are not considered equal, and can’t be mixed in arithmetic." [Source](https://numpy.org/doc/stable/reference/routines.polynomials.html)

## Scripts
- `scripts/numpy-polynomial_tool.py`: Implements curve fitting and root finding using the modern API.
- `scripts/numpy-polynomial_tool.js`: Simulated polynomial evaluator logic.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)