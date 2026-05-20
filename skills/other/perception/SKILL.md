---
name: mfe-perception
description: "Foundational measurements and relationships. The axioms of the system — numbers, distance, angles, and the geometry of seeing."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "number"
          - "count"
          - "distance"
          - "magnitude"
          - "circle"
          - "trigonometric"
          - "angle"
          - "inner product"
          - "orthogonal"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Perception

## Summary

**Perception** (Part I: Seeing)
Chapters: 1, 2, 3
Plane Position: (-0.2, 0.2) radius 0.4
Primitives: 43

Foundational measurements and relationships. The axioms of the system — numbers, distance, angles, and the geometry of seeing.

**Key Concepts:** Sine Function, Cosine Function, Real Numbers, Unit Circle, Inner Product (Dot Product)

## Key Primitives



**Sine Function** (definition): The sine function sin: R -> [-1,1] is defined as the y-coordinate of the point on the unit circle at angle theta from the positive x-axis. It is periodic with period 2*pi, odd: sin(-theta) = -sin(theta).
  - computing vertical components of circular or oscillatory motion
  - modeling periodic phenomena like waves and vibrations

**Cosine Function** (definition): The cosine function cos: R -> [-1,1] is defined as the x-coordinate of the point on the unit circle at angle theta. It is periodic with period 2*pi, even: cos(-theta) = cos(theta). cos(theta) = sin(theta + pi/2).
  - computing horizontal components of circular or oscillatory motion
  - finding phase relationships between periodic signals

**Real Numbers** (definition): The real numbers R form a complete ordered field: closed under +, -, *, /, ordered by <, and satisfying the completeness axiom. R = Q union (R \ Q).
  - any calculation involving continuous quantities
  - measuring distances, areas, or physical quantities

**Unit Circle** (definition): The unit circle is the set of points (x, y) in R^2 satisfying x^2 + y^2 = 1. Every point on the unit circle can be written as (cos(theta), sin(theta)) for a unique angle theta in [0, 2*pi).
  - defining trigonometric functions geometrically
  - representing angles and rotations in the plane

**Inner Product (Dot Product)** (definition): The inner product (dot product) of vectors u = (u1,...,un) and v = (v1,...,vn) in R^n is u . v = sum_i u_i * v_i = |u||v|cos(theta), where theta is the angle between u and v.
  - computing the angle between two vectors
  - finding the component of one vector along another direction

**Natural Numbers** (axiom): The natural numbers N = {1, 2, 3, ...} satisfy the Peano axioms: there exists a first element 1, every element n has a unique successor S(n), no two elements share a successor, and the induction principle holds.
  - counting objects or elements in a set
  - establishing the basis for mathematical induction

**Pythagorean Theorem** (theorem): In a right triangle with legs a and b and hypotenuse c: a^2 + b^2 = c^2. Conversely, if a^2 + b^2 = c^2 for a triangle with sides a, b, c, then the triangle is right-angled.
  - computing the length of the hypotenuse in a right triangle
  - finding distance between two points in Euclidean space

**Complex Numbers** (definition): The complex numbers C = {a + bi : a, b in R, i^2 = -1} form an algebraically closed field. Every complex number has modulus |z| = sqrt(a^2 + b^2) and argument arg(z) = atan2(b, a).
  - representing quantities with both magnitude and phase
  - solving polynomial equations that have no real roots

**Absolute Value** (definition): For x in R, the absolute value |x| = x if x >= 0, |x| = -x if x < 0. Equivalently, |x| = sqrt(x^2). It measures the distance from x to 0 on the number line.
  - measuring distance from zero or between two numbers
  - bounding the size of a quantity regardless of sign

**Euler's Formula** (identity): For all theta in R: e^(i*theta) = cos(theta) + i*sin(theta). The special case theta = pi gives Euler's identity: e^(i*pi) + 1 = 0.
  - converting between trigonometric and exponential forms of complex numbers
  - simplifying products and powers of trigonometric expressions using exponentials

## Composition Patterns

- Integers + perception-natural-numbers -> Complete additive group with identity and inverses (sequential)
- Rational Numbers + perception-integers -> A number system where division is always defined (except by zero) (sequential)
- Irrational Numbers + perception-rational-numbers -> The complete real number line without gaps (parallel)
- Real Numbers + perception-real-line-completeness -> A number system where limits of convergent sequences always exist (nested)
- Complex Numbers + perception-unit-circle -> Polar form of complex numbers: z = r*e^(i*theta) (parallel)
- Absolute Value + perception-number-line -> Distance between two points on the line: |a - b| (sequential)
- Number Line + perception-absolute-value -> Metric space structure on R with distance d(a,b) = |a-b| (parallel)
- Density of Rationals + perception-real-line-completeness -> Understanding that Q is dense but not complete — R fills the gaps (parallel)
- Triangle Inequality for Absolute Value + perception-distance-formula -> Metric space axiom: d(a,c) <= d(a,b) + d(b,c) (sequential)
- Unit Circle + perception-complex-numbers -> Complex numbers of modulus 1: z = e^(i*theta) on the unit circle (parallel)

## Cross-Domain Links

- **waves**: Compatible domain for composition and cross-referencing
- **change**: Compatible domain for composition and cross-referencing
- **structure**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- number
- count
- distance
- magnitude
- circle
- trigonometric
- angle
- inner product
- orthogonal
