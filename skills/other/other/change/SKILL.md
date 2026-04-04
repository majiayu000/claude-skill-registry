---
name: mfe-change
description: "Calculus and continuous transformation — derivatives, integrals, ODEs, Taylor series, and optimization. Computes rates of change, accumulates quantities over intervals, solves differential equations, and classifies critical points. Use when computing derivatives or integrals, solving ordinary differential equations, performing Taylor series approximations, finding critical points, or analyzing continuous change and motion."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "derivative"
          - "integral"
          - "rate"
          - "differential"
          - "Taylor"
          - "optimization"
          - "limit"
          - "continuous"
          - "accumulation"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Change

Part III: Moving — Chapters 8, 9, 10 — Plane Position: (0, -0.2) radius 0.4 — 58 Primitives

## Workflow

1. **Verify continuity** at the point or interval of interest — confirm the function meets the three conditions (defined, limit exists, limit equals value)
2. **Compute derivatives** using the appropriate rule (power, chain, product, quotient) to find rates of change
3. **Find critical points** where f'(x) = 0 or f'(x) is undefined, then classify using the first or second derivative test
4. **Integrate** using antiderivatives and the Fundamental Theorem of Calculus to accumulate quantities
5. **Solve ODEs** by identifying the equation type and applying the matching technique (separation, integrating factor, etc.)

## Key Concepts

**Derivative** (definition): The derivative of f at x is f'(x) = lim_{h->0} [f(x+h) - f(x)]/h, when this limit exists. It represents the instantaneous rate of change of f at x, and the slope of the tangent line to the graph at (x, f(x)).
  - computing the instantaneous rate of change of a quantity
  - finding the slope of a curve at a specific point

**Definite Integral** (definition): The definite integral of f from a to b is integral_a^b f(x)dx = lim_{n->inf} sum_{i=1}^{n} f(x_i*)*Delta_x, when this limit exists. It represents the signed area between f and the x-axis over [a,b].
  - computing the total accumulation of a quantity over an interval
  - finding the area enclosed between a curve and the x-axis

**Ordinary Differential Equation** (definition): An ordinary differential equation (ODE) is an equation involving a function y(x) and its derivatives: F(x, y, y', y'', ..., y^(n)) = 0. The order is the highest derivative present. A solution is a function that satisfies the equation on an interval.
  - modeling systems where the rate of change depends on the current state
  - describing physical laws relating a quantity to its derivatives

**Limit** (definition): The limit of f(x) as x approaches a is L, written lim_{x->a} f(x) = L, if for every epsilon > 0 there exists delta > 0 such that 0 < |x - a| < delta implies |f(x) - L| < epsilon.
  - finding the value a function approaches near a point where it may not be defined
  - establishing the foundation for derivatives and integrals

**Continuity** (definition): A function f is continuous at a point a if: (1) f(a) is defined, (2) lim_{x->a} f(x) exists, and (3) lim_{x->a} f(x) = f(a). f is continuous on an interval if continuous at every point in the interval.
  - verifying that a function has no jumps or breaks at a point
  - determining the domain on which a function is well-behaved for calculus

**Higher-Order Derivatives** (definition): The nth derivative f^(n)(x) is obtained by differentiating f n times. f''(x) = d^2f/dx^2 (acceleration, concavity). f^(n)(x) = d^n f/dx^n. A function is C^n if its first n derivatives are continuous.
  - computing acceleration as the second derivative of position
  - determining concavity and inflection points of curves

**Critical Point** (definition): A critical point of f is a value c in the domain of f where f'(c) = 0 or f'(c) does not exist. Critical points are candidates for local maxima, local minima, or inflection points.
  - finding where a function might achieve its maximum or minimum value
  - locating turning points of a curve

**Antiderivative (Indefinite Integral)** (definition): An antiderivative of f is a function F such that F'(x) = f(x). The indefinite integral integral f(x)dx = F(x) + C represents the family of all antiderivatives, where C is an arbitrary constant.
  - finding a function whose derivative is a given function
  - reversing differentiation to recover original functions

**Power Rule** (theorem): For any real number n: d/dx(x^n) = n*x^(n-1). This holds for integer, rational, and real exponents (where the function is defined).
  - differentiating polynomial terms and power functions
  - finding the derivative of any expression of the form x^n

**Chain Rule** (theorem): If g is differentiable at x and f is differentiable at g(x), then the composite function f(g(x)) is differentiable at x with: d/dx[f(g(x))] = f'(g(x)) * g'(x).
  - differentiating compositions of functions like sin(x^2) or e^(3x)
  - computing rates of change through connected relationships

## Composition Patterns

- Limit + perception-real-line-completeness -> Foundation for epsilon-delta analysis: the limit exists because R is complete (nested)
- Continuity + change-limit -> The no-surprises condition: the limit equals the function value (sequential)
- Derivative + change-fundamental-theorem-2 -> The fundamental connection: differentiation and integration are inverse operations (parallel)
- Differentiability + change-continuity -> Hierarchy: differentiable => continuous => defined (each implication is strict) (sequential)
- Higher-Order Derivatives + change-taylor-series -> Taylor coefficients: f(x) ~ sum f^(n)(a)/n! * (x-a)^n, each coefficient from an nth derivative (sequential)
- Critical Point + change-first-derivative-test -> Complete local extremum classification: find critical points then test sign changes (sequential)
- Inflection Point + change-critical-point -> Complete curve analysis: critical points for extrema, inflection points for concavity changes (parallel)
- Power Rule + change-chain-rule -> Generalized power rule: d/dx(f(x)^n) = n*f(x)^(n-1)*f'(x) (nested)
- Chain Rule + change-power-rule -> d/dx[f(x)]^n = n[f(x)]^(n-1) * f'(x) (nested)
- Product Rule + change-quotient-rule -> Complete toolkit for differentiating rational expressions (parallel)

## Cross-Domain Links

- **perception**: Compatible domain for composition and cross-referencing
- **waves**: Compatible domain for composition and cross-referencing
- **structure**: Compatible domain for composition and cross-referencing
- **emergence**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- derivative
- integral
- rate
- differential
- Taylor
- optimization
- limit
- continuous
- accumulation
